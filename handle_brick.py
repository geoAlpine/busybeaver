"""BUILD: attack line (5) (orbit Haar-genericity) via the ONLY provable handle -- the effective
equidistribution of the leading phase theta_n = {n*log2(3/2)} (Weyl + effective discrepancy; log2(3/2)
irrational with known measure).

THE TEST (higher-order than the linear coupling brick): condition the even-indicator on the leading phase.
  - If P(c_n even | theta_n in bin) VARIES with the bin, then even-density = integral over the
    EQUIDISTRIBUTED theta of a computable conditional density => the provable phase-equidistribution
    TRANSFERS to effective control of even-density => a handle for (5).
  - If it is FLAT (~0.5 in every bin), the parity is independent of the leading phase at this order too,
    and the leading-bit handle is definitively closed for (5).
Also test: gaps g_n=v2(c_n-1) vs theta_n, and the actual orbit phase {log2 c_n}.
0 false proofs: report the conditional even-density per bin with its sampling band; a 'handle' is claimed
ONLY if the variation across bins beats the per-bin sampling noise by a clear margin.
"""
import math

N = 400_000
alpha = math.log2(1.5)          # provably-equidistributed rotation number
def log2_big(c):
    """{log2 c} safe for huge ints (math.log2 overflows above ~1024 bits)."""
    m = c.bit_length()
    if m <= 53:
        return math.log2(c)
    top = c >> (m - 53)
    return (m - 53) + math.log2(top)
c = 8
NB = 20
# accumulators: per-bin even count and total, for theta=({n alpha}) and for actual {log2 c_n}
ev_a = [0]*NB; tot_a = [0]*NB
ev_b = [0]*NB; tot_b = [0]*NB
gap_by_bin = [[] for _ in range(NB)]   # gap (v2(c-1)) when odd, binned by theta_n
def v2m1(x):
    x = x-1; r=0
    if x==0: return 0
    while x & 1 == 0: x >>= 1; r += 1
    return r
for n in range(N):
    th = ((n+1)*alpha) % 1.0          # {n alpha}, provable rotation
    bina = int(th*NB) % NB
    even = (c & 1)==0
    ev_a[bina] += even; tot_a[bina] += 1
    # actual orbit leading phase {log2 c_n}
    lb = log2_big(c) % 1.0 if c>0 else 0.0
    binb = int(lb*NB) % NB
    ev_b[binb] += even; tot_b[binb] += 1
    if not even:
        gap_by_bin[bina].append(v2m1(c))
    c = (3*c)//2

overall = sum(ev_a)/N
band = lambda t: (0.5/math.sqrt(t)) if t>0 else 0   # ~1 sigma per-bin band on a density
print(f"overall even-density = {overall:.5f}   (N={N}, per-bin ~ {N//NB} samples)")
print(f"\n(1) even-density conditioned on the PROVABLE leading phase theta_n = {{n log2(3/2)}}:")
print(f"    {'bin (theta)':>12} {'even-density':>12} {'dev from overall':>17} {'(~3 sigma band)':>15}")
maxdev = 0
for i in range(NB):
    d = ev_a[i]/tot_a[i]; dev = d-overall; maxdev=max(maxdev,abs(dev))
    flag = "  <== varies?" if abs(dev) > 3*band(tot_a[i]) else ""
    print(f"    [{i/NB:.2f},{(i+1)/NB:.2f}) {d:>12.4f} {dev:>+17.4f} {3*band(tot_a[i]):>15.4f}{flag}")
print(f"    max |dev across bins| = {maxdev:.4f}   (3-sigma per-bin band ~ {3*band(N//NB):.4f})")

print(f"\n(2) even-density conditioned on the ACTUAL orbit phase {{log2 c_n}}:")
maxdev_b = max(abs(ev_b[i]/tot_b[i]-overall) for i in range(NB) if tot_b[i]>0)
for i in range(0,NB,4):
    d = ev_b[i]/tot_b[i] if tot_b[i] else 0
    print(f"    [{i/NB:.2f},{(i+1)/NB:.2f}) even-density={d:.4f}  dev={d-overall:+.4f}")
print(f"    max |dev across bins| = {maxdev_b:.4f}")

print(f"\n(3) mean gap (v2(c-1) on odd steps) conditioned on theta_n (renewal vs leading phase):")
for i in range(0,NB,4):
    g = gap_by_bin[i]
    print(f"    [{i/NB:.2f},{(i+1)/NB:.2f}) mean gap={sum(g)/len(g):.3f} (n_odd={len(g)})")

print(f"""
VERDICT:
  If max|dev| (~{maxdev:.4f}) is within the 3-sigma per-bin band (~{3*band(N//NB):.4f}), the even-density is
  FLAT across the provable leading phase => the parity is independent of {{n log2(3/2)}} at the conditional-
  density order too. Then the leading-bit equidistribution does NOT transfer, and line (5)'s last arithmetic
  handle is closed (the genericity cannot be supplied by the provable phase). If instead it VARIES beyond
  the band, the provable phase-equidistribution would control the even-density => a genuine crack in (5).
  The numbers decide. (Honest: even if flat, this is the expected result given the middle-digit obstruction;
  if it varies, it is the first handle on (5) and must be pursued.)""")
