"""Orbit-level BOOTSTRAP test: does small PAST imbalance force the current Korobov sum / parity bit
to be balanced?  This is the SEQUENCE-level (not measure-level) version of the contraction idea.

Causality asset: e_n = bit_n(8.3^n) XOR bit_n(T_n), T_n = sum_{k<n} 2^k 3^{n-1-k} e_k depends ONLY on
e_0..e_{n-1}.  So the sequence is a deterministic forward recursion (no fixed-point circularity).

We test the load-bearing hypothesis of the bootstrap inductive step:
    A(delta, N) := mean over n<N and over trials of (-1)^{bit_n(T_n)}  with e_k i.i.d. sign-mean delta.
If the bootstrap works we need A(delta,N) <= C*|delta| (output balance forced by input imbalance).
Decompose A(delta) ~ A(0) + gain*delta.  KEY QUESTION: is the CONSTANT TERM A(0,N) (balanced input)
already ~0 for cheap reasons (then |delta|<=eps gives output balance), or is A(0,N) itself the open
Mahler product Phi(N) (then the inductive step BASE is Mahler, not weaker)?

Also: real-orbit conditional response (is there a mean-restoring force?), and the same-D spread test.
All numerics with .venv python. 0 false proofs: we only MEASURE; conclusions labelled in the .md.
"""
import math, random

def real_orbit_bits(N):
    c = 8; e = []
    for _ in range(N):
        e.append(c & 1)
        c = (3*c) >> 1   # floor(3c/2)
    return e

def phase(j):  # exact {(3/2)^j/4} = (3^j mod 2^{j+2})/2^{j+2}
    return (pow(3, j) % (1 << (j+2))) / (1 << (j+2))

def annealed_Phi(N):  # the open Mahler product = |E[e(T_n/2^{n+1})]| at p=1/2, as a function of cutoff
    prod = 1.0
    out = []
    for j in range(N):
        prod *= abs(math.cos(math.pi*phase(j)))
        out.append(prod)
    return out

# ---------------------------------------------------------------------------
# 1. Real orbit: confirm D_N -> 0, and test for a MEAN-RESTORING force.
# ---------------------------------------------------------------------------
print("="*78)
print("1. REAL ORBIT  D_N = (1/N) sum (-1)^{e_n}  and mean-restoring-force test")
N = 200000
e = real_orbit_bits(N)
s = [1-2*b for b in e]                  # (-1)^{e_n}
for M in (1000, 10000, 100000, 200000):
    D = sum(s[:M])/M
    print(f"   N={M:>7}   D_N = {D:+.5f}   even-density=(1+D)/2 = {(1+D)/2:.5f}")

# restoring force: correlation between next sign s[n] and trailing-window imbalance of s[n-W..n-1]
import statistics
def trailing_corr(s, W):
    xs=[]; ys=[]
    for n in range(W, len(s)):
        ys.append(s[n])
        xs.append(sum(s[n-W:n])/W)
    mx=statistics.fmean(xs); my=statistics.fmean(ys)
    num=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
    dx=math.sqrt(sum((a-mx)**2 for a in xs)); dy=math.sqrt(sum((b-my)**2 for b in ys))
    return num/(dx*dy) if dx>0 and dy>0 else float('nan')
print("   restoring-force test: corr( next sign s[n] , trailing-mean s[n-W:n] ):")
for W in (8, 32, 128, 512):
    print(f"      W={W:>4}   corr = {trailing_corr(s, W):+.4f}   (|corr|~0 => NO mean-restoring force)")

# ---------------------------------------------------------------------------
# 2. Feedback decomposition: A(delta,N) = A(0,N) + gain*delta ?  (the inductive-step hypothesis)
#    e_k i.i.d. with P(e=1)=p, sign-mean delta = E[(-1)^e] = 1-2p  => p=(1-delta)/2.
#    output per step = (-1)^{bit_n(T_n)}, T_{n+1}=3T_n+2^n e_n.
# ---------------------------------------------------------------------------
print("="*78)
print("2. FEEDBACK DECOMPOSITION  A(delta,N) = mean_n (-1)^{bit_n(T_n)}  vs input imbalance delta")
def Arun(delta, N, trials, seed):
    p = (1-delta)/2.0
    rng = random.Random(seed)
    tot = 0.0
    for t in range(trials):
        T = 0; acc = 0
        for n in range(N):
            acc += 1 - 2*((T >> n) & 1)        # (-1)^{bit_n(T_n)}
            b = 1 if rng.random() < p else 0
            T = 3*T + (b << n)
        tot += acc / N
    return tot / trials

Ncut = 1200; trials = 400
Phi = annealed_Phi(Ncut)
PhiN = Phi[Ncut-1]
print(f"   annealed Mahler product Phi(N={Ncut}) = {PhiN:.3e}   (the OPEN quantity = A(0) target)")
print(f"   {'delta':>8} {'A(delta,N)':>12}")
res={}
for delta in (-0.30,-0.15,-0.05,0.0,0.05,0.15,0.30):
    a = Arun(delta, Ncut, trials, seed=12345+int(1000*delta))
    res[delta]=a
    print(f"   {delta:>8.2f} {a:>12.5f}")
A0 = res[0.0]
gain = (res[0.30]-res[-0.30])/0.60
print(f"\n   CONSTANT TERM  A(0,N) = {A0:+.5f}   (compare Phi(N)={PhiN:.3e}; A(0) ~ Phi => Mahler)")
print(f"   SLOPE (gain)   dA/ddelta ~ {gain:+.4f}   (the feedback gain; small => sub-critical/stable)")

# ---------------------------------------------------------------------------
# 3. SAME-|D| SPREAD test: is past imbalance D a SUFFICIENT statistic for the output bit?
#    Generate many past bit-strings ALL with the SAME small imbalance D, different arrangements;
#    measure spread of the resulting bit_{N}(T_N).  Large spread => D does NOT determine output.
# ---------------------------------------------------------------------------
print("="*78)
print("3. SAME-|D| SPREAD: fix past imbalance D, vary arrangement, measure output-bit balance spread")
def out_bit_for_arrangement(bits):
    N=len(bits); T=0
    for n in range(N):
        T = 3*T + (bits[n] << n)
    return (T >> N) & 1
def spread_at_D(D, N, trials, seed):
    # number of ones to hit imbalance D: D = (#zeros-#ones)/N => #ones = N(1-D)/2
    ones = round(N*(1-D)/2)
    rng = random.Random(seed)
    outs=[]
    for t in range(trials):
        bits=[0]*(N-ones)+[1]*ones
        rng.shuffle(bits)
        outs.append(1-2*out_bit_for_arrangement(bits))  # (-1)^{bit}
    m=statistics.fmean(outs); sd=statistics.pstdev(outs)
    return m, sd, len(outs)
Ns=240; tr=300
for D in (0.0, 0.05, 0.15):
    m,sd,k = spread_at_D(D, Ns, tr, seed=777+int(100*D))
    print(f"   D={D:.2f}: mean output sign = {m:+.4f}, stdev across arrangements = {sd:.4f} (n={k})")
print("   => if mean ~0 and stdev ~1 for ALL D, the output bit is ~fair & D-insensitive:")
print("      past imbalance D is NOT a sufficient statistic => bootstrap step cannot read balance off D.")
