# The BB(6) Expanding-Kernel Collatz Core: Exact Reductions, an Ergodic-Optimization Barrier, and Placement under the Andrieu–Eliahou–Vivion Normality Conjecture

*A self-contained mathematical note. Draft for arXiv submission (math.DS / math.NT / cs.CC).*

**Author.** (PI, ORCID 0009-0002-3791-2372).

**Soundness discipline (paramount, governs the whole note).** Every mathematical assertion carries an
explicit label, copied without upgrade from the program's source documents:
- **[PROVEN]** — a conjecture-free proof is given **in full inline**, or is elementary;
- **[PROVEN, cites X]** — proven **given** a stated external theorem X used as an input (the proof of X is not
  reproduced);
- **[VERIFIED]** — machine-checked this program by exact (big-integer / exact-`Fraction`) computation,
  cross-checked against the `bb_sim` Turing-machine semantics, but **not** promoted to a theorem unless a
  separate argument is given;
- **[CONDITIONAL on Y]** — true modulo a stated open hypothesis Y;
- **[OPEN]** — a named, recognized open problem.

No machine is decided in this note. No non-halting is asserted unconditionally. Where the source program
recorded a "[PROVEN]" that in fact rested on a sketch or on numerics, this note either supplies the full proof
inline or downgrades the claim and states its dependency. Numerical reproductions below were re-run with the
`/Users/aokiyousuke/quantum-ecc/.venv` exact big-integer interpreter against `bb_sim` semantics.

---

## Abstract

Let `BB(6)` denote the sixth busy-beaver number. Its determination is obstructed by a small set of 6-state
2-symbol Turing machines — the **cryptids** — whose halting is equivalent to recognized open problems in
arithmetic dynamics. We isolate the **expanding-kernel Collatz core**: machines whose blank-tape evolution is
governed by a Mahler multiplier `μ = 2^a/3^b` whose lowest-terms denominator is a single prime `p` (i.e.
`v_p(μ) = −1`), giving the shared kernel map `T_μ(x) = ⌊μx⌋` on the `p`-adic integers `ℤ_p`.

We prove three theorems and a placement result, all conjecture-free except where explicitly marked.

- **Theorem 1 (exact reductions).** For the in-scope set
  **{Antihydra, o10-inner, o18, o15}** the raw Turing machine's halting is reduced to an explicit `2^a/3^b`
  arithmetic event: Antihydra halts iff an even-density Cesàro average drops below `1/3` (`q=2`, density
  facet); o18/o15 halt iff a base-3 carry collision ever occurs (`q=3`, existence facet); o10-inner runs the
  literal ceiling `⌈3m/2⌉`. **For Antihydra the reduction is now [PROVEN] outright:** the raw-TM → counter
  macro-structure (`c ↦ ⌊3c/2⌋`, the balance counter, and the halt criterion) is a full conjecture-free
  hand-proof from the transition table — three induction-proven shift lemmas, the inner ×3/2 lemma, the
  even/odd carry lemmas, the macro-step `c' = ⌊3c/2⌋`, and the halt criterion (TM-extraction note §1) — and
  the downstream arithmetic was already inline. For **o18/o15/o10-inner** the reduction is **[PROVEN] modulo a
  [VERIFIED] macro-structure** (their halt criteria are table-trivially [PROVEN]). For o18 the honest content is
  sharper: the elementary sweep lemmas and the **conditional clean-epoch lemma** are [PROVEN], the macro-coordinate
  `⌊8k/3⌋+2` is [VERIFIED] only on the carry-absorbed epochs (0–6), and the **unconditional** width map
  `M(k) → M(⌊8k/3⌋+2)` is **[DISPROVEN]** (it breaks at the deep base-3 carry `k=3890≡2 mod 3`, epoch 7); the
  carry-finiteness `(K_o18)` that would restore it is [OPEN] = the AEV `q=3` facet = the halt event itself. The
  supporting **GAP**, **renewal**, and **valuation** lemmas are proved in full. The AEV/Mahler kernel that
  decides the orbits remains [OPEN].

- **Theorem 2 (induced-map structure, [PROVEN]).** For every `μ = 2^a/3^b` with `v_p(μ) = −1`, `T_μ` is a
  clean `p`-to-1 Haar-measure-preserving endomorphism of `ℤ_p`. Antihydra's induced odd-return map
  `T(o) = 3^{D−1}(3o−1)/2^D`, `D = v₂(3o−1)`, is Haar-preserving with gap symbols `D_j` i.i.d. geometric
  `P(D = d) = 2^{−d}` (mean `2`); exactness/Bernoullicity follow from the full-branch structure (cites
  standard 2-adic Collatz theory).

- **Theorem 3 (density ergodic-optimization barrier for Antihydra, [PROVEN, cites ergodic optimization]).**
  The ergodic-optimization value of Antihydra's one-sided test function is `β = +1/2 > 0`, **attained at the
  genuinely halting fixed point `o = 1`**. Hence no all-orbits / structure-only one-sided inequality can
  prove non-halting: the halting/non-halting distinction is irreducibly single-orbit. The pointwise bound
  `ψ ≤ 1/2` (proved in full via the **`ψ = f(D)` lemma**) makes `β = +1/2` exact; the dual LP infeasibility
  for `k = 3..12` is [VERIFIED].

- **Placement ([PROVEN] bridge / [OPEN] kernel).** The residual single line is the `p/q = 3/2`,
  single-orbit, single-level (`k=2`), one-sided, **floor-mirror** fragment of the Andrieu–Eliahou–Vivion
  (2025) normality conjecture (its `q=2` Mahler density facet; the `q=3` Erdős existence facet for `8/3`). We
  prove **in full** the negation conjugacy `T_c = R∘T_f∘R` that identifies the floor-mirror conjecture with
  literal AEV 1.6(3/2) up to a cosmetic seed-sign quantifier, closing the floor-vs-ceiling gap.

The contribution is the **characterization and the barrier**, not a decision: per-cryptid completion is
[CONDITIONAL] on the AEV/Mahler kernel, for which no analytic handle is known. A **Blocking Theorem**
([PROVEN] structural) explains why the in-scope set is exactly four: the remaining `μ=3/2` machines carry a
nested doubly-exponential refill layer that lifts them off the single-orbit reduction.

---

## 1. Introduction

### 1.1 BB(6) and the cryptids

The busy-beaver function `BB(n)` is the maximum number of steps a halting `n`-state 2-symbol Turing machine
makes on the blank tape. `BB(5) = 47{,}176{,}870` is known (machine-verified, reproduced by this program).
`BB(6)` is not: the bbchallenge frontier contains a small set of 6-state machines — the **cryptids** — that no
finite-state decider settles and whose halting is equivalent to open arithmetic-dynamics problems. The
program reverse-engineered all 19 BB(6) cryptids against their raw transition tables (Section 8); each carries
**irregular geometric `2^a/3^b`-rate (Mahler/Collatz) content**, presented in one of two cosmetic width
envelopes. There is no tractable subclass.

### 1.2 The expanding-kernel Collatz core

This note treats the structurally cleanest stratum: the **expanding-kernel** machines, defined by a Mahler
multiplier whose denominator is a single prime.

> **Definition 1 (expanding-kernel class).** Let `μ = 2^a/3^b` in lowest terms with denominator a single
> prime `p` (equivalently `v_p(μ) = −1`). The shared kernel object is
> `T_μ(x) = ⌊μx⌋` on `ℤ_p`.

The **in-scope set** — those whose *entire* halting reduces to a single arithmetic event of one `T_μ`-orbit —
is exactly

> **{Antihydra (`μ=3/2`, `p=2`), o10-inner (`μ=3/2`, `p=2`), o18 (`μ=8/3`, `p=3`), o15 (`μ=8/3`, `p=3`)}.**

Two facets occur. Antihydra's halt is a **density** event (a Cesàro average underflow, `q=2`). o18/o15's halt
is an **existence** event (a carry collision is ever realized, `q=3`/Erdős). o10-inner runs the literal
ceiling map and is [CONDITIONAL] (its full machine o10-FULL is composite and out of scope, Section 8).

Scope is enforced throughout: the family-wide [PROVEN] fact is the **kernel structure** (Theorem 2). The
**barrier** (Theorem 3) is [PROVEN] for **Antihydra only**; o10-inner is [CONDITIONAL]; o18/o15 do **not**
receive it (different facet). The remaining `μ=3/2` machines (o2, o7, o8, o11–o14, o16) are *in-family by
multiplier but not in-scope by proof* — Section 7 proves why (the Blocking Theorem).

### 1.3 The result, in one sentence

> The BB(6) expanding-kernel Collatz core reduces, by exact reductions whose macro-structure is
> machine-verified and whose arithmetic is proved in full, to a named single-orbit fragment of the
> Andrieu–Eliahou–Vivion / Mahler equidistribution conjecture; Antihydra additionally carries a fully proven
> ergodic-optimization barrier (`β = +1/2 > 0`, attained at a genuine halting orbit) showing that no
> structure-only proof of its non-halting can exist.

What this note does **not** claim: it decides no machine, offers no shortcut to any cryptid, and asserts no
non-halting. The single honest [OPEN] kernel is named; per-cryptid completion is [CONDITIONAL] on it with no
known shortcut.

