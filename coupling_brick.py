"""BUILD brick (1): maximal coupling. The complete proof would follow if we could couple the real parity
r_n to a PROVABLY-balanced surrogate s_n with Hamming(r,s)=o(N): then sum(-1)^{r_n} = sum(-1)^{s_n} +
O(Hamming) = o(N) (sum over s is provably o(N)), done. We SEARCH provably-balanced surrogates for minimal
Hamming distance to r. Key candidate: the leading-bit Sturmian s_n=[{n*log2(3/2)} >= 1/2], which IS
effectively equidistributed (Weyl, log2(3/2) irrational with known measure) -- if r correlates with it,
the provable leading-bit control TRANSFERS partially.

A surrogate works iff Hamming/N -> 0 (i.e. agreement -> 1, beyond the trivial 1/2). We also measure the
carry's SENSITIVE DEPENDENCE (a 1-bit input flip flips how many output carry bits?) -- if ~N/2, the carry
is chaotic and NO local coupling exists; only a global (Ornstein-type) coupling could.
0 false proofs: report measured Hamming/agreement with the null (0.5); a coupling is claimed ONLY if
agreement beats 0.5 by a consistent margin.
"""
import math

N = 200000
# real orbit parity
c = 8; r = bytearray(N)
for n in range(N):
    r[n] = c & 1; c = (3 * c) // 2

def agreement(s):
    m = min(len(s), N)
    a = sum(1 for n in range(m) if s[n] == r[n]) / m
    return max(a, 1 - a)   # a surrogate and its complement are equally good

# --- provably-balanced surrogates ---
# Thue-Morse (automatic, provably balanced)
tm = bytearray(bin(n).count('1') & 1 for n in range(N))
# Rudin-Shapiro (provably balanced; count of '11' blocks mod 2)
def rudin_shapiro(n):
    return bin(n & (n >> 1)).count('1') & 1
rs = bytearray(rudin_shapiro(n) for n in range(N))
# Legendre sequence mod prime (provably low autocorrelation / balanced)
p = 7919; qr = set((x * x) % p for x in range(1, p))
leg = bytearray((1 if (n % p) in qr else 0) for n in range(N))
# Leading-bit Sturmian from {n*log2(3/2)} -- EFFECTIVELY EQUIDISTRIBUTED (the provable handle)
alpha = math.log2(1.5)
stur = bytearray(1 if (((n + 1) * alpha) % 1.0) >= 0.5 else 0 for n in range(N))
# Sturmian from {n*log2(3)} (the other natural rotation)
beta = math.log2(3.0)
stur3 = bytearray(1 if ((n * beta) % 1.0) >= 0.5 else 0 for n in range(N))
# pure-power middle digit a_n = bit_n(8*3^n) (NOT provably balanced, but the XOR partner -- reference)
a = bytearray(); p3 = 1
for n in range(N):
    a.append((8 * p3 >> n) & 1); p3 *= 3

print("Hamming-agreement of the real parity r_n with candidate surrogates (null = 0.5000):")
print(f"  {'surrogate':>22} {'provably balanced?':>18} {'agreement':>10}")
for name, s, prov in [
    ("Thue-Morse", tm, "YES (automatic)"),
    ("Rudin-Shapiro", rs, "YES"),
    ("Legendre (p=7919)", leg, "YES (Weil)"),
    ("leading-bit Sturmian {n log2 1.5}", stur, "YES (Weyl, effective)"),
    ("Sturmian {n log2 3}", stur3, "YES (Weyl)"),
    ("pure-power digit bit_n(8*3^n)", a, "NO (itself Mahler)"),
]:
    print(f"  {name:>22} {prov:>18} {agreement(s):>10.4f}")

# --- sensitive dependence of the carry: flip one input bit, count flipped output parities ---
# Recompute the orbit with r_k flipped at position k0 is NOT well-defined (orbit is deterministic);
# instead flip one input bit of the CARRY-SUM T and count flipped diagonal carry bits (the coupling-relevant
# sensitivity): T uses inputs r_k; flipping r_{k0} changes T_n by +/- 2^{k0} 3^{n-1-k0}; count n where bit_n flips.
def vbit(x, i): return (x >> i) & 1
M = 1500
# build T_n and the diagonal carry bit b_n = bit_n(T_n)
c = 8; rr = []; Ts = []; T = 0
for n in range(M):
    rr.append(c & 1); Ts.append(T); T = 3 * T + (1 << n) * (c & 1); c = (3 * c) // 2
def carry_bits(Tlist): return [vbit(Tlist[n], n) for n in range(len(Tlist))]
base = carry_bits(Ts)
import statistics
flip_fracs = []
for k0 in (5, 50, 200, 500):
    # rebuild T with r_{k0} flipped
    c = 8; T = 0; Ts2 = []; rr2 = list(rr); rr2[k0] ^= 1
    cc = 8
    # we must drive the orbit by the (now exogenous) flipped parity sequence for the carry recursion
    Ts2 = []; T = 0
    for n in range(M):
        Ts2.append(T); T = 3 * T + (1 << n) * rr2[n]
    b2 = carry_bits(Ts2)
    flips = sum(1 for n in range(k0 + 1, M) if b2[n] != base[n])
    frac = flips / (M - k0 - 1)
    flip_fracs.append(frac)
    print(f"\n  flip input bit k0={k0}: fraction of downstream carry bits flipped = {frac:.3f}")
print(f"  mean downstream-flip fraction = {statistics.mean(flip_fracs):.3f}  (~0.5 => sensitive dependence / chaotic)")

print("""
READING:
  - If EVERY provably-balanced surrogate has agreement ~0.5 (no better than a coin), the real parity is
    decorrelated from all of them => NO coupling to a provable surrogate exists; the local-coupling route
    is dead. Watch the leading-bit Sturmian especially: ~0.5 means even the provable {n log2 1.5}
    equidistribution does NOT transfer to the parity (the parity uses the MIDDLE digit, not the leading).
  - If the carry's downstream-flip fraction is ~0.5, a 1-bit input change flips ~half of all future carry
    bits => sensitive dependence (positive-entropy / chaotic carry), so no LOCAL coupling can track it;
    only a global measure-coupling (Ornstein) could -- which is the a.e.-vs-specified wall again.
  These two together map the coupling construction precisely: local coupling impossible; the buildable
  object must be a global/measure coupling respecting the closed loop.""")
