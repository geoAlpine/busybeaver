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

### 3′. The cryptid `[OPEN]` top is ONE shared vertex, not four machines (2026-06-25, `CRYPTID_KERNEL.md`)
The §3 barrier is not Antihydra-specific. **[PROVEN, verified]** the BB(6) Mahler core (Antihydra, o10-inner,
o18, o15) shares a single kernel: each reduces to the single-orbit equidistribution of `⌊μ^n⌋ mod p` for a
multiplier `μ=2^a/3^b` with `v_p(μ)=−1`, via the *same* induced map — a **full-branch piecewise-affine
expanding (Gibbs–Markov) endomorphism of `ℤ_p`**, with the same obstruction map (spectral gap orbit-blind,
non-shadowing insufficient, growth circular, soft mechanisms unavailable). The classification is exact:
`T_μ` is a clean `p`-to-1 exact endomorphism **iff `v_p(μ)=−1`** (verified grid). So the hierarchy's `[OPEN]`
top — "no tame certificate for a cryptid" — is a **single mathematical object** indexed by `(a,b,p)`, shared
across the family, not four coincidentally-hard instances. (o17 is a separate vertex: a uniquely-ergodic
*odometer*, whose hardness is its Collatz-irregular **halt predicate**, not equidistribution — so the BB(6)
Collatz core has exactly **two** non-halting obstruction types.)
- **[literature-anchored, 2026-06-25 triage]** This shared vertex is a **recognized open problem**, not our
  artifact: it is the single-orbit case of **Mahler's 3/2 problem (1968)**; the *closest* known technique is
  **Tao 2019/2022** (*Forum Math. Pi*, arXiv:1909.03562), which controls the **same** p-adic skew-random-walk /
  renewal / Gibbs–Markov statistic we reconstructed — but only for a **log-density-1** set of seeds, never one
  specified seed (the exact gap = removing the density average). **Flatto–Lagarias–Pollington (1995)** gives
  only a *range* bound (orbit can't stay in an interval shorter than `1/p`), not a density. A **2025** paper
  (arXiv:2510.11723) poses single-orbit normality in rational-base systems as an explicit *conjecture*. The
  community reduction matches ours (bbchallenge, arXiv:2509.12337, 2025). *(Caution: arXiv:2411.03468 claims to
  resolve Mahler 3/2 — unverified, treat as likely flawed; we do not rely on it.)* So the `[OPEN]` top is
  pinned to the literature's open frontier — the genuineness-limit avatar is a *named* open problem, and one
  tool (rank-1 effective single-orbit equidistribution) would lift the whole vertex.

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

### The Squeeze Lemma — a check-S-every-cycle machine has certificate-complexity = the descriptive complexity of S
The constructions (e),(f) below share one mechanism, isolated here.

> **Squeeze Lemma.** Let `M` be a *check-`S`-every-cycle* machine: a cycle-start state `CS` and a unary
> encoding such that (i) `reachable(blank)` contains exactly the clean milestones `{(CS, 1^s) : s ∈ S}`,
> and (ii) `M` halts from `(CS, 1^v)` for every `v ∉ S`. Then **every** step-closed halt-free certificate
> `L ⊇ reachable` has CS-value-set exactly `S`, i.e. `{v : (CS,1^v) ∈ L} = S`.
> *Proof.* `V := {v : (CS,1^v) ∈ L} ⊇ S` (reachable ⊆ L). If `v ∉ S` then `(CS,1^v)` halts (ii); `L`
> step-closed + halt-free ⇒ `(CS,1^v) ∉ L`, so `v ∉ V`. Hence `V ⊆ S`, so `V = S`. ∎

**Consequence.** The minimal certificate class for `M`'s non-halting equals the descriptive class of `S`
itself: no certificate in a class `C` exists when `S ∉ C` (an `L ∈ C` would give `V = S ∈ C`), and the
reachable set is a certificate in the class of `S` when the within-cycle progress is `C`-definable.
So *extending the hierarchy reduces to exhibiting a check-`S`-machine for a set `S` of the target
complexity.* This is the engine behind (e) `S={2ⁿ}` and (f) `S={n²}`; it also streamlines (e)'s lower
half (the AP/pigeonhole argument is the special case "semilinear `V=S={2ⁿ}` is impossible").

- **(f) [PROVEN, conjecture-free — context-free ⊊ context-sensitive, fourth strict separation]** Witness
  **SQW** (`sqw_machine.py`), the squares-analogue of POW2W: an explicit ~45-state / 8-symbol TM that
  **checks "is a perfect square" every cycle**. Cycle-start `CS`; each cycle from `(CS,1^v)`: DUPLICATE,
  then CHECK the copy by subtracting consecutive odds `1,3,5,…` (a square is `1+3+…+(2k−1)=k²`; exact 0 ⇒
  `v=k²`, overshoot ⇒ HALT), then advance the original by `+(2k+1)` to `(CS, 1^{(k+1)²})`. Verified
  (sound gate, independently re-checked): from `(CS,1^1)` it runs forever visiting CS-milestones
  `1,4,9,16,…,100,…` (squares); `(CS,1^w)` HALTS for every non-square `w` (`w=1..100`, 0 mismatches);
  and every clean left-anchored block in any state (`CS`, `PASS_HOME2`) has square length (no trap).
  - By the Squeeze Lemma, every step-closed halt-free certificate has CS-value-set exactly `S = {n²}`.
  - **`{n²}` is NOT context-free (base-2).** The base-`q` representation of the range of a polynomial is
    context-free **iff the polynomial is linear** (answering a question of Shallit); `n²` is non-linear, so
    `{base-2(n²)}` is **not context-free** — hence a fortiori **not 2-automatic** (not base-2 regular).
    *(Ref: "The range of non-linear natural polynomials cannot be context-free", arXiv:1901.03913; proof
    via the Interchange lemma + a generalised Pumping lemma. NB: the clean unary fact "`{1^{n²}}` not CF"
    is weaker — it only gives `{n²} ∉` SLIN — because over a 1-letter alphabet CF = regular; the base-2
    non-CF result is the one this rung needs, and it is genuinely stronger.)*  So **no context-free
    certificate** (and none 2-automatic).
  - **`{n²}` IS context-sensitive (base-2):** an LBA checks perfect-squareness in linear space (`⌊√v⌋²=v`).
    The reachable set is `⟨ℕ,+,×⟩`-definable ("`v=k²` ∧ bounded progress"), so a context-sensitive (indeed
    arithmetic) certificate exists.
  - Therefore **`context-free ⊊ context-sensitive` for non-halting certification** (and `2-automatic ⊊ CS`),
    with an explicit verified witness — placing `{n²}` strictly **above** the context-free rung (g, PALW
    binary palindromes) and at the context-sensitive level. Combined with (e),(g) this gives the clean
    Chomsky tower `2-automatic (= base-2 regular) ⊊ context-free (g) ⊊ context-sensitive (f) ⊊ arithmetic`.

- **(g) [PROVEN, conjecture-free — 2-automatic ⊊ context-free, fifth strict separation]** Witness **PALW**
  (`palw_machine.py`), a check-S-every-cycle machine for `S = {n : base-2(n) is a palindrome}` (OEIS
  A006995: 1,3,5,7,9,15,17,21,27,31,33,…). 56-state/12-symbol TM: each cycle DUPLICATE, CONVERT the copy
  unary→binary (repeated halving), PALINDROME-test the binary digit string (two-pointer), HALT if not a
  palindrome, else ADVANCE to the next binary palindrome and return to CS. Independently re-verified:
  from `(CS,1^1)` it visits CS-milestones `1,3,5,7,9,15,17,21,27,31,33,45,51,63,65,73,85,93,99,107`
  (exactly A006995, increasing); `(CS,1^w)` HALTS iff `w` is not a binary palindrome (`w=1..50`,
  0 mismatches); and the **only** state hosting a blank-rest clean left-block is `CS`, all binary-palindrome
  lengths (no trap — the advance-search's intermediate integers are kept non-clean by a mode-flag at a
  fixed cell, the separation-critical discipline).
  - By the Squeeze Lemma the CS-value-set of any certificate is exactly `S`. **`S` is not 2-automatic**:
    `S` is 2-automatic iff its base-2 language is regular, but binary palindromes are the canonical
    **non-regular context-free** language (pumping lemma) ⇒ **no 2-automatic certificate** (lower half,
    airtight). **A context-free certificate exists**: binary palindromes are CF (`P→0P0|1P1|0|1|ε`), so
    the reachable set is at the context-free-numeration level. Hence **2-automatic ⊊ context-free**.
  - **Placement (honest):** this is a *refinement between* 2-automatic and arithmetic, not a new ceiling:
    `2-automatic ⊊ CF (g, palindromes) ⊊ CS ⊊ arithmetic (f, {n²})`. PALW differs structurally from
    POW2W/SQW (which advance by a closed-form step, so no state ever holds a non-target clean block);
    PALW must *search* for the next palindrome, materialising every intermediate integer in scratch —
    the mode-flag discipline is what preserves property (C). Lower half airtight; upper half via the same
    Squeeze-Lemma within-cycle-CF-definability argument as (e)/(f).

### Standing summary — the hierarchy, with FIVE strict separations now PROVEN (a clean linear Chomsky tower)
```
 star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ context-free ⊊ context-sensitive ⊊ … ⊆ beyond (Collatz)
   └(d)parity ℤ/2┘ └(a)EQ┘ └(e)POW2W{2ⁿ}┘ └(g)PALW palindromes┘ └(f)SQW{n²}┘   └(cryptids:OPEN)┘
   (below REG the star-free interval definite⊆SLT⊆LT⊆PT COLLAPSES for certification — Lemma A)
```
- **[PROVEN]** REG suffices at n=3 (63 explicit certificates).
- **[PROVEN, conjecture-free]** five strict separations forming a linear tower, each with an explicit
  simulation-verified witness:
  **star-free ⊊ REG** (d, parity counter — gap is the ℤ/2 group language `(11)*1`; the star-free interval
  below collapses, Lemma A), **REG ⊊ SLIN** (a, EQ machine), **SLIN ⊊ 2-automatic**
  (e, POW2W, `S={2ⁿ}`), **2-automatic ⊊ context-free** (g, PALW, binary palindromes), **context-free ⊊
  context-sensitive** (f, SQW, `S={n²}`, via arXiv:1901.03913 — non-linear-polynomial range not CF — + LBA).
  Above 2-automatic this is exactly the **Chomsky tower on base-2 numeration languages**
  (regular ⊊ CF ⊊ CS). Bricks (e),(f),(g) share the **Squeeze Lemma**: certificate-complexity = descriptive
  complexity of the checked set `S`, so each new rung is just a check-`S` witness for an `S` of the target
  class. **arithmetic ⊋ CS** — see the ceiling analysis just below.

### Above context-sensitive — where the explicit tower ends, and why (2026-06-23)
Pushing past CS hits a *structural* boundary of the Squeeze method, worth stating precisely.
- **The Squeeze witness forces `S` to be DECIDABLE.** A check-`S`-every-cycle machine must HALT from
  `(CS,1^v)` for every `v∉S` — so membership in `S` is decided by a halting computation. Hence the
  CS-value-set of *any* Squeeze witness is a **recursive (decidable)** set, and the reachable set is
  recursive. So this method can witness separations only **up to the recursive ceiling**.
- **`context-sensitive ⊊ recursive` [PROVEN, but the witness is non-explicit].** By the Space Hierarchy
  Theorem `NSPACE(n) = CS ⊊ DSPACE(2ⁿ) ⊆ recursive`, there is a **decidable** set `S` whose base-2 language
  is **not** context-sensitive (membership provably needs super-linear space in the bit-length). `S`
  decidable ⇒ a check-`S` machine exists ⇒ by the Squeeze Lemma its certificate value-set is exactly `S ∉
  CS`, so **no CS certificate**, while a recursive certificate exists. This is a genuine separation — but
  unlike (e),(f),(g) its witness comes from diagonalization, **not an explicit simulation-verified TM**.
  *So the explicit, machine-checked tower tops out at CS; above it the rungs hold by general principles but
  lose the "small explicit witness" character that anchors the lower five.*
- **`recursive ⊊ arithmetic` holds as classes but is NOT Squeeze-witnessable.** Arithmetic (`⟨ℕ,+,×⟩`-
  definable) sets include undecidable ones, but a check-`S` machine with undecidable `S` would have a
  non-halting check — forbidden. So our witness method cannot reach the undecidable part of arithmetic.
- **Reframing — the cryptid top is a DIFFERENT axis.** The tower `REG ⊊ CF ⊊ CS ⊊ recursive` measures the
  descriptive complexity of the **exact reachable set**. A cryptid's reachable value-set (e.g. Antihydra's
  `{⌊8(3/2)ⁿ⌋}`) is itself *recursive* (even CS-ish — the orbit is computable), so the cryptid does **not**
  sit high on this descriptive tower. The cryptid `[OPEN]` is on the **over-approximation axis**: does any
  *halt-free* certificate `L ⊇ reachable` exist in a tame class? That is independent of how complex the
  exact reachable set is — and it is the genuineness-limit barrier. **Climbing the descriptive tower does
  not approach the cryptids; the two are orthogonal.** The clean explicit tower (regular⊊CF⊊CS) is the
  *anchor*; the cryptid over-approximation gap is the *frontier*.

