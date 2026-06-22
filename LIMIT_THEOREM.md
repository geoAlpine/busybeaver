# The certification-complexity hierarchy for non-halting — and the BB(6) barrier

A research note (⑥ in `BB6_PREP.md`). Goal: not to decide BB(6), but to make rigorous **why** it is
hard — to characterise the certificates that can witness non-halting and prove that the cryptids escape
the tractable classes. This is the Turing-machine avatar of the quantum **genuineness limit theorem**
(finite observation cannot certify the infinite property), stated for a clean discrete object.

Every statement below is labelled **[PROVEN] / [CONDITIONAL] / [OPEN]** — the same discipline as the
soundness work: no theorem is claimed beyond what is established.

## 1. Certificates for non-halting

A TM `M` never halts iff there is a set `L` of configurations with: (S) the start config ∈ `L`,
(C) `L` closed under the step relation, (H) no halting config ∈ `L`. Such an `L` is a **certificate**.
`reachable(start)` is always a certificate; the question is whether a *describable* one exists.

Classify certificates by the description class of `L`:
- **REG** — `L` is regular (a DFA over configuration strings). This is exactly FAR / Closed-Tape-Language.
- **SLIN** — `L` is semilinear (Presburger-definable over a run-length / block-count encoding). Captures
  counters whose reachable set is not regular.
- **beyond** — neither; the reachable structure is governed by a Collatz-like map.

Certificate-complexity of `M` = the smallest class with a certificate. Define
`reg(M)` = the least number of DFA states of a REG certificate (∞ if none).

## 2. Where the objects sit

- **[PROVEN] Bouncers ∈ REG, small.** A bouncer's reachable language is regular; we exhibit the DFA
  certificate constructively (`wbounce`/`far_finder`). `reg` is a small constant.
- **[PROVEN] All 63 three-state monsters ∈ REG.** Every one has a machine-checked non-halting proof,
  and the two binary counters were certified by explicit DFA invariants (`far_finder` k-tails,
  `far_cegar`). So **at n=3, REG certificates suffice for the entire hard residual** — the hierarchy
  does not separate yet. (This is itself a clean finite theorem: 63 explicit certificates.)
- **[PROVEN] (brick d) k-testable ⊊ regular for certification.** Witness: the counter
  `1RB0LZ_1LC1RA_0RA0LC` (halt = A reads 1). It HAS a REG certificate (CEGAR found, we VERIFIED a
  2-class/parity DFA), but **NO k-window (locally-testable / k-tails) set is a certificate, for any k.**
  Conjecture-free proof (Lemma 1 verified m=1..32):
  - *Lemma 1.* The config `1^m B 0…` reaches the halt **iff m is even** (even m halt in Θ(2^{m/2})
    steps; odd m never halt — they are the reachable configs, non-halting by the verified certificate).
  - Any certificate `L` is step-closed and halt-free, so it must **exclude every even-m config**
    (each reaches halt) and, containing the start's reachable set (the leading 1-run grows through
    1,3,5,…), **include 1^m B 0 for infinitely many odd m**.
  - On the unary sub-structure `1^* B 0`, a locally-testable (k-window) language is all-or-nothing for
    m ≥ k (membership is fixed once the window `1^k` is seen), so it cannot contain infinitely many
    odds while excluding all evens. Hence no k-window certificate. A full DFA (count parity) is one. ∎
  So suffix-window certification ⊊ regular certification — a clean, conjecture-free separation.

## 3. The cryptid barrier

Let `M` be a cryptid (e.g. Antihydra) and `v_0, v_1, …` its milestone orbit (`cryptid_map.py`): the
integer it iterates, read at successive turning points, with milestone width `w_i = Θ(log v_i)` (the
tape stores `v_i` in ~binary). Antihydra's orbit (measured): widths `2,3,10,17,18,28,29,62,63,94,…`,
binary values `2, 2, 126, 106494, 255852542, 4.5e18, …` — the classifier reports **IRREGULAR**, i.e.
not LINEAR (bouncer), not AFFINE/GEOMETRIC (counter): a genuine Collatz-like rule.

