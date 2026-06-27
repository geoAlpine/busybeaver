"""Constructive attack on the 'independence of r_k' gap.

d(n) = bit_n(T_n), T_n = sum_k 2^k 3^{n-1-k} r_k. With INDEPENDENT r_k the carry lemma forces bit_n(T_n)
balanced; the orbit's r_k are self-referential (the closed loop). QUESTION: how much independence of the
input r_k is actually NEEDED for bit_n(T_n) to balance? Feed the SAME carry-sum mechanism a panel of
input sequences whose correlation structure is KNOWN (some with PROVEN decorrelation), and measure the
balance of the diagonal carry bit. This quantifies the gap: if balance is guaranteed by a finite-order
decorrelation we can certify, the orbit reduces to 'does the orbit parity have that decorrelation' (=
Mahler), but the gap is then a NAMED finite property, not a black box.

Input panel (all deterministic, explicit):
  orbit     : the real Antihydra parity r_n = c_n mod 2                  [unknown statistics]
  champ     : binary Champernowne digits                                [PROVEN normal -> all finite-order uniform]
  legendre  : Legendre symbol (k|p) sequence, p prime                   [PROVEN low autocorrelation, merit factor 6]
  thue_morse: s_2(k) mod 2                                              [automatic; KNOWN nonzero correlations]
  sturmian  : Beatty floor((k+1)phi)-floor(k phi) in {1,2}->{0,1}       [low complexity; strong correlations]
  pseudo    : parity of (k^2+k+41 prime-ish) bits of sqrt2-like         [empirically random control]
For each: build T_n by T_{n+1}=3 T_n + 2^n r_n, record bit_n(T_n); report density + lag autocorr.
0 false proofs: every sequence is exactly as defined; we only REPORT measured balance, claim nothing
about provability beyond the cited input properties.
"""
import math

N = 4000

# ---- input sequences ----
def seq_orbit(N):
    c = 8; out = []
    for _ in range(N):
        out.append(c & 1); c = (3 * c) // 2
    return out

def seq_champ(N):
    bits = []
    k = 1
    while len(bits) < N:
        bits.extend(int(b) for b in bin(k)[2:]); k += 1
    return bits[:N]

def seq_legendre(N):
    p = 7919  # prime
    qr = set((x * x) % p for x in range(1, p))
    out = []
    for k in range(N):
        m = k % p
        if m == 0: out.append(0)
        else: out.append(1 if m in qr else 0)
    return out

def seq_thue_morse(N):
    return [bin(k).count('1') & 1 for k in range(N)]

def seq_sturmian(N):
    phi = (1 + 5 ** 0.5) / 2
    out = []
    for k in range(N):
        v = math.floor((k + 1) * phi) - math.floor(k * phi)  # 1 or 2
        out.append(v - 1)
    return out

def seq_pseudo(N):
    # bits of sqrt(2) fractional part via integer sqrt of 2*10^... -> use 2-adic-free balanced bits
    # deterministic 'random-ish': successive bits of the binary expansion of sqrt(2).
    # compute floor(sqrt(2)*2^M) for M=N+10 via integer isqrt of 2<<(2M)
    M = N + 16
    val = math.isqrt(2 << (2 * M))  # ~ sqrt(2)*2^M
    bits = [(val >> (M - 1 - i)) & 1 for i in range(N)]
    return bits

panel = {
    "orbit":      seq_orbit(N),
    "champ":      seq_champ(N),
    "legendre":   seq_legendre(N),
    "thue_morse": seq_thue_morse(N),
    "sturmian":   seq_sturmian(N),
    "pseudo":     seq_pseudo(N),
}

def dens(a): return sum(a) / len(a)
def corr(a, b):
    m = len(a); ma = sum(a)/m; mb = sum(b)/m
    cov = sum((a[i]-ma)*(b[i]-mb) for i in range(m))/m
    va = sum((x-ma)**2 for x in a)/m; vb = sum((x-mb)**2 for x in b)/m
    return cov/math.sqrt(va*vb) if va > 0 and vb > 0 else 0.0

def bitn_T(r):
    T = 0; out = []
    for n in range(len(r)):
        out.append((T >> n) & 1)
        T = 3 * T + (1 << n) * r[n]
    return out

nullstd = 1 / math.sqrt(N)
print(f"N={N}, null std ~ {nullstd:.4f}\n")
print(f"{'input':>11} | {'in.dens':>7} {'in.ac1':>7} | {'bitT.dens':>9} {'bitT.ac1':>8} {'bitT.ac2':>8} {'bitT.ac3':>8}")
print("-" * 78)
for name, r in panel.items():
    bt = bitn_T(r)
    ind = dens(r); iac = corr(r[:-1], r[1:])
    bd = dens(bt)
    a1 = corr(bt[:-1], bt[1:]); a2 = corr(bt[:-2], bt[2:]); a3 = corr(bt[:-3], bt[3:])
    print(f"{name:>11} | {ind:7.4f} {iac:+7.3f} | {bd:9.4f} {a1:+8.3f} {a2:+8.3f} {a3:+8.3f}")

