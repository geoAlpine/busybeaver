# BB(6) cryptid programme — master summary & re-analysis (2026-06-24)

Goal: a **complete proof of BB(6)**. This file synthesises the whole arc, re-analyses what the results mean,
and lays out the next paths. Discipline throughout: **0 machine decisions claimed, 0 false proofs, 2
over-claims self-retracted** (§4c orbit conflation; o4 "decision lead"). Detail in the per-topic notes.

## A. What was done (the arc)
1. **Catalogue (Stage 1) — COMPLETE.** All 19 community cryptids reverse-engineered against the raw TM
   (`CRYPTID_REDUCTIONS.md`, `CRYPTID_CENSUS.md`). Result: exactly **two structural templates** (two-counter
   `1^a01^b`; single drifting defect over `(10)*`). The "poly-time vs exponential" width split is an
   **envelope artefact** — no tractable subclass.
2. **Kernels sharpened (Stage 2).** Antihydra (`antihydra_attack.md` §4), o18 (`o18_attack.md`), o15, o10,
   o17: exact mechanism + sharp halt predicate + equidistribution heuristic + located wall.
3. **Open core mapped.** Every cryptid's halting = a **base-p digit/carry alignment** of a `×2^a/3^b` orbit
   with a moving frontier. Clusters: **Mahler-3/2** {Antihydra,o7,o8,o10}, **Erdős-ternary**
   {o5,o15,o18}, base-3 odometer {o17}.
4. **UNIFICATION (the central result).** Both the Mahler and Erdős clusters collapse to **one kernel**
   (`mahler_equidistribution_attack.md` §8–10, `BB6_OPEN_CORE.md` §6): the **diagonal base-p digit**
   `δ_n = ⌊(2^a/3^b)ⁿ⌋ mod p` equidistributing. Proven for both that (a) the real β-map has a spectral gap
   but is digit-blind, (b) the p-adic `×2^a` is a zero-entropy isometry whose fixed digits are periodic, and
   `δ_n` is the **diagonal read** of that isometry — the one open object.
5. **Live path found — 2-adic shift-renewal** (`antihydra_renewal_attack.md`). The *actual* orbit
   `c→⌊3c/2⌋` (unlike pure `(3/2)ⁿ`) carries a **mixing 2-adic shift**: `T(x)=⌊3x/2⌋` is a **rigorous
   measure-preserving exact endomorphism of ℤ₂**. The low-bit Markov chain has a **near-total spectral gap
   (0.99)** with uniform stationary ⇒ even-density `½`, depth `o(n)` ⇒ non-halt — and the real orbit matches.
6. **Bootstrap closure attacked** (§6) and **re-analysed** (§7): the depth is a **renewal process** —
   PROVEN deterministic countdown (`d≥1 ⇒ d↦d−1`) + geometric jumps `D=v2(3c'−1)` at even-steps.

## B. Re-analysis — what the totality means
- **Everything is one wall, in many faces.** Diagonal-digit equidistribution (arithmetic) = exact-`ℤ₂`-
  endomorphism seed-non-exceptionality (dynamical) = renewal jump-heights well-distributed (probabilistic) =
  "even-subsequence `c'_j` doesn't approach `3⁻¹` 2-adically too fast." All **provably equivalent**, all the
  **specific-orbit-vs-a.e.** gap. This is the same class as famous open **specific-point normality**
  questions (e.g. "is 2 normal to base 3?").
- **Two genuine assets the wall did NOT consume:**
  1. **A weakened target.** Non-halt needs only **average jump height `< 2`** (true value 1) /
     balanced+decorrelated incoming bits — *one-sided & averaged*, strictly weaker than full equidistribution.
  2. **A proven skeleton.** The depth countdown is deterministic; **all** the difficulty is in the geometric
     jump heights `D_j=v2(3c'_j−1)` at even-steps — i.e. in a single subsequence `c'_j` mod `2^k`.
