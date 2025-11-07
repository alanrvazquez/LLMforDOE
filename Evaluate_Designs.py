import numpy as np
import pandas as pd      
import matplotlib.pyplot as plt  
import seaborn as sns 
from FrF2 import *

# Define the columns of the DataFrame
columns = ['Replicate', 'Runs', 'Factors', 'Resolution', 'MA']

df = pd.DataFrame(columns=columns)
citer = 0 
for ii in range(1, 6):

  read_file = "numpy_results/parsed_responses_n32_replicate" + str(ii) + ".npy"
  designs = np.load(read_file, allow_pickle=True)
  
  for j in range(len(designs)):
    
    des = designs[j]
    D = np.delete(des, 0, axis = 1)
  
    N, n = np.shape(D)
    
    if N == 32:
    
      # Resolution
      R = resolution(D)
      
      # Moment aberration
      MApattern = moment_aberration(D)
      
      df.loc[citer] = [ii, N, n, R, MApattern.round(decimals = 3)]
  
      citer = citer + 1

# Number of feasible designs
(df
.sort_values('Factors')
.groupby(["Runs", "Factors"])
.count()
)

# Evaluation in terms of resolution  
(df
.groupby(["Runs", "Factors"])
.agg(Min = ("Resolution", "min"),
     Median = ("Resolution", "median"),
     Max = ("Resolution", "max"))
)

## Select best designs in terms of the resolution
best_designs = (df
                .query("Resolution >= 4")
                .filter(["Factors", "MA"])
                .sort_values('Factors')
                )

MA_pattern = (best_designs
.query("Factors == 6")
.filter(['MA'])
)

MA_pattern.to_string()
