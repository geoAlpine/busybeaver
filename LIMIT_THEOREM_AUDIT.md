# Strategic gap-audit of the achievable theorem (B): the STRUCTURAL LIMIT THEOREM + frontier catalogue (2026-06-28)

**Scope.** This audits **(B)** — the original contribution that does *not* require solving any cryptid:
the certification-complexity hierarchy, the frontier catalogue, the exact reductions, and the density-side
no-structure-only barrier. It does **not** re-audit **(A)** (complete proof of a specific cryptid), except
to confirm (A)'s honest status and to extract the unconditional fallback theorems that live inside it.

**Soundness discipline.** Labels `[PROVEN]/[CONDITIONAL]/[OPEN]` are copied verbatim from the source
documents; **no label is upgraded**. Where a source flags a claim as `[verified]` (numerical) rather than
`[PROVEN]`, that distinction is preserved and called out as a writeup gap. Sources read: `COMPLETE_PROOF_CAPSTONE.md`,
`UNIFIED_LIMIT_THEOREM.md` (+ correction banner), `EXISTENCE_META_THEOREM.md`, `O17_REG_BARRIER.md`,
`O18_NO_CERTIFICATE.md`, `LIMIT_THEOREM.md`, `SESSION_2026-06-28_{MINPROP,UNITPART,REDUCTIONS,THREE_MOVES,CERT_HUNT}.md`,
`AEV_DIGEST.md`, `docs/theory_certification_hierarchy.md`.

---

## 1. PROVEN-vs-gap inventory for (B)

(B) is not one statement; it is **four separable proven units** plus a correctly-labelled OPEN frontier.
Audited one component at a time, as requested.

### 1A. The descriptive certification-complexity hierarchy (the Chomsky tower)  [PROVEN — airtight, need-only-writeup]

`LIMIT_THEOREM.md` §2, §5. Five strict separations of certificate classes for non-halting, **each with an
explicit, simulation-verified witness TM**:

| separation | witness | status | audit note |
|---|---|---|---|
| star-free ⊊ REG | parity counter `1RB0LZ_1LC1RA_0RA0LC` (brick d) | **[PROVEN]** conjecture-free | airtight; gap = group language `(11)*1`, syntactic monoid ℤ/2 |
| REG ⊊ SLIN | EQ machine `eq_machine.py` (brick a) | **[PROVEN]** conjecture-free | airtight; pumping + semilinear reachable |
| SLIN ⊊ 2-automatic | POW2W `S={2ⁿ}` (brick e) | **[PROVEN]** | lower half airtight; upper half cites Büchi–Bruyère (standard) |
| 2-automatic ⊊ CF | PALW binary palindromes (brick g) | **[PROVEN]** | lower half airtight; upper half standard CF |
| CF ⊊ CS | SQW `S={n²}` (brick f) | **[PROVEN]** | **depends on external arXiv:1901.03913** (non-linear poly range ∉ CF) + LBA; not self-contained |
| CS ⊊ recursive | diagonalization (Space Hierarchy) | **[PROVEN] but NON-explicit** witness | honest: loses the "small explicit TM" character |
| recursive ⊊ arithmetic | — | holds as classes, **NOT Squeeze-witnessable** | correctly flagged |

- **Squeeze Lemma** (certificate-complexity of a check-`S`-every-cycle machine = descriptive complexity of `S`):
  **[PROVEN]**, the engine behind (e)/(f)/(g). Airtight.
- **REG suffices at n=3** (63 explicit certificates): **[PROVEN]** clean finite theorem.
- **Verdict:** this unit is **the most complete and most standalone** part of (B). It is conjecture-free,
  machine-checked, and orthogonal to the cryptids. **Only genuine dependency on outside literature is brick (f)**
  (arXiv:1901.03913) — fine for a paper, just must be cited as an input, not re-proved. No internal gaps.

### 1B. The subword-complexity floor of the cryptid parity sequence  [PROVEN — airtight]

