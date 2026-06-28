# A unified structural limit theorem for the BB(6) exponential-Collatz core (2026-06-28)

> **⚠ SOUNDNESS CORRECTION 2026-06-28 (later same day, see `SESSION_2026-06-28_REDUCTIONS.md` + `EXISTENCE_META_THEOREM.md`).**
> This document placed **o18/o15 under the density `β>0` barrier** via the shared renewal kernel. That is a
> **MISLABEL — RETRACTED.** o18/o15 do **NOT** halt on a renewal-density underflow; they halt on an
> **EXISTENCE** event (a base-3 carry alignment *ever* occurring = Borel–Cantelli / Erdős facet). The
> `2^a/3^b` *kernel* (exact `T_μ`, `v_p(μ)=−1`, Haar-Bernoulli) IS shared family-wide, but the **FACET**
> (density vs existence) decides which LIMIT_THEOREM **axis** governs:
> - **density facet (3/2):** the `β>0` ergodic-optimization barrier is **[PROVEN]** (Antihydra). The only
>   family-wide proven no-structure-only result. o10-inner [conditional]; **o10 FULL is OUT** (composite
>   criterion, genericity makes it *halt* — likely a delayed halter, direction OPEN).
> - **existence facet (8/3: o18, o15):** the barrier is the **[OPEN] over-approximation axis** (an invariant
>   *set* can simply exclude the halting orbit, so there is NO `β`). NEW [PROVEN] components instead: a
>   closed-over-approximation lemma + an **unconditional annealed Borel–Cantelli-I non-halting** result
>   (Haar-a.e. seed; `ΣHaar(B_n)≍Σ(8/3)^{-n}=1.54e-4<∞`, needs no independence). Quenched kernel = Erdős-facet AEV q=3 fragment.
> - **o17:** kernel-less (isometric odometer), outside both.
> No machine's status changes (all open); the β>0 barrier's PROVEN scope is **Antihydra only**, not the
> existence machines. Read the corrected two-facet/two-axis picture below as amended by this banner.

**Goal.** Decide whether Antihydra's "no structure-only proof exists" *meta-theorem*
(`COMPLETE_PROOF_CAPSTONE.md` §5; `SESSION_2026-06-28_{MINPROP,UNITPART}.md`) is a one-off, or whether it
**generalizes to a single limit theorem covering the whole `2^a/3^b` Collatz core of BB(6)** — a new,
original structural result that does not decide any cryptid but proves a uniform limit on *all* of them.

**Verdict.** It generalizes. The meta-theorem is *not* Antihydra-specific: it rests on two structural
facts that are now machine-verified to hold **family-wide** (`kernel_classification.py`, `cross_cryptid.py`,
`CRYPTID_KERNEL.md`). The result below is a **[PROVEN] abstract template** + a **[CONDITIONAL] unified
theorem** (conditional only on the per-machine exact reductions, which are themselves PROVEN for Antihydra
and partial for the others). Soundness discipline: every line is labelled; nothing is upgraded; the honest
scope (which machines are in, which are out, and *why*) is stated precisely in §4.

---

## 1. The abstract meta-theorem template  [PROVEN — it is the existing Antihydra proof, abstracted]

Antihydra's "no structure-only proof" (`MINPROP` F3) rests on exactly three ingredients. Strip them of the
number `3/2` and they become a template.

Let `M` be a Turing machine whose halting reduces to a **deterministic single-orbit dynamical system**
`(X, T, x_0)` carrying a real **depth/renewal statistic** `ρ` (a Birkhoff time-average of a bounded
function `ϕ`), such that:

> **(H-criterion) One-sided single-orbit equidistribution halting criterion.**
> `M` **does not halt** `⟺` `liminf_{N} (1/N) Σ_{n<N} ϕ(T^n x_0) ≥ θ` for a fixed threshold `θ`
> (equivalently the Cesàro empirical measure of the orbit does not push `ρ` below `θ`). Halting is the
> *complementary* one-sided event "`ρ` drops below `θ`."
>
> **(H-fixed-point) A halting fixed point realizing the unfavorable extreme.**
> `T` has an invariant probability measure `μ_*` (concretely: an atom on a `T`-fixed/periodic point) with
> `∫ ϕ dμ_* < θ` — i.e. `μ_*` violates the non-halt inequality — **and `μ_*` corresponds to a genuinely
> halting orbit**. Write `β := max_{T-invariant μ} ∫ (θ − ϕ) dμ`. Then `(H-fixed-point) ⟹ β > 0`.

