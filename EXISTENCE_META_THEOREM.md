# The EXISTENCE-version of the no-structure-only meta-theorem — making the unified limit theorem family-wide (2026-06-28)

**Problem.** `UNIFIED_LIMIT_THEOREM.md`'s barrier is a **density-type** meta-theorem: it covers machines whose
halting is a one-sided Cesàro/Birkhoff underflow (Antihydra, o10-inner, the `3/2` core), via Bousch ergodic
optimization (`β := max_{T-invariant μ} ∫(θ−ϕ)dμ > 0` attained at a halting invariant measure). But **o18 and
o15 halt on an EXISTENCE event** — a forbidden carry-alignment that *ever* occurs (`non-halt ⟺ the bad event
never occurs`), a Borel–Cantelli/Erdős statement, **not** a one-sided density inequality
(`CRYPTID_O18_FRAMEWORK.md` §1, `CRYPTID_O17_O15.md` §2). The density template does not literally apply to
them. This note formulates and scopes the **existence-version** of the meta-theorem.

**Soundness.** Every line is `[PROVEN]` / `[CONDITIONAL]` / `[OPEN]` / `[MODEL]`. The central honest finding is
a **negative-with-a-twist**: the existence version does **not** yield a clean proven barrier the way the
density version does — and the precise reason is illuminating (it lives on the *other* axis of
`LIMIT_THEOREM.md`). Nothing is upgraded; one over-reach in `UNIFIED_LIMIT_THEOREM.md` §3 is corrected (§5).

---

## 1. The existence-version template  [PROVEN as a definition + elementary observations]

Let `M` be a TM whose halting reduces to a deterministic single-orbit system `(X, T, x_0)` (here `X = ℤ_p`,
`T = T_μ`, `μ = 2^a/3^b`, `v_p(μ) = −1`), together with a **halting set** `H ⊆ X`. For the `8/3` cryptids `H`
is a **clopen cylinder** (a finite-window "carry/frontier collision" condition at the head — o18: a `D`-read of
a `1` whose left neighbour is `1`; o15: an A-frontier `1`-collision). Then:

> **(E-criterion) Existence/avoidance halting criterion.**
> `M` **halts** `⟺` `∃ n ≥ 0 : T^n x_0 ∈ H`  (the bad event `B_n := {T^n x_0 ∈ H}` occurs for some `n`).
> Equivalently `M` **does not halt** `⟺` `∀ n : T^n x_0 ∉ H` — the orbit of `x_0` **avoids** `H` forever.
>
> Halting is `Σ⁰₁` / r.e. / **semi-decidable** (run until you hit `H`); non-halting is `Π⁰₁` / co-r.e., the
> **tail avoidance** event `limsup_n B_n = ∅` after a finite verified prefix. (Contrast the density
> criterion, which is a *limit average*, not a hitting/avoidance event.)

> **(E-hitting) A halting orbit that enters `H`** (the analog of `(H-fixed-point)`).
> `H ≠ ∅` and `H` is reached by *some* orbit: `∃ y_* , m : T^m y_* ∈ H`. The trivial witness is any
> `y_* ∈ H` itself (`m = 0`). Concretely, off-orbit configurations that DO halt exist and are exhibited for
> every cryptid (`LIMIT_THEOREM.md` "honest negative": Antihydra `0 1^2 0 0 1^9 0` halts; o17 `0A01^k`,
> `k≢0 mod 3`; for o18/o15 the collision cylinder `H` is nonempty by construction).

> **No-structure-only-proof analog (E-form).** A *structure-only / all-orbits / finite-certificate* proof of
> `M`'s non-halting is a **forward-invariant over-approximation** `L ⊆ X` with
> **(S)** `x_0 ∈ L`, **(C)** `T(L) ⊆ L`, **(A)** `L ∩ H = ∅`. (This is *exactly* the certificate-hierarchy
> object of `LIMIT_THEOREM.md` §1 — start∈L, step-closed, halt-free — transported to the dynamical model.)
> The claim "no structure-only proof exists" is: **no `L` in the chosen description class** (REG / SLIN /
> automatic / "all-orbits invariant") satisfies (S)+(C)+(A).

