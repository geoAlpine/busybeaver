# The Nested-Collatz CONDITIONAL THEOREM — Axis-2 analog of the single-orbit reductions (2026-06-29)

*Formalizes the nested-Collatz halt predicate and halting direction as a clean **conditional theorem**, the
Axis-2 counterpart to the in-scope single-orbit AEV reductions ({Antihydra, o10-inner, o18, o15}). The halt is
reduced to a **Borel–Cantelli statement over the outer refill orbit**; the conditional theorem states the
exact analytic input that turns that BC statement into a halting **direction**, and isolates which side
(convergent) is provable-ish vs which (divergent) hits the o10 single-orbit wall.*

**Soundness paramount. NO machine is decided. NO halting direction is claimed.** Labels: `[PROVEN]`
(elementary / unit-tested / exact-bigint machine-checked vs raw TM) / `[VERIFIED]` (machine-checked this
program, bb_sim-faithful) / `[CONDITIONAL]` (theorem holds *modulo* a named analytic hypothesis) /
`[HEURISTIC]` (ensemble model, NOT a proof) / `[OPEN]`. None upgraded. All numerics this session use
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (exact big-ints) on a bb_sim.py-faithful simulator;
script `scratchpad/nct_verify.py`.

Sources: `NESTED_COLLATZ_STRUCTURE.md`, `NESTED_DIRECTION.md`, `O10_REDUCTION.md`, `O10_HALTER.md`,
`EXISTENCE_META_THEOREM.md`, `REDUCE_O11_O16.md`, `REDUCE_O2_O7_O8.md`, `BB6_STRUCTURAL_LIMIT_THEOREM.md`.

---

## 0. Headline

> **(NESTED-COLLATZ HALT THEOREM, exact reduction) `[PROVEN structural; PROVEN-instance o10]`.**
> A nested-Collatz machine `M` (clean inner expanding map `T_μ`, outer refill orbit `{B_e}` doubly-exp,
> per-epoch halt-set `H_e`) satisfies
>
> > **`M` halts ⟺ ∃ epoch `e` : the reseeded inner orbit `O_e` (started at `B_e`) hits `H_e`.**
> > Equivalently `M` runs forever ⟺ the reseeded family `{O_e}_{e≥0}` **avoids `H` for every epoch**.
>
> This is a **hitting/avoidance (existence, Π⁰₁-avoidance) event over the outer orbit**, *not* a single
> inner-orbit equidistribution. Writing `p_e :=` (measure of) the per-epoch halt target, the **direction**
> is a **Borel–Cantelli dichotomy on `Σ_e p_e`**.

> **(NESTED-COLLATZ DIRECTION THEOREM, conditional) `[CONDITIONAL]`.**
> **IF** each reseeded inner orbit `O_e` is **effectively equidistributed** for the halt-phase, with a
> discrepancy rate beating the per-epoch target `p_e` *uniformly enough across the doubly-exp reseed family*,
> **THEN** the halt direction is read off `Σ_e p_e`:
> - **convergent** `Σ_e p_e < ∞` ⟹ **non-halt** (Borel–Cantelli **I**, *no independence needed*) — the
>   provable-ish side, the Axis-2 analog of o18's BC-I existence reduction;
> - **divergent** `Σ_e p_e = ∞` ⟹ **halt** — but this requires **Borel–Cantelli II**, whose independence /
>   quasi-independence hypothesis a **single deterministic reseed family cannot supply** = the **o10 wall**
>   (`O10_HALTER.md` `[PROVEN negative]`). The divergent side is therefore **not** delivered by
>   equidistribution alone.

---

## 1. The exact reduction — halt ⟺ Borel–Cantelli over the outer orbit  [PROVEN structural]

### 1.1 Objects (from `NESTED_COLLATZ_STRUCTURE.md` Def.)

A nested-Collatz `M` carries:
- an **inner clean expanding map** `T_μ`, `μ = 2^a/3^b`, `v_p(μ) = −1` (all nine: `μ = 3/2`, `p = 2`), acting
  on an integer "mass" `m` along the admissible (even/parity-safe) head-pass subsequence;
