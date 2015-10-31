from gmpy import *

n=10
p=0.5
k=5

def f(n,k,p,prec=256):
    return mpf(comb(n,k),prec) * mpf(p,prec)**k * mpf(1-p,prec)**(n-k)

print(f(n,k,p))

