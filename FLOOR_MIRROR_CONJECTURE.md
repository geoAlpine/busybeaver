# The Floor-Mirror of AEV Conjecture 1.6 (3/2), and the Ceiling↔Floor Bridge

*Formalizing the floor-mirror analog of Andrieu–Eliahou–Vivion Conjecture 1.6 for base 3/2, so the
floor cryptids (Antihydra family) sit under one named conjecture (2026-06-29). Soundness paramount:
every line carries `[PROVEN]`/`[CONDITIONAL]`/`[OPEN]`/`[VERIFIED]`; no label upgraded. No machine is
decided; no non-halting asserted. Numerics: `.venv` exact big-int via `floor_mirror_bridge.py`,
cross-checked against the branch identities `Tf=⌊3x/2⌋`, `Tc=⌈3x/2⌉` and the already-`bb_sim`-verified
reductions (`induced_map.py` reproduces the real `c₀=8` even-subsequence; `o10_attack`/
`CRYPTID_O10_FRAMEWORK.md` verify the literal ceiling orbit against the raw TM). NOT committed.*

Sources: `AEV_DIGEST.md` (Conj 1.6 verbatim), `MAHLER_3_2_DOMINANCE.md`,
`BB6_STRUCTURAL_LIMIT_THEOREM.md` §3,§4,§8, `ADELIC_COUPLING.md`+`WALLB_VALUATION_SHARP.md`
(GAP/Countdown lemmas, `v3(o_{j+1})=D_j−1`), `CRYPTID_O10_FRAMEWORK.md` (the literal ceiling).

---

## 0. One-line answer

> **The floor map `Tf(x)=⌊3x/2⌋` and the AEV ceiling map `Tc(x)=⌈3x/2⌉` are EXACTLY conjugate by the
> negation involution `R(x)=−x`:** `Tc = R∘Tf∘R`, i.e. `Tc(x) = −Tf(−x)` for every integer `x`
> `[PROVEN]` `[VERIFIED]`. Hence on the full domain (all of `ℤ`, equivalently `ℤ₂`) the **floor-mirror
> Conjecture 1.6(3/2) is LITERALLY EQUIVALENT to AEV Conjecture 1.6(3/2)** `[PROVEN bridge]`. The only
> residual is a **seed-sign bookkeeping** mismatch with AEV's *literally-stated* positive-only
> quantifier: the bridge sends **floor-positive orbits to ceiling-NEGATIVE orbits**, so AEV's
> positive-`n` statement maps to the floor map on *negative* seeds, and the machines' (positive) orbits
> map to *negative* ceiling seeds. Under the natural all-`ℤ₂` (sign-symmetric) form of the conjecture
> this residual vanishes; under the literal positive-only form it is a `[CONDITIONAL]` sign extension.

---

## 1. The floor-mirror conjecture, stated precisely (+ fragments)

**Maps (branch form, `[PROVEN]` elementary).** For `x∈ℤ`:

| | even `x=2k` | odd `x=2k+1` |
|---|---|---|
| **floor** `Tf(x)=⌊3x/2⌋` | `3k = 3x/2` | `3k+1 = (3x−1)/2` |
| **ceiling** `Tc(x)=⌈3x/2⌉` | `3k = 3x/2` | `3k+2 = (3x+1)/2` |

They agree on evens and differ on odds by exactly `+1` (`Tc=Tf+1` on odds): the parity-flip the source
notes call the "`±1`". `[VERIFIED]` branch defs for `x∈[−50,50]` (`floor_mirror_bridge.py` test B).

> **Floor-Mirror Conjecture 1.6 (3/2) — FM(3/2) `[OPEN]`.**
> For every starting integer `n` and every `k≥0`, the orbit `(Tf^l(n))_{l∈ℕ}` of `Tf(x)=⌊3x/2⌋` is
> equidistributed in the residue classes mod `2^k`.

This is the verbatim mirror of AEV Conj 1.6(3/2) with `⌈·⌉` replaced by `⌊·⌋`. As with AEV, the
domain of `n` matters; we make it explicit:

- **FM-`ℤ₂` (all-orbits, natural form):** quantify `n` over all of `ℤ₂` (equivalently all of `ℤ`,
  fixed point `o=1` excepted). This is the sign-symmetric form.
- **FM-`ℕ₊` (positive form):** quantify `n∈ℕ_{>0}` only — the exact mirror of AEV's literal
  positive-only quantifier.

**Fragments needed downstream (strictly weaker, in increasing strength):**

