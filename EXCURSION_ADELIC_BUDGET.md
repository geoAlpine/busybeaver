# The adelic magnitude–depth budget for excursions of `V=v₂(c−1)`: does it bound the 2nd moment / deep-excursion frequency a priori? (2026-06-30)

*Sub-route of the a-priori excursion estimate (`CORE_ORBIT_ARITHMETIC.md` §5): the un-pre-empted shape is a
quenched return-time/Lyapunov argument on the 2-adic potential `V=v₂(c−1)` whose decrease must live in the
**conditional return-time law** — but that law **is** the D-statistics (circular). This note asks whether the
**ADELIC magnitude–depth coupling** (dual-repulsion §`REPELLER_ESCAPE` + product formula §`ADELIC_COUPLING`)
supplies the a-priori input — i.e. bounds the **deep-excursion frequency** `f_K` or the **second moment**
`E[K²]` (= `μ({1})=0`, `NONATOMIC_FIXEDPOINT.md`) **without** assuming the D-law. WEAPONS_AUDIT style. Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/excursion_adelic.py`, exact big-int, induced odd map
`o↦o'=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)`, `o₀=27`, `N=10⁵`. SOUNDNESS: every line labelled; no (K) claim; no
false proof. NOT committed.*

---

## 0. One-line verdict

**The adelic magnitude–depth coupling does NOT give an a-priori second-moment / deep-frequency bound. It
reduces to the FIRST-MOMENT tautology `Σᵢ Kᵢ ≤ ΣD` (= the known renewal identity), and bounding the
deep-excursion frequency `f_K = freq{o≡1 mod 2^K}` a priori IS bounding the occupancy = (K).** `[PROVEN
reduction]` The exact step: the **per-excursion archimedean cost is LINEAR in the height `K`** (the countdown
of a height-`K` excursion multiplies `|o−1|_∞` by exactly `(3/2)^K`, i.e. log-cost `=(K−1)·log(3/2)`), so the
magnitude budget charges **`log(3/2)` per `D=1` step** — a constant per unit of `K`, independent of the current
depth. Summed, this charges `Σᵢ Kᵢ` (first moment) and is **blind** to the depth-occupancy `Σₙ Vₙ = ½Σᵢ Kᵢ²`
(second moment). No adelic observable charges `K²` per height-`K` excursion; the product formula, being **one
scalar identity per term** (codim-1, additive in logs), cannot manufacture the codim-∞ / quadratic tail
control `E[K²]<∞`. Numerics confirm cost`(K)=(K−1)log(3/2)` to machine precision and exhibit the
**clustering-indifference**: a single giant excursion of height `49948` carries the *identical* archimedean
budget as the actual `≈50000` short ones, yet has `E[K²]=∞`. **No partial toward `μ({1})=0`.**

---

## 1. The per-excursion adelic budget — DERIVED `[PROVEN]`

**Excursion structure (Countdown Lemma, `NONATOMIC §1`/`REPELLER §2`).** With `V=v₂(o−1)`: a `D=1` step
(`o≡1 mod 4`, `V≥2`) sends `o'−1=(3/2)(o−1)`, so `V↦V−1`; a deep step (`D≥2`, `V=1`) refills `V` to a fresh
`r'`. So `V` descends by 1 each `D=1` step until `V=1` (deep), and the orbit visits residue `1 mod 2^k` only in
**contiguous countdown runs**. An excursion of **height `K`** (entry depth `=r'`) occupies levels
`K,K−1,…,1`, one micro-step each: `K` steps, of which `K−1` are `D=1` and the closing one is deep.

**Dual-Repulsion Lemma `[PROVEN]` (`REPELLER §1`, verified 0 fails).** On every `D=1` step:
`|o−1|_∞ ×(3/2)`, `|o−1|_2 ×2`, `oddpart(o−1) ×3`; adelic product `|o−1|_∞·|o−1|_2 ×3`.

**Per-excursion archimedean cost (derived).** Over the `K−1` `D=1` steps of a height-`K` excursion,
`|o−1|_∞` multiplies by `(3/2)^{K−1}`, so

> **`[PROVEN]` `cost_arch(K) := Δ log|o−1|_∞` over the countdown `= (K−1)·log(3/2)` — LINEAR in `K`.**

