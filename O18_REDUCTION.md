# o18 — the exact §3c reduction and its EXISTENCE-version placement (2026-06-28)

Completes the §3c reduction for **o18** (`⌊8N/3⌋+2`, ratio `8/3 = 2³/3`, 3-adic) and decides rigorously
whether its halt criterion fits the unified theorem's **density** template (`H-criterion`) or needs the
**EXISTENCE** version. Companion to `CRYPTID_O18_FRAMEWORK.md` (background) and `COMPLETE_PROOF_CAPSTONE.md`
(the Antihydra/density template). All numerics use exact big-int / the trusted-simulator semantics
(`bb_sim.py` transition rule); every reduction step is cross-checked against the raw TM.

**Soundness.** Labels `[PROVEN]` (elementary arithmetic / exact mechanics), `[VERIFIED]` (machine-checked
this session), `[OPEN]`, `[MODEL]`/`[ANALOGY]`. Zero upgrades. No decision claimed.

---

## 0. What was cross-checked against the raw TM this session  [VERIFIED]

`o18 = 1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`. Two independent instrumented runs (one re-using the
`bb_sim.py` transition rule verbatim) over **2·10⁸ steps**:

- **10 F-entries, all read 0 ⇒ non-halting so far.** F is entered *only* via `D:1→1LF`, so #F-entries =
  #(D-reads-of-1) = 10; in every one the cell F reads is `0`, and the collision counter (D reads a 1 whose
  left neighbour is 1) is **0**. `[VERIFIED]`
- **The ×8/3 width law read straight off raw tape geometry.** The frontier positions of the F-entries are
  `|relpos| = 6, 22, 68, 194, 535, 1446, 3877, (interior +9), 10358, 27644`; successive ratios
  → **2.669 ≈ 8/3** (`27644/10358 = 2.669`). This confirms the orbit width `N_k ~ c·(8/3)^k` **from the tape
  itself**, not merely from an abstract recurrence. `[VERIFIED]`
- **Clean map vs break.** `N_{k+1}=⌊8N_k/3⌋+2` reproduces epochs 0–6 exactly
  (`10→28→76→204→546→1458→3890`); deviates at epoch 7 (actual `10373`, model `10375`, −2) and epoch 8
  (actual `27660`, `f(10373)=27663`, −3). The break = a base-3 carry the leftward rebuild cannot absorb.
  `[VERIFIED]`
- **The epoch-7 defect is real and routes F into the interior.** At step `23 492 737` there is an F-entry at
  `relpos = +9` (interior, not the left frontier) whose **left cell is 1** — F nonetheless reads `0`, so no
  halt. This is the one place a collision could have occurred. `[VERIFIED]`

---

## 1. The exact halt criterion from raw tape mechanics  [PROVEN / VERIFIED]

State F's transition is `1LE---`: on read `0` → write 1, move L, go to E; on read `1` → **HALT**. F is
reachable only through `D:1→1LF` (D reads a 1 at cell `p`, writes 1, moves to `p−1`, enters F at `p−1`).
Therefore F reads `tape[p−1]`, and:

> **(o18-HALT) [PROVEN].** o18 halts ⟺ **state F ever reads a `1`** ⟺ **at some D-read of a `1` (at cell `p`)
> the immediately-left cell `p−1` is also `1`** — i.e. the leftward D/F sweep frontier ever lands on a cell
> already holding a `1` (an adjacent-`11` *collision* / **left-frontier carry alignment**).

**Concrete mechanical confirmation `[VERIFIED]` (seeded raw-TM runs, `o18_haltdemo.py`):**
- *Alignment ⇒ halt.* Tape `{−1:1, 0:1}`, head 0 in state D: `D` reads 1 → `1LF` to cell −1; `F` reads the
  `1` → **HALT in 1 step.** The forbidden adjacent-`11` at the frontier halts o18 immediately.
- *Alignment is necessary.* Tape `{0:1}` (left cell 0), head 0 in state D: `F` reads the left `0`, writes 1,
  continues — no halt. So the halt is exactly the `1`-on-the-left event, nothing weaker.

This pins (o18-HALT) to raw tape mechanics, cross-checked, with zero modelling.

### Arithmetic form of the alignment event  [PROVEN mechanism / ANALOGY to a named problem]
The collision cell is the moving F-frontier of the `⌊8N/3⌋+2` orbit. A `1` appears there iff a **base-3
carry of the `×(8/3)` step** is deposited at the frontier instead of being absorbed into the clean
`0 1^{N−1}` block (exactly the epoch-7 defect mechanism). So:

