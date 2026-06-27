"""WALL B bilinear / cross-correlation van der Corput probe (2026-06-28).

Question: does the JOINT/BILINEAR structure of the cross-correlation
    C_N = (1/N) sum_{n<N} (-1)^{a_n} (-1)^{b_n},   a_n=bit_n(8*3^n), b_n=bit_n(T_n)
enable cancellation the lacunary MARGINAL sums cannot?

We test the precise hypothesis: the two leading phases
    phi_a(n) = {4 (3/2)^n}            (drives (-1)^{a_n})
    phi_b(n) = {T_n / 2^{n+1}}        (drives (-1)^{b_n})
SHARE the same fast (3/2)^n mode, so it CANCELS in the difference combination,
leaving a slow tractable residual.

All exact big-int arithmetic. Zero false proofs: we report exactly what is an
identity vs what remains open.
"""
import math

N = 200000

# --- real Antihydra/Hydra orbit: c0=8, c_{k+1}=floor(3 c_k /2); parity r_n = c_n mod 2
def build():
    h = 8
    r = []
    hs = []
    for n in range(N):
        hs.append(h)
        r.append(h & 1)
        h = (3 * h) // 2
    return r, hs

r, hs = build()

# --- a_n = bit_n(8*3^n)  (exact)
# --- T_n recurrence T_{n+1}=3 T_n + 2^n r_n, T_0=0 ; b_n = bit_n(T_n)
# --- check identities
pow3 = 1            # 3^n
T = 0               # T_n
a = []
b = []
phia = []           # {4(3/2)^n} = (8*3^n mod 2^{n+1})/2^{n+1}
phib = []           # {T_n/2^{n+1}} = (T_n mod 2^{n+1})/2^{n+1}
phisum = []         # {phi_a+phi_b}
phidiff = []        # {phi_a-phi_b}
ok_xor = True
ok_cn  = True
ok_int = True       # T_n == 8*3^n mod 2^n
ok_diff = True      # phi_a-phi_b == r_n/2  (the EXACT fast-mode cancellation)
prod_eq_parity = True

NCHECK = 40000      # exact-identity checks up to here (big-int cost), stats over full N
for n in range(N):
    eight3n = 8 * pow3
    an = (eight3n >> n) & 1
    bn = (T >> n) & 1
    a.append(an); b.append(bn)

    if n < NCHECK:
        m1 = 1 << (n + 1)
        pa = (eight3n % m1) / m1
        pb = (T % m1) / m1
        phia.append(pa); phib.append(pb)
        phisum.append((pa + pb) % 1.0)
        phidiff.append((pa - pb) % 1.0)
        # identities
        if (an ^ bn) != r[n]:
            ok_xor = False
        cn = (eight3n - T) >> n           # should be exact integer = h_n
        if (eight3n - T) % (1 << n) != 0 or cn != hs[n]:
            ok_cn = False
        if (eight3n - T) % (1 << n) != 0:
            ok_int = False
        # phi_a-phi_b == (8*3^n - T)/2^{n+1} = c_n/2  -> mod 1 == (c_n mod 2)/2 = r_n/2
        diff_exact = ((eight3n - T) % m1) / m1
        if abs(diff_exact - (r[n] / 2.0)) > 1e-12:
            ok_diff = False
        # product == parity
        if ((-1) ** an) * ((-1) ** bn) != (-1) ** r[n]:
            prod_eq_parity = False

    # advance
    T = 3 * T + (1 << n) * r[n]
    pow3 *= 3

print("=== EXACT IDENTITIES (big-int, n < %d) ===" % NCHECK)
print(f"  r_n == a_n XOR b_n                         : {ok_xor}")
print(f"  c_n == (8*3^n - T_n)/2^n == real orbit h_n : {ok_cn}")
print(f"  T_n == 8*3^n (mod 2^n) [low n bits cancel] : {ok_int}")
print(f"  phi_a - phi_b == c_n/2  (mod 1) == r_n/2   : {ok_diff}   <-- FAST MODE CANCELS EXACTLY")
print(f"  (-1)^a_n (-1)^b_n == (-1)^r_n              : {prod_eq_parity}")

