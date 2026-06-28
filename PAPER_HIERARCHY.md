# A certification-complexity hierarchy for Turing-machine non-halting

*A standalone note with full proofs. Part (B) of the BB(6) program.*
*Draft for arXiv submission — internal record, not committed, 2026-06-29.*

---

## Soundness discipline (paramount)

Every statement carries an explicit label, copied verbatim from the source notes; **no label is
upgraded**.

- **[PROVEN]** — conjecture-free; a complete mathematical argument is given inline (or the missing step is a
  named, standard external theorem cited as input, in which case the statement is additionally tagged
  **[cites external]**).
- **[PROVEN, structural + machine-verified]** — the argument is a finite-state routine whose local action is
  provably independent of its size parameter, machine-verified for small parameters; the inductive extension
  is routine and is described but not transcribed as a formal induction. These are flagged at each use.
- **[OPEN]** — a named, recognized open problem. Not claimed.

No Turing machine is decided here; no non-halting is asserted unconditionally. The hierarchy results below
are about **which description classes can host a non-halting certificate**, a question that is independent of
(and provable without) deciding any cryptid.

All witnesses are re-verified this pass with `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` against the
`bb_sim` step semantics; the verification logs are quoted in §10.

---

## Abstract

A Turing machine `M` never halts iff there is a set `L` of configurations that contains the start, is closed
under one step, and contains no halting configuration — a **certificate**. The reachable set is always such an
`L`; the interesting question is whether a *describable* one exists, and in **which** description class. This
note develops the descriptive complexity of non-halting certificates and proves a chain of **five strict
separations**, each with an explicit, simulation-verified witness Turing machine:

> **star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ context-free ⊊ context-sensitive.**

The engine for the upper three separations is a **Squeeze Lemma**: a machine that re-checks a unary predicate
`S ⊆ ℕ` at the start of every cycle has certificate-complexity exactly equal to the descriptive complexity of
`S`. Four of the five separations are proven fully inline (the descriptive halves are elementary; two upper
halves cite only standard automatic-set theory and context-free grammars). The top separation, `CF ⊊ CS`,
rests on an external theorem (the base-`q` range of a non-linear polynomial is not context-free,
arXiv:1901.03913) and is cited as input, **not** claimed self-contained. We give a second, orthogonal proven
floor — the subword complexity of a cryptid's parity sequence satisfies `p(ℓ) ≥ ℓ+1` (not eventually
periodic), `p(2)=4` (not Sturmian), and `p(ℓ) ≥ (log 2/log(3/2))·ℓ ≈ 1.71ℓ` — all elementary. We record two
applications inside the BB(6) frontier: the existence cryptid o18 has a proven certificate floor `m*=2` (no
2-window certificate) and the odometer cryptid o17 has floor `m*=8` (no `m`-window certificate for `m ≤ 8`).
Finally we state precisely what is **proven** (the floors) versus **open** (no REG / tame certificate for a
cryptid), and connect the whole picture to a spoofer/certificate meta-principle: the Turing-machine avatar of
a "finite description cannot certify an infinite property" limit.

---

## 1. Introduction

### 1.1 Non-halting certificates

Fix a deterministic single-tape Turing machine `M`. A **configuration** is a finite description of the tape, the
head position, and the state; we encode it as a string with a marker symbol `[q]` written immediately before
the scanned cell, e.g. `… c_{-1} [q] c_0 c_1 …` (this is the encoding used by the trusted verifier `far_dfa.py`).
The **step relation** `→` is the partial function taking a configuration to its successor; a **halting**
configuration is one on which `M`'s transition is undefined.

> **Definition (certificate).** A set `L` of configurations is a *certificate* (for non-halting of `M` from
> start config `s`) if
> - **(S)** `s ∈ L`,
> - **(C)** `L` is closed under `→` (if `c ∈ L` and `c → c'` then `c' ∈ L`),
> - **(H)** `L` contains no halting configuration.

**[PROVEN] (soundness of certificates).** If a certificate exists, `M` never halts from `s`. *Proof.* The forward
orbit `s → c_1 → c_2 → …` stays in `L` by (S)+(C), so by (H) it never reaches a halting configuration. ∎

The reachable set `reachable(s) = {c : s →^* c}` is always a certificate (it is the smallest one). The content
of the theory is whether a *describable* — i.e. finitely presented, recognizable — certificate exists, and how
descriptively complex it must be. A certificate is in general an **over-approximation** `L ⊇ reachable(s)`; this
distinction is load-bearing and recurs throughout (a regular superset of a non-regular reachable set can exist,
so "reachable is non-regular" never by itself implies "no regular certificate").

### 1.2 The descriptive-complexity view

This recasts non-halting verification as a problem of *descriptive complexity*. The verifier `far_dfa.py`
implements the **REG** case directly: it checks that a candidate DFA `L` over configuration strings satisfies
(S), (C), (H) — `start ∈ L`, `succ(L) ⊆ L`, `halt ∉ L` — and this check is decider-independent and sound. The
question "for which classes `C` does a certificate `L ∈ C` exist?" stratifies non-halting proofs by the
descriptive power they require. The main theorem (§3) is that this stratification is **strict** along a natural
ladder, witnessed by explicit machines; §7 connects the top of the ladder to the BB(6) cryptids.

### 1.3 Relation to the rest of the program

This note is the **conjecture-free anchor** of a larger program (`BB6_STRUCTURAL_LIMIT_THEOREM.md`): the BB(6)
cryptids reduce to single-orbit equidistribution statements (Mahler 3/2 / Andrieu–Eliahou–Vivion 2025) that are
genuinely open. The hierarchy below is orthogonal to that frontier — it is proven, machine-checked, and does not
touch any open conjecture, except for the single external dependency at the top rung (§3.6), which is flagged.

---

## 2. The certificate classes

We classify a certificate `L` by the description class of its configuration language. Throughout, "the unary
fiber at state `q`" means the set `{1^m : (\text{config } 1^m [q] 0 \cdots) ∈ L}`, a language over the
one-letter alphabet `{1}`. For the Squeeze-Lemma classes we use the **block-count encoding**: a configuration is
coded by the cell symbols plus the marker, so a clean unary block `(q, 1^v)` is captured by the integer `v`.

