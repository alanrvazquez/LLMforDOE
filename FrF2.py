import numpy as np
import math
from scipy.special import stirling2
import pandas as pd
import io
import re
from datetime import datetime

## Classes
class LLMDesign(object):
    def __init__(self, D, n, N, R, MA, rrankX, cMEs, cIEs):
        self.design = D
        self.nFactors = n
        self.nRuns = N
        self.resolution = R
        self.momentaberration = MA
        self.rank = rrankX
        self.clearMEs = cMEs
        self.clearIEs = cIEs

## Functions

def moment_aberration(D):
  
  N, n = np.shape(D)
  
  T = np.zeros((N, N))
  
  for i in range(N):
    for j in range(N):
      T[i,j] = np.sum(D[i,:]*D[j,:] > 0) 
  
  aux_cnst = N*(N-1)/2
  deltaMat = np.triu(T, 1)
  Kt = np.zeros((n, 1))
  for t in range(1, n+1):
    Kt[t-1] = np.sum(deltaMat**t)/aux_cnst
  
  return Kt

def KtLowerBound(N, n, t):
  aux_sum = np.zeros((t+1,1))
  for k in range(t+1):
    aux_cnst = 0
    for j in range(k+1):
      aux_cnst = aux_cnst + math.factorial(j)*(2**(-j))*(math.comb(n,j))*stirling2(k, j)
      
    aux_sum[k] = ((-1)**k)*(n**(t-k))*(math.comb(t,k))*aux_cnst
      
  return (N/(N-1))*np.sum(aux_sum) - (n**t)/(N-1)


def resolution(D, tol = 0.00000001):
  
  N, n = np.shape(D)
  Kt_vec = moment_aberration(D)  
  resolution = n
  for t in range(1,n+1):
    check = abs(Kt_vec[t-1] - KtLowerBound(N, n, t))
    
    if check > tol:
      resolution = t
      break
    
  return resolution  

def interaction_matrix(D, N, n):
  
  nIE = int(n*(n-1)/2)
  Xtwo = np.zeros((N, nIE))
  
  citer = 0
  for i in range(n-1):
    for j in range(i+1, n):
      Xtwo[:,citer] = D[:,i]*D[:,j]
      citer = citer + 1
      
  return Xtwo    

def rankX(D):
  
  N, n = np.shape(D)
  
  nIE = int(n*(n-1)/2)
  Xtwo = interaction_matrix(D, N, n)
  
  Xfull = np.concatenate((D, Xtwo), axis = 1)

  rankXfull = np.linalg.matrix_rank(Xfull)
  rankXtwo = np.linalg.matrix_rank(Xtwo)
  
  return rankXfull, rankXtwo


def aliasmatrix(Xone, Xtwo):
  
  XoneXone = np.matmul(Xone.T, Xone)
  Partone = np.linalg.inv(XoneXone)
  Parttwo = np.matmul(Xone.T, Xtwo)
  A = np.matmul(Partone, Parttwo)
  
  return A  
  #if linalg.cond(XoneXone) < 1/sys.float_info.epsilon:


def find_clear_MEs(D):

  # Calculate minimum moment aberration.
  N, n = np.shape(D)
  
  # Calculate interaction matrix
  Xtwo = interaction_matrix(D, N, n)

  # Compute alias matrix
  A = aliasmatrix(D, Xtwo)
  clearME = np.sum(np.sum(A != 0, 1) == 0)
      
  return clearME

def find_clear_INTs(D):

  # Calculate minimum moment aberration.
  N, n = np.shape(D)
  
  # Calculate interaction matrix
  Xtwo = interaction_matrix(D, N, n)

  nIE = int(n*(n-1)/2)
  
  clearIEs = []
  for i in range(nIE):
    Xs = Xtwo[:,i].reshape((N,1))
    remaining_cols = np.delete(Xtwo, i, axis=1)
    effects_matrix = np.concatenate((D, remaining_cols), axis = 1)
    A = aliasmatrix(Xs, effects_matrix)
    clearIE = np.sum(np.sum(A != 0, 1) == 0)
    
    if clearIE == 1:
      
      clearIEs.append(i)

  nClearIEs = len(clearIEs)
  return nClearIEs

##### FUNCTIONS FOR READING DESIGNS

# Parser for embedded CSV tables
def parse_embedded_csv(response_str):
    if pd.isna(response_str):
        return None

    # Step 1: Remove code block markers and strip whitespace
    cleaned = response_str.replace("```csv", "").replace("```", "").strip()

    # Step 2: Split lines, clean trailing backslashes
    lines = [re.sub(r'\\$', '', line.strip()) for line in cleaned.split('\n') if line.strip()]
    if len(lines) < 2:
        return None

    # Step 3: Normalize whitespace and remove leading commas
    lines = [','.join([col.strip() for col in line.split(',')]) for line in lines]

    # Step 4: Validate column count
    header = lines[0].split(',')
    expected_cols = len(header)
    valid_data_rows = [row for row in lines[1:] if len(row.split(',')) == expected_cols]
    if not valid_data_rows:
        return None

    # Rebuild CSV content
    cleaned_csv = '\n'.join([','.join(header)] + valid_data_rows)

    try:
        df_parsed = pd.read_csv(io.StringIO(cleaned_csv))
        return df_parsed.to_numpy()
    except Exception as e:
        print("Failed to parse response:\n", cleaned_csv)
        return None

# Normalize responses that look like CSV tables but lack code markers
def enforce_csv_block(response):
    if pd.isna(response):
        return response

    # Fix mislabeled or missing block types
    response = re.sub(r'```(plaintext|text|tsv)', '```csv', response, flags=re.IGNORECASE)

    # If already wrapped with a block marker, leave as-is
    if "```csv" in response:
        return response

    # If it appears to be a CSV-like table (e.g., lines with commas and starting with digits or commas), wrap it
    if re.search(r"^\s*[,0-9]+\s*,", response.strip(), re.MULTILINE):
        return f"```csv\n{response.strip()}\n```"
      
    # If response has text
    if "sorry" in response:
        return None      

    return response