---

## 2. The expanding-kernel class `T_μ`

> **Proposition 2.1 (clean `p`-to-1 endomorphism, [PROVEN]).** Let `μ = 2^a/3^b` in lowest terms with
> single-prime denominator `p`, `v_p(μ) = −1`. Then `T_μ(x) = ⌊μx⌋` is a well-defined, clean `p`-to-1,
> Haar-measure-preserving endomorphism of `ℤ_p`, and its induced (first-return / renewal) map is full-branch
> piecewise-affine expanding with a `ℤ_p` fixed point on every branch.

*Proof of the measure-preservation skeleton.* Write `μ = M/p` with `gcd(M,p)=1`, `M = 2^a` (if `p=3`) or
`M = 3^{−b}·2^a`-type numerator (if `p=2`); in all in-scope cases the numerator is a `p`-adic unit. For
`x ∈ ℤ_p` write `x = py + r`, `r ∈ {0,…,p−1}`. Then `⌊μx⌋ = ⌊(M/p)(py+r)⌋ = My + ⌊Mr/p⌋`. As `r` ranges over
a fixed residue class the map `y ↦ My + ⌊Mr/p⌋` is affine with `p`-adic Jacobian `|M|_p = 1` (since `M` is a
`p`-adic unit), so on each of the `p` residue branches `T_μ` acts as a measure-preserving affine bijection of
`ℤ_p` onto a translate; the `p` branches partition the image with multiplicity 1 (cleanness). Haar
preservation follows by summing the `p` branch pushforwards. ∎

The cleanness dichotomy is sharp and was checked exhaustively.

> **[VERIFIED] (`kernel_classification.py`).** `μ ∈ {3/2, 5/2, 7/2, 27/2}` (`p=2`) and
> `{8/3, 4/3, 16/3, 2/3}` (`p=3`) are all clean `p`-to-1 with a fixed point on every branch (8/8 for each
> prime). The `v_p = −2` controls `{9/4, 16/9, 27/4, 25/4}` are **not** clean (mixed branch multiplicities).
> Hence `v_p(μ) = −1` is *exactly* the clean regime.

Across the entire BB(6) Collatz core the class `{μ : v_p(μ) = −1}` is realized by **exactly four [VERIFIED]
multipliers**: `3/2` and `5/2` (`p=2`); `4/3` and `8/3` (`p=3`). The two non-`3/2`,non-`8/3` members (`5/2`
Space Needle, `4/3` o4/o5) are [VERIFIED] (exact integer reset-difference ratios over ≥4 clean epochs),
**not** [PROVEN], and extend the kernel *class* but not the in-scope *proof* set of Section 3.

---

## 3. Theorem 1 — the exact reductions (raw TM → arithmetic criterion)

> **Theorem 1.** For each in-scope machine `M ∈ {Antihydra, o10-inner, o18, o15}`, the halting of `M` is
> equivalent to an explicit arithmetic event of a `2^a/3^b` orbit, as stated in §3.1–§3.4.

**Honesty note on the reduction (general; Antihydra exception in the next paragraph).** Each reduction has two layers. (i) The **macro-structure
extraction** — that the blank-tape evolution maintains the stated unary counters / blocks and evolves them by
the stated map — is [VERIFIED]: it was obtained by reverse-engineering the raw transition table and confirmed
step-for-step against `bb_sim` to the cited horizons (`bb_sim` is the program's exact-semantics simulator,
independently validated by reproducing `BB(5)=47{,}176{,}870`). It is **not** reproduced here as a
human-checked proof; it is a machine-verified input. (ii) The **arithmetic criterion** given that
macro-structure — the GAP/renewal/valuation chain below — is **proved in full inline**. We therefore label
the reductions **[PROVEN] modulo the [VERIFIED] macro-structure**, faithful to the source's "exact,
machine-verified reduction."

**Exception — Antihydra (§3.1) is now [PROVEN] outright.** For Antihydra the macro-structure-extraction layer
(i) has been upgraded from [VERIFIED] to a full conjecture-free hand-proof: every macro-step is *derived* by a
finite case analysis on the transition table plus an induction over each sweep — three induction-proven shift
lemmas (A→, E→, C←), the inner ×3/2 lemma `I(a,L,R) ⟹ I(a,L−2,R+3)`, the even- and odd-carry lemmas, the
macro-step theorem (`b' = ⌊3b/2⌋+3`, i.e. `c' = ⌊3c/2⌋` under `c = b+6`), and the halt criterion (halt iff an
odd-`c` step occurs at balance `0`) — with `bb_sim` used **only** as confirmation (full derivation in the
companion note, §"Antihydra — FULL hand-proof"). Hence Antihydra's reduction is **[PROVEN]** with no residual
[VERIFIED] dependence (the AEV/Mahler kernel remains [OPEN]). For **o18/o15** only the **halt criterion** is
table-trivially [PROVEN]; for o18 the elementary sweep lemmas and the **conditional clean-epoch lemma** are
additionally [PROVEN], but the **unconditional** base-3 width map `M(k) → M(⌊8k/3⌋+2)` is **[DISPROVEN]** (it is
false beyond epoch 6 — a deep carry breaks the clean form at `k=3890≡2 mod 3`, §3.3), so the width coordinate is
**[VERIFIED] only on the carry-absorbed epochs**, with the carry-finiteness `(K_o18)` [OPEN]; the obstruction is
not "induction not transcribed" but that the unconditional map is not true. **o10-inner**'s ceiling map stays
**[VERIFIED]**/[CONDITIONAL].

### 3.1 Antihydra — density facet, `q=2`

The blank-tape evolution maintains the integer orbit `c₀ = 8`, `c_{n+1} = ⌊3c_n/2⌋`, and a counter equal to
`balance_n := 3E_n − n`, where `E_n = #{i < n : c_i even}` (**[PROVEN] macro-structure**, hand-derived from
the raw transition table in the TM-extraction note §1; shift lemmas + inner ×3/2 lemma + carry lemmas +
macro-step + start config `C(0,2)` ↔ `c = 8`). The machine halts iff this counter underflows.

> **Lemma 3.1 (halting criterion, [PROVEN]).** Given the macro-structure, Antihydra halts
> `⟺ ∃ n : balance_n < 0 ⟺ ∃ n : E_n/n < 1/3`. Equivalently, non-halting `⟺ E_n/n ≥ 1/3` for all `n`. The
> threshold `1/3` is exact: if `liminf E_n/n < 1/3` then `balance_n → −∞` along a subsequence and the counter
> underflows.

*Proof.* `balance_n = 3E_n − n < 0 ⟺ E_n/n < 1/3`; the machine halts exactly at the first underflow, and the
liminf statement is the contrapositive at the subsequence realizing it. ∎

[VERIFIED] this note: `balance_n ≥ 0` to `N₀ = 2·10⁵` with `min balance = +2`; even-density `≈ 0.5002`.

We now pass to the induced odd-return map, where the density `1/3` becomes a mean-gap statement.

> **Lemma 3.2 (GAP LEMMA, [PROVEN] in full).** For odd `o`, set `D := v₂(3o − 1) ≥ 1`. Then the floor
> `3/2`-map reaches its **next odd value after exactly `D` steps**, and that value is
> `T(o) = 3^{D−1}(3o − 1)/2^D`.

*Proof.* `o` odd `⟹ 3o` odd `⟹ ⌊3o/2⌋ = (3o−1)/2`. Write `3o − 1 = 2^D m` with `m` odd, so the first step
gives `o ↦ 2^{D−1}m`. On an **even** value `x = 2k`, `⌊3x/2⌋ = 3k`, i.e. the map sends `2k ↦ 3k`, which lowers
the 2-adic valuation by exactly 1 (3 is odd). Hence the iterates have valuations `D−1, D−2, …, 1, 0`, reaching
an odd value after `D−1` further steps. Total steps `= 1 + (D−1) = D`, and the terminal odd value is
`3^{D−1} m = 3^{D−1}(3o − 1)/2^D`. ∎

The induced orbit starts at `o₀ = 27` (from `c₀ = 8 → 12 → 18 → 27`, the first odd value). [VERIFIED]: GAP
lemma holds with 0 exceptions over `10⁵` odd-steps.

> **Lemma 3.3 (renewal identity, [PROVEN] in full).** Even steps of the `c`-orbit are renewal points whose
> inter-renewal gaps are exactly the `D`-values of the induced odd map. By the Kac/renewal identity
> `(mean gap) · (even-density) = 1`,
> `even-density = 1 − 1/(mean D)`, hence `even-density ≥ 1/3 ⟺ mean D ≥ 3/2`.

*Proof.* By Lemma 3.2 each induced (odd→odd) excursion of length `D` contains exactly one odd step and `D−1`
even steps among the `D` steps; equivalently exactly **one** of every `D` consecutive `c`-values is odd over
an excursion, so over the first `N` induced excursions the number of even `c`-values is `Σ(D_j − 1)` out of
`ΣD_j` total, giving even-density `= 1 − N/ΣD_j = 1 − 1/(\overline{D})` in the Cesàro limit. Then
`1 − 1/\overline{D} ≥ 1/3 ⟺ \overline{D} ≥ 3/2`. ∎

