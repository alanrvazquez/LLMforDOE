###############################################################
# CODE TO EVALUATE DESIGNS 
#
# Authors: Marco V. Charles-Gonzalez and Alan R. Vazquez
# Affiliation: Tecnologico de Monterrey
#
###############################################################

import pandas as pd
import numpy as np
import io
import re
from datetime import datetime
from FrF2 import *

# Load folder ("gemini" or "gpt")
llm = "gemini"

# Set up information
nRunsize = 8
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