| fragment | statement | who needs it |
|---|---|---|
| **single-orbit** | FM for one fixed seed `n` only | every in-scope machine (each needs only its own orbit) |
| **level-`k`** | equidistribution mod `2^k` for one fixed `k` (e.g. `k=2`), not all `k` | Antihydra: `k=2` |
| **one-sided** | a `liminf` lower bound on one residue-class frequency, not full equidistribution | Antihydra: `liminf freq(o≡3 mod 4) ≥ 1/2` |
| **density (qualitative)** | a Cesàro/limiting frequency exists and meets a threshold | density-facet (Antihydra, o10-inner) |
| **effective-rate** | equidistribution with a *discrepancy rate* beating a summable target | existence-facet (o2,o7,o8,o18,o15,…) |

**Antihydra's exact requirement** (the weakest fragment in the program; `BB6_STRUCTURAL_LIMIT_THEOREM.md`
§4.3, §8): the **single-orbit, level-`k=2`, one-sided density** fragment of FM(3/2) at the induced seed
`o₀=27`: `liminf_N (1/N)#{l<N : D(o_l)≥2} ≥ 1/2`, where `D=v₂(3o−1)`.

**Exact comparison to AEV Conj 1.6(3/2).** AEV is the **ceiling**, **two-sided full** equidistribution,
**all `k`**, **all positive `n`**. FM differs on three independent strength axes that the source notes
already enumerate (one-sided vs two-sided; level `k=2` vs all `k`; single orbit vs all `n`) **plus** the
floor-vs-ceiling map axis resolved in §2. On the three strength axes FM-fragments are strictly *weaker*
than the full conjecture; on the map axis they are *equivalent* (§2). No named conjecture sits at the
weaker fragment level — AEV/FM is the weakest established-open named conjecture implying the kernel.

---

## 2. The ceiling↔floor BRIDGE `[PROVEN]`

**Lemma (negation conjugacy) `[PROVEN]`.** Let `R(x)=−x` on `ℤ` (equivalently on `ℤ₂`). Then
`Tc = R∘Tf∘R`, i.e.

> **`Tc(x) = −Tf(−x)` for every `x∈ℤ`.**

*Proof.* `⌈y⌉ = −⌊−y⌋` for every real `y`. With `y=3x/2`:
`Tc(x)=⌈3x/2⌉ = −⌊−3x/2⌋ = −⌊3(−x)/2⌋ = −Tf(−x)`. ∎

`R` is an involution (`R=R^{-1}`), a homeomorphism of `ℤ₂`, a group automorphism preserving Haar
measure, and on each finite quotient `ℤ/2^k` it is the residue permutation `r ↦ (−r mod 2^k)` — a
measure-preserving bijection. `[VERIFIED]` `Tc(x)=−Tf(−x)` for all `x∈[−200,200]`; and by iteration

> **`Tf^l(n) = −Tc^l(−n)` for all `l`** `[PROVEN]` `[VERIFIED]` (several `n` incl. `2^40+1`, `l<400`).

**Consequences for equidistribution `[PROVEN]`.**
- Since `R` permutes `ℤ/2^k` bijectively, a sequence `(y_l)` equidistributes mod `2^k` **iff** `(−y_l)`
  does. Combined with `Tf^l(n) = −Tc^l(−n)`:
  > **The floor orbit of `n` equidistributes mod `2^k` ⟺ the ceiling orbit of `−n` equidistributes mod
  > `2^k`.** Orbit-by-orbit, exactly. `[PROVEN]`
- This is a **measure-preserving correspondence** (in fact an exact topological+measurable isomorphism
  of dynamical systems on `ℤ₂`), the strongest possible bridge — not merely "same difficulty."

**At the induced-odd-map level the bridge is an EXACT IDENTITY of the load-bearing statistic
`[PROVEN]`.** Induced maps: floor `T(o)=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)`; ceiling
`T'(m)=3^{D'−1}(3m+1)/2^{D'}`, `D'=v₂(3m+1)`. For odd `o`, with `m=−o`:
`3m+1 = −(3o−1)`, so `D'(−o)=v₂(3o−1)=D(o)` and `T'(−o) = 3^{D−1}·(−(3o−1))/2^D = −T(o)`. Hence

> **`D_l^{ceil}(−o₀) = D_l^{floor}(o₀)` for every `l`** — the depth/gap sequences are *literally identical*,
> not just equidistributed. `[PROVEN]` `[VERIFIED]` `200,000` induced steps, `o₀=27` vs `m₀=−27`,
> `0` exceptions; `mean D` identical to `1.996270`; `freq(D≥2)` identical to `0.499660`.