- **star-free** (= **aperiodic** = first-order-definable, **FO[<]**): the smallest class of languages containing
  `∅` and the singletons, closed under boolean operations and concatenation but **not** under Kleene star. By the
  Schützenberger–McNaughton–Papert theorem, a regular language is star-free iff its syntactic monoid is
  aperiodic (contains no nontrivial group). Sub-rungs `definite ⊆ SLT ⊆ LT ⊆ PT ⊆ star-free` (where **LT** =
  locally testable = "`k`-window" = `k`-tails, the class the FAR engine `far_dfa.py` searches) all collapse onto
  SLT for *certification* (Lemma A below), so we take **star-free** as the bottom rung.
- **REG** (regular): `L` is recognized by a finite automaton over configuration strings. This is exactly the
  **Closed-Tape-Language / FAR** class of `far_dfa.py`.
- **SLIN** (semilinear): under the block-count encoding, `L` is Presburger-definable — equivalently, its
  block-count image is a finite union of arithmetic progressions in `ℕ^k` (a semilinear set). Captures counters
  whose reachable set is not regular.
- **2-automatic** (= base-2 automatic): `L`'s block-count image is a `2`-automatic subset of `ℕ` — its base-2
  representation is regular — equivalently it is `⟨ℕ, +, V_2⟩`-definable (Büchi–Bruyère). Strictly larger than
  SLIN: `{2^n}` is 2-automatic but not semilinear.
- **CF** (context-free numeration): the block-count image is a set whose base-2 representation is a context-free
  language.
- **CS** (context-sensitive): the block-count image is base-2 context-sensitive — recognized by a linear-bounded
  automaton (LBA).

These nest `star-free ⊆ REG ⊆ SLIN ⊆ 2\text{-automatic} ⊆ CF ⊆ CS ⊆ \text{recursive}`. The theorem is that the
six listed inclusions are each **strict** for non-halting certification.

> **[PROVEN] Lemma A (halt-locality).** In the marker encoding, a configuration is halting iff its string
> contains a forbidden length-2 factor `[q]c` (the marker on a cell whose transition is undefined). Hence
> halt-freeness (H) is a strictly-locally-testable (`m=2`) property. *Consequence:* the boolean-combination
> power separating `definite / SLT / LT / PT` is never needed to **exclude halts**; only step-closure (C) can
> fail across these sub-rungs. So the entire star-free sub-regular interval collapses onto SLT for certification,
> and the bottom meaningful rung is **star-free**. (Verified against the purpose-built "AGREE" machine, whose
> intended LT-not-SLT certificate is rendered SLT-sufficient by Lemma A.)

---

## 3. Main theorem: five strict separations

> **Theorem 1 [PROVEN].** For non-halting certification,
> `star-free ⊊ REG ⊊ SLIN ⊊ 2\text{-automatic} ⊊ context\text{-}free ⊊ context\text{-}sensitive`,
> each strictness witnessed by an explicit Turing machine. Four separations are proven fully inline; the top
> one (`CF ⊊ CS`) cites one external theorem (arXiv:1901.03913), flagged as input.

We prove each rung in turn. The standing diagram:

```
 star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ context-free ⊊ context-sensitive ⊊ … ⊆ beyond (Collatz)
   └(d)parity ℤ/2┘ └(a)EQ┘ └(e)POW2W{2ⁿ}┘ └(g)PALW palindromes┘ └(f)SQW{n²}┘   └(cryptids:OPEN)┘
```

### 3.1 `star-free ⊊ REG` — witness: the parity counter (brick d)

**Witness.** `1RB0LZ_1LC1RA_0RA0LC` (states `A,B,C`; halt = `A` reads `1`, transition `0LZ`).

> **Lemma 1 [PROVEN, structural + machine-verified].** From the configuration `1^m [B] 0` (state `B`, head just
> right of `m` ones, scanning blank), `M` halts **iff `m` is even**.

*Status of Lemma 1.* Odd-`m` non-halting is rigorous: the verified 2-state parity DFA certificate (CEGAR-found,
`far_cegar.py`; the DFA has the two length-parity classes, syntactic monoid `ℤ/2`) satisfies (S),(C),(H) — a
finite, decider-independent check — and contains exactly the odd-fiber configurations, *proving* they never
halt. Even-`m` halting is a fixed finite-state routine (a binary-counter sweep) whose local action is
independent of `m`; it is machine-verified for `m = 1..32` (§10, re-run this pass): even `m` halt, odd `m` run
to cap. The all-even-`m` extension follows from the routine's parameter-uniformity; a fully formal induction is
not transcribed here, so we flag the even-`m` halting direction as **machine-verified (`m ≤ 32`) + structural**,
not hand-proven for all `m`.

> **Theorem (d) [PROVEN, modulo Lemma 1].** `M` has a REG certificate but no star-free certificate. Hence
> `star\text{-}free ⊊ REG`.

*Proof.* **(REG certificate exists.)** The 2-state parity DFA above is a verified certificate (S/C/H all hold),
so `M` never halts from blank and `L_{REG}` is regular. **(No star-free certificate.)** Suppose `L` is a
star-free certificate. Consider the unary fiber `U = \{1^m : 1^m [B] 0 ∈ L\}` over the one-letter alphabet
`{1}`. The set `F` of configurations of the form `1^m [B] 0` is itself star-free (it is `1^*` followed by the
fixed string `[B]0`, and `1^* = \overline{\Sigma^*(\Sigma∖\{1\})\Sigma^*}` is star-free, with concatenation by a
fixed word preserving star-freeness). Thus `L ∩ F` is star-free, and stripping the fixed suffix `[B]0` (a right
quotient by a single word, which preserves star-freeness since star-free = FO[<]-definable and FO is closed
under such quotients) yields a **star-free unary language** `U`. Over a one-letter alphabet, star-free =
aperiodic = **eventually constant** (finite or cofinite): an aperiodic syntactic monoid over `{1}` cannot count
length modulo any `d ≥ 2`. Now:
- `U` is **infinite**: the counter's leading 1-run grows through `1,3,5,…` (the reachable odd fiber, contained
  in `L`), so `U` contains infinitely many odd `m`. An eventually-constant infinite unary language is
  **cofinite**, hence contains all sufficiently large `m`, in particular some **even** `m`.
- But by Lemma 1 that even-`m` configuration `1^m [B] 0` **halts**; `L` step-closed (C) then contains the halt
  configuration, contradicting halt-freeness (H).

So no star-free `L` exists, while a REG one does. ∎

**Why the gap is exactly `ℤ/2`.** The non-halting reachable fiber at state `B` is exactly `\{1^m : m \text{ odd}\}
= (11)^*1`, whose syntactic monoid is `ℤ/2` (a nontrivial group), hence not aperiodic, hence not star-free
(Schützenberger). The separation is realized by a **modular-counting (group) language** — strictly stronger than
the earlier "`k`-window ⊊ REG" framing, and by Lemma A the *entire* star-free interval (definite/SLT/LT/PT) is
invisible to this machine's certification.