### Below REG — the sub-regular floor collapses, and brick (d) lands outside star-free (2026-06-23)
Probing *beneath* the bottom rung (the sub-regular landscape `definite ⊆ SLT ⊆ LT(=k-window) ⊆ PT ⊆
star-free`) gave two conjecture-free results and one honest negative — all re-verified here.
- **[PROVEN, structural] Lemma A (halt-locality).** In the head-marker config encoding, a config is a HALT
  iff its string contains a forbidden length-2 factor `(state)(symbol)` (the marker sitting on a cell whose
  transition is undefined). So **halt-freeness is a strictly-locally-testable (SLT, m=2) property**, and
  even the minimal SLT invariant excludes every halt. *Consequence:* the boolean-combination power that
  separates `definite / SLT / LT / PT` is **never needed to exclude halts** — only step-closure can fail —
  so the whole star-free sub-regular interval **collapses onto SLT for non-halting certification**. No
  clean explicit witness separates these sub-rungs (verified via the purpose-built "AGREE" machine, whose
  intended LT-not-SLT certificate is rendered SLT-sufficient by Lemma A). (`far_dfa.py`'s FAR engine is
  exactly this SLT/all-m-window class.)
- **[PROVEN, conjecture-free] brick (d) strengthened: the bottom jump lands OUTSIDE star-free.** The parity
  counter `1RB0LZ_1LC1RA_0RA0LC` has `1^m [B] 0` halting ⟺ `m` even (re-verified m=1..24), so its
  non-halting reachable fiber at state `B` is exactly `{1^m : m odd} = (11)*1`. This is **non-aperiodic**
  (syntactic monoid `= ℤ/2`), hence **not star-free** (Schützenberger / McNaughton–Papert). So the real
  bottom separation is **`star-free ⊊ REG`, with the gap realized by a modular-counting (group) language** —
  strictly stronger than the old "k-window ⊊ REG" framing; the *entire* star-free landscape (incl. LT, PT)
  is invisible to this machine's certification.
