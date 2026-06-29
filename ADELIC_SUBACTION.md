# Adelic (3-place) magnitude-aware sub-action: does mixing R, Q_2, Q_3 escape the 1-place sign tension? (2026-06-29)

*Angle (WEAPONS_AUDIT style): the magnitude-aware Lyapunov is inherently ADELIC. The induced odd map
`T(o)=3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`, seed `o0=27`, lives on the (2,3)-solenoid; the magnitude `log o` is
the archimedean coordinate, `D=v2(3o-1)` the 2-adic, `v3(o')=D-1` the 3-adic. Build a genuine 3-place
sub-action `g = α∞ log|o|∞ + α2(2-adic pot) + α3(3-adic pot) + h(residues)` with exact per-step drifts in all
three places (dual-repulsion + adelic coupling) and ask: does combining places, under the product-formula
constraint `Σ_v log|·|_v = 0`, let a sign choice be SIMULTANEOUSLY feasible (sub-action bounded above over ALL
invariant measures, incl. high-D) AND useful (telescoping forces `limsup avg ψ ≤ 0`)? Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (`scratchpad/adelic_subaction.py`, exact big-int, N=1e5).
Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line verdict

**(b) CLEAN ADELIC NO-GO.** Combining all three places does **not** escape the 1-place sign tension; the
product formula closes it. On the decisive `D=1` self-loop the three local drifts of the genuinely adelic
"distance-to-1" coordinate are exactly `(log(3/2), log2, −log3)` for `(∞,2,3)` and **sum to 0** with no other
prime moving — the product formula is *saturated by the three special places on every shallow step*. Hence the
**diagonal** weight `α∞=α2=α3` is annihilated (drift 0 < ψ=+1/2), forcing an **anti-diagonal** weight; but the
anti-diagonal that cancels the current-step depth `D` merely relocates the unbounded term to the **previous**
depth via the proven coupling `v3(o)=D_prev−1` (the T2 time-shift). The two place-constraints
"bounded-above over high-D" (gives `α∞ log(3/2) − α3 log3 ≥ 0`) and "bounded-above over high-e" (gives `α3 ≥ 0`)
together force `α∞ ≥ 0`, while useful telescoping needs `α∞ < 0`. **The third place adds a constraint that
reinforces the sign tension rather than relaxing it.** `[PROVEN]` Numerics: every useful sign (`α∞<0`) is
infeasible (`max ψ̃ > 0`) for `α3∈{0, cancel-D, α∞}`, and the cancel-D choice makes it strictly worse. No machine
decided. No label upgraded.

---

## 1. The adelic sub-action setup and exact per-step drifts `[PROVEN]`

Orbit point `o_j∈Z[1/6]`, `o_j=3^{e_j}u_j`, `gcd(u_j,6)=1`, `e_j=v3(o_j)=D_{j−1}−1`. Sub-action candidate
> `g(o) = α∞·log|o|∞ + α2·log|o|_2 + α3·log|o|_3 + h(o mod 2^k)`,  `log|o|_p = −v_p(o)·log p`.

Two natural adelic coordinates; both give the same no-go.

### 1a. Coordinate `o` itself (the magnitude / size-drift, ties directly to the kernel ΣD) `[PROVEN]`
Exact per-step place drifts (verified 0 failures / 1e5, `§4`):
- **∞:** `Δlog|o|∞ = log(o'/o) = D·log(3/2) + log(1−1/(3o))`, the second term `∈(−ε,0]`, `→0`. Drift `≈ D·log(3/2)`.
- **2:** `v2(o)=0` for **all** terms (o is odd), so `log|o|_2 ≡ 0` — **the 2-adic place of `o` carries literally
  no potential.** The 2-adic depth `D=v2(3o−1)` is the *argument of ψ*, not a coordinate of `o`; it cannot also
  be a sub-action place. `α2` is inert here.
