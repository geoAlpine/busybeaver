"""
o18 = floor(8N/3)+2 cryptid: apply the Antihydra capstone framework (base 8/3, 3-adic).
Exact big-int only. Soundness: every printed claim is either [VERIFIED] arithmetic or a model.
"""
from collections import Counter
from fractions import Fraction

# ---------------------------------------------------------------------------
# 0. RAW TM verification: orbit map and halt criterion
# ---------------------------------------------------------------------------
SPEC = "1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"
def parse(spec):
    M=[]
    for stt in spec.split('_'):
        ts=[stt[i:i+3] for i in (0,3)]; row=[]
        for t in ts:
            if t[0]=='-' or t[2]=='Z': row.append(None)
            else: row.append((int(t[0]), 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M
M=parse(SPEC)

def run_raw(maxsteps):
    SZ=1<<25; tape=bytearray(SZ); off=SZ//2
    pos=off; st=0
    Dreads1=0; Dreads1_leftIs1=0
    for step in range(maxsteps):
        r=tape[pos]
        if st==3 and r==1:        # D reads 1 -> F ; F then reads pos-1
            Dreads1+=1
            if tape[pos-1]==1: Dreads1_leftIs1+=1
        if st==5 and r==1:
            return ('HALT',step,Dreads1,Dreads1_leftIs1)
        tr=M[st][r]
        if tr is None: return ('HALT',step,Dreads1,Dreads1_leftIs1)
        w,d,ns=tr; tape[pos]=w; pos+=d; st=ns
    return ('RUN',maxsteps,Dreads1,Dreads1_leftIs1)

print("="*70)
print("0. RAW TM o18 =", SPEC)
tag,last,Dr,Drl = run_raw(60_000_000)
print(f"   60M steps: status={tag}; D-reads-1 events={Dr}; of these left-neighbor==1 (=>HALT): {Drl}")
print(f"   halt criterion: F reads 1  <=>  D reads a 1 whose LEFT cell is 1 (frontier collision).")
print(f"   [VERIFIED] {Drl} violations => non-halting so far; halt is an EXISTENCE event, not a density underflow.")

# ---------------------------------------------------------------------------
# 1. Orbit map f(N)=floor(8N/3)+2 ; reproduce known reset widths
# ---------------------------------------------------------------------------
def f(N): return (8*N)//3 + 2
print("="*70)
print("1. Orbit map f(N)=floor(8N/3)+2  (ratio p/q = 8/3)")
N=10; orb=[N]
for _ in range(12): N=f(N); orb.append(N)
print("   orbit from 10:", orb[:9], "...")
print("   [VERIFIED] matches doc 10->28->76->204->546->1458->3890:", orb[:7]==[10,28,76,204,546,1458,3890])

# ---------------------------------------------------------------------------
# 2. GAP-LEMMA analog (3-adic). Pure Mahler map g(N)=floor(8N/3).
#    For N coprime to 3:  r = 8N mod 3 = 2N mod 3 ;  D'' = v3(8N - r) ;
#    induced map to next coprime-to-3 value:  T''(N) = 8^{D''-1}(8N-r)/3^{D''}.
# ---------------------------------------------------------------------------
def v3(x):
    if x==0: return 10**9
    c=0
    while x%3==0: x//=3; c+=1
    return c
def g(N): return (8*N)//3
print("="*70)
print("2. GAP-LEMMA analog (3-adic) for the pure Mahler map g(N)=floor(8N/3)")
# verify: starting at N coprime to 3, # steps of g until next coprime-to-3 value == D''=v3(8N-r)
bad=0; checks=0
for N in range(1, 4000):
    if N%3==0: continue
    r=(8*N)%3
    Dpp=v3(8*N-r)
    # iterate g, count steps to next coprime-to-3
    cnt=0; x=N
    while True:
        x=g(x); cnt+=1
        if x%3!=0: break
        if cnt>200: break
    if cnt!=Dpp: bad+=1
    checks+=1
print(f"   [VERIFIED] gap == D''=v3(8N-r) for {checks-bad}/{checks} coprime seeds (violations={bad})")
# verify induced map closed form equals iterated g
bad2=0
for N in range(1,4000):
    if N%3==0: continue
    r=(8*N)%3; Dpp=v3(8*N-r)
    Tpp = 8**(Dpp-1)*(8*N-r)//(3**Dpp)
    x=N
    for _ in range(Dpp): x=g(x)
    if x!=Tpp: bad2+=1
print(f"   [VERIFIED] T''(N)=8^(D''-1)(8N-r)/3^D'' equals iterated g for all coprime seeds (violations={bad2})")

# ---------------------------------------------------------------------------
# 3. Distribution of D'' under Haar (Z_3*) vs along the actual induced orbit
#    Haar prediction:  P(D''=d) = (2/3)(1/3)^{d-1} ,  mean D'' = 3/2.
# ---------------------------------------------------------------------------
print("="*70)
print("3. Depth statistic D'' = v3(8o-r): Haar law vs orbit")
print("   Haar prediction: P(D''=d)=(2/3)(1/3)^(d-1), mean D'' = 3/2")
# Haar mean exact
mean_haar = sum(Fraction(d)*Fraction(2,3)*Fraction(1,3)**(d-1) for d in range(1,60))
print(f"   mean D'' (Haar, exact partial sum) = {float(mean_haar):.6f}  (-> 3/2)")
# along the induced orbit of the PURE map starting from a coprime seed near the real orbit
def induced_orbit(N0, steps):
    seq=[]; N=N0
    for _ in range(steps):
        if N%3==0:   # advance to coprime
            N=g(N); continue
        r=(8*N)%3; Dpp=v3(8*N-r)
        seq.append(Dpp)
        N=8**(Dpp-1)*(8*N-r)//(3**Dpp)
        if N> 10**4000: break
    return seq
seq=induced_orbit(7, 4000)   # 7 coprime to 3
cnt=Counter(seq)
n=len(seq)
print(f"   induced orbit (seed 7), {n} steps:")
for d in range(1,6):
    print(f"     P(D''={d}) orbit={cnt.get(d,0)/n:.4f}  Haar={float(Fraction(2,3)*Fraction(1,3)**(d-1)):.4f}")
print(f"   mean D'' along orbit = {sum(seq)/n:.4f}   (Haar=1.5)")
# 3-adic 'mult-of-3 density' = 1 - 1/mean :  renewal identity
md=sum(seq)/n
print(f"   renewal: density(N=0 mod3 steps)=1-1/meanD'' = {1-1/md:.4f}  (Haar=1-2/3=1/3)")

# ---------------------------------------------------------------------------
# 4. Base-3 digit equidistribution of the ACTUAL orbit f(N)=floor(8N/3)+2
#    (the Erdos-type kernel: does the base-3 digit of the (8/3)^n orbit equidistribute?)
# ---------------------------------------------------------------------------
print("="*70)
print("4. Base-3 digit equidistribution of the actual orbit floor(8N/3)+2")
N=10
for _ in range(50): N=f(N)
# now N is large; take many further steps, record units base-3 digit and full-expansion digit-2 density
units=Counter(); tot2=0; totd=0; second=Counter()
NN=N
for _ in range(6000):
    NN=f(NN)
    units[NN%3]+=1
    second[(NN//3)%3]+=1
    # digit-2 density (sample: count trits)
    x=NN;
    while x:
        if x%3==2: tot2+=1
        totd+=1; x//=3
print(f"   units trit distribution: {dict(units)}  (uniform=1/3 each)")
print(f"   2nd-lowest trit distribution: {dict(second)}")
print(f"   digit-2 density over full base-3 expansions: {tot2/totd:.4f}  (uniform=0.3333)")

# ---------------------------------------------------------------------------
# 5. Halting fixed point search (analog of Antihydra o=1)
# ---------------------------------------------------------------------------
print("="*70)
print("5. Halting fixed point / cycle search")
# integer fixed point of f: N=floor(8N/3)+2
fp=[N for N in range(-50,50) if f(N)==N]
print(f"   integer fixed points of f(N)=floor(8N/3)+2 in [-50,50]: {fp}")
print(f"   exact (no floor) fixed point N=8N/3+2 -> N = {Fraction(-6,5)}  (not a positive integer)")
# D''=1 branch fixed point of induced map: o=(8o-r)/3 -> 5o=r -> o=r/5 in Z_3 (off the integer orbit)
print(f"   induced D''=1 fixed point  o=r/5 in Z_3 (r in {{1,2}}): {Fraction(2,5)} or {Fraction(1,5)} (3-adic units, NOT integers)")
print(f"   monotonicity: f(N)-N = floor(8N/3)+2-N = floor(8N/3)-N+2 > 0 for N>=1  => orbit strictly increasing, transient")
incr=all(f(N)>N for N in range(1,100000))
print(f"   [VERIFIED] f(N)>N for N in [1,1e5]: {incr}  (no positive-integer cycle; like Antihydra, transient)")
# small seeds that DO halt (raw TM not needed: use the structural collision model is machine-specific;
# here we just note which tiny seeds of f reach the documented halting structure is a TM question.)
print("="*70)
print("DONE.")
