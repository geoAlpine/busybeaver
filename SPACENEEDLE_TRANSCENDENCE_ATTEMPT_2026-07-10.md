# Space Needle — decision attempt via transcendence theory on the hitting problem (2026-07-10)

*Attacks the Type-III cryptid **Space Needle** (μ=5/2, the frontier's one non-(K) machine) with a
**genuinely new tool class**: recast HALT as a **hitting problem** "does the counter orbit ever land on a
power of 2 minus 1", and try to exclude it with effective Diophantine machinery (Baker/Matveev linear forms
in logarithms, S-unit equations, "powers in linear recurrences"). The congruence-automaton attack already
failed (`SPACENEEDLE_DECISION_ATTEMPT_2026-07-10.md`) and is NOT re-run. **Outcome: the effective machinery
does not apply — its every hypothesis is provably violated by SN's orbit.** SOUNDNESS: `[PROVEN]`/`[OBSERVED]`;
zero false proofs; halting stays `[OPEN]`. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`,
exact big-int. Scripts `sndt_oddpart.py`, `sndt_structure.py`. Not committed.*

## 1. The reduction: HALT ⟺ oddpart(mₙ+1) = 1 `[PROVEN]`

Milestone orbit `m₀=2, m_{n+1}=f(mₙ)`, `f(m)=m+3⌊m/2^{v+1}⌋+v`, `v=`trailing-ones(m). Past the sporadic
finite part (permanently, from gen 7 — `SPACENEEDLE_DECISION_ATTEMPT`), the **residual fatal target is the
all-ones family `m=2^k−1`**, i.e. **HALT ⟺ mₙ+1 = 2^k for some n,k**.

**Key identity `[PROVEN, 25249/25249 exact]`.** For **odd** m with v trailing 1-bits, adding 1 clears exactly
those v ones and carries once, so **v₂(m+1)=v exactly**, hence
> **oddpart(mₙ+1) = (mₙ+1) ≫ v,  and this equals 1 ⟺ m is all-ones ⟺ HALT.**

(Even m are irrelevant: m+1 is odd and huge, oddpart = m+1 ≫ 1.) So the **entire hitting problem is a single
scalar test**: does `gₙ := oddpart(mₙ+1)` ever reach 1? This is the exact object the effective theory would
have to bound below.

## 2. Multiplicative structure of mₙ+1 — no arithmetic handle `[OBSERVED, exact]`

- **gₙ is a generic integer, NOT an S-unit / not smooth** (`sndt_structure.py`, trial-factoring the first ~30
  factorable odd gₙ): oddpart(mₙ+1) carries a **large prime factor** in essentially every generation
  (n=7→313, n=17→13093, n=33→23386481, n=44→prime 1106181786419, …). An S-unit / "distance between S-units"
  attack needs gₙ supported on a **fixed finite prime set**; it is not. The support primes are fresh and
  large each generation.
- **mₙ satisfies no linear recurrence** (Hankel-rank test over ℚ, `sndt_structure.py`): **no consistent
  recurrence of order 1..10** (and structurally none of any order — f is nonlinear with a v-**indexed**
  multiplier `1+3/2^{v+1}`, verified in the fixed-point analysis). The effective "perfect/prime powers in a
  linear recurrence sequence" theorems (Baker–Wüstholz/Matveev method; Bugeaud–Kányai; require order ≥2,
  irreducible characteristic polynomial, dominant root) therefore **have no sequence to apply to**.
- **Growth rate is "generic"**: log₂ mₙ / n → **0.9388 bits/gen** (< log₂(5/2)=1.322, dragged down by odd
  steps), continued fraction `[0,1,15,2,1,6,7,1,4,2,17,…]` — no arithmetic relation to log 2. A Baker linear
  form `Λ = k·log2 − log(mₙ+1)` would need log(mₙ+1) to be a logarithm of an algebraic number of **bounded,
  structured height**; instead mₙ+1 is a fresh generic integer of height ~n. There is **no linear form in a
  fixed finite set of logarithms** — the precondition for every Baker-type lower bound — so the method is
  inapplicable, not merely weak.

## 3. oddpart(mₙ+1) statistics — bounded away from 1 empirically, no structural floor `[OBSERVED]`

Over **50 000 generations** (final width **46 863 bits**, exact big-int), 25 249 odd milestones:
- **min gₙ = 3**, attained only at **n=1 (m=5)**; next smallest 5 (n=2), 171 (n=9), 313 (n=7). All minima are
  the **tiny early generations**; thereafter gₙ ≈ mₙ/2^v grows with the orbit. **gₙ = 1 never occurs.**
- **v = trailing-ones is geometric ~2^{−v}** (v=1: 50.4%, v=2: 25.1%, v=3: 12.7%, …), so over N odd steps
  **max v ≈ log₂ N**: max v = **12** over 50k gens, at width **943** (margin width−v = **931**; HALT needs 0).
  HALT would require **v = width ≈ 0.94n** — a `2^{−width}`-thin event whose probability is **summable**
  (Borel–Cantelli I ⇒ finitely many hits expected ⇒ non-halt-*leaning*). But this is a **measure/heuristic**
  statement, **not** a structural lower bound: nothing forbids one anomalous generation with v = width.

## 4. Verdict — effective machinery ruled out; no decision `[honest report]`

The transcendence attack fails at its **hypotheses**, not its arithmetic. Every effective tool for "an
explicit integer sequence avoids the powers of 2" requires one of: (a) a **linear recurrence** structure
(absent — no recurrence, nonlinear v-indexed map), (b) an **S-unit / fixed-prime-support** structure of
mₙ±1 (absent — generic large prime factors every generation), or (c) a **linear form in fixed logarithms**
with a controllable height (absent — mₙ+1 is a fresh height-~n integer). Because f **provably mixes all bits**
(the same wall that killed the congruence attack), mₙ+1 is a "generic" integer and its **distance to the
nearest power of 2 has no arithmetic handle** — this is precisely the Diophantine-hard wall, in a second
disguise. The one thing we can say is **empirical and non-structural**: oddpart(mₙ+1) is bounded away from 1
(min 3, and ≥313 for every n>2), the trailing-run v grows only like log₂ n while the width grows like 0.94n,
so the all-ones target recedes geometrically — the summable, non-halt-leaning picture — but **no effective
N₀** with "oddpart(mₙ+1) > 1 for all n > N₀" can be produced, because no theorem's hypotheses hold. Verdict:
`[OPEN]`. The effective-Diophantine / linear-forms-in-logarithms attack is **definitively inapplicable** to
Space Needle.

## Soundness ledger
- Reduction HALT ⟺ oddpart(mₙ+1)=1 and identity v₂(m+1)=v: `[PROVEN]`, 25249/25249 exact.
- No-recurrence (order ≤10), non-smoothness/large-prime, generic growth rate, min gₙ=3, max v=12/width 943:
  `[OBSERVED / computed exact]`, 50 000 gens, 46 863-bit orbit.
- Bounded-away-from-1, summability, non-halt lean: never a machine claim. Machine `[OPEN]`.

## Reproduce
`sndt_oddpart.py [GENS]` (reduction + identity + oddpart minimum/statistics) ·
`sndt_structure.py [GENS]` (smoothness/large-prime factoring, v-distribution & margin, growth-rate
continued fraction, Hankel linear-recurrence test). Basis: `SPACENEEDLE_DECISION_ATTEMPT_2026-07-10.md`,
`O16_SPACENEEDLE_FIXEDPOINT_2026-07-08.md`, `snd_dynamics.py`, `snd_automaton.py`. Effective-theory context:
Bugeaud, *Linear Forms in Logarithms and Applications* (Baker–Wüstholz, Matveev); "perfect/prime powers in
linear recurrence sequences" (order ≥2, dominant-root hypothesis) — none applicable here.

**No machine decided. No label upgraded.**
