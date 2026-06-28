# The BB(6) Structural Limit Theorem and Frontier Catalogue for the Expanding-Kernel Collatz Core

*A standalone, self-contained consolidation of result (B) of the BB(6) program (2026-06-28).*

**Soundness discipline (paramount).** Every assertion carries an explicit `[PROVEN]` / `[CONDITIONAL]` /
`[OPEN]` / `[VERIFIED]` label copied verbatim from the source documents; **no label is upgraded**, and scope
is enforced precisely. `[PROVEN]` means conjecture-free and/or elementary; `[VERIFIED]` means machine-checked
this program (exact arithmetic, `bb_sim`-cross-checked) but not promoted to a proof unless separately argued;
`[CONDITIONAL]` states its exact dependency; `[OPEN]` is a named, recognized open problem. Zero false claims;
no machine is decided; no non-halting is asserted unconditionally.

Source documents consolidated: `PATH_TO_COMPLETE_PROOF.md`, `LIMIT_THEOREM_AUDIT.md`,
`COMPLETE_PROOF_CAPSTONE.md`, `UNIFIED_LIMIT_THEOREM.md` (+ its correction banner), `EXISTENCE_META_THEOREM.md`,
`LIMIT_THEOREM.md`, `O17_REG_BARRIER.md`, `O18_NO_CERTIFICATE.md`, `CRYPTID_REDUCTIONS.md`,
`SESSION_2026-06-28_{MINPROP, UNITPART, REDUCTIONS, CERT_HUNT}.md`, `FLOOR_MIRROR_CONJECTURE.md`,
`MAHLER_3_2_DOMINANCE.md`, `SESSION_2026-06-29_FLOOR_MIRROR.md`, `REDUCE_O2_O7_O8.md`, `REDUCE_O11_O16.md`.

---

## 1. Abstract — the defensible headline

> For the BB(6) **expanding-kernel Collatz cryptids** (multiplier `μ = 2^a/3^b`, `v_p(μ) = −1`: Antihydra, o18,
> o15, o10-inner), non-halting reduces — by **exact, machine-verified reductions** — to a single-orbit
> equidistribution statement that is the **floor-mirror, single-orbit, single-level fragment of the
> Andrieu–Eliahou–Vivion (2025) normality conjecture** (its q=2/Mahler *density* facet for `3/2`; its
> q=3/Erdős *existence* facet for `8/3`). On the **density facet, Antihydra additionally carries a PROVEN
> no-structure-only barrier** (ergodic optimization `β = +1/2 > 0`, attained at the halting fixed point
> `o=1`): no all-orbits / structure-only argument can prove non-halting, so the halting/non-halting
> distinction lives **only** in single-orbit genericity. Independently and conjecture-free, the
> **certification-complexity hierarchy** for non-halting has **five strict separations** with explicit
> machine-verified witnesses (`star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ CF ⊊ CS`); the cryptid lies on an
> **orthogonal over-approximation axis** whose floor is pinned from below (subword complexity `p(ℓ) ≥ 1.71ℓ`;
> certificate floors `m*=2` for o18, `m*=8` for o17), while the REG / all-k certificate barrier itself
> remains **OPEN**.

**One-sentence version.** *BB(6)'s expanding-kernel Collatz cryptids reduce, by exact machine-verified
reductions, to a named fragment of the AEV/Mahler equidistribution conjecture, with a proven
ergodic-optimization barrier (Antihydra) showing no structure-only proof can exist — anchored by a
conjecture-free five-level certification-complexity hierarchy.*

**What this document does and does not claim.** It does *not* decide any cryptid, claim any shortcut to a
cryptid, or assert any non-halting. It is the original contribution that does *not* require solving any
cryptid: a structural limit theorem + frontier catalogue characterizing **what the BB(6) Collatz core is
equivalent to** and **why it is structurally resistant**. The single honest `[OPEN]` kernel is named
(AEV/Mahler), and per-cryptid completion (result (A)) is conditional on it.

**Scope of "Collatz core" (enforced).** The phrase is scoped to the `v_p(μ) = −1` expanding-kernel machines
**{Antihydra, o18, o15, o10-inner}**, **explicitly excluding**:
- **o17** — kernel-less odometer (uniquely ergodic isometry); its hardness is a Collatz-irregular *halt
  predicate*, not equidistribution. It contributes the highest certificate floor (`m*=8`) but is outside the
  equidistribution kernel.
- **o10-FULL** — composite/existence; genericity makes it *halt* (likely a delayed halter; direction `[OPEN]`).
  Only its **inner** `3/2` sub-orbit is in the kernel.

The shared family-wide `[PROVEN]` fact is the **kernel structure** (`T_μ` exact, Haar-preserving, Bernoulli,
`v_p(μ) = −1`), **NOT** the barrier (the `β>0` barrier is `[PROVEN]` for **Antihydra only**).

**Completed frontier catalogue `[VERIFIED]`.** The BB(6) Collatz core is now classified end-to-end (§7.2,
`SESSION_2026-06-28_CATALOGUE_COMPLETE.md`, `CATALOGUE_{O2_O5, O7_O12, O13_SN}.md`): the expanding-kernel class
`{μ : v_p(μ) = −1}` is realized by **exactly four `[VERIFIED]` multipliers — `3/2`, `5/2` (`p=2`); `4/3`, `8/3`
(`p=3`)** — so the entire core is a finite catalogue of **named Mahler/Erdős equidistribution problems**, plus
two kernel-less odometers (o3, o17) and five too-irregular machines (o11–o14, o16). The two new multipliers,
**`5/2` (Space Needle) and `4/3` (o4/o5)**, are `[VERIFIED]` (exact integer reset-difference ratios,
`bb_sim`-cross-checked), **not** `[PROVEN]`; they extend the kernel *class* but do **not** add to the in-scope
exact-reduction set (which stays {Antihydra, o18, o15, o10-inner}, §3) and do **not** carry any new barrier.

---

## 2. Setup — BB(6), cryptids, and the expanding-kernel class

**BB(6).** The sixth busy-beaver value is governed by a small set of 6-state 2-symbol Turing machines on the
bbchallenge frontier — the **cryptids** — whose halting is not settled by any finite-state decider and is
equivalent to recognized open problems in arithmetic dynamics. The complete catalogue of 19 BB(6) cryptids
was reverse-engineered against the raw TMs (`CRYPTID_REDUCTIONS.md`, Stage-1): every one carries **irregular
geometric `2^a/3^b`-rate (Mahler/Collatz) content** in one of two cosmetic width envelopes (direct-geometric
or sawtooth `~√t`). There is no tractable subclass; the envelope dichotomy is cosmetic, the deep difficulty is
one and the same.

**The expanding-kernel class.** For a Mahler multiplier `μ = 2^a/3^b` in lowest terms with denominator a
single prime `p` (i.e. `v_p(μ) = −1`), the map

> `T_μ(x) = ⌊μ x⌋`   on   `ℤ_p`

is the shared kernel object. The relevant in-scope machines and their multipliers:

| machine | multiplier `μ` | prime `p` | facet | in scope? |
|---|---|---|---|---|
| **Antihydra** | `3/2` | `p=2` | density | **IN** (fully `[PROVEN]`) |
| **o10-inner** | `3/2` | `p=2` | density (inner sub-orbit) | **IN** (`[CONDITIONAL]`) |
| **o18** | `8/3 = 2³/3` | `p=3` | existence (Erdős) | **IN** (`[CONDITIONAL]`) |
| **o15** | `8/3 = 2³/3` | `p=3` | existence (Erdős) | **IN** (`[CONDITIONAL]`) |
| o17 | base-3 odometer (`≈×8`) | — | existence-shaped | **OUT** — kernel-less |
| o10-FULL | composite | — | composite | **OUT** — probabilistically halts |

The wider family (o5 `4/3`, o7/o8 `3/2`, the slow-width majority) is **in-family by multiplier but not
in-scope by proof** — their reductions are "reduced to family + multiplier," not exact halt criteria, so the
hypotheses below are not established for them and the theorem covers them only conjecturally
(`UNIFIED_LIMIT_THEOREM.md` §4, `CRYPTID_REDUCTIONS.md` Tier-1).

**The full multiplier set `[VERIFIED]`.** With the frontier catalogue now complete
(`SESSION_2026-06-28_CATALOGUE_COMPLETE.md`), the expanding-kernel class `{μ : v_p(μ) = −1}` is realized across
the whole BB(6) Collatz core by **exactly four distinct multipliers**:

| multiplier `μ` | prime `p` | `v_p(μ)` | facet (AEV) | machines (`[VERIFIED]`) |
|---|---|---|---|---|
| `3/2` | `p=2` | `−1` | q=2 density / existence | Antihydra (density), o10-inner, o2, o7, o8 (existence) |
| `5/2` (**new**) | `p=2` | `−1` | q=2 existence | Space Needle |
| `4/3 = 2²/3` (**new**) | `p=3` | `−1` | q=3 Erdős existence | o4, o5 |
| `8/3 = 2³/3` | `p=3` | `−1` | q=3 Erdős existence | o18, o15 |

