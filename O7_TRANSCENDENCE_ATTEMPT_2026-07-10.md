# o7 decision attempt via transcendence theory / linear forms in logarithms (Baker) on the "orbit = power of 2" hitting problem (2026-07-10)

*Second DECISION attempt on o7 (the sole non-Type-I BB(6) census machine). The congruence/automaton attack
already FAILED (`O7_DECISION_ATTEMPT_2026-07-10.md`: reachable set fills ℤ/m, Collatz coupling). This is a
**different** question — not density/residues but effective Diophantine approximation of powers of 2 by the
orbit. Tool class new to o7: Baker linear forms in logs / S-unit equations / "powers in linear recurrences"
(Bugeaud–Mignotte–Siksek, Shorey–Stewart, Pethő). Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`,
exact big-int. Scripts `o7t_form.py`, `o7t_decomp.py`, `o7t_vdist.py`. SOUNDNESS PARAMOUNT: labels
`[PROVEN]`/`[OBSERVED]`/`[OPEN]`. Nothing committed.*

## 0. Verdict

**FAILURE MODE 4 (the honest one): the orbit has NO S-unit / linear-recurrence target for Baker.** The additive
corrections in o7's cascade map are not bounded constants — they are a **Collatz-coupled MULTIPLICATIVE
perturbation of median 25% per step** (`[OBSERVED]`, max 10/7). They inject ≈27% of the orbit's total
bit-growth `[OBSERVED]`, so `u_n` is **not an S-unit, not a bounded combination of S-units, and not a linear
recurrence** (its 2-adic exponents `v_n` are free/geometric, unbounded). Every effective theorem in this class
(BMS, Shorey–Stewart, Pethő, S-unit finiteness) requires exactly the structure `u_n` lacks — a fixed
characteristic recurrence / dominant root / boundedly-many S-unit terms. **Baker has no equation to be applied
to.** This confirms the o7 wall is **Diophantine-hard, not merely congruence-hard**: the same Collatz
valuation-coupling that filled ℤ/m also destroys the multiplicative structure Baker needs. o7 stays `[OPEN]`.

## 1. The exact S-integer form of `u_n` `[PROVEN given the automaton; 0-mismatch re-derived]`

Work on cascade-entry values `u_n` (even; `HALT ⟺ oddpart(u_n)=1 ⟺ u_n=2^k`). Re-deriving the b-free cascade
map `F` (0-mismatch vs raw TM, 49,940 transitions — banked) into closed multiplicative form and **re-verifying
0-mismatch vs `F` over 5,000 entries** (`o7t_form.py`, `step_clean`):

> **`u_{n+1} + 1 = (3/2)^{v_n} · x_n`,  where  `x_n = u_n + c_n`,  `c_n = (w_n+3)/2 + d_n`,**
> with `w_n = oddpart(u_n)`, `d_n = v2(u_n)`, `v_n = v2(x_n)`.  Equivalently `u_{n+1} = 3^{v_n}·oddpart(x_n) − 1`.

Two operations destroy any pure S-unit structure at **every** step: `oddpart(·)` (not congruence-continuous, not
algebraic) and the `−1`. Unrolling with `S_n := x_n = u_n + c_n`:

> `S_{n+1} = (3/2)^{v_n} S_n + (c_{n+1}−1)`   ⟹  `u_N = (∏_{n<N}(3/2)^{v_n})·S_0 + Σ_{j=1}^{N}(∏_{n=j}^{N-1}(3/2)^{v_n})(c_j−1) − 1.`

Each product `∏(3/2)^{v_n} = 3^{ΣV}/2^{ΣV}` **is** an S-unit (S={2,3}). So `u_N` is a linear combination of
S-units — but with **`N` terms (unbounded)** and coefficients `(c_j−1)` that are **not fixed**: `c_j =
(oddpart(u_j)+3)/2 + v2(u_j) ≈ u_j/2^{d_j+1}` is itself of order `(3/2)^j`.

## 2. The S-unit-vs-additive decomposition — the corrections are the obstruction `[OBSERVED]`

If `u_n` were a **pure** S-unit `3^A/2^B·c`, "`u_n=2^k`" would be `|A log3 − (k+B)log2| = 0`, impossible for
`A>0` by unique factorization — an **instant** non-halt. The real question is the size/structure of the additive
corrections. Measured exactly (`o7t_decomp.py`, `o7t_vdist.py`, N=20,000 entries, `u_N` ≈ 16,255 bits):

| quantity | value | meaning |
|---|---|---|
| correction multiplier `x_n/u_n` | median **1.250**, max **1.4286 (=10/7)**, min 1.00006 | NOT a small additive constant — a ~25% **multiplicative** kick |
| entries with `x_n/u_n > 1.05` | **88.0%** | the kick is generic, not rare |
| bit-growth from `(3/2)^{v}` factors | 11,879 bits | the "S-unit" contribution |
| bit-growth from additive corrections | **4,372 bits (27%)** | the corrections drive >¼ of the growth |
| `u_N` vs pure-S-unit prediction | true 16,254 bits vs 11,883 | corrections inflate `u_N` by a factor **≈ 2^4371** |
| `v_n` (S-unit exponent/step) | geometric `2^{−(v+1)}`, mean **1.02**, **max 14** | variable & unbounded — no fixed recurrence |
| `d_n = v2(u_n)` | geometric, mean ~1, max 15 | the free Collatz valuation |

The multiplicative kick `x_n/u_n = 1 + c_n/u_n ≈ 1 + 2^{−(d_n+1)}` is a direct function of the 2-adic valuation
`d_n` — the very quantity that is free and Collatz-coupled. So the perturbation is neither small nor structured;
it slaves the multiplicative geometry of the orbit to an uncontrolled valuation sequence.

## 3. Does any effective theorem apply? — NO `[PROVEN-in-literature that the hypotheses fail]`

The effective machinery for "powers (of 2) in a sequence" — Bugeaud–Mignotte–Siksek (Fibonacci/Lucas perfect
powers), Shorey–Stewart & Bugeaud–Kaneko (`U_n=y^m`), Pethő, and the S-unit-equation finiteness theorems
(solution count bounded by the **number of terms**) — **without exception requires the sequence to be a genuine
linear recurrence with a dominant root**, equivalently a **bounded**-term power sum `U_n = Σ_{i=1}^{r} P_i(n)α_i^n`
with **fixed** roots `α_i`. Then and only then is `U_n = 2^k` a linear form in **fixed** logs `|n logα − k log2|`
with effective Baker/Matveev lower bound, or a fixed-term S-unit equation.

o7's `u_n` satisfies **none** of these hypotheses:
- **Not a linear recurrence:** the exponents `v_n` are variable and unbounded (`[OBSERVED]` geometric to 14),
  so there is no fixed characteristic polynomial, no dominant root, no bounded `r`.
- **Not a bounded S-unit combination:** §1 gives `N` terms with orbit-scaled (`~(3/2)^j`), non-constant
  coefficients `(c_j−1)`. The S-unit-equation count "bounded by number of terms" is **vacuous** (terms → ∞).
- **No fixed linear form in logs:** "`u_n=2^k`" is *not* `|A log3 − B log2|` for controlled integers `A,B` —
  the analogue of `A` (the total 3-exponent) is pinned, but the **additive** `Σ(c_j−1)·S-unit` term has no log
  representation and is of the **same magnitude** as the main term (§2), so it cannot be treated as a bounded
  perturbation of a two-log form.

This is the exact dual of `BAKER_LINFORMS.md`'s archimedean finding (Baker/Padé are individual-term/support
tools, never a density): here Baker's *Diophantine* form is also inapplicable, for the complementary reason —
there is no algebraic target, the orbit is a "generic" integer whose 2-adic valuation is the free Collatz
quantity sitting inside **both** the dynamics and the halt condition `oddpart=1`.

## 4. Soundness ledger

- `step_clean` (the closed multiplicative form) vs `F`: **0 mismatch / 5,000 entries** (`o7t_form.py`); `F`
  itself is 0-mismatch vs the raw TM (banked, 49,940 transitions). The S-integer form of §1 is re-derived, not
  assumed.
- All decomposition figures `[OBSERVED]`, exact big-int (`o7t_decomp.py`, `o7t_vdist.py`, N=20,000). No
  heuristic enters the verdict; the verdict is the **structural** non-applicability of §3, which is a
  literature fact about the theorems' hypotheses, not a numerical extrapolation.
- Nothing strengthens any non-halting claim; a `[PROVEN]` non-halt would have needed either the pure-S-unit
  contradiction (§2, which fails because corrections are Θ(orbit)) or an effective `N₀` (§3, no theorem
  applies). **Neither exists.** No candidate decision to red-team. Nothing committed.

**The o7 hitting wall is Diophantine-hard: `u_n` is not an S-unit, not a linear recurrence, and its 2-adic
valuation is the free Collatz-coupled quantity — Baker has no target. o7 stays [OPEN].**

**No machine decided. No label upgraded.**