- **3:** `Δlog|o|_3 = −(v3(o')−v3(o))·log3 = −(D−1−e)·log3`, with `e=v3(o)=D_prev−1`. Coefficient of the current
  depth `D` is `−log3`. (`v3(o')=D−1` is the PROVEN adelic coupling, ADELIC_COUPLING §1a.)

So `Δg = [α∞ log(3/2) − α3 log3]·D + α3(1+e)·log3 + α∞·ε`, and since `1+e = D_prev`,
> `Δg = [α∞ log(3/2) − α3 log3]·D + α3·D_prev·log3 + α∞·ε`.

### 1b. Coordinate `o−1` (the dual-repeller height; the genuinely 3-place D=1 drift) `[PROVEN]`
On a `D=1` step (`o'−1 = (3/2)(o−1)` exactly, REPELLER_ESCAPE §1, extended here to the 3-adic place):
- **∞:** `|o'−1|∞ = (3/2)|o−1|∞` → `Δlog|o−1|∞ = +log(3/2)`.
- **2:** `v2(o'−1)=v2(o−1)−1` → `Δlog|o−1|_2 = +log2`.
- **3:** `v3(o'−1)=v3(o−1)+1` → `Δlog|o−1|_3 = −log3`.  **[new, verified 0 failures / 49948 D=1 steps]**
- **all p≥5:** `(o'−1)/(o−1)=3/2` exactly → `v_p` unchanged → drift `0`. **[verified: ratio≡3/2, 0 failures]**

> **`[PROVEN]` Product-formula saturation on D=1.** `log(3/2)+log2−log3 = 0`, and no prime `p≥5` moves, so the
> three special places `{∞,2,3}` **exactly saturate** `Σ_v Δlog|o−1|_v = 0` on every shallow step. The
> archimedean expansion (×3/2), the 2-adic escape (×2), and the 3-adic descent (×1/3) are the three faces of a
> single product-formula identity, not three independent drifts.

---

## 2. The crux: does combining places escape, or does the product formula force it closed? `[PROVEN: closed]`

The coboundary/sub-action logic: if `ψ(o) ≤ Δg(o) := g(To)−g(o)` pointwise, then
`Σ_{j<N} ψ ≤ g(o_N)−g(o_0)`, so `limsup (1/N)Σψ ≤ limsup g(o_N)/N`. Define `ψ̃ = ψ − Δg`.
- **USEFUL** requires `α∞ < 0`: then `g(o_N)/N ≈ α∞·meanD·log(3/2) ≤ 0` (exploits `o_N→∞`), giving the bound.
  (The 2- and 3-adic parts of `g(o_N)` are **bounded** — `v2(o_N)=0`, `v3(o_N)=D_{N−1}−1` is a single bounded
  depth — so only the archimedean place can drive the telescoping. Adding places cannot supply usefulness.)
- **FEASIBLE** requires `ψ̃ ≤ 0` (≡ `sup over all T-invariant μ of ∫ψ̃ ≤ 0`), in particular bounded above as
  `D→∞` AND as `e→∞`.

Read the `D`- and `e`-coefficients of `ψ̃ = ψ − Δg` (ψ bounded in `{1/2,−1/2,−3/2}`), from §1a:
- coeff of `D`:  `−[α∞ log(3/2) − α3 log3]`. Bounded above as `D→∞` ⟺ **`α∞ log(3/2) − α3 log3 ≥ 0`**  …(i)
- coeff of `e`(=D_prev): `−α3 log3`. Bounded above as `e→∞` ⟺ **`α3 ≥ 0`**  …(ii)

> **`[PROVEN]` The product formula forces the sign tension closed.** From (ii) `α3 ≥ 0`; plug into (i):
> `α∞ log(3/2) ≥ α3 log3 ≥ 0`, hence **`α∞ ≥ 0`**. But usefulness needs `α∞ < 0`. **No `(α∞,α2,α3)` is
> simultaneously feasible and useful.** The 2-adic place is inert (`α2` free, contributes nothing); the 3-adic
> place is NOT a free third direction — by the coupling `e=D_prev−1` it is an invertible **time-shift** of the
> 2-adic depth (INTRATERM T2), so "high-e" measures **are** "high-D" measures. The third place therefore adds
> constraint (ii), which *reinforces* the tension instead of relaxing it.

