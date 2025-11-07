import numpy as np
import math
from scipy.special import stirling2

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