> **Template Meta-Theorem [PROVEN, conjecture-free given (H-criterion)+(H-fixed-point)].**
> *No structure-only / finite-certificate proof of `M`'s non-halting can exist.*
>
> *Proof.* By Mañé–Conze–Guivarc'h–Bousch ergodic optimization, a one-sided inequality
> "`(1/N)Σ ϕ(T^n y) ≥ θ` for **all** orbits `y`" is equivalent to `β ≤ 0`. A "structure-only" proof — one
> that uses only `T`-invariant data (measure preservation, exactness, specification, spectral gap,
> contraction, a coboundary/sub-action bound, any all-orbits Lyapunov argument) — establishes the inequality
> for every orbit simultaneously, hence forces `β ≤ 0`. But `(H-fixed-point)` gives `β > 0`. So a
> structure-only proof would prove the **false** statement "every orbit is non-halting" — contradicted by the
> halting orbit `μ_*`. Therefore the non-halt distinction is invisible to all-orbits structure; it lives only
> in whether the *specific* orbit `x_0` is generic (its Cesàro average `≥ θ`). ∎

Two corollaries reproduce the two faces of the Antihydra capstone §5:
- **(i) ergodic-optimization face.** The obstruction is the **atomic maximizer** `δ_{x_*}` at the halting
  fixed point; the generic (Haar) slack is irrelevant because `β` is set by `max_μ`, not by Haar.
- **(ii) shared-free-structure face.** Every "free" (finite-window, pathwise, genericity-independent)
  observable agrees on `x_0` and on the halting orbit `x_*` (both obey the same finite-window synchronization
  of `T`), so no free observable can separate halting from non-halting; the separation is a pure
  **tail-average (genericity)** fact. (This is `UNITPART` I4, which is just the contrapositive packaging of
  the same `β > 0`.)

The template makes precise *why* every structural attack only **relocates** the gap: each is a finite-window
or all-orbits tool, and the template proves both classes are blind to the one quantity that separates halting
from non-halting — the single-orbit tail average.

---

## 2. The family-wide structural engine  [PROVEN, machine-verified]

The template applies to a machine the instant its reduction supplies `(H-criterion)` and `(H-fixed-point)`.
For the BB(6) Collatz core, **both are delivered by one shared object**, proven family-wide (not per-machine):

> **Shared-kernel classification theorem (`CRYPTID_KERNEL.md`, `kernel_classification.py`). [PROVEN].**
> For a Mahler multiplier `μ = 2^a/3^b` in lowest terms with denominator a single prime `p`
> (`v_p(μ) = −1`), the map `T_μ(x) = ⌊μx⌋` is a **clean `p`-to-1, Haar-measure-preserving, exact
> endomorphism of `ℤ_p`**, and its **induced (renewal) map is full-branch piecewise-affine expanding
> (slopes `μ^g`) with a `ℤ_p` fixed point on EVERY branch.**

Reproduced this session (`kernel_classification.py`): `3/2, 5/2, 7/2, 27/2` (`p=2`) and
`8/3, 4/3, 16/3, 2/3` (`p=3`) are all clean `p`-to-1 (`onto`, multiplicities `={p}`, interval argument
holds); the `v_p = −2` controls (`9/4, 16/9, 27/4, 25/4`) are **not** clean (mixed multiplicities) — so
`v_p(μ) = −1` is exactly the clean regime. "Fixed point on every branch" verified 8/8 for both `p = 2` and
`p = 3` (`cross_cryptid.py`; `CRYPTID_KERNEL.md` table).

**Why this is exactly the engine the template needs:**
- The **depth statistic** `ϕ` is the renewal indicator `1{p \mid x}` (the `÷p` event); its Birkhoff average
  is the **renewal density**, `→ 1/p` under Haar (mean inter-renewal gap `→ p`), the i.i.d.-geometric law.
- "**Fixed point on every branch**" is precisely `(H-fixed-point)`: each branch is an itinerary word `w` of
  length `L_w` (one renewal per period), so its fixed-point orbit has **renewal density `1/L_w`**, and the
  branch family realizes renewal densities ranging over a set with **infimum `0`** — below *any* positive
  halting threshold `θ`. Hence there is always an invariant measure with `∫ϕ dμ_* < θ`, i.e. `β > 0`.
  The full-branch expanding structure is the *uniform mechanism* guaranteeing `β > 0` across the family.

So the meta-theorem's hypothesis `(H-fixed-point)` is **structurally automatic** for every `2^a/3^b` core
machine whose halting reduces to a renewal-density / `p`-adic-digit criterion: the cryptid kernel
`T_μ` *always* carries the deficit-maximizing low-renewal invariant measure that kills structure-only proofs.

