"""Improve the PROVEN complexity floor from slope 1 (Morse-Hedlund, p(l)>=l+1) to slope log_{3/2}(2)~1.71,
elementarily, via the bijection lemma + the orbit's strict monotonic growth.

LEMMA (bijection, proven earlier): p(l) = #{ c_n mod 2^l : n>=0 } = number of residues mod 2^l visited.
THEOREM (elementary): p(l) >= #{ n : c_n < 2^l } >= (l-3)/log2(3/2) ~ 1.71*l - 5.
PROOF: the orbit is strictly increasing (c_{n+1}=floor(3c_n/2) > c_n for c_n>=2; c_0=8), so c_0<c_1<...
are distinct integers. All c_n with c_n < 2^l are distinct integers in [8, 2^l), hence DISTINCT mod 2^l,
contributing distinct residues => p(l) >= #{n: c_n < 2^l}. And c_n <= 8*(3/2)^n (since each step multiplies
by <= 3/2), so 8*(3/2)^n < 2^l  (i.e. n < (l-3)/log2(3/2))  forces c_n < 2^l; there are >= (l-3)/log2(3/2)
such n. QED.
Slope log_{3/2}(2) = 1/log2(3/2) = log2/log(3/2) ~ 1.7095 -- MATCHES the Dubickas (2009) liminf bound
p_w(l)/l >= log q/log(p/q) for base-p/q minimal words (here log2/log(3/2)), re-derived elementarily.
0 false proofs: the bound is the elementary argument above; the script certifies its premises and that the
first m(l) orbit values are genuinely distinct mod 2^l.
"""
import math

LOG = 1.0 / math.log2(3/2)   # = log_{3/2}(2) ~ 1.7095
print(f"slope constant log_{{3/2}}(2) = 1/log2(3/2) = {LOG:.4f}")
print(f"(Dubickas base-p/q liminf p_w(l)/l >= log q/log(p/q) = log2/log(3/2) = {math.log(2)/math.log(3/2):.4f})")

def T(c): return (3*c)//2

# verify: count n with c_n < 2^l, check those c_n are distinct mod 2^l, and compare to the bound + to true p(l)
def phi(c, l):
    w = 0
    for _ in range(l):
        w = (w<<1)|(c&1); c=T(c)
    return w

print(f"\n{'l':>3} {'#(c_n<2^l)':>10} {'bound 1.71(l-3)':>15} {'distinct mod 2^l?':>17} {'true p(l)':>10}")
for l in range(4, 22):
    # count orbit values below 2^l
    c = 8; vals = []
    cap = 1 << l
    while c < cap:
        vals.append(c); c = T(c)
    m = len(vals)
    distinct = len(set(v & (cap-1) for v in vals)) == m   # distinct mod 2^l (must be true: distinct ints < 2^l)
    bound = (l-3)*LOG
    # true p(l) = number of distinct residues mod 2^l visited over a long run = #distinct length-l factors
    c = 8; res = set()
    for _ in range(min(1<<(l+2), 400000)):
        res.add(c & (cap-1)); c = T(c)
    truep = len(res)
    print(f"{l:>3} {m:>10} {bound:>15.1f} {str(distinct):>17} {truep:>10}")

print(f"""
=> #(c_n < 2^l) tracks ~1.71*l (the first ~1.71*l orbit values are below 2^l and, being distinct integers,
   distinct mod 2^l), so p(l) >= 1.71*l - O(1) is PROVEN elementarily -- slope log_{{3/2}}(2)~1.71 > 1,
   strictly better than Morse-Hedlund's l+1, and matching the Dubickas literature liminf constant.
   (The true p(l) is far higher -- toward 2^l -- but that maximal growth is the Mahler-class part.)

PROVEN FLOOR (updated, elementary, no Mahler):
   eventually-periodic  <  Sturmian (p=l+1)  <  p(l) >= 1.71*l  [our slope bound]   <<  p(l)=2^l [Mahler].
   The certificate-hierarchy placement of the Antihydra parity now has an explicit proven linear floor of
   slope log_{{3/2}}(2), tying the elementary complexity bound to the base-3/2 growth rate; the gap to
   maximal complexity (full non-automaticity) is exactly the specified-orbit equidistribution = Mahler.""")
