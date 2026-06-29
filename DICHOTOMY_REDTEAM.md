# Red-team: the constant-on-M vs measure-selecting dichotomy (2026-06-30)

*Adversarial audit of the proposed unifying dichotomy that splits the Antihydra obstruction
landscape into UNCONDITIONALLY-PROVABLE (= constant over the attainable invariant-measure set M)
vs (K)-HARD (= varies over M, value at Haar is the target). Job: try to FALSIFY it. SOUNDNESS:
zero false proofs; labels [PROVEN]/[PROVEN-in-lit]/[OBSERVED]/[OPEN]; no label upgraded; no machine
decided. Numerics `scratchpad/rt.py`, exact big-int, N=10^5. NOT committed.*

---

## 0. One-line verdict

**DICHOTOMY SURVIVES — but NEEDS AMENDMENT.** The literal claim "FREE ⟺ constant on M" with the
**M as defined** (the specification / ergodic-optimization set that *contains the halting fixed point
`δ₁`*) is **FALSIFIED on its FREE half** by at least four PROVEN results — `#even(n) ≥ 0.89 log n`,
subword-complexity `p(ℓ) ≥ 1.71ℓ`, non-periodicity (C3), top-digit equidistribution — each of which is
**not constant on that M** (each FAILS at `δ₁`). The HARD half is sound and in fact PROVEN-backed. The
defect is a **conflation of two different M's** in the definition; once M is fixed correctly the
dichotomy holds, in a form the corpus already half-states (the *topological-entropy (FREE) vs
measure-entropy (HARD)* axis is the whole principle in miniature). No **hard-but-constant**
counterexample exists. No machine decided. No label upgraded.

---

## 1. The fatal ambiguity in M (direction 4 — and the source of every counterexample)

The definition packs two **incompatible** sets under one symbol:

- **M_sys** = *all* `T`-invariant probability measures of the induced odd map (a full-branch Bernoulli
  shift). By **specification + ergodic-optimization** this is huge: it contains `δ₁` (Dirac at the
  halting fixed point `o=1`, `freq(D≥2)=0`), `δ_{3/5}` (`freq=1`), Haar (`freq=1/2`), and a
  **full-Hausdorff-dimension** family realizing every Birkhoff value in `[0,1]`
  (`MINPROP_COUPLING.md` §2, `MINPROP_COBOUNDARY_LP.md` §3). This is the set the meta-theorems describe.
- **M_orb** = the weak-* limits of the **empirical measures of the *specific* seed-8 orbit**
  ("orbit-empirical limits / Birkhoff values"). This is conjecturally a single point `{Haar}` — and
  *that conjecture is exactly (K)*.

The definition says M is *"the set of measures realizable as orbit-empirical limits"* (= M_orb) *"which
…is a large set containing …δ₁"* (= M_sys). **These are not the same set.** `δ₁` is in M_sys but the
seed-8 orbit provably escapes the fixed point (it grows like `(3/2)ⁿ` and is non-periodic), so `δ₁` is
**not** an empirical limit of seed-8 in the naive sense. Every counterexample below exploits exactly
this gap: a quantity proven for seed-8 by **topological / growth** data that *excludes the bad atoms*,
which therefore is **not** constant on the atom-containing M_sys.

---

## 2. Tier-by-tier audit table

Legend — **Kind:** UI = universal pointwise identity/inequality (holds for *every* orbit); ANN =
annealed / a.e. / fixed-measure Fourier fact; TOP = **topological / tail invariant of the orbit
closure** (not a function of any single invariant measure); MF = **measure functional** (a Birkhoff
average / function of the invariant measure). **`δ₁`?** = does the stated PROVEN fact hold at the
halting fixed point `δ₁ ∈ M_sys`?

