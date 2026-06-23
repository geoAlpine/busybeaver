# The adversarial all-odd trap requires c ≡ 1 mod 2^k. Real orbit grows => can't stay trapped.
# Verify: odd-run length at step n EXACTLY equals v2(c_n - 1) (distance from the odd-trap c≡1),
# and an odd-run of length L means c was ≡1 mod 2^L then escaped. depth=o(n) <=> residence near trap is o(n).
c=8
def v2m1(x): 
    x=x-1
    if x==0: return 99
    r=0
    while x&1==0: x>>=1; r+=1
    return r
N=200000
# check: during an odd run, is c ≡ 1 mod 2^(remaining run)? and run length = v2(c_n-1) at run start
runstart_depth=[]; curlen=0; started=None
seq=[]
c=8
prev_parity=None
for n in range(N):
    p=c&1
    seq.append((n,c%32,p,v2m1(c)))
    c=3*c//2
# verify run-length == v2(c-1) at the step the run starts (c becomes odd from even)
c=8; parity=[]; 
cs=[]
c=8
for n in range(N): parity.append(c&1); cs.append(c); c=3*c//2
ok=True; checks=0
i=0
while i<N-40:
    if parity[i]==1 and (i==0 or parity[i-1]==0):
        # run start; measure run length
        L=0
        while i+L<N and parity[i+L]==1: L+=1
        d=v2m1(cs[i])
        if d!=L and d<90:
            ok=False
        checks+=1
        i+=L
    else:
        i+=1
print(f"verified on {checks} odd-runs: run-length == v2(c_start - 1) (=distance from odd-trap c≡1): {ok}")
# distribution: max odd-run (max residence near trap) vs n
maxrun=0; c=8; parity2=[]
c=8
mr=[]
for n in range(N): parity2.append(c&1); c=3*c//2
run=0
import math
for n in range(N):
    if parity2[n]==1: run+=1
    else: run=0
    maxrun=max(maxrun,run)
    if n in (1000,10000,100000,N-1): mr.append((n,maxrun,round(math.log2(n),1)))
print("max odd-run (max trap-residence) vs n, with log2(n):", mr)
print("\nINTERPRETATION: depth_n = v2(c_n-1) = distance from the odd-trap c≡1 mod 2^depth.")
print("The orbit's GROWTH (c_n->inf) forbids permanent trapping; non-halt <=> residence = o(n).")
print("This = the original depth=o(n); the shift-renewal shows it needs only BALANCED+decorrelated")
print("incoming bits (even-density>1/3 robust to bias q in (.01,.99)), not full uniformity.")