**Why cancellation fails concretely.** The one anti-diagonal that kills the current-`D` blow-up is
`α3 = α∞ log(3/2)/log3` (sets (i) to equality 0). Then `Δg = α∞ log(3/2)·D_prev + α∞ε`: with `α∞<0` the
right side `→ −∞` as the **previous** depth `D_prev` grows, while `ψ ≥ −3/2`. Since `D_prev ⊥ ψ(o)` (current
depth `D` is ~independent of `D_prev`, corr≈0), there are steps with `D_prev` large and `ψ=+1/2` (`D=1`):
infeasible. **The cancellation does not remove the unbounded term; it moves it one step back through the
product-formula coupling** — an adelic instance of the T2 tautology. (Numerics §4 confirm: cancel-D makes
`max ψ̃` strictly *larger*, and the worst residuals sit exactly at large `e_j`.)

**The o−1 coordinate gives the same closure.** There the D=1 drift `(log3/2, log2, −log3)` sums to 0 (§1b), so
the diagonal weight is annihilated (`Δg=0<ψ=1/2`, infeasible); any anti-diagonal that makes `Δg≥1/2` on D=1
needs `α∞<0`-incompatible weights on the unbounded archimedean part, OR loads the 2-/3-adic parts whose orbit
telescoping is bounded (post-deep `v2(o−1)=1`; `v3(o−1)` net-bounded) — never producing useful growth. This
is the §3 REPELLER_ESCAPE degeneracy theorem (`H=log oddpart(o−1)` collapses ∞+2 to ΣD), now seen to *persist*
when the 3-adic place is added, because that place is the third saturating face of the same identity.

**The fixed point still blocks any GLOBAL statement (independent of places).** At `o=1`: `log o=0`, `v2(o)=0`,
`v3(o)=0`, and `D=1` so `v3(o')=0` — **all three place-potentials are stationary at the fixed point**, while
`ψ(1)=+1/2`. So no adelic `g` (any signs) sees the `δ_1` self-loop: `max ψ̃ ≥ +1/2` for every weight (numerics
§4 show `max ψ̃ → +1/2` even for the feasible sign `α∞>0`). The adelic enrichment changes nothing at `o=1`
because 1 is a unit at every finite place and a fixed magnitude at ∞ — the obstruction is place-blind.

---

## 3. Honest verdict

| ask | answer | label |
|---|---|---|
| Does a genuine 3-place adelic sub-action escape the 1-place sign tension? | **No.** | `[PROVEN]` |
| (a) adelic escape / partial? | **No partial.** The 2-adic place of `o` is inert (`v2(o)≡0`); the 3-adic place is a time-shift of the 2-adic depth (`e=D_prev−1`), not an independent direction. No conditional adelic certificate emerges: even the cancel-D anti-diagonal is infeasible (relocated blow-up). | `[PROVEN]` |
| (b) clean adelic no-go? | **Yes.** Feasibility forces `α3≥0` (high-e) and `α∞ log(3/2)≥α3 log3` (high-D) ⟹ `α∞≥0`; usefulness forces `α∞<0`. The product formula (D=1 drift `(log3/2,log2,−log3)` sums to 0; coupling `v3(o)=D_prev−1`) closes the gap. | `[PROVEN]` |
| (c) reduces? | The residual is identical to the 1-place magnitude residual and to the kernel: single-orbit equidistribution / `E_deep≤2` / Mahler-3/2 (REPELLER §2, INTRATERM §4). The adelic apparatus is an **isomorphism of the obstruction, not a reduction.** | `[PROVEN reduction]` |

