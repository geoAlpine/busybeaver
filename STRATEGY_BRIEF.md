# BB(6)/Antihydra — strategy brief (2026-06-25)
*A one-page status + decision memo, for planning next moves (incl. with ChatGPT). The full technical note is
`STATE_FOR_REVIEW.md`; the append-only attack log is `RESEARCH_LOG.md`. Discipline throughout: 0 false proofs;
~10 tempting leads retracted after verification; every claim below is machine-checked (exact arithmetic) or
explicitly labelled measured/open.*

## 1. One-paragraph status
We set out to prove the open kernel behind BB(6) — that **Antihydra** (`c_{n+1}=⌊3c_n/2⌋`, `c_0=8`) never halts,
i.e. its running **even-density ≥ 1/3** forever. Over this programme we reduced it to a single sharp object,
built five exact reformulations, and attacked it from additive combinatorics (Q8), the transfer-operator /
Gibbs–Markov route (Q9), and head-on (α). **The lines have converged**: the kernel is now a *fully-specified*
open problem with a complete obstruction map on both the arithmetic and the dynamical side, and exactly **one
named missing tool**. We did **not** prove Antihydra (it is genuinely Mahler-1968-class), and we are honest
that we did not.

## 2. What is proven / verified (the assets we own)
- **Exact halting criterion:** non-halt ⟺ `balance_n=3E_n−n ≥ 0 ∀n` ⟺ running even-density ≥ 1/3.
- **Renewal map `F` on ℤ₂** (the induced `×3/2` map) is **full-branch, piecewise-affine, expanding,
  Haar-preserving** (verified exactly): on cylinder `P_D={v2(3c'−1)=D}`, `F(c')=(3^{D+1}c'−3^D+2^D)/2^{D+1}`,
  slope `(3/2)^{D+1}`, zero distortion, each branch onto all of ℤ₂. (Structurally a Gibbs–Markov system.)
- **`F` advances the renewal sequence:** `c'_{j+1}=F(c'_j)` (verified 1999/1999), so the §6.5 additive energy
  is *literally* the renewal sequence's 2-adic self-correlation `#{(i,j): v2(c'_i−c'_j)≥k}`.
- **Two exact identities (NEW, this week):**
  - `Σ_{j<J} v2(3c'_j−1) = #odd steps` ⇒ **`avg jump = #odd/#even` exactly**, `even-density = 1/(1+avg jump)`.
  - telescoping `2c'_{j+1}−1 = (3/2)^{D_j}(3c'_j−1)`.
- **Appendix-B numerics:** the orbit's cylinder-visit moments `M_2,M_4` match the random-iid model to 0.4–5%
  over k=2..14, with `M_4` *below* random (the favorable side). Measured for the one orbit; that is the open part.

## 3. The convergence (Q8 → Q9 → (i)/(ii) → (α)) — what each step settled
1. **§6.5 / Q8 (additive combinatorics).** Non-halt follows from a **4th-moment additive-energy bound**
   `M_4 = O(J^4/2^{3k})` (constant `C ≤ 3.45`; measured `C ≈ 1.3`). Strictly weaker-looking than full
   equidistribution → the concrete target.
2. **Q9 (transfer operator).** `F` is Gibbs–Markov; on 2-adic-Lipschitz functions the spectral gap gives
   exponential decay of correlations *for Haar* — but the energy is along the **specific** orbit.
3. **Q9(b) obstruction [PROVEN, negative].** The spectral gap is a property of `(F,Haar)` **alone** = orbit-blind.
   `F` has a fixed point on **every** branch (`0,1/5,5/19,19/65,…`, exact 2-adic integers) and periodic points of
   all periods; these **violate** the `M_4` bound (`M_4=J^4/p^3`). Even integer seeds that *shadow* them
   over-concentrate (`≡1/5 mod 2^60` ⇒ `~7000×` random on a window). ⇒ the gap **cannot** imply the bound; the
   bound is intrinsically **orbit-specific**.
4. **(i)/(ii) sufficiency [PROVEN, both NO].** Is a non-shadowing/Diophantine seed condition (i) sufficient,
   (ii) weaker than equidistribution? **No and no.** We *construct* (via the full-branch coding + inverse
   branches) an orbit that is **dense in ℤ₂, fully supported, aperiodic = maximally non-shadowing** yet has
   `avg jump = 3.10 > 2` — violating the bound. And `avg jump` is **dominated by small k** (k≤3 ≈ 88%), where
   `N_k` = fixed-cylinder count = **fixed-k equidistribution** = the original open class. The genuinely-weaker
   large-k separation tail is negligible.