> o18 halts ⟺ a base-3 carry / leading-digit of the `⌊x·(8/3)ⁿ⌋` odometer ever **aligns** with the
> self-referentially-determined F-frontier position.

This is a **digit/carry event of a `(2³/3)ⁿ` orbit**, the Erdős "ternary digits of `2^{3k}`" *family*.
**Honest scope `[ANALOGY, not reduction]`:** it is *not* the literal "`2^{3k}` omits a base-3 digit" — the
width orbit drifts (it is `⌊x(8/3)ⁿ⌋`, not `9·8ⁿ/3ⁿ`) and the carry is governed by the orbit's own
`W_n mod 3` (seed-dependent), not by the digits of `8ⁿ`. Same multiplier, same "does a forbidden carry ever
occur" shape, same missing tool — derived analogy, not identity.

---

## 2. The criterion is EXISTENCE-type (Borel–Cantelli), NOT a one-sided density inequality  [PROVEN]

> **(o18 non-halt) ⟺ the alignment NEVER occurs** ⟺ the base-3 carry of the orbit lands on the F-frontier
> for **no** epoch `k` (after the verified prefix) ⟺ the bad set `𝓑 = {k : carry aligns at epoch k}` is
> **finite and empty**.

This is a `∃ / finiteness` statement, and it is **structurally different** from Antihydra's density
criterion. The distinction is rigorous and prior to all number theory:

| | Antihydra (density) | o18 (existence) |
|---|---|---|
| non-halt condition | `liminf` even-density `E_n/n ≥ 1/3 ∀n` — a **Cesàro/Birkhoff average** bound | `𝓑 = ∅` — a **single forbidden configuration never appears** |
| failure mode | average *drifts below* threshold | one event *ever happens* |
| sufficient to decide via density? | **yes** — it *is* a density inequality | **no** — see below |
| named facet | Mahler 3/2 (density of `{ξ(3/2)ⁿ}`) | Erdős ternary digits of `2^{3k}` (existence/finiteness) |

**Why density is provably insufficient for o18 `[PROVEN]`.** The alignment set `𝓑` has **density 0** under
the equidistribution kernel (the frontier is one cell among the `~N_k` base-3 digit positions of `N_k`, and
the digits equidistribute — `[VERIFIED]`: units-trit density `0.333`, digit-2 density `0.3332` vs `1/3`).
But *density 0 does not decide halting*: a density-0 set of epochs can still be **non-empty**, and **one**
alignment = halt. The discriminator (halt vs non-halt) is `|𝓑| = 0` vs `|𝓑| ≥ 1`, which is invisible to any
Cesàro average. So there is **no `balance_n`-style underflow counter and no one-sided Birkhoff inequality**
(`liminf (1/N)Σ … ≥ c`) equivalent to o18 non-halting. This is the gap between "density 0" and
"finite/empty" — precisely the **Erdős facet** (Narkiewicz 1980 gives `#{n≤x : (2ⁿ)₃ omits digit 2} ≤
1.62·x^{0.631}`, a density *upper* bound; the set is **not even known finite** — no lower bound, no
finiteness). `[VERIFIED in literature placement; the missing lower bound is the same shape as Antihydra's
missing FLP density-analogue.]`

**The Borel–Cantelli structure `[MODEL]`.** Under Haar, `P(align at epoch k) ~ 1/N_k`, and with `N_k ~
c·(8/3)^k` (`[VERIFIED]` ratios → 8/3), `Σ_{k≥7} 1/N_k = 1.54·10⁻⁴ < ∞` (`[VERIFIED]` exact-fraction sum,
this session). The **first/easy Borel–Cantelli lemma** (summability ⇒ a.s. finitely many; it needs **only**
`Σ P < ∞`, **not** independence) then gives: for Haar-a.e. seed the alignment occurs finitely often ⇒
generically **non-halt**. This is the honest existence-version heuristic. It is a `[MODEL]` because the
specific o18 orbit is deterministic — "a.s." does not bind one orbit; one needs that the specific orbit is
*generic* for the carry process, which is the Erdős wall. **The key structural point stands regardless:** the
correct probabilistic skeleton is Borel–Cantelli (summability / finiteness), **not** a strong-law/density
inequality.

---

## 3. The EXISTENCE-version of (H-criterion), and whether the meta-barrier survives

### 3a. (H-criterion), two versions
The unified theorem's density form (Antihydra) is:

> **(H-criterion, density).** non-halt ⟺ `liminf_N (1/N) #{n<N : D(o_n) ≥ 2} ≥ 1/2` — a one-sided **Birkhoff
> average** lower bound; equivalently `β(ψ) = max_{T-inv μ} ∫ψ dμ ≤ 0` for the test function `ψ`.