| # | Catalogued result | Status | Kind | Const. on **M_sys**? | Const. on **M_orb / M_feas** (§4)? | Fits dichotomy? |
|---|---|---|---|---|---|---|
| F1 | Valuation budget `Σv₂(3c_i−1)=n+v₂(c_n)−v₂(c_0)` | [PROVEN] | UI | **YES** (true at `δ₁` too) | yes | FREE ✓ |
| F2 | GAP/Countdown/Dual-repulsion; `ψ=fn(D)`; floor-mirror; family classn | [PROVEN] | UI | YES | yes | FREE ✓ |
| F3 | 2-adic FLP budget range `n−v₂(c₀)≤Σv₂≤1.585n−3` | [PROVEN] | UI | YES (range) | yes | FREE ✓ |
| F4 | Induced map = exact Bernoulli; `D_j` iid geom, mean 2 | [PROVEN] | ANN (Haar) | n/a (a statement *about* Haar) | — | FREE ✓ |
| F5 | Rajchman `ν̂_{2/3}→0`; `Φ(N)→0`; `C=0.7748…`; Salem–Zygmund; Vaaler J=5; transfer-op a.e. CLT | [PROVEN(-in-lit)] | ANN | n/a (fixed annealed measure / a.e. ξ) | — | FREE ✓ |
| F6 | FLP spread `Ω(3/2)≥1/3`; Zudilin `‖(3/2)ⁿ‖>0.5803ⁿ` | [PROVEN-in-lit] | UI (support/pointwise) | YES (∀ξ) | yes | FREE ✓ |
| **C1** | **`#even(n) ≥ 0.89 log n`** (only quantitative count for the seed) | **[PROVEN]** | **TOP/tail** | **NO** — `δ₁` has **0** even steps | yes (orbit unbounded) | **counterexample → amend** |
| **C2** | **Subword complexity `p(ℓ) ≥ 1.71ℓ`** | **[PROVEN]** | **TOP** | **NO** — `δ₁` orbit has `p(ℓ)=O(1)` | yes | **counterexample → amend** |
| **C3** | **Non-periodicity (C3): orbit eventually-aperiodic** | **[PROVEN]** | **TOP** | **NO** — `δ₁` is periodic | yes | **counterexample → amend** |
| **C4** | **Top-digit equidist.: top `Θ(log N)` digits equidistribute** | **[PROVEN]** | **TOP/growth** | **NO** — needs growth; trivial at `δ₁` | yes | **counterexample → amend** |
| F7 | Certificate-complexity hierarchy (5 strict separations) | [PROVEN] | TOP/descriptive | not a measure fn (orthogonal to M) | — | FREE (topological) — see §3.3 |
| K1 | even-density `≥ 1/3` ⟺ mean `D ≥ 3/2` (= non-halt) | [OPEN] | MF | **NO — varies `[0,1]`**, Haar `1/2` | =(M_orb={Haar}) | HARD ✓ |
| K2 | single-orbit equidist. `c_n mod 2^k` (= (K) = Mahler/AEV) | [OPEN] | MF | NO — varies | = "M_orb={Haar}" | HARD ✓ |
| K3 | odd-character feedback `Inj_a→0`; `M₂ᵒᵈᵈ=o(2^k)` | [OPEN] | MF | NO — varies | varies | HARD ✓ |
| K4 | measure entropy (vs topological entropy `=log2`, FREE/constant) | — | MF | NO — `δ₁` has `h=0`, Haar `>0` | varies | HARD ✓ |

---

## 3. Counterexample hunt — the three directions

### 3.1 Direction 1 — "FREE ⟹ constant on M": **FALSIFIED as literally stated** (rows C1–C4)