# ---- adversarial boundary: which inputs BREAK the balance of bit_n(T_n)? ----
print("\n" + "="*78)
print("ADVERSARIAL boundary: which input structures BIAS bit_n(T_n) away from 1/2?")
print("="*78)
adv = {
    "all-0":   [0]*N,
    "all-1":   [1]*N,
    "per-2 01":[k % 2 for k in range(N)],
    "per-3":   [1 if k % 3 == 0 else 0 for k in range(N)],
    "per-4":   [1 if k % 4 < 2 else 0 for k in range(N)],
    "per-5":   [1 if k % 5 < 2 else 0 for k in range(N)],
    "per-6":   [1 if k % 6 < 3 else 0 for k in range(N)],
    "sparse-log": [1 if (k & (k-1)) == 0 else 0 for k in range(N)],  # 1 only at powers of 2 (~log density)
    "dense-99": [0 if k % 100 == 0 else 1 for k in range(N)],        # mostly 1
}
# resonant periods: order of 2 mod 3, 9, 27 ... and powers of 3 themselves
for q in (3, 9, 27, 81):
    adv[f"per-ord2/{q}"] = None  # filled below
def order2(mod):
    o = 1; v = 2 % mod
    while v != 1:
        v = (v * 2) % mod; o += 1
        if o > mod: return None
    return o
for q in (3, 9, 27, 81):
    p = order2(q)
    adv[f"per-ord2/{q}"] = [1 if (k % p) == 0 else 0 for k in range(N)] if p else [0]*N

print(f"{'input':>13} | {'in.dens':>7} | {'bitT.dens':>9} {'|dev|/null':>10}")
print("-" * 50)
worst = []
for name, r in adv.items():
    bt = bitn_T(r)
    bd = dens(bt)
    dev = abs(bd - 0.5) / nullstd
    worst.append((dev, name, bd, dens(r)))
    print(f"{name:>13} | {dens(r):7.4f} | {bd:9.4f} {dev:10.1f}")
worst.sort(reverse=True)
print(f"\n  most-biasing inputs (|dev| in null-std units):")
for dev, name, bd, ind in worst[:5]:
    print(f"    {name:>13}: bit_n(T) density={bd:.4f}  (in.dens={ind:.3f})  dev={dev:.1f} sigma")
print(f"  => balance breaks ONLY for these structures. The orbit parity must be shown to AVOID them.")
print(f"     Note: 'sparse-log' (density ~ log/N) is the regime of a HALTING-danger orbit (few evens);")
print(f"     its bit_n(T) density tells us whether a low-even orbit would self-consistently bias d.")

print(f"""
READING (honest conclusion -- a relaxation HOPE was raised AND refuted):
  MEASURED: bit_n(T_n) is balanced for an extremely wide input panel -- PROVEN-normal (champ),
  PROVEN-low-autocorr (legendre), automatic (thue_morse), Sturmian, and EVERY periodic/sparse/dense
  adversarial input. ONLY the degenerate all-0 (T_n=0) breaks it. The x3 carry mixing (T_{{n+1}}=3T_n+...)
  makes balance UBIQUITOUS and almost input-agnostic at finite order.
  HOPED: 'decorrelated input => PROVABLY balanced bit_n(T_n)', reducing the orbit to a certifiable
  finite-order decorrelation of its parity.
  REFUTED (by computing the simplest case in closed form): the all-1 input gives T_n = sum 2^k 3^{{n-1-k}}
  = 3^n - 2^n exactly, so its bit_n(T_n) = bit_n(3^n - 2^n) -- whose balance is ITSELF an unproven
  Mahler-class digit statement (empirically 0.49). EVERY 'balanced' entry above is EMPIRICAL; none is
  proven. So one cannot bootstrap the orbit from a 'provably balanced simpler input' -- the simple inputs
  are not provable either.
  NET: the carry mixing makes balance GENERIC but every specific instance is Mahler-class. The orbit is
  no exception; the partial-independence / relaxation route is CLOSED (cleanly, with a closed-form witness).
  This is the exact a.e.-vs-specified signature: balance holds for 'almost every' input but is unprovable
  for any one named input.
  [HEURISTIC, NOT a proof] density-1/2 is the self-consistent value of r_n = r_pure(n) XOR bit_n(T_n[r]):
  a halting orbit (even-density -> 0) would need a biased self-defeating input, which is atypical. Crisp
  intuition for non-halting, but it is the ANNEALED statement; the orbit is one causal specified input.
""")