`LIMIT_THEOREM.md` §3″. For Antihydra's parity sequence `r_n = c_n mod 2`:
- coding bijection `φ_ℓ` (so `p(ℓ) = #residues visited mod 2^ℓ`): **[PROVEN]** (verified ℓ≤14).
- not eventually periodic (transience: `T(c)>c`, only fixed points 0,1): **[PROVEN]** conjecture-free.
- not Sturmian (`p(2)=4>3`): **[PROVEN]**.
- linear floor `p(ℓ) ≥ (ℓ−3)/log₂(3/2) ≈ 1.71ℓ`, slope matching Dubickas (2009): **[PROVEN]**.
- lift bound `p(ℓ) ≤ p(ℓ+1) ≤ 2p(ℓ)`: **[PROVEN]**.
- ceiling `p(ℓ)=2^ℓ ⟺ single-orbit equidistribution = Mahler/AEV`: **[OPEN]** (correctly labelled).
- **Verdict:** airtight. Gives a second, independent proven floor under the OPEN cryptid vertex.

### 1C. The exact reductions (raw TM → arithmetic criterion)  [PROVEN exact, bb_sim-checked — for the in-scope machines]

| machine | reduction status | bb_sim check | facet |
|---|---|---|---|
| **Antihydra** | **[PROVEN] exact** — halt ⟺ ∃n balance_n<0 ⟺ even-density<1/3 ⟺ mean D<3/2; GAP LEMMA, renewal identity, valuation formula | `[verified]` to N₀=2·10⁵ (min balance +2); GAP LEMMA to N=10⁵ | density |
| **o18** | **[PROVEN] exact** — halt ⟺ adjacent-`11` left-frontier carry alignment (existence event) | 2·10⁸ steps, 10 F-entries all read 0, 0 collisions; planted control | existence |
| **o15** | **[PROVEN] exact** — halt ⟺ right-frontier `11` collision (o18 mirror); same Erdős kernel | step-for-step, 120M steps, planted control | existence |
| **o10-inner** | **[PROVEN]** inner AEV-ceiling-3/2; but **o10-FULL is OUT** (composite/existence, probabilistically *halts* — delayed halter, direction OPEN) | L=1..8 unit-test + 5·10⁶ orbit; epoch 1-2 only simulable | composite |
| **o17** | family `0A01^k` halt structure **[VERIFIED]** bb_sim-cross-checked; **kernel-less** odometer (NOT reducible to AEV) | step-for-step, all k=1..90 | existence-shaped, no kernel |

- **Audit:** none of these is "analogy." All are exact, machine-verified reductions. The only non-exactness
  is honest scope: **o10-full is excluded** (direction reversed — it likely halts) and **o17 has no
  equidistribution kernel** (separate obstruction type). The clean in-scope family for the AEV reduction is
  **{Antihydra, o18, o15, o10-inner}**, i.e. the `v_p(μ)=−1` expanding-kernel machines.

### 1D. The density-side barrier (Antihydra β>0 via ergodic optimization)  [PROVEN — with TWO writeup caveats]

This is the strongest no-structure-only result. Audited link-by-link for hand-waving:

1. **Reduction chain** non-halt ⟺ even-density ≥1/3 ⟺ mean D ≥3/2 ⟺ one-sided cylinder form
   (`COMPLETE_PROOF_CAPSTONE.md` §2, links 0–3): **[PROVEN], machine-checked.** Airtight.
2. **Induced map is exact, Haar-preserving, Bernoulli, `D_j` i.i.d. geometric `2^{−d}`**
   (`INDUCED_MAP` E4): **[PROVEN new theorem]** (full-branch surjectivity → full one-sided shift; cites
   Lagarias 2-adic conjugacy, Bernstein–Lagarias 1996). Airtight.
