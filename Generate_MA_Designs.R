library(FrF2)
source("DoE_functions.R")

n = 32

for (k in 5:15){
  my.design = FrF2(n, k)
  D = desnum(my.design)
  print(round(moment_aberration(D), 3))
}

n = 32
k = 18
my.design = FrF2(n, k)
D = desnum(my.design)
MA = moment_aberration(D)
for (i in 1:length(MA)){
  print(MA[i])  
}
save.file.name = paste("MA_designs/MA_n", n, "_k", k, ".csv", sep = '')
write.table(D, file = save.file.name, 
            col.names = FALSE, row.names = FALSE, sep = ',')
