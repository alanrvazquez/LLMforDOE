import pandas as pd
import numpy as np
import io
import re
from datetime import datetime
from FrF2 import *

# Load folder
llm = "gemini"

# Set up information
nRunsize = 32
nReplicates = 10
nFactors = min(nRunsize-1, 26) - int(np.log2(nRunsize))

# Define the columns of the DataFrame
columns = ['TaskID', 'Replicate', 'Runs', 'Factors', 'Resolution', 'MA']

des_evaluation = pd.DataFrame(columns=columns)

# Compile and evaluate arrays
citer = 0
for ii in range(nReplicates):
  
    df = pd.read_csv(f"{llm}_results/responses_{llm}_n{nRunsize}_replicate{ii+1}.csv")

    df['Response'] = df['Response'].apply(enforce_csv_block)

    # Apply parser to each response
    df['ParsedResponse'] = df['Response'].apply(parse_embedded_csv)
    
    for jj in range(nFactors):
    
        # Filter valid arrays
        des = df['ParsedResponse'][jj]
        
        if np.any(des):
            
            D = np.delete(des, 0, axis = 1)
          
            N, n = np.shape(D)
            
            # Resolution
            R = resolution(D)
            
            # Moment aberration
            MApattern = moment_aberration(D)
            
            des_evaluation.loc[citer] = [df['TaskID'][jj], ii+1, N, n, R, MApattern.round(decimals = 3)]
            citer = citer + 1

des_evaluation.to_excel(f"evaluation_results/n{nRunsize}_{llm}.xlsx", index=False)
des_evaluation
# Number of feasible designs
(des_evaluation
.sort_values('Factors')
.groupby(["Runs", "Factors"])
.count()
)

# Evaluation in terms of resolution  
(des_evaluation
.groupby(["Runs", "Factors"])
.agg(Min = ("Resolution", "min"),
     Median = ("Resolution", "median"),
     Max = ("Resolution", "max"))
)

## Read MA designs

# Define the columns of the DataFrame

MAcolumns = ['Runs', 'Factors', 'Resolution', 'MA']
MAEvaluation = pd.DataFrame(columns=MAcolumns)

factor_list = [6, 7, 8, 9, 10, 12, 14, 15, 17, 18]
citer = 0
for jj in factor_list:

    MAdes = np.loadtxt(f'MA_designs/MA_n32_k{jj}.csv', delimiter=',')

    N, n = np.shape(MAdes)
    
    # Resolution
    R = resolution(MAdes)
    
    # Moment aberration
    MApattern = moment_aberration(MAdes)
    
    MAEvaluation.loc[citer] = [N, n, R, MApattern.round(decimals = 3)]
    citer = citer + 1

nRunsize = 32
MAEvaluation.to_excel(f"evaluation_results/MA_designs_n{nRunsize}.xlsx", index=False)
moment_aberration(MAdes)
MAEvaluation
