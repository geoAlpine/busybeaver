"""
Effective discrepancy of the archimedean rotation {n*beta}, beta=log_3(4/3),
via Ostrowski / three-distance, and the Baker two-log irrationality bound.
"""
import mpmath as mp
mp.mp.dps = 120
log3 = mp.log(3)
beta = mp.log(mp.mpf(4)/3)/log3
LOG4 = mp.log(4)

def cont_frac(x, n):
    a=[]; y=mp.mpf(x)
    for _ in range(n):
        f=mp.floor(y); a.append(int(f)); fr=y-f
        if fr==0: break
        y=1/fr
    return a
def convergents(a):
    hm2,hm1=0,1; km2,km1=1,0; out=[]
    for ai in a:
        h=ai*hm1+hm2; k=ai*km1+km2; out.append((h,k)); hm2,hm1=hm1,h; km2,km1=km1,k
    return out
A=cont_frac(beta,60); conv=convergents(A)

# ---- (a) empirical star-discrepancy of {n beta}, n=1..N ---------------------
def star_disc(alpha, N):
    pts=sorted(float((mp.mpf(alpha)*n)%1) for n in range(1,N+1))
    D=0.0
    for i,x in enumerate(pts):
        D=max(D, abs((i+1)/N - x), abs(i/N - x))
    return D
print("=== empirical star-discrepancy D*_N of {n beta} ===")
print(" N        D*_N        N*D*_N     (log N)")
import math
for N in [100,1000,10000,50000,150000]:
    D=star_disc(beta,N)
    print(" %-8d %.6f   %8.3f   %6.3f"%(N,D,N*D,math.log(N)))

# ---- (b) Ostrowski bound  N D*_N <= sum_{k: q_k<=N} a_{k+1} ------------------
print("\n=== Ostrowski/CF discrepancy bound  N D*_N <= 2 + sum_{q_k<=N} a_{k+1} ===")
for N in [100,1000,10000,50000,150000]:
    s=0
    for k,(p,q) in enumerate(conv):
        if q<=N and k+1<len(A): s+=A[k+1]
        if q>N: break
    print(" N=%-8d  sum a_{k+1} (q_k<=N) = %-4d  => bound N D*_N <= %d"%(N,s,s+2))

# ---- (c) three-distance theorem: gaps of {n beta}, n=0..N-1 take <=3 values -
print("\n=== three-distance theorem check (gaps take at most 3 distinct lengths) ===")
for N in [500,5000,50000]:
    pts=sorted(float((mp.mpf(beta)*n)%1) for n in range(N))
    gaps=[round(pts[i+1]-pts[i],10) for i in range(len(pts)-1)]
    gaps.append(round(1-pts[-1]+pts[0],10))
    distinct=sorted(set(gaps))
    print(" N=%-6d distinct gap lengths=%d  values=%s"%(N,len(distinct),
          [round(g,6) for g in distinct[:4]]))

# ---- (d) Baker two-log: ||q beta|| = |q log4 - (p+q) log3| / log3 ------------
print("\n=== Baker two-log form: ||q_k beta|| via Lambda = q log4 - (p+q) log3 ===")
print(" the rotation's approximability is a LINEAR FORM IN TWO LOGS (Baker-reach)")
print(" k   q_k                a_{k+1}   ||q_k beta||        q_k*||q_k beta||")
for k,(p,q) in enumerate(conv[:20]):
    Lam = q*LOG4 - (p+q)*log3          # = log(4^q / 3^{p+q})
    nrm = abs(Lam)/log3                # = ||q beta||
    # cross-check against direct
    direct = abs(q*beta-p)
    assert abs(nrm-direct)<mp.mpf(10)**(-30)
    print(" %-3d %-18d %-8s %s   %s"%(k,q,str(A[k+1]) if k+1<len(A) else '-',
          mp.nstr(nrm,6), mp.nstr(q*nrm,5)))

# empirical irrationality-measure exponent: mu ~ 2 + limsup log a_{k+1}/log q_k
print("\n=== empirical irrationality-measure indicator  1 + log a_{k+1}/log q_k ===")
worst=0
for k,(p,q) in enumerate(conv):
    if k+1>=len(A) or q<2: continue
    val = 1 + math.log(A[k+1])/math.log(q) if A[k+1]>1 else 1.0
    worst=max(worst,val)
print(" max over reliable k of (1 + log a_{k+1}/log q_k) =", round(worst,4),
      "  (mu ~ 2 <=> this stays near 1; unbounded => spikes)")
print(" => empirically mu(beta) ~ 2 (a_k grow far slower than q_k);")
print("    UNCONDITIONALLY finite & EFFECTIVE by Baker/Baker-Wustholz on 2 logs.")
