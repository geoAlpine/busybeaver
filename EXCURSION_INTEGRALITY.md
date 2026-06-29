# Does integrality / the floor-map arithmetic forbid heavy-tailed excursions a priori? (2026-06-30)

*WEAPONS_AUDIT-style. Sub-route of the a-priori excursion estimate on `V=v₂(c−1)`. Question: does the
**integrality** of the floor map `c↦⌊3c/2⌋` — the `−1` in `(3c−1)/2`, the integer constraint, the M4
valuation budget — forbid a HEAVY-TAILED excursion-height distribution a priori, i.e. bound the tail
`P(K≥k)` or the energy `ΣKᵢ²` WITHOUT assuming the D-law / (K)? Excursion height (prompt def)
`K = v₂(3o−1) =` jump depth of the induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `o₀=27` (= induced odd
orbit of `c₀=8`); a height-`K` excursion needs `o ≡ 3⁻¹ mod 2^K`. `E[K²]<∞ ⟺` mean depth bounded `⟺
μ({1})=0` (NONATOMIC). SOUNDNESS PARAMOUNT; every line labelled; (K) NOT claimed; willing to retract.
Numerics `.venv`, exact big-int, N=10⁵, `scratchpad/exc_integ.py`. NOT committed.*

---

## 0. One-line verdict

**Integrality / floor-structure does NOT give an a-priori tail or second-moment bound — it is
exactly as bias-blind / (K)-hard for the SECOND moment as it is for the first.** The `−1` and the
integer constraint only (i) *define* the arithmetic progression `o ≡ 3⁻¹ mod 2^K` that a height-`K`
excursion must hit, and (ii) via `v₂(c_n)=o(n)` pin the first-moment SUM `ΣKᵢ=O(N)` and the crude
support cap `Kᵢ≤0.585n`. Converting these into any tail rate `P(K≥k)=O(k^{−(1+ε)})` or energy bound
`ΣKᵢ²=O(N)` requires the **visit FREQUENCY** of that AP — which *is* its occupancy `f_K≈2^{−(K−1)}` =
single-orbit equidistribution = (K). **New here:** the deep-excursion **spacing** route also fails —
integrality imposes **no a-priori spacing** between deep excursions; they cluster at the iid rate
(min gap = 1, adjacent height-`≥k` pairs occur, count ≈ `N·p²`), so the dual-repulsion that ends each
*countdown run* does NOT repel *deep entries* from one another. No partial moment is bought.

---

## 1. What integrality actually supplies, exactly [PROVEN]

The only quantitative outputs of the integer/floor structure are three, all proven elsewhere:

- **(I1) The defining AP.** `K=v₂(3o−1)≥k ⟺ 3o≡1 mod 2^k ⟺ o ≡ 3⁻¹ mod 2^k` — a single odd residue
  class mod `2^k`, Haar density `2^{−(k−1)}` among odds. The `−1` is precisely what makes the target
  an AP through `3⁻¹` rather than through `0`. [PROVEN; this is just `v₂(3o−1)`.]
- **(I2) The valuation budget (M4, first moment).** `Σ_{odd i<n} v₂(3cᵢ−1) = n + v₂(c_n) − v₂(c₀)`
  (`VALUATION_BUDGET.md`). With `c_n ~ A(3/2)ⁿ` integer, `v₂(c_n) ≤ ⌊log₂ c_n⌋ ≈ 0.585n`, and observed
  `v₂(c_n)=O(log n)`. [PROVEN exact identity.]
- **(I3) The support cap.** From `0 ≤ v₂(c_n) ≤ 0.585n`: each `Kᵢ ≤ 0.585·(position)` and
  `ΣKᵢ = #{dₙ≥1} ≤ N (+O(log N))`. [PROVEN.]

**(I1) is a SUPPORT statement; (I2)/(I3) are a SUM/COUNT and a MAX.** None is a frequency. This is the
whole of what "the arithmetic of `⌊3c/2⌋`" contributes a priori.

---

## 2. Does (I2)/(I3) forbid a heavy tail? — NO, the gap is total [PROVEN negative]