The two **new** multipliers are `[VERIFIED]` this program (exact integer reset-difference ratios over ≥4 clean
epochs, `bb_sim`-cross-checked), **not promoted to `[PROVEN]`**:
- **`5/2` — Space Needle** (`1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD`): clean-reset widths give first
  differences `24, 60, 150, 375`, each exactly `×5/2`, so the clean induced map is `T_μ(x) = ⌊5x/2⌋` on `ℤ₂`,
  `v₂(5/2) = −1` (`5` odd). `5/2 ∉ {2^a/3^b}`, so it is **neither** the literal Antihydra `3/2` orbit **nor**
  the Erdős `8·3⁻¹` cluster — its own `μ=5/2`, `p=2` member of the clean class. This **corrects** the earlier
  loose "Mahler-3/2-type" tag (`CATALOGUE_O13_SN.md` §1, `[VERIFIED]`).
- **`4/3 = 2²/3` — o4, o5**: reset-peak ratios converge to `1.334–1.337 ≈ 4/3`, placing both in the **Erdős
  ternary-digits family alongside o15/o18**, so the q=3 Erdős existence cluster is `{o4, o5, o15, o18}`. This
  **corrects** o5's stray "exponential-envelope" tag — `4/3` is the *content* multiplier; the *width* envelope is
  `~√t` (`CATALOGUE_O2_O5.md` §o5, `[VERIFIED]`).

These extend the kernel **class** but not the in-scope **proof** set of §3 (which stays {Antihydra, o18, o15,
o10-inner}); the new machines remain in-family-by-multiplier, not-in-scope-by-proof, and carry no new barrier.
The clean-`p`-to-1 status of both new multipliers was already independently `[VERIFIED]` in §4.1 (`5/2` for
`p=2`; `4/3` for `p=3`).

---

## 3. Theorem 1 [PROVEN] — the exact reductions (raw TM → arithmetic criterion)

Each in-scope machine's halting was pinned to a specific structural/arithmetic event by an **exact,
machine-verified reduction** (no analogy), `bb_sim`-cross-checked. The per-machine statements:

### 3.1 Antihydra — density facet, q=2 [PROVEN exact]
Antihydra tracks the integer orbit `c₀ = 8`, `c_{n+1} = ⌊3c_n/2⌋`, counting `E_n =` (# even values among
`c_0,…,c_{n-1}`). With `balance_n := 3E_n − n`:

> **[PROVEN] (Link 0).** Antihydra halts `⟺ ∃n: balance_n < 0 ⟺` even-density `E_n/n` drops below `1/3` at
> some `n`. Equivalently non-halt `⟺ E_n/n ≥ 1/3 for all n`. Sharpness: if `liminf E_n/n < 1/3` the machine
> halts, so `1/3` is exact (`COMPLETE_PROOF_CAPSTONE.md` §2 Link 0, `KERNEL_FINAL.md` §2 converse).

`[VERIFIED]` `balance_n ≥ 0` to `N₀ = 2·10⁵` (min balance `+2`). Facet: **density** (a Cesàro/limit average).
Equivalent exact 2-adic form (`LIMIT_THEOREM.md` §3, `antihydra_attack.md` §3c):
`HALT ⟺ ∃n: v₂(c_n − 1) ≥ balance_n + 1`.

### 3.2 o10 — composite/existence; inner is q=2, but o10-FULL is OUT [PROVEN reduction, scope-corrected]
> **[PROVEN] exact halt criterion** (L=1..8 unit-test + real orbit `5·10⁶`, `O10_REDUCTION.md`,
> `SESSION_2026-06-28_REDUCTIONS.md`). o10 halts `⟺` the C/F leftward eat-sweep consumes an **odd-length
> 1-run**. The inner orbit is `m → ⌈3m/2⌉` (**literally the AEV ceiling 3/2**); the inner eat-length is always
> even, so the inner loop never halts; the epoch halts when the b-countdown lands at `b=0` on an odd `m`.

> **Scope (enforced).** o10 is **COMPOSITE/EXISTENCE**, not a one-sided density criterion. The direction is
> **reversed**: genericity makes each epoch halt w.p. `≈1/3` (`[OBSERVED]` 33.67% over B=1..3000), so over
> infinitely many epochs the halt-probability `→1` — o10 is a **probabilistically-halting (likely delayed)
> halter**, true direction `[OPEN]`. **o10-FULL is OUT of scope.** Only the inner `3/2` kernel
> (`[CONDITIONAL]`) is in-family.

### 3.3 o18 — existence facet, q=3 [PROVEN exact, existence-type]
> **[PROVEN] exact halt criterion** (`2·10⁸` steps, 10 F-entries all read `0`, 0 collisions; planted control;
> `O18_REDUCTION.md`, `SESSION_2026-06-28_REDUCTIONS.md`). o18 halts `⟺` state F reads `1` `⟺` the leftward
> D/F sweep frontier lands on an existing `1` — an **adjacent-`11` left-frontier carry alignment**. Clean
> width law `f(N) = ⌊8N/3⌋ + 2` (`[VERIFIED]` epochs `10→28→76→204→546→1458→3890`); **breaks at epoch 8**
> (`f(3890)=10375 ≠ 27660`) via a carry.

> **[PROVEN] existence-type.** non-halt `⟺` the bad set `𝓑 = {k : carry aligns}` is empty/finite. **Density is
> provably insufficient** (`𝓑` is density-0 but a single alignment halts; `O18_REDUCTION.md`: "there is no
> `mean D'' ≥ const` halt threshold for o18"). Facet: **existence** (a hitting/avoidance event, Π⁰₁
> tail-avoidance), reduced to the **q=3, single-orbit, floor-mirror, existence/Erdős fragment of AEV
> Conj 1.6 `[OPEN]`**.

### 3.4 o15 — same q=3 Erdős kernel as o18, messier coordinate [PROVEN exact]
> **[PROVEN] exact halt criterion** (step-for-step `bb_sim` agreement, `120M` steps, planted control;
> `O15_REDUCTION.md`). o15 halts `⟺` the rightward F→A handoff reads `11` (two 1-blocks abut) — a
> **right-frontier collision (o18 mirror)**. Same width map `W ↦ ⌊8W/3⌋ + 2` (different seed, fixed point
> `N=−1`); the **parity-irregularity lives in the block decomposition** = the base-3 digit string of the
> `(8/3)^n` orbit (separator positions = carry boundaries). Counter `V` is parity-irregular
> (`V = 6,39,107,289,6,2059,6,3`), so there is **no clean scalar orbit map** — the harder-to-model 8/3
> partner. **Same Erdős kernel, same AEV q=3 existence facet** as o18; the model is harder but the number
> theory is identical.

### 3.5 Scope exclusions baked in
- **o10-FULL OUT** (composite; probabilistically halts — direction reversed, `[OPEN]`).
- **o17 kernel-less** (odometer / uniquely ergodic; carry-overflow halt predicate, not equidistribution).
  Exact embedded family `0 A 0 1^k`: `k ≢ 0 (mod 3)` always halts fast (80/80, `k≤120`); `k ≡ 0 (mod 3)`
  Collatz-irregular — **18 proven halters**, two **delayed past `10⁷`** (`k=102 @ 2.8·10⁷`,
  `k=108 @ 6.7·10⁷`), no modulus, non-monotone (`O17_REG_BARRIER.md` §1, `[VERIFIED]`). The non-halting
  remainder is an embedded `[OPEN]` Collatz statement.

> **Reduction theorem [PROVEN] (Theorem 1, summary).** Each in-scope cryptid's halting is an **exact,
> machine-verified arithmetic event** of a `2^a/3^b` orbit: Antihydra's density underflow / 2-adic depth
> (`q=2`), o18/o15's base-3 carry alignment / collision (`q=3` existence), o10-inner's `3/2` ceiling. This is
> a clean unconditional theorem (raw 6-state TM → named `p`-adic predicate) — itself a publishable result —
> independent of whether the underlying equidistribution kernel is settled.

---

## 4. Theorem 2 [PROVEN] — the induced-map structure (the family-wide kernel)

The kernel `T_μ` is a bona-fide exact Syracuse-type system; the measure side is **complete**.

### 4.1 Shared-kernel classification [PROVEN]
> **[PROVEN] (`CRYPTID_KERNEL.md`, `kernel_classification.py`).** For `μ = 2^a/3^b` in lowest terms with
> single-prime denominator `p` (`v_p(μ) = −1`), `T_μ(x) = ⌊μx⌋` is a **clean `p`-to-1, Haar-measure-preserving,
> exact endomorphism of `ℤ_p`**, and its induced (renewal) map is **full-branch piecewise-affine expanding
> (slopes `μ^g`) with a `ℤ_p` fixed point on every branch**. `[VERIFIED]`: `3/2, 5/2, 7/2, 27/2` (`p=2`) and
> `8/3, 4/3, 16/3, 2/3` (`p=3`) all clean `p`-to-1; the `v_p = −2` controls (`9/4, 16/9, 27/4, 25/4`) are NOT
> clean (mixed multiplicities). So `v_p(μ) = −1` is *exactly* the clean regime. Fixed-point-on-every-branch
> `[VERIFIED]` 8/8 for both primes.

