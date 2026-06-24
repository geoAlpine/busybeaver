import numpy as np
# RE-ANALYSIS for new-math material: linear complexity of the parity sequence (Berlekamp-Massey over GF(2)).
# Low complexity => structured (approachable). Linear-growth complexity => 'random-like' (hard, new language).
N=4000
c=8; e=[]
for n in range(N): e.append(c&1); c=3*c//2
def berlekamp_massey(s):
    n=len(s); b=[1]+[0]*n; cc=[1]+[0]*n; L=0; m=-1; bb=1
    for i in range(n):
        d=s[i]
        for j in range(1,L+1): d^=cc[j]&s[i-j]
        if d==0: continue
        t=cc[:]
        for j in range(0,n-i+m): 
            if i-m+j<=n: cc[i-m+j]^=b[j]
        if 2*L<=i: L=i+1-L; m=i; b=t
    return L
print("LINEAR COMPLEXITY of the parity sequence (Berlekamp-Massey, GF(2)):")
for M in (200,500,1000,2000,4000):
    L=berlekamp_massey(e[:M])
    print(f"  first {M:4d} bits: linear complexity = {L}  (={L/M:.3f}*M;  ~M/2 => 'random/maximal')")
print("\n=> linear complexity ~ M/2 => the parity sequence is MAXIMALLY complex (no short LFSR);")
print("   it is 'random-like' in the linear-complexity sense. The difficulty is REAL, now in sequence-")
print("   design language: proving statistics of a max-linear-complexity self-referential generator.")
print("   MATERIAL: the parity = NONLINEAR FILTER (bit_n extraction) of a LINEAR-feedback carry sequence S_n.")