- an **outer refill orbit** `{B_e}_{e≥0}`, `B_0` the blank-tape seed, `B_{e+1} = R(`terminal config of epoch
  `e`)`, where `R` is the TM-derived (piecewise-affine within residue classes) refill map; an epoch with seed
  `k` runs `≈ k/Δ` inner `×μ` steps, so `B_{e+1} ≈ μ^{k/Δ}` ⟹ **`{B_e}` is doubly-exponential and not
  eventually periodic**;
- a **per-epoch halt-set** `H_e ⊆` (inner phase space), the local-collision condition for epoch `e` (o10:
  "countdown lands `b=0` at odd `m`"; o18-type: a carry-alignment clopen cylinder; `00`-gap / phase-race
  machines: a defect cylinder).

`O_e` denotes the inner `T_μ`-orbit reseeded at `B_e`. By Definition clause 3 the halt mechanic is
**structurally absent from every inner epoch** (`[VERIFIED]` §3 below: the halt-precursor state is visited
~1500–2300×/2M steps and the halt symbol is **never** the read cell within an epoch), so the only halt sites
are the per-epoch boundary events `O_e ∩ H_e`.

### 1.2 The reduction

> **(REDUCTION) `[PROVEN structural; PROVEN-instance o10 — O10_REDUCTION.md (FULL)]`.**
> `M` halts ⟺ `∃ e : O_e ∩ H_e ≠ ∅`. Non-halt ⟺ `∀e : O_e ∩ H_e = ∅` (tail-avoidance after a finite
> verified prefix), a `Π⁰₁` statement over the deterministic family `{B_e}`.

For **o10** this is the literal `[PROVEN]` criterion: `H_e =` "b-countdown reaches exactly `b=0` at odd `m`",
inner eat-length `L = 2m−8` is **always even** so `O_e` provably never halts mid-epoch
(`O10_REDUCTION.md` (INNER), re-`[VERIFIED]` §3.4 below). For the other eight the halt **mechanic** is
`[PROVEN, unit-tested]` and the inner-never-triggers fact is `[VERIFIED]`; the closed-form `R` / `H_e` is
`[OPEN]`, so the reduction is `[CONDITIONAL]` on the verified structural model.

### 1.3 The Borel–Cantelli framing

Model the inner phase at the (forced) underflow/boundary index of epoch `e` as a draw, and set
`p_e := P(O_e ∩ H_e ≠ ∅)` — the **per-epoch halt probability**, i.e. the Haar measure of the halt target seen
by epoch `e`. Then "M halts" is `limsup_e {epoch e hits H_e}`, and the direction is governed by `Σ_e p_e`:

| | **convergent** `Σ p_e < ∞` | **divergent** `Σ p_e = ∞` |
|---|---|---|
| per-epoch target | `p_e → 0` (thin / shrinking) | `p_e ≈ const > 0` (fixed-measure) |
| heuristic direction | **non-halt** | **halt** |
| BC side | **BC-I** (convergence; **no independence**) | **BC-II** (divergence; **needs independence**) |
| rigor | a.e.-finite hits, *clean annealed* (cf. `EXISTENCE_META_THEOREM.md` §3a, o18) | a.s.-∞ hits **only** for (quasi-)independent events; a single orbit lacks it (`O10_HALTER.md`) |
| exemplar | o18 (carry-align, density-0 summable target); o2/o7/o8/o11/o12/o14/o16 | **o10** (`p_e ≈ 1/3` constant, `[VERIFIED]` non-decay §3.3) |

> **`p_e` is heuristic for the deterministic orbit.** For the actual seed `B_0`, each `1{O_e ∩ H_e ≠ ∅}` is
> already `∈{0,1}` (fixed by the parity/carry of `O_e`); `p_e` is the *ensemble* (annealed) measure. The
> conditional theorem (§2) is exactly what is needed to transfer the annealed `Σ p_e` verdict to the single
> deterministic family — and it transfers cleanly only on the convergent side.

---

## 2. The CONDITIONAL theorem — the exact analytic input  [CONDITIONAL]

### 2.1 The hypothesis

> **(EFF-EQ, effective reseeded equidistribution).** There is a discrepancy bound `D_N(B)` for the inner map
> `T_μ` started at seed `B`, such that for the reseed family `{B_e}` the empirical count of halt-phase hits
> through epoch `N` satisfies
>
> > `#{e ≤ N : O_e ∩ H_e ≠ ∅} = Σ_{e≤N} p_e + O( E_N )`,  with `E_N` controlled by `D_N(B_e)`,
>
> i.e. the realized hit-count tracks the expected `Σ p_e` up to an error that does **not overwhelm the
> target**. This is the **single-orbit equidistribution of `⌊μ^n x⌋ mod p`** (Axis-1 object) *plus*
> **uniformity across the doubly-exp reseed family**.