### 4.2 The Antihydra induced map is exact Bernoulli [PROVEN new theorem]
The GAP LEMMA collapses Antihydra's orbit to its induced odd map.

> **GAP LEMMA [PROVEN].** For odd `c`, `D := v₂(3c − 1)`; the number of steps to the next odd value is
> *exactly* `D`. (`[VERIFIED]` to `N = 10⁵`, zero exceptions.) Induced odd map:
> `T(o) = 3^{D−1}(3o − 1)/2^D`, `D = v₂(3o − 1)`, started at `o₀ = 27`.

> **[PROVEN new theorem] (`INDUCED_MAP` E4).** `T` is **Haar-measure-preserving, exact, and Bernoulli on the
> odd 2-adic units `ℤ₂*`**, with gap exponents `D_j` **i.i.d. geometric** `P(D = d) = 2^{−d}` (mean `2`).
> *Sketch.* Partition `ℤ₂*` by cylinders `A_d = {o : v₂(3o−1) = d}`, each Haar `2^{−d}`. On `A_d`, `T` is
> affine with 2-adic Jacobian `2^d`, mapping `A_d` bijectively onto all of `ℤ₂*` (the `3^{d−1}` factor is a
> unit, Jacobian 1). Full-branch surjectivity ⇒ full one-sided shift on `{d}` with weights `2^{−d}` ⇒
> exact/Bernoulli, `D_j` i.i.d. geometric. (Cites Lagarias 2-adic conjugacy, Bernstein–Lagarias 1996,
> Matthews–Watts.)

**Consequence [PROVEN].** Under Haar, `mean D = Σ_d d·2^{−d} = 2 > 3/2`, so the kernel inequality holds for
Haar-a.e. point with room to spare (CLT + exponential large-deviation concentration of even-density at `1/2`).
The entire remaining problem is whether the single orbit `o₀ = 27` is **Haar-generic** for `T`.

### 4.3 The reduction chain and its bridges [PROVEN]
A sequence of `[PROVEN]` equivalences carries the halting question down to a one-sided single-orbit density
statement (`COMPLETE_PROOF_CAPSTONE.md` §2):

| Form | Statement | Bridge `[PROVEN]` |
|---|---|---|
| (i) | even-density of `c`-orbit (`c₀=8`) `≥ 1/3` | renewal identity ↔ (ii) |
| (ii) | `mean D ≥ 3/2` along `o₀=27`, `D=v₂(3o−1)` | `mean D = Σ_k freq(o≡3⁻¹ mod 2^k)` ↔ (iii) |
| (iii) | `freq(D≥2)+freq(D≥3) ≥ 1/2`; tight: `freq(o≡3 mod4) ≥ 1/2` | residue arithmetic ↔ (iv) |
| (iv) | `freq(D=1) = freq(o≡1 mod4) ≤ 1/2` | ergodic-opt ↔ (v) |
| (v) | the orbit's Cesàro empirical measure does not concentrate on `D=1` near the fixed point `o=1` | meta-theorem (Thm 3) |

- **Renewal identity [PROVEN]** (Link 2): even steps are renewal points; `(mean gap)·(even-density) ≡ 1`
  (Kac) ⇒ even-density `= 1 − 1/(mean D)`, so even-density `≥ 1/3 ⟺ mean D ≥ 3/2`. `[VERIFIED]`
  `mean D ≈ 1.9989`.
- **Exact valuation formula [PROVEN]** (Link 3): `3` a 2-adic unit ⇒ `D ≥ k ⟺ o ≡ 3⁻¹ (mod 2^k)`, so
  `mean D = Σ_{k≥1} freq(o ≡ 3⁻¹ mod 2^k)`.

### 4.4 The GAP / Countdown / Dual-Repulsion lemmas [PROVEN]
- **GAP LEMMA** (above): odd-run length `= v₂(3c−1)` exactly.
- **Countdown Lemma [PROVEN]** (`MINPROP` F2). With `φ(o) = v₂(o − 1)`, each `D=1` step decrements `φ` by
  exactly 1; hence `m` consecutive `D=1` steps `⟺ o_start ≡ 1 (mod 2^{m+1})` (a thin cylinder of measure
  `2^{−(m+1)}`); any maximal `D=1` run has length `v₂(o_start − 1) − 1`. Runs are **self-limiting**: an
  infinite `D=1` run occurs only at the off-orbit fixed point `o = 1`. `[VERIFIED]`: all 75139 runs of the
  `o₀=27` orbit match, longest `= 19`, zero exceptions.
- **Dual-Repulsion Lemma [PROVEN]** (`ADELIC_KERNEL` G3). On each `D=1` step `o'−1 = (3/2)(o−1)` exactly, so
  `|o−1|_∞ ×3/2`, `|o−1|_2 ×2`, adelic product `×3`. The halting fixed point `o=1` is simultaneously repelling
  in both valuations. `[VERIFIED]` 300174/300174 steps.
- **v₃ identity [PROVEN]**: `v₃(o_{j+1}) = D_j − 1` (`[VERIFIED]` 0 exceptions over `2·10⁵` steps); a relabel
  (3-adic dual provably isomorphic to the 2-adic wall), not a reduction.

### 4.5 The `ψ = f(D)` lemma [PROVEN] — FIX #1 (closed)
This promotes a previously `[verified]`-numerical fact (`MINPROP` F3 recorded "ψ a function of D only,
0 mismatch for `o < 2·10⁶`") to an elementary `[PROVEN]` lemma, making `β` airtight. Let
`ψ := 1{o≡1 mod4} − 1{o≡3 mod8} − 1/2` be the one-sided test function (Thm 3).

> **Lemma (ψ is a function of D) [PROVEN].** For odd `o`, with `D = v₂(3o − 1)` and `3⁻¹ ≡ 3 (mod 8)`:
> - `D = 1 ⟺ o ≡ 1 (mod 4)`,
> - `D = 2 ⟺ o ≡ 7 (mod 8)`,
> - `D ≥ 3 ⟺ o ≡ 3 (mod 8)`.
>
> Consequently `ψ = +1/2` (when `D=1`), `−1/2` (when `D=2`), `−3/2` (when `D≥3`) — i.e. `ψ` is a pure
> function of `min(D, 3)`, hence of `D`.
>
> *Proof.* `D ≥ k ⟺ 3o ≡ 1 (mod 2^k) ⟺ o ≡ 3⁻¹ (mod 2^k)` since `3` is a 2-adic unit. With `3⁻¹ ≡ 3 (mod 4)`
> and `3⁻¹ ≡ 3 (mod 8)`: `D ≥ 2 ⟺ o ≡ 3 (mod 4)` (so `D=1 ⟺ o ≡ 1 mod 4`); `D ≥ 3 ⟺ o ≡ 3 (mod 8)`; and
> `D=2 ⟺ (o ≡ 3 mod 4) ∧ (o ≢ 3 mod 8) ⟺ o ≡ 7 (mod 8)`. Each residue class fixes `min(D,3)`, and `ψ` is
> constant on each, taking the same value `−3/2` for all `D ≥ 3`. ∎

`[VERIFIED]` this session: the three residue equivalences hold for all odd `o < 2·10⁵`, and
`3⁻¹ ≡ 3 (mod 8)`. This elementary lemma is what makes the `β = +1/2` computation of Theorem 3 airtight (no
numerical residue remains in the load-bearing chain).

### 4.6 Periodic-itinerary exclusion (the bisection) [PROVEN]
> **C3 [PROVEN]** (`WALL_B_DEEP`). The parity coding is injective; a period-`q` cycle of `T` has closed form
> `c₀ = N/(3^q − 2^q)` with `N ≤ 3^q − 2^q`, so **every cycle point lies in `[0,1]` and the only integer
> cycle points are `{0,1}`**. Since the integer orbit is strictly increasing (`T(c)−c = ⌊c/2⌋ ≥ 1`), it
> reaches no cycle ⇒ Antihydra's itinerary is **not eventually periodic** (no equidistribution assumed).
> `[VERIFIED]`: all 2046 cycles of period `q ≤ 10` enumerated. This bisects the exceptional set into
> structured/periodic (now killed) ⊔ aperiodic/full-complexity (= the kernel).

---

## 5. Theorem 3 [PROVEN for Antihydra] — the density ergodic-optimization barrier

This is the strongest no-structure-only result in the program. **It is `[PROVEN]` for Antihydra ONLY**
(o10-inner `[CONDITIONAL]`; o18/o15 do NOT get it — they are existence facet, §7). The audit's FIX #2 and
FIX #4 are baked in below.

### 5.1 The airtight core (FIX #2)
> **[PROVEN, standard theory].** A one-sided bound holding for **all** orbits is equivalent to
> `β(ψ) := max_{T-invariant μ} ∫ ψ dμ ≤ 0` (Mañé / Conze–Guivarc'h / Bousch sub-action / ergodic
> optimization). The mathematically airtight core has two halves:
>
> 1. **The all-orbits inequality is FALSE.** `β(ψ) = +1/2 > 0`, attained at the **fixed point `o = 1`**
>    (`T(1)=1`, `D=1` forever ⟹ even-density `0` ⟹ a genuinely **halting** orbit). The maximizer is the
>    atom `δ₁`, with `ψ(1) = +1/2` (by the §4.5 lemma). Because `o = 1` is a real halting orbit, the
>    universally-quantified statement "all orbits non-halt" is **false** — so the target is **irreducibly
>    orbit-27-specific**, not all-orbits. (The full `β` value rides on the full-shift/SFT structure where
>    `β = max_d ψ(d) = ψ(1) = +1/2`; with `ψ` a finite-coordinate function on a full shift, this is the
>    *well-understood* case of ergodic optimization, more rigorous than the generic case.)
> 2. **Machine-checked LP infeasibility.** The coboundary/Lyapunov LP `ψ(o) ≤ g(T(o)) − g(o)` is solved with
>    exact `Fraction` arithmetic and is **INFEASIBLE for every `k = 3..12`**, the dual obstruction being the
>    `o=1` self-loop of weight `+1/2` (max-mean-cycle `= +1/2` for all `k`). Tail truncation audited sound
>    (undetermined residues are all `D≥3`, `ψ=−3/2`, handled conservatively, 0 violations); infeasibility is
>    driven by the determined `+1/2` self-loop, tail-independent.

The Haar `1/4` slack is irrelevant: feasibility is set by `max_μ` (the atomic maximizer `δ₁`, value `+1/2`),
not by Haar (value `−1/4`).

> **FIX #2 labelling discipline (enforced).** The **airtight `[PROVEN]` core** is exactly (1)+(2): the
> all-orbits inequality is *false* (witnessed by the halting fixed point `o=1`, `β(ψ)=+1/2>0`), and the LP is
> machine-checked infeasible for `k=3..12`. The broader reading **"no structure-only proof of non-halting can
> exist"** is a **sound META-level statement** relative to a *stated* proof class (proofs using only
> `T`-invariant / all-orbits Lyapunov data) — **NOT** an unconditional theorem about all conceivable proofs.
> It is presented as such.