The cleanest is **C1, `#even(n) ≥ 0.89 log n`** (`EVEN_DENSITY_PARTIAL.md`). It is [PROVEN]
*unconditionally for the specified seed*, hence FREE. Its value at the halting fixed point
`δ₁ ∈ M_sys` is **0 even steps, forever** (verified `rt.py`: `c=1 → 1 → …`, zero even steps; seed-8
`#even = 50159` at `N=10⁵`). So the proven quantity is **NOT constant over M_sys** — a proven fact that
takes different values on different members of the very set the definition names. By the dichotomy's
own contrapositive, FREE-but-not-constant-on-M should be impossible. **It happens.** Same structure for
C2 (subword complexity collapses to `O(1)` at the periodic `δ₁`), C3 (`δ₁` *is* periodic), C4 (no
growth at `δ₁`, top digits don't equidistribute).

**Why this does not actually break the program**, and the precise repair: each proof uses **topological
/ growth** data, not a Birkhoff average. C1's engine is `c_p ∼ A(3/2)^p` (unbounded) ⇒ the orbit is not
the bounded all-odd fixed point ⇒ infinitely many even steps; C2/C4 likewise ride orbit growth and
`log₂3` irrationality; C3 is the integer-growth-past-all-cycles argument
(`WALLB_NONATOMIC.md`). These facts **exclude the atoms** `δ₁` (and all low periodic orbits) from being
relevant to seed-8. They are constant on the *correct* set (§4), just not on the atom-laden M_sys. So
the FREE tier provably contains a **topological sub-mechanism** that "constant on M (measures)" cannot
express — because some FREE facts are **not measure functionals at all** (C1 is a *tail* statement,
finer than any empirical measure; see §3.4).

### 3.2 Direction 2 — "(K)-HARD ⟹ varies on M": **no counterexample; in fact PROVEN-backed**

I searched for a (K)-hard target that is **constant on M_sys** (which would be a different gap: provable
yet unproven). **None exists**, and this direction is not merely empirically robust — it is *forced* by
the **ergodic-optimization meta-theorem** (`MINPROP_COBOUNDARY_LP.md`, `MINPROP_COUPLING.md`):

> `β = max_{μ∈M_sys} ∫(θ−ϕ)dμ = +1/2 > 0`, attained at `δ₁`.

`β > 0` is *exactly* the statement that the kernel observable is **non-constant on M_sys** (its max,
at `δ₁`, exceeds its Haar value). Every cataloged hard target reduces to this observable: even-density
(K1, `δ₁→0` vs Haar `1/2`), mean `D` (K1, `δ₁→1` vs `2`), `Inj_a`/`M₂ᵒᵈᵈ` (K3), measure entropy (K4)
— each takes its bad value at `δ₁` and its target value at Haar. The **specification** meta-theorem then
certifies the converse for the *proof side*: any observable that varies on M_sys has seed-8 sitting in
the full-dimension non-generic set, so no universal/structural argument fixes its value ⇒ HARD. So
**"HARD ⟺ varies on M_sys" is the meta-theorem content**, and it stands.

### 3.3 Direction 3 — fits NEITHER tier

- **Certificate-complexity hierarchy** (F7, `LIMIT_THEOREM.md`): star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic
  ⊊ CF ⊊ CS, each a strict [PROVEN] separation. This is a **descriptive/topological** invariant of the
  symbolic orbit, **orthogonal to every invariant measure** — it is neither a Birkhoff average nor does
  it vary over M. It sits in the FREE tier via the topological mechanism (§3.1), confirming FREE ⊋
  {measure-constant}.
- **The reductions / conditional theorems** are not orbit-facts at all but **morphisms** between
  functionals: the 5-link halt⟺even-density⟺meanD⟺equidist chain; the conditional
  "even-defect ≤ contraction · odd-defect" (`ENDOGENOUS_UE_BUILD.md` §7.2); the magnitude-aware Lyapunov
  *conditional* certificate (`MINPROP_COBOUNDARY_LP.md` §5). These are objects of a different category
  (implications), orthogonal to the FREE/HARD object-classification, and the dichotomy should not be
  read as classifying them.

### 3.4 The sharpest single counterexample, sharpened further

C1/"infinitely many even steps" is not merely *not constant on M_sys* — it is **not a measure
functional for ANY M**. `#even → ∞` with **density 0** is fully consistent with empirical measures
converging to `δ₁`. So two orbits can share the empirical-limit `δ₁` yet differ on
"infinitely-many-even" (one eventually all-odd, one sparse-even). Hence the property is **strictly
finer than the empirical measure** (a basin/tail invariant: "not eventually all-odd"). **No statement
of the form "constant on M" — any M of measures — can capture a PROVEN fact of this kind.** This is the
decisive structural reason the FREE half of the dichotomy must be amended to admit a topological/tail
register, not just a measure-constant register.

---

## 4. The sharpest correct formulation

Replace the ambiguous M by an explicit **pair**, and split FREE into its two genuine mechanisms.

**The set.** Let `Ω` = the closure (in `ℤ₂`) of the seed-8 forward orbit, a compact `T`-invariant set.
Let

> **M_feas** = { `T`-invariant probability measures `μ` with `supp μ ⊆ Ω` that violate **no** PROVEN
> constraint on the seed-8 orbit } — the proven topological constraints (orbit unbounded; non-periodic;
> growth slope `log₂(3/2)`; subword complexity `≥1.71ℓ`) plus the universal first-moment valuation-budget
> identity.

By **specification**, M_feas *still* contains non-Haar measures (full Hausdorff dimension), so it is a
genuine, non-trivial set strictly between `{Haar}` and M_sys. The conjecture is the **collapse**:

> **(K) ⟺ M_orb = {Haar}** (the seed-8 orbit is generic for Haar). Equivalently, the open content is
> *"is M_feas effectively `{Haar}` along the seed?"* — single-orbit equidistribution = Mahler 3/2 / AEV.

**The amended dichotomy.** A property `P` of the seed-8 orbit is

- **FREE (unconditionally provable) ⟺** `P` is determined by **`Ω` together with the universal
  identities** — i.e. `P` is either (a) a **measure functional constant on all of M_sys** (universal:
  F1–F3, F6), or (b) **constant on the annealed / fixed measure** (F4–F5), or (c) a **topological /
  tail invariant of `Ω`** pinned by the proven constraints **without** locating M_orb inside M_feas
  (C1–C4, F7) — including topological entropy `=log2` (FREE/measure-constant; the earlier "=0" was the retracted sign error);
- **(K)-HARD ⟺** `P` is a **measure functional that varies over M_feas**, with `P(Haar)` the target —
  equivalently `P` separates `{Haar}` from the non-Haar members of M_feas, so fixing its value **is**
  the collapse `M_orb = {Haar}` = single-orbit equidistribution = Mahler/AEV.

The clean boundary is therefore **topological-orbit-closure-determined (FREE)** vs
**Haar-vs-M_feas-separating (HARD)** — exactly the *topological-entropy / measure-entropy* split the
corpus already lists (row K4: measure entropy HARD vs `h_top=log2` FREE), now promoted to the global organizing principle.
The original phrasing "constant on M" is **correct only for the measure-functional sub-tier** and only
with **M = M_feas, not the `δ₁`-containing M_sys**; using M_sys as the FREE-side test is the error, while
M_sys remains the correct **HARD-side witness** (where `β=+1/2` and specification live).

---

## 5. Net assessment

- **Survives?** Yes, in the amended form (§4). The *spirit* — "the proven/open boundary is the
  constant-vs-measure-selecting boundary" — is correct and is even PROVEN on the HARD side by the
  ergodic-optimization (`β=+1/2`) and specification meta-theorems.
- **Counterexamples found?** Yes, all on the **FREE half**, all of the **proven-but-not-constant-on-M_sys**
  type: `#even ≥ 0.89 log n`, subword complexity `≥1.71ℓ`, non-periodicity, top-digit equidistribution.
  Each is a **topological/tail** fact, not a measure functional; `#even` is provably *not a measure
  functional for any M*. **No hard-but-constant** counterexample exists (forbidden by `β>0`). Conditional
  theorems / reductions / the certificate hierarchy **fit neither** object-tier (they are morphisms or
  descriptive invariants).
- **Sharpest M and invariant.** `M_feas` = invariant measures on the seed-8 orbit closure `Ω` consistent
  with all proven (topological + first-moment) constraints; `{Haar} ⊊ M_feas ⊊ M_sys`. (K) ⟺ the
  collapse `M_orb = {Haar}`. The invariant that decides FREE-vs-HARD is **"does `P` separate Haar from
  the rest of M_feas?"** — FREE iff no (topologically pinned or universally constant), HARD iff yes
  (selecting Haar = single-orbit equidistribution = Mahler 3/2 / AEV Conj 1.6 at `α=8`).

---

## Sources

- `MINPROP_COUPLING.md` (specification full-dimension; `freq(D≥2)` ranges `[0,1]`; `δ₁`, `δ_{3/5}`, Haar).
- `MINPROP_COBOUNDARY_LP.md` (ergodic-optimization `β=+1/2` at `δ₁`; coboundary LP infeasible all `k`).
- `EVEN_DENSITY_PARTIAL.md` (`#even ≥ 0.89 log n`; growth `(3/2)ⁿ`; even-density→0 marginally consistent).
- `WEAPONS_AUDIT_2026-06-29.md` §1–2 (the funnel; banked weapons; non-periodicity C3; subword `1.71ℓ`;
  certificate hierarchy; top-digit; FLP; Zudilin; Rajchman/annealed).
- `ANNEALED_PARTIAL_BANKED.md` (all annealed/a.e. partials with exact gap-to-H₂ column).
- `SESSION_2026-06-29_AEV_CORE.md` §3–4 (obstruction map; (K) equivalent forms; α=8 irreducible).
- `ENDOGENOUS_UE_BUILD.md` (`L_ann χ_odd ≡ 0`; odd-block feedback; conditional even≤contraction·odd).
- `WALLB_NONATOMIC.md` (non-periodicity / grows past all cycles).
- Numerics: `scratchpad/rt.py` (seed-8 even-density 0.50159, `#even` 50159 at N=10⁵; fixed point `c=1`
  zero even steps — confirms C1 not constant on M_sys), interpreter
  `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`.

No machine decided. No label upgraded.