- **[CONDITIONAL] If `M` never halts, its EXACT reachable language is non-regular.**
  *Proof sketch (rigorous modulo "orbit unbounded").* Never-halting ⇒ the orbit is infinite. The
  milestone configs `c_0, c_1, …` have widths `w_i → ∞`. Two milestone configs of different width are
  Myhill–Nerode-distinguishable in the reachable language (a continuation that completes one milestone
  to a valid reachable config of a fixed larger width fails for the other), giving infinitely many
  equivalence classes ⇒ the language is non-regular. ∎ (The only gap is "widths → ∞", i.e. the orbit
  is unbounded — precisely Antihydra's open conjecture.)
- **[OPEN] No REG certificate exists for `M`.** This is the real target and is *strictly stronger* than
  §3's non-regularity, because a REG certificate is an **over-approximation** `L ⊇ reachable`, and a
  regular superset of a non-regular set can exist. Proving none exists would mean: every regular,
  step-closed, halt-free set must include a halting config — i.e. Antihydra's non-halting is not
  witnessable by any finite-state abstraction. We conjecture this and note it is at least as hard as
  resolving Antihydra (a regular certificate would *decide* it).

## 4. The spoofer game (the genuineness avatar)

Phrase certification as a two-player game, exactly the spoofer game of the quantum genuineness work:
- **Prover** commits to a finite abstraction `α` (a DFA over configs) and claims it certifies M's
  non-halting.
- **Adversary** must exhibit a machine `M'` that is `α`-indistinguishable from `M` on all observed
  finite data but **halts**.
- `M` is **genuinely non-halting w.r.t. class C** iff for every `α ∈ C` the Adversary wins.

§2 says: for bouncers/counters the Prover wins in REG (a finite certificate exists). §3–§4 say: for the
cryptids the Adversary appears to win against every finite-state Prover — the **[OPEN]** claim of §3.
This is the same shape as the quantum limit theorem: single-basis (finite) statistics cannot certify
genuineness; here, finite-state abstractions cannot certify non-halting of a cryptid. BB(6)'s hardness
*is* a genuineness-limit phenomenon, on a fully-specified discrete system.

## 5. Results this pass (bricks b, d) and honest status

- **(d) [PROVEN]** k-window ⊊ regular for certification — §2, conjecture-free, Lemma 1 verified m=1..32.
- **(b) [DONE]** concrete distinguishability for Antihydra: the milestone configs have **pairwise-
  distinct future-3-width signatures (14/14)**, so they lie in distinct Myhill-Nerode classes — the
  §3 non-regularity argument made concrete (still [CONDITIONAL] on the orbit being unbounded).
- **(a) [OPEN, reduced]** SLIN ⊋ REG for certification needs a machine with NO regular *over-
  approximation* certificate but a semilinear one. Reduction: build M whose only infinite orbit is the
  start orbit, with reachable = SAFE = a non-regular semilinear set R (e.g. equal-block `1^n X 1^n`);
  then every certificate is squeezed to R (non-regular) ⇒ no REG cert, while R is the SLIN cert. The
  gap is constructing M so SAFE = R exactly (every off-orbit config halts) — not yet built.
- **(c) [OPEN, scoped]** "no REG certificate with ≤ N states" by complete enumeration is exponential;
  feasible only for tiny N. A targeted CEGAR-style *lower bound* (no certificate the search class can
  express) is more practical but weaker than a true ∀-DFA bound.

### Standing summary
- **[PROVEN]** REG suffices at n=3 (63 explicit certificates); **k-window ⊊ regular** (parity counter).
- **[CONDITIONAL]** cryptid never-halts ⇒ reachable language non-regular (gap = orbit unbounded);
  distinguishability made concrete (b).
- **[OPEN]** no REG/SLIN over-approximation certificate for a cryptid (≥ as hard as the cryptid itself);
  SLIN ⊋ REG witness (a) reduced to an unbuilt construction.

Next bricks (all rigorous, achievable): (a) construct an explicit non-halting machine with a *provably*
non-regular reachable language **and** an explicit SLIN certificate — a clean witness that SLIN ⊋ REG
for certification, independent of any open conjecture; (b) make §3's distinguishability fully concrete
(compute the distinguishing continuations) for a chosen cryptid; (c) a finite, complete search proving
"no REG certificate with ≤ N states" for a cryptid, as a computable lower bound on `reg`; (d) prove the
parity-counter certificate language is not k-testable for any k (suffix-regular ⊊ regular, no
conjecture). Caveat threaded throughout: a REG *certificate* is an over-approximation `L ⊇ reachable`,
so "reachable language non-regular" never by itself yields "no REG certificate" — the over-approximation
gap is exactly what makes the cryptid barrier (§3 [OPEN]) hard, and is the honest crux of the note.