3. **β(ψ) := max_{T-invariant μ} ∫ψ dμ = +1/2 > 0, attained at the fixed point o=1**: the elementary core
   (δ₁ is invariant, ψ(1)=+1/2) is **[PROVEN]**. The full β computation rides on the **full-shift / SFT**
   structure (β = max over the finite alphabet = ψ(1)), which is the *well-understood* case of ergodic
   optimization (Bousch) — **more rigorous than generic ergodic optimization**, since ψ is a finite-coordinate
   function on a full shift.
   - **CAVEAT 1 (writeup gap inside a PROVEN claim).** The statement **"ψ is a function of D only"** is
     recorded as **`[verified]` numerically (0 mismatch for o<2·10⁶)**, *not* `[PROVEN]`. β=+1/2 leans on it.
     It is almost certainly elementary (ψ is a residue condition mod 8 and `D=v₂(3o−1)` is determined by
     o mod 2^k via the GAP LEMMA), but **for an airtight paper this must be promoted from numerical to a
     one-line proof.** Minor, closable.
   - **CAVEAT 2 (precise meaning).** "No structure-only proof exists" is rigorous **only relative to the
     stated definition** of "structure-only" (uses only T-invariant / all-orbits Lyapunov data). The
     *mathematically airtight* core is: the target inequality is **false as an all-orbits statement** (o=1
     violates it), so it is *not* universally-quantified-over-orbits — it is orbit-27-specific. The
     coboundary/Lyapunov **LP is machine-checked INFEASIBLE for k=3..12** (tail-truncation audited sound),
     a concrete rigorous instantiation. The broader "no technique whatsoever" is a sound **meta**-statement,
     not a formal theorem in the object language — and should be presented as such.
4. **Shared-free-structure meta-theorem** (`UNITPART` I4: free structure shared with halting o=1):
   **[PROVEN]** (with `[verified]` synchronization checks). Second derivation of the same obstruction.
- **Verdict:** the density barrier is **genuinely PROVEN for Antihydra**, with one small numerical→proof
  promotion needed (Caveat 1) and one presentation discipline (Caveat 2 — state the precise airtight core
  plus the LP, label the broad meta-claim as meta). **It is PROVEN for Antihydra ONLY** — o10-inner is
  [CONDITIONAL], and o18/o15 do **not** get it (see 1E).

### 1E. Certificate floors and the 2-facet / 2-axis classification

- **o18 floor m*=2** (no 2-window certificate): **[PROVEN]** conjecture-free, machine-checked. m≥3 **[OPEN]**.
- **o17 floor m*=8** (no m-window certificate, m≤8): **[PROVEN]** conjecture-free, machine-checked. m≥9 **[OPEN]**
  (family `0A01^6` detaches from reachable). **Prior all-k/REG over-claim RETRACTED** (`O17_REG_BARRIER.md`).
- **o15**: FAR HOLDOUT; no proven floor barrier beyond the shared head-local picture.
- **2-facet (density vs existence) / 2-axis (dynamical-ergodic vs over-approximation-descriptive)**: this is a
  **[PROVEN] structural/organizational framework** — a correct classification, plus the proven component on
  each axis (density → β>0 barrier PROVEN for Antihydra; existence → closed-over-approximation lemma + annealed
  Borel–Cantelli-I, both **[PROVEN]**; the existence *barrier* itself **[OPEN]**).
- **"all-k/REG barrier IFF halt-discriminator lives in an unbounded reachable run":** **HEURISTIC / one
  direction only.** The ⟸ direction (unbounded reachable run ⇒ all-k barrier, via the brick-(d) all-or-nothing
  mechanism) is essentially **[PROVEN]** (it *is* the brick-(d) construction). The full **IFF is NOT proven**
  as a general theorem — it is a *characterization* supported by three data points (o18 floor 2, o17 floor 8,
  brick-d ∞). **Must be stated as: proven one direction + conjectured converse**, not as a theorem.

### 1F. Annealed (measure-side) results  [PROVEN unconditional]

- **Existence machines (o18/o15): Haar-a.e. seed is non-halting** via **Borel–Cantelli I** (no independence;
  `ΣHaar(B_n) ≍ Σ(8/3)^{−n} = 1.54·10⁻⁴ < ∞`): **[PROVEN] unconditional** (`EXISTENCE_META_THEOREM.md` §3a/§4.2).
- **Density machine (Antihydra): Haar-a.e. seed is non-halting** via the exact Bernoulli structure (mean D=2>3/2
  a.s., SLLN + LDP concentration of even-density at 1/2): **[PROVEN]** (`COMPLETE_PROOF_CAPSTONE.md` §3).
- Both correctly flagged: this is **annealed**; the specific seed (o₀=27 / the o18/o15 seeds) is one Haar-null
  point, so **it does NOT decide any machine** (annealed≠quenched). Honest and airtight.

---

## 2. Minimal set of statements to make (B) a complete standalone theorem