[VERIFIED]: induced `o₀=27` has `mean D = 1.99627`, `freq(D≥2) = 0.49966` over `2·10⁵` steps.

> **Lemma 3.4 (valuation formula, [PROVEN] in full).** Since `3` is a 2-adic unit,
> `D ≥ k ⟺ 3o ≡ 1 (mod 2^k) ⟺ o ≡ 3^{−1} (mod 2^k)`. Hence
> `mean D = Σ_{k≥1} freq(o ≡ 3^{−1} mod 2^k)`, with `k=1` term `≡1` and `k=2` term `= freq(o ≡ 3 mod 4)`.
> Consequently `mean D ≥ 3/2 ⟸ freq(o ≡ 3 mod 4) ≥ 1/2`, and `D=1 ⟺ o ≡ 1 (mod 4)`, `D≥2 ⟺ o ≡ 3 (mod 4)`.

*Proof.* `D = v₂(3o−1) ≥ k ⟺ 2^k | 3o − 1 ⟺ 3o ≡ 1 (mod 2^k)`; multiplying by the 2-adic unit `3^{−1}` gives
`o ≡ 3^{−1} (mod 2^k)`. Summing `mean D = Σ_{k≥1} P(D ≥ k)` (valid for `ℕ`-valued `D`) gives the series. All
`k ≥ 3` terms are `≥ 0`, so dropping them yields the one-sided sufficient bound. ∎

**Conclusion (Antihydra reduction).** Combining Lemmas 3.1–3.4: Antihydra **non-halts** iff
`E_n/n ≥ 1/3 ∀n`, which holds iff the finite check `balance_n ≥ 0` for `n ≤ N₀` holds **and** the asymptotic
one-sided density bound `liminf freq(o ≡ 3 mod 4) ≥ 1/2` holds along `o₀ = 27`. The asymptotic line is the
[OPEN] kernel (Section 6). Equivalent exact 2-adic form: `HALT ⟺ ∃n : v₂(c_n − 1) ≥ balance_n + 1`. **[PROVEN]**
— the macro-structure (`c₀ = 8`, `c_{n+1} = ⌊3c_n/2⌋`, the balance counter, and the halt criterion) is now
hand-derived in full from the raw transition table (TM-extraction note §1: shift lemmas, inner ×3/2 lemma,
even/odd carry lemmas, macro-step `c' = ⌊3c/2⌋`, halt), so no [VERIFIED] residue remains in the reduction; the
AEV/Mahler kernel remains [OPEN].

### 3.2 o10-inner — `q=2` ceiling; o10-FULL out of scope

The inner mass evolves by `m ↦ ⌈3m/2⌉` (the **literal AEV ceiling**); the inner eat-length is always even, so
the inner loop never halts ([VERIFIED]: from `m=6` the orbit `6,9,14,21,32,48,72,108,162,243,365,548`
reproduces exactly; eat-length `L = 2m − 8` is even). An epoch halts when an outer `b`-countdown lands at
`b=0` on an odd `m`.

> **Scope (enforced).** o10-FULL is **COMPOSITE/EXISTENCE**: genericity makes each epoch halt with probability
> `≈1/3` ([VERIFIED] 33.67% over `B=1..3000`), so over infinitely many epochs the halt-probability `→1` —
> o10-FULL is a **probabilistically (likely delayed) halter**, true direction [OPEN], and is **out of scope**.
> Only the inner `3/2` ceiling sub-orbit is in-family; its reduction is [PROVEN] but the criterion is for the
> inner sub-orbit only, hence o10-inner is [CONDITIONAL].

### 3.3 o18 — existence facet, `q=3`

Macro-structure ([VERIFIED], `2·10⁸` steps, 10 F-entries all read `0`, 0 collisions, planted-control test):
the leftward D/F sweep is a **base-3 odometer** whose clean milestones `M(k) := 0^∞[A]1\,0\,1^k\,0^∞` evolve, on
the **carry-absorbed (clean) epochs**, by the width law `f(k) = ⌊8k/3⌋ + 2`. The clean law is **[VERIFIED]
exactly on epochs 0–6**: `10 → 28 → 76 → 204 → 546 → 1458 → 3890` (each an exact `⌊8k/3⌋+2` step, 0
mismatches). **The *unconditional* map `M(k) → M(⌊8k/3⌋+2)` for all reachable `k` is [DISPROVEN]** (TM-extraction
companion, o18-extraction note): it **breaks at epoch 7** at `k = 3890 ≡ 2 (mod 3)` — the residue with the
deepest base-3 carry — where a carry reaches the left frontier and the clean `M`-form is destroyed; the next
clean milestone is **`27660`, not the predicted `⌊8·3890/3⌋+2 = 10375`** (`o18milestones.py`, exact). So the
honest content is the **conditional** clean-epoch lemma plus the table-trivial halt criterion (Lemma 3.5), not
an unconditional width law.

> **Lemma 3.5 (o18 halt criterion).** o18 halts `⟺` state F reads
> `1`, i.e. the leftward D/F frontier lands on an existing `1` (an adjacent-`11` left-frontier carry
> alignment of the `⌊(8/3)x⌋` orbit on `ℤ₃`). The **halt-form** "halts `⟺` F reads `1`" is **[PROVEN, trivial]**
> (the only halting transition is `F,1`, forced by the table; TM-extraction note §3.1). The elementary sweep
> lemmas (A/B-march, REFILL, leftward sweeps) and the **conditional clean-epoch lemma** "`M(k) ⟹ M(⌊8k/3⌋+2)`
> *given the sweep absorbs every carry before the leading block*" are **[PROVEN, conditional]** from the table;
> but the **unconditional** width law `k ↦ ⌊8k/3⌋+2` for all reachable `k` is **[DISPROVEN]** (it is false beyond
> epoch 6: the clean form breaks at the deep `k=3890 ≡ 2 (mod 3)` carry, §3.3 above), so the milestone
> coordinate is machine-checked only on the carry-absorbed epochs (**[VERIFIED] on epochs 0–6**). The carry
> **never** reaching the left frontier — i.e. the clean form persisting for all epochs — is exactly the
> finiteness statement `(K_o18)` **[OPEN]**, the `q=3` AEV/Erdős facet, and is the *same event* as the halt
> criterion (a frontier carry both halts F and breaks `M`-form).
>
> **Remark (why o18 is conditional but Antihydra is [PROVEN]).** Antihydra's macro-configuration `C(a,b)` is
> preserved **unconditionally at every step** — the parity branch and both carries are clean with no overflow —
> so its macro-map `c ↦ ⌊3c/2⌋` is unconditionally true and was hand-proved (§3.1). o18's clean `M(k)`-form is
> instead **destroyed by deep base-3 carries** (epoch 7), so only the *conditional* clean-epoch lemma survives.
> This carry-overflow vs. carry-clean dichotomy is precisely why Antihydra is the unique **fully-reduced
> flagship** ([PROVEN] outright) while o18/o15 remain reductions modulo a [VERIFIED]/conditional macro-coordinate.
>
> **Existence-type ([PROVEN]).** non-halt `⟺` the bad set `𝓑 = {k : carry aligns}` is empty. Density is
> **provably insufficient**: `𝓑` has density 0 yet a single alignment halts, so there is no
> `mean ≥ const` density threshold for o18. The facet is **existence** (a `Π⁰₁` tail-avoidance hitting
> event), reduced to the `q=3`, single-orbit, floor-mirror **existence/Erdős** fragment of AEV Conj 1.6.

### 3.4 o15 — same `q=3` Erdős kernel as o18, harder coordinate

Macro-structure ([VERIFIED], step-for-step `bb_sim` agreement, `120M` steps, planted control): `1^V 0 (10)^m`,
width `W ↦ ⌊8W/3⌋ + 2` (widths `19,40,108,290,773,2060,5493,14634`, ratios `→ 8/3`).

> **Lemma 3.6 (o15 halt criterion).** o15 halts `⟺` the rightward
> F→A handoff reads `11` (two 1-blocks abut) — a right-frontier collision (the mirror of o18). The
> **halt-form** "halts `⟺` state A ever reads a `1`" is **[PROVEN, trivial]** (the only halting transition is
> `A,1`, forced by the table; TM-extraction note §4). The counter
> `V` is **parity-irregular** (`V = 6,39,107,289,6,2059,6,3`), so there is no clean scalar orbit map; the
> irregularity is the base-3 digit string of the `(8/3)^n` orbit (separator positions = carry boundaries), and
> the macro-coordinate (width `W ↦ ⌊8W/3⌋+2`) **stays [VERIFIED]** (no clean scalar map to hand-prove).
> Same Erdős kernel, same AEV `q=3` existence facet as o18; harder model, identical number theory.

### 3.5 Scope exclusions