**The budget is bias-blind to the SECOND moment exactly as to the first.** The budget RHS `n+v₂(c_n)`
is bounded by `n+o(n)` for a reason **external to the depth distribution** (you cannot spend more
2-adic valuation than the orbit's magnitude permits). It pins the *value* of `ΣKᵢ`; it says nothing
about how that sum splits across small vs large excursions. Concretely, with the proven envelope
`Kᵢ≤0.585n`, `ΣKᵢ≤N`, a **single** excursion of height `K≈0.585N` is consistent with **every** proven
identity, and it gives `ΣKᵢ² ≥ (0.585N)² ≫ N`, i.e. `E[K²]=∞`, `μ({1})≥0.585`. So:

> **[PROVEN] No support/sum bound from integrality (however good, short of `max K=O(1)`) yields any
> fractional moment `E[K^{1+ε}]<∞`, ε>0.** `ΣK^{1+ε} ≤ (max K)^ε·ΣK ≤ (0.585N)^ε·N = O(N^{1+ε})`,
> a factor `N^ε` above the `O(N)` needed; even the (unproven) `max K=o(N)` fails — `g(N)^ε·N=O(N)`
> only if `g` is *bounded*, false. (Same calculation as `EK2_PARTIAL_MOMENTS §3`.)

**No exact second-moment identity exists.** Any current-depth potential `Q(dₙ)` telescopes `ΣKᵢ^p`
into (countdown decrements) + (refill injections) which are the SAME `p`-th moment — the identity
**closes on itself**, free at `p=1` (refill = count `≤N`, the budget) and `(K)`-hard at `p=2` (refill
= `Σdₙ` itself, no `O(N)` cap) (`EK2_SECOND_BUDGET §3`). **The integer `−1`/floor enters the budget
only through `v₂(c_n)=o(n)`, which is a first-moment input; there is no integrality fact that injects
into the `p=2` accounting.** [PROVEN: the second moment is equally bias-blind.]

---

## 3. The deep-excursion SPACING route — also fails, NOT via the min-gap-vs-density wall [OBSERVED, decisive]

The remaining hope distinct from §2: even if no single bound caps the tail, perhaps the **dynamics**
forbid two deep excursions close together in `n` (an a-priori spacing), which would bound their
frequency. The dual-repulsion (`REPELLER_ESCAPE.md`) proves the orbit *escapes* each deep cylinder.
**Does that escape repel deep ENTRIES from one another?**

**Two distinct "excursion" notions must not be conflated:**
- **Within one full-orbit countdown run**, depths are forced to *decrease* `K,K−1,…,1` (Countdown
  Lemma, `MINPROP_RUNS §2`) — so residue-`1 mod 2^k` visits are contiguous, never clustered. This is
  the self-limiting structure, and it is the only "repulsion" integrality proves.
- **Between induced-map deep JUMPS** (the prompt's `K=v₂(3o−1)` = entry depths of *successive* runs)
  there is **no such constraint.** After a deep jump `o ≡ 3⁻¹ mod 2^K`, the successor
  `o' = 3^{D−1}(3o−1)/2^D` is free to land in `3⁻¹ mod 2^k` again.

**Numerics [OBSERVED, `exc_integ.py`, N=10⁵] settle it: deep excursions cluster at the iid rate.**

| k | #{K≥k} | min gap | mean gap | #adjacent (gap=1) | iid pred `N·p²` |
|---|---|---|---|---|---|
| 2 | 50052 | **1** | 2.00 | 24927 | 25052 |
| 4 | 12488 | **1** | 8.01 | 1525 | 1559 |
| 6 | 3146 | **1** | 31.8 | 80 | 99 |
| 8 | 803 | **1** | 124.6 | 3 | 99→3 |
| 10 | 200 | 2 | 495 | 0 (finite-N) | — |

> **[OBSERVED] The minimum spacing between height-`≥k` excursions is `1` (adjacency occurs) up to
> `k=8`, and the count of adjacent deep pairs ≈ the iid prediction `N·p²` (mild ≤sub-1σ
> anti-correlation at small counts, within noise).** So integrality imposes **NO a-priori positive
> spacing**; two deep excursions can be adjacent. The route does NOT even reach the
> min-gap-vs-density wall (`DIOPHANTINE_DENSITY`) — it fails earlier, because there is no nontrivial
> min-gap to play against density. A heavy tail (clustered deep excursions, or one giant one) is not
> excluded by any spacing/anti-clustering mechanism. *(Consistent with `EK2_TAIL_SEPARATION`'s verdict
> (c): separation/BC cannot bound the occupancy tail; countdown forces only min index-gap 1.)*

---

## 4. Where it bottoms out: the AP frequency = (K) [PROVEN reduction]

The AP-occupancy is the *only* missing quantity, and it is exactly the equidistribution wall:

| k | freq(`o ≡ 3⁻¹ mod 2^k`) | Haar `2^{−(k−1)}` | ratio |
|---|---|---|---|
| 4 | 0.124880 | 0.125000 | 0.999 |
| 7 | 0.015900 | 0.015625 | 1.018 |
| 10 | 0.002000 | 0.001953 | 1.024 |
| 13 | 0.000190 | 0.000244 | 0.778 (finite-N) |

`f_K := freq(o ≡ 3⁻¹ mod 2^K) ≈ 2^{−(K−1)}` [OBSERVED geometric]. A tail bound is `f_K=O(k^{−(1+ε)})`
or better; the heavy-tail scenario is `f_K ↛ 0` fast enough, equivalently the orbit over-occupies a
deep class. **Integrality (I1) names this class through `3⁻¹` and the `−1`; it does not bound how
often the iterated-floor orbit visits it.** That visit frequency is the single-orbit equidistribution
of `o_n mod 2^k` = the Mahler `(3/2)ⁿ` / AEV kernel = (K) (`CORE_ORBIT_ARITHMETIC §4–5`: the action is
twisted by `÷2^{D_n}`, non-unit, so it does not descend to a finite quotient — that non-descent IS the
non-integrality of 3/2).

> **The exact step that breaks:** the integer/floor structure yields `v₂(c_n)=o(n)` ⇒ first-moment
> SUM `≤N` + support `K≤0.585n` (§1). Upgrading either to a **tail/2nd-moment** bound needs the AP
> **frequency** `f_K` (a count-per-class), which integrality does not supply — the `−1`/floor are
> *blind to occupancy*, just as M4 proved them blind to even-density bias (`M4_P2_RESULT.md`). The
> frequency is (K).

---

## 5. Numerics [OBSERVED, exact big-int, N=10⁵, `exc_integ.py`]

- `E[K]=2.0007`, `E[K²]=6.0035`, `max K=16 ≈ log₂N=16.6`. `ΣK²/N` stable across prefixes
  (¼N..N: 5.97, 6.03, 6.01, 6.00) — **OBSERVED bounded, unbounded by proof.**
- Tail `P(K≥k) ≈ 2^{−(k−1)}` (ratio 0.99–1.03 to k≈10) — geometric, consistent with `E[K²]<∞`,
  evidence not proof.
- **Spacing:** min gap between height-`≥k` excursions = 1 (adjacency) up to k=8; adjacent-pair count
  ≈ iid `N·p²` — **no a-priori spacing.** (§3.)
- **AP-occupancy** `freq(o≡3⁻¹ mod 2^k) ≈ 2^{−(k−1)}` (Haar) — the frequency IS the genericity
  quantity. (§4.)

---

## 6. Honest verdict (a)/(b)/(c)

| option | status |
|---|---|
| **(a)** integrality/floor gives an a-priori tail `P(K≥k)` or 2nd-moment `ΣKᵢ²=O(N)` bound (partial!) | **NOT achieved** — §2 (support/sum yields no ε), §3 (no spacing), §4 (frequency missing) |
| **(b)** the 2nd moment is as bias-blind / (K)-hard as the first, with the exact step | **THIS** — `−1`/budget feed only `v₂(c_n)=o(n)` ⇒ first-moment SUM + support; the `p=2` accounting closes on itself (`EK2_SECOND_BUDGET`); exact gap = AP frequency `f_K` (§4) |
| **(c)** reduces to (K) | the missing `f_K = freq(o≡3⁻¹ mod 2^k)` IS single-orbit equidistribution of `o_n mod 2^k` = Mahler/(K)-adjacent (§4), consistent with EK2/NONATOMIC/MINPROP |

**New, banked (negative but sharp):** the **deep-excursion spacing** route is closed with a *proven
reason* — the Countdown self-limitation acts only *within* one run (forcing decrease), and imposes **no
spacing between successive deep entries**, which cluster at the iid rate (min gap 1, adjacency
present). So this route fails *earlier* than the min-gap-vs-density wall: there is no nontrivial min-gap
to deploy. Integrality is occupancy-blind for the tail exactly as M4 found it bias-blind for the mean.

---

## 7. Sources

- `EK2_PARTIAL_MOMENTS.md` — no fractional moment from support/sum (§2 calc reused); first-moment SUM
  is the only free fact; gap = pointwise tail rate.
- `EK2_SECOND_BUDGET.md` — no exact 2nd-moment identity; `p`-potential telescopes `ΣK^p` to itself
  (free p=1, (K)-hard p=2). [Used §2.]
- `EK2_TAIL_SEPARATION.md` — separation/anti-clustering/BC cannot bound `Σf_k`; countdown forces min
  index-gap 1. [Used §3.]
- `NONATOMIC_FIXEDPOINT.md` — `μ({1})=0 ⟺ f_k→0 ⟸ mean depth bounded ⟺ E[K²]<∞`; a single ≈0.585N run
  ⇒ `E[K²]=∞`, atom ≥0.585.
- `MINPROP_RUNS.md` — Countdown Lemma `φ→φ−1`; run⟺thin-cylinder `o≡1 mod 2^{m+1}`; self-limiting
  *within* a run only. [Used §3.]
- `VALUATION_BUDGET.md` — exact M4 budget `Σv₂(3cᵢ−1)=n+v₂(c_n)−v₂(c₀)`; support `K≤0.585n`;
  `avgD≥3/2`. [Used §1.]
- `M4_P2_RESULT.md` — integrality is bias-blind (rigidity, not density). [The mean-analog of §4.]
- `CORE_ORBIT_ARITHMETIC.md` — the `÷2^{D_n}` twist does not descend to a finite quotient = the
  non-integrality of 3/2; AP frequency = (K). [Used §4.]
- Numerics: `scratchpad/exc_integ.py` (exact big-int; tail, `ΣK²/N`, spacing/adjacency, AP-occupancy;
  N=10⁵, induced odd map `o₀=27`).

---

No machine decided. No label upgraded.