Verified exactly (`N=10⁵`): mean arch-cost per height-`K` excursion `= (K−1)log(3/2)` to 5 dp for all
`K=1..12` (table §4); `cost(K)/K → log(3/2)=0.40547` (a **constant** per unit height).

**Per-excursion 2-adic depth.** `|o−1|_2` multiplies by `2^{K−1}` (depth `K→1`); equivalently a height-`K`
excursion **requires** `o≡1 mod 2^K` at entry — a 2-adic approach to `1`.

**Adelic height (derived, `REPELLER §3`).** `H(o)=log oddpart(o−1)=log|o−1|_∞+V·log2` jumps by **exactly
`+log 3` per `D=1` step** — a **constant increment, independent of the current depth `V`**.

**Global magnitude budget `[PROVEN]` (`ADELIC_COUPLING §1`).** `log o_N = log o₀ + (Σⱼ Dⱼ)·log(3/2)+O(1)`;
verified ratio `1.000000`. The `D=1` steps contribute `#{D=1}·log(3/2)=(Σᵢ Kᵢ − #exc)·log(3/2)` to the total
`Σⱼ Dⱼ·log(3/2)`; deep steps contribute the rest.

---

## 2. Does the budget bound `Σ Kᵢ²` or only `Σ Kᵢ`? — FIRST MOMENT ONLY `[PROVEN]`

Sum the archimedean cost over all excursions:

> `Σᵢ cost_arch(Kᵢ) = Σᵢ (Kᵢ−1)·log(3/2) = #{D=1}·log(3/2) ≤ (Σⱼ Dⱼ)·log(3/2) = log o_N + O(1).`

Cancelling `log(3/2)`: **`Σᵢ (Kᵢ−1) ≤ Σⱼ Dⱼ`** — i.e. `Σᵢ Kᵢ ≲ N`. This is **exactly the renewal/first-moment
identity** (`NONATOMIC §2`: `E[K]=`mean gap`≈2`, a first-moment tautology). Verified: `Σᵢ Kᵢ/N = 1.0000`.

**Why the second moment is NOT reachable — the exact step.** The quantity controlling `μ({1})=0` is
`mean depth = Σₙ Vₙ/N = (½Σᵢ Kᵢ²)/N` ⟺ `E[K²]<∞` (`NONATOMIC §1`, renewal–reward). For the budget to bound
`Σᵢ Kᵢ²` it would need an adelic observable whose **per-excursion cost grows like `K²`**. There is none:

> **`[PROVEN]` The archimedean / adelic cost is ADDITIVE per step with a depth-independent increment
> (`(3/2)` on `|o−1|_∞`, `+log 3` on `H`). Hence the per-excursion cost is `Θ(K)` (linear), and the summed
> budget charges `Σᵢ Kᵢ` (first moment) only. The depth-occupancy `Σₙ Vₙ = ½Σᵢ Kᵢ²` is a depth-WEIGHTED sum
> (step `n` weighted by its current depth `Vₙ`); the magnitude grows at the same rate `(3/2)` regardless of
> `Vₙ`, so the budget is depth-blind and cannot see the second moment.**

**Clustering-indifference (the decisive picture) `[OBSERVED, exact]`.** The budget depends only on
`Σᵢ(Kᵢ−1)`, NOT on how those steps are partitioned into excursions. A single excursion of height
`H=Σᵢ(Kᵢ−1)=49948` carries the **identical** archimedean budget `H·log(3/2)=20252.2` as the actual `≈5·10⁴`
short excursions — yet has `Σ K² = H² = 2.5·10⁹` (`E[K²]=∞`, an atom `μ({1})>0`) versus the actual
`Σ K²=2.98·10⁵`. **The budget cannot distinguish a heavy-tailed (atom-producing) excursion profile from the
benign one.** This is precisely the `NONATOMIC §2` "giant-run obstruction": the proven first-moment budget
permits a single run of length `≈0.585N` without contradiction. The adelic coupling adds nothing here.

---

## 3. Does the product formula bound the deep-frequency `f_K` a priori? — NO; it IS occupancy/(K) `[PROVEN]`