- **o10-FULL OUT** (composite; probabilistically halts; direction [OPEN]).
- **o17 kernel-less** (base-3 odometer / uniquely ergodic isometry; the halt is a Collatz-irregular carry
  predicate, not equidistribution). Embedded family `0 A 0 1^k`: `k ≢ 0 (mod 3)` halts fast ([VERIFIED]
  80/80, `k ≤ 120`); `k ≡ 0 (mod 3)` is Collatz-irregular (18 proven halters; two delayed past `10⁷`:
  `k=102` at `2.8·10⁷`, `k=108` at `6.7·10⁷`; no separating modulus). The non-halting remainder is an embedded
  [OPEN] Collatz statement. o17 contributes the highest descriptive-certificate floor (companion note) but is
  **outside the equidistribution kernel**.

> **Theorem 1 (summary).** Each in-scope cryptid's halting is an
> explicit `2^a/3^b` arithmetic event: Antihydra's density underflow / 2-adic depth (`q=2`); o18/o15's base-3
> carry alignment / collision (`q=3` existence); o10-inner's `3/2` ceiling. This is an unconditional reduction
> (raw 6-state TM → named `p`-adic predicate), independent of whether the underlying kernel is settled.
> **Antihydra is [PROVEN] outright** (the raw-TM → counter macro-structure is hand-proved in full, §3.1);
> **o18/o15/o10-inner are [PROVEN] modulo a [VERIFIED] macro-structure** (their halt criteria are
> table-trivially [PROVEN], their base-3 / ceiling macro-coordinates [VERIFIED] only on the checked epochs —
> note o18's *unconditional* width map `M(k)→M(⌊8k/3⌋+2)` is [DISPROVEN] beyond epoch 6, only its conditional
> clean-epoch lemma being [PROVEN], §3.3).

---

## 4. Theorem 2 — the induced-map structure

> **Theorem 2.** (a) [PROVEN] For every `μ = 2^a/3^b` with `v_p(μ) = −1`, `T_μ` is a clean `p`-to-1
> Haar-measure-preserving endomorphism of `ℤ_p` (Proposition 2.1). (b) [PROVEN, full inline measure side;
> cites standard 2-adic Collatz theory for exactness/Bernoullicity] Antihydra's induced odd-return map
> `T(o) = 3^{D−1}(3o − 1)/2^D`, `D = v₂(3o − 1)`, is Haar-measure-preserving on the odd 2-adic units `ℤ₂*`,
> with gap symbols `D_j` i.i.d. geometric `P(D = d) = 2^{−d}` (mean `2`); it is exact and Bernoulli.

*Proof of (b), branch-by-branch.* Partition `ℤ₂*` by the cylinders `A_d := {o ∈ ℤ₂* : v₂(3o−1) = d}`,
`d ≥ 1`. By Lemma 3.4, `A_d = {o : o ≡ 3^{−1} (mod 2^d), o ≢ 3^{−1} (mod 2^{d+1})}`, a single residue class
mod `2^{d+1}` intersected with `ℤ₂*`, of Haar measure `2^{−(d+1)} · 2 = 2^{−d}` (the factor 2 because we
normalize Haar on the units `ℤ₂*`, of total mass `1`). On `A_d`, `T(o) = 3^{d−1}(3o − 1)/2^d` is affine in
`o`; its 2-adic Jacobian is `|3^{d−1} · 3 / 2^d|_2 = |2^{−d}|_2 = 2^d` (the `3^{d}` factor is a 2-adic unit).

*Claim: `T` maps `A_d` bijectively onto `ℤ₂*`.* Injectivity is clear (affine, nonzero 2-adic derivative). For
surjectivity: `T(o) = 3^{d−1}(3o−1)/2^d`; as `o` ranges over the class `o ≡ 3^{−1} (mod 2^d)` (so
`(3o−1)/2^d ∈ ℤ₂`) the quantity `(3o−1)/2^d` ranges over all of `ℤ₂` affinely, and over the sub-condition
`o ∉ A_{>d}` it ranges over the **odd** elements; multiplying by the unit `3^{d−1}` keeps it in `ℤ₂*`. Hence
`T(A_d) = ℤ₂*`. Each branch pushes Haar`|_{A_d}` (mass `2^{−d}`) forward by the contraction factor `2^{−d}`
of the inverse, i.e. onto `2^{−d}·`Haar`_{ℤ₂*}`; summing over `d` gives `Σ_d 2^{−d} = 1`, reproducing
Haar`_{ℤ₂*}`. This is Haar-preservation.

Because each branch is **full** (maps onto the whole space) and the branch index is exactly the symbol `D`,
the system is measurably isomorphic to the one-sided Bernoulli shift on the alphabet `{1,2,3,…}` with weights
`P(d) = 2^{−d}` (the symbol `D_j` records which branch the `j`-th iterate is in, and full-branch surjectivity
makes the symbols independent and the past-independent). The i.i.d.-geometric law and **exactness/Bernoullicity**
of such full-branch piecewise-affine `p`-adic maps are standard (Lagarias's 2-adic conjugacy of the `3x+1`
map; Bernstein–Lagarias 1996; Matthews–Watts); we cite these rather than reproduce them. ∎

> **Corollary 4.1 ([PROVEN]).** Under Haar, `mean D = Σ_{d≥1} d·2^{−d} = 2 > 3/2`, so the kernel inequality
> `mean D ≥ 3/2` holds with margin `1/2` for Haar-a.e. seed (SLLN + exponential large-deviation
> concentration of even-density at `1/2`). The entire remaining problem is whether the **single** orbit
> `o₀ = 27` is Haar-generic for `T`.

**Conjecture-free facts about the specific orbit `o₀=27`.** The following are proved in full and used by
Theorem 3.

> **Lemma 4.2 (Countdown Lemma, [PROVEN] in full).** Let `φ(o) = v₂(o − 1)`. Then a `D=1` step occurs iff
> `o ≡ 1 (mod 4)` iff `φ(o) ≥ 2`, and on such a step `o' − 1 = (3/2)(o − 1)` exactly, so `φ` **decreases by
> exactly 1**. Consequently `m` consecutive `D=1` steps `⟺ o ≡ 1 (mod 2^{m+1})` (a cylinder of measure
> `2^{−(m+1)}`), and any maximal `D=1` run has length `v₂(o_start − 1) − 1`. An infinite `D=1` run occurs
> only at the off-orbit fixed point `o = 1`.

*Proof.* `D = 1 ⟺ v₂(3o−1)=1 ⟺ 3o ≡ 3 (mod 4) ⟺ o ≡ 1 (mod 4) ⟺ φ(o) ≥ 2`. For such `o`,
`T(o) = (3o−1)/2`, so `o' − 1 = (3o−1)/2 − 1 = (3(o−1))/2`; thus `v₂(o'−1) = v₂(3) + v₂(o−1) − v₂(2) = φ(o)−1`
(as `3` is odd). Iterating, a `D=1` run continues while `φ ≥ 2` and stops when `φ = 1` (`o ≡ 3 mod 4`,
`D ≥ 2`); so the run length is `φ(o_start) − 1`, and `m` steps require `φ(o_start) ≥ m+1`, i.e.
`o_start ≡ 1 (mod 2^{m+1})`. An infinite run forces `φ = ∞`, i.e. `o = 1`. ∎

[VERIFIED]: all 75139 `D=1` runs of the `o₀=27` orbit match, longest `= 19`, 0 exceptions.

> **Lemma 4.3 (periodic-itinerary exclusion, [PROVEN] in full).** Antihydra's itinerary is **not eventually
> periodic**, with no equidistribution assumed.

*Proof.* The parity coding `o ↦ (D_j)` is injective. A period-`q` cycle of `T` with itinerary
`(e_0,…,e_{q−1})` has the closed form `c₀ = N/(3^q − 2^q)` with
`N = Σ_j 2^j 3^{q−1−j} e_j ≤ 3^q − 2^q`, so every cycle point lies in `[0,1]`, and the only **integer** cycle
points are `{0,1}`. But the integer `c`-orbit is strictly increasing (`T(c) − c = ⌊c/2⌋ ≥ 1` for `c ≥ 2`), so
it reaches no cycle. Hence the itinerary is not eventually periodic. ∎

[VERIFIED]: all 2046 cycles of period `q ≤ 10` enumerated; integer fixed points of `⌊3c/2⌋` in `[0,50)` are
`{0,1}`; `3^q − 2^q` for `q=1..10` confirmed.

This bisects the exceptional set into structured/periodic (now killed) ⊔ aperiodic/full-complexity (= the
kernel).

---

## 5. Theorem 3 — the density ergodic-optimization barrier (Antihydra)

This is the program's strongest no-structure-only result. **It is [PROVEN] for Antihydra only** (o10-inner
[CONDITIONAL]; o18/o15 do **not** receive it — existence facet, Section 7). The barrier rests on the
ergodic-optimization framework, which we cite, plus a fully inline computation of the optimization value.

### 5.1 The test function and the `ψ = f(D)` lemma

Let `ψ := 1{o ≡ 1 mod 4} − 1{o ≡ 3 mod 8} − 1/2`, the one-sided test function whose nonnegativity-on-average
is the kernel. Lemma 3.4 already shows `D=1 ⟺ o≡1 mod4`. The next lemma — promoted here from a numerical
observation to an elementary proof — fixes `ψ` as a pure function of `min(D,3)`, which is what makes `β`
airtight.

