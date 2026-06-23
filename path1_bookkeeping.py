import math, numpy as np
# Exact bookkeeping: log2(c_n) ~ 0.585n + 3 (parity-INDEPENDENT growth). At even-step j, n_j = j + sum_{i<j} D_i.
# So sum D_i = n_j - j, and avg D < 2 <=> n_j < 3j <=> even-density > 1/3. Test if growth law constrains it.
c=8; logs=[]; evensteps=[]; n=0; jumpsum=0; jcount=0
data=[]
for n in range(200000):
    if c%2==0:
        jcount+=1
        data.append((n, jcount, math.log2(c)))
    c=3*c//2
data=np.array(data,float)
ns=data[:,0]; js=data[:,1]; lg=data[:,2]
# growth law: log2(c_n) vs 0.585n
slope=np.polyfit(ns,lg,1)
print(f"log2(c_n) ~ {slope[0]:.5f}*n + {slope[1]:.2f}  (log2(3/2)={math.log2(1.5):.5f}) -- PARITY-INDEPENDENT")
# relation sum D_i = n_j - j; avg D = (n_j-j)/j ; even-density = j/n_j
print(f"at end: n={ns[-1]:.0f} even-steps j={js[-1]:.0f} => even-density={js[-1]/ns[-1]:.4f} avg jump={(ns[-1]-js[-1])/js[-1]:.4f}")
print("\n=> the growth slope 0.585 is FIXED regardless of parities (parity-blind),")
print("   so it gives NO lower bound on even-density. The exact bookkeeping sum D_i=n_j-j is")
print("   a TAUTOLOGY (avg jump<2 <=> even-density>1/3). Circularity NOT broken by growth.")

# Last check: is there ANY conserved/drift quantity in the induced jumps? test partial sums vs sqrt fluctuations
def v2(x):
    r=0
    while x&1==0 and x: x>>=1; r+=1
    return r
def F(cp):
    x=3*cp-1; D=v2(x); u=x>>D; return (pow(3,D)*u+1)//2, D
cp=4; Ds=[]
for _ in range(100000):
    cp,D=F(cp); Ds.append(D)
Ds=np.array(Ds); cums=np.cumsum(Ds-1)  # centered (E[D]=1)
print(f"\ncentered cumulative sum of (D_j - 1): final={cums[-1]:.0f}, max|.|={np.abs(cums).max():.0f}, sqrt(N)={math.sqrt(len(Ds)):.0f}")
print("  (fluctuations ~ sqrt(N) = random-walk => no drift/conserved quantity to exploit; jumps are 'iid-like')")
