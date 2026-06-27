"""Wall B decorrelation structure: cross- and lagged-correlation of the two Antihydra digital functions
   a_n = bit_n(8*3^n)   (explicit (3/2)^n top digit; = 1[{4*(3/2)^n} in [1/2,1)])
   b_n = bit_n(T_n),  T_{n+1}=3 T_n + 2^n r_n,  r = a XOR b  (self-generated carry)
The complete proof needs only A_r = (1/N) sum (-1)^{a_n}(-1)^{b_n} -> 0  (asymptotic ORTHOGONALITY).
We measure: cross-correlation A_r, its decay exponent; lagged corr(a_n, b_{n+k}); and compare b to an
INDEPENDENT digital-function surrogate (Thue-Morse, Rudin-Shapiro, and a (3/2)^j carry driven by an
independent scenery) to see whether the a-b decorrelation looks like two INDEPENDENT digital functions.
Exact big-int arithmetic. .venv only. No claim beyond measured numbers (null band ~1/sqrt(N)).
"""
import math

N = 200000

# --- the real orbit: a_n, b_n, r_n exact ---
a = bytearray(N); b = bytearray(N); r = bytearray(N)
T = 0; p3 = 1
for n in range(N):
    an = (8 * p3 >> n) & 1
    bn = (T >> n) & 1
    rn = an ^ bn
    a[n] = an; b[n] = bn; r[n] = rn
    T = 3 * T + (1 << n) * rn
    p3 *= 3

def sgn(byte_seq, lo, hi):
    return [1 - 2*byte_seq[i] for i in range(lo, hi)]

def mean(x):
    return sum(x)/len(x)

# means / balance
print(f"N={N}")
print(f"mean a = {mean(a):.5f}  mean b = {mean(b):.5f}  mean r = {mean(r):.5f}")

# cross-correlation A_r = mean (-1)^a (-1)^b   (= -1..1)
def cross(M):
    s = 0
    for n in range(M):
        s += (1-2*a[n])*(1-2*b[n])
    return s/M

print("\n--- cross-correlation A_r = (1/M) sum (-1)^{a}(-1)^{b}  (orthogonality target; null band ~1/sqrt(M)) ---")
Ms = [1000, 3000, 10000, 30000, 100000, 200000]
for M in Ms:
    Ar = cross(M)
    print(f"  M={M:>7}  A_r={Ar:+.5f}  band={1/math.sqrt(M):.5f}  A_r*sqrt(M)={Ar*math.sqrt(M):+.3f}")

# decay exponent of |A_r| via log-log slope over a window
import statistics
xs=[]; ys=[]
for M in [2000,4000,8000,16000,32000,64000,128000]:
    v=abs(cross(M))
    if v>0:
        xs.append(math.log(M)); ys.append(math.log(v))
# least squares slope
mx=mean(xs); my=mean(ys)
slope = sum((xs[i]-mx)*(ys[i]-my) for i in range(len(xs)))/sum((xs[i]-mx)**2 for i in range(len(xs)))
print(f"\n  log-log decay exponent of |A_r| ~ M^slope : slope = {slope:+.3f}   (-0.5 = sqrt-cancellation / independent)")

# --- lagged cross-correlation corr(a_n, b_{n+k}) for k = -K..K ---
print("\n--- lagged sign-correlation  g(k) = mean_n (-1)^{a_n} (-1)^{b_{n+k}}  (null band ~1/sqrt(N)) ---")
K = 12
band = 1/math.sqrt(N)
for k in range(-K, K+1):
    lo = max(0, -k); hi = min(N, N-k)
    s = 0; cnt = hi-lo
    for n in range(lo, hi):
        s += (1-2*a[n])*(1-2*b[n+k])
    g = s/cnt
    flag = "" if abs(g) < 3*band else "  <-- >3 sigma"
    print(f"  k={k:+3d}  g={g:+.5f}   ({g/band:+.2f} sigma){flag}")
print(f"  null band 1/sqrt(N) = {band:.5f}")

# --- surrogate: replace b by INDEPENDENT digital functions; compare cross-corr with a ---
print("\n--- a_n cross-correlated with INDEPENDENT digital functions (surrogates for b) ---")
def thue_morse(n): return bin(n).count('1') & 1
def rudin_shapiro(n): return bin(n & (n>>1)).count('1') & 1
tm = bytearray(thue_morse(n) for n in range(N))
rs = bytearray(rudin_shapiro(n) for n in range(N))
# (3/2)^j carry bit driven by an INDEPENDENT pseudo-random scenery (not the orbit's own parity)
def indep_carry(N, seed=12345):
    out = bytearray(N); T=0
    for n in range(N):
        out[n] = (T>>n)&1
        u = ((n*2654435761 + seed) & 0xFFFFFFFF)
        bit = (u>>13)&1
        T = 3*T + (1<<n)*bit
    return out
ic = indep_carry(N)

def xcorr_with_a(s):
    sm=0
    for n in range(N):
        sm += (1-2*a[n])*(1-2*s[n])
    return sm/N

for name, s in [("b (real self-gen carry)", b),
                ("Thue-Morse", tm),
                ("Rudin-Shapiro", rs),
                ("indep-scenery (3/2)^j carry", ic)]:
    print(f"  corr(a, {name:<28}) = {xcorr_with_a(s):+.5f}   ({xcorr_with_a(s)/band:+.2f} sigma)")
print(f"  null band 1/sqrt(N) = {band:.5f}")

print("""
READING:
  - If A_r -> 0 at slope ~ -0.5 and A_r*sqrt(M) stays O(1): the two digital functions are orthogonal at the
    sqrt-cancellation rate = behave like INDEPENDENT balanced digital functions (no resonance, no conspiracy).
  - If lagged g(k) is white (all within ~3 sigma): no phase-lag resonance between the explicit top digit a_n
    and the carry b_{n+k} at any small lag => the decorrelation has NO short-range structure.
  - If corr(a, b) is the same order as corr(a, Thue-Morse/Rudin-Shapiro): the real self-generated carry is,
    cross-correlation-wise, indistinguishable from a genuinely independent digital function => a_n ⊥ b_n is
    empirically an instance of "two independent digital functions", NOT a fine conspiracy.
""")
