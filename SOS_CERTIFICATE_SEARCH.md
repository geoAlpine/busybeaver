# Nonlinear / magnitude-aware / SOS certificate search for the induced Antihydra map (2026-06-30)

*Computational search for a NONLINEAR / magnitude-aware Lyapunov certificate that the bounded
coboundary LP no-go (`MINPROP_COBOUNDARY_LP.md`) does NOT cover, with an HONEST adversarial
verdict on whether any found certificate is genuine or collapses to (K) / the known no-go.
Induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `D=v2(3o−1)≥1`, seed `o0=27`. Violation observable
`ψ(o)=½−1{D≥2}−1{D≥3}` (a fn of `o mod 8`); `(K) ⟺ limsup (1/N)Σψ(o_j) ≤ 0` on the orbit of 27.
SOUNDNESS: zero false proofs; every claim labelled. Reproducible scripts in scratchpad
(`sos_search.py`, `sos_lp_direct.py`), `.venv`, exact `Fraction` for the LP/cycle work,
float only for the archimedean `log` drift. NOT committed.*

---

## §0. Verdict

**The theory's prediction is CONFIRMED computationally with precision: every nonlinear /
magnitude-aware template collapses to the known no-go or to (K). NO certificate became
genuinely feasible-and-useful.** `[PROVEN/[OBSERVED]-as-labelled]`

- The bounded ergodic-optimization value is recomputed exactly: **`β = sup_ν ∫ψ dν = +1/2`**
  at every level `k=3..12`, driven by the `δ₁` atom (fixed point `o=1`, self-loop weight `+½`).
- The **magnitude-aware** linear Lyapunov `g=α·log₂o+h(res)` has a hard **sign tension**: the
  exact feasibility threshold is `α ≥ 1/(2c) = 0.854756` (`c=log₂(3/2)`), but every feasible
  `α>0` makes the telescope `Σψ ≤ α·log₂o_N → +∞` **vacuous**; the only useful sign `α<0` gives
  `β(α) → +∞` (**infeasible**). Confirmed by BOTH an exact max-mean-cycle and a direct scipy LP.
- The **nonlinear quadratic** `V=α·log₂o+β₂·(log₂o)²+h(res)` (and max-of-linear / piecewise) is
  **globally infeasible for the SAME reason as the bounded LP** — at the fixed point `o=1` the
  magnitude drift vanishes identically, leaving the bare `ψ(1)=+½>0` obstruction — and its only
  "useful" sign `β₂<0` fails the per-step constraint at large `D` (which occurs at arbitrarily
  large `o`). Same wall, sharper.
- **Thresholding** (excluding a neighborhood of `o=1` / forbidding the `D=1` symbol) drops
  `β≤0` **only** by forbidding a positive density of the `D=1` (`ψ=+½`) symbol — i.e. by
  assuming the frequency statement (K) itself. The difficulty is fully localized to (K).