A height-`K` excursion requires `o≡1 mod 2^K`, frequency `f_K = freq{o≡1 mod 2^K} = freq{V≥K}`. The hope: the
product formula `|o−1|_∞·|o−1|_2·∏_{p odd}|o−1|_p = 1` couples 2-adic depth (smallness of `|o−1|_2=2^{−V}`) to
archimedean size, limiting deep approaches.

**It does not.** For the integer `o−1`, the product formula is literally `o−1 = 2^V·oddpart(o−1)` — the
fundamental theorem of arithmetic, **one scalar identity per term** (`ADELIC_COUPLING §1`,
`INTRATERM_ADELIC §3`). Taking `log|·|_∞` and summing gives back the §2 first-moment renewal `log o_N=(ΣD)log(3/2)`
and nothing more. By dimension count: **product formula = codim-1 (one equation/step); the deep-frequency
`{f_K}_{K≥1}` is codim-∞ (a whole tail / all-window liminf).** A single global product `=1` cannot constrain a
distribution.

**The two costs are NOT independent (degeneracy) `[PROVEN]` (`REPELLER §3`).** One might hope the archimedean
cost `(3/2)^K` and the 2-adic rarity `f_K` *multiply* (adelic product) to doubly-suppress tall excursions. But
the adelic-height telescoping is **degenerate**: the 2-adic balance `Σ_deep(r'−1)=#{D=1}` absorbs the
archimedean side, collapsing the combined height to the trivial `ΣD` identity. The two valuations are the
**same** balance, not two constraints — combining them yields no second-moment term.

> **`[PROVEN]` Bounding `f_K` a priori IS bounding the residue-1 occupancy = `(K)`.** `f_K=lim` occupancy of
> `{V≥K}`; `μ({1})=inf_K f_K`. The product formula supplies no upper bound on `f_K`; the only adelic constraint
> is the first moment. So the deep-frequency route **reduces to occupancy/(K)**, exactly as
> `INTRATERM_ADELIC` found the product formula collapses to a first-moment tautology.

**Numerics (occupancy is geometric — evidence, not proof).** `f_K/f_{K−1}≈0.49` for `K≤10` (`f_K≈2^{−K}`,
consistent with `E[K²]<∞` and `μ({1})=0`); small-sample drift for `K≥11` (`n<20`). This is the same
equidistribution-flavoured data finite `N` can never upgrade — it is the occupancy itself, not an a-priori bound.

---

## 4. Numerics `[OBSERVED, exact big-int, N=10⁵, o₀=27]`

**Per-excursion archimedean cost = `(K−1)log(3/2)` (LINEAR), `cost/K → const`:**

| `K` | count | mean arch cost | `(K−1)log(3/2)` | `cost/K` |
|---|---|---|---|---|
| 2 | 12542 | 0.40547 | 0.40547 | 0.20273 |
| 4 | 3084 | 1.21640 | 1.21640 | 0.30410 |
| 6 | 785 | 2.02733 | 2.02733 | 0.33789 |
| 8 | 175 | 2.83826 | 2.83826 | 0.35478 |
| 10 | 45 | 3.64919 | 3.64919 | 0.36492 |
| 12 | 8 | 4.46012 | 4.46012 | 0.37168 |

Cost matches `(K−1)log(3/2)` to 5 dp (0 deviation) — **per-excursion cost is exactly linear in height.**

**First vs second moment:**
- `freq(D=1)=0.49948`, `mean D=2.00069`; total `log|o−1|` growth `=81121.0 = (ΣD)log(3/2)` ratio `1.000000`.
- **First moment (budget):** `Σᵢ Kᵢ/N = 1.0000`; `E[K]=1.998`; `Σᵢ(Kᵢ−1)=49948 ≤ ΣD=200069` (slack = deep steps). ✓
- **Second moment (NOT budgeted):** `E[K²]=5.95`; `Σᵢ Kᵢ²/N = 2.977 = 2·mean depth`; `mean depth=1.989`.
- **Clustering test:** one excursion of height `49948` → identical arch budget `20252.2`, but `ΣK²=2.49·10⁹`
  (`E[K²]=∞`) vs actual `2.98·10⁵`. Budget cannot distinguish. **Decisive.**