---

## 3. Per-machine verification of the template hypotheses

Numerics this session (`scratchpad/unified_verify.py`, exact arithmetic):

| machine | `μ` (`p`) | `(H-criterion)`: non-halt ⟺ one-sided single-orbit equidist. | `(H-fixed-point)`: halting fixed point / extreme | `β` |
|---|---|---|---|---|
| **Antihydra** | `3/2` (`p=2`) | **[PROVEN]** non-halt ⟺ even-density `≥ 1/3` ⟺ `mean D ≥ 3/2` (renewal chain, capstone §2) | **[PROVEN]** `o = 1` (raw fixed point `⌊3·1/2⌋=1`); constant orbit all-odd ⟹ `E_n = 0` ⟹ `balance_n = −n < 0` ⟹ **HALTS**; even-density `0` = minimal extreme | **`β = +1/2`** (ψ-form, `MINPROP` F3); deficit form `θ−0 = 1/3 > 0` |
| **o10-inner** | `3/2` (`p=2`) | **[CONDITIONAL]** inner orbit `m→⌈3m/2⌉` is the same `p=2` kernel; but the *full* o10 halting is the **nested outer refill** (doubly-exp, irregular), so the single-orbit equidist. criterion is established for the **inner** sub-orbit only | **[PROVEN for the kernel]** the inner `3/2` kernel carries the same minimal-renewal fixed point (density `0`) ⟹ `β > 0`; whether it is a single halting integer orbit of the *full* machine is not derived | `β > 0` (inner kernel) |
| **o18** | `8/3` (`p=3`) | **[CONDITIONAL]** halt ⟺ base-3 leading-digit/carry overflow of `⌊x·(8/3)^n⌋`; non-halt ⟺ one-sided base-3 digit-density bound. Clean width law `⌊8N/3⌋+2` verified for 7 epochs, **breaks at epoch 8** (carry) — reduction is partial | **[PROVEN, structural]** `p=3` kernel: fixed point on every branch, renewal densities `→ 0`, Haar `1/3` ⟹ a low-renewal invariant measure below `θ` exists ⟹ `β > 0`. (No nonzero *raw* fixed point of `⌊8x/3⌋`, only `x=0`; the extreme is a long-itinerary branch measure, not a single integer halting orbit — see §4) | `β > 0` (deficit) |
| **o15** | `8/3` (`p=3`) | **[CONDITIONAL]** same `p=3` kernel object `⌊(8/3)^n⌋ mod 3`; halt ⟺ right-frontier `11`-collision; **no clean scalar orbit map** (genuine parity-irregularity) — reduction is the weakest of the four | **[PROVEN, structural]** identical `p=3` kernel ⟹ `β > 0` exactly as o18 | `β > 0` (deficit) |
| **o17** | odometer (`x→x+1`, base-≈3 carry) | **FAILS** — not a `⌊μx⌋` expanding map; an **isometry** of `ℤ_p`, **uniquely ergodic** ⟹ equidistribution is *automatic*; the hardness is the **Collatz-irregular halt predicate** (`0 A 0 1^k`, halts by `k mod 3` with proven halters interleaved), not a renewal-density inequality | **FAILS** — no expanding induced map, no renewal-density extreme, no halting fixed point of the required form | n/a |

Confirmed numerically (`unified_verify.py`): Antihydra `c_0=1` balances `0,−1,−2,…` (halts), even-density `0`
(extreme) vs `c_0=8` even-density `0.5002`; `kernel_classification.py` reproduces the clean-`p`-to-1
classification for both primes (the `(H-fixed-point)` engine of §2).

**Reading of the table.** `(H-criterion)` is **PROVEN exactly for Antihydra** and **CONDITIONAL** for the
others (their exact halt-predicate reductions are partial: o18 breaks at epoch 8, o15/o10 have no clean
scalar map). `(H-fixed-point)` — the part that powers the meta-theorem — is **PROVEN family-wide** by the
shared expanding-kernel structure (§2), *independently* of how clean each reduction is, because `β > 0`
needs only "the kernel carries a below-threshold invariant measure," which the full-branch fixed-point
structure guarantees for every `v_p(μ) = −1` multiplier.

---

## 4. The unified theorem and its exact scope

