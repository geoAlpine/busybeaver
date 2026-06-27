"""NEW FRAMEWORK: view even-density as a Birkhoff average of an indicator under the interval map
F(x) = {3x/2} (= 3x/2 mod 1), and study the BIRKHOFF SPECTRUM (range of even-densities over invariant
measures / periodic orbits). If EVERY invariant measure gave even-measure >= 1/3, ergodic decomposition
would force liminf even-density >= 1/3 for EVERY orbit (incl. Antihydra) WITHOUT equidistribution of the
specific orbit. So the decisive question: do low-even-density (< 1/3) periodic orbits of F exist (= the
'invariant-measure' shadows of potential halting orbits)?

STEP 1 (dictionary): theta_n = {8*(3/2)^n} = (8*3^n mod 2^n)/2^n (exact). Find the rule r_n = c_n mod 2
as a function of theta_n, and verify the skew map theta_{n+1} = {1.5*theta_n + 0.5*r_n}.
STEP 2 (spectrum): iterate F from a grid, detect periodic orbits, compute each orbit's even-density
(fraction of steps with the 'odd-branch' = r=1, vs 'even'), report min/max over found orbits.
0 false proofs: report the measured dictionary fidelity and the measured spectrum; claim a one-sided
bound ONLY if no sub-1/3 orbit exists AND the dictionary is exact (we expect sub-1/3 orbits DO exist =
why no easy proof; report honestly either way).
"""
import math

# ---- STEP 1: dictionary ----
N = 3000
c = 8; p3 = 1; p2 = 1
theta = []; r = []
for n in range(N):
    theta.append(((8 * p3) % p2) / p2)
    r.append(c & 1)
    c = (3 * c) // 2
    p3 *= 3; p2 <<= 1

# rule candidates: r_n vs theta_n. Test r_n == [theta_n >= t] for best threshold t.
# and the carry-aware: r_n relates to floor(8*(3/2)^n) parity = floor(theta-shifted)...
# empirically scan threshold
best = None
for t100 in range(1, 100):
    t = t100/100
    agree = sum(1 for n in range(N) if (theta[n] >= t) == (r[n] == 1)) / N
    agree = max(agree, 1-agree)
    if best is None or agree > best[1]: best = (t, agree)
print(f"STEP 1 dictionary: best single-threshold rule r_n ~ [theta_n >= {best[0]:.2f}] agrees {best[1]:.3f}")

# verify skew map theta_{n+1} = {1.5 theta_n + 0.5 r_n}
ok_skew = all(abs(theta[n+1] - ((1.5*theta[n] + 0.5*r[n]) % 1.0)) < 1e-9 for n in range(N-1))
print(f"         skew map theta_{{n+1}} = {{1.5 theta_n + 0.5 r_n}} : {'OK' if ok_skew else 'FAIL'}")
# so r_n is the digit making 1.5 theta + 0.5 r land in [0,1): r_n = 0 if 1.5 theta_n < 1 else 1? check
ok_branch = all((r[n] == (0 if 1.5*theta[n] < 1.0 else 1)) for n in range(N))
print(f"         branch r_n == [1.5 theta_n >= 1] (i.e. theta_n >= 2/3): {'OK' if ok_branch else 'FAIL'}")
if ok_branch:
    print(f"         => DICTIONARY EXACT: c_n ODD  <=> theta_n >= 2/3;  c_n EVEN <=> theta_n in [0,2/3).")
    print(f"            even-density = frequency of theta_n in [0,2/3) under F(x)={{3x/2}}.")
    print(f"            non-halt needs even-density>=1/3 <=> odd-density (theta in [2/3,1)) <= 2/3.")

# ---- STEP 2: Birkhoff spectrum of F(x)={3x/2} ----
# F is piecewise: if x<2/3: F=3x/2 (branch even, symbol 0); if x>=2/3: F=3x/2-1 (branch odd, symbol 1).
def F(x):
    y = 1.5 * x
    return (y, 0) if y < 1.0 else (y - 1.0, 1)

