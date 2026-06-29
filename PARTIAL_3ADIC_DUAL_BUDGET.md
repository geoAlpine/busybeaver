# The 3-adic / adelic dual budget — does the 3-adic side give a new floor on Sum D? (2026-06-30)

*Angle: the 2-adic budget `Σ_{odd}v₂(3c_i−1)=n+v₂(c_n)−v₂(c_0)` controls `ΣD` from ABOVE (running
accumulator `v₂(c_n)∈[0,0.585n]`). The PROVEN coupling `v₃(o_{j+1})=D_j−1` gives a candidate COMPLEMENTARY
3-adic budget `Σ_{j<R}(D_j−1)=Σ_j v₃(o_{j+1})`. Target: does a 3-adic conservation law / floor (`v₃≥0`)
bound `Σv₃` and hence pin `ΣD` more tightly — yielding positive even-density or `E[K²]<∞` (both strictly
weaker than (K), genuine partials)? Induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)`, seed `o₀=27`.
Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (`scratchpad/three_adic_budget.py`, exact
big-int, `N=10⁵` induced steps, ≈8s). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line verdict

**The 3-adic dual budget is NOT a new conservation law — it COLLAPSES to the first-moment tautology, and
the reason is sharp and structural.** Unlike the 2-adic place, the 3-adic place is **inert in `3o−1`**
(`3o−1≡−1 mod 3`, so `v₃(3o−1)=0` every step, verified 0 exceptions), hence `v₃(o_j)` is **NOT a running
accumulator**: it is RESET to 0 and re-injected fresh at every induced step. There is therefore **no
telescoping 3-adic budget and no new floor**. The identity `Σ_{j<R}(D_j−1)=Σ_j v₃(o_{j+1})` is — verified
exactly — algebraically `ΣD−R`, i.e. the SAME first moment relabelled; combining it with the 2-adic budget
gives the tautology `R+Σv₃=ΣD` (`200069=200069`, exact). The 3-adic floor `v₃≥0` says only `D≥1` (trivial,
permits even-density 0); the per-term ceiling `v₃(o_{j+1})≤log₃o_{j+1}` is the 3-adic FLP range (holds
`10⁵/10⁵`) and sums to `O(R²)`, useless. **No positive even-density. No `E[K²]<∞`. Reduces to (K)/Mahler.**

---

## 1. The 3-adic budget identity `[PROVEN, verified exact]`

From `v₃(o_{j+1})=D_j−1` (ADELIC_COUPLING §1a), summing over the induced orbit:

> **`[PROVEN]` `Σ_{j<R}(D_j−1) = Σ_{j<R} v₃(o_{j+1}) = ΣD − R`.**  Verified exact: `Σ(D_j−1)=100069 =
> Σv₃(o_{j+1})=100069` at `N=10⁵`.

This is the candidate "total 3-adic valuation accumulated by the orbit." **The catch:** it is literally
`ΣD − R` (sum of depths minus number of renewals) — a quantity the first moment already names. It is not an
independent budget.

### 1a. Why there is NO 3-adic conservation law (the decisive asymmetry) `[PROVEN]`

The 2-adic budget is genuine because `v₂(c_n)` is a **running coordinate** that telescopes
(`v₂(c_{i+1})−v₂(c_i)∈{−1,D_i−1}`) and is pinned between a **floor** (`v₂(c_n)≥0`) and an **archimedean
ceiling** (`v₂(c_n)≤log₂c_n≈0.585n`) — two genuinely external bounds on an accumulating quantity, giving
the two-sided range `n−v₂(c_0)≤ΣD≤1.585n`.

The 3-adic place has no such accumulator:

> **`[PROVEN]` `v₃(3o−1)=0` for every `o`** (since `3o−1≡−1≡2 mod 3`). Verified: nonzero count `0/10⁵`.

So at every induced step the 3-adic valuation of the *argument* `3o_j−1` is **zero** — the entire 3-adic
content `3^{D_j−1}` of `o_{j+1}` is **annihilated** when forming `3o_{j+1}−1`, and a fresh `v₃(o_{j+2})=D_{j+1}−1`
is injected with no memory of the previous one. `v₃(o_j)` is a **memoryless per-step injection, not a
conserved running quantity.** Telescoping it gives only the boundary term
`Σ_j(v₃(o_{j+1})−v₃(o_j))=D_{R−1}−D_0` (trivial). **There is no 3-adic analogue of `v₂(c_n)`, hence no new
floor and no complementary budget.** The 3-adic "floor" `v₃≥0` is merely `D_j−1≥0`, i.e. `D_j≥1` — the
trivial per-step minimum that permits `ΣD=R` (mean `D=1`, even-density `0`).

The only other 3-adic bound is the **per-term ceiling** `v₃(o_{j+1})≤log₃o_{j+1}` (3-adic FLP range; holds
`10⁵/10⁵`) `⟺ D_j≤1+log₃o_{j+1}` — a per-term spread bound identical in spirit to the 2-adic FLP range, and
summing it gives `Σv₃≲Σ_j log₃o_{j+1}=O(R²)≫ΣD`, vacuous for the sum.

---

## 2. Does 2-adic + 3-adic pin mean D, or `Σ D²`? `[PROVEN: NO — tautology]`

**Mean D / positive even-density.** Combine the two budgets:
- 2-adic (micro-time accounting / gap): `ΣD = n + v₂(c_n) − v₂(c_0)` (= renewal first moment).
- 3-adic: `Σ(D_j−1) = Σv₃(o_{j+1})`, i.e. `ΣD = R + Σv₃`.

These are **not two independent equations**: `Σv₃=Σ(D_j−1)=ΣD−R` by definition, so the second reads
`ΣD=R+(ΣD−R)`, i.e. `0=0`. **Verified:** `R+Σv₃=200069=ΣD`. The 3-adic budget adds **no constraint** to the
2-adic first moment. Positive even-density `freq(D≥2)>0` would need a *lower* bound on `Σv₃` better than the
trivial `Σv₃≥0`; the only 3-adic floor is `v₃≥0` (⟺`D≥1`), which permits `Σv₃=0` (all `D=1`, even-density
`0`). **No positive even-density.**

**Second moment / `E[K²]<∞`.** The 3-adic second-moment version is `Σv₃(o_{j+1})²=Σ(D_j−1)²` — verified
exact (`300217=300217`). But this is the **second moment itself**, relabelled; bounding it needs an
independent `O(N)` cap on `Σv₃²`, and the 3-adic place supplies none (no accumulator, §1a). This is
**exactly the EK2_SECOND_BUDGET obstruction**: degree-1 valuation telescopes give a *count* (free, `≤N`);
degree-2 give the *energy* equated to itself, with no proven cap (one deep refill `K≈0.585n` injects
`K²≈0.34n²`, permitted by every proven identity). The 3-adic dressing does not escape it — it reproduces it,
because `Σv₃²` IS `Σ(D−1)²`. **No `E[K²]<∞`.**

So the INTRATERM tautology verdict holds on the dual side too: the product formula / coupling is
codimension-1 (first moment, one scalar/step); the 3-adic budget, having no independent accumulator, lives
entirely inside that one scalar. **It escapes neither the first-moment tautology nor (K).**

---

## 3. Numerics `[OBSERVED, exact big-int, N=10⁵]`

| quantity | value | reading |
|---|---|---|
| `Σ(D_j−1)` vs `Σv₃(o_{j+1})` | `100069 = 100069` | **identity exact** |
| `v₃(3o−1)≠0` count | `0 / 10⁵` | 3-adic place inert ⇒ no accumulator |
| `R + Σv₃` vs `ΣD` | `200069 = 200069` | **combination = tautology** |
| `Σv₃²` vs `Σ(D−1)²` | `300217 = 300217` | 2nd moment = itself, no cap |
| mean `D` | `2.00069` | first moment Haar-consistent |
| even-density `freq(D≥2)` | `0.50052` | = `density{3∣o_{j+1}}` (coupling) |
| `P(v₃=k)`, `k=0..8` | `.4995,.2504,.1252,.0629,…` | geometric `2^{−(k+1)}` (NOT `Z₃`-Haar) |
| mean `v₃` | `1.00069` | `= mean D − 1` |
| max `v₃` | `15` | `≈log₂N`, per-term range only |
| `v₃(o_{j+1})≤log₃o_{j+1}` | `10⁵/10⁵` | per-term ceiling holds; sums to `O(R²)` |
| first-moment ratio `logo_N : ΣD·log(3/2)` | `1.0000002` | product formula = renewal, verified |

The `v₃` distribution is geometric base-2 (`P(v₃=k)=2^{−(k+1)}`), **dictated by the 2-adic predecessor**
(`v₃(o_{j+1})=D_j−1`, `D` geometric), NOT the `Z₃`-Haar `(2/3)3^{−k}` — confirming the 3-adic statistics
carry zero information beyond the 2-adic depth law.

---

## 4. Honest verdict (the four asks)

| ask | answer | label |
|---|---|---|
| (1) exact 3-adic budget identity? bound on RHS? | `Σ(D−1)=Σv₃(o_{j+1})=ΣD−R`, exact. RHS bounded only by trivial floor `v₃≥0`(⟺`D≥1`) and per-term ceiling `v₃≤log₃o`(FLP range, sums to `O(R²)`). **No conservation law:** `v₃(3o−1)=0` always ⇒ `v₃` is reset/re-injected each step, not an accumulator (contrast `v₂(c_n)∈[0,0.585n]`). | `[PROVEN]` |
| (2) does 2-adic+3-adic pin mean D / `ΣD²`? | **No.** `Σv₃=ΣD−R` by definition ⇒ combination is the tautology `R+Σv₃=ΣD` (verified). No lower floor ⇒ no positive even-density. 2nd-moment `Σv₃²=Σ(D−1)²` is the energy equated to itself ⇒ no `E[K²]<∞` (EK2 obstruction reproduced). | `[PROVEN]` |
| (3) genuine new partial or collapse? | **Collapse to the first-moment tautology / (K).** The 3-adic budget is `ΣD−R` relabelled; codim-1, mean-only; the 3-adic place is inert in `3o−1` so supplies no independent accumulator. | `[PROVEN]` |
| (4) numerics | identity exact (`100069`); `v₃(3o−1)=0` (`0/10⁵`); combination tautology exact; `v₃` geometric base-2 (forced by `D`-law); no pinning of mean `D` or `ΣD²` beyond first moment. | `[OBSERVED]` |

### The exact gap
A genuine 3-adic budget would require `v₃` to be a **conserved accumulator** with an external floor/ceiling,
as `v₂(c_n)` is. But `3o−1≡−1 mod 3` makes the 3-adic place **inert at every step** (`v₃(3o−1)=0`), so the
3-adic valuation is memoryless: injected `=D_j−1`, annihilated next step, never accumulating. The 2-adic
budget works precisely because `v₂(c_n)` *does* accumulate (and is floored at 0, capped by archimedean
size); the 3-adic side has no such running coordinate, so `Σv₃` is forced to equal `ΣD−R` with no
independent bound. **The complementary lower-pin the prompt sought does not exist on the 3-adic side; the
two valuations carry one and the same first moment.**

### New asset banked `[PROVEN]`
**3-adic inertness ⇒ no dual budget.** `v₃(3o−1)=0` for all `o` (since `3o−1≡−1 mod 3`), so `v₃(o_j)` is a
memoryless per-step injection (`v₃(o_{j+1})=D_j−1`), not a conserved accumulator. Consequently the candidate
3-adic budget `Σ(D−1)=Σv₃(o_{j+1})` is identically `ΣD−R`, the first moment; combined with the 2-adic budget
it yields only the tautology `R+Σv₃=ΣD`. This pinpoints **why** the 2-adic side has a genuine two-sided
range while the 3-adic side has none: the 2-adic place accumulates (floor 0, ceiling 0.585n); the 3-adic
place is reset every step. The asymmetry is the inertness `v₃(3o−1)=0`.

### Why this confirms rather than breaches (honest)
Fully consistent with: ADELIC_COUPLING (coupling is an isomorphism of obstructions, product formula =
first moment); INTRATERM_ADELIC_MINING (3-adic exponent additively annihilated in the kernel density,
codim-1 vs codim-∞); EK2_SECOND_BUDGET (degree-2 telescope equals the energy itself, no `O(N)` cap);
REPELLER_ESCAPE (the adelic height degenerates to the trivial `ΣD` identity; the two valuations are not
independent constraints). This note adds the *sharpest reason the 3-adic side specifically gives no
complementary budget*: 3-adic inertness in `3o−1` ⇒ no running accumulator ⇒ no floor ⇒ `Σv₃≡ΣD−R`.

## Sources
- `ADELIC_COUPLING.md` (§1a `v₃(o_{j+1})=D_j−1`; §1 product formula = first moment), `VALUATION_BUDGET.md`
  (2-adic budget `Σv₂(3c_i−1)=n+v₂(c_n)−v₂(c_0)`, accumulator `v₂(c_n)∈[0,0.585n]`, FLP range),
  `INTRATERM_ADELIC_MINING.md` (L1 `v₃(3o−1)=0`; product formula codim-1 tautology; 3-adic additively null),
  `EK2_SECOND_BUDGET.md` (first moment = count free, second moment = energy with no `O(N)` cap),
  `REPELLER_ESCAPE.md` (adelic-height degeneracy; valuations not independent at the height level).
- `scratchpad/three_adic_budget.py` — exact big-int verification of the identity, inertness, tautology,
  second moment, `v₃` distribution, and per-term ceiling, `N=10⁵`.
- Literature (repo knowledge): Furstenberg/Rudolph/Lindenstrauss ×2,×3 (measure rigidity, not single-orbit);
  Mahler 3/2 / Flatto–Lagarias–Pollington (range, not density); AEV 2025 (arXiv:2510.11723), Algom–Baker–
  Shmerkin 2025 (arXiv:2504.18192) — the open anchors.

No machine decided. No label upgraded.