So the GAP-LEMMA `D=v₂(3o±1)` (`WALLB_VALUATION_SHARP.md` §1) is exactly the bridge the source notes
named: the *same* depth statistic drives both maps, with `3o−1` (floor) `↔` `3m+1=−(3o−1)` (ceiling)
under negation. (The `v₃(o_{j+1})=D_j−1` coupling of `ADELIC_COUPLING.md` §1a transfers verbatim, since
`3m+1≡1 (mod 3)` mirror of `3o−1≡−1 (mod 3)`.)

**The precise residual / obstruction `[PROVEN-characterization]`.** The conjugacy `R` maps **positive
floor orbits to negative ceiling orbits**, never positive→positive. There is **no** conjugacy
`Tf↔Tc` on the positive integers alone: on odds `Tc=Tf+1`, and the two positive orbits *diverge*
(`Tc(x+j)−Tf(x)` grows like `(3/2)^l`; explicitly `Tc(x+1)=Tf(x)+2`, not a conjugacy because the shift
`1↦2` is not preserved). So:

> **The bridge is `[PROVEN]` and exact on the full domain (all `ℤ`/`ℤ₂`), where floor-mirror and
> ceiling are LITERALLY EQUIVALENT. The single residual is the seed-sign quantifier: floor-positive
> ⟺ ceiling-NEGATIVE (not ceiling-positive). The natural all-`ℤ₂` conjecture is sign-symmetric so the
> residual vanishes; AEV's literal positive-only statement leaves a `[CONDITIONAL]` sign extension.**

`[VERIFIED]` (test D): along the full orbits, `floor(+27)` residue `r` count `=` `ceil(−27)` residue
`(−r mod 2^k)` count **exactly** for `k=2,3,4` (bridge identity); while `floor(+27)` and `ceil(+27)`
are genuinely *different* orbits (distributions differ) though both within `≈0.002` of uniform.

---

## 3. Does AEV 1.6(3/2) imply the floor-mirror version? — exact logical relationship

| implication (base 3/2) | status | reason |
|---|---|---|
| **AEV-ceiling(all `ℤ₂`) ⟺ FM-floor(all `ℤ₂`)** | **`[PROVEN]`** (biconditional) | negation conjugacy `Tc=R∘Tf∘R`, `R` Haar-preserving + residue-permuting (§2) |
| **AEV-ceiling(literal `ℕ₊`) ⟹ FM-floor(`ℕ₊`)** | **`[CONDITIONAL]`** on sign-symmetry | the bridge gives AEV-`ℕ₊` ⟺ FM on *negative* seeds; floor-positive ⟺ ceiling-*negative*, which AEV's positive quantifier does not contain |
| **AEV-ceiling(literal `ℕ₊`) ⟹ FM-floor on the machines' (positive) seeds** | **`[CONDITIONAL]`** on the negative-seed (≡ all-`ℤ₂`) extension | Antihydra's `o₀=27` floor orbit ≡ the ceiling orbit at `−27` (§2), a *negative* ceiling seed outside AEV's literal scope |
| **AEV-ceiling(all `ℤ₂`) ⟹ the machines' fragments** | **`[CONDITIONAL]`, over-implied** on the density facet | qualitative all-`k` equidistribution over-implies Antihydra's one-sided level-`k=2` density fragment; the existence-facet members need *effective-rate*, **stronger** than AEV (§4) |

**Net.** The floor-mirror conjecture is **not a new open problem**: on the natural domain it is the
*same* conjecture as AEV 1.6(3/2), with a `[PROVEN]` exact bridge. The only honest caveat is the
seed-sign quantifier. Two equally valid ways to discharge it, both sound:
1. **Adopt the all-`ℤ₂` (sign-symmetric) form of Conj 1.6** — the mathematically natural form, under
   which AEV(3/2) and FM(3/2) are *literally equivalent* `[PROVEN]`; or
2. **Keep AEV's literal positive form** — then "AEV(3/2) ⟹ FM(3/2) at the machines' seeds" is
   `[CONDITIONAL]` on the (believed, unproven) sign-symmetry / negative-seed extension. The conjugacy
   does **not** by itself bridge ceiling-positive to ceiling-negative (negation maps ceiling↔floor, not
   ceiling↔ceiling, and no positive-only conjugacy exists, §2).

There is no *direct* (non-bridge) argument that closes the sign gap: it is exactly the gap between
AEV's chosen positive domain and the full `ℤ₂` dynamics, and is cosmetic only under the standard
expectation that these equidistribution conjectures are sign-blind.