> **Lemma 5.1 (`ψ = f(D)`, [PROVEN] in full).** For odd `o`, with `D = v₂(3o − 1)` and `3^{−1} ≡ 3 (mod 8)`:
> `D = 1 ⟺ o ≡ 1 (mod 4)`; `D = 2 ⟺ o ≡ 7 (mod 8)`; `D ≥ 3 ⟺ o ≡ 3 (mod 8)`. Consequently
> `ψ = +1/2` (when `D=1`), `−1/2` (when `D=2`), `−3/2` (when `D≥3`); i.e. `ψ` is a function of `min(D,3)`,
> hence of `D`. In particular `ψ(o) ≤ 1/2` for every odd `o`.

*Proof.* By Lemma 3.4, `D ≥ k ⟺ o ≡ 3^{−1} (mod 2^k)`. Now `3^{−1} ≡ 3 (mod 4)` and `3^{−1} ≡ 3 (mod 8)`
(indeed `3·3 = 9 ≡ 1 mod 8`). Thus `D ≥ 2 ⟺ o ≡ 3 (mod 4)` (so `D = 1 ⟺ o ≡ 1 mod 4`), and
`D ≥ 3 ⟺ o ≡ 3 (mod 8)`; therefore `D = 2 ⟺ (o ≡ 3 mod 4) ∧ (o ≢ 3 mod 8) ⟺ o ≡ 7 (mod 8)`. Evaluating
`ψ` on each class: `o ≡ 1 mod 4 ⟹ ψ = 1 − 0 − 1/2 = +1/2`; `o ≡ 7 mod 8 ⟹ ψ = 0 − 0 − 1/2 = −1/2`;
`o ≡ 3 mod 8 ⟹ ψ = 0 − 1 − 1/2 = −3/2`. These are constant on each `min(D,3)`-class, and the maximum value is
`+1/2`. ∎

[VERIFIED] this note: the three residue equivalences hold for all odd `o < 2·10⁵` (0 violations) and
`3^{−1} ≡ 3 (mod 8)`.

### 5.2 The ergodic-optimization value and the barrier

> **External input (cited, not reproduced): ergodic-optimization criterion.** For a continuous `ψ` on a
> compact system `(X,T)`, a one-sided inequality `(1/N)Σ_{n<N} ψ(T^n x) ≤ 0 + o(1)` holding for **all** `x`
> is governed by the **maximum ergodic average**
> `β(ψ) := max_{μ ∈ M_T} ∫ ψ dμ`, where `M_T` is the set of `T`-invariant Borel probability measures: the
> all-orbits bound is possible only if `β(ψ) ≤ 0`, and a sub-action / coboundary certificate exists exactly
> when `β(ψ) ≤ 0` (Mañé; Conze–Guivarc'h; Bousch sub-action theory; see Jenkinson's survey). We use this as
> a black box.

> **Theorem 3 (density barrier, [PROVEN, cites ergodic optimization]).** For Antihydra's induced system,
> `β(ψ) = +1/2 > 0`, attained at the fixed point `o = 1`. Hence **no all-orbits / structure-only one-sided
> inequality can prove non-halting**: such a proof would establish the false statement "all orbits non-halt,"
> contradicted by the genuinely halting fixed point `o = 1`. The target is therefore irreducibly
> orbit-27-specific.

*Proof.* Two halves, both proved in full given the cited criterion.

**(1) `β(ψ) = +1/2`, attained at a halting orbit.** By Lemma 5.1, `ψ(o) ≤ 1/2` pointwise, so
`∫ ψ dμ ≤ 1/2` for **every** `μ ∈ M_T`; thus `β(ψ) ≤ 1/2`. The point `o = 1` is a fixed point: `T(1) = 3^0(3·1−1)/2^1 = 1`
([VERIFIED]), with `D(1) = v₂(2) = 1` forever, so the atom `δ_1 ∈ M_T` and `∫ ψ dδ_1 = ψ(1) = +1/2` (since
`1 ≡ 1 mod 4`). Hence `β(ψ) = +1/2`, attained at `δ_1`. The orbit of `o=1` has even-density `0 < 1/3`, i.e.
it is a **genuinely halting** orbit. Therefore the all-orbits inequality is **false**, and (by the cited
criterion) no sub-action / structure-only certificate of the all-orbits bound exists.

**(2) Dual LP infeasibility ([VERIFIED]).** The coboundary/Lyapunov linear program
`ψ(o) ≤ g(T(o)) − g(o)` on the finite quotient mod `2^k` is solved with exact `Fraction` arithmetic and is
**infeasible for every `k = 3..12`**, the dual obstruction being the `o = 1` self-loop of weight `+1/2`
(max-mean-cycle `= +1/2` for all `k`). Tail truncation was audited sound: undetermined residues are all
`D ≥ 3` (`ψ = −3/2`, handled conservatively), 0 violations, and infeasibility is driven by the determined
`+1/2` self-loop, hence tail-independent. (This corroborates (1) but is not needed for it.) ∎

The Haar margin `1/4` (Corollary 4.1) is irrelevant to feasibility: `β` is set by the atomic maximizer `δ_1`
(value `+1/2`), not by Haar (value `−1/4`).

### 5.3 Scope and the labelling discipline

> **Labelling (enforced).** The **airtight [PROVEN] core** is exactly part (1): the all-orbits inequality is
> *false* (`β(ψ) = +1/2 > 0`, witnessed by the halting fixed point `o = 1`), with the pointwise bound
> `ψ ≤ 1/2` making `β = +1/2` exact. The broader reading **"no structure-only proof of non-halting can
> exist"** is a **sound meta-level statement relative to a stated proof class** (proofs using only
> `T`-invariant / all-orbits Lyapunov data); it is **not** an unconditional theorem about all conceivable
> proofs, and is presented as such.

> **[PROVEN] scope.** The density `β > 0` barrier holds for **Antihydra only**, with `β = +1/2` at a genuine
> halting integer fixed point `o = 1` (the sharpest possible form: the maximizer is a single literally-halting
> orbit). **o10-inner** is [CONDITIONAL] (same minimal-renewal fixed point in the inner sub-orbit, but
> o10-FULL is composite/OUT). **o18 / o15 do NOT get this barrier**: their facet is **existence**, not
> density, and there is no `β` (Section 7.1). Putting them under the density `β` was a mislabel and is
> **retracted**. **o10-FULL** is OUT (probabilistically halts); **o17** is kernel-less.

**Second derivation (shared free structure), [PROVEN].** Independently, the "free" part of the dynamics
(pathwise determined by the symbol sequence: the 3-adic fiber contraction `Φ_D(x) = 3^{D−1}2^{−D}(3x−1)` of
rate `≤ 1/3`; the synchronization `o_j mod 3^k = f(`recent `D`-history`)`) **synchronizes identically at the
halting fixed point `o = 1`** ([VERIFIED]). Hence any free/structure-only condition that holds along the real
orbit also holds at `o = 1`; since `o = 1` halts, no free condition implies non-halting. The free part is
blind to `freq(D ≥ 2)` — the sole halting discriminator — and `MI(`free 3-adic data; `D_j) = 0` (shuffle-null:
the dynamics route free data and the hard target into two CRT-independent coordinates joined only by a null
channel). The two meta-theorems are the **same obstruction seen twice** (invariant simplex vs free algebra),
which is *why* every structural attack only relocated the gap.

---

## 6. Kernel placement: AEV 1.6, the floor-mirror bridge, and the corrected dominance

After all [PROVEN] reductions, per-cryptid completion rests on exactly one named open statement, in two facets
of the same AEV instance family.

### 6.1 The open kernel

> **Kernel, density facet (`q=2`). [OPEN].** For the induced `3/2`-Syracuse orbit `o₀ = 27`:
> `liminf_{N→∞} (1/N)#{n < N : D(o_n) ≥ 2} ≥ 1/2`. Equivalently `mean D ≥ 3/2`; `liminf` even-density of
> `c₀ = 8` `≥ 1/3`; `liminf freq(o ≡ 3 mod 4) ≥ 1/2`; 3-adic form `density{3|o_j} + density{9|o_j} ≥ 1/2`.

> **Kernel, existence facet (`q=3`). [OPEN].** For o18/o15: the orbit of the seed under `⌊(8/3)x⌋` on `ℤ₃`
> avoids the clopen carry-alignment set `H` forever — the `q=3` single-orbit floor-mirror **existence/Erdős**
> fragment of AEV Conj 1.6, requiring an **effective** equidistribution rate beating a *summable* target
> (strictly stronger than the qualitative density needed in the `q=2` case).

> **Conditional theorem ([PROVEN] reduction).** Antihydra does not halt **iff** the density kernel holds
> **together with** the finite check `balance_n ≥ 0` for `n ≤ N₀`. Under Haar (Corollary 4.1) the kernel holds
> with room to spare; the whole problem is the Haar-genericity of the single orbit `o₀ = 27`.

### 6.2 Exact literature placement