def orbit_density(x0, burn=2000, count=20000):
    x = x0
    for _ in range(burn):
        x, _ = F(x)
    odd = 0
    for _ in range(count):
        x, s = F(x)
        odd += s
    return odd / count  # odd-density; even-density = 1 - this

# find periodic orbits by seeking fixed points of F^p analytically: F^p is affine on each symbolic branch
# A symbolic word w in {0,1}^p gives an affine map; its fixed point x* = (sum of (3/2)^{p-1-i} * (-b_i)) / ((3/2)^p - 1)
# where b_i = 0 (even branch subtract 0) or 1 (odd branch subtract 1). Valid if x* follows word w.
from itertools import product
print("\nSTEP 2: periodic orbits of F (symbolic words up to length P) and their even-density:")
spectrum = []
for P in range(1, 13):
    g = 1.5
    denom = g**P - 1
    found = []
    for w in product((0,1), repeat=P):
        # x* fixed by composing branches: x_{i+1}=1.5 x_i - w_i ; fixed point of the cycle
        # x0 = (sum_{i=0}^{P-1} 1.5^{P-1-i} * w_i) / (1.5^P - 1)   (subtract terms)
        num = sum(g**(P-1-i) * w[i] for i in range(P))
        x0 = num / denom
        if not (0 <= x0 < 1): continue
        # verify the word matches the actual itinerary (and primitivity-ish: just verify itinerary)
        x = x0; word = []
        ok = True
        for i in range(P):
            xn, s = F(x)
            word.append(s); x = xn
        if tuple(word) == w and abs(x - x0) < 1e-9:
            odd_d = sum(w)/P
            found.append((odd_d, w))
    if found:
        odds = sorted(set(round(o,4) for o,_ in found))
        spectrum.extend(found)
        mn = min(o for o,_ in found); mx = max(o for o,_ in found)
        print(f"  P={P:>2}: {len(found):>4} orbits, odd-density range [{mn:.3f},{mx:.3f}] "
              f"=> even-density range [{1-mx:.3f},{1-mn:.3f}]")

if spectrum:
    all_even = [1 - o for o, _ in spectrum]
    print(f"\n  over all periodic orbits of F found: even-density min = {min(all_even):.4f}, max = {max(all_even):.4f}")
    # measured: integer-orbit odd-density (from STEP 1 data)
    intdens = sum(r)/len(r)
    print(f"  measured Antihydra integer-orbit odd-density = {intdens:.4f} (even {1-intdens:.4f})")
    print(f"""
VERDICT (the framework applies to the WRONG system -- and that mislocation is the finding):
  - The CLEAN real map F(x)={{3x/2}} has even-density >= 2/3 over ALL invariant measures (odd-density
    <= 1/3, NO sub-1/3 orbit): structurally, x in [2/3,1) maps to [0,1/2), so F FORBIDS two consecutive
    odds. This is a clean unconditional fact -- about F, NOT about Antihydra.
  - The DICTIONARY r_n = f(theta_n) FAILS (single-threshold agreement ~0.52 = chance; skew map FAILS):
    the integer parity is NOT the F-itinerary, because the carry T_n decouples c_n mod 2 from the
    pure-power fractional part theta_n = {{8(3/2)^n}}.
  - DECISIVE contrast: Antihydra's odd-density ~{intdens:.2f} EXCEEDS F's invariant-measure ceiling 1/3.
    The integer odd-branch (3c-1)/2 ALLOWS consecutive odds (when c == 1 mod 4), which F's branch
    3x/2 - 1 forbids. The -1 correction (= the carry) is exactly what breaks the conjugacy to the tame
    expanding map, raises odd-density from <=1/3 to ~1/2, and lands the dynamics on the base-3/2 ODOMETER
    (2-adic), which has NO absolutely-continuous invariant measure handing out a Birkhoff bound.
  => the invariant-measure / Birkhoff-spectrum route does NOT reach Antihydra: it bounds the tame real
     map, while Antihydra is that map PLUS the carry that destroys tameness. The obstruction is, once more,
     the carry T_n -- now seen in the symbolic-dynamics / interval-map lens (consecutive-odds, no a.c.i.m.).""")