### 5.2 The second derivation (shared free structure)
> **[PROVEN] (`UNITPART` I4).** "Free" = pathwise-determined by the base symbol sequence, genericity-
> independent (the 3-adic fiber contraction `Φ_D(x) = 3^{D−1}2^{−D}(3x−1)`, rate `≤ 1/3`; the synchronization
> `o_j mod 3^k = f(`recent `D`-history`)`, depth `L ≈ k/2`; every unit-part observable). The halting fixed
> point `o = 1` (`D ≡ 1`) **synchronizes under the very same free contraction** as the real orbit
> (`[VERIFIED]`). Hence any free condition also holds at `o=1`; since `o=1` halts, **no free/structure-only
> condition can imply non-halting.** The free part is blind to `freq(D≥2)` — the sole halting/non-halting
> discriminator. Supporting `[PROVEN]`: the 3-adic contraction is real but **orthogonal to the target** (it
> contracts in the 3-adic place while `D` is read off the 2-adic place); `MI(`free 3-adic data; `D_j) = 0`
> (shuffle-null); the dynamics route free data and the hard target into two CRT-independent coordinates joined
> only by a null channel.

The two meta-theorems are the **same obstruction seen twice** — via the invariant simplex (maximizer = atom
`δ₁`) and via the free/contraction algebra (free structure shared with `o=1`). The split is exact: the
finite-window/free part carries no halting information (shared with `o=1`); the distinction lives **only** in
the tail-average (genericity) = the AEV/Mahler kernel. This is *why* every structural attack (contraction,
bootstrap, van der Corput, Mauduit–Rivat, twisted RPF, residue, coboundary, adelic coupling) only *relocated*
the gap.

### 5.3 Exact scope (FIX #4)
> **[PROVEN for Antihydra]** the density `β>0` barrier holds with `β = +1/2` at a **genuine halting integer
> fixed point `o=1`** — the sharpest form (the maximizer is a single, literally-halting orbit). **This is the
> only family-wide no-structure-only result that is `[PROVEN]`, and its PROVEN scope is Antihydra ONLY.**
> - **o10-inner**: `[CONDITIONAL]` (the inner `3/2` kernel carries the same minimal-renewal fixed point ⇒
>   `β>0`, but o10-FULL is composite and OUT; the criterion is for the inner sub-orbit only).
> - **o18 / o15**: do **NOT** get this barrier. Their halt facet is **existence**, not density; there is **no
>   `β`** (see §7). Putting them under the density `β` was a mislabel, **RETRACTED** (`UNIFIED_LIMIT_THEOREM.md`
>   correction banner; `SESSION_2026-06-28_REDUCTIONS.md`).
> - **o10-FULL**: OUT (probabilistically halts).
> - **o17**: kernel-less (no expanding induced map, no renewal-density extreme).

---

## 6. Theorem 4 [PROVEN] — the certification-complexity hierarchy

A conjecture-free, machine-checked descriptive theory of which **certificates** can witness non-halting. A
certificate is a config set `L` with (S) start `∈ L`, (C) `L` step-closed, (H) no halt config `∈ L`;
`reachable(start)` is always one, the question is whether a *describable* one exists (`LIMIT_THEOREM.md`).

### 6.1 Five strict separations [PROVEN], each with an explicit simulation-verified witness

| separation | witness TM | status | note |
|---|---|---|---|
| **star-free ⊊ REG** | parity counter `1RB0LZ_1LC1RA_0RA0LC` (brick d) | **[PROVEN]** conjecture-free | gap = the modular-counting group language `(11)*1` (syntactic monoid `ℤ/2`); the whole star-free interval (definite/SLT/LT/PT) collapses onto SLT for certification (Lemma A) |
| **REG ⊊ SLIN** | EQ machine `eq_machine.py` (brick a) | **[PROVEN]** conjecture-free | pumping forces an unequal block (halt) into any regular halt-free superset; reachable is semilinear |
| **SLIN ⊊ 2-automatic** | POW2W `S={2ⁿ}` (brick e) | **[PROVEN]** | lower half airtight (AP/pigeonhole); upper half cites Büchi–Bruyère (standard) |
| **2-automatic ⊊ CF** | PALW binary palindromes (brick g) | **[PROVEN]** | lower half airtight (palindromes non-regular); upper half standard CF |
| **CF ⊊ CS** | SQW `S={n²}` (brick f) | **[PROVEN]** | **depends on external arXiv:1901.03913** (non-linear poly range ∉ CF) + LBA; cite as input, not self-contained |

Standing tower:
```
 star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ context-free ⊊ context-sensitive ⊊ … ⊆ beyond (Collatz)
   └(d)parity ℤ/2┘ └(a)EQ┘ └(e)POW2W{2ⁿ}┘ └(g)PALW palindromes┘ └(f)SQW{n²}┘   └(cryptids:OPEN)┘
```

- **Squeeze Lemma [PROVEN].** For a check-`S`-every-cycle machine, every step-closed halt-free certificate has
  CS-value-set exactly `S`; so the minimal certificate class for `M` equals the descriptive class of `S`. This
  is the engine behind (e)/(f)/(g). Airtight.
- **REG suffices at n=3 [PROVEN].** All 63 three-state monsters have explicit REG certificates (63 explicit
  certificates) — a clean finite theorem; the hierarchy does not separate at `n=3`.
- **Above CS [PROVEN but non-explicit]:** `CS ⊊ recursive` holds by the Space Hierarchy Theorem but its
  witness is diagonalization (loses the small-explicit-TM character); `recursive ⊊ arithmetic` holds as
  classes but is **not** Squeeze-witnessable. Honestly flagged.

This unit is **the most complete and most standalone** part of (B): conjecture-free, machine-checked,
orthogonal to the cryptids; the only outside dependency is brick (f)'s arXiv:1901.03913.

### 6.2 The subword-complexity floor [PROVEN]
For Antihydra's parity sequence `r_n = c_n mod 2` with subword complexity `p(ℓ)` (`LIMIT_THEOREM.md` §3″):
- coding bijection `p(ℓ) = #{c_n mod 2^ℓ}`: **[PROVEN]** (`[VERIFIED]` `ℓ≤14`);
- not eventually periodic (transience): **[PROVEN]** conjecture-free ⇒ `p(ℓ) ≥ ℓ+1` (Morse–Hedlund);
- not Sturmian (`p(2)=4>3`): **[PROVEN]**;
- linear floor `p(ℓ) ≥ (ℓ−3)/log₂(3/2) ≈ 1.71ℓ` (slope `log_{3/2}2` matching Dubickas 2009): **[PROVEN]**;
- lift bound `p(ℓ) ≤ p(ℓ+1) ≤ 2p(ℓ)`: **[PROVEN]**;
- ceiling `p(ℓ) = 2^ℓ ⟺ single-orbit equidistribution = Mahler/AEV`: **[OPEN]** (correctly labelled).

> `eventually-periodic ⊊ Sturmian ⊊ [PROVEN] p(ℓ) ≥ 1.71ℓ ⊊⊊ [Mahler/OPEN] p(ℓ) = 2^ℓ`.