This is the *same* analytic kernel as the in-scope reductions (AEV Conj 1.6, `v_p(μ)=−1` floor/ceiling-mirror
fragment), with one extra demand: **effectiveness / a rate**, and **uniformity over reseeds**.

### 2.2 The two halves

> **(NESTED-COLLATZ DIRECTION THEOREM) `[CONDITIONAL on EFF-EQ]`.**
>
> **(a) Convergent half — provable-ish.** If `Σ_e p_e < ∞` and `EFF-EQ` holds with a rate beating the
> *summable* target (BC-I strength: `E_N = o(1)` past the tail where `Σ_{e>N} p_e < 1`), then the reseeded
> family hits `H` only finitely often; with a finite verified prefix, **`M` does not halt**. **No independence
> is needed** — this is Borel–Cantelli **I** (`Σ P < ∞ ⟹ Haar(limsup)=0`), exactly the
> `EXISTENCE_META_THEOREM.md` §3a / o18 mechanism, transported to the reseed family. The required input is a
> rate beating a summable target — **strictly weaker** than a positive liminf density.
>
> **(b) Divergent half — the o10 wall.** If `Σ_e p_e = ∞` (fixed-measure per-epoch target), the *annealed*
> conclusion is "halts a.s.", but the rigorous conclusion **needs Borel–Cantelli II**, which requires
> **independence** (or Kochen–Stone quasi-independence: a second-moment `Σ_{i,j} (P(B_i∩B_j) − p_i p_j)`
> bound). The reseed events are **deterministic functions of one fixed family** `{B_e}` — there is no
> probability space and nothing to be independent of (`O10_HALTER.md` `[PROVEN negative]`). So **EFF-EQ alone
> does NOT determine the divergent direction**; one additionally needs a **quenched divergent BC** (an
> effective quasi-independence / equidistribution-of-pairs statement across the doubly-exp reseeds), which is
> **unavailable** and is precisely the o10 open kernel.

### 2.3 Exact analytic input, summarized

- **Convergent direction (non-halt):** EFF-EQ with **BC-I strength** — a single-orbit equidistribution rate
  beating a *summable* per-epoch target, uniform across the reseed family. `[CONDITIONAL]`, *and* this is the
  weaker ask (matches o18's in-scope convergent reduction; the annealed half is already `[PROVEN]` via BC-I,
  the gap is annealed→quenched, `EXISTENCE_META_THEOREM.md` §3a).
- **Divergent direction (halt):** EFF-EQ with **BC-II strength** — additionally a quenched quasi-independence
  / pair-correlation bound across the doubly-exp reseeds. `[OPEN]`; structurally unavailable for a single
  deterministic family (the o10 wall). This is **strictly harder** than any in-scope (single-orbit) object.

> **Slogan.** Convergent nested-Collatz = the **o18 (BC-I, existence) reduction lifted to a reseed family** —
> conditional on an effective rate, *provable-ish, non-halt*. Divergent nested-Collatz = an object with **no
> Axis-1 analog**: it needs the divergence side of BC, which a single deterministic orbit cannot feed = the
> o10 wall, *halt-leaning, open*.

---

## 3. Application to the nine machines  [classification + conditional directions]

### 3.1 Convergent-vs-divergent classification