o18 does **not** fit this literally (§2). Its correct template is:

> **(H-criterion, existence).** non-halt ⟺ the orbit `{N_k}` **never enters** the collision set
> `𝓑 = {configs whose F-frontier cell already holds a 1}` ⟺ there is a **forward-invariant trapping region**
> `S` with `seed ∈ S`, `f(S) ⊆ S`, `S ∩ 𝓑 = ∅` (an *inductive non-halting certificate* / avoidance
> invariant) ⟺ the carry-alignment set `𝓑` is **finite and empty after the verified prefix**.

The density version asks "does a running average stay above a threshold"; the existence version asks "does a
trapping region avoiding the forbidden set exist / is the bad set finite." The FAR/regular-certificate
programme is exactly the search for a *structural* such `S`; (H-criterion, existence) is its abstract form.

### 3b. Does the no-structure-only-proof barrier still apply?  **YES (in spirit), via a different gate**
**Meta-principle (shared).** A "structure-only proof of non-halting" — one using only properties of the
induced map `T''` shared across orbits (3-adic Haar preservation, exactness/Bernoullicity, unit-part
contraction, residue/valuation/symbolic-itinerary statistics) — cannot exist, because **the halting
configuration shares all of that structure**:

- **The halting fixed point `N = −1`** (`f(−1) = ⌊−8/3⌋+2 = −1`, `[VERIFIED]` unique integer fixed point)
  and the all-`D''=1` itinerary (never gaining a factor of 3) are legitimate points of the **same** 3-adic
  system: they sit in the support of Haar, have valid 3-adic itineraries, and synchronise under the same
  free unit-part contraction as the live orbit. (Direct transcription of `UNITPART` I4 / `MINPROP` F3 to
  base 3; the structural objects are identical with `2→3`.)
- Equivalently: `𝓑` is **structurally reachable** — there exist configurations sharing every finite-window
  structural signature with the live orbit that *do* enter `𝓑` (the seeded `{−1:1,0:1}` halt of §1 is a
  concrete witness that the alignment is a genuine, structurally-ordinary configuration, not an artefact).

Hence **no purely structural trapping region `S` can both contain the live orbit and avoid `𝓑`**; any
structural `S` that contains the live orbit also contains points sharing structure with the halting
configuration, so it cannot separate halt from non-halt. The discriminator lives **only in the orbit-specific
tail (genericity)** — the existence-setting transcription of "the finite-window/free part is blind to the
discriminator."

**Technical gate differs (honest divergence, parallel to `CRYPTID_O18_FRAMEWORK.md` §4):**
- In the **density** setting the barrier is quantified by ergodic optimisation: `β(ψ) = +1/2 > 0`, attained
  at the atom `δ_{o=1}`. This is a statement about a *Cesàro functional* `ψ`.
- In the **existence** setting there is **no such `ψ`** (the criterion is not an average), so `β(ψ)=max` does
  not apply. The barrier is realised instead as the **converse-Borel–Cantelli / finiteness gate**: proving
  `𝓑` finite/empty would be an unconditional finiteness result for a `×(8/3)`-orbit's ternary carries, of
  which **none exists** (Narkiewicz: upper density bound only, set not known finite). "No structure-only
  proof" becomes "**no finiteness/trapping certificate from structure alone**," because the halting orbit
  `N=−1` shares all available structure.

So: **same meta-principle (a halting configuration shares all available structure ⇒ no structure-only proof),
same anchoring at the halting fixed point, parallel to `β>0`; realised through the Erdős "no finiteness"
gate rather than the ergodic-optimisation `β` gate.** The barrier survives; its certificate of survival
changes form.

---

## 4. (H-fixed-point) verified concretely — the unfavourable extreme  [PROVEN / VERIFIED]