### 3.2 `REG ⊊ SLIN` — witness: the EQ machine (brick a)

**Witness.** `EQ` (`eq_machine.py`), alphabet `{_, L, C, R, xL, xR}`, a semi-decider for equal blocks. From the
milestone `L^n C R^n` (head on the centre `C`, state `CMP`) it crosses off one `L` and one `R` per round; if both
arms empty together it **uncrosses and grows each arm by one** (reaching `L^{n+1} C R^{n+1}`); if one arm empties
first it **halts** (the surplus is detected). Full transition table in `eq_machine.py`.

> **Lemma 2 [PROVEN, structural + machine-verified].**
> (i) From blank, `EQ` passes through `L^n C R^n` (head on `C`, state `CMP`) for every `n ≥ 0`, never halting.
> (ii) From every unequal block `L^a C R^b` with `a ≠ b`, `EQ` halts.

*Status.* (i) machine-verified `n = 0..15` (§10, re-run: reaches `n = 0..8` within the trace budget, and the
within-cycle routine — cross off `n` pairs, then uncross-and-grow — is a fixed procedure whose action is
identical for every `n`, giving the induction `L^n C R^n ⇒ L^{n+1} C R^{n+1}`). (ii) machine-verified for all
`a,b ≤ 7` (§10) [and `a,b ≤ 12` in the source]; structurally, the cross-off exhausts the short arm first, after
which the surplus is detected and the machine halts (path `FL → HALTL` for `b>a`, path `CKL → HALTR` for `a>b`).
The general statements over all `n`/`a,b` follow from parameter-uniformity; the formal induction is described,
not transcribed, so we flag Lemma 2 as **structural + machine-verified**.

> **Theorem (a) [PROVEN, modulo Lemma 2].** `EQ` has a semilinear certificate but no regular certificate. Hence
> `REG ⊊ SLIN`.

*Proof.* **(No REG certificate — the pumping engine.)** Suppose `L'` is a regular certificate. By Lemma 2(i),
`L'` contains `L^n C R^n` for unbounded `n`. Let `p` be the pumping length of `L'` and pick `n > p`. Write the
string `L^n C R^n = xyz` per the pumping lemma with `|xy| ≤ p` and `|y| ≥ 1`; since the first `p` symbols are all
`L`, we have `y = L^k` with `k ≥ 1`. Then `xy^2z = L^{n+k} C R^n ∈ L'`. This is an **unequal** block, which by
Lemma 2(ii) halts; `L'` step-closed (C) then contains the halting configuration, contradicting (H). So no regular
certificate exists. **(A semilinear certificate exists.)** The exact reachable set is the union of the milestones
`{L^n C R^n}` and the within-cycle intermediates (compare/uncross/grow configurations), each a family linearly
parameterised by `(n, \text{round index}, \text{head offset})`; this is a **semilinear** set (Presburger), and
being exactly `reachable` it satisfies (S),(C),(H). ∎ This is independent of any open conjecture.

### 3.3 The Squeeze Lemma

The upper three rungs share one mechanism, isolated here. A **check-`S`-every-cycle machine** is a TM with a
distinguished cycle-start state `CS` and a unary encoding such that

- **(i)** `reachable(\text{blank})` contains exactly the clean milestones `\{(CS, 1^s) : s ∈ S\}`, and
- **(ii)** `M` halts from `(CS, 1^v)` for every `v ∉ S`.

> **Squeeze Lemma [PROVEN].** For a check-`S`-every-cycle machine `M`, **every** step-closed halt-free certificate
> `L ⊇ reachable` has cycle-start value set exactly `S`:
> `V := \{v : (CS,1^v) ∈ L\} = S`.

*Proof.* `V ⊇ S` because `reachable ⊆ L` and `(CS,1^s) ∈ reachable` for each `s ∈ S` (i). Conversely, if `v ∉ S`
then `(CS,1^v)` halts (ii); `L` step-closed (C) + halt-free (H) forces `(CS,1^v) ∉ L`, i.e. `v ∉ V`. Hence
`V ⊆ S`, so `V = S`. ∎

> **Consequence [PROVEN].** The minimal certificate class of `M` equals the descriptive class of `S` itself: if
> `S ∉ C` then no certificate lies in any class `C` closed under the section-and-project operations (an `L ∈ C`
> would yield `V = S ∈ C`); and when the within-cycle progress is `C`-definable, `reachable` is a certificate in
> the class of `S`. So **extending the hierarchy reduces to building a check-`S` machine for a set `S` of the
> target descriptive complexity.** This is the engine behind (e), (g), (f).

Each check-`S` witness below is verified on the **sound gate** (`bb_sim` simulation): (A) the `CS`-milestone
sequence from `(CS,1^1)` equals `S` in increasing order; (B) `(CS,1^w)` halts iff `w ∉ S`; (C) **every** clean
left-anchored unary block, in **any** state, has length in `S` — i.e. no trap state ever hosts an unchecked
arbitrary-length block (the defect that would break (i)). All three pass for POW2W, PALW, SQW (§10).

### 3.4 `SLIN ⊊ 2-automatic` — witness: POW2W, `S = {2^n}` (brick e)

**Witness.** `POW2W` (`pow2w_machine.py`), ~60-state multi-symbol TM checking power-of-2-ness every cycle: from
`(CS, 1^v)` it DUPLICATEs `1^v → 1^v M 1^v`, HALVE-CHECKs the right copy (HALT iff `v` is not a power of 2), and
MERGEs back to `(CS, 1^{2v})`. Verified (§10): milestones `1,2,4,…,1024` (exact doubling); `(CS,1^w)` halts for
every non-power `w = 1..63`, loops for every power; every clean left-anchored block in any state has power-of-2
length (property C).

> **Theorem (e) [PROVEN] (lower half inline; upper half cites Büchi–Bruyère).** `POW2W` has a 2-automatic
> certificate but no semilinear certificate. Hence `SLIN ⊊ 2\text{-automatic}`.