A second, independent proven floor under the OPEN cryptid vertex, on an axis orthogonal to §6.1.

### 6.3 Per-machine certificate floors [PROVEN]
- **o18 floor `m*=2` [PROVEN]** conjecture-free, machine-checked: no 2-window (SLT) certificate exists
  (reachable's 2-grams `{(1,D),(D,1)}` force the halt-reaching `1[D]1` into any 2-window superset; `c=1[D]1`
  halts in 2 steps). `m ≥ 3` is **[OPEN]** — the discriminator is head-local (a 3-window gates it)
  (`O18_NO_CERTIFICATE.md`).
- **o17 floor `m*=8` [PROVEN]** conjecture-free, machine-checked: no m-window certificate exists for `2 ≤ m ≤ 8`
  (the trivial halter `A 0 1^k` lies in the tight over-approximation `L*_m` and halts). `m ≥ 9` is **[OPEN]** —
  the binding gram `0 A 0 1^6` is absent from reachable (state A reads `0` only with left-0-run `∈ {0,∞}`;
  ∞-frontier right-1-run `≤ 5`), so the family detaches from reachable's window set (`O17_REG_BARRIER.md`).
  **The prior all-k/REG over-claim is RETRACTED.**
- **o15**: FAR HOLDOUT; no proven floor barrier beyond the shared head-local picture.