| machine | halt-target type | BC side | `Σ p_e` | conditional direction | status |
|---|---|---|---|---|---|
| **o10** | b-countdown lands `b=0` at odd `m` — **fixed-measure** (`p_e≈1/3`, non-decay `[VERIFIED]`) | **divergent** | `=∞` | **HALT**-leaning | `[HEURISTIC]`; BC-II inapplicable ⟹ `[OPEN]` |
| **o13** | even-run at an outer collapse — **scaling UNEXTRACTED** | **unknown** | ? | **UNCLEAR** | `[OPEN]` (could be divergent like o10) |
| **o2** | `00`-gap right of D→F frontier — **thin** | convergent-lean | `<∞`? | **non-halt**-leaning | `[OPEN]` (`(10)*`-sea, no scalar outer map) |
| **o7** | left counter empties (`00`-left) — **thin** (a≥2 always) | convergent-lean | `<∞`? | **non-halt**-leaning | `[OPEN]` |
| **o8** | left counter empties (`00`-left) — **thin** (a≥2 always) | convergent-lean | `<∞`? | **non-halt**-leaning | `[OPEN]` |
| **o11** | `00`-gap forms at refill — **thin** (neighbor=1 in 2330/2330) | convergent-lean | `<∞`? | **non-halt**-leaning | `[OPEN]` |
| **o12** | `00`-gap forms at refill — **thin** (neighbor=1 in 3516/3516) | convergent-lean | `<∞`? | **non-halt**-leaning | `[OPEN]` |
| **o14** | `00`-gap forms at refill — **thin** (neighbor=1 in 1996/1996) | convergent-lean | `<∞`? | **non-halt**-leaning | `[OPEN]` (marker-accreting outer) |
| **o16** | F-phase `0` beats E-phase exit — **thin** (exit wins 22/22) | convergent-lean | `<∞`? | **non-halt**-leaning | `[OPEN]` (phase race) |

### 3.2 The direction-structure map (honest caveats)

- **Divergent ⟹ HALT-leaning: o10 only.** It is the *only* nested machine with (i) an extracted clean
  outer-epoch model and (ii) a halt target of constant non-decaying per-epoch measure (the **forced**
  b-underflow, whose `m`-parity is a fair coin). `Σ p_e = ∞`. **But** the divergent half needs BC-II, which a
  single deterministic orbit cannot supply (`O10_HALTER.md`), so o10 is HALT-*leaning* `[HEURISTIC]`, decision
  `[OPEN]`. Exact-simulation decides **epochs 1–2 only (both non-halt)**; epoch 3 (`B_3 = 210273201`, terminal
  `m` ≈ 24.7-million digits) is infeasible (§3.3).
- **Convergent ⟹ NON-HALT-leaning: o2, o7, o8, o11, o12, o14, o16.** All have a **spontaneous-defect** halt
  target (`00`-gap / phase misalignment) that must *appear* in a field structurally containing only isolated
  0s — the target gets *rarer* with growth ⟹ `p_e → 0`, convergent-leaning. Their per-epoch scaling is **not
  extracted** (no clean scalar outer map), so the convergent classification is `[HEURISTIC]` and the direction
  `[OPEN]`. Even granting convergence, the rigorous non-halt still needs EFF-EQ (BC-I rate) which is
  unproven — same status as the in-scope o18 (annealed `[PROVEN]`, quenched `[OPEN]`).
- **UNCLEAR: o13.** Structural twin of o10 (mirror eat-sweep, parity-safe inner — inner runs always ODD,
  7214/7214) but its halt target's per-collapse measure is **un-extracted** (sea-/δ-coupled outer, not
  separable). It could be divergent (halt-leaning like o10) or convergent (non-halt-leaning). **Genuinely
  `[OPEN]`** — the often-quoted "o13 ~0" is only the *inner* safe-rate (which o10 *also* has: 0 inner halts),
  **not** o13's outer halt-prob; the comparison "o10 ~1/3 vs o13 ~0" is confounded (`NESTED_DIRECTION.md` §2).

> **The inner ×3/2 all-odd/all-even fact is shared by the whole class and is ORTHOGONAL to direction.**
> Every nested machine has a parity-safe inner (its eat/run never matches the halt target). Direction lives
> entirely on the **outer** refill orbit's per-epoch halt-target measure — the convergent-vs-divergent BC
> question.

---

## 4. Is the "no structure-only proof" barrier inherited?  [PROVEN, two-part]

The halt object is an **existence/avoidance** event (∃ epoch hits `H`) over the reseed family — the
**existence facet** of `EXISTENCE_META_THEOREM.md`, not the density facet. So the barrier analysis there
transfers, with a sharp two-part answer.

### 4.1 A halting reseed EXISTS (the analog of the halting fixed point)  `[PROVEN]`