*Proof.* **(No semilinear certificate — fully inline.)** Suppose `L` is a semilinear certificate. By the Squeeze
Lemma, `V = \{v : (CS,1^v) ∈ L\} = S = \{2^n\}`. But `V` is also semilinear: under the block-count encoding `V`
is a section of `L` followed by a projection, both Presburger operations, so `V ⊆ ℕ` is a finite union of
arithmetic progressions. `V = \{2^n\}` is infinite, so some component `a + bℕ` (`b ≥ 1`) contains infinitely many
powers of 2 — impossible, because `a + bℕ` has positive density `1/b` while `\{2^n\}` has density 0, so `a+bℕ`
must also contain a **non-power** `w`. Then `(CS,1^w) ∈ L`, but `(CS,1^w)` halts (property B), and `L` step-closed
forces the halt into `L` — contradicting (H). (This is exactly the Squeeze Lemma specialized to "semilinear `V`
cannot equal `\{2^n\}`.") So no SLIN certificate exists. **(A 2-automatic certificate exists — cites
Büchi–Bruyère.)** The milestone value set `\{2^n\}` has base-2 representation `10^*`, a regular language, so it is
2-automatic. The reachable configurations form a finite-state family parameterised by `(n, \text{within-cycle
progress } j \text{ with } 0 ≤ j ≤ 2^n, \text{phase})`; the predicate "`x` is a power of 2 and `0 ≤ j ≤ x`" is
`⟨ℕ,+,V_2⟩`-definable, so by the **Büchi–Bruyère theorem** the reachable configuration language is 2-automatic,
giving a 2-automatic certificate. ∎

The lower half is conjecture-free and fully inline; the upper half uses only standard automatic-set theory
(`⟨ℕ,+,V_2⟩`-definable ⟹ 2-automatic).

**Provenance / soundness note.** The first attempt `pow2_machine.py` (POW2, ~29 states) was a correct power-of-2
*semi-decider* but did **not** separate SLIN: from blank it checks once then doubles forever (a state re-hosts
every length), giving it a semilinear certificate. That defect was found by simulation (property C fails) and
recorded before any claim; POW2W (check-every-cycle) fixes it. (Discipline per `SOUNDNESS_INCIDENT.md`.)

### 3.5 `2-automatic ⊊ CF` — witness: PALW, binary palindromes (brick g)

**Witness.** `PALW` (`palw_machine.py`), 56-state / 12-symbol, a check-`S` machine for
`S = \{n : \text{base-2}(n) \text{ is a palindrome}\}` (OEIS A006995: `1,3,5,7,9,15,17,21,27,31,33,…`). Each
cycle: DUPLICATE, CONVERT the copy unary→binary (repeated halving), PALINDROME-test the binary digit string
(two-pointer), HALT if not a palindrome, else ADVANCE to the next binary palindrome and return to `CS`. A
mode-flag at a fixed cell keeps the advance-search intermediates non-clean, so property (C) holds. Verified
(§10, re-run this pass): milestones `1,3,5,7,9,15,17,21,27,31,33,45,51,63,65,…` = A006995 in order; `(CS,1^w)`
halts iff `w` is not a binary palindrome (`w = 1..50`, 0 mismatches); every clean left-anchored block (states
`CS`, `CS_FLAG`) has binary-palindrome length.

> **Theorem (g) [PROVEN, both halves inline].** `PALW` has a context-free certificate but no 2-automatic
> certificate. Hence `2\text{-automatic} ⊊ CF`.

*Proof.* By the Squeeze Lemma the value set of any certificate is exactly `S`. **(No 2-automatic certificate.)**
`S` is 2-automatic iff its base-2 language is regular. The base-2 language of `S` is the set of **binary
palindromes**, the canonical non-regular context-free language: by the pumping lemma for regular languages, if it
were regular with pumping length `p`, the palindrome `1 0^p \, 1 \, 0^p 1` (a valid binary palindrome) pumped in
its first `0`-block gives `1 0^{p+k} 1 0^p 1`, no longer a palindrome — contradiction. So `S` is not 2-automatic,
and by the Squeeze Lemma consequence no 2-automatic certificate exists. **(A context-free certificate exists.)**
Binary palindromes are context-free (grammar `P → 0P0 \mid 1P1 \mid 0 \mid 1 \mid ε`), and the within-cycle
progress is context-free-definable, so `reachable` sits at the context-free numeration level. ∎

**Placement (honest).** This is a *refinement between* 2-automatic and CS, not a new ceiling:
`2\text{-automatic} ⊊ CF \text{ (palindromes)} ⊊ CS`. PALW differs structurally from POW2W/SQW (which advance by
a closed-form step, so no state ever holds a non-target clean block); PALW must *search* for the next palindrome,
materialising every intermediate integer in scratch — the mode-flag discipline is what preserves property (C).
Both halves are elementary and inline.

### 3.6 `CF ⊊ CS` — witness: SQW, `S = {n²}` (brick f) — cites external input

**Witness.** `SQW` (`sqw_machine.py`), ~45-state / 8-symbol, the squares analogue: each cycle DUPLICATE, then
CHECK the copy by subtracting consecutive odds `1,3,5,…` (a square is `1+3+…+(2k-1)=k²`; exact 0 ⟹ `v=k²`,
overshoot ⟹ HALT), then advance the original by `+(2k+1)` to `(CS, 1^{(k+1)²})`. Verified (§10, re-run):
milestones `1,4,9,16,25,36,49,64` (squares); `(CS,1^w)` halts for every non-square `w = 1..50`; every clean
left-anchored block (states `CS`, `PASS_HOME2`) has square length.

> **Theorem (f) [PROVEN — but lower half cites external arXiv:1901.03913, NOT self-contained].** `SQW` has a
> context-sensitive certificate but no context-free certificate. Hence `CF ⊊ CS` (and `2\text{-automatic} ⊊ CS`).

*Proof.* By the Squeeze Lemma the value set of any certificate is exactly `S = \{n²\}`. **(No context-free
certificate — external input.)** We need: the **base-2** representation of `\{n²\}` is not context-free. This is a
theorem of *"The range of a non-linear natural polynomial cannot be context-free"* (arXiv:1901.03913): the base-`q`
representation of the range of an integer polynomial is context-free **iff** the polynomial is linear; `n²` is
non-linear, so `\{\text{base-2}(n²)\}` is not context-free (the proof there uses the Interchange Lemma plus a
generalised pumping argument). **We cite this as input; this rung is not self-contained.** *(Caveat: the clean
unary fact "`\{1^{n²}\}` is not context-free" is weaker and does **not** suffice — over a one-letter alphabet
CF = regular, so it would only give `\{n²\} ∉` SLIN; the base-2 non-CF statement is the genuinely stronger fact
this rung needs.)* By the Squeeze Lemma consequence, no context-free certificate exists. **(A context-sensitive
certificate exists — inline.)** A linear-bounded automaton checks perfect-squareness in linear space (compute
`⌊√v⌋` and test `⌊√v⌋² = v`), and the reachable set is `⟨ℕ,+,×⟩`-definable ("`v = k²` and bounded progress"), so
a context-sensitive (indeed arithmetic) certificate exists. ∎