### 6.4 The all-k / REG principle — one direction proven, converse conjectured (FIX #3)
> **One direction [PROVEN] (the brick-(d) mechanism).** If a cryptid's halt discriminator lives in an
> **unbounded reachable run** (so an embedded halter family is window-equivalent to reachable for *every* `m`
> while its halting pattern is not eventually constant / not regular), then no `m`-window (resp. REG)
> certificate exists — this is the brick-(d) all-or-nothing construction. The parity counter realizes it (floor
> `∞ /` all-`k`), but it is a *counter* with a known REG certificate, not a cryptid.
>
> **Converse [CONJECTURE, NOT a theorem].** The full statement *"a cryptid gets an all-k/REG barrier **iff**
> its halt discriminator lives in an unbounded reachable run"* is **NOT proven as an iff**. It is a
> *characterization* supported by three data points (o18 floor 2, o17 floor 8, brick-d `∞`); the `⟸` direction
> is the proven brick-(d) construction, the `⟹` converse is conjectured. (FIX #3.)

> **[OPEN] No REG / tame certificate for a cryptid.** Strictly stronger than "reachable language non-regular"
> (a REG certificate is an over-approximation `L ⊇ reachable`, and a regular superset of a non-regular set can
> exist). Both BB(6) existence cryptids o18/o17 have only **finite-floor** barriers (`m*=2`, `m*=8`); neither
> reaches REG. The REG vertex is **at least as hard as resolving the cryptid** and stays `[OPEN]`. The only
> top-level `[PROVEN]` no-structure-only barrier in the whole family is **Antihydra's density `β>0`** (§5).

### 6.5 The spoofer game (the genuineness avatar) [framing]
Certification is a two-player game: the Prover commits to a finite abstraction `α` claiming it certifies
non-halting; the Adversary must exhibit an `α`-indistinguishable machine that halts. For bouncers/counters the
Prover wins in REG (§6.1, `n=3`); for the cryptids the Adversary appears to win against every finite-state
Prover — the `[OPEN]` claim. This is the TM avatar of the quantum genuineness-limit theorem (finite
observation cannot certify the infinite property), on a fully-specified discrete object.

---

## 7. The frontier catalogue

Classifying each analyzed Collatz-core cryptid by **facet** (density / existence), **kernel** (AEV/Mahler
multiplier or none), **halt discriminator** (locality), and **proven barrier status**. (`bb_sim`-verified
specs; kernel placements from `CRYPTID_KERNEL.md`; barriers from `O17_REG_BARRIER.md`,
`O18_NO_CERTIFICATE.md`, §5.)

| machine | facet | kernel `q` (`μ`, `p`) | halt discriminator | **proven barrier** | over-approx / REG |
|---|---|---|---|---|---|
| **Antihydra** | **density** | **q=2** (`μ=3/2`, `p=2`) | head-local (balance read at F) | **`β>0` `[PROVEN]`** — all-orbits density certs blocked | `[OPEN]` |
| **o10** (inner) | density/existence (coupled) | **q=2** (`μ=3/2`, `p=2`; literal AEV-1.6 ceiling) | head-local | none on existence axis; inner `β>0` `[CONDITIONAL]` | `[OPEN]` |
| **o15** | existence | **q=3** (`μ=8/3`, `p=3`; Erdős ternary) | head-local (A-frontier collision; block-decomp parity-irregular but halt is a local read) | none proven | `[OPEN]` (Erdős wall) |
| **o18** | existence | **q=3** (`μ=8/3`, `p=3`; Erdős ternary) | **head-local** (adjacent-`11`, 3-window) | **no 2-window `[PROVEN]`; floor `m*=2`** | `[OPEN]` (`≥3` head-local) |
| **o17** | existence (shaped) | **none** (uniquely-ergodic odometer; equidistribution automatic) | non-local-in-block-length but **bounded-frontier** (`k mod 3` + Collatz, `≤5`-cell tail) | **no m-window for `m≤8` `[PROVEN]`; floor `m*=8`** | `[OPEN]` (family detaches `m≥9`) |

**Two obstruction types in the BB(6) Collatz core** (confirmed): an **equidistribution kernel** (Antihydra,
o10-inner = AEV q=2 `μ=3/2`; o15, o18 = AEV q=3 `μ=8/3`/Erdős) whose hardness is single-orbit `⌊μⁿ⌋ mod p`
equidistribution (the shared Mahler vertex), versus **one odometer outlier o17** (no kernel; Collatz-irregular
halt predicate). On the certificate axis the existence cryptids have **finite-floor** barriers only (floors
`0/0` for o15/o10-existence, `2` for o18, `8` for o17), never REG. The only top-level proven no-structure-only
barrier in the family is **Antihydra's density-axis `β>0`**.

### 7.1 The two-facet / two-axis structure [PROVEN organizational framework]
The "unified theorem" is **two barriers on two `LIMIT_THEOREM.md` axes**, not one:

| | density version | existence version |
|---|---|---|
| halting object | tail average drops below `θ` (non-clopen limit event) | orbit hits clopen `H` |
| structure-only proof | all-orbits one-sided inequality | forward-invariant `L ⊇ orbit`, `L∩H=∅` |
| obstruction type | invariant **measure** (`β = max_μ`) | invariant **set** (descriptive complexity) |
| does a halting orbit block it? | **YES** — `δ_{y_*}` is in the `max`, forces `β>0` `[PROVEN]` | **NO** — a set excludes `y_*` `[PROVEN negative]` |
| barrier status | **`[PROVEN]`** (Bousch ergodic optimization) — **Antihydra only** | **`[OPEN]`** (= the over-approximation top) |
| LIMIT_THEOREM axis | dynamical / ergodic | over-approximation / descriptive |

The crucial asymmetry (`EXISTENCE_META_THEOREM.md` §2): a density all-orbits inequality must account for
**every** invariant measure including the atom `δ_{y_*}` at the halting orbit (ergodic optimization is a
`max_μ`), so a halting orbit *forces* `β>0`. But an existence structure-only proof is a forward-invariant
**set** `L`, and **a set can simply exclude `y_*` and all of `H`** — so the mere existence of a halting orbit
does **not** block an avoidance certificate. Hence the existence barrier is `[OPEN]`, equal to
`LIMIT_THEOREM.md`'s over-approximation top.

### 7.2 The completed 19-cryptid frontier catalogue `[VERIFIED]`

End-to-end classification of the whole BB(6) Collatz frontier (the 19 cryptids; the named machines below),
consolidating `SESSION_2026-06-28_CATALOGUE_COMPLETE.md` and the per-machine deep dives
`CATALOGUE_{O2_O5, O7_O12, O13_SN}.md`. Every multiplier, facet, and halt discriminator below is
`bb_sim`-cross-checked `[VERIFIED]` this program (exact big-int simulation); **no machine is decided** — all are
**HOLDOUT** under every sound decider (`far_dfa` m≤8, `far_finder` k≤7, `far_cegar` 80–120 rounds). The
*proven barriers* are exactly those already established above (Antihydra `β>0`, §5; the o18/o17 certificate
floors, §6.3); no new barrier is claimed.

| machine | `μ` | `p` | facet | regime (`p<q²` hard / `p>q²` easy) | proven barrier | class |
|---|---|---|---|---|---|---|
| **Antihydra** | `3/2` | `2` | **density** q=2 | hard (`3<4`) | **`β>0` `[PROVEN]`** (only) | Mahler `3/2` density |
| o2 | `3/2` `[VERIFIED]` | `2` | existence q=2 | hard (`3<4`) | none proven | Mahler `3/2` (nested) |
| o7 | `3/2` `[VERIFIED]` | `2` | existence q=2 | hard (`3<4`) | none proven | Mahler `3/2` family |
| o8 | `3/2` `[VERIFIED]` | `2` | existence q=2 (nested) | hard (`3<4`) | none proven | Mahler `3/2` nested |
| o10-inner | `3/2` | `2` | composite (inner clean) | hard (`3<4`) | inner `β>0` `[CONDITIONAL]` | inner clean; **o10-FULL OUT** (prob. halts) |
| **Space Needle** | **`5/2`** `[VERIFIED]` | `2` | existence q=2 | **easy (`5>4`)** | none proven | **Mahler `5/2` (new)** |
| o18 | `8/3` | `3` | existence q=3 | hard (`8<9`) | no 2-window `[PROVEN]`; floor `m*=2` | Erdős ternary |
| o15 | `8/3` | `3` | existence q=3 | hard (`8<9`) | none proven (FAR HOLDOUT) | Erdős ternary |
| **o4** | **`4/3 = 2²/3`** `[VERIFIED]` | `3` | existence q=3 | hard (`4<9`) | none proven | **Erdős ternary (new)** |
| **o5** | **`4/3 = 2²/3`** `[VERIFIED]` | `3` | existence q=3 | hard (`4<9`) | none proven | **Erdős ternary (new)** |
| o3 | — (kernel-less) | — | existence | n/a | none proven | bounded-alphabet odometer (o17-type, runs ≤6) |
| o17 | — (odometer, `≈×8`) | — | existence (shaped) | n/a | no `m`-window `m≤8` `[PROVEN]`; floor `m*=8` | kernel-less odometer |
| o11 | irregular (`3,9,26,303`) | — | — | n/a | none proven | too irregular (T2 `(10)*`-collapse) |
| o12 | irregular (`4,10,28,370`) | — | — | n/a | none proven | too irregular (T2 `(10)*`-collapse) |
| o13 | irregular (block-swap) | — | existence | n/a | none proven | too irregular (T1 two-counter) |
| o14 | irregular (block-swap) | — | existence | n/a | none proven | too irregular (T1 two-counter) |
| o16 | irregular (defect peak) | — | existence | n/a | none proven | too irregular (T2 single-defect) |

**The convergence `[VERIFIED]`.** The BB(6) Collatz core resolves into **three structural strata**:
1. **Expanding-kernel `{μ : v_p(μ) = −1}` — a complete catalogue of four named Mahler/Erdős multipliers**
   `{3/2, 5/2 (p=2); 4/3, 8/3 (p=3)}`. Every member's halt is a single-orbit `⌊μⁿ⌋ mod p`
   equidistribution / carry-avoidance event = the shared AEV/Mahler vertex (§8). The only `[PROVEN]`
   no-structure-only barrier in the whole stratum is **Antihydra's density `β>0`** (§5); all other members are
   existence-facet with no proven barrier (their barrier is the `[OPEN]` over-approximation top, §7.1).
2. **Kernel-less odometers** (o3, o17): no expanding `T_μ`, bounded local content; hardness is a
   Collatz-irregular carry/halt predicate, **not** equidistribution. o17 carries the highest certificate floor
   (`m*=8`, §6.3); o3 is the tamest (runs ≤6) but still HOLDOUT.
3. **Too-irregular machines** (o11–o14, o16): regular `~√t` width envelope hiding irregular geometric content
   with **no clean scalar `2^a/3^b` map** over the observed epochs — `[OPEN]`, no exact reduction extracted yet.

**The `p<q²` / `p>q²` regime note `[VERIFIED]/[OPEN]` (tractability flag).** Writing each multiplier in lowest
terms as `μ = p/q` (here `p =` **numerator**, distinct from the prime-denominator `p` of `v_p(μ) = −1` — `q` is
that prime), AEV Thm 1.5 connects the conjecture to Mahler's 1968 problem precisely in the **hard regime
`p < q²`**. Three of the four multipliers are hard: `3/2` (`3<4`), `4/3` (`4<9`), `8/3` (`8<9`). The new
**`5/2` is the lone easy case `p > q²` (`5 > 4`)** — and the easy regime is structurally *different*: the
arguments that organize the `3/2`-cluster (and the AEV `p<q²` ⇒ Mahler bridge) **break in the `p>q²` regime**
(`FRESH_ANGLES_SCOUT.md`, `SESSION_2026-06-28_CATALOGUE_COMPLETE.md`). So **`5/2`'s tractability may differ**
from the other three — flagged here, `[OPEN]` whether this helps or hurts. (Full Space Needle derivation:
`CATALOGUE_O13_SN.md` §1.)

---

## 8. The open kernel — AEV/Mahler equivalence [OPEN]

After all `[PROVEN]` reductions, per-cryptid completion (result (A)) rests on exactly one named open
statement, in two facets of the same AEV instance family.

> **Kernel (density facet, q=2). [OPEN].** For the induced 3/2-Syracuse orbit `o₀ = 27`:
> `liminf_{N→∞} (1/N) #{ n < N : D(o_n) ≥ 2 } ≥ 1/2`. Equivalently `mean D ≥ 3/2`; `liminf` even-density of
> `c₀=8` `≥ 1/3`; `liminf freq(o ≡ 3 mod 4) ≥ 1/2`; 3-adic form `density{3 | o_j} + density{9 | o_j} ≥ 1/2`.

> **Kernel (existence facet, q=3). [OPEN].** For o18/o15: the orbit of `x₀` under `⌊(8/3)x⌋` on `ℤ₃` avoids the
> clopen carry-alignment set `H` forever — the `q=3` single-orbit floor-mirror **existence/Erdős** fragment of
> AEV Conj 1.6 (`EXISTENCE_META_THEOREM.md` §4.4), needing an effective equidistribution rate beating a
> *summable* target.

> **Conditional theorem [PROVEN reduction] (`KERNEL_FINAL.md` §2).** Antihydra does not halt **iff** the
> density kernel holds **together with** the finite check `balance_n ≥ 0` for `n ≤ N₀`. Under Haar (`T` exact,
> `mean D = 2`, `[PROVEN]`) the kernel holds with room to spare; the whole problem is whether the single orbit
> `o₀ = 27` is Haar-generic.

**Exact literature placement [PROVEN/verified].** The kernel is the **`p/q = 3/2`, one-sided, single-level
(`k=2`), single-orbit floor-mirror fragment of the Andrieu–Eliahou–Vivion (2025) normality conjecture**
(arXiv:2510.11723, Conj 1.6). AEV Thm 1.7 gives Conj 1.6 ⇔ their normality Conj 1.2; AEV Thm 1.5 gives (for
`p < q²`, which holds at `3/2`) Conj 1.2 ⇒ **Mahler's 1968 Z-number conjecture**. So AEV is the single umbrella
above the entire 3/2 cluster (Mahler 1968, Flatto Z-numbers, Akiyama 2008, Dubickas–Mossinghoff 2009), and the
kernel is one instance under it. Calibrations: AEV uses the *ceiling* `(3x+1)/2`, Antihydra the *floor*
`(3x−1)/2` (the `±1` flips parity; **not** positive-to-positive conjugate; the floor↔ceiling relation is
resolved exactly in §8.1; GAP-LEMMA `v₂(3o−1)` is the bridge) — the kernel is
the **floor-mirror**. The kernel is strictly weaker than AEV on three axes (one-sided vs two-sided; level `k=2`
vs all `k`; single orbit vs all `n`), **yet no named conjecture sits at this weaker level** — AEV is the
weakest named established-open conjecture that implies it.

### 8.1 The floor-mirror bridge [PROVEN] — gap #1 closed (`FLOOR_MIRROR_CONJECTURE.md`, `SESSION_2026-06-29_FLOOR_MIRROR.md`)

The earlier "floor-mirror" calibration carried an honest caveat: the cryptids run the **floor** map
`Tf(x) = ⌊3x/2⌋`, while AEV Conj 1.6 is stated for the **ceiling** `Tc(x) = ⌈3x/2⌉`, and the `±1` parity flip
left it `[OPEN]` whether the floor-mirror conjecture was a *formally distinct* open problem from literal AEV.
This gap (**"gap #1"**) is now **closed by an exact conjugacy** — the floor-mirror conjecture is the **same**
named conjecture as AEV 1.6(3/2), not a new one.

> **Negation-conjugacy lemma [PROVEN].** Let `R(x) = −x` on `ℤ` (equivalently on `ℤ₂`). Then
> `Tc = R ∘ Tf ∘ R`, i.e. **`Tc(x) = −Tf(−x)` for every `x ∈ ℤ`.**
> *Proof.* `⌈y⌉ = −⌊−y⌋` for every real `y`; with `y = 3x/2`,
> `Tc(x) = ⌈3x/2⌉ = −⌊−3x/2⌋ = −⌊3(−x)/2⌋ = −Tf(−x)`. ∎

`R` is an involution, a Haar-measure-preserving homeomorphism of `ℤ₂`, and on each finite quotient `ℤ/2^k` it
acts as the residue permutation `r ↦ (−r mod 2^k)` (a measure-preserving bijection). Iterating,
`Tf^l(n) = −Tc^l(−n)` for all `l` `[PROVEN]`. Consequences:

- **Floor and ceiling equidistribution are equivalent, orbit-by-orbit [PROVEN].** Because `R` permutes `ℤ/2^k`
  bijectively, `(y_l)` equidistributes mod `2^k` **iff** `(−y_l)` does; combined with `Tf^l(n) = −Tc^l(−n)`,
  *the floor orbit of `n` equidistributes mod `2^k` ⟺ the ceiling orbit of `−n` equidistributes mod `2^k`* —
  an exact measure-preserving (topological+measurable) isomorphism of the two systems on `ℤ₂`, the strongest
  possible bridge (not merely "same difficulty").
- **The load-bearing statistic is literally identical [PROVEN] [VERIFIED].** At the induced-odd-map level, for
  odd `o` with `m = −o`: `3m+1 = −(3o−1)`, so `D'(−o) = v₂(3o−1) = D(o)` and `T'(−o) = −T(o)`. Hence the
  depth/gap sequences coincide exactly: **`D_l^{ceil}(−o₀) = D_l^{floor}(o₀)` for every `l`.** `[VERIFIED]`
  `200,000` induced steps, `o₀ = 27` (floor) vs `m₀ = −27` (ceiling), **0 exceptions**; `mean D` identical at
  `1.996270`, `freq(D≥2)` identical at `0.499660` (re-confirmed this session, `.venv` exact big-int). So
  Antihydra's entire load-bearing statistic is carried verbatim across the bridge.
- **The floor cryptids live under AEV 1.6(3/2) [PROVEN bridge / OPEN conjecture].** The floor-mirror
  conjecture FM(3/2) ("every orbit of `Tf(x)=⌊3x/2⌋` equidistributes mod `2^k`") is, on the full sign-symmetric
  domain `ℤ₂`, **literally equivalent** to AEV Conj 1.6(3/2) by the conjugacy above. The **bridge is `[PROVEN]`**;
  **FM(3/2) / AEV 1.6(3/2) itself remains `[OPEN]`** (finite `N` proves nothing about the `liminf`). So gap #1
  — "is the floor-mirror a separate open problem?" — is closed: the q=2 floor cryptids sit under the **one**
  named conjecture AEV 1.6(3/2).

> **Cosmetic seed-sign quantifier (stated honestly) [PROVEN-characterization / CONDITIONAL].** The conjugacy
> `R` maps **floor-positive orbits to ceiling-NEGATIVE orbits** (never positive→positive: on odds `Tc = Tf + 1`
> and the two positive orbits diverge like `(3/2)^l`, so no positive-only conjugacy exists). Thus the machines'
> positive floor orbits (e.g. Antihydra's `o₀=27`) correspond to *negative* ceiling seeds (`−27`), which lie
> outside AEV's *literally-stated* positive-only quantifier. Two equally sound readings: (i) adopt the natural
> **all-`ℤ₂` (sign-symmetric)** form of Conj 1.6 — under which AEV(3/2) and FM(3/2) are literally equivalent,
> `[PROVEN]`; or (ii) keep AEV's literal positive form — under which "AEV(3/2) ⟹ FM(3/2) at the machines' seeds"
> is `[CONDITIONAL]` on the (believed, unproven) negative-seed / sign-symmetry extension. The residual is
> **cosmetic** under the standard expectation that such equidistribution conjectures are sign-blind, but it is
> not discharged by the conjugacy alone and is flagged as `[CONDITIONAL]`.

### 8.2 The corrected 3/2-dominance [CONDITIONAL] — shared kernel, 2 exact + 8 through a nesting layer

With the bridge closed, the dominance headline ("the BB(6) Collatz core is essentially the single Mahler 3/2
problem") can be stated precisely — and **without over-claiming "one conjecture decides all ten"**
(`MAHLER_3_2_DOMINANCE.md` §2/§4, `SESSION_2026-06-29_FLOOR_MIRROR.md`):

> **Corrected dominance statement.** **All ten `μ=3/2` machines** — Antihydra, o2, o7, o8, o10-inner, o11, o12,
> o13, o14, o16 — **share the floor `⌊3x/2⌋` kernel** (o10-inner runs the literal AEV ceiling `⌈3m/2⌉`); via
> §8.1 they are all instances of the **one** named conjecture AEV 1.6(3/2). But the dependency is **not** "one
> conjecture decides all ten." Precisely:
> - **2 reduce exactly** (decided `[CONDITIONAL]` on AEV 1.6(3/2)): **Antihydra** (single-orbit, level-`k=2`,
>   one-sided **density** fragment at `o₀=27`; qualitative AEV **over-implies** it; plus the finite check
>   `balance_n ≥ 0`, `[VERIFIED]` to `n ≤ 2·10⁵`) and **o10-inner** (literal-ceiling inner sub-orbit; o10-FULL
>   composite/OUT).
> - **8 ALSO require an o10-FULL-grade nested-refill reduction** (`[OPEN]`): **o2, o7, o8, o11, o12, o13, o14,
>   o16**. Their clean `⌊3x/2⌋` law holds **only on an even-`a` inner subsequence**; the odd-`a` steps fire a
>   nested 2-adic halving-cascade **refill** (isomorphic to the o10-FULL two-level structure), and the halt
>   event is **coupled to the outer refill alignment**, not to a clean single `3/2` orbit. So even a full proof
>   of AEV 1.6(3/2) (floor-mirror included) does **not** by itself decide these eight — they need, in addition,
>   (a) their exact `2^k` valuation halt predicate **derived** (`[OPEN]`) and (b) for the existence-facet members
>   an **effective-rate** strengthening (stronger than qualitative AEV; §7.1).
>
> **Honest headline.** "All ten share the `⌊3x/2⌋` kernel; **2 reduce exactly** (Antihydra, o10-inner), **8
> through a nesting layer**." The in-scope exact-reduction set is therefore **unchanged at 4 machines**
> {Antihydra, o18, o15, o10-inner} (§3), of which **2 are the `3/2` density facet**. The attempt to extend the
> in-scope set across the eight `μ=3/2` machines returned **0/8** this session — every one is an o10-FULL-grade
> nested blocker (`SESSION_2026-06-29_FLOOR_MIRROR.md`, V2/V3; `REDUCE_O2_O7_O8.md`, `REDUCE_O11_O16.md`).

### 8.3 The nested-Collatz second structural class [VERIFIED] — in-family, not in-scope (cross-reference)

The eight blocked `μ=3/2` machines above, **together with o10-FULL**, form a **second structural class** — the
**nested-Collatz machines** (nine in all: o2, o7, o8, o10-FULL, o11, o12, o13, o14, o16). Their shared signature
`[VERIFIED]`: a clean inner `⌊3x/2⌋` engine running only on an inner (even-`a`) subsequence, wrapped in an
**outer doubly-exponential "refill"** layer, with the **halt event living in the outer-layer alignment** rather
than in the inner `3/2` orbit. This is exactly why they are **in-family by multiplier but not-in-scope by
proof**: the avoidance target is a *nested* map, not a clean `3/2` orbit, so even the full floor-mirror AEV
conjecture does not decide them. A newly-sharpened `[VERIFIED]` data point: **o13 is the exact structural twin
of o10** (a D→E eat-sweep that halts on an even-length run, the mirror of o10's odd-length leftward eat-sweep;
inner all-odd "safe" 7214/7214), with the *opposite* direction signal (o13 leans non-halting, o10 leans halting
~1/3-per-epoch) but only ~4 outer epochs reachable, so the per-epoch direction is `[OPEN]` for all nine. The
full per-machine treatment is in `REDUCE_O2_O7_O8.md` and `REDUCE_O11_O16.md` (consolidation designated for
`NESTED_COLLATZ_STRUCTURE.md`, not yet written); this paragraph is a pointer only. This class is **disjoint**
from the in-scope expanding-kernel core of §3 and from the kernel-less odometers (o3, o17, §7.2 stratum 2).

**Distinct from the support axis [PROVEN/verified].** Mahler's literal conjecture and the
Flatto–Lagarias–Pollington bound (`limsup − liminf ≥ 1/3`, 1995) are **support/spread** statements; the kernel
is a **frequency/density** statement. FLP's `1/3` and the kernel's `1/3` are numerically identical but on
**orthogonal axes** (which values are hit vs how often); an orbit can have full spread while its empirical
measure concentrates (the `δ₁`-drift permitted by §5). So **FLP is not a partial result toward the kernel**;
there is no published bridge from spread to density. Likewise Tao 2019 is a log-density-over-almost-all-seeds
ensemble theorem (no per-orbit output); Birkhoff averaging is empty (the integer orbit is transient, grows like
`(3/2)ⁿ`, no invariant probability measure).

**No analytic handle [OPEN].** AEV supports Conj 1.6 with combinatorics-on-words + numerics only — no ergodic
theory, transfer operator, exponential sums, or Fourier analysis, and **zero unconditional results at `3/2`**.
The lone candidate route is **effective power Fourier-decay** `|ν̂_{2/3}(t)| ≤ C|t|^{−a}` → Erdős–Turán →
`liminf` even-density `≥ 1/2 − O(decay)`. It is `[PROVEN]` (commit 984f70f) that `3/2` is **non-Pisot ⟹
`ν_{2/3}` is Rajchman** (Fourier transform `→ 0`), but the **annealed/quenched gap is the lone remaining
analytic missing link [OPEN]**: `ν̂_{2/3}`'s decay is *annealed* (i.i.d. weights), whereas the orbit's
even-density needs the *quenched* Weyl sum `Σ e(h·4·(3/2)ⁿ)`, which `ν̂_{2/3}` does not directly bound. AEV
itself does not cross this gap. (For the existence facet, the analog `[OPEN]` is an effective inhomogeneous
Diophantine / shrinking-target estimate = AEV q=3 Archimedean/Mahler facet; `(R3)` carry-run targets reduce to
it — the only unconditional bound `run_n ≤ k_n` coincides with the threshold, zero slack;
`SESSION_2026-06-28_CERT_HUNT.md` ②.)

> **Honest statement of (A)'s dependency.** Per-cryptid complete proofs are **[CONDITIONAL] on AEV/Mahler with
> NO shortcut.** Data analysis (`PATH_TO_COMPLETE_PROOF.md`) confirms there is no near-shortcut, partial
> result, or unactivated signal: the lone live lead is the quenched Weyl-sum cancellation `Σ e(h·4·(3/2)ⁿ)`,
> which *is* AEV/Mahler. The reduction itself is the unconditional contribution.

---

## 9. Unconditional fallback theorems

These hold **unconditionally** (no dependence on the open kernel) and are publishable standalone.

1. **The exact reduction theorem [PROVEN]** (Thm 1). Each in-scope cryptid's halting `=` a named `2^a/3^b`
   arithmetic event (Antihydra: `∃n: balance_n<0 ⟺ ∃n: v₂(c_n−1) ≥ balance_n+1`, via the GAP LEMMA induced map
   `T(o)=3^{D−1}(3o−1)/2^D`, `o₀=27`; o18/o15: base-3 carry alignment; o10-inner: `3/2` ceiling). Raw 6-state
   TM → named `p`-adic predicate. *The strongest standalone result.*
2. **The induced-map Bernoulli/exactness theorem [PROVEN]** (Thm 2). `T_μ` on `ℤ_p` is Haar-preserving, exact,
   Bernoulli for `v_p(μ)=−1`; for Antihydra `D_j` i.i.d. geometric `2^{−d}`, `mean D = 2`. *The second
   strongest standalone result.*
3. **Haar-a.e. non-halting [PROVEN, annealed].**
   - *Density (Antihydra):* Haar-a.e. 2-adic seed is non-halting (`mean D = 2 > 3/2` a.s., SLLN + LDP
     concentration of even-density at `1/2`).
   - *Existence (o18/o15):* Haar-a.e. seed is non-halting via **Borel–Cantelli I** (no independence:
     `Σ Haar(B_n) ≍ Σ (8/3)^{−n} = 1.54·10⁻⁴ < ∞`).
   - *Honest caveat:* annealed ≠ quenched; the actual seed (`o₀=27` / the o18/o15 seeds) is one Haar-null
     point, so this does **NOT decide any machine**.
4. **Not eventually periodic [PROVEN, conjecture-free]** (C3). The itinerary is not eventually periodic — the
   integer orbit is strictly increasing (`T(c)−c = ⌊c/2⌋ ≥ 1`) and reaches no cycle (only integer cycle points
   are `{0,1}`).
5. **Subword-complexity floor [PROVEN]** (§6.2). `p(ℓ) ≥ 1.71ℓ` (slope `log_{3/2}2`, matching Dubickas),
   non-Sturmian, not eventually periodic.
6. **No-structure-only meta-theorem [PROVEN, Antihydra]** (Thm 3, with FIX #2 precision). `β(ψ)=+1/2>0` at the
   halting fixed point `o=1`; LP infeasible `k=3..12`; free structure shared with `o=1`.

Plus the two existence-facet `[PROVEN]` components: the **closed-over-approximation lemma** (open `H` +
non-halting ⇒ orbit closure is forward-invariant and disjoint from `H`) and the **annealed Borel–Cantelli-I
avoidance** (item 3, existence). And the **descriptive certification hierarchy** (Thm 4) is entirely
unconditional.

---

## 10. What is genuinely new (BB6-specific) vs the inherited open problem

**BB6-specific contributions (all `[PROVEN]` unless noted):**
- **The induced-map identification** — Antihydra's halting is the exact, Haar-preserving, Bernoulli induced
  odd map `T(o)=3^{D−1}(3o−1)/2^D`, `o₀=27`, `D_j` i.i.d. geometric (Thm 2). Maximal localization; completes
  the measure side.
- **The exact reduction chain** non-halt `⟺` even-density `≥1/3 ⟺ mean D ≥ 3/2 ⟺` one-sided cylinder, via the
  renewal identity and valuation formula (Thm 1, §4.3).
- **The `ψ = f(D)` lemma** (§4.5, FIX #1) — promoted from numerical to elementary `[PROVEN]`, making `β`
  airtight.
- **The two meta-theorems** proving no structure-only proof exists for **Antihydra** (Thm 3): `β(ψ)=+1/2` at
  the halting fixed point and free-structure sharing with `o=1` — a genuinely new structural insight explaining
  *why every structural attack only relocated the gap*.
- **The arithmetic lemmas** (§4.4–§4.6): GAP, Countdown, Dual-Repulsion, v₃ identity, periodic-itinerary
  bisection C3.
- **The two-facet / two-axis classification and frontier catalogue** (§7): density (β-barrier `[PROVEN]`
  Antihydra) vs existence (over-approximation barrier `[OPEN]`; closed-over-approximation + Borel–Cantelli-I
  `[PROVEN]`); o17 kernel-less; o10-FULL OUT.
- **The certification-complexity hierarchy** (Thm 4): five strict conjecture-free separations with explicit
  witnesses + Squeeze Lemma + REG-suffices-at-n=3; two proven floors under the OPEN vertex (subword `1.71ℓ`;
  certificate `m*=2`, `m*=8`); the all-k/REG principle (one direction proven, converse conjectured).
- **Precise literature placement** of the kernel as the floor-mirror, triple-weakened fragment of AEV Conj 1.6
  (q=2 density / q=3 existence), with the support-vs-density (FLP) axis distinction made rigorous and the lone
  analytic route (effective Fourier rate) + its annealed/quenched obstruction identified.

**Inherited open problem (not ours to claim):**
- The kernel is a single-orbit equidistribution statement of `{(3/2)ⁿ}` / `{(8/3)ⁿ}`-type — the `p/q ∈
  {3/2, 8/3}`, single-orbit fragment of the **AEV normality conjecture (2025)**, which implies **Mahler's 3/2
  conjecture (1968)** / sits in the **Erdős ternary-digits family**. A recognized, generational open problem
  with **no analytic handle in the literature**; the annealed→quenched bridge is the missing analytic link AEV
  itself does not cross. `[OPEN]`.

**Bottom line.** Result (B) is the complete, self-contained statement of **what the BB(6) expanding-kernel
Collatz core is equivalent to and why it is structurally resistant**: four `[PROVEN]` units (exact reductions;
induced-map Bernoulli structure; density `β>0` barrier for Antihydra; the descriptive certification hierarchy
with two floors), assembled around one named `[OPEN]` kernel (AEV/Mahler). No machine is decided; per-cryptid
completion (A) is conditional on the kernel with no shortcut. The contribution is the *characterization and the
barrier*, not a decision — and every quantitative piece (five separations, two floors, the reductions,
`β=+1/2`, the annealed a.e. results, the `ψ=f(D)` lemma) is machine-checked or elementary, with the OPEN
frontier named.

---

## References
- Andrieu, Eliahou, Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (2025) — Conj. 1.2/1.6, Thm 1.5/1.7.
- Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. 8 (1968).
- Flatto, Lagarias, Pollington, *On the range of fractional parts {ξ(p/q)ⁿ}*, Acta Arith. 70 (1995) 125–147.
- Erdős (1979) ternary digits of powers of 2; Narkiewicz (1980) `#{n≤x : (2ⁿ)₃ omits digit 2} ≤ 1.62 x^{α₀}`, `α₀=log₃2` (upper bound only; finiteness unknown).
- Stérin, Woods, *Hardness of busy beaver value BB(15)*, arXiv:2107.12475 (BB↔Erdős reduction).
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562 (2019/2022).
- Lagarias / Bernstein–Lagarias (1996), Matthews–Watts — 2-adic Collatz conjugacy and ergodicity.
- Mañé / Conze–Guivarc'h / Bousch — ergodic optimization and sub-action theory.
- Büchi–Bruyère (automatic sets); arXiv:1901.03913 (range of non-linear polynomials not context-free); Dubickas, Mossinghoff (2009); Akiyama (2008).

*Soundness statement: every label above is copied verbatim from its source; none upgraded. No machine decided;
no non-halting asserted unconditionally; the four audit fixes (ψ=f(D) promotion; airtight-core/meta restatement;
all-k/REG one-direction+conjecture; scope discipline) are applied. Zero false claims.*