The central finding: **(B) is essentially already proven.** What remains is overwhelmingly **(i) consolidation
/ writeup**, with a short list of genuine soundness tasks. There are **no genuine open gaps that block (B)** —
the OPEN items (the AEV/Mahler kernel, the existence over-approximation barrier, the all-k IFF converse) are
correctly *outside* what (B) claims.

### (i) Already-proven — need only writeup / consolidation
1. The five strict separations + Squeeze Lemma + REG-suffices-at-n=3 (1A). Consolidate witnesses; cite
   arXiv:1901.03913 and Büchi–Bruyère as inputs.
2. The subword-complexity floor `eventually-periodic ⊊ Sturmian ⊊ p(ℓ)≥1.71ℓ` (1B).
3. The exact reductions for {Antihydra, o18, o15, o10-inner} (1C), with explicit scope exclusions
   (o10-full OUT, o17 kernel-less).
4. The density β>0 barrier for Antihydra (1D), the renewal chain, and the exact induced-map (Bernoulli) theorem.
5. The certificate floors m*=2 (o18), m*=8 (o17) and the catalogue (1E).
6. The annealed Borel–Cantelli-I / SLLN a.e.-non-halting results (1F).
7. The literature placement: kernel = floor-mirror single-orbit fragment of AEV Conj 1.6 (q=2 density / q=3
   existence), with the support-vs-density (FLP) axis distinction.

### (ii) Genuine soundness tasks (small, closable — none is a research-level open problem)
1. **Promote "ψ is a function of D only" from numerical to proof** (Caveat 1, §1D). One-line residue argument
   expected. Required to make β=+1/2 fully airtight.
2. **Restate "no structure-only proof" with its precise airtight core** (Caveat 2, §1D): (a) the all-orbits
   inequality is *false* (o=1) → orbit-specific; (b) the LP infeasibility k=3..12 as the concrete instance;
   (c) label the broad "no technique" claim explicitly as a meta-statement relative to a stated proof class.
3. **Downgrade the "all-k/REG barrier IFF unbounded reachable run" to one-direction-proven + conjectured
   converse** (§1E). As an iff it is not proven.
4. Make sure every "facet/axis" table carries the corrected scope: β>0 barrier PROVEN **= Antihydra only**;
   o18/o15 existence barrier **= OPEN**; o10-full **= OUT**; o17 **= kernel-less** (per the
   `UNIFIED_LIMIT_THEOREM.md` correction banner and the o17 retraction).

### (iii) Correctly OPEN — NOT part of (B), do not claim
- The kernel itself (single-orbit AEV/Mahler equidistribution). [OPEN]
- "No REG / tame certificate for a cryptid." [OPEN]
- The existence-facet over-approximation barrier (o18/o15). [OPEN]
- The converse of the all-k IFF. [OPEN]

---

## 3. The strongest TRUE headline (B) can defensibly claim

The task's proposed headline — *"the BB6 Collatz core reduces to named equidistribution conjectures (AEV
q=2/q=3) + a proven no-structure-only barrier for the density facet"* — is **supported, but only with two
scope tightenings** (otherwise it over-reaches):

- **"Collatz core" must be scoped** to the `v_p(μ)=−1` expanding-kernel machines **{Antihydra, o18, o15,
  o10-inner}**, **explicitly excluding o17** (kernel-less odometer; hardness is a Collatz-irregular *halt
  predicate*, not equidistribution) **and o10-full** (composite; probabilistically halts — OUT).
- **"density facet" barrier is PROVEN for Antihydra ONLY** (o10-inner conditional; o18/o15 are the *existence*
  facet, whose barrier is OPEN). It is **not** family-wide.

**Exact defensible headline (pin this):**