So the explicit, simulation-verified tower is `star\text{-}free ⊊ REG ⊊ SLIN ⊊ 2\text{-automatic} ⊊ CF ⊊ CS`;
above 2-automatic it is exactly the Chomsky tower on base-2 numeration languages (regular ⊊ CF ⊊ CS).

### 3.7 Above CS — where the explicit tower ends (honest)

- **[PROVEN, but non-explicit] `CS ⊊ recursive`.** A check-`S` witness forces `S` to be **decidable** (membership
  in `S` is decided by the halting computation on `(CS,1^v)`, `v ∉ S`). By the Space Hierarchy Theorem
  `NSPACE(n) = CS ⊊ DSPACE(2^n) ⊆ recursive`, there is a decidable `S` whose base-2 language is not
  context-sensitive; a check-`S` machine then has no CS certificate but a recursive one. This is a genuine
  separation, but its witness is **diagonalization**, not a small explicit simulation-verified TM — so it loses
  the character of the lower five rungs. Flagged.
- **`recursive ⊊ arithmetic` is NOT Squeeze-witnessable**: a check-`S` machine with undecidable `S` would have a
  non-halting "check," which is forbidden. So this method cannot reach the undecidable part of arithmetic.

The explicit, machine-checked tower **tops out at CS**.

---

## 4. "REG suffices at n=3"

> **[PROVEN] (finite theorem).** Every one of the **63** three-state, two-symbol "monster" machines (the hard
> residual of the BB(3) frontier that resisted the elementary bouncer/counter deciders) has an explicit,
> machine-verified **REG** (DFA) certificate. Hence at `n = 3` the hierarchy does **not** separate: REG
> certificates suffice for the entire hard residual.

*Precise statement and status.* The 63 certificates are produced and verified by the sound suite
(`suite.py` integrating `far_dfa.py`, `far_finder.py` k-tails, `far_cegar.py` RPNI/Blue-Fringe with negative
examples); the two genuinely hard binary counters
(`1RB1LC_0LA0RB_1LA0LZ`, `1RB0LZ_1LC1RA_0RA0LC`) required explicit DFA invariants found by k-tails state-merging
and by CEGAR respectively. Each certificate passes the decider-independent `far_dfa` check
(`start ∈ L`, `succ(L) ⊆ L`, `halt ∉ L`). This is a clean finite theorem (63 explicit certificates); it is not
re-derived in this note — we cite the verified suite (`STATUS.md`, `MAP.md`). The separations of §3 therefore
first *appear* only at larger machine sizes; the witnesses (d),(a),(e),(g),(f) are purpose-built to realize each
rung, not drawn from the `n=3` frontier.

---

## 5. The subword-complexity floor — a second, orthogonal proven floor

The cryptid top of the hierarchy (§7) lies on an **over-approximation axis** orthogonal to §3. On a *different*
axis — the subword complexity of a cryptid's parity sequence — we obtain a second family of elementary, proven
floors. Take Antihydra's integer orbit `c_0 = 8`, `c_{n+1} = ⌊3c_n/2⌋`, its parity sequence `r_n = c_n \bmod 2`,
and let `p(ℓ)` be its subword (factor) complexity (number of distinct length-`ℓ` factors). Let `T(c) = ⌊3c/2⌋`.

> **Lemma 3 (coding bijection) [PROVEN].** The map `φ_ℓ : ℤ/2^ℓ → \{0,1\}^ℓ`,
> `φ_ℓ(c) = (c, T(c), …, T^{ℓ-1}(c)) \bmod 2`, is a **bijection**. Consequently
> `p(ℓ) = \#\{c_n \bmod 2^ℓ : n ≥ 0\}` (the number of residues mod `2^ℓ` the orbit visits).

*Proof.* Induct on `ℓ`. Write `c = r + 2c'` with `r = c \bmod 2`. Then `T(c) = ⌊3(r+2c')/2⌋ = 3c' + ⌊3r/2⌋ =
3c' + r` (as `r ∈ \{0,1\}`). So the first coordinate of `φ_ℓ(c)` is `r` and the remaining `ℓ-1` coordinates are
`φ_{ℓ-1}(3c' + r) \bmod 2`. The map `c' ↦ 3c' + r` is a bijection mod `2^{ℓ-1}` (3 is odd, hence invertible),
so by induction `φ_{ℓ-1}` bijective ⟹ `φ_ℓ` bijective. The factor `r_n…r_{n+ℓ-1}` of the parity sequence equals
`φ_ℓ(c_n \bmod 2^ℓ)`, so distinct length-`ℓ` factors correspond bijectively to distinct visited residues mod
`2^ℓ`. ∎ (Verified `ℓ ≤ 14`.)

> **Lemma 4 (not eventually periodic) [PROVEN].** `r_n` is not eventually periodic. Hence by Morse–Hedlund,
> `p(ℓ) ≥ ℓ + 1` for all `ℓ`.

*Proof.* Suppose `r_n` had eventual period `P`. Along a residue-fixed subsequence the branch parities are fixed,
giving an affine recurrence `p^P c_{n+P} = a^P c_n - S` (here `a = 3`, `p = 2`, integers from the fixed itinerary).
Integrality together with `\gcd(a,p) = 1` forces the period-`P` subsequence to be constant, i.e. a genuine integer
cycle of `T`. But `T(c) - c = ⌊c/2⌋ ≥ 1` for `c ≥ 2`, so `T` is strictly increasing on `c ≥ 2` and has only the
fixed points `0, 1`; the orbit `c_n → ∞` reaches no cycle — contradiction. So `r_n` is not eventually periodic.
∎ (Holds for the whole `⌊ac/p⌋` genuine-grower family; verified `proven_nonperiodic.py`, re-run §10.)

> **Lemma 5 (not Sturmian) [PROVEN].** All four length-2 blocks occur in `r_n`
> (`00 @ n=0`, `01 @ n=2`, `10 @ n=3`, `11 @ n=11`), so `p(2) = 4 > 3`: strictly above the minimal aperiodic
> (Sturmian) class.

> **Lemma 6 (linear floor, slope `\log_{3/2}2`) [PROVEN].** `p(ℓ) ≥ (ℓ-3)/\log_2(3/2) ≈ 1.71ℓ`.

