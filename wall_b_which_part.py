"""WALL (B) — which part of the parity carries it? a_n = bit_n(8*3^n) vs b_n = bit_n(T_n).

r_n = a_n XOR b_n.
  a_n = bit_n(8*3^n)  -- FULLY EXPLICIT, non-self-generated. bit_n(8*3^n) = floor(8*(3/2)^n) mod 2.
        Its balance (1/N)sum(-1)^{a_n} -> 0  <=>  equidistribution of {4*(3/2)^n} mod 1  (SPECIFIC point).
  b_n = bit_n(T_n)    -- SELF-GENERATED carry, T_{n+1} = 3 T_n + 2^n r_n  (closed loop r=a XOR b).

Soundness: exact big-int arithmetic; cross-check r_n against the REAL hydra orbit parity h_k mod 2.
Measure balance of a_n, b_n, r_n and the a/b correlation, with rates, to large N.
"""
import math

N = 60000

# ---- 1. real hydra orbit parity (ground truth): h0=8, h_{k+1}=floor(3h/2), parity h&1 ----
def hydra_parities(N):
    h = 8
    p = bytearray(N)
    for k in range(N):
        p[k] = h & 1
        h = h + (h >> 1)   # floor(3h/2)
    return p

# ---- 2. closed-loop identity: a_n=bit_n(8*3^n), b_n=bit_n(T_n), r=a XOR b, T_{n+1}=3T+2^n r ----
def identity_sequences(N):
    a = bytearray(N); b = bytearray(N); r = bytearray(N)
    x = 8           # = 8*3^n, grows
    T = 0           # carry sum
    for n in range(N):
        an = (x >> n) & 1
        bn = (T >> n) & 1
        rn = an ^ bn
        a[n] = an; b[n] = bn; r[n] = rn
        x *= 3
        T = 3 * T + (rn << n)
    return a, b, r

ph = hydra_parities(N)
a, b, r = identity_sequences(N)

# cross-check identity vs real orbit (find best offset)
def first_mismatch(u, v, off=0):
    m = min(len(u), len(v) - off)
    for i in range(m):
        if u[i] != v[i + off]:
            return i
    return -1

print("SOUNDNESS cross-check: identity r_n  vs  real hydra parity h_n&1")
for off in (0, 1, 2, -1):
    if off >= 0:
        agree = sum(1 for i in range(N - off) if r[i] == ph[i + off]) / (N - off)
    else:
        agree = sum(1 for i in range(N + off) if r[i - off] == ph[i]) / (N + off)
    print(f"   offset {off:+d}: agreement = {agree:.4f}")
print(f"   first 24 r_n : {''.join(map(str,r[:24]))}")
print(f"   first 24 h&1 : {''.join(map(str,ph[:24]))}")

# ---- 3. balances with rates ----
def balance(seq, upto):
    s = 0
    for i in range(upto):
        s += 1 - 2 * seq[i]   # (-1)^bit
    return s / upto

print("\nBALANCE  A(M) = (1/M) sum_{n<M} (-1)^{bit}   (-> 0 means balanced)")
print(f"  {'M':>7} {'A_a (explicit)':>16} {'A_b (carry)':>14} {'A_r (parity)':>14} {'A_a*A_b':>10}")
Ms = [1000, 3000, 10000, 30000, 60000]
Ms = [m for m in Ms if m <= N]
for M in Ms:
    Aa = balance(a, M); Ab = balance(b, M); Ar = balance(r, M)
    print(f"  {M:>7} {Aa:>16.5f} {Ab:>14.5f} {Ar:>14.5f} {Aa*Ab:>10.5f}")

# rate fit: |A(M)| ~ C M^{-alpha}.  Compare to 1/sqrt(M) ~ M^{-0.5}.
def rate(seq):
    pts = []
    M = 1000
    while M <= N:
        pts.append((M, abs(balance(seq, M)) + 1e-12))
        M *= 2
    xs = [math.log(m) for m, _ in pts]
    ys = [math.log(v) for _, v in pts]
    k = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    slope = (k*sxy - sx*sy) / (k*sxx - sx*sx)
    return slope
print(f"\n  log-log decay exponent (A(M) ~ M^slope; -0.5 = sqrt-cancellation):")
print(f"    a_n : slope = {rate(a):+.3f}")
print(f"    b_n : slope = {rate(b):+.3f}")
print(f"    r_n : slope = {rate(r):+.3f}")

# ---- 4. correlation between a_n and b_n ----
# Pearson on the bit sequences; also the sign-product mean (= A_r exactly) vs independent A_a*A_b.
import statistics
ma = sum(a)/N; mb = sum(b)/N
cov = sum((a[i]-ma)*(b[i]-mb) for i in range(N))/N
va = ma*(1-ma); vb = mb*(1-mb)
pear = cov / math.sqrt(va*vb) if va>0 and vb>0 else 0.0
signprod = sum((1-2*a[i])*(1-2*b[i]) for i in range(N))/N   # = A_r
indep = (sum(1-2*ai for ai in a)/N) * (sum(1-2*bi for bi in b)/N)  # A_a*A_b
print(f"\nCORRELATION a_n vs b_n  (N={N}):")
print(f"   mean a = {ma:.5f}   mean b = {mb:.5f}")
print(f"   Pearson(a,b)               = {pear:+.5f}")
print(f"   E[(-1)^a (-1)^b] (=A_r)    = {signprod:+.5f}")
print(f"   A_a * A_b (if independent) = {indep:+.5f}")
print(f"   => XOR balance differs from independent product by {signprod-indep:+.5f}")

# ---- 5. a_n explicit-half framing: is its balance the {4*(3/2)^n} equidistribution? ----
# a_n = floor(8*(3/2)^n) mod 2 = 0  iff  {8*(3/2)^n / 2} = {4*(3/2)^n} in [0,1/2).
# verify a_n equals the half-interval indicator of {4*(3/2)^n} mod 1 (exact via integers).
def check_a_is_specific_point(M):
    x = 8  # 8*3^n
    mis = 0
    for n in range(M):
        # {4*(3/2)^n} = {8*3^n / 2^{n+1}} = (8*3^n mod 2^{n+1}) / 2^{n+1}
        frac_num = x % (1 << (n + 1))   # numerator over 2^{n+1}
        # in [0,1/2)  iff  frac_num < 2^n
        half = 1 if frac_num < (1 << n) else 0  # 1 means {.}<1/2 => a_n should be 0
        an = (x >> n) & 1
        if (an == 0) != (half == 1):
            mis += 1
        x *= 3
    return mis
mm = min(N, 20000)
mis = check_a_is_specific_point(mm)
print(f"\nEXPLICIT-HALF IDENTITY (n<{mm}):")
print(f"   a_n == [ {{4*(3/2)^n}} in [0,1/2) ] mismatches = {mis}  (0 => a_n balance IS the")
print(f"   equidistribution of the SPECIFIC point sequence {{4*(3/2)^n}} mod 1 = Mahler-for-a-point).")