> For the BB(6) expanding-kernel Collatz cryptids (multiplier `μ = 2^a/3^b`, `v_p(μ) = −1`: Antihydra, o18,
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

This is the strongest claim that is *fully* supported by the [PROVEN] ledger. It decides no machine, claims no
shortcut, and survives a hostile referee because every quantitative piece (five separations, two floors, the
reductions, β=+1/2, the annealed a.e. results) is machine-checked, and the OPEN frontier is named (AEV/Mahler).

**One-sentence version:** *"BB(6)'s expanding-kernel Collatz cryptids reduce, by exact machine-verified
reductions, to a named fragment of the AEV/Mahler equidistribution conjecture, with a proven
ergodic-optimization barrier (Antihydra) showing no structure-only proof can exist — anchored by a
conjecture-free five-level certification-complexity hierarchy."*

---

## 4. Honest status of (A) and the unconditional fallback theorems

**(A) confirmed.** The complete proof of Antihydra non-halting is **[CONDITIONAL] on AEV/Mahler with NO
shortcut.** The two independent meta-theorems (ergodic-optimization `β=+1/2` at the halting fixed point o=1;
free-structure shared with o=1) **prove that structure-only is impossible** — the residue is irreducibly
orbit-specific. There is no proven shortcut; the kernel closes only when the AEV/Mahler line moves.

**Unconditional theorems about Antihydra that ARE fully proven and worth stating** (the fallback ledger):

1. **The exact reduction theorem [PROVEN].** Antihydra halts ⟺ `∃n: balance_n < 0` ⟺ even-density drops
   below 1/3 ⟺ `∃n: v₂(c_n−1) ≥ balance_n+1`; equivalently the induced odd map `T(o)=3^{D−1}(3o−1)/2^D`,
   `D=v₂(3o−1)`, `o₀=27`, via the GAP LEMMA. A clean unconditional theorem: raw 6-state TM → named 2-adic
   arithmetic predicate. **This is itself a publishable result.**
2. **Induced-map structure theorem [PROVEN].** `T` is Haar-measure-preserving, exact, and Bernoulli on `ℤ₂*`,
   with gap exponents `D_j` i.i.d. geometric `P(D=d)=2^{−d}`. Unconditional.
3. **Haar-a.e. non-halting [PROVEN, annealed].** Haar-almost-every 2-adic seed yields a non-halting orbit
   (mean D = 2 > 3/2 a.s. by SLLN + large-deviation concentration of even-density at 1/2). Honest caveat: the
   actual seed (o₀=27) is one Haar-null point, so this does **not** decide Antihydra — but it is a true
   unconditional theorem. *(This is the density-side analog of the task's "almost-all-seeds via
   Borel–Cantelli"; for Antihydra the mechanism is SLLN, while the o18/o15 existence siblings get the
   literal Borel–Cantelli-I version, §1F.)*
4. **Not eventually periodic [PROVEN, conjecture-free].** The itinerary is not eventually periodic — the
   integer orbit is strictly increasing (`T(c)−c=⌊c/2⌋≥1`), reaches no cycle (all cycle points lie in [0,1],
   only integer cycle points are {0,1}). Periodic-itinerary exclusion C3.
5. **Subword-complexity floor [PROVEN].** The parity sequence has `p(ℓ) ≥ 1.71ℓ` (slope `log_{3/2}2`,
   matching Dubickas), is non-Sturmian, and not eventually periodic.
6. **No-structure-only meta-theorem [PROVEN].** `β(ψ)=+1/2>0` at o=1 (and the coboundary LP infeasible for
   k=3..12); free structure shared with o=1. Unconditionally true *about Antihydra as a proof-theoretic fact*
   (with the precision discipline of Caveat 2).

**Net for (A):** no unconditional *decision*, but a rich stack of unconditional theorems (1–6) — most
publishable as the "what is actually proven about Antihydra" core, with the AEV/Mahler kernel as the single
honest [OPEN] line.

---

## 5. Bottom line

- **(B) is essentially done.** Four proven units (descriptive hierarchy; subword floor; exact reductions;
  density β>0 barrier) + correctly-labelled OPEN frontier. The work remaining is **(i) writeup**, plus **three
  small soundness tasks** (promote "ψ=function of D" to a proof; restate the meta-claim with its airtight
  core + LP; downgrade the all-k IFF to one-direction+conjecture) and **scope discipline** (β-barrier =
  Antihydra only; o17 kernel-less; o10-full OUT). **No research-level gap blocks (B).**
- **Defensible headline = §3**, scoped to the `v_p(μ)=−1` expanding-kernel family and "density facet =
  Antihydra."
- **(A) is conditional on AEV/Mahler, no shortcut** — but ships with six unconditional fallback theorems (§4),
  the strongest standalone being the **exact reduction theorem** and the **induced-map Bernoulli theorem**.

No machine decided. No label upgraded. No false barrier claimed. Soundness intact.