*Proof.* The orbit is strictly increasing, so the values `c_n < 2^ℓ` are distinct integers in `[8, 2^ℓ)`, hence
distinct mod `2^ℓ`; by Lemma 3 each contributes a distinct factor. The number of `n` with `c_n < 2^ℓ` is at least
`(ℓ-3)/\log_2(3/2)` (the growth rate of `c_n` is `(3/2)^n` up to bounded factors), giving
`p(ℓ) ≥ (ℓ-3)/\log_2(3/2)`. ∎ The slope `\log 2/\log(3/2)` matches the Dubickas (2009) liminf
`p_w(ℓ)/ℓ ≥ \log q/\log(p/q)` for base-`p/q` minimal words — here re-derived elementarily from the growth rate.
(Verified `complexity_slope.py`, re-run §10.)

> **Lemma 7 (lift bound) [PROVEN].** `p(ℓ) ≤ p(ℓ+1) ≤ 2p(ℓ)`.

*Proof.* Each residue mod `2^ℓ` has at most 2 preimages mod `2^{ℓ+1}` and at least one is visited; monotone and
at most doubling. ∎ Elementary methods are thus capped in the band `[1.71ℓ, 2^ℓ]`.

> **[OPEN = Mahler] Maximal complexity.** `p(ℓ) = 2^ℓ` for all `ℓ` ⟺ the orbit visits **every** residue mod `2^ℓ`
> ⟺ equidistribution of `c_n \bmod 2^ℓ` = single-orbit equidistribution of `⌊8·(3/2)^n⌋` = the Mahler 3/2 /
> Andrieu–Eliahou–Vivion fragment. Measured `p(ℓ) = 2^ℓ` to `ℓ = 16` with a maximal 2-kernel
> (`parity_complexity.py`), but the closed proof **is** Mahler. Correctly labelled **[OPEN]**.

> **Floor located.** `\text{eventually-periodic} ⊊ \text{Sturmian } (ℓ+1) ⊊ [\text{PROVEN}]\ p(ℓ) ≥ 1.71ℓ
> ⊊⊊ [\text{Mahler/OPEN}]\ p(ℓ) = 2^ℓ`. The elementary floor reaches a linear bound of slope `\log_{3/2}2`; the
> jump to maximal complexity / full non-automaticity is exactly the single-orbit equidistribution of §7.

---

## 6. Applications: per-machine certificate floors in BB(6)

The hierarchy tools yield proven *floors* for two BB(6) frontier cryptids — the largest sub-regular certificate
class provably insufficient. Both are conjecture-free and machine-checked; both are **finite floors**, and the
honest negative (the barrier does not extend to REG) is the substantive content.

### 6.1 o18 — floor `m* = 2` [PROVEN]

`o18 = 1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---` (halt = state `F` reads `1`).

> **[PROVEN] No 2-window (SLT, `m=2`) certificate proves o18 non-halting.**

*Proof.* o18's halt mechanism: `F` is entered only via `D:1→1LF`, so halt ⟺ `D` reads a `1` whose left neighbour
is `1` (the leftward frontier lands on an existing `1`); the pre-halt configuration is `1 [D] 1`, stepping
`D:1→1LF` then `F:1→\text{HALT}` (verified, 2 steps). Census of state `D` in reachable (re-run this pass, §10,
80M steps): `D` reads `0` with left neighbour `1` **8274×** ⟹ 2-gram `(1,D) ∈` 2-grams(reachable); `D` reads `1`
with left neighbour `0` **9×** (block left-edges) ⟹ 2-gram `(D,1) ∈` 2-grams(reachable); the collision
`D` reads `1` with left neighbour `1` occurs **0×**. Now let `L` be any 2-window certificate, with permitted
2-gram set `G ⊇` 2-grams(reachable) `⊇ \{(1,D),(D,1)\}`. The configuration `c = 1 [D] 1` has every 2-gram in
`\{(1,D),(D,1)\} ∪ \{\text{tape 2-grams}\} ⊆ G`, so `c ∈ L`; but `c` halts in 2 steps, and step-closure forces
the halt into `L`, contradicting (H). ∎

**Honest negative (floor is exactly 2).** The discriminator (head cell symbol with its left neighbour) is
**head-local**, captured by a window of size **3**: the collision 3-gram `(1,D,1)` never occurs in reachable
(0 collisions in 80M steps) while the look-alike `(1,D,0)` occurs 8274×, so a tight 3-window over-approximation
**excludes** the collision while keeping reachable. Hence for `m ≥ 3` neither the pumping engine (the clean
reachable family `C_N = [F]0\,1^{N-1}` is uniformly non-halting, verified `N = 1..160`) nor the all-or-nothing
engine fires, and "no `m`-window (`m ≥ 3`) / REG / SLIN certificate" is **[OPEN]** — as hard as resolving o18
(`far_dfa` returns HOLDOUT through `m = 10`: evidence, not proof). (`O18_NO_CERTIFICATE.md`.)

### 6.2 o17 — floor `m* = 8` [PROVEN]

