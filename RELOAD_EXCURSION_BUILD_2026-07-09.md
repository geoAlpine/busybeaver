# Reload-excursion build — the exact ℤ_q^× reload-unit dynamics, its coupling probe, and the constructive tail-adversary (2026-07-09)

*Genuine BUILD on the single un-blocked mechanism from `NEWMATH_BUILD_SYNTHESIS`: an a-priori excursion/return
estimate on the EXACT reload map (not the abstract excursion of `EXCURSION_SYNTHESIS`). Task: derive the exact
ℤ_q^× reload-unit recursion `u_{i+1}=F(u_i,K_i)`, probe it for the carry-coupling between consecutive depths that
the abstract model left free, and attempt the second-moment estimate the abstract excursion could not reach.
STRICT SOUNDNESS: `[PROVEN]`/`[CONSTRUCTED-partial]`/`[OBSERVED]`/`[OPEN]`. Does NOT re-run the logged
EXCURSION/telescoping NO-GOs — it uses the new reload handle. Numerics exact big-int,
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/reload_excursion_build.py`, orbits to n=2·10⁵ steps
(10⁵ Antihydra reloads, 1.3·10⁵ o4 reloads). NOT committed.*

---

## 0. What was built, in one paragraph

The exact reload map is not just the depth recursion `K_{i+1}=v_q(p^{K_i}u_i+s_i)` of `NEWMATH_SOLENOID_BUILD`; it
is a genuine **skew-product on the q-adic units** `u_{i+1}=(p^{K_i}u_i+s_i)/q^{K_{i+1}}` `[PROVEN, 0 mismatch /
10⁵]`. Building it out and probing it yields a precise, honest verdict: **the reload map's arithmetic PINS the
one-step transition kernel exactly (conditional law geometric, unit refreshed) but supplies NO coupling that
reaches the tail** — measured consecutive-depth correlation is at the sampling-noise floor (`corr≈+0.008`,
`I(K_i;K_{i+1})=0.0003` bits) and, decisively, the conditional mean `E[K_{i+1}|K_i≥6]=2.018≈E[K]` is flat, so a
large depth does **not** constrain the next. And the reload map **constructively realizes the heavy-tail
adversary**: I solve the q-adic constraints to exhibit an explicit unit `u₀` whose reload orbit has any prescribed
depth sequence, including a genuine `E[K²]=∞` heavy tail (max K=42 in 40 steps), each step satisfying the exact map.
So the reload handle converts "the adversary is abstractly drift-indistinguishable" into "**the adversary is an
explicit q-adic unit the map itself does not exclude**" — a sharper statement of the same (K)-wall, and the second
moment remains the conclusion, not an input.

---

## 1. The exact ℤ_q^× reload-unit dynamics `[PROVEN, verified 0/10⁵]`

**Setup.** Each branch of a {2,3}-smooth cryptid is affine `b(v)=(pv+e)/q` with integer fixed point `x=−e/(p−q)`;
the maximal same-branch run from entry `v` has length `K=v_q(v−x)`, and drains to the exit `b^K(v)=x+(p/q)^K(v−x)`.
Write the q-adic **unit** `u=(v−x)/q^K ∈ ℤ_q^×` (the orbit's higher-place residual). Because `(p/q)^K(v−x)=p^K u`
(the `q^K` cancels), the exit is exactly `x+p^K u`, and the next entry's depth/unit are read off it. This gives the
**exact reload-unit recursion**:

> **`K_{i+1}=v_q(p^{K_i}u_i+s_i)`,  `u_{i+1}=(p^{K_i}u_i+s_i)/q^{K_{i+1}} ∈ ℤ_q^×`,  `s_i=x_i−x_{i+1}`.**

This is precisely the affine-then-normalize skew map `u↦(p^K u+s)/q^{K'}` the design spec named. The offset `s_i` is
the **carry**: bounded and branch-determined.

- **Antihydra `(p,q)=(3,2)`:** parities alternate, `x_even=0`, `x_odd=1`, so `s_i∈{−1,+1}` alternating —
  `u_{i+1}=(3^{K_i}u_i∓1)/2^{K_{i+1}}` on ℤ₂^×.  `[VERIFIED 0 mismatch / 100 067 transitions]`
- **o4 `(p,q)=(4,3)`:** three branches, `x_1=−14,x_2=−1,x_0=−9`; the next residue is `ρ'=(ρ+u mod3) mod 3` (since
  `4≡1`), and `s_i=x_ρ−x_{ρ'}∈{0,±5,±8,±13}` — `u_{i+1}=(4^{K_i}u_i+s_i)/3^{K_{i+1}}` on ℤ₃^×.
  `[VERIFIED 0 mismatch / 133 145 transitions]`

**This is the concrete object `NEW_MATH_PROGRAM` abstracted.** Its marginals are exactly the annealed geometric:
`P(K=k)=(q−1)/q^k` to 3 decimals (`E[K]=1.999≈2`, Antihydra; `1.502≈3/2`, o4), and the empirical second moments are
finite (`E[K²]=5.97≈6`; `3.01`) — but that finiteness is the conclusion; the build asks whether the map's
arithmetic *forces* it.

---

## 2. The coupling probe — the carry does NOT reach the tail `[OBSERVED, sharp]`

The design-spec hypothesis: *a large `K_i` forces `u_i≈±p^{−K_i} mod q^{K_i}`, which constrains `u_{i+1}`, which
bounds `K_{i+1}` — a carry-coupling the abstract model ignored.* I built and measured this coupling directly.

| probe (Antihydra, 10⁵ reloads) | value | independence baseline |
|---|---|---|
| `corr(K_i,K_{i+1})` | `+0.0084` | `0` (noise floor `1/√N≈0.003`) |
| `I(K_i;K_{i+1})` | `0.00033` bits | `0` |
| `E[K_{i+1} \| K_i=1,…,7]` | `1.99,2.00,2.00,2.05,2.03,2.02,2.01` | flat at `E[K]=2` |
| **`E[K_{i+1} \| K_i≥6]`** | **`2.018`** | **`2.0` — no tail coupling** |
| `corr(K_i,K_{i+r})`, `r=1..8` | all `\|·\|≤0.008` | white |
| renewal: `max\|P(u_{i+1} mod 8 \| K_i,K_{i+1})−¼\|` | `0.021` | `0` (unit refreshed) |

o4 is the same story (`corr=−0.004`, `E[K_{i+1}|K_i≥4]=1.47≈1.5`). **The probe answers the spec's question
negatively and precisely:** the coupling is present only at the noise floor and is **flat in the tail** — a deep
excursion tells you *nothing* about the next depth. The mechanism is visible in the map: the normalization
`÷q^{K_{i+1}}` **shifts out exactly the `K_{i+1}` bits of `u_i` that the large jump constrained**, so the residual
unit `u_{i+1}` inherits only the *unconstrained* higher bits of `u_i`. The map **refreshes** the unit (renewal
test 0.02), which is exactly why consecutive depths decouple — and exactly why no bounded-memory renewal bound on
`Σ K²` can be manufactured from it.

**The genuine a-priori residue the reload map DOES give `[CONSTRUCTED-partial]`.** From the identity
`u_{i+1}−p^{K_i}u_i/q^{K_{i+1}}=s_i/q^{K_{i+1}}`, the carry is **q-adically negligible on deep excursions**
(`|s_i/q^{K_{i+1}}|_q=q^{−K_{i+1}}→0`). So on the deep-excursion sub-dynamics the reload map **linearizes to the
bare host automorphism `×(p/q)`** with the nonlinear correction confined to shallow depth. This is a clean new
structural statement — the nonlinearity lives at bounded depth — and it dovetails with `O4_RUN_STRUCTURE` ("depth
unconditionally capped; frequency open"): the reload map controls the *shape* of each excursion but not the
*frequency* of deep ones, which is the entire open content.

---

## 3. The estimate attempt — and the constructive adversary that obstructs it `[OBSERVED]`

**The estimate the abstract excursion could not reach** is an a-priori `Σ_{i≤M}K_i² = O(M)` (⟺ `E[K²]<∞` ⟺
even-density `>0` ⟺ non-halting). A supermartingale/renewal bound needs a potential `W(K,u)` with reload-drift
`≳K²`. The reload map exposes exactly one additive invariant: `Σ_i K_i =` the total q-adic drainage `= v_q`-flux
`= log_q` of the accumulated q-part — a **first-moment** quantity. Every potential built from `u` is q-adically
constant (`|u|_q≡1`, units) and archimedean-linear in the excursion count; none has `K²` drift. Rather than
re-run the logged telescoping NO-GO, the reload map **confirms it at the mechanism level**: because the map
refreshes the unit (§2), the only conserved read-out is `ΣK`, and `ΣK²` is not a function of the transported state
— it is the very tail statistic being sought.

**The decisive adversary test `[CONSTRUCTED-partial]`.** Does the reload map's arithmetic *exclude* the heavy-tail
adversary? I answer by **construction**: solving the q-adic congruences `p^{K_i}u_i≡−s_i (mod 2^{K_{i+1}})`,
`≢ (mod 2^{K_{i+1}+1})` bit-window by bit-window (the windows are disjoint, so a consistent 2-adic `u₀` exists), I
exhibit an explicit unit whose Antihydra reload orbit has **any prescribed depth sequence**:

- target `K=[1,2,3,…,19]` (linear-growing depths, `ΣK²∼M³`): **realized exactly**, 0 error.
- a genuine i.i.d. heavy-tail sample with `P(K≥k)∼1/k` (`E[K]<∞`, **`E[K²]=∞`**): **realized exactly**,
  max realized depth `42` in 40 steps.

Every step satisfies the exact reload map `K_{i+1}=v_2(3^{K_i}u_i+s_i)` on the nose. **Conclusion: the reload map
does NOT a-priori exclude the heavy-tail adversary — it explicitly contains it.** This upgrades
`EXCURSION_SYNTHESIS`'s "abstract drift-indistinguishable adversary" and `NEWMATH_SOLENOID_BUILD`'s "a specific
ℤ_q^× misalignment" to a **fully explicit, map-faithful `u₀`** realizing `E[K²]=∞`. The misalignment is not merely
consistent with the map; it is a solvable q-adic congruence system with a guaranteed solution (a concrete instance
of the No-Structure realizability, now through the exact reload handle).

---

## 4. Honest verdict

**(b) — no crossing; one exact object built, the coupling probed to its floor, the adversary made explicit.**

- **Built `[PROVEN]`:** the exact ℤ_q^× reload-unit skew map `u_{i+1}=(p^{K_i}u_i+s_i)/q^{K_{i+1}}` for both
  Antihydra (q=2) and o4 (q=3), verified 0 mismatch over 2.3·10⁵ transitions on the real orbits.
- **Probed `[OBSERVED, sharp]`:** the carry-coupling the abstract model lacked is **absent at the tail** — the
  transition kernel is exactly the conditional geometric law and the unit is refreshed, so consecutive depths
  decouple (`corr≈0`, `E[K_{i+1}|K_i` large`]≈E[K]`). The reload map pins the *conditional* law and, as a genuine
  new partial, shows the **carry is q-adically negligible on deep excursions (the nonlinearity is depth-bounded;
  deep dynamics = bare host `×(p/q)`)** — but it leaves the *marginal tail* free.
- **Obstruction, made explicit `[CONSTRUCTED-partial]`:** the heavy-tail `E[K²]=∞` adversary is not just consistent
  with the reload map — it is an explicitly **constructible** unit `u₀` (solvable disjoint-window congruences),
  realized exactly with max depth 42. So the map's arithmetic cannot force `E[K²]<∞`.

**Precise residual (unchanged in species, sharpest form):** the reload map determines the excursion *shape* (the
one-step kernel, exactly geometric given the unit) and confines the nonlinear carry to bounded depth, but the
*frequency of deep excursions* = equidistribution of the units `u_i` on ℤ_q^× = an a-priori upper bound on
`E[K²]`/the marginal odd-energy = single-orbit normality on base `p/q` = (K) = Mahler 3/2 / AEV Conj 1.6 — remains
free, and is now shown to be exactly the freedom of the constructible q-adic misalignment `u₀`.

Reproduce: `scratchpad/reload_excursion_build.py` (exact map verification 0/2.3·10⁵; coupling table; correlation
decay; explicit heavy-tail adversary). Basis: `NEWMATH_SOLENOID_BUILD_2026-07-09`, `EXCURSION_SYNTHESIS`,
`O4_RUN_STRUCTURE_2026-07-07`, `NEW_MATH_PROGRAM`, kernel anchor AEV arXiv:2510.11723.

No machine decided. No label upgraded.