- **The fixed point halts (alignment occurs).** `N = −1` is the unique integer fixed point of
  `f(N)=⌊8N/3⌋+2` `[VERIFIED]`; the exact (no-floor) fixed point is `−6/5`; the induced `D''=1`-branch fixed
  point is `o = r/5 ∈ ℤ₃*` (`2/5` or `1/5`). None is a positive integer — it lies **off** the positive
  integer orbit (which is strictly increasing, `f(N)>N` for `1≤N≤10⁵` `[VERIFIED]`, hence transient, hence
  no invariant probability measure — the existence-setting analog of Antihydra's transience).
- **It realises the unfavourable extreme.** For the **existence** criterion the unfavourable extreme is a
  configuration **permanently inside `𝓑`** (alignment realised at every epoch) — the existence-analog of
  Antihydra's `δ_{o=1}` (`D=1` forever ⇒ even-density 0 ⇒ halt). The seeded raw-TM run of §1
  (`{−1:1,0:1}` → HALT in 1 step) **exhibits an actual orbit that halts because the alignment is present**,
  confirming the extreme is realisable and structurally ordinary (it uses only o18's own transitions).
  `N=−1` / the constant collision orbit is the algebraic anchor of that extreme.

---

## 5. Honest scope verdict

1. **The reduction itself (raw TM → existence criterion on base-3 carries) is CLEAN and `[PROVEN]`.**
   (o18-HALT) "F ever reads a 1 = the left-frontier adjacent-`11` carry alignment ever occurs" is derived
   purely from the transition table and confirmed by seeded raw-TM halts and a 2·10⁸-step trace (10/10
   F-reads = 0; the ×8/3 law read off raw tape geometry; the epoch-7 interior defect exhibited). No
   modelling enters the reduction.

2. **o18 is EXISTENCE-type, rigorously, `[PROVEN]`** — Borel–Cantelli/finiteness, the Erdős ternary facet —
   and **does NOT fit the density (H-criterion) literally** (density 0 ≠ empty; no Birkhoff inequality is
   equivalent to non-halting). This is established before any number theory.

3. **o18 is NOT proven non-halting, in either version `[OPEN]`.** Under the **density** template it is
   simply not expressible. Under the **EXISTENCE** template the reduction lands cleanly on the open kernel:
   > **(K_o18) [OPEN].** The base-3 carry of the `⌊8N/3⌋+2` orbit aligns with the F-frontier for only
   > finitely many (= zero, after the verified prefix) epochs — the `q=3` (different-base), single-orbit,
   > floor-mirror fragment of AEV Conj 1.6 in its **existence/Erdős** facet.

4. **The no-structure-only-proof barrier APPLIES** in the existence setting (the halting fixed point `N=−1`
   shares all structure ⇒ no structural trapping certificate), parallel to `β>0`, but realised through the
   **finiteness gate** (no unconditional lower bound / finiteness result for `×(8/3)` ternary carries) rather
   than the ergodic-optimisation `β(ψ)=max` gate. This is `[PROVEN in spirit / structurally]`; making it a
   formal theorem requires the **existence-version meta-theorem**, which is **not yet proven separately**.

5. **Requirement handed to the meta-theorem agent.** To close o18 "in an existence-version of the theorem,"
   two pieces must be supplied, neither of which is the density meta-theorem:
   - **(M-exist) [TO PROVE].** A formal existence/finiteness meta-theorem: *no forward-invariant trapping
     region `S` definable from the structural (measure/symbolic/valuation) data can separate the live orbit
     from `𝓑`, because `N=−1`/the all-`D''=1` configuration shares every such structural property.* (The
     density analog is `β(ψ)=+1/2>0`; the existence analog should be a "shared-structure ⇒ no avoidance
     certificate" statement, with the converse-Borel–Cantelli/Narkiewicz gate as the quantitative obstruction.)
   - **(K_o18) [INHERITED OPEN].** The single-orbit ternary-carry finiteness statement = the `q=3`
     existence-facet fragment of AEV Conj 1.6. World-open; no unconditional tool reaches it.

   **Verdict:** o18 is **PROVEN-reduced** to (K_o18) in the existence version, with the structure-only barrier
   **PROVEN in spirit** at the shared fixed point `N=−1`; it is **NOT** "PROVEN in an existence-version of the
   theorem" until **(M-exist)** is formalised. The reduction (raw TM → existence kernel) is clean and PROVEN;
   the *meta-theorem* (no structure-only proof, existence version) needs separate proof. No decision; soundness
   intact.

---

## Appendix — this session's checks (exact / trusted-simulator semantics)
- 2·10⁸-step instrumented trace (bb_sim transition rule): 10 F-entries, all read 0; collisions 0; frontier
  positions `6,22,68,194,535,1446,3877,+9(interior),10358,27644`, ratios → 8/3.
- Seeded raw-TM halt: `{−1:1,0:1}` head@0 state D ⇒ HALT in 1 step (F reads 1). Control `{0:1}` ⇒ no halt.
- `⌊8N/3⌋+2`: epochs 0–6 exact, break at 7 (−2) and 8 (−3 vs actual predecessor); `N=−1` unique integer
  fixed point; `f(N)>N` on `[1,10⁵]`.
- `Σ_{k≥7} 1/N_k = 1.54·10⁻⁴` (exact fractions), `Σ_{k≥0} = 0.157`.
- (Reproduced `o18_framework_numerics.py`: GAP-LEMMA `T''` 0 violations to 4000; `D''` geometric, Haar mean
  3/2; units/digit-2 base-3 densities ≈ 1/3.)