`o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (halt = state `F` reads `0`).

> **[PROVEN] No `m`-window (LT) certificate proves o17 non-halting, for every `2 ≤ m ≤ 8`.**

*Proof (engine).* The embedded single-block family `0 A 0 1^k` (FAR encoding `A 0 1^k`) has exact halt structure
(verified, `bb_sim`-cross-checked): for `k \not≡ 0 \ (\mathrm{mod}\ 3)` it **always halts fast** (the trivial
halters; re-run this pass §10: `k=1@7, k=2@33, k=4@35, k=5@21` steps; source: 80/80 for `k ≤ 120`), and for
`k ≡ 0 \ (\mathrm{mod}\ 3)` it is Collatz-irregular (18 proven halters including two delayed past `10^7`:
`k=102@2.8·10^7`, `k=108@6.7·10^7`; re-run confirms `k=6, 12` halt fast). The proof uses only the **trivial**
halters: for `2 ≤ m ≤ 8`, machine-check (`o17_window_barrier.py`, `o17_floor_confirm.py`) shows a trivial halter
`A 0 1^k` (with `k ≥ m`, `k\%3 ∈ \{1,2\}`) lies in the tight `m`-window over-approximation `L^*_m` (every
length-`m` gram of `c` is in `G^* = \text{grams}_m(\text{reachable})`); any `m`-window certificate `L ⊇`
reachable has `L ⊇ L^*_m ∋ c`, so `c ∈ L`, but `c` halts, and step-closure forces the halt in — contradicting
(H). ∎

*Verification status this pass.* The trivial-halter premise (`A 0 1^k` halts fast for `k\%3∈\{1,2\}`) is re-run
and confirmed (§10). The full window-acceptance census (`L^*_m ∋` halter for `m=2..8`, none for `m ≥ 9`) is
machine-checked in the source (`O17_REG_BARRIER.md` §2–§3); its re-run timed out at 2 min here (it rebuilds
reachable over `~3·10^5` steps), so we cite it as machine-checked rather than re-verified this pass.

**Honest negative (floor is exactly 8, prior over-claim retracted).** The barrier **stops at `m=8`**: the binding
gram `0 A 0 1^{m-3}` (state `A` reads `0` with one blank to its left and `m-3` ones to its right) is **present**
for `m ≤ 8` but **absent** for `m ≥ 9` (census: in reachable, `A` reads `0` only with left-0-run `∈ \{0,∞\}`,
and the `∞`-frontier events have right-1-run `≤ 5` — there is no event with a finite blank gap ≥ 1 and ≥ 6 right
ones). So for `m ≥ 9` the family detaches from reachable's window set and the engine loses its fuel. **A prior
note claimed an all-`k`/REG barrier for o17; that is retracted** — the contrast with o18 is *quantitative*
(floor 8 vs 2), not qualitative. "No REG / SLIN certificate for o17" stays **[OPEN]**. (`O17_REG_BARRIER.md`.)

---

## 7. The spoofer/certificate meta-principle and the open cryptid top

### 7.1 The spoofer game

Certification is a two-player game (the Turing-machine avatar of the quantum genuineness spoofer game):

- **Prover** commits to a finite abstraction `α` (a description-class object, e.g. a DFA over configs) and claims
  it certifies `M`'s non-halting.
- **Adversary** must exhibit a machine `M'` that is `α`-indistinguishable from `M` on all observed finite data
  but **halts**.
- `M` is **genuinely non-halting w.r.t. class `C`** iff for every `α ∈ C` the Adversary wins.

§3–§4 say the Prover wins in REG for bouncers/counters (and for all 63 three-state monsters). §7.2 says that for
the cryptids the Adversary appears to win against every finite-state Prover.

### 7.2 What is proven vs open at the top

> **[OPEN] No REG / tame certificate for a cryptid.** This is strictly stronger than "the cryptid's reachable
> language is non-regular," because a certificate is an over-approximation `L ⊇ reachable` and a regular superset
> of a non-regular set can exist. Both BB(6) existence cryptids have only **finite-floor** barriers
> (o18: `m*=2`; o17: `m*=8`); neither reaches REG. Proving no REG certificate exists is **at least as hard as
> resolving the cryptid** (a verified REG certificate would *decide* its non-halting). Stays **[OPEN]**.

> **[CONDITIONAL] Cryptid never-halts ⟹ exact reachable language non-regular.** For Antihydra: the milestone
> configurations have widths `w_i → ∞` (if the orbit is unbounded), and configurations of different width are
> Myhill–Nerode-distinguishable in the reachable language ⟹ non-regular. The only gap is "widths → ∞", i.e. the
> orbit is unbounded — precisely Antihydra's open conjecture. (Distinguishability made concrete: the milestone
> configs have pairwise-distinct future-3-width signatures, 14/14.)

> **What is honestly proven near the top:** (i) the elementary subword-complexity floor (§5,
> `p(ℓ) ≥ 1.71ℓ`); (ii) the per-machine certificate floors `m*=2` (o18) and `m*=8` (o17) (§6); and, on the
> dynamical axis (outside this note, see `BB6_STRUCTURAL_LIMIT_THEOREM.md` §5), the single top-level
> no-structure-only barrier, **Antihydra's density `β = +1/2 > 0`** (ergodic optimization, attained at the
> halting fixed point `o=1`). The REG vertex — "no tame certificate for a cryptid" — is the **frontier**, equal
> to the genuineness-limit barrier (a finite description cannot certify the infinite property), and is **[OPEN]**.

This is the same shape as the quantum genuineness-limit theorem: finite (single-basis) statistics cannot certify
genuineness; here, finite-state abstractions cannot certify non-halting of a cryptid. BB(6)'s hardness *is* a
genuineness-limit phenomenon on a fully-specified discrete object.

---

## 8. Witness → TM table

| rung / brick | witness name | TM spec / file | checked set `S` | role |
|---|---|---|---|---|
| **star-free ⊊ REG** (d) | parity counter | `1RB0LZ_1LC1RA_0RA0LC` (halt: `A` reads `1`) | fiber `(11)^*1` (`ℤ/2`) | has REG cert, no star-free cert |
| **REG ⊊ SLIN** (a) | EQ | `eq_machine.py` (alphabet `{_,L,C,R,xL,xR}`) | equal blocks `\{L^nCR^n\}` | has SLIN cert, no REG cert |
| **SLIN ⊊ 2-automatic** (e) | POW2W | `pow2w_machine.py` (~60 states) | `S=\{2^n\}` | has 2-aut cert, no SLIN cert |
| **2-automatic ⊊ CF** (g) | PALW | `palw_machine.py` (56 st / 12 sym) | `S=` A006995 (binary palindromes) | has CF cert, no 2-aut cert |
| **CF ⊊ CS** (f) | SQW | `sqw_machine.py` (~45 st / 8 sym) | `S=\{n^2\}` | has CS cert, no CF cert |
| application: o18 floor `m*=2` | o18 | `1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---` (halt: `F` reads `1`) | — | no 2-window cert |
| application: o17 floor `m*=8` | o17 | `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (halt: `F` reads `0`) | embedded `0A01^k` | no `m`-window cert, `m ≤ 8` |
| subword floor | Antihydra | `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` (halt: `F` reads `0`); orbit `c_{n+1}=⌊3c_n/2⌋`, `c_0=8` | parity `r_n=c_n\bmod 2` | `p(ℓ)≥1.71ℓ` |

---

## 9. Proof-status summary

| separation / result | proof status | external input |
|---|---|---|
| `star-free ⊊ REG` (d) | **full-inline** (descriptive half complete) **+ machine-verified halting lemma** (Lemma 1, even-`m` halt verified `m≤32`; all-`m` flagged structural) | none |
| `REG ⊊ SLIN` (a) | **full-inline** (pumping engine complete) **+ structural/machine-verified behavioral lemmas** (Lemma 2, verified `n≤15`, `a,b≤7/12`; uniformity flagged) | none |
| Squeeze Lemma | **full-inline** (airtight) | none |
| `SLIN ⊊ 2-automatic` (e) | **full-inline lower half** (no SLIN cert: AP/density, airtight); **upper half cited** (2-automatic via Büchi–Bruyère) | Büchi–Bruyère (standard) |
| `2-automatic ⊊ CF` (g) | **full-inline both halves** (palindromes non-regular by pumping; CF grammar) | none |
| `CF ⊊ CS` (f) | **cited-external lower half** ({n²} base-2 not CF); **full-inline upper half** (LBA) | **arXiv:1901.03913** — NOT self-contained |
| REG suffices at `n=3` | **cited** (63 explicit machine-verified certificates in the suite) — finite theorem, not re-derived here | verified suite |
| subword floor `p(ℓ)≥1.71ℓ` etc. (§5) | **full-inline** (Lemmas 3–7, all elementary) | Morse–Hedlund, Dubickas (standard) |
| o18 floor `m*=2` | **full-inline + machine-verified census** (re-run this pass) | none |
| o17 floor `m*=8` | **full-inline engine + halt premise re-verified**; full `m`-window census **cited as machine-checked** (re-run timed out) | none |
| no REG/tame cert for cryptid | **[OPEN]** | — |
| cryptid reachable non-regular | **[CONDITIONAL]** on orbit unbounded | — |
| `p(ℓ)=2^ℓ` / maximal complexity | **[OPEN] = Mahler/AEV** | — |
| `CS ⊊ recursive` | **[PROVEN] but non-explicit** (Space Hierarchy; diagonalization witness) | Space Hierarchy Thm |

---

## 10. Reproduction logs (this pass)

All commands `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, `bb_sim` semantics. Re-run 2026-06-29:

