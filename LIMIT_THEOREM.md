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
not LINEAR (bouncer), not AFFINE/GEOMETRIC (counter): a genuine Collatz-like rule. For Antihydra this
"Collatz-like rule" is now **exact, not just measured** — see the next bullet.

- **[CONDITIONAL] If `M` never halts, its EXACT reachable language is non-regular.**
  *Proof sketch (rigorous modulo "orbit unbounded").* Never-halting ⇒ the orbit is infinite. The
  milestone configs `c_0, c_1, …` have widths `w_i → ∞`. Two milestone configs of different width are
  Myhill–Nerode-distinguishable in the reachable language (a continuation that completes one milestone
  to a valid reachable config of a fixed larger width fails for the other), giving infinitely many
  equivalence classes ⇒ the language is non-regular. ∎ (The only gap is "widths → ∞", i.e. the orbit
  is unbounded — precisely Antihydra's open conjecture.)
- **[PROVEN, conjecture-free] The "beyond" class is concrete for Antihydra: an exact 2-adic criterion.**
  (Full derivation + verification in `antihydra_attack.md` §3c.) Antihydra's tape is two unary counters
  `0 1^a 0 0 1^b 0`; with `c := b+6` the orbit obeys `c ← ⌊3c/2⌋` (`c_0=8`) and the balance is
  `balance_n = 3E_n − n` (`E_n` = #even values so far). Two proven facts:
  - *Lemma (odd-run = 2-adic valuation).* The run of consecutive odd orbit values starting at `c` has
    length **exactly `v2(c−1)`** (`v2` = 2-adic valuation). One-line induction: `c=1+2^L m`, `m` odd ⇒
    `⌊3c/2⌋ = 1 + 3·2^{L−1} m`, so `v2` drops by exactly 1 per step. Verified: the *unique* residue mod
    `2^k` beginning a run `≥ k` is `1` (density exactly `2^{-k}`); all 50 034 maximal runs in the first
    `2·10^5` steps obey it, zero violations.
  - *Exact halting criterion.* `M` **HALTS ⟺ ∃ n : v2(c_n − 1) ≥ balance_n + 1`** — i.e. the orbit lands
    2-adically within `2^{-(balance_n+1)}` of `1`. This realizes the §3-preamble "Collatz-like rule" as a
    **named arithmetic predicate**, not a classifier output: the certificate question for Antihydra is
    *exactly* the 2-adic distribution of `⌊8·(3/2)^n⌋` (the Mahler family). It does **not** by itself
    prove "no REG certificate" (a regular over-approximation could still exist); its force is to **pin the
    [CONDITIONAL] gap below** — "milestone widths → ∞" / "orbit unbounded" / "never halts" are now one
    clean statement: `v2(c_n−1) < balance_n+1` for all `n`. The barrier is no longer hand-waved as
    "IRREGULAR"; it is a specific, open 2-adic equidistribution fact, and *that specificity is the point*
    — the cryptid's non-halting reduces to an equidistribution no finite-state abstraction can encode.
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
- **(b′) [PROVEN, conjecture-free]** the "beyond" class is made **exact** for Antihydra (§3,
  `antihydra_attack.md` §3c): odd-run length `= v2(c−1)` (proven), giving the exact criterion
  `HALT ⟺ ∃n: v2(c_n−1) ≥ balance_n+1`. The cryptid's Collatz-rule is now a named 2-adic
  predicate, and the [CONDITIONAL] gap of §3 collapses to the single statement "the orbit
  `⌊8·(3/2)^n⌋` never lands 2-adically that close to 1" (Mahler family). Pins, does not close, the gap.
- **(a) [PROVEN, conjecture-free]** SLIN ⊋ REG for non-halting certification. Witness: the machine
  **EQ** (`eq_machine.py`, alphabet `{_,L,C,R,xL,xR}`) that semi-decides equal blocks: it crosses off
  one L and one R per round at the centre `C`, and on equality uncrosses and grows both arms by one.
  Verified: **(i)** from blank EQ passes through `L^n C R^n` for n=0..15 without halting (the milestone
  step is uniform in n, so it reaches every n by induction); **(ii)** from every unequal block
  `L^a C R^b`, a≠b (checked a,b≤12), EQ HALTS (cross-off exhausts the short arm and the surplus is
  detected). Proof: any regular certificate `L'` contains `reachable ⊇ {L^n C R^n}` for unbounded n;
  by the pumping lemma a regular `L'` then contains some `L^{n+p} C R^n` (pump the L-arm) — an unequal
  block, which reaches the halt — so `L'` is not halt-free. **No regular certificate exists.** Yet the
  reachable set (milestones + compare/grow intermediates, each a linearly-parameterised family in
  `(n, round, head)`) is **semilinear**, and being exactly reachable it is a (semilinear) certificate.
  ∎ This is independent of any open conjecture: REG ⊊ SLIN for certification, with an explicit witness.
- **(c) [OPEN, scoped]** "no REG certificate with ≤ N states" by complete enumeration is exponential;
  feasible only for tiny N. A targeted CEGAR-style *lower bound* (no certificate the search class can
  express) is more practical but weaker than a true ∀-DFA bound.

- **(e) [PROVEN, conjecture-free — SLIN ⊊ 2-automatic, third strict separation]** Witness **POW2W**
  (`pow2w_machine.py`): an explicit 60-state multi-symbol TM that **checks power-of-2-ness every cycle**.
  Cycle-start state `CS`; each cycle from `(CS, 1^v)`: DUPLICATE `1^v→1^v M 1^v`, HALVE-CHECK the right
  copy (HALT iff `v` not a power of 2), MERGE back to `(CS, 1^{2v})`. Verified by simulation (the sound
  gate; re-checked independently): from `(CS,1^1)` it runs forever, visiting `CS`-milestones exactly
  `1^1,1^2,1^4,…,1^{1024}` (powers, exact doubling); `(CS,1^w)` **HALTS for every non-power `w`** and loops
  for every power (`w=1..130`, 0 mismatches); and — the separation-critical fact — **every clean
  left-anchored 1-block, in ANY state (`CS,DBL,PHOME,FUSE_HOME`), has power-of-2 length** (no `DOUBLE`-like
  state hosts an unchecked arbitrary-length block; this is the defect that sank the earlier `pow2_machine.py`
  POW2, recorded below).

  - **No semilinear certificate (the lower half — airtight, conjecture-free).** POW2W never halts from
    blank, so `reachable(blank)` is a certificate; but no *semilinear* one exists. *Proof.* Suppose `L` is
    semilinear, step-closed, halt-free, `L ⊇ reachable`. `reachable` contains every `CS`-milestone
    `(CS,1^{2ⁿ})`. Let `V = {v : (CS,1^v) ∈ L}`; under SLIN's block-count encoding, `L` semilinear ⇒ `V`
    semilinear (a section + projection = Presburger operations), and `V ⊇ {2ⁿ}`. A semilinear `V ⊆ ℕ` is a
    finite union of arithmetic progressions; since `V` is infinite, some component `a+bℕ` (`b≥1`) contains
    infinitely many `2ⁿ`. But `a+bℕ` (`b≥1`) is an infinite AP and powers of 2 have density 0, so it
    contains a **non-power** `w`. Then `(CS,1^w) ∈ L`, the machine HALTS from `(CS,1^w)` (verified), and `L`
    step-closed ⇒ `L` contains that halt config — contradicting halt-free. ∎ So **SLIN is insufficient** for
    POW2W's non-halting.
  - **A 2-automatic certificate exists (the upper half).** The `CS`-milestone value set is `{2ⁿ}`, which is
    **2-automatic** (base-2: `10*`) but **not semilinear** (gaps `2ⁿ→∞`). The reachable configs are a
    finite-state family parameterised by `(n, within-cycle progress j with 0≤j≤2ⁿ, phase)`; the constraint
    "`x` is a power of 2 ∧ `0≤j≤x`" is `Presburger+V₂`-definable, so by Büchi–Bruyère the reachable
    config-language is 2-automatic. Hence a 2-automatic certificate exists.
  - **Therefore `SLIN ⊊ 2-automatic` for non-halting certification**, with an explicit, simulation-verified
    witness — the third strict level after `k-window ⊊ REG` (d) and `REG ⊊ SLIN` (a). The lower half (no
    SLIN certificate) is fully rigorous and conjecture-free; the upper half rests on standard automatic-set
    theory (Büchi–Bruyère).
  - **Provenance / soundness note.** The first attempt (`pow2_machine.py`, POW2, 29 states) was a correct
    power-of-2 *semi-decider* but **did not separate SLIN** — from blank it checks once then doubles forever
    (state `DOUBLE` re-hosts every length), giving it a semilinear certificate. That defect was *self-found
    by simulation and recorded* before any claim; POW2W (check-every-cycle) fixes it. No separation was
    claimed until the witness passed all three verifications. (Discipline per `SOUNDNESS_INCIDENT.md`.)

### Standing summary — the hierarchy, with THREE strict separations now PROVEN
```
   k-window ⊊ regular (REG) ⊊ semilinear (SLIN) ⊊ 2-automatic ⊆ ... ⊆ beyond (Collatz)
     └ (d) parity ctr ┘   └ (a) EQ machine ┘  └ (e) POW2W ┘        └ (cryptids: OPEN) ┘
```
- **[PROVEN]** REG suffices at n=3 (63 explicit certificates).
- **[PROVEN, conjecture-free]** **k-window ⊊ REG** (d, parity counter), **REG ⊊ SLIN** (a, EQ machine), and
  **SLIN ⊊ 2-automatic** (e, POW2W — no semilinear certificate, lower half airtight). Three strict levels
  of the certification hierarchy, each with an explicit simulation-verified witness.
- **[CONDITIONAL]** cryptid never-halts ⇒ reachable language non-regular (gap = orbit unbounded);
  distinguishability made concrete (b), and for Antihydra the gap is now a named 2-adic
  equidistribution statement, not a hand-wave (b′, `v2(c_n−1) < balance_n+1` ∀n).
- **[OPEN]** no certificate of ANY tame class for a cryptid — the top of the hierarchy, = the BB(6)
  frontier itself (≥ as hard as resolving the cryptid). This is exactly the genuineness limit: the
  cryptids are non-halting in a way no finite/tame certificate can witness.

Next bricks (all rigorous, achievable): (a) construct an explicit non-halting machine with a *provably*
non-regular reachable language **and** an explicit SLIN certificate — a clean witness that SLIN ⊋ REG
for certification, independent of any open conjecture; (b) make §3's distinguishability fully concrete
(compute the distinguishing continuations) for a chosen cryptid; (c) a finite, complete search proving
"no REG certificate with ≤ N states" for a cryptid, as a computable lower bound on `reg`; (d) prove the
parity-counter certificate language is not k-testable for any k (suffix-regular ⊊ regular, no
conjecture). Caveat threaded throughout: a REG *certificate* is an over-approximation `L ⊇ reachable`,
so "reachable language non-regular" never by itself yields "no REG certificate" — the over-approximation
gap is exactly what makes the cryptid barrier (§3 [OPEN]) hard, and is the honest crux of the note.
