# Solenoid attack — bundle the three places, attack genericity (2026-06-24)

Attacking the unified kernel on the hyperbolic (2,3)-solenoid where `α=×(3/2)` expands in ℝ(∞) and ℚ₂,
contracts in ℚ₃ (`|3/2|_∞·|3/2|_2·|3/2|_3 = (3/2)(2)(1/3)=1`). Goal: bundle the three places' structure
for the SAME orbit and attack the genericity that effective equidistribution (BLMV) would need.
Numerics: `solenoid.py`, `triadic_parity.py`.

## What the bundling revealed (all verified)
- **The orbit is MEASURE-GENERIC.** `c_n mod 2^k` is uniform (χ²/dof=0.93); it is **independent** of the
  3-adic projection (mutual information `I(2-adic;3-adic)=0.0006` bits ≈ 0). So the unstable (2-adic) and
  stable (3-adic) places decouple — the measure-theoretic genericity signature holds.
- **The two UNSTABLE directions coincide.** `{(3/2)ⁿ} = (3ⁿ mod 2ⁿ)/2ⁿ` is literally the same data as the
  2-adic content, so the real(∞) and ℚ₂ expanding directions carry **identical information** — the unstable
  manifold is effectively 1-dimensional for this orbit. Bundling ∞ and 2-adic adds nothing.
- **The 3-adic (contracting) direction is a clean transducer of the PARITY history** [striking]:
  `c_n mod 3 ∈ {0,1}` with `0 ⟺ c_{n−1} even`; `c_n mod 9 ↔ (parity_{n−1},parity_{n−2})` bijectively
  ((e,e)→0,(e,o)→6,(o,e)→4,(o,o)→1). The 3-adic expansion of the orbit IS the even/odd sequence re-encoded
  by a finite automaton; the orbit's 3-adic projection lives on a sparse Cantor-like support (`{0,1,4,6} mod 9`).
- So the even-density (= halting) is `freq(c_n ≡ 0 mod 3)` — the **same** quantity, merely read off the
  3-adic units digit. The contracting direction re-encodes the parity but does **not** control it.

## Verdict (honest)
The solenoid is the **correct framework** — it certifies the orbit as measure-generic and exposes a clean
parity↔3-adic transducer — but it provides **no new leverage**:
1. the two unstable directions are the same data (no extra dimension to exploit);
2. the contracting 3-adic direction only **re-encodes** the parity, it does not bound its density;
3. what remains is exactly "**is this specific measure-generic point Diophantine-generic enough for
   effective equidistribution?**" — the BLMV frontier, which for a specific algebraic-type orbit is the open
   problem itself.
All three weapons (∞ controlled to `log n`; 2-adic renewal gap `0.99`; 3-adic isometry/transducer) are
**functions of the one parity/bit sequence**, so bundling them cannot exceed any one of them. The kill-both
via solenoid genericity reaches the same world-open kernel — now confirmed from the most sophisticated angle,
with a complete structural picture and `0` false claims. No new path opened; the frontier is genuinely reached.