---

## 4. Clean restatement of the dominance implication

With FM(3/2) formalized and the bridge `[PROVEN]`, `MAHLER_3_2_DOMINANCE.md` §2/§4 restates cleanly:

> **The Floor-Mirror AEV 1.6(3/2) conjecture ⟹ the 10 `μ=3/2` machines** (Antihydra, o2, o7, o8,
> o10-inner, o11, o12, o13, o14, o16), with the following **exact per-machine scope** — and the
> floor-mirror is `[PROVEN]`-equivalent to literal AEV(3/2) on the full domain (§2,§3), so this is one
> named conjecture, not a new one.

| machine | seed (induced) | facet | exact fragment of FM(3/2) it needs | what closing FM(3/2) gives |
|---|---|---|---|---|
| **Antihydra** | floor `o₀=27` (≡ ceiling `−27`) | **density** | **single-orbit, level-`k=2`, one-sided** `liminf freq(o≡3 mod4)≥1/2` | **decided `[CONDITIONAL]`**; qualitative FM **over-implies** it; + finite check `balance_n≥0` `[VERIFIED]` to `2·10⁵` |
| **o10-inner** | **ceiling `m₀=9`** (literal AEV side, **no bridge**) | density (inner sub-orbit) | single-orbit, level-`k`, one-sided (inner) | **decided `[CONDITIONAL]`** for the inner kernel; o10-FULL composite/OUT (irregular two-level refill, `[OPEN]`) |
| **o2, o7, o8** | floor reset orbits `5,11,…` / `6,11,…` / `2,4,7,…` | **existence** | single-orbit **effective-rate** (avoid a thin clopen target forever) | **kernel input only, NOT decided**: (i) exact `2^k` halt predicate `[OPEN]` (not derived); (ii) needs effective rate, **stronger** than qualitative FM |
| **o11, o12, o13, o14, o16** | nested floor `3/2` sea/refill orbits | existence (density-type growth) | single-orbit effective-rate + completed nested predicate | **kernel input only, NOT decided**: exact predicate `[OPEN]`; nested/doubly-exp refill not yet a clean scalar event |

**Scope ledger (verbatim discipline, none upgraded):**
- **One-sided fragment suffices** for: **Antihydra** (and the o10-inner sub-orbit, `[CONDITIONAL]`).
  Qualitative FM(3/2) over-implies these (gives exact density `1/2 ≥ 1/3`).
- **Effective rate required** for: **all existence-facet `3/2` machines** (o2,o7,o8,o11–o14,o16) — they
  must *avoid* a thin (summable) target, which qualitative equidistribution does **not** give; this is
  **strictly stronger** than FM(3/2) as stated (`BB6_STRUCTURAL_LIMIT_THEOREM.md` §7.1).
- **Exact predicate still to be completed (`V2`/`V3` = the `v₂(3o−1)` / `v₃(o_{j+1})=D−1` valuation
  predicates):** for o2,o7,o8,o11–o16 the halt event is pinned only to a head-local "reads 0" hitting
  event; the exact `2^k` (resp. `2^a/3^b` carry) predicate in terms of the verified valuation identities
  is **not yet derived** (`[OPEN]`). The `v₂`/`v₃` identities themselves are `[PROVEN]`+`[VERIFIED]`
  (`WALLB_VALUATION_SHARP.md` §1, `ADELIC_COUPLING.md` §1a) and transfer across the bridge (§2), but the
  reduction "halt ⟺ [explicit valuation event]" is completed only for Antihydra (and o10-inner).
- **Barrier:** the `[PROVEN]` density `β=+1/2>0` no-structure-only barrier (ergodic optimization,
  halting fixed point `o=1`; ceiling mirror `m=−1`) holds for **Antihydra only** (o10-inner
  `[CONDITIONAL]`); existence-facet members have **no `β`** — their barrier is the `[OPEN]`
  over-approximation top.

**Honest count.** FM(3/2)≡AEV(3/2) supplies the kernel for **10 of 17** frontier machines (the dominant
single conjecture); but only **2 are decided outright `[CONDITIONAL]`** (Antihydra, o10-inner), the
other **8 are reduced modulo (a) completing their exact valuation predicate and (b) an effective-rate
strengthening for the existence facet**. The morally-correct headline ("one named problem under the
`3/2` cluster") is sound; the literal "one conjecture decides all ten" remains over-claimed (flagged in
`MAHLER_3_2_DOMINANCE.md` §2), now with the floor↔ceiling axis fully closed `[PROVEN]`.

