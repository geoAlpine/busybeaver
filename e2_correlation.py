"""E2 -- the designated research theme (per the ChatGPT meeting): can the correlation expansion of the
self-generation feedback be made a theorem?
    ||F|| (the closed-loop feedback) = a_annealed + sum_h K(h) C(h),  a_annealed = 0 (measured),
where C(h) = autocovariance of the orbit's parity (the scenery) and K(h) = the carry kernel (response of the
output carry density to a lag-h input correlation). The research target: bound  sum_h |K(h)| |C(h)| < 1.

This script does the CLEAN half precisely -- measure C(h) (a trustworthy autocorrelation) and its decay --
and states the theorem target. The K(h) kernel is the hard/open half (its single-flip estimate was noise-
dominated, sensitivity_profile.py); it is left as the research theme, NOT forced here.
0 false proofs: C(h) is a clean measured autocovariance with a null band; no claim about K(h) or a bound.
"""
import math

N = 500_000
c = 8
r = bytearray(N)
for n in range(N):
    r[n] = c & 1; c = (3 * c) // 2

mu = sum(r) / N
def autocov(h):
    s = 0
    for n in range(N - h):
        s += (r[n] - mu) * (r[n + h] - mu)
    return s / (N - h)
var = autocov(0)
nullstd = 1.0 / math.sqrt(N)        # ~1 sigma band on the normalized autocorrelation
print(f"orbit parity: mean={mu:.5f}, var={var:.5f}, N={N}")
print(f"C(h) = normalized parity autocorrelation (null band ~ {nullstd:.4f}); the 'C' factor of E2")
print(f"  {'h':>4} {'C(h)':>10} {'/null':>7}")
maxc = 0.0
for h in [1, 2, 3, 4, 5, 8, 13, 21, 34, 55, 100, 200, 500, 1000]:
    ch = autocov(h) / var
    maxc = max(maxc, abs(ch))
    flag = "  <== signal?" if abs(ch) > 4 * nullstd else ""
    print(f"  {h:>4} {ch:>+10.5f} {ch/nullstd:>+7.1f}{flag}")
print(f"  max |C(h)| over tested lags = {maxc:.5f}   (4-sigma band = {4*nullstd:.4f})")

print(f"""
READING (E2 research theme):
  - C(h) [CLEAN, measured]: the orbit parity autocorrelation is ~null at every tested lag (|C(h)| within a
    few sigma of 0; max {maxc:.4f}). So the 'C' factor of E2 is empirically tiny/decaying -- the scenery is
    i.i.d.-indistinguishable at the correlation level. PROVING C(h) -> 0 fast is itself part of the mixing
    (= the orbit's own equidistribution), so it is not free; but it is the measurable, structured half.
  - K(h) [the open half]: the carry kernel -- response of the output carry density to a lag-h input
    correlation. Its single-flip estimate is noise-dominated (sensitivity_profile.py). A clean K(h) and a
    bound sum_h |K(h)| |C(h)| < 1 is the THEOREM TARGET. Candidate tools: a Mauduit-Rivat carry-lemma /
    Gowers-norm bound on K(h) (carry-propagation decay), combined with the measured C(h) decay.
  - STATUS: E2 is the live research theme toward the complete proof. The framework reduces the proof to
    ||F||<1; ||F|| = sum_h K(h) C(h) with C measured ~0 and K the open carry kernel. Making this a theorem
    (a quantitative carry-kernel bound x correlation decay) is the next research step -- NOT resolved here.""")