The kernel is the **`p/q = 3/2`, one-sided, single-level (`k=2`), single-orbit floor-mirror fragment of the
Andrieu–Eliahou–Vivion (2025) normality conjecture** (arXiv:2510.11723, Conjecture 1.6). AEV Conj 1.6: for
coprime `p > q ≥ 1`, every orbit of the **ceiling** map `T_{p/q}(x) = ⌈px/q⌉` is equidistributed mod `q^k` for
all `k`. AEV Theorem 1.7 gives Conj 1.6 ⇔ their normality Conjecture 1.2; AEV Theorem 1.5 gives (for
`p < q²`, which holds at `3/2` since `3 < 4`) Conj 1.2 ⇒ Conj 1.4 = **Mahler's 1968 Z-number conjecture**. So
AEV is the single umbrella above the `3/2` cluster (Mahler 1968; Flatto's Z-numbers; Akiyama 2008;
Dubickas–Mossinghoff 2009), and the kernel is one instance under it. The `q=3`, `μ=8/3` existence facet sits
in the **Erdős ternary-digits-of-`2^n`** family (Narkiewicz's 1980 density upper bound; no lower bound; the
BB↔Erdős reduction of Stérin–Woods, arXiv:2107.12475).

The kernel is **strictly weaker** than AEV on three axes (one-sided vs two-sided; level `k=2` vs all `k`;
single orbit vs all `n`), yet **no named conjecture sits at this weaker level** — AEV is the weakest named
established-open conjecture that implies it.

### 6.3 The floor-mirror bridge (closing the floor-vs-ceiling gap)

AEV is stated for the **ceiling** `T_c(x) = ⌈3x/2⌉`; the cryptids run the **floor** `T_f(x) = ⌊3x/2⌋`, and the
`±1` parity flip left it open whether the "floor-mirror conjecture" was a *formally distinct* open problem.
This is closed in full.

> **Lemma 6.1 (negation conjugacy, [PROVEN] in full).** Let `R(x) = −x` on `ℤ` (equivalently `ℤ₂`). Then
> `T_c = R ∘ T_f ∘ R`, i.e. `T_c(x) = −T_f(−x)` for every `x`.

*Proof.* `⌈y⌉ = −⌊−y⌋` for every real `y`; with `y = 3x/2`,
`T_c(x) = ⌈3x/2⌉ = −⌊−3x/2⌋ = −⌊3(−x)/2⌋ = −T_f(−x)`. ∎

`R` is an involution, a Haar-measure-preserving homeomorphism of `ℤ₂`, and on each finite quotient `ℤ/2^k`
acts as the residue permutation `r ↦ (−r mod 2^k)` (a measure-preserving bijection). Iterating Lemma 6.1,
`T_f^l(n) = −T_c^l(−n)` for all `l` ([VERIFIED], several `n` incl. `2^40+1`, `l < 400`). Consequences:

> **Corollary 6.2 ([PROVEN]).** (i) The floor orbit of `n` equidistributes mod `2^k` **iff** the ceiling
> orbit of `−n` does — an exact measure-preserving (topological + measurable) isomorphism of the two systems
> on `ℤ₂`. (ii) At the induced-odd-map level the load-bearing statistic is **literally identical**: for odd
> `o` with `m = −o`, `3m + 1 = −(3o − 1)`, so `D'(−o) = v₂(3o−1) = D(o)` and `T'(−o) = −T(o)`, whence
> `D_l^{ceil}(−o₀) = D_l^{floor}(o₀)` for every `l`.

[VERIFIED] this note: `T_c(x) = −T_f(−x)` for all `x ∈ [−200,200]`; and over `5·10⁴` (doc: `2·10⁵`) induced
steps the depth sequences of floor-`27` and ceiling-`(−27)` coincide with 0 exceptions, `mean D` and
`freq(D≥2)` identical to `1.99627` / `0.49966`.

> **The bridge ([PROVEN]) and its sole residual ([CONDITIONAL]).** The floor-mirror conjecture FM(3/2) is, on
> the full sign-symmetric domain `ℤ₂`, **literally equivalent** to AEV Conj 1.6(3/2). The single residual is a
> **seed-sign quantifier**: the conjugacy `R` maps floor-**positive** orbits to ceiling-**negative** orbits
> (no positive-only conjugacy exists — on odds `T_c = T_f + 1` and the two positive orbits diverge like
> `(3/2)^l`). Thus the machines' positive floor orbits (e.g. `o₀ = 27`) correspond to *negative* ceiling
> seeds (`−27`), outside AEV's literal positive-only quantifier. Two sound readings: (i) adopt the natural
> all-`ℤ₂` (sign-symmetric) form of Conj 1.6, under which AEV(3/2) ⟺ FM(3/2) is **[PROVEN]**; or (ii) keep
> AEV's literal positive form, under which "AEV(3/2) ⟹ FM(3/2) at the machines' seeds" is **[CONDITIONAL]** on
> the believed-but-unproven sign-symmetry extension. The bridge itself is [PROVEN]; the kernel FM(3/2) /
> AEV 1.6(3/2) is [OPEN].

### 6.4 The corrected dominance statement

> **Corrected dominance ([CONDITIONAL]).** All ten `μ = 3/2` machines (Antihydra, o2, o7, o8, o10-inner, o11,
> o12, o13, o14, o16) **share the `⌊3x/2⌋` kernel** (o10-inner runs the ceiling `⌈3m/2⌉`); via §6.3 they are
> instances of the **one** named conjecture AEV 1.6(3/2). But the dependency is **not** "one conjecture decides
> all ten":
> - **2 reduce exactly** (decided [CONDITIONAL] on AEV 1.6(3/2)): **Antihydra** (single-orbit, level-`k=2`,
>   one-sided **density** fragment at `o₀=27`; qualitative AEV over-implies it; plus the finite check
>   `balance_n ≥ 0`, [VERIFIED] to `n ≤ 2·10⁵`) and **o10-inner** (literal ceiling; o10-FULL composite/OUT).
> - **8 also require an o10-FULL-grade nested-refill reduction** ([OPEN]): o2, o7, o8, o11–o14, o16. Their
>   clean `⌊3x/2⌋` law holds only on an even-`a` inner subsequence; the halt couples to an **outer**
>   doubly-exponential refill alignment (Section 7), so even a full proof of AEV 1.6(3/2) does not by itself
>   decide them — they additionally need (a) their exact `2^k` valuation halt predicate derived ([OPEN]) and
>   (b) for the existence-facet members an **effective-rate** strengthening (stronger than qualitative AEV).

So the rigorous count is **"2 decided outright [CONDITIONAL], 8 reduced modulo completing reductions + an
effective-rate strengthening,"** not "1 ⇒ 10." The in-scope exact-reduction set is **unchanged at four**
machines {Antihydra, o18, o15, o10-inner}.

### 6.5 No analytic handle ([OPEN])

AEV supports Conj 1.6 with combinatorics-on-words and numerics only — no ergodic theory, transfer operator,
exponential sums, or Fourier analysis, and **zero unconditional results at `3/2`**. The lone candidate route
is **effective power Fourier-decay** `|ν̂_{2/3}(t)| ≤ C|t|^{−a}` → Erdős–Turán → `liminf` even-density
`≥ 1/2 − O(decay)`. It is [PROVEN] (program commit) that `3/2` is **non-Pisot ⟹ `ν_{2/3}` is Rajchman**
(`ν̂_{2/3} → 0`), but the **annealed/quenched gap is the lone remaining analytic missing link [OPEN]**:
`ν̂_{2/3}`'s decay is annealed (i.i.d. weights), whereas the orbit's even-density needs the quenched Weyl sum
`Σ e(h·4·(3/2)^n)`, which `ν̂_{2/3}` does not directly bound. AEV itself does not cross this gap.

> **Honest statement of the dependency.** Per-cryptid complete proofs are **[CONDITIONAL] on AEV/Mahler with
> no known shortcut.** The reduction (Theorem 1), the induced-map structure (Theorem 2), the barrier
> (Theorem 3), and the bridge (Lemma 6.1) are the unconditional contributions.

---

## 7. Why exactly four: the nested-Collatz Blocking Theorem

This section proves why the in-scope set is **{Antihydra, o10-inner, o18, o15}** and not larger, and is the
formal content of "in-family by multiplier, not in-scope by proof."

> **Definition 7.1 (nested-Collatz machine).** A 6-state TM is **nested-Collatz** if its blank-tape evolution
> decomposes as: (1) an **inner clean expanding map** `T_μ` (`v_p(μ)=−1`) acting on a unary "mass" along an
> admissible subsequence of head-passes; (2) an **outer counter + refill**: a second quantity decremented each
> inner step that, on roll-over, fires a refill re-seeding the inner orbit, with refill seeds `{B_e}` growing
> **doubly-exponentially** (an epoch with seed `k₀` runs `≈ k₀/Δ` inner `×μ` steps, so `B_{e+1} ≈ μ^{k₀/Δ}`)
> and not eventually periodic; (3) an **outer-coupled halt**: the halt mechanic is structurally impossible
> during a normal inner epoch and can fire only at a refill boundary.

The nine instances are **{o2, o7, o8, o10-FULL, o11, o12, o13, o14, o16}** (all `μ=3/2`), with inner maps,
doubly-exponential refill orbits, and outer-coupled halts [VERIFIED] against `bb_sim`.