# --- velocities (discrete derivative mod 1, signed to (-1/2,1/2]) ---
def vel(seq):
    out = []
    for n in range(len(seq) - 1):
        d = (seq[n + 1] - seq[n]) % 1.0
        if d > 0.5:
            d -= 1.0
        out.append(abs(d))
    return out

va = vel(phia)                 # marginal a phase velocity
vsum = vel(phisum)             # off-diagonal (k+l!=0) product mode velocity
vdiff = vel(phidiff)           # diagonal difference residual velocity
import statistics as st
def stats(x):
    return f"mean={st.mean(x):.4f} median={st.median(x):.4f} max={max(x):.4f}"
print("\n=== PHASE VELOCITIES (|d/dn| mod 1) over n<%d ===" % NCHECK)
print(f"  marginal  phi_a       (fast (3/2)^n)        : {stats(va)}")
print(f"  SUM mode  phi_a+phi_b (fast, doubled)       : {stats(vsum)}")
print(f"  DIFF mode phi_a-phi_b (residual = c_n/2)    : {stats(vdiff)}")
print("  (a 'fast'/equidistributed phase has mean vel ~0.25, max ~0.5;")
print("   the diff residual is {0,1/2}-valued: velocity is bounded, NOT smooth.)")
# distribution of the residual values
from collections import Counter
cnt = Counter(round(x, 6) for x in phidiff)
print(f"  residual phi_a-phi_b takes values: {dict(cnt)}  (= {{0, 1/2}} only)")

# --- cross-correlation decay vs marginals ---
def slope(seq, sign_pow):
    # |(1/M) sum_{n<M} (-1)^{seq_n}| at geometric M, log-log slope
    Ms = [m for m in [1000, 3000, 10000, 30000, 100000, N] if m <= len(seq)]
    pts = []
    csum = 0
    vals = {}
    target = set(Ms)
    for n in range(len(seq)):
        csum += (-1) ** seq[n]
        if (n + 1) in target:
            vals[n + 1] = abs(csum) / (n + 1)
    xs = [math.log(m) for m in Ms]
    ys = [math.log(vals[m]) if vals[m] > 0 else float('nan') for m in Ms]
    # least squares on finite points
    fin = [(x, y) for x, y in zip(xs, ys) if math.isfinite(y)]
    mx = sum(x for x, _ in fin) / len(fin); my = sum(y for _, y in fin) / len(fin)
    sl = sum((x - mx) * (y - my) for x, y in fin) / sum((x - mx) ** 2 for x, _ in fin)
    return vals, sl, Ms

prod = [a[n] ^ b[n] for n in range(N)]   # a_n+b_n mod 2 == a XOR b == r_n
va_, sa, Ms = slope(a, 1)
vb_, sb, _  = slope(b, 1)
vp_, sp, _  = slope(prod, 1)
vr_, sr, _  = slope(r, 1)
print("\n=== DECAY of balance/cross-correlation  |.|/N  (slope ~ -0.5 = sqrt-cancel) ===")
hdr = "  M:" + "".join(f"{m:>12}" for m in Ms)
print(hdr)
print("  A_a (marg a) :" + "".join(f"{va_[m]:>12.5f}" for m in Ms) + f"   slope={sa:+.3f}")
print("  A_b (marg b) :" + "".join(f"{vb_[m]:>12.5f}" for m in Ms) + f"   slope={sb:+.3f}")
print("  C_N (a*b)    :" + "".join(f"{vp_[m]:>12.5f}" for m in Ms) + f"   slope={sp:+.3f}")
print("  W_N (parity) :" + "".join(f"{vr_[m]:>12.5f}" for m in Ms) + f"   slope={sr:+.3f}")
print("\n  (C_N and W_N are IDENTICAL columns: the cross-correlation IS the parity kernel,")
print("   because (-1)^a (-1)^b = (-1)^{a XOR b} = (-1)^{r_n} exactly.)")
