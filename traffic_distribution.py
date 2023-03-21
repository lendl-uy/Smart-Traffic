# Author: Jan Lendl R. Uy
# CoE 199 Traffic Volume Distribution Generation

import numpy as np

def uniformify(T, n):

  # Get uniform distribution of hourly traffic volume with 3600/T samples
  t = int(3600/T)
  p = np.empty(t)
  for i in range(len(p)):
    p[i] = int(n/t+0.5)
  sum_p = int(sum(p))

  # Ensure that sum is equal to n
  if sum_p != n:
    if sum_p > n:
      p[-1] = int(p[-1]-(sum_p-n))
    else:
      p[-1] = int(p[-1]+(n-sum_p))

  return p

def poissonify(T, n):

  # Get Poisson distribution of hourly traffic volume with 3600/T samples
  t = int(3600/T)
  p = np.random.poisson(n/t, t)
  sum_p = sum(p)

  # Scale entries and convert them into integers
  p = p*(n/sum(p))
  p = [int(round(p[i])) for i in range(len(p))]
  sum_p = int(sum(p))

  # Ensure that sum is equal to n
  if sum_p != n:
    if sum_p-n > n:
      p[-1] = int(p[-1]-(sum_p-n))
    else:
      p[-1] = int(p[-1]+(n-sum_p))
  
  return p