> **Theorem 5 (Nested-Collatz Blocking).** Let `M` be nested-Collatz. Then `M`'s exact halt predicate is
> **not** equivalent to a single-orbit equidistribution / carry-avoidance statement about its inner `T_μ`
> (the form that decides the in-scope cryptids). Precisely:
>
> **(i) [PROVEN, definitional].** The halt does not occur within any inner epoch (Def. 7.1 clause 3); the
> inner map alone has no halt site, so no statement about the single inner orbit can be equivalent to "M
> halts".
>
> **(ii) [PROVEN, structural].** `M` halts `⟺ ∃ e :` the `e`-th reseeded inner orbit (started at the
> doubly-exponential seed `B_e`) produces the lethal outer alignment at its boundary — an **existence
> statement over infinitely many restarting orbits**, a strictly larger logical object than "the single inner
> orbit equidistributes."
>
> **(iii) [PROVEN-instance for o10; CONDITIONAL/VERIFIED-instance for the other 8].** For o10 the exact
> predicate is derived (halt `⟺ ∃` epoch whose `b`-countdown lands on `b=0` at odd `m`) and the inner
> eat-length `L = 2m − 8` is provably always even, so the blocking is [PROVEN]. For o2,o7,o8,o11–o14,o16 the
> halt mechanic is [PROVEN, unit-tested] and the inner-never-triggers fact is [VERIFIED] (the
> halt-determining cell is never the halt symbol across millions of inner-epoch visits), but the exact
> closed-form predicate is [OPEN]; the blocking is [CONDITIONAL] on the verified structural model.