For o10 the per-epoch halt set is reached by concrete configs: **every config `1 0^{2m−8} 0 1` with `m` ODD,
`b=0` HALTS** (`O10_REDUCTION.md` §5, `[VERIFIED]` raw TM `m=5,7,9,11,21,101`). The inner ceiling fixed point
is `m = ⌈3m/2⌉ ⟹ m = −1 ∈ ℤ₂` (all-odd orbit), the 2-adic mirror of Antihydra's `o=+1`. So a **halting
reseed** exists — the Axis-2 analog of the halting fixed point / the `E-hitting` witness.

### 4.2 But its existence does NOT force a structure-only impossibility  `[PROVEN negative]`

By `EXISTENCE_META_THEOREM.md` §2b (`[PROVEN negative]`): a forward-invariant **set** `L ⊇ orbit(x_0)` with
`L ∩ H = ∅` need **not** contain the halting orbit — a set can simply *exclude* the halting reseed. The
density barrier was a *theorem* only because ergodic optimization is a `max over invariant measures` that
**must** include the atom `δ` at the halting orbit (forcing `β>0`); an invariant **set** has no such
obligation. Therefore:

> **(BARRIER INHERITANCE) `[PROVEN]`.** The existence of a halting reseed does **NOT** give nested-Collatz a
> clean *proven* "no structure-only proof" barrier of the density (`β>0`) type. The nested-Collatz barrier is
> the **`[OPEN]` over-approximation / descriptive-complexity** barrier: does a *tame* (REG / SLIN / automatic)
> forward-invariant `L` separating the reseed family from `H` exist? This is **harder** than the single-orbit
> existence case — `L` must separate a **doubly-exponentially-indexed family of restarting orbits** from `H`
> — and **empirically blocked**: all nine are FAR/CEGAR HOLDOUT (`REDUCE_O11_O16.md` §0). So the barrier is
> inherited as the *open over-approximation axis*, with empirical (not proven) strength.

### 4.3 The one inherited PROVEN sub-barrier (inner density factor)  `[PROVEN]`

The **inner** sub-factor *does* inherit the density `β`-barrier: the inner ceiling-`3/2` kernel attains
`β = +1/2 > 0` at the atom `δ_{m=−1}` (odd-density →1), so **no structure-only argument forces the inner
parity bound** (`O10_REDUCTION.md` §5, transferred from Antihydra). Hence the full picture:

> **Net (two-part).** Nested-Collatz **inherits the PROVEN density `β`-barrier on its inner parity-at-underflow
> sub-factor**, but its **full** halt is the outer existence event, whose no-structure-only barrier is the
> **`[OPEN]` over-approximation axis** (the halting reseed exists but does not block an avoidance set — exactly
> like `E-hitting`). So the full machine does **not** get a clean proven barrier; it gets (inner) PROVEN +
> (outer) OPEN, plus the empirical FAR/CEGAR HOLDOUT. This is the precise Axis-2 mirror of the
> `EXISTENCE_META_THEOREM.md` density⊕existence split.

---

## 5. Numerical verification (this session, bb_sim-faithful, exact big-ints)  `[VERIFIED]`

Script `scratchpad/nct_verify.py`, run under `.venv/bin/python`.

**(1) o10 abstract epoch model vs raw TM — `[VERIFIED]` 0 mismatch.** Abstract `epoch(B)` (inner
`m→⌈3m/2⌉`, `b→b−(1+[m odd])`, halt ⟺ lands `b=0` at odd `m`) vs raw bb_sim run from clean config
`1 0^{2m−8} 1^b 0 1`. For `B=1..15`: **every predicted HALT confirmed by the raw TM** (B=1,4,11,13 all
HALT); predicted REFILLs do not halt within the 1.3M-step raw budget (raw refill-detection times out for most
B — a budget limit, not a mismatch; the authoritative `o10_crosscheck.py` confirms refill `B_next` with 0
mismatch over B=1..16). **Verdict mismatches = 0.**