**The key structural difference from the density template, stated immediately.** The density "no-structure"
proof was forbidden because *any* all-orbits inequality must account for **every invariant measure**, including
the atom `δ_{y_*}` at the halting orbit (ergodic optimization is a `max over μ`). The existence object is a
forward-invariant **set** `L`, and **a set can simply exclude `y_*` and all of `H`.** `(E-hitting)` — the mere
*existence* of a halting orbit — therefore does **not**, by itself, block an avoidance certificate. This is the
crux of §2–§3 and the reason the two versions are genuinely different.

---

## 2. The existence-version barrier — what is PROVEN, and what it reduces to

### 2a. The topological half is PROVEN — and it is *favorable*, not a barrier  [PROVEN]

> **Lemma (closed over-approximation exists for any non-halting existence-machine with open `H`).**
> If `H` is open (clopen cylinder) and the orbit of `x_0` avoids `H` (i.e. `M` does not halt), then the
> **orbit closure** `L₀ := cl{T^n x_0 : n ≥ 0}` is forward-invariant, contains `x_0`, and is **disjoint from
> `H`**.
> *Proof.* Forward-invariance and `x_0 ∈ L₀` are immediate (`T` continuous on `ℤ_p`). If some `y ∈ H ∩ L₀`,
> then `H` open ⇒ a neighbourhood `U ∋ y` lies in `H`, and `y ∈ cl(orbit)` ⇒ some `T^n x_0 ∈ U ⊆ H` — i.e.
> the orbit hits `H`, contradicting non-halting. So `L₀ ∩ H = ∅`. ∎

So unlike the density case, a *non-halting existence-machine always has a working over-approximation* — the
orbit closure. **The existence barrier is therefore NOT "no invariant set avoids `H`"** (one always does). It
is purely a **descriptive-complexity** question:

> **(E-barrier reduction) [PROVEN].** For an existence-machine with clopen `H`, a structure-only avoidance
> proof in class `C` exists `⟺` some forward-invariant `L ⊇ orbit(x_0)` with `L ∩ H = ∅` is **describable in
> `C`**. The obstruction is **not** measure-theoretic (no `β`); it is whether the orbit closure — or a tame
> forward-invariant set separating it from `H` — has a finite/regular/automatic description.