*Proof of (i)–(ii).* (i) is Definition 7.1 clause 3. For (ii): each refill restarts a fresh inner orbit at
`B_e`; the halt is realized only at a boundary, so the predicate quantifies over the reseed family
`{O_e}_{e≥0}`, not over `O_0`. The required analysis is: (1) the inner single-orbit AEV statement governing
the parity/carry phase at each underflow index, **⊗** (2) the outer refill map `B_{e+1} = R(`terminal config of
epoch `e`)` (piecewise-affine, doubly-exponential), **⊗** (3) a **Borel–Cantelli existence test** over the
deterministic, doubly-exponentially-sparse `{B_e}` — whether the inner phase **ever** realizes the lethal
alignment at a reseeded boundary, which needs **effective** equidistribution (a rate beating a summable
target), strictly stronger than the qualitative single-orbit statement that suffices in scope. ∎

[VERIFIED] (`nc_verify*.py`, `2·10⁶` steps): for o10/o11/o13 the halt-precursor state is entered ~1500
times within inner epochs yet the halt transition never fires; inner refill orbits reach doubly-exponential
seeds (`o11`: `k=201` at step `12088`, `k=582` at step `56237`).

> **Placement.** Nested-Collatz `=` in-scope single-orbit object **+** doubly-exponential outer reseed map
> **+** Borel–Cantelli-over-restarts existence test. It is a strict super-structure of the in-scope cryptids,
> disjoint from them and from the kernel-less odometers (o3, o17). The in-scope set is therefore exactly four.

> **Cross-reference (Axis-2 conditional theorem).** The halt object isolated in Theorem 5(ii) —
> `M` halts `⟺ ∃ e : O_e ∩ H_e ≠ ∅`, a Borel–Cantelli hitting/avoidance event over the doubly-exponential
> reseed family `{B_e}` — is developed as a standalone **conditional theorem** in the companion note
> `NESTED_COLLATZ_THEOREM.md`, the Axis-2 counterpart of the Axis-1 single-orbit reductions of §3. Conditional
> on an effective reseeded-equidistribution hypothesis (EFF-EQ), it splits cleanly: the **convergent** side
> `Σ_e p_e < ∞ ⟹ non-halt` follows from **Borel–Cantelli I** (no independence; the *weaker* ask, lifting
> o18's existence reduction to the reseed family, **[CONDITIONAL]** on a rate beating a summable target), while
> the **divergent** side `Σ_e p_e = ∞ ⟹ halt` needs **Borel–Cantelli II** / quenched quasi-independence that a
> single deterministic reseed family cannot supply — the **o10 wall**, **[OPEN]**. The note also records the
> two-part barrier inheritance: the inner parity sub-factor inherits the [PROVEN] density `β = +1/2 > 0`
> barrier, while the full outer existence event sits on the [OPEN] over-approximation axis. No machine is
> decided and no halting direction is claimed there.

---

## 8. The frontier catalogue (context, [VERIFIED])

For completeness: the BB(6) Collatz core was classified end-to-end ([VERIFIED]; no machine decided — all are
HOLDOUT under every sound decider in the program). The core resolves into three strata.

1. **Expanding-kernel `{μ : v_p(μ) = −1}` — four named Mahler/Erdős multipliers** `{3/2, 5/2 (p=2); 4/3,
   8/3 (p=3)}`. Each member's halt is a single-orbit `⌊μ^n⌋ mod p` equidistribution / carry-avoidance event.
   The only [PROVEN] no-structure-only barrier is **Antihydra's density `β > 0`** (Theorem 3); all other
   members are existence-facet with no proven barrier.
2. **Kernel-less odometers** (o3, o17): no expanding `T_μ`; hardness is a Collatz-irregular carry/halt
   predicate, not equidistribution. o17 carries the highest descriptive-certificate floor (`m* = 8`,
   companion note); o3 is the tamest (runs `≤ 6`) but still HOLDOUT.
3. **Too-irregular machines** (o11–o14, o16): regular `~√t` width envelope hiding irregular geometric content
   with no clean scalar `2^a/3^b` map over the observed epochs; [OPEN], no exact reduction extracted.

**Two-facet asymmetry ([PROVEN organizational]).** A *density* all-orbits inequality must account for **every**
invariant measure, including the atom `δ_{y_*}` at a halting orbit (ergodic optimization is a `max_μ`), so a
halting orbit *forces* `β > 0` — this is why Antihydra's barrier is [PROVEN]. An *existence* structure-only
proof is a forward-invariant **set** `L` that can simply **exclude** the halting orbit and all of `H`, so a
halting orbit does **not** block an avoidance certificate; hence the existence barrier (o18/o15) is [OPEN],
equal to the descriptive over-approximation top.

**Companion note.** The conjecture-free **certification-complexity hierarchy** (five strict separations
`star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ CF ⊊ CS` with explicit simulation-verified witnesses; the subword
floor `p(ℓ) ≥ 1.71ℓ`; per-machine certificate floors `m* = 2` for o18, `m* = 8` for o17) is orthogonal to the
equidistribution kernel and is documented separately (it has its own external dependency, arXiv:1901.03913,
for the `CF ⊊ CS` step). It is not part of this note.

---

## 9. Unconditional fallback theorems

These hold **unconditionally** (no dependence on the open kernel) and are publishable standalone:

1. **Exact reduction theorem** (Theorem 1): each in-scope cryptid's halting `=` a named `2^a/3^b` arithmetic
   event. **[PROVEN] outright for Antihydra** (macro-structure hand-proved from the raw transition table);
   **[PROVEN] modulo [VERIFIED] macro-structure for o18/o15/o10-inner** (halt criteria table-trivially [PROVEN];
   for o18, additionally the conditional clean-epoch lemma is [PROVEN] while the unconditional `⌊8k/3⌋+2` width
   map is [DISPROVEN] beyond epoch 6, §3.3).
2. **Induced-map Haar/Bernoulli theorem** (Theorem 2): `T_μ` Haar-preserving on `ℤ_p` for `v_p(μ)=−1`;
   Antihydra's `D_j` i.i.d. geometric, `mean D = 2`. **[PROVEN]** (measure side full; exactness/Bernoulli
   cited).
3. **Haar-a.e. non-halting (annealed)** **[PROVEN]**: density (Antihydra) `mean D = 2 > 3/2` a.s.; existence
   (o18/o15) via Borel–Cantelli I (`Σ Haar(B_n) ≍ Σ (8/3)^{−n} < ∞`). *Honest caveat:* annealed ≠ quenched;
   the actual seed is a single Haar-null point, so this decides **no** machine.
4. **Not eventually periodic** (Lemma 4.3): **[PROVEN], conjecture-free.**
5. **No-structure-only density barrier for Antihydra** (Theorem 3): `β = +1/2 > 0` at the halting fixed point.
   **[PROVEN, cites ergodic optimization].**
6. **The floor-mirror bridge** (Lemma 6.1, Corollary 6.2): **[PROVEN], conjecture-free.**

---

## 10. Open problems

1. **The kernel (`q=2` density). [OPEN].** `liminf freq(o ≡ 3 mod 4) ≥ 1/2` along `o₀ = 27` — the
   single-orbit, level-`k=2`, one-sided floor-mirror fragment of AEV 1.6(3/2). The lone analytic lead is the
   quenched Weyl-sum cancellation `Σ e(h·4·(3/2)^n)`; the annealed→quenched bridge is the missing link.
2. **The kernel (`q=3` existence). [OPEN].** Effective carry-avoidance for the `⌊(8/3)x⌋` orbit (o18/o15) —
   the Erdős ternary-digits facet; needs an effective rate beating a summable target.
3. **The seed-sign extension. [CONDITIONAL → OPEN].** Whether AEV 1.6 is sign-symmetric (so its literal
   positive form implies the floor-mirror version at the machines' seeds).
4. **The exact `2^k` predicates and effective-rate reductions for the eight nested-Collatz `μ=3/2`
   machines. [OPEN]** (Theorem 5(iii)).
5. **Direction for the nested-Collatz machines. [OPEN].** A heuristic Borel–Cantelli reads "genericity ⟹
   halt" (o10-FULL leans halting `~1/3` per epoch) but the per-epoch probability is not cleanly extractable
   for the other eight; no direction is claimed.

---

## 11. Label → Turing-machine definitions

bbchallenge standard-format transition strings (from `busybeaver/suite.py`, lines 32–50). Format: six
state-blocks `A_B_C_D_E_F` separated by `_`, each block two transitions (read 0, read 1) as
`<write><move><next>`; `Z` = halt, `---` = undefined (halt). Blank symbol `0`.

| label | role in this note | TM string |
|---|---|---|
| **Antihydra** | in-scope, `μ=3/2`, density (Thm 1,2,3) | `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` |
| **cryptid o10** | o10-inner in-scope ([CONDITIONAL]); o10-FULL OUT/nested | `1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC` |
| **cryptid o15** | in-scope, `μ=8/3`, existence (Thm 1) | `1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA` |
| **cryptid o18** | in-scope, `μ=8/3`, existence (Thm 1) | `1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---` |
| **cryptid o17** | kernel-less odometer (OUT; companion note) | `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` |
| **Space Needle** | `μ=5/2` (in-class [VERIFIED], not in-scope) | `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD` |
| **cryptid o2** | nested-Collatz `μ=3/2` | `1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA` |
| **cryptid o3** | kernel-less odometer (OUT) | `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC` |
| **cryptid o4** | `μ=4/3` (in-class [VERIFIED], not in-scope) | `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---` |
| **cryptid o5** | `μ=4/3` (in-class [VERIFIED], not in-scope) | `1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB` |
| **cryptid o7** | nested-Collatz `μ=3/2` | `1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC` |
| **cryptid o8** | nested-Collatz `μ=3/2` | `1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE` |
| **cryptid o11** | nested-Collatz `μ=3/2` | `1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF` |
| **cryptid o12** | nested-Collatz `μ=3/2` | `1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB` |
| **cryptid o13** | nested-Collatz `μ=3/2` | `1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA` |
| **cryptid o14** | nested-Collatz `μ=3/2` | `1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE` |
| **cryptid o16** | nested-Collatz `μ=3/2` | `1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE` |

---

## References

All locators pinned and verified against the program's citation digest (`CITATIONS.md`). The only genuinely
unpinnable item — Conze–Guivarc'h — is cited honestly as unpublished.

**Equidistribution / Mahler frontier (the [OPEN] kernel and its umbrella).**

- M. Andrieu, S. Eliahou, L. Vivion, *A Normality Conjecture on Rational Base Number Systems*,
  arXiv:**2510.11723** (2025) — Conjectures 1.2, 1.4, 1.6; Theorems 1.5, 1.7. (The single named [OPEN] kernel
  of this note.)
- K. Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. **8** (1968), no. 2, 313–321.
  DOI 10.1017/S1446788700005371.
- L. Flatto, J. C. Lagarias, A. D. Pollington, *On the range of fractional parts {ξ(p/q)ⁿ}*,
  Acta Arith. **70** (1995), no. 2, 125–147. (The support/spread `1/3` bound; distinct axis from the density
  kernel.)
- S. Akiyama, Ch. Frougny, J. Sakarovitch, *Powers of rationals modulo 1 and rational base number systems*,
  Israel J. Math. **168** (2008), 53–91. DOI 10.1007/s11856-008-1056-4. (The "Akiyama 2008" triple-expansions
  structure.)
- A. Dubickas, M. J. Mossinghoff, *Lower bounds for Z-numbers*, Math. Comp. **78** (2009), no. 267,
  1837–1851. DOI 10.1090/S0025-5718-09-02240-9. (The "4/3 problem" paper.)
- S. Eliahou, J.-L. Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem*,
  arXiv:**2504.13716** (2025), to appear in C. R. Math. Acad. Sci. Paris.
- T. Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:**1909.03562**
  (2019/2022). (Log-density ensemble theorem; no per-orbit output.)

**Erdős ternary-digits facet (`q=3` existence kernel).**

- P. Erdős, *Some unconventional problems in number theory*, Math. Mag. **52** (1979), no. 2, 67–70.
- W. Narkiewicz, *A note on a paper of H. Gupta concerning powers of 2 and 3*, Univ. Beograd. Publ.
  Elektrotehn. Fak. Ser. Mat. Fiz. No. 678–715 (1980), 173–174. (Density bound `≤ 1.62 x^{α₀}`,
  `α₀ = log₃ 2`.)
- T. Stérin, D. Woods, *Hardness of busy beaver value BB(15)*, arXiv:**2107.12475**. (The BB↔Erdős reduction
  for the `q=3` facet.)

**Ergodic optimization / sub-action theory (Theorem 3 external input).**

- R. Mañé, *Generic properties and problems of minimizing measures of Lagrangian systems*, Nonlinearity **9**
  (1996), no. 2, 273–310. DOI 10.1088/0951-7715/9/2/002. (Measure-rigidity half.)
- T. Bousch, *Le poisson n'a pas d'arêtes*, Ann. Inst. H. Poincaré Probab. Statist. **36** (2000), no. 4,
  489–508. (Sub-action / "revelation" existence half.)
- T. Bousch, *La condition de Walters*, Ann. Sci. Éc. Norm. Supér. (4) **34** (2001), no. 2, 287–311.
  DOI 10.1016/S0012-9593(00)01062-4. (Sub-action existence in the Walters class.)
- O. Jenkinson, *Ergodic optimization*, Discrete Contin. Dyn. Syst. **15** (2006), no. 1, 197–224.
  DOI 10.3934/dcds.2006.15.197. (Survey; the `β = sup_μ ∫ f dμ` variational principle + revelation theorem,
  cited for the equivalence as stated.)
- O. Jenkinson, *Ergodic optimization in dynamical systems*, Ergodic Theory Dynam. Systems **39** (2019),
  no. 10, 2593–2618. DOI 10.1017/etds.2017.142 (arXiv:1712.02307). (Updated survey.)
- A. Conze, Y. Guivarc'h, sub-action lemma, **unpublished** (c. 1993). (Genuinely never formally published;
  cited as the original attribution alongside the published anchors Mañé / Bousch / Jenkinson.)

**2-adic Collatz conjugacy / Bernoulli structure (Theorem 2(b) external input).**

- J. C. Lagarias, *The 3x+1 problem and its generalizations*, Amer. Math. Monthly **92** (1985), no. 1, 3–23.
  DOI 10.1080/00029890.1985.11971528.
- D. J. Bernstein, J. C. Lagarias, *The 3x+1 conjugacy map*, Canad. J. Math. **48** (1996), no. 6,
  1154–1169. DOI 10.4153/CJM-1996-060-x.
- K. R. Matthews, A. M. Watts, *A generalization of Hasse's generalization of the Syracuse algorithm*,
  Acta Arith. **43** (1984), no. 2, 167–175.

**Used only by the companion certification-hierarchy note (not by this paper), pinned for completeness.**

- D. Pálvölgyi, *The range of non-linear natural polynomials cannot be context-free*, arXiv:**1901.03913**
  (2019). (Base-`q` range of a polynomial is context-free iff linear.)

---

*Soundness statement. Every label above is copied without upgrade from the program's source documents
(`BB6_STRUCTURAL_LIMIT_THEOREM.md`, `COMPLETE_PROOF_CAPSTONE.md`, `CRYPTID_REDUCTIONS.md`,
`FLOOR_MIRROR_CONJECTURE.md`, `MAHLER_3_2_DOMINANCE.md`, `NESTED_COLLATZ_STRUCTURE.md`,
`O18_EXTRACTION_PROOF.md`, `SESSION_2026-06-29_NESTED_COLLATZ.md`). Lemmas 3.1–3.4, 4.2, 4.3, 5.1, 6.1 and
Corollary 6.2 are proved in
full inline. Antihydra's Theorem 1 macro-structure layer is now [PROVEN] (a full conjecture-free hand-proof
from the raw transition table; companion note `TM_EXTRACTION_PROOFS.md` §1); for o18 (companion note
`O18_EXTRACTION_PROOF.md`) the conditional clean-epoch lemma and the halt criterion are [PROVEN] while the
unconditional `⌊8k/3⌋+2` width map is [DISPROVEN] beyond epoch 6 (§3.3); o18/o15/o10-inner's remaining
macro-structure and Theorem 3's LP step remain [VERIFIED] (machine-checked), explicitly flagged. Theorem 2(b)'s
exactness/Bernoullicity and Theorem 3's ergodic-optimization equivalence are external inputs, cited as such. The kernel (AEV/Mahler) is [OPEN]; per-cryptid completion is [CONDITIONAL]
on it with no known shortcut. No machine is decided; no non-halting is asserted unconditionally. Numerics
re-verified this session with the `.venv` exact big-integer interpreter against `bb_sim` semantics.*