No machine decided; no label upgraded. `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.

---

## §1. Magnitude-aware LP result

**Exact size-drift identity** (`[PROVEN]`, re-derived): `log₂(T(o)/o) = D·c + ε(o)`,
`c = log₂(3/2) = 0.5849625…`, `ε(o)=log₂(1−1/(3o)) < 0`, `ε(o)→0⁻`, and `Σ_j ε(o_j)` converges
(`o_j` grows geometrically) so `ε` contributes only `O(1)` to any telescope. Hence the
magnitude coboundary `ψ(o) ≤ α(log₂To−log₂o)+h(To)−h(o)` reduces **exactly** to a bounded-`h`
sub-action for the modified observable

> `ψ̃(o) := ψ(o) − α·c·D`,  feasible ⟺ `β(α) := sup_ν ∫ψ̃ dν ≤ 0`.

**Recomputed two independent ways, agreeing to 6 digits:**

| `α` | `β(α)` exact max-mean-cycle (Karp, k=7) | `β(α)` direct scipy LP (min uniform slack `t*`) | feasible? | useful? |
|---|---|---|---|---|
| −0.5 | +0.79248 | +0.792481 | NO | (would be useful) |
| −0.1 | +0.55850 | +0.558496 | NO | useful |
| 0.0 | +0.50000 | +0.500000 | NO | — |
| +0.5 | +0.20752 | +0.207519 | NO | vacuous |
| **+0.85476** | **−0.00003** | **−0.000003** | **YES (threshold)** | vacuous |
| +0.9 | −0.02647 | −0.026466 | YES | vacuous |
| +1.0 | −0.08496 | −0.084963 | YES | vacuous |

- The exact feasibility threshold is `α ≥ 1/(2c) = 0.854756` (analytic: `sup_ν ∫ψ̃ = ½ − αc`,
  attained at the `D=1` symbol). Matches the LP `t*` crossing zero at `0.85476`.
- For `α<0`: the analytic sup over constant-`D=d` invariant measures is
  `∫ψ̃ = ψ(d)+|α|·c·d → +∞` (e.g. `α=−½`: `+0.79` at `d=1`, `+1.43` at `d=10`, `+56.99` at
  `d=200`) — **infeasible**, and the residue-graph `β(α)` is the truncation of this `+∞`.
- **Does it certify (K) globally, or only conditionally?** Neither, for any single `α`: the
  feasible `α≥0.855` telescopes to `Σ_{j<N}ψ ≤ α·log₂o_N+O(1)`, and since `log₂o_N/N → c·meanD>0`
  the per-step bound on `limsup(1/N)Σψ` is a **positive** constant ⇒ **vacuous**. The conditional
  `o>M₀` version does NOT escape: `D=v2(3o−1)` is unbounded at arbitrarily large `o` (e.g.
  `o≈7.3·10¹¹` has `D=41`), so the useful sign `α<0` fails the **per-step** constraint on the
  tail with no invariant measure needed. (Re-confirms `MAGNITUDE_LYAPUNOV.md`.) `[PROVEN]`

---

## §2. Nonlinear / SOS templates tried + adversarial check

**C1 — quadratic `V(o)=a·log₂o+b·(log₂o)²+h(o mod 2^k)`.** Drift
`V(To)−V(o)=a(Dc+ε)+b((Dc+ε)²+2(log₂o)(Dc+ε))+Δh`; the `b·2(log₂o)(Dc)` piece is genuinely
**magnitude-aware** (it grows with `log₂o`, something residues cannot see). Two decisive findings:

- **Global infeasibility = the same `δ₁` no-go.** At the genuine fixed point `o=1`:
  `log₂1=0`, `T(1)=1`, so `Δh=0` and **all magnitude terms vanish identically for any `a,b`** ⇒
  drift `= 0`, and the constraint demands `ψ(1)=+½ ≤ 0` — FALSE. So **every template of the
  form `f(log₂o)+h(res)` is globally infeasible by the exact same obstruction as the bounded LP**:
  the magnitude coordinate is blind at the atom. `[PROVEN]`
- **Conditional (`o>M₀`) + useful sign `b<0` fails per-step at large `D`.** Telescope sign:
  `Σψ ≤ V(o_N) ~ b·(log₂o_N)² ~ b·(c·meanD·N)²`, so `/N → sign(b)·∞`: `b<0` useful, `b>0`
  vacuous. But for `b<0` the per-step RHS at a `ψ=−3/2` residue is `aDc − |b|(Dc)² + …`, which
  `→ −∞` as `D→∞`; the constraint `−3/2 ≤ RHS` fails for `D > D_crit` (root of
  `|b|c²D² − acD − 3/2 = 0`): e.g. `(a,b)=(1,−0.001) ⇒ D_crit≈1712`, `(1,−0.01) ⇒ ≈173`,
  `(0,−0.001) ⇒ ≈66`. Such `D` exist at `o≈2^{D_crit}` in class `3⁻¹ mod 2^D` ⇒ no threshold
  `M₀` excludes them. **Same wall as §1, sharper (quadratic in `D`).** `[PROVEN]`

**C2 — max-of-linear / piecewise `V=max_i(a_i log₂o+h_i(res))`.** A telescoping-useful piece
needs negative effective slope on the growth direction; each such linear piece inherits the §1
`α<0` per-step infeasibility (unbounded `D` at unbounded `o`). A max of finitely many linear
functions cannot dominate `ψ+|a|cD` as `D→∞`. No feasible-and-useful piecewise template. `[PROVEN]`

**C3 — ADVERSARIAL "is it secretly the finite check / circular?"** Direct LP test:
- bounded-`h` (`α=0`) over the orbit-of-27's **own realized** residue transitions (`N=2999`,
  `k=7`): `t*=+½` — **infeasible** even there (the realized path already contains positive
  residue cycles from recurring `D=1` returns). So there is **no residue-domain restriction
  cheat**.
- The same template over **all** odd residues mod `2⁷`: `t*=+½` — infeasible (the `+½`
  self-loop at `o=1`).
- The ONLY potential that "fits" is one indexed by **step** (`h(j)=`partial sum) — which is
  literally the finite check `balance_n≥0` up to `N`, bounding the truncated sum but yielding
  nothing asymptotic. Any unbounded-magnitude template made "feasible" on a finite integer
  sample is feasible **trivially** because a finite Birkhoff sum is bounded — that is the
  finite-check cheat, not a certificate. `[PROVEN]`

**Net for §2: no nonlinear/SOS template became genuinely feasible. Where one is "feasible" it is
either vacuous (telescope `→+∞`) or it secretly = the finite check (step-indexed / finite
sample) = verifying (K) up to `N`.**

---

## §3. Ergodic-optimization `β` recomputation + threshold experiment

**`β = sup_ν ∫ψ dν = +1/2` at every `k=3..12`** `[PROVEN]`. Computed as the max-mean-cycle of
the sound residue constraint graph (full reachability from `27 mod 2^k`: `4/4 … 2048/2048`).
Since `ψ` takes values in `{+½,−½,−3/2}` and `o=1` (`T(1)=1`, `ψ(1)=+½`) gives a **self-loop of
weight `+½`** at residue `1` for every `k≥3`, the max-mean-cycle equals the max single-edge
weight `+½` exactly. This re-confirms the bounded-LP no-go computationally (independent code).

**Threshold / deletion experiment (exact Karp, determined-edge graph):**

| `k` | `β` full | `β` delete node 1 (atom `δ₁`) | `β` forbid `D=1` symbol (drop all `ψ=+½` edges) |
|---|---|---|---|
| 3 | 1/2 | 0 | −1/2 |
| 4 | 1/2 | 1/6 | −1/2 |
| 5 | 1/2 | 1/4 | −1/2 |
| 6 | 1/2 | 3/10 | −1/2 |
| 7 | 1/2 | 1/3 | −1/2 |
| 8 | 1/2 | 5/14 | −1/2 |

- Deleting **only** the atom `o=1` does **not** push `β≤0` (`β=1/6…5/14>0`): reachable
  positive-mean residue pseudo-cycles remain (matches `MINPROP_COBOUNDARY_LP.md §3`). So
  excluding the single fixed point is insufficient.
- `β≤0` is reached (`β=−½`) **only** by forbidding the entire `D=1` (`ψ=+½`) symbol — i.e.
  forcing the orbit to avoid residue `≡1 mod 4` with full density.
- **Magnitude-threshold reading.** A magnitude threshold `o>M₀` cannot remove `D=1` steps: the
  `ψ=+½` contributions come from integers `o≡1 mod 4` of **every size** (including arbitrarily
  large `o`, which are `D=1` with `ψ=+½`). So thresholding in magnitude does **not** lower `β`;
  the supremum `+½` is approached by measures concentrating on `D=1` regardless of `|o|`. To get
  `β≤0` you must bound the **frequency** `freq(D=1)` away from `1` (equivalently
  `freq(D≥2)+freq(D≥3) ≥ ½`) — which **is** (K). The entire difficulty localizes to: "the orbit
  of 27 visits the `D=1` symbol with Cesàro frequency `< 1` by the right margin" = single-orbit
  equidistribution = (K)-content. `[PROVEN]`

---

## §4. Net

The computation is a precise, independent confirmation of the program's structural prediction.
The recomputed ergodic-optimization value is **`β = +1/2`** at all levels `k=3..12` (the `δ₁`
atom), so the bounded LP is infeasible. The **magnitude-aware** linear Lyapunov is feasible only
for `α ≥ 1/(2c) ≈ 0.8548` and that regime is **vacuous** (telescope `→+∞`); the useful sign
`α<0` is **infeasible** (`β(α)→+∞`), verified by both exact max-mean-cycle and direct scipy LP.
The **nonlinear quadratic** and **piecewise/max-of-linear** templates add a genuine
magnitude-aware term but are **globally infeasible by the identical `δ₁` mechanism** (the
magnitude drift vanishes at the fixed point) and, conditionally, fail the **per-step** constraint
at the unbounded `D=v2(3o−1)` available at arbitrarily large `o` — the same wall, made sharper
(quadratic in `D`). No template is simultaneously feasible and useful. Adversarially, the only
"feasible" object is a step-indexed potential = the finite check (= verifying (K) up to `N`),
and even the orbit's own realized residue transitions are infeasible for a bounded `h`, so there
is no residue-restriction escape. **Thresholding localizes the entire difficulty to (K)**: `β≤0`
is attainable only by forbidding a positive density of the `D=1` symbol, which is the frequency
statement (K) = Mahler 3/2 / AEV itself. **No genuine surprise; the collapse is confirmed with
precision. No machine decided; no label upgraded.**

### Reproducibility
- `scratchpad/sos_search.py` — §A (exact `β`, k=3..12; threshold/deletion table), §B (magnitude
  `β(α)` analytic + Karp), §C (quadratic/piecewise + adversarial reasoning). Exact `Fraction`.
- `scratchpad/sos_lp_direct.py` — direct scipy `linprog` solve of the magnitude-aware feasibility
  (`t*=β(α)`, matches Karp to 6 digits) and the C3 finite-sample/all-residue cheat check.

### Sources
- `MINPROP_COBOUNDARY_LP.md` (bounded-LP no-go, `β=+½`, `δ₁`).
- `MAGNITUDE_LYAPUNOV.md` (linear magnitude-aware sign-tension no-go — re-confirmed here).
- `BB6_NO_STRUCTURE_THEOREM.md` (§4 magnitude-aware/adelic closure; the three structural classes).
- `MINIMAL_CORE_2ADIC.md` (the minimal (K) object).