**The exact gap.** A useful sub-action must (i) penalize archimedean size (`α∞<0`, to convert `o_N→∞` into a
telescoping `−∞`) and (ii) stay bounded above on high-depth measures. The product formula ties the three places
so that the only place with unbounded useful telescoping is ∞, while the boundedness constraint it imposes on ∞
(via the coupled 3-adic `e=D_prev−1` and the saturated D=1 identity) is exactly `α∞≥0`. The two requirements
are product-formula-antipodal. Closing this would require an *independent* third drift the solenoid does not
provide — equivalently the missing rank-2 second direction (NEWMATH_ADELIC_RIGIDITY AIU), which is `(K)`-hard.

---

## 4. Numerics `[OBSERVED, exact big-int, N=1e5, seed o0=27]` (`scratchpad/adelic_subaction.py`)

- **Exact per-step laws, 0 failures:** `v2(o)≡0`; `v3(o_{j+1})=D_j−1`; on 49948 D=1 steps
  `v2(o'−1)=v2(o−1)−1`, **`v3(o'−1)=v3(o−1)+1`** (new), `oddpart(o'−1)=3·oddpart(o−1)`, and
  **`(o'−1)/(o−1)≡3/2`** (all `p≥5` inert). The 3-place D=1 drift `(log3/2,log2,−log3)` sums to 0 exactly.
- `meanD=2.00069`, `freq(D=1)=0.49948`, `mean ψ=−0.25063` (Haar `−1/4`).
- **Sub-action scan `ψ̃=ψ−Δg` (coordinate `o`):** for EVERY useful sign `α∞∈{−1,−0.5,−0.2}` and every
  `α3∈{0, cancel-D=α∞log(3/2)/log3, α∞}`, `max ψ̃ > 0` (infeasible): e.g. `α∞=−0.5`: `max ψ̃ = +1.74 (α3=0),
  +3.54 (cancel-D), +8.39 (α3=α∞)`. **Cancel-D is strictly worse**, confirming the blow-up relocates rather
  than cancels. For feasible signs `α∞≥0`, `max ψ̃ → +0.5` (the place-blind `δ_1` self-loop), never ≤0.
- **Blow-up relocation (α∞=−0.5, cancel-D):** the top `ψ̃` residuals are all `D_j=1` steps with **large
  `e_j` (=D_{j−1}−1): e_j=14,13,13,13,12,…** — the unbounded term sits at the *previous* depth, exactly the
  T2 time-shift. `[OBSERVED, matches §2 PROVEN]`

---

## 5. Sources

- Repo: `MINPROP_COBOUNDARY_LP.md` (§5 magnitude-aware Lyapunov `α log o + h`, the `α<0` useful / `α>0`
  feasible sign tension; bounded LP infeasible, obstruction `δ_1`), `REPELLER_ESCAPE.md` (§1 dual-repulsion
  ×3/2/×2/×3, §3 adelic-height degeneracy ∞+2→ΣD, §4 no positive-weight escape sub-action),
  `ADELIC_COUPLING.md` (§1 product formula = first-moment only; §1a `v3(o')=D−1`),
  `INTRATERM_ADELIC_MINING.md` (T1 codim-1 product formula, T2 `e=D_prev−1` invertible time-shift),
  `NEWMATH_ADELIC_RIGIDITY.md` ((2,3)-solenoid, AIU = the missing rank-2 second direction).
- Literature (repo knowledge): product formula / strong approximation give one scalar per step (first moment);
  Furstenberg–Rudolph–Johnson ×2,×3 measure rigidity (need positive-entropy *jointly* invariant measure our
  single orbit does not supply); Mahler-3/2 / Flatto–Lagarias–Pollington (gap ≥1/3, not density). No
  adelic/S-arithmetic self-consistency yields a useful+feasible single-orbit sub-action for the hyperbolic
  solenoid orbit.

No machine decided. No label upgraded.
