"""Make the FLP 'support-vs-frequency' gap CONCRETE on the Antihydra orbit, and measure the safety margin
of the balance random walk to the halting boundary.

Findings to anchor (from the proven-partials search):
  - FLP/Dubickas (PROVEN, unconditional): limsup_n {xi(3/2)^n} - liminf_n {xi(3/2)^n} >= 1/p = 1/3.
    This bounds the SUPPORT (spread) of the fractional parts -- NOT the frequency. Striking: 1/3 also =
    the non-halt threshold (even-density >= 1/3), both from the '3' in x3.
  - No proven one-sided DENSITY bound exists; the gap is 'kind, not size' (support vs time-average).
We show on the real orbit: the FLP spread is satisfied with HUGE margin (≈ full circle), while the
even-density (the actual constraint) hovers near 1/2 with a modest but positive margin above 1/3.
And balance_n = 3 E_n - n: its running MINIMUM = the closest the orbit ever comes to halting.
0 false proofs: we only REPORT measured trajectories; the spread >= 1/3 is the proven FLP fact, the
even-density staying >= 1/3 is the OPEN conjecture (we report the empirical margin, not a proof).
"""
import math

N = 500_000
c = 8
E = 0          # running #even
balance = 0    # 3E - n
min_balance = 0
min_balance_n = 0
min_density = 1.0
min_density_n = 0
# also track fractional parts of 8*(3/2)^n for the FLP spread (use floats with periodic renorm via the orbit)
# {8*(3/2)^n} -- track frac of c_n / 2^? Instead track the true frac via high-precision: use the orbit's
# own low bits as a proxy is wrong; instead track theta_n = frac(8 * (1.5)^n) via log to avoid overflow:
# theta_n = frac( exp( ln8 + n ln1.5 ) ) is imprecise for large n. Use exact: frac(8*3^n/2^n) = (8*3^n mod 2^n)/2^n.
fracs_min = 1.0; fracs_max = 0.0
p3 = 1; p2 = 1
checkpts = [10, 100, 1000, 10000, 100000, N-1]
print(f"orbit c_{{n+1}}=floor(3c/2), c_0=8, N={N}")
print(f"{'n':>9} {'E_n/n':>9} {'balance=3E-n':>13} {'frac-spread':>11}")
for n in range(1, N + 1):
    even = (c & 1) == 0
    if even: E += 1
    balance = 3 * E - n
    if balance < min_balance:
        min_balance = balance; min_balance_n = n
    dens = E / n
    if n > 100 and dens < min_density:
        min_density = dens; min_density_n = n
    # exact fractional part of 8*(3/2)^n = (8*3^n mod 2^n)/2^n -- only cheap for small n
    if n <= 4000:
        fr = ((8 * p3) % p2) / p2
        if fr < fracs_min: fracs_min = fr
        if fr > fracs_max: fracs_max = fr
        p3 *= 3; p2 <<= 1   # stop growing these monsters after n=4000
    c = (3 * c) // 2
    if n in checkpts:
        spread = fracs_max - fracs_min if n <= 4000 else float('nan')
        print(f"{n:>9} {E/n:>9.5f} {balance:>13d} {spread:>11.4f}")

print("\n" + "="*72)
print("RESULTS")
print("="*72)
print(f"even-density E_n/n at N: {E/N:.5f}  (conjectured -> 1/2; non-halt needs >= 1/3 for ALL n)")
print(f"worst (min) even-density over n>100: {min_density:.5f} at n={min_density_n}")
print(f"  => empirical margin above 1/3: {min_density - 1/3:+.5f}  (POSITIVE = stays non-halting so far)")
print(f"balance = 3E_n - n: value at N = {3*E-N}, running MIN = {min_balance} at n={min_balance_n}")
print(f"  => the orbit's closest approach to the halting boundary (balance<0) is {min_balance}")
print(f"     (bbchallenge: never observed to go negative; halting would need balance < 0)")
print(f"FLP fractional-part spread (n<=4000): [{fracs_min:.4f}, {fracs_max:.4f}] = {fracs_max-fracs_min:.4f}")
print(f"  => PROVEN (FLP) spread >= 1/3 = 0.3333; empirically ~{fracs_max-fracs_min:.2f} (near full circle).")
print(f"""
THE GAP, MADE CONCRETE:
  - FLP gives, UNCONDITIONALLY, spread >= 1/3 -- and the orbit's spread is ~{fracs_max-fracs_min:.2f}, satisfied
    with enormous margin. This is the SUPPORT (where the orbit goes), and it is PROVEN.
  - The non-halt condition needs the FREQUENCY (time in the 'even' half) >= 1/3. Empirically the even-
    density sits at ~{E/N:.3f} with worst dip {min_density:.3f} (margin {min_density-1/3:+.3f} above 1/3), but this is
    the OPEN conjecture -- FLP's support bound implies NOTHING about it (a sequence can span the whole
    circle yet visit the even half a vanishing fraction of the time).
  - So the proven 1/3 (support) and the needed 1/3 (frequency) are the SAME NUMBER on DIFFERENT AXES;
    the gap is of KIND, not size. This is the precise statement for the kernel's 'closest proven result'.
""")
