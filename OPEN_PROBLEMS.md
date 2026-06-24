# BB(6)/Antihydra programme — the remaining open problems, in detail (2026-06-25)
*A working list for a strategy session. Companion to `STATE_FOR_REVIEW.md` (technical note), `STRATEGY_BRIEF.md`
(decision memo), `EXPERT_ASK.md` (the throwable question), `CRYPTID_KERNEL.md` (cross-cryptid result),
`LIMIT_THEOREM.md` (certificate hierarchy). Every item is labelled **[OPEN]/[CONDITIONAL]/[PROVEN]** and tagged
with **status / what we ruled out / what would close it / difficulty / who answers it**. Discipline: 0 false
proofs; ~10 leads retracted on verification; nothing below is claimed beyond its label.*

---

## 0. Orientation — what is settled, so we can see what is not
**Settled (verified, this programme):** the exact halt criterion (even-density ≥ 1/3 ⟺ avg jump ≤ 2 ⟺
`Σⱼv2(3c'ⱼ−1)=#odd`); the renewal/Gibbs–Markov structure of the induced map on `ℤ_p`; the cross-cryptid
classification (`T_μ` clean `p`-to-1 iff `v_p(μ)=−1`; Antihydra/o10-inner = `3/2`, o18/o15 = `8/3`); the
**obstruction map** — spectral gap orbit-blind, non-shadowing insufficient (by construction), growth-argument
circular, soft mechanisms unavailable; the literature anchoring (= single-orbit Mahler 3/2; Tao 2022 closest,
a.e.-only). **The entire difficulty is now localized into the items below.**

The open problems fall in five buckets: **A** the central wall, **B** possibly-easier partials, **C** finishing
the cryptid classification, **D** the certificate-hierarchy (recordable theory), **E** strategy/meta.

---

## A. The central open core — the hard wall (one problem, several faces)

### A0 · [OPEN] **THE SUMMIT — what the complete proof actually requires** (re-centred 2026-06-25)
The goal is the **complete proof** of Antihydra non-halt, not a partial. Exactly (verified):
```
non-halt  ⟺  balance_n = 3E_n − n ≥ 0  for all n  ⟺  avg jump ≤ 2  (running, all prefixes),
            avg jump = (1/J) Σ_{k≥1} N_k ,   N_k = #{j<J : c'_j ≡ 3^{-1} mod 2^k}.
```
**Key reframing (verified):** `avg jump = (1/J)Σⱼ v2(c'ⱼ − 1/3)` = the orbit's **average 2-adic proximity to the
single fixed point `1/3 ∈ ℤ₂`**; `N_k/J` = visit frequency to the shrinking ball `2^{−k}` around `1/3`. So the
complete proof is a **single-target shrinking-target / one-sided anti-concentration** statement.
- **What the complete proof needs vs the neighbours (verified true value `avg jump ≈ 1.004`):**
  | target | bound | what it is |
  |---|---|---|
  | positive density (B2) | `avg jump ≤` any const | a *partial*, **NOT** the proof |
  | **complete proof (A0)** | **`avg jump ≤ 2`** | one-sided, **factor-2 margin** over the truth |
  | equidistribution (A1) | `avg jump → 1` | the knife-edge, *stronger* than needed |
- **Crucial point (verified):** the complete proof does **NOT** require A1 (equidistribution). The condition
  `avg jump ≤ 2` is **strictly weaker as a condition** — we *constructed* a non-Haar orbit with `avg jump = 1.56`
  that satisfies it without equidistributing. So `{measures with avg jump ≤ 2} ⊋ {Haar}`.
- **The budget decomposition (verified):** complete proof `⟸ [k=1 term ≤ 1, trivial] + [Σ_{k≥2} N_k/J ≤ 1]`
  (true value of the tail `≈ 0.50`, so a **2× margin**). The tail splits again: **large-k** = deep approaches to
  `1/3` = the **Baker / separation** regime (B1, accessible); **k=2,3** = the irreducible **small-k** core.
