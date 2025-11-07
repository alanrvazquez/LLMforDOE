library(kStatistics) # for Stirling numbers

moment_aberration = function(D){
  
  N = nrow(D)
  n = ncol(D)
  
  Tmat = matrix(NA, ncol = N, nrow = N)
  
  for (i in 1:(N-1)){
    for (j in (i+1):N){
      Tmat[i,j] = sum(D[i,]*D[j,] > 0)
    }
    
  }
  
  aux_cnst = N*(N-1)/2
  
  Kt = rep(NA, times = n)
  for (t in 1:n){
    Kt[t] = sum(Tmat**t, na.rm = TRUE)/aux_cnst  
  }
  
  return(Kt)
}

KtLowerBound = function(N, n, t){
  
  aux_sum = rep(0, times = t+1)
  for (k in 0:t){
    aux_cnst = 0
    for (j in 0:k){
      aux_cnst = aux_cnst + factorial(j)*(2^(-j))*choose(n,j)*nStirling2(k, j) 
    }
    aux_sum = ((-1)^k)*(n^(t-k))*choose(t,k)*aux_cnst
  }
  
  kw_lower_b = (N/(N-1))*sum(aux_sum) - (n^t)/(N-1)
  
  return(kw_lower_b)
}