**(2) Deterministic refill orbit (actual seed `B_1=5`) — `[VERIFIED]`.**
`5 → 57 → 210273201 → …` (epochs 1–2 inner-steps 3, 40, both REFILL/non-halt; `5→57` reproduces the real
machine's epoch-1→2 refill). Epoch 3 (`B_3≈2.1×10⁸`, terminal `m` ≈ 24.7-million digits) is **INFEASIBLE** —
the refill orbit is doubly-exponential, unreachable by simulation. Consistent with the ≥40M-step holdout.

**(3) Divergent-BC signature: per-epoch halt fraction NON-DECAYING across disjoint B-windows — `[VERIFIED]`.**

| window | halt fraction |
|---|---|
| `[1,500)` | 0.3166 |
| `[500,1000)` | 0.3400 |
| `[1000,2000)` | 0.3390 |
| `[2000,3000)` | 0.3430 |
| `[3000,5000)` | 0.3310 |
| `[1,3000)` | **0.33678** |

The fraction is **flat (does not decay) across disjoint outer-index windows** = the divergent-BC signature
(`Σ p_e = ∞`). The overall `0.33678` **reproduces `O10_HALTER.md`'s bb_sim-cross-checked 33.67%** — this
session's implementation resolves the earlier `~1/6` reimpl discrepancy noted in `NESTED_DIRECTION.md` §3.

**(4) Inner eat-length always EVEN — `[VERIFIED]`.** `L=2m−8` over the inner orbit `m→⌈3m/2⌉` from `m=6`:
`4,10,20,34,56,88,136,208,316,478,722,1088,1636,2458` — **zero odd** ⟹ by (HALT-MECHANIC) the inner orbit
**never halts** (halt only at the outer underflow).

**(5) Halt couples to OUTER not inner — `[VERIFIED]`.** o10 from blank, 2M steps: halt-precursor state **F
entered 1614×, read-symbol distribution `{0:0, 1:1614}`** — it **always** reads `1`, the halt symbol `0` is
**never** read ⟹ halt fires `False`. The halt-determining cell is never the halt symbol within an epoch:
operational confirmation of the outer-coupling (Reduction §1.1).

**(6) Convergent machine o11 (thin target) — `[VERIFIED]`.** Inner sea map `m'=⌊3m/2⌋+4` holds **12/12**
consecutive. From blank, 5M steps: halt-precursor state **C entered 2330×, read distribution `{0:0,
1:2330}`** — the halt symbol `0` (the lethal `00`-gap) is **never** read; the thin target never spontaneously
opens ⟹ convergent-leaning, non-halt. Does not halt.

---

## 6. Soundness ledger

- **(REDUCTION)** halt ⟺ ∃ epoch hits `H_e`: `[PROVEN structural]`, `[PROVEN-instance]` for o10
  (`O10_REDUCTION.md` (FULL)), `[CONDITIONAL]`/`[VERIFIED]` for the other 8 (mechanic proven, inner-never
  verified, closed-form `R`/`H_e` `[OPEN]`).
- **(DIRECTION THEOREM)** `[CONDITIONAL on EFF-EQ]`: convergent half = BC-I, no independence, the weaker ask
  (provable-ish, non-halt); divergent half = BC-II, needs quenched quasi-independence a single deterministic
  reseed family lacks = **o10 wall** `[OPEN]`. The analytic input is an **effective single-orbit
  equidistribution rate uniform across the doubly-exp reseeds**, beating a summable target (convergent) or
  with pair-correlation control (divergent).
- **Classification:** divergent⟹halt-leaning = **o10** (`[HEURISTIC]`, `[OPEN]`); convergent⟹non-halt-leaning
  = **o2,o7,o8,o11,o12,o14,o16** (`[HEURISTIC]`, `[OPEN]`); **o13 UNCLEAR/`[OPEN]`**. Inner parity orthogonal
  to direction.
- **Barrier inheritance** `[PROVEN, two-part]`: inner density sub-factor inherits the **PROVEN `β=+1/2`
  barrier**; the full outer existence event sits on the **`[OPEN]` over-approximation axis** (halting reseed
  exists but does not block an avoidance set), empirically FAR/CEGAR HOLDOUT. No clean proven full barrier.
- **Numerics:** `[VERIFIED]`, exact big-int, bb_sim-faithful — 0 abstract/raw mismatch (halt side), 33.678%
  non-decaying halt fraction, inner all-even, precursor never reads halt symbol (o10 & o11).
- **NO machine decided; NO non-halting asserted; NO direction claimed.** Scope set
  {Antihydra, o10-inner, o18, o15} unchanged. This note is the Axis-2 conditional theorem, parallel to the
  Axis-1 single-orbit reductions.