> **Unified Structural Limit Theorem (BB(6) exponential-Collatz core). [CONDITIONAL].**
> Let `M` be a BB(6) cryptid whose halting reduces (via its `§3c` exact reduction) to the single-orbit
> dynamics of `T_μ(x) = ⌊μx⌋` on `ℤ_p` with `μ = 2^a/3^b`, `v_p(μ) = −1`, and whose **non-halting condition
> is the one-sided single-orbit renewal-density inequality** `liminf (renewal density of x_0) ≥ θ` for some
> `θ ∈ (0, 1)` (hypothesis `(H-criterion)`). Then:
>
> 1. `(H-fixed-point)` holds automatically: `T_μ`'s induced map is full-branch expanding with a `ℤ_p` fixed
>    point on every branch (`CRYPTID_KERNEL.md`, **[PROVEN]**), so the renewal-density spectrum of
>    `T_μ`-invariant measures has infimum `0 < θ`, giving `β = max_μ ∫(θ − ϕ)dμ > 0`.
> 2. **By the Template Meta-Theorem (§1), no structure-only / all-orbits / finite-certificate proof of `M`'s
>    non-halting can exist.** The halting/non-halting distinction lives **only** in the single-orbit
>    genericity of `x_0` — a Mahler/AEV-type single-orbit equidistribution statement (the `μ`-instance of
>    the AEV-2025 / Mahler-1968 conjecture, `v_p(μ)=−1`).
>
> The result is **uniform**: it is one theorem indexed by `(a, b, p)`, sharing one kernel, one obstruction,
> and one missing analytic input (rank-1 effective single-orbit equidistribution of `⌊μ^n⌋ mod p`).

**"[CONDITIONAL]" means exactly:** conditional on each machine's `(H-criterion)` reduction being correct.
That reduction is **[PROVEN]** for **Antihydra**, and **partial/[CONDITIONAL]** for **o18, o15, o10**
(epoch-8 break / parity-irregular / nested-outer respectively). Conclusion (1) — and hence the
no-structure-only-proof conclusion — is **[PROVEN] for Antihydra unconditionally**, and holds for the
others the moment their reduction is completed; the engine (1) itself needs no reduction beyond `v_p(μ)=−1`.

### Honest scope — exactly which machines are covered

- **IN, fully [PROVEN]:** **Antihydra** (`3/2`). Both hypotheses proven; `β = +1/2` at a *genuine halting
  integer fixed point* `o = 1`. This is the meta-theorem in its sharpest form (the maximizer is a single,
  literally-halting orbit).
- **IN, [CONDITIONAL] on the (partial) reduction:** **o18, o15** (`8/3`), **o10-inner** (`3/2`). The
  shared-kernel engine gives `β > 0` and hence "no structure-only proof" the moment `(H-criterion)` is
  pinned. **Caveat (precise):** for the `8/3` machines there is **no nonzero raw fixed point** of `⌊8x/3⌋`
  (only `x=0`, the *maximal*-renewal extreme); the deficit-maximizing measure is a **long-itinerary branch
  measure** of the induced map, not a single integer halting orbit. So `(H-fixed-point)` holds in its
  measure form (`β > 0`, which is all the meta-theorem needs), but the picturesque "single halting fixed
  point" is exact only for the `3/2`-**floor** machines (Antihydra, and any `3/2`-floor sibling such as the
  flagged Lucy's Moonlight candidate). The conclusion (no structure-only proof) is unaffected — it depends
  on `β > 0`, not on the maximizer being a single orbit.
- **OUT — o17 (odometer).** Genuinely excluded, for a *structural* reason: o17's base object is a carrying
  base-≈3 odometer, an **isometry** of `ℤ_p`, **uniquely ergodic** — so single-orbit equidistribution is
  *automatic*, there is no renewal-density inequality, and no halting fixed point of the required form. o17's
  hardness is its **Collatz-irregular halt predicate**, a different obstruction type (`CRYPTID_KERNEL.md` §
  "two obstruction types"). The unified theorem does **not** cover it and does not claim to.
- **OUT — the slow-width / poly-envelope majority** (Space Needle, o2,o3,o4,o5,o7,o8,o11–o14,o16). These
  carry the *same* irregular `2^a/3^b` content (`CRYPTID_REDUCTIONS.md` Stage-1: "one difficulty in two
  costumes"), so **morally** they inherit the template through their family membership (o5 `4/3`; o7,o8
  `3/2`; o15,o18 `8/3`). But their reductions are only "**reduced to family + multiplier**," not exact halt
  criteria — so `(H-criterion)` is **not** established for them, and the unified theorem covers them only
  **conjecturally**, pending `§3c` completion. Stated honestly: in-family by multiplier, not yet in-scope by
  proof.