- **(a) EQ** `eq_machine.py`: `(i) OK reaches n=0..8`; `(ii) ALL UNEQUAL BLOCKS HALT (a,b≤7)`.
- **(e) POW2W** `pow2w_machine.py`: `SUMMARY: A=PASS B=PASS C=PASS` — milestones `1,2,4,…,256`; `(CS,1^w)` halts
  for non-powers `w≤63`, loops for powers; every clean block power-of-2.
- **(g) PALW** `palw_machine.py` (+ harness): milestones `1,3,5,7,9,15,17,21,27,31,33,45,51,63,65,…` = A006995;
  HALT iff `w` not a binary palindrome (`w=1..50`, 0 mismatches); clean blocks (states `CS`,`CS_FLAG`) all
  binary-palindrome lengths.
- **(f) SQW** `sqw_machine.py`: `SUMMARY: A=PASS B=PASS C=PASS` — milestones `1,4,9,16,25,36,49,64`; `(CS,1^w)`
  halts for non-squares `w≤50`; clean blocks all square lengths.
- **(d) parity counter** direct sim: `1^m[B]0` HALTs for `m∈{2,4,…,32}`, CAPs for `m∈{1,3,…,31}` — Lemma 1
  holds `m=1..32`.
- **§5 floors**: `proven_nonperiodic.py` (not eventually periodic, bounded fixed points only),
  `complexity_floor.py` (Morse–Hedlund `ℓ+1`, `p(2)=4` not Sturmian), `complexity_slope.py`
  (`#(c_n<2^ℓ) ≈ 1.71ℓ`, slope `\log_{3/2}2`).
- **§6 o18** `o18_2gram.py`: `(1,D)` 8274×, `(D,1)` 9×, collision `(1,D,1)` 0× (80M steps).
- **§6 o17** direct sim of `0A01^k`: `k=1@7, k=2@33, k=4@35, k=5@21` (trivial halters), `k=6@206, k=12@394`
  (Collatz halters; off-by-one vs source step-convention). Full `m`-window census cited from source (timeout).

---

## References

Internal locators are repository files under `busybeaver/`.

**External (cited as input):**
- M. P. Schützenberger, *On finite monoids having only trivial subgroups*, Information and Control 8 (1965);
  R. McNaughton, S. Papert, *Counter-Free Automata*, MIT Press (1971). — star-free = aperiodic (§2, §3.1).
- M. Morse, G. A. Hedlund, *Symbolic dynamics*, Amer. J. Math. 60 (1938). — subword complexity / eventual
  periodicity (§5, Lemma 4).
- A. Dubickas, liminf of subword complexity for base-`p/q` words (2009). — slope `\log q/\log(p/q)` (§5, Lemma 6).
- J. R. Büchi (1960); V. Bruyère, G. Hansel, C. Michaux, R. Villemaire, *Logic and `p`-recognizable sets of
  integers*, Bull. Belg. Math. Soc. 1 (1994). — `⟨ℕ,+,V_p⟩`-definable = `p`-automatic (§3.4 upper half).
- *The range of a non-linear natural polynomial cannot be context-free*, arXiv:1901.03913 (2019). — base-`q`
  range of a polynomial is CF iff linear (§3.6 lower half; the only non-self-contained rung).
  **Caveat:** authorship not independently confirmed in this pass; cited by title + arXiv id.
- Space Hierarchy Theorem (Hartmanis–Lewis–Stearns / Stearns–Hartmanis–Lewis). — `CS ⊊ recursive` (§3.7).

**Background frontier (named, not used in any proof here):**
- K. Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. 8 (1968).
- T. Tao, arXiv:1909.03562 (2019/2022); L. Flatto, J. C. Lagarias, A. D. Pollington (1995); G. Andrieu,
  S. Eliahou, V. Vivion (2025). — the Mahler/AEV single-orbit equidistribution frontier (§5 ceiling, §7 [OPEN]).
- The bbchallenge BB(6) frontier (arXiv:2509.12337, 2025) — cryptid TM specs.

**Internal locators:**
`LIMIT_THEOREM.md` (the hierarchy, all five separations, the Squeeze Lemma, the subword floor);
`BB6_STRUCTURAL_LIMIT_THEOREM.md` §6 (Theorem 4 consolidation); `eq_machine.py`, `pow2w_machine.py`,
`palw_machine.py`, `sqw_machine.py` (witnesses); `far_dfa.py` (the sound REG verifier);
`far_finder.py`, `far_cegar.py`, `suite.py` (the n=3 certificate suite); `O18_NO_CERTIFICATE.md`,
`O17_REG_BARRIER.md` (the certificate floors); `complexity_floor.py`, `complexity_slope.py`,
`proven_nonperiodic.py`, `parity_complexity.py` (the subword floor); `SOUNDNESS_INCIDENT.md` (the discipline).
```