- **The shift matters.** The iterated orbit has a mixing mechanism the pure power lacks; this is why the
  renewal framing is more promising than bare Mahler — the difficulty is *concentrated* (jumps only), not
  spread over every step.

## C. Honest status
Complete proof remains gated behind this single kernel, which is **world-open** (specific-orbit
equidistribution of a `2^a/3^b` orbit; same class as Mahler-3/2 1968 & Erdős-ternary 1979). No in-session
breakthrough. But the programme has compressed BB(6)'s entire open core from "19 machines / 2 problems" to
**one crisp, measured, multiply-equivalent kernel** with a proven renewal skeleton and a weakened target.

## D. Next paths (ranked, honest probability)
1. **Induced-map / jump-height attack [most concrete].** Study the first-return-to-even map `F(c'_j)→c'_{j+1}`
   directly; the only thing to bound is `v2(3c'_j−1)`'s tail. `F` collapses the proven countdown, so it may
   have cleaner (possibly expanding/mixing) structure than the raw orbit. Target the *one-sided averaged*
   statement (avg jump `<2`), not full equidistribution. **Best shot at a genuine partial.**
2. **(×2,×3) effective equidistribution [most credible "real math"].** Furstenberg–Rudolph–Lindenstrauss–
   BLMV is the tool family built for exactly this 2-vs-3 structure; only superficially tried. It is a.e./
   measure-theoretic, so reaching the specific seed needs a Diophantine-genericity input — but the unified
   solenoid picture is now set up for it. **Deep frontier; low but nonzero.**
3. **Port shift-renewal to Erdős (base-3 shift) [breadth].** Confirm o18/o15 have the same renewal skeleton;
   would put both clusters under one mechanism and might expose a cluster with a favourable growth/trap ratio.
4. **Consolidate as a citable problem statement [capitalise].** Write the reduction "BB(6) cryptid core ⟺
   specific-point equidistribution of `⌊(2^a/3^b)ⁿ⌋ mod p`" as a self-contained problem for number theorists.

## E. Paths attacked in probability order (2026-06-24) — both top paths hit the SAME wall
**Path 1 (induced map / jump heights) — attacked, cleanest framing, wall intact** (`antihydra_renewal_attack.md`
§8). Derived the first-return-to-even map `F(c')=(3^D u+1)/2`, `D=v2(3c'−1)`. Jumps iid-geometric (mean
1.005<2). But growth is **parity-blind** (`log₂ c_n=0.585n+3` regardless of parities) ⇒ no lower bound on
even-density; the bookkeeping `ΣD_i=n_j−j` is a tautology; jump-sums fluctuate like `√N` (no drift/
supermartingale). Cleanest possible framing, but the complete proof still needs `c'_j mod 2^k` equidistribution.

**Path 2 ((×2,×3) effective equidistribution) — no applicable theorem; it IS Mahler.** Furstenberg/Rudolph/
Host/BLMV are about **invariant measures / a.e. points**. The specific orbit `{(3/2)ⁿ}` furnishes **no
(×2,×3)-invariant positive-entropy measure** (a single trajectory has zero entropy; its closure is not
`×2`/`×3`-invariant in any usable way), so rigidity cannot bite. Equidistributing the specific orbit IS
Mahler's 1968 problem — no unconditional theorem applies. Same wall as path 1.

## F. Verdict (honest)
The two highest-probability routes to the complete proof both **converge to the identical world-open kernel**:
specific-orbit equidistribution of a `2^a/3^b` orbit (= Mahler-3/2 / Erdős-ternary / the unified diagonal
digit). Path 1 produced the **cleanest reduction the programme has** (renewal map, iid jumps, one-sided
averaged target) but cannot break the circularity; path 2 has **no applicable unconditional theorem**. There
is **no in-session route to an unconditional complete proof** — it requires resolving a ~50-year-open problem.
This is the genuine mathematical frontier, now reached and documented, with `0` decisions and `0` false proofs.