**One-line scope summary.** The unified theorem rigorously covers the **`v_p(μ) = −1` expanding-kernel
cryptids with a renewal-density halting criterion** — Antihydra unconditionally, {o18, o15, o10-inner}
conditionally on their partial reductions — and **provably excludes o17** (odometer / uniquely ergodic) and
does **not** yet reach the slow-width majority (reductions incomplete).

---

## 5. Connection to the certificate hierarchy (`LIMIT_THEOREM.md`) — what it proves, what it does NOT

The certificate hierarchy's top item is **[OPEN] "no REG / no tame-class certificate exists for a cryptid"**
(the over-approximation axis: does a regular, step-closed, halt-free `L ⊇ reachable` exist?). The unified
limit theorem **does not close this** — and the distinction is exact and important:

- **What the unified theorem PROVES (a NEW, family-wide result):** it closes the **all-orbits / dynamical /
  ergodic** proof axis. `LIMIT_THEOREM.md`'s "analytic content" note lists, as an *honest caveat*, that "a
  measure/spectral certificate route is blind to the specified orbit (rank-1, continuum of invariant
  measures)." The unified theorem **upgrades that caveat from heuristic to a [PROVEN] obstruction, and
  generalizes it from Antihydra to the entire `2^a/3^b` core**: it is not merely that the measure route is
  *blind*, but that ergodic optimization gives `β > 0` **attained at a halting invariant measure**, so any
  all-orbits/structural bound provably proves a *false* statement. This is the rigorous, uniform version of
  "why the over-approximation top resists," covering the whole family by one mechanism (the shared expanding
  kernel of §2), not four separate machines.
- **What it does NOT prove:** "no REG certificate of any kind." A REG certificate is an **over-approximation**
  `L ⊇ reachable`, *not* an all-orbits ergodic inequality. The meta-theorem forbids proofs that argue from
  `T`-invariant structure for all orbits; a hypothetical regular invariant *set* need not be built through
  the orbit's Birkhoff statistics, so it escapes the `β > 0` argument. The two axes —
  **(dynamical, all-orbits)** vs **(over-approximation, exact-set)** — coincide only at the cryptid vertex,
  where **both remain [OPEN]** as constructions; the unified theorem closes the *dynamical* one and leaves
  the *over-approximation* one open (exactly as `LIMIT_THEOREM.md` §"analytic content" already flags).

**Net.** The unified theorem is a genuinely new contribution at the **dynamical/ergodic** axis: a single
structural limit theorem proving that **no all-orbits/structure-only proof of non-halting can exist for the
entire BB(6) `v_p(μ)=−1` Collatz core at once** (Antihydra unconditionally; o18/o15/o10-inner conditionally),
because each shares the full-branch expanding kernel whose deficit-maximizing invariant measure (`β > 0`) is
a halting one. It **strengthens and generalizes** `LIMIT_THEOREM.md`'s "measure route is blind" caveat into
a proven, family-wide ergodic-optimization barrier, and it **pins the halting/non-halting distinction to a
single point**: the single-orbit genericity (Mahler/AEV equidistribution) of `x_0`. It does **not** resolve
the certificate hierarchy's [OPEN] over-approximation top, which is a strictly different (and still open)
axis. No machine is decided; no false proof; soundness intact.

---

## Reproduce
- `python kernel_classification.py` — clean `p`-to-1 iff `v_p(μ) = −1` (the §2 engine; `3/2,8/3,4/3` clean,
  `9/4,16/9,…` not).
- `scratchpad/unified_verify.py` — Antihydra halting fixed point `o=1` (balances `0,−1,−2,…`, even-density
  `0`) vs `c_0=8` (even-density `0.5002`); `p`-adic fixed-point renewal-density extremes for `3/2, 8/3, 4/3`.
- `cross_cryptid.py`, `CRYPTID_KERNEL.md` — fixed-point-on-every-branch (Q9b), 8/8 for `p=2,3`.

## Source documents
`COMPLETE_PROOF_CAPSTONE.md` (§5 the two meta-theorems), `SESSION_2026-06-28_MINPROP.md` (β(ψ)=+1/2 at o=1),
`SESSION_2026-06-28_UNITPART.md` (shared-free-structure face), `CRYPTID_KERNEL.md` (shared expanding kernel +
classification theorem), `CRYPTID_REDUCTIONS.md` (per-machine reductions and their partiality),
`CRYPTID_CENSUS.md`, `LIMIT_THEOREM.md` (certificate hierarchy + over-approximation axis).