- **★ THE SHARP OPEN QUESTION (the real frontier for the complete proof):**
  > Is the one-sided, margin-2 bound `avg jump ≤ 2` (equivalently `N_k/J ≤ C·2^{−k}` summing to `≤ 2`)
  > **provably easier** for the seed-8 orbit than full equidistribution `avg jump → 1`, **or** does the
  > small-k part `k=2,3` make it just as hard?
  - If **easier** → the complete proof is reachable **without solving Mahler 3/2** (a margin-exploiting,
    one-sided argument on the orbit's distribution mod `4, 8`). This is the *best* hope for a real proof.
  - If **just as hard** → the complete proof `=` A1 `=` new mathematics (multi-year).
  - **Status:** UNRESOLVED. We proved non-shadowing is insufficient and that small-k binds; we have **not**
    shown the one-sided/margin version equals equidistribution, nor found an argument that exploits the margin.
    *This is the single most important question for the complete proof — put it to the meeting first.*

### A1 · [OPEN] Single-orbit rank-1 effective equidistribution
**Statement.** For `μ=2^a/3^b` with `v_p(μ)=−1`, does the empirical measure of the **one** forward orbit
`x, T_μx, T_μ²x, …` (`T_μ=⌊μ·⌋` on `ℤ_p`, specific seed e.g. 8) converge to Haar? Equivalently: does
`⌊μⁿ⌋ mod p` equidistribute for that single orbit? Equivalently (Antihydra): even-density `→ 1/2` (≥ 1/3
suffices for non-halt).
- **Status.** This **is** the single-orbit case of **Mahler's 3/2 problem (1968)** — open 57 years.
- **Ruled out (so don't retry):** transfer-operator spectral gap (orbit-blind — gives only μ-a.e.); any
  "spread/non-shadowing" condition (we *built* a dense, fully-supported, aperiodic orbit with avg jump 3.10);
  growth/counting (provably circular: `n=#even+#odd=J+ΣD` cancels); unique ergodicity (continuum of invariant
  measures); rank-≥2 rigidity (orbit is rank 1); Weyl/van-der-Corput (closed on `(3/2)ⁿ`).
- **Closest known result.** Tao 2019/2022 (arXiv:1909.03562) — controls the **same** p-adic
  renewal/Gibbs–Markov statistic, but for a **log-density-1** set of seeds. **Exact gap = remove the density
  average to pin one seed.** FLP 1995 gives only a *range* bound (`1/p`), not a density.
- **What would close it.** A genuinely new **rank-1, single-orbit, effective** equidistribution mechanism that
  takes a **Diophantine input on `log_q p`** (`log₂3` for Antihydra) and is intrinsically `p`-adic (engages the
  moving diagonal digit, not the off-diagonal). No such mechanism is known.
- **Difficulty / who.** Very hard (Mahler-class). Ergodic-theory / analytic-number-theory specialists; the
  honest near-term action is to *ask*, not to solve solo.

### A2 · [OPEN] Could the *one-sided* / weaker forms be more tractable? (sub-questions a specialist can rule on)
These are strictly weaker than A1 and are the real content of `EXPERT_ASK.md` Q1:
- **A2a.** Does the spectral gap + a **large-deviation rate function** for Gibbs–Markov give a *one-sided* upper
  bound `M_4 ≤ C·J⁴/2^{3k}` for a single orbit under a non-shadowing/Diophantine seed hypothesis? *(We proved
  non-shadowing alone is insufficient and small-k binds; the question is whether some Diophantine strengthening
  + LDP closes it, or whether it provably needs full equidistribution.)*
- **A2b.** Is there a Tao-style transport/entropy-decrement argument that survives **fixing the seed** given a
  Diophantine hypothesis — i.e. is the density average removable in principle for a Diophantine seed?
- **A2c.** [meta] Is single-orbit equidistribution here *provably* as hard as Mahler 3/2 (a reduction), or only
  "in the same class" heuristically? A clean reduction either way is itself a result.

---

## B. Possibly-easier sub-problems — genuine partial-result targets (do not need A1)

### B1 · [OPEN] The large-k separation bound via p-adic Baker (the non-binding tail)
**Statement.** Prove unconditionally `#{(i,j) : v2(c'ᵢ − c'ⱼ) ≥ k} = O(J²/2^k)` (anti-clustering of orbit
differences). The differences `c'ᵢ − c'ⱼ` are **S-unit-like**.
- **Status.** [OPEN] but possibly accessible — this is the **large-k** part, which is *not* binding for avg
  jump (small-k equidistribution binds), so a clean result here is a **genuine partial that does not require
  A1**.
- **What would close it.** A **p-adic Baker / linear-forms-in-logarithms** lower bound on `v2(c'ᵢ − c'ⱼ)` for
  this orbit. Subtlety flagged: `c'ⱼ = A_j(9/4)^j` with `A_j` self-referential (not a clean S-unit), so a
  direct Baker application is *not immediate*.
- **Difficulty / who.** Medium-hard; analytic number theorist (transcendence/linear forms). `EXPERT_ASK.md` Q2.

### B2 · [OPEN] Any unconditional *positive* even-density bound? (improve `Ω(log n)`) — **scaffold, not summit**
**Statement.** Prove even-density `≥ c` for some explicit `c > 0` (currently only `E_n = Ω(log n)`, i.e.
density `→ 0` is all that's unconditional). Even `c = 0.01` would be a real first. **NB: this is a partial that
does NOT prove non-halt** (non-halt needs `c ≥ 1/3`, A0). It is a scaffold / feasibility probe — if even
`c > 0` is circular, the margin in A0 is illusory; if `c > 0` is reachable via the Baker tail (B1≡B2 below),
the A0 summit is one small-k bound away.
- **Ruled out.** Growth/counting arguments (provably circular, A1). The trivial 2-adic bound gives nothing
  positive.
- **What would close it.** Unclear — possibly an averaged/second-moment argument that gets a one-sided density
  without full equidistribution. *Open whether any route exists.* High-value if any `c>0` is reachable.
- **Difficulty / who.** Unknown; this is the most "maybe there's an elementary-ish trick" item — worth a
  focused attempt and a specific ChatGPT brainstorm.

### B3 · [CONDITIONAL→?] Are any of the sufficient hypotheses themselves provable?
We have several **conditional theorems** (each hypothesis ⟹ non-halt). Open: is any hypothesis provable?
- **(H)** incoming high digit `bit_k(c_n) ⊥ c_n mod 2^k` (asymptotic independence). [measured: MI≈0]
- **The 4th-moment bound** `M_4 = O(J⁴/2^{3k})`, constant `C ≤ 3.45` (measured `C ≈ 1.3`). [the §6.5 target]
- Each is *equivalent-in-class* to A1, but the **constants have slack** (3.45 vs 1.3) — is the slack
  exploitable, i.e. is the *one-sided* moment bound with a loose constant easier than equidistribution?
- **Difficulty / who.** Same class as A1, but the loose-constant one-sided version is the most likely "weaker
  but still useful" target — a specific question for the additive-combinatorics / Gibbs–Markov experts.

---

## C. Finishing the cryptid classification (the theory deliverable — mostly tractable by us)

### C1 · [verifiable by us] o15 width-sequence rigorous extraction
**Task.** Simulate the o15 TM, extract its width/exponent sequence, and confirm it follows the `×8/3` Mahler
map (ratios `→ 8/3` measured: `107,289,772`). Confirms o15 ∈ the `8/3` kernel class at the level of the raw
machine, not just the census fit. **Status:** plausible, not yet done at TM level. **Difficulty:** low (we have
the simulators). **Guards a soundness corner** (avoid a census-fit artifact, per `SOUNDNESS_INCIDENT`).

### C2 · [verifiable by us] o17 odometer — is it actually *less* hard?
**Observation (new).** o17's base object is a **uniquely-ergodic odometer** ⇒ equidistribution is *automatic*;
its hardness is the **Collatz-irregular halt predicate** (`0 A 0 1^k`, `k mod 3`). **Open question:** is the
halt predicate itself decidable by a *different* tool than equidistribution (a modular/automatic-sequence
argument), making o17 the **most likely cryptid to actually fall**? Worth a dedicated attempt distinct from the
Mahler wall. **Difficulty:** medium; **leverage:** if o17 falls, that's a *decided BB(6) holdout* (route i).

### C3 · [verifiable by us] The full `(a,b,p)` family and which holdouts populate it
**Task.** Map each of the 19 named cryptids (and ideally the 1104 holdouts) to its `(μ, p)` kernel class or
mark it "odometer / other / unreduced." We have the Mahler core (4) and o17 (odometer); the **slow-width 15**
are unclassified at the kernel level (`CRYPTID_CENSUS`: all genuinely hard, but their kernel object is
unextracted). **Difficulty:** medium (per-machine reverse-engineering); **deliverable:** the complete "BB(6)
Collatz/Mahler frontier = these named kernels" catalogue — a publishable artifact.

### C4 · [OPEN] Are the slow-width 15 a *third* obstruction type?
**Question.** The slow-width majority resisted all deciders and are IRREGULAR but their kernel is unextracted —
are they (a) Mahler kernels in disguise, (b) odometers, or (c) a genuinely new type? **Difficulty:** high
(needs the §3c reduction per machine); **value:** completes the classification / could reveal a new structure.

---

## D. Certificate-complexity hierarchy — recordable theory, conjecture-free bricks (`LIMIT_THEOREM.md`)

### D1 · [OPEN→achievable] Brick (a): an explicit `SLIN ⊋ REG` certificate witness
**Task.** Construct a concrete non-halting machine with a **provably non-regular** reachable language **and** an
explicit **semilinear** certificate — a clean, conjecture-free proof that semilinear certificates are strictly
stronger than regular ones. **Status:** identified as achievable; not done. **Difficulty:** medium.

### D2 · [OPEN→achievable] Brick (c): "no REG certificate with ≤ N states" finite search
**Task.** A finite, complete search proving no DFA certificate of ≤ N states certifies a chosen cryptid — a
computable **lower bound on `reg(M)`**. **Status:** designable; exponential but bounded. **Difficulty:**
medium; **value:** the first concrete `reg` lower bound for a cryptid.

### D3 · [OPEN] The hierarchy top — "no tame certificate for a cryptid"
**Statement.** No certificate of any tame class (REG/SLIN/…) witnesses a cryptid's non-halting. This is the
**over-approximation axis** and is `≥` as hard as resolving the cryptid (= A1). **Now sharpened (D-integration):**
it is **one shared vertex** indexed by `(a,b,p)`, literature-anchored (Mahler 3/2 / Tao / 2025 normality
conjecture). **Status:** [OPEN], = the genuineness-limit avatar. Not expected to fall without A1, but the
*framing* (single named vertex) is the recordable contribution.

---

## E. Strategic / meta open questions (for the ChatGPT session)

1. **Routing (complete-proof first).** The headline question for the meeting is **A0's sharp question** — is
   the one-sided/margin-2 bound `avg jump ≤ 2` provably easier than equidistribution, or does small-k (`k=2,3`)
   make it equally hard? Put this **first** (to an ergodic-theory / additive-combinatorics specialist and to a
   ChatGPT brainstorm: are there *margin-exploiting one-sided* arguments — one-sided ergodic theorems,
   sub-additivity, a Lyapunov/drift on the renewal map `F` — that bound a single orbit's visit frequency to a
   fixed small cylinder from one side without proving equidistribution?). Then the supports: B1 (Baker tail) to
   a transcendence specialist; B3 (loose-constant moment) to additive combinatorics.
2. **The o17 lottery.** Is C2 (decide o17 via its halt predicate, bypassing equidistribution) worth a dedicated
   sprint? It is the **only** remaining route to *deciding an actual BB(6) holdout* (route i) we haven't
   exhausted at the predicate level.
3. **Publication / recording.** The verified deliverables (exact criterion + cross-cryptid classification +
   two-sided obstruction map + certificate-hierarchy framing + literature anchoring) are real and independent
   of resolving any cryptid. Record as a note now, or wait for expert signal on A? What venue (arXiv math.DS /
   bbchallenge writeup / internal record only, per the publication-stance memo)?
4. **Stop conditions.** What result would make us *stop* (a clean reduction "this = Mahler 3/2", an expert "no
   tool exists", or a positive partial in B)? Define the success/stop criteria before investing more.
5. **The unverified claim.** arXiv:2411.03468 claims to resolve Mahler 3/2. Worth one careful read to confirm
   it is flawed (if it were correct, A1 would be *closed* and Antihydra would essentially follow)? Low
   probability, high payoff-if-true — a bounded-cost check.

---

## One-line status (re-centred on the complete proof)
**The summit is A0: `avg jump ≤ 2` (one-sided, factor-2 margin) — the complete proof, which is strictly weaker
than equidistribution (A1) yet still has a small-k core we have not cracked.** The decisive question is whether
that one-sided/margin gap makes the complete proof reachable *without* solving Mahler 3/2 — **UNRESOLVED, and
the first thing to put to the meeting.** Everything else is support: A1 is the knife-edge (harder than needed);
B1≡B2 (the Baker tail) is the scaffold that would secure the large-k half and give positive density; C is the
cross-cryptid classification (one tool lifts the family); D is the recordable certificate-hierarchy theory.
**For the complete proof specifically, the live target is the small-k one-sided bound `Σ_{k≥2} N_k/J ≤ 1`** —
not the partials.