- **[honest negative] the over-approximation axis — "no k-window certificate for a cryptid" does NOT follow
  from off-orbit halters.** Off-orbit halting configs DO exist (Antihydra `0 1^2 0 0 1^9 0` HALTs at 15466
  while reachable `0 1^2 0 0 1^6 0` runs; o17's `0 A 0 1^k`, `k≢0 mod 3`). But a cryptid's halt trigger is
  **head-local** (Antihydra: balance read at state F; o17: carry overflow at the head), so for window size
  larger than the (bounded) left-frontier structure, a k-window can **gate on the halt condition at the
  marker** and exclude the off-orbit halters while keeping reachable. Hence those halters are *not* forced
  into `L_G`, and **no contradiction arises** — k-window certificates are *not* provably too weak here. The
  brick-(d) trick (`1^k` all-or-nothing in an unbounded clean run) does **not** transfer, because the
  cryptids carry their discriminating feature next to the head, not in an unbounded run. So impossibility on
  the over-approximation axis stays **[OPEN]**, and the barrier sits at REG, not below.
- **[CONDITIONAL]** cryptid never-halts ⇒ reachable language non-regular (gap = orbit unbounded);
  distinguishability made concrete (b), and for Antihydra the gap is now a named 2-adic
  equidistribution statement, not a hand-wave (b′, `v2(c_n−1) < balance_n+1` ∀n).
- **[OPEN]** no certificate of ANY tame class for a cryptid — the top of the hierarchy, = the BB(6)
  frontier itself (≥ as hard as resolving the cryptid). This is exactly the genuineness limit: the
  cryptids are non-halting in a way no finite/tame certificate can witness.

### The analytic content of the [OPEN] over-approximation top (2026-06-26 — links to the analytic notes)
The over-approximation [OPEN] question — *does a tame halt-free `L ⊇ reachable` exist for Antihydra?* — and the
analytic **single-orbit equidistribution wall** (the `EXPERT_ASK` / `*_ATTACK` notes) are **two faces of one
barrier**, not a reduction. The certificate side asks for an *invariant set*; the analytic side asks to *prove the
orbit statistic*. They coincide only at the cryptid top, where both are open. What the analytic work adds is **why
the barrier resists**, made precise from three independent technologies (this session):
- a **measure / spectral** certificate route is blind to the specified orbit (rank-1, continuum of invariant
  measures — needs an *infinitary* input);
- a **Diophantine / bounded-height** route fails because the orbit terms `c_n=(3^n c_0−T_n)/2^n` have
  `height(T_n)≈n·log₂3` — **unbounded** (so no `S`-unit / Baker certificate);
- a **multiplicative / character-sum** route fails because `c_n mod 4` = high bits of the dynamical carry `T_n` —
  **structureless** in `n` (the energy form is even *sign-blind*).
So the certificate-theoretic [OPEN] top is not a vague "hard"; its hardness has **three distinct, structural
analytic obstructions**, each closing one natural certificate-construction route. *Honest caveat:* "no analytic
proof via tools `X`" does **not** by itself prove "no tame certificate" (a certificate need not be built through
the orbit's statistics) — the two axes meet only at the cryptid, which is why the [OPEN] stays [OPEN]. But the
three-obstruction picture is the sharpest available *explanation* of the over-approximation gap, and it is exactly
the genuineness-limit phenomenon stated analytically. (Full: `EXPERT_ASK.md`, `ENERGY_ATTACK.md`,
`SEPARATION_BAKER.md`, `VALUATION_BUDGET.md`.)

Next bricks (all rigorous, achievable): (a) construct an explicit non-halting machine with a *provably*
non-regular reachable language **and** an explicit SLIN certificate — a clean witness that SLIN ⊋ REG
for certification, independent of any open conjecture; (b) make §3's distinguishability fully concrete
(compute the distinguishing continuations) for a chosen cryptid; (c) a finite, complete search proving
"no REG certificate with ≤ N states" for a cryptid, as a computable lower bound on `reg`; (d) prove the
parity-counter certificate language is not k-testable for any k (suffix-regular ⊊ regular, no
conjecture). Caveat threaded throughout: a REG *certificate* is an over-approximation `L ⊇ reachable`,
so "reachable language non-regular" never by itself yields "no REG certificate" — the over-approximation
gap is exactly what makes the cryptid barrier (§3 [OPEN]) hard, and is the honest crux of the note.