5. **(α) head-on [the wall, fully mapped].** (α) = *force the single seed-8 orbit's empirical measure to Haar.*
   - the two exact identities ⇒ every reformulation **collapses to even-density ≥ 1/3 as an exact identity**
     (no slack, no-free-lunch);
   - the telescoping makes the **growth/counting argument a tautology** (`n=J+ΣD_j` cancels `ΣD_j`) ⇒ elementary
     attacks are **provably circular**;
   - the three single-orbit-equidistribution mechanisms are each **structurally unavailable**: unique ergodicity
     (F has a continuum of invariant measures), rank-≥2 rigidity (orbit is rank 1), character cancellation
     (van der Corput closed on `(3/2)^n`).

## 4. The single open residue (what would actually break it)
> A **rank-1 effective-equidistribution** theorem forcing **one specific** `×(2^a/3^b)` orbit's empirical
> measure to Haar, using a **Diophantine input on `log₂3`** — beyond the rank-≥2 scope of measure rigidity and
> beyond the off-diagonal reach of Fourier/sieve. Equivalently: control the **moving 2-adic diagonal digit**
> `⌊(3/2)^n⌋ mod 2` of a single orbit. This is Mahler-1968-class. Nothing in the literature reaches it for a
> single orbit (the closest, Tao-2019 Collatz, decides almost-all, not one orbit).

## 5. Strategic options (for the planning session)
**A. Take it to experts now (lowest cost, high information).** The note is ready and, crucially, is now framed
as **questions a dynamicist/number-theorist can answer yes/no**, not as "please solve Mahler": e.g. *is there
any rank-1 effective-equidistribution mechanism with a Diophantine input that applies to a single Gibbs–Markov
orbit?* and *is the large-k separation tail (Baker / linear-forms-in-logs on `v2(c'_i−c'_j)`) provable
unconditionally even though it is not binding?* Target: bbchallenge community (Sterin, sligocki, mxdys), an
ergodic-theory specialist, ChatGPT-as-first-pass. **Recommended first.**

**B. Multi-year build of the missing tool** (the "settle in and make new mathematics" path). Concretely: develop
rank-1 effective equidistribution for `×3/2` on ℤ₂ with a `log₂3`-Diophantine hypothesis — the single, named,
sharply-scoped open problem from §4. High risk, high reward; this is the real prize.

**C. Cross-cryptid test — a *new* (non-circular) attack surface.** Port the same dissection to the **Erdős 8/3
side (o18 / ternary-digit-of-`2^n`)** and other cryptid clusters, and check whether the kernel is **isomorphic
across cryptids** (same `δ_n=⌊(2^a/3^b)^n⌋ mod p` object, same obstruction map). If yes: one tool kills a whole
family, and the "certificate-complexity hierarchy for non-halting" (already drafted) gets a second, independent
instance — strengthening the *theory* deliverable even while the single proof stays open. Fresh terrain, not the
circular wall.

**D. Bank the meta-result.** Even with the proof open, the verified deliverable is real: *a fully-specified
kernel + complete two-sided obstruction map + the certificate-complexity-hierarchy framing* (regular ⊊
semilinear ⊊ cryptid). That is a publishable/recordable artifact independent of resolving Antihydra, and aligns
with the programme's "framework + theory" centre of gravity.

## 6. Recommendation
Run **A and C in parallel**: A is cheap and tells us whether anyone has the rank-1 tool (or a reason it's
impossible); C is the only remaining *non-circular* attack we can run ourselves and it feeds the theory
deliverable (D) regardless. Hold **B** for a deliberate decision *after* A returns signal — committing multi-year
effort should follow expert triage, not precede it. **Do not** keep attacking (α) solo inside one session: we
just proved that elementary route is circular.

## 7. Honesty ledger
Proved: the reformulations, the renewal/Gibbs–Markov structure, the two identities, the Q9(b) obstruction, the
(i)/(ii) negatives, the circularity of growth arguments. **Not** proved: Antihydra non-halt, fixed-k
equidistribution, (α). No claim is made beyond what is labelled. The programme's honest output is **"the wall is
now specified on every side; breaching it is new mathematics, not a missed trick."**