This is **identical to the over-approximation axis of `LIMIT_THEOREM.md`** (§3 [OPEN] top, "does a tame
halt-free `L ⊇ reachable` exist?"). The existence meta-theorem is the dynamical-model phrasing of that exact
axis. It directly confirms the task's hint: **existence/avoidance sits on the over-approximation axis, not the
density/dynamical axis.**

### 2b. Why `(E-hitting)` does NOT give a clean proven barrier  [PROVEN negative]

The density barrier was a *theorem* (`β > 0 ⇒ no all-orbits bound`). The existence analog **fails to be a
theorem** for a precise, conjecture-free reason:

> **Observation [PROVEN].** `(E-hitting)` (a halting orbit `y_* ∈ H` exists) does **not** imply "no tame
> forward-invariant `L ⊇ orbit(x_0)` avoids `H`." A forward-invariant set need not contain `y_*`; it must
> only contain `orbit(x_0)` and avoid `H`, and (§2a) such sets exist. The halting orbit `y_*` lives on a
> *different* orbit that the certificate is free to exclude.

This is the **same** content as `LIMIT_THEOREM.md`'s "honest negative" (lines 359–368): off-orbit halters exist
for every cryptid, but a window/over-approximation can **gate on the head-local halt condition** and exclude
them while keeping `reachable`. The cryptid carries its discriminating feature **next to the head** (a local
collision), not in an unbounded clean run, so the brick-(d) "all-or-nothing on an unbounded `1^k` run" trick
does *not* transfer, and no contradiction is forced. **Hence the existence barrier is [OPEN], not [PROVEN].**

> **Contrast table.**
> | | density version | existence version |
> |---|---|---|
> | halting object | tail average drops below `θ` (a *non-clopen* limit event) | orbit hits clopen `H` |
> | structure-only proof | all-orbits one-sided inequality | forward-invariant `L ⊇ orbit`, `L∩H=∅` |
> | obstruction type | invariant **measure** (`β = max_μ`) | invariant **set** (descriptive complexity) |
> | does a halting orbit block it? | **YES** — `δ_{y_*}` is in the `max`, forces `β>0` `[PROVEN]` | **NO** — a set excludes `y_*` `[PROVEN]` |
> | barrier status | **[PROVEN]** (Bousch ergodic optimization) | **[OPEN]** (= LIMIT_THEOREM over-approx top) |
> | LIMIT_THEOREM axis | dynamical / ergodic | over-approximation / descriptive |

**Net (§2).** The existence version does **not** give "no structure-only proof" as cleanly as the density
version. The density barrier is a proven ergodic-optimization theorem; the existence barrier is the *still-open*
over-approximation/descriptive-complexity question. The two meta-theorems are **the two axes of
`LIMIT_THEOREM.md`**, and only the dynamical one is closed.

---

## 3. Are existence-type cryptids EASIER or HARDER than density-type? — split by axis  [honest]

The right answer is **not** a single verdict; it differs by axis, and the split is itself the finding.

### 3a. Annealed / measure side: existence is EASIER (and **unconditionally provable**)  [PROVEN]

> **Annealed avoidance via Borel–Cantelli I [PROVEN, no independence needed].** Let `B_n ⊆ X` be the set of
> starting points whose step-`n` image lands in the (epoch-`n`) collision cylinder, of Haar measure
> `Haar(B_n) ~ 1/N_n` where `N_n ≍ (8/3)^n` is the width. Then `Σ_n Haar(B_n) < ∞` (geometric, ratio `3/8`;
> `o18_bc.py`: `Σ_{k≥7} 1/N_k = 1.54·10⁻⁴`). **Borel–Cantelli I** (`Σ P(B_n) < ∞ ⇒ Haar(limsup B_n) = 0`,
> which needs **no independence**) gives: **Haar-a.e. starting point hits `H` only finitely often**, hence
> (with a finite verified prefix) **never** — i.e. **Haar-a.e. orbit is non-halting.**

This is a *genuine, clean, unconditional* annealed theorem, and it is **easier than the density annealed
statement**: density's a.e. result (`mean D = 2 > 3/2` for Haar-a.e. point) needs a CLT/large-deviation
argument, whereas existence needs only a **convergent sum** and the union bound. The summable target is the
source of the ease: the orbit's *total* bad-measure budget along the whole future is **finite** (`< 1`), so the
expected number of post-prefix collisions is `~0`.

> **Important correction to the literature note.** `o18_bc.py`'s comment "B-C needs INDEPENDENCE" is imprecise:
> it conflates **B-C I** (summable ⇒ a.s. finite — *no independence*, used above) with **B-C II** (the
> converse). The annealed avoidance result is **unconditional**; independence is *not* required. The
> obstruction is **annealed → quenched** (the single specified seed is one Haar-null point), exactly as on the
> density side — **not** a missing independence hypothesis.

### 3b. Analytic-input axis: existence needs a STRICTLY WEAKER input  [OPEN, but weaker ask]

The quenched (single-orbit) statements are:
- **density:** `liminf_N (1/N)#{n<N : D(o_n)≥2} ≥ θ` — a **positive one-sided lower density**, must hold in the
  limit (an *eternally-tight* constraint).
- **existence:** `#{n : T^n x_0 ∈ H_n} < ∞` with `Σ Haar(H_n) < ∞` — avoid a target of **finite total
  measure-budget**.

If one had an **effective single-orbit equidistribution rate** `|discrepancy_N| ≤ e_N`, then
`#{hits ≤ N} ≈ Σ_{n≤N} Haar(H_n) + O(e_N · (·))`; since `Σ Haar(H_n)` **converges**, finiteness follows the
moment the discrepancy term does not overwhelm a *summable* target — a **weaker** demand than producing a
positive liminf density. So on the analytic-input axis **existence is plausibly closer to provable**: it asks
only for a rate that beats a summable target (Borel–Cantelli-I strength), whereas density asks for a positive
lower density floor that holds forever.

**Caveat [OPEN, both].** Both are currently open with the *same shape* of missing piece: density lacks any
lower-density bound for a specific `3/2` orbit (FLP gives only a *range* bound, not density —
`COMPLETE_PROOF_CAPSTONE.md` §6); existence lacks a *finiteness* proof for the Erdős ternary-digit family
(Narkiewicz 1980 gives only an *upper bound on the count*, the set is not known finite —
`CRYPTID_O18_FRAMEWORK.md` §3). Neither has an effective rate in the literature. So "easier" is a statement
about the *strength of the analytic input required*, not about either being currently solved.

### 3c. No-structure-only-proof (barrier) axis: existence is HARDER (its barrier is OPEN)  [PROVEN meta]

By §2: the density machines get a **[PROVEN]** barrier (ergodic optimization, `β>0`); the existence machines
get only the **[OPEN]** over-approximation barrier (a separating set can exclude the halting orbit). So as a
*barrier-producing* template, existence is **weaker/harder** — there is no proven obstruction explaining why
structure-only fails; that explanation is itself the open over-approximation question.

> **One-line verdict (§3).** Existence-type cryptids have an **EASIER annealed/measure side** (Borel–Cantelli I,
> unconditional, no independence; summable target) and a **WEAKER required analytic input** (a rate beating a
> summable target vs a positive liminf), but a **HARDER (open) no-structure-only barrier** (no `β`; the barrier
> *is* the over-approximation axis). Density-type are the mirror image: harder annealed side, stronger required
> input, but a **proven** barrier. They are not ordered; they are *dual*, sitting on the two axes of
> `LIMIT_THEOREM.md`.

---

## 4. The existence-version meta-theorem, stated  [scoped]

> **Existence-version meta-theorem (BB(6) carry-alignment cryptids). [PARTIAL — components labelled].**
> Let `M` be a BB(6) cryptid whose halting reduces to `(X=ℤ_p, T_μ, x_0)` with `v_p(μ)=−1` and a **clopen
> halting set `H`**, under the existence criterion `(E-criterion)`. Then:
>
> 1. **[PROVEN]** (topological) for non-halting, the orbit closure `L₀` is forward-invariant and `L₀∩H=∅`: a
>    *closed* avoidance over-approximation always exists. The barrier is descriptive-complexity of `L₀`, **not**
>    existence of an invariant set.
> 2. **[PROVEN]** (annealed) `Σ Haar(B_n) < ∞` ⇒ (Borel–Cantelli I, no independence) Haar-a.e. orbit avoids `H`
>    eventually ⇒ Haar-a.e. seed is non-halting.
> 3. **[OPEN]** (the barrier) no *tame* (REG/SLIN/automatic) forward-invariant `L ⊇ orbit(x_0)` with `L∩H=∅`
>    exists. This is identical to `LIMIT_THEOREM.md`'s over-approximation [OPEN] top; it does **not** follow
>    from `(E-hitting)` (a halting orbit can be excluded by a set).
> 4. **[OPEN]** (the kernel) the quenched statement "`x_0` avoids `H` forever" `=` the `q=p` single-orbit
>    floor-mirror fragment of AEV Conj 1.6 in its **existence/Erdős facet** (`CRYPTID_O18_FRAMEWORK.md` §3),
>    needing an effective equidistribution rate beating the summable target (§3b).

So the existence version contributes **two new [PROVEN] components** (the closed-over-approximation lemma and
the unconditional annealed Borel–Cantelli-I avoidance) and **precisely locates** the barrier on the
over-approximation axis — but it does **not** deliver a proven family-wide no-structure-only barrier the way the
density version does.

---

## 5. Final family-wide scope of the unified theorem (density ⊕ existence)

The unified limit theorem is **two barriers on the two `LIMIT_THEOREM.md` axes**, not one. Honest scope:

| machine | `μ` | halt facet | barrier that governs | barrier status |
|---|---|---|---|---|
| **Antihydra** | `3/2` | **density** (Cesàro underflow) | dynamical/ergodic, `β=+1/2` at halting fixed pt `o=1` | **[PROVEN] unconditional** |
| **o10-inner** | `3/2` | **density** (inner sub-orbit) | dynamical/ergodic, kernel `β>0` | **[CONDITIONAL]** on inner reduction |
| **o18** | `8/3` | **existence** (Erdős carry-align) | **over-approximation/descriptive** | **[OPEN]** barrier + [PROVEN] §4.1, §4.2 |
| **o15** | `8/3` | **existence** (Erdős, messy coord) | **over-approximation/descriptive** | **[OPEN]** barrier + [PROVEN] §4.1, §4.2 |
| **o17** | odometer | **existence** (carry overflow) | over-approximation, but **kernel-less** (isometry, uniquely ergodic; Collatz-irregular halt) | **[OPEN]**, outside both equidistribution kernels |

**Reading.**
- **Density machines (`3/2`):** covered by the **[PROVEN]** dynamical barrier (Antihydra unconditional;
  o10-inner conditional). This is the only family-wide *proven* no-structure-only result.
- **Existence machines (`8/3`: o18, o15):** their actual halt facet is existence, so the **density `β`-barrier
  of `UNIFIED_LIMIT_THEOREM.md` §3 does not govern their halting** (see correction below). Their barrier is the
  over-approximation axis = **[OPEN]**. What is newly **[PROVEN]** for them: the closed-over-approximation lemma
  (§4.1) and the unconditional annealed Borel–Cantelli-I non-halting (§4.2). Their quenched kernel is the
  Erdős-facet AEV fragment (§4.4, **[OPEN]**), with a *weaker required analytic input* than density (§3b).
- **o17:** existence-criterion *in shape* (carry ever overflows) but **kernel-less** — an isometric odometer,
  uniquely ergodic, so neither the density nor the existence-*equidistribution* kernel applies; its hardness is
  a Collatz-irregular halt predicate (`CRYPTID_O17_O15.md` §1). The existence criterion is therefore **not**
  tied to the `v_p(μ)=−1` expanding kernel: o17 shows existence-shaped machines can have a totally different
  substrate. Outside the unified theorem, as before.

### Correction to `UNIFIED_LIMIT_THEOREM.md` §3 (soundness)  [retraction of an over-reach]

`UNIFIED_LIMIT_THEOREM.md` §3 (table rows o18/o15) assigns `β > 0 (deficit)` to o18/o15 via the **shared
renewal-density kernel** and places them under the **density** barrier. That `β` is genuine **for the kernel's
renewal density**, but it is **not** the obstruction to proving o18/o15's *actual* halting, because **o18/o15
do not halt on a renewal-density underflow** — they halt on an existence (carry-alignment) event
(`CRYPTID_O18_FRAMEWORK.md` §4 is explicit: "there is no `mean D'' ≥ const` halt threshold for o18"). The
existence analysis here **sharpens the scope**: the no-structure-only barrier that governs o18/o15 is the
**over-approximation axis ([OPEN])**, not the proven dynamical `β`. The shared *kernel/equidistribution object*
is real and family-wide (`CRYPTID_KERNEL.md`); but the **facet** (density vs existence) decides **which axis's
barrier applies**, and **only the density facet has a [PROVEN] barrier**. The o18/o15 rows should read "barrier
= over-approximation [OPEN]," not "density `β>0` [proven]." No machine's status changes (all still open); this
removes a mislabelled barrier attribution.

### Integration with the M1/M2/M3 milestones (`RESEARCH_PROGRAM.md`)

- **M1** (fixed-point uniqueness of the self-consistent renewal process, `M1_*.py`): a **density-side** tool
  (it constrains the parity-process law). It speaks to the density machines; for the existence machines the
  analog "milestone" is **an effective equidistribution rate beating a summable target** (§3b) — a *different
  and weaker* target than M1's positive-density fixed point.
- **M2** (unconditional partial density bound, `even-density ≥ ε`): **density-only**; the existence analog is
  **already achieved annealed** by §4.2 (Borel–Cantelli I gives the a.e. avoidance with *zero* extra
  hypothesis — strictly stronger than an `ε`-bound, on the measure side). So the existence machines' "M2" is
  done annealed; their open part is purely quenched.
- **M3** (reduce to a named conjecture): both facets reduce to **AEV Conj 1.6** — density to its Mahler facet
  (`q=2`), existence to its Erdős facet (`q=3`). M3 is **uniform across facets**; the existence reduction is
  the `q=3` floor-mirror fragment in the existence facet (`CRYPTID_O18_FRAMEWORK.md` §3, **[OPEN]**).

---

## 6. Bottom line

1. **Template (§1).** Existence version: `non-halt ⟺ orbit avoids clopen `H` forever`; structure-only proof `=`
   a forward-invariant `L ⊇ orbit(x_0)` with `L∩H=∅`; `(E-hitting)` `=` a halting orbit enters `H`.
2. **Barrier (§2).** It does **NOT** give no-structure-only as cleanly as density. `(E-hitting)` does **not**
   block an avoidance certificate (a *set* can exclude the halting orbit — [PROVEN] negative), so there is **no
   ergodic-optimization `β`**. The barrier reduces *exactly* to `LIMIT_THEOREM.md`'s **over-approximation /
   descriptive-complexity axis** ([OPEN]) — confirming the task hint that existence lives on the *other* axis.
   What *is* [PROVEN]: a closed over-approximation always exists (open `H` + non-halting ⇒ orbit closure avoids
   `H`); the barrier is purely whether a *tame* one exists.
3. **Easier or harder (§3).** **Dual, not ordered.** Existence is **EASIER on the annealed/measure side**
   (Borel–Cantelli I, unconditional, *no independence* — the `o18_bc.py` "needs independence" remark is
   corrected: that's the annealed→quenched gap, not B-C I) and needs a **strictly weaker analytic input** (a
   rate beating a *summable* target vs a positive liminf density), but has a **HARDER (open) barrier** (no
   `β`). Density is the mirror.
4. **Scope (§5).** Unified theorem = **two barriers on two axes**. **Density (`3/2`)** machines: **[PROVEN]**
   dynamical barrier (Antihydra unconditional, o10-inner conditional). **Existence (`8/3`)** machines (o18,o15):
   barrier is the **[OPEN]** over-approximation axis, plus **two new [PROVEN] components** (closed
   over-approximation; unconditional annealed Borel–Cantelli-I non-halting). **o17:** existence-shaped but
   kernel-less, outside. Corrects the §3 `UNIFIED_LIMIT_THEOREM.md` over-reach that put o18/o15 under the
   density `β`.

**No machine decided; no false barrier claimed; one mislabel retracted. Soundness intact.**

## Reproduce / sources
- `o18_bc.py` — `Σ_{k≥7} 1/N_k = 1.54·10⁻⁴` (summable target, geometric ratio `3/8`) → Borel–Cantelli I input (§3a, §4.2).
- `CRYPTID_O18_FRAMEWORK.md` §1, §4 — existence-vs-density facet; "no `mean D'' ≥ const` halt threshold" (basis of §5 correction).
- `CRYPTID_O17_O15.md` — o15 existence/Erdős facet; o17 kernel-less odometer (§5).
- `LIMIT_THEOREM.md` §3, §3′, "honest negative" (lines 359–368), "analytic content" (over-approximation axis = the existence barrier of §2).
- `UNIFIED_LIMIT_THEOREM.md` §1 (density template), §3 (the corrected rows), §5 (two-axes discussion).
- `COMPLETE_PROOF_CAPSTONE.md` §5–§6, `SESSION_2026-06-28_MINPROP.md` (density `β=+1/2`), `RESEARCH_PROGRAM.md` (M1/M2/M3).