**Deep frequency `f_K=freq{o≡1 mod 2^K}`:** `f_1..f_{10}=1.0, .4995, .2482, .1224, .0604, .0292, .0142,
.00705, .00352, .00174`; ratios `≈0.49` (geometric `≈2^{−K}`). This is occupancy = `(K)`, not an a-priori bound.

---

## 5. Verdict (the prompt's asks)

| ask | answer | label |
|---|---|---|
| Derive per-excursion adelic budget | `cost_arch(K)=(K−1)log(3/2)` (linear); `H` jumps `+log3`/`D=1` step (depth-independent); global `log o_N=(ΣD)log(3/2)`. All derived & verified. | `[PROVEN]` |
| Does the magnitude budget bound `ΣKᵢ²` / 2nd moment, or only `ΣKᵢ` / 1st? | **Only the FIRST moment** `ΣᵢKᵢ≤ΣD` (= renewal identity). The cost is linear in `K` (depth-independent per-step increment), so it is blind to the depth-weighted `ΣₙVₙ=½ΣKᵢ²`. Clustering-indifference: a giant excursion (`E[K²]=∞`) has the same budget. | `[PROVEN]` |
| Does the product formula bound `f_K=freq{o≡1 mod 2^K}` a priori, or collapse to (K)/tautology? | **Collapses.** Product formula = one scalar/term (codim-1) = first moment; `f_K` is codim-∞. Bounding `f_K` a priori IS bounding occupancy = (K). The two valuations are degenerate (same balance), so no second-moment term. | `[PROVEN]` |
| 2nd-moment / deep-freq partial toward `E[K²]<∞` / `μ({1})=0`? | **No partial.** Reduces to occupancy/(K) and the first-moment tautology. The exact step: per-excursion cost is `Θ(K)`, never `Θ(K²)`; no adelic observable charges the depth-occupancy. | `[PROVEN reduction]` |

### The exact step, stated once
`E[K²]<∞` (`⟺ μ({1})=0 ⟺ mean depth Σₙ Vₙ/N bounded`) needs control of the **depth-weighted** occupancy
`Σₙ Vₙ = ½ Σᵢ Kᵢ²`. Every adelic quantity (archimedean magnitude `(3/2)`/step, adelic height `+log3`/step,
product formula's per-step log-identity) is **additive with a depth-INDEPENDENT per-step increment**, so its
sum is `Θ(Σᵢ Kᵢ)` = first moment. **The map from {per-step adelic increments} to {moments of K} lands in the
first moment and cannot reach the second** — that is the precise gap. The second moment is the
conditional-return-time law (`CORE_ORBIT_ARITHMETIC §5`) = the D-statistics = `(K)`.

### The gap (honest)
The adelic coupling confirms `o=1` is dual-repelling and pins the first moment exactly, but the
return-time/Lyapunov decrease `CORE_ORBIT_ARITHMETIC` seeks must live in the **second moment / tail** of the
excursion-height law `K=r'`, which the depth-blind adelic budget never charges. Supplying it = the refill law
`E_deep≤2` / single-orbit equidistribution of `V` = (K). Isomorphism of the obstruction, not a reduction.

## Sources
- Repo: `REPELLER_ESCAPE.md` (dual-repulsion ×3/2,×2,×3; adelic-height `+log3`/step; degeneracy theorem),
  `ADELIC_COUPLING.md` (product formula = first moment; `v₃(o')=D−1`), `INTRATERM_ADELIC_MINING.md`
  (codim-1 vs codim-∞ dimension count; product formula = first-moment tautology), `NONATOMIC_FIXEDPOINT.md`
  (`μ({1})=0 ⟺ f_K→0 ⟸ mean depth bounded ⟺ E[K²]<∞`; first-vs-second-moment gap; giant-run obstruction),
  `CORE_ORBIT_ARITHMETIC.md` (§5 quenched return-time/Lyapunov on `V=v₂(c−1)`, the un-pre-empted shape and its
  circularity), `DIOPHANTINE_DENSITY.md` (separation controls min-gap not density — companion no-go).
- Numerics: `scratchpad/excursion_adelic.py` (exact big-int, `N=10⁵`): linear cost `(K−1)log(3/2)`,
  `ΣKᵢ/N=1.0000`, clustering-indifference, `f_K≈2^{−K}`.

**No machine decided. No label upgraded.**