---

## 5. Numerical verification of the bridge `[VERIFIED]` (`floor_mirror_bridge.py`, `.venv` exact)

```
(B) branch defs Tf=floor(3x/2), Tc=ceil(3x/2) for x in [-50,50]: True
(A1) Tc(x) == -Tf(-x) for x in [-200,200]: True                       # conjugacy, exact
(A2) Tf^l(n) == -Tc^l(-n) for several n (incl 2^40+1), l<400: True    # orbit-level conjugacy
(C) induced depth equality D_l^floor(27)==D_l^ceil(-27) over 200000 steps: True
    mc == -of at end: True
    mean Df = 1.996270  mean Dc = 1.996270  (Haar 2)                  # identical statistic
(E) freq(D>=2) floor(27)=0.499660  ceil(-27)=0.499660  identical: True# Antihydra kernel, identical
(D) k=2: bridge identity floor(+27)[r]==ceil(-27)[-r]: True | maxdev floor=0.0018 ceil(+27)=0.0009 | floor(+27)==ceil(+27): False
(D) k=3: bridge identity floor(+27)[r]==ceil(-27)[-r]: True | maxdev floor=0.0017 ceil(+27)=0.0014 | floor(+27)==ceil(+27): False
(D) k=4: bridge identity floor(+27)[r]==ceil(-27)[-r]: True | maxdev floor=0.0019 ceil(+27)=0.0015 | floor(+27)==ceil(+27): False
```

**Reading.** (A)/(B) confirm the conjugacy `Tc=R∘Tf∘R` at the map and orbit level (exact big-int).
(C)/(E) confirm the strongest form of the bridge — the induced **depth sequences are literally identical**
for floor-`27` and ceiling-`(−27)`, so Antihydra's entire load-bearing statistic is carried verbatim.
(D) confirms the **residue bridge identity** `floor(+27)[r] = ceil(−27)[(−r) mod 2^k]` holds *exactly*
(not approximately) for `k=2,3,4`, while floor-`27` and ceiling-`+27` are genuinely *different* orbits
(distributions differ) — the precise content of "floor-positive ↔ ceiling-negative, not ceiling-positive."
Both stay within `≈0.002` of uniform (consistent with, not proof of, equidistribution).

*Finite `N` proves nothing about the `liminf`; the equidistribution kernel itself is `[OPEN]`. What is
`[PROVEN]` here is the bridge: floor and ceiling 3/2 are the same dynamical system up to the negation
isomorphism, so the floor-mirror conjecture is the AEV conjecture, and the floor cryptids sit under it.*

---

## 6. Verdict (the asks)

1. **Floor-mirror conjecture:** FM(3/2) = "every orbit of `Tf(x)=⌊3x/2⌋` equidistributes mod `2^k`,
   for all `n`, all `k`." Fragments: single-orbit ⊃ level-`k` ⊃ one-sided ⊃ density (qualitative) ⊂
   effective-rate. Antihydra needs single-orbit + level-`k=2` + one-sided density at `o₀=27`. `[OPEN]`.
2. **Floor ↔ ceiling EQUIVALENT?** **YES, `[PROVEN]` bridge** via the exact negation conjugacy
   `Tc=R∘Tf∘R`, `Tc(x)=−Tf(−x)`. Equivalent on all of `ℤ₂`. **Obstruction = seed-sign only:** the
   bridge maps floor-positive to ceiling-*negative*; no positive-only conjugacy exists (the maps differ
   by `+1` on odds and the positive orbits diverge geometrically).
3. **AEV(3/2) ⟹ floor version?** `[PROVEN]` biconditional on the all-`ℤ₂` (sign-symmetric) domain;
   `[CONDITIONAL]` (on the negative-seed/sign extension) for AEV's literal positive-only statement,
   because the machines' positive floor orbits map to negative ceiling seeds outside AEV's stated scope.
4. **Dominance restatement:** FM(3/2)≡AEV(3/2) ⟹ the 10 `μ=3/2` machines, with: Antihydra (+ o10-inner)
   needing only the **one-sided** fragment (decided `[CONDITIONAL]`, qualitative over-implies); all
   existence-facet members (o2,o7,o8,o11–o16) needing **effective rate** (stronger than AEV) **and**
   their **exact `v₂`/`v₃` valuation predicate completed** (`[OPEN]`); barrier `β>0` `[PROVEN]` for
   Antihydra only.

*No machine decided; no non-halting asserted. Bridge `[PROVEN]`+`[VERIFIED]`; kernel `[OPEN]`.*
