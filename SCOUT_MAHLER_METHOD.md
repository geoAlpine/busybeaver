# Cross-disciplinary scout — Mahler's METHOD (functional equations) on the Antihydra kernel (2026-06-30)

*Literature scout. Does Mahler's METHOD for functional equations `f(z^k)=R(z,f(z))` (Mahler 1929; Nishioka;
Adamczewski–Faverjon; Becker; Bell–Coons) give a GENUINELY NEW attack on the kernel (K)? NOT Mahler's 3/2 problem —
a different theory. SOUNDNESS PARAMOUNT: every claim labelled; transcendence ≠ equidistribution kept honest; (K) is
NOT solved; no label upgraded. This note REFUTES the central hope (no Mahler equation holds for the kernel's
generating function) and locates the one near-miss sub-thread. NOT committed by default.*

---

## 0. One-line verdict

> **[NOT-APPLICABLE]** to the frequency kernel (K). A Mahler functional equation **provably does NOT hold** for the
> kernel's generating function: a *bounded* `k`-regular sequence is exactly a `k`-automatic one, and the Antihydra
> parity/moving-diagonal word is **PROVEN non-automatic** (subword complexity `≥1.71ℓ`, irregular; non-Pisot base,
> unbounded carry). The only Mahler structure present in the orbit is the **fixed-column** read of `3ⁿ` (Rowland —
> eventually periodic ⇒ automatic ⇒ Mahler), which is the *already-equidistributed easy part* and the
> *already-closed* automatic-sequence wall — not the moving diagonal that is (K). Even granting an equation, Mahler's
> method outputs **transcendence / algebraic independence / a rational–transcendental dichotomy of VALUES**, which is
> orthogonal to digit frequency. The single near-miss (regular-sequence summatory asymptotics, Heuberger–Krenn) needs
> the regularity that provably fails and would only reproduce the already-banked `log n` floor.

---

## 1. The kernel and the precise question (so "applicable" is judged against the right bar)

The kernel (`WEAPONS_AUDIT §1`, `SESSION_…_AEV_CORE §4`):
> **(K)** the moving diagonal `d_n = bit_{n+k}(⌊8·(3/2)ⁿ⌋)` equidistributes ⟺ even-density `≥1/3` ⟺ mean `D≥3/2`
> ⟺ single-orbit equidistribution of `c_n mod 2^k` = Mahler 3/2 / AEV Conj 1.6 at `α=8`. **A FREQUENCY statement.**

The proposal to test: does a generating function attached to the orbit — the parity GF `F(z)=Σ b_n z^n`
(`b_n=(−1)^{c_n}` itinerary), the carry GF (`S_n=Σ_{j<n} 3^{n−1−j}2^j b_j`), or the 2-adic/3-adic digit series —
satisfy a **Mahler functional equation** `f(z^q)=R(z,f(z))`; and if so, does Mahler's method reach (K)?

---

## 2. Does a Mahler functional equation hold? — DERIVED / REFUTED [PROVEN, against repo facts]

**The decisive structural theorem (literature).** A power series is a **Mahler function** iff (Becker; Dumas;
Adamczewski–Bell) it is, up to the standard reductions, governed by a finite-dimensional `q`-kernel; the canonical
solutions are generating series of **`q`-regular sequences**, and a sequence is `q`-regular iff its `q`-kernel spans a
**finite-dimensional module** (Allouche–Shallit). Two facts pin the verdict:

- **(i) Bounded `q`-regular ⟺ `q`-automatic.** A `q`-regular sequence taking finitely many values is exactly a
  `q`-automatic sequence (its kernel is then a finite *set*). The parity word `b_n∈{0,1}` is bounded, so *if* its GF
  were Mahler it would be the GF of an automatic sequence.
- **(ii) The kernel word is PROVEN non-automatic.** Repo `[PROVEN]`: subword-complexity floor `p(ℓ)≥1.71ℓ` and
  "IRREGULAR" classification (`LIMIT_THEOREM §3″`), and non-Pisot base `|3/2|₂=2>1` ⇒ the normalization transducer
  does **not** close to a finite automaton; the moving diagonal is **not** an automatic sequence
  (`NEWMATH_DIAGONAL_RENORM §3.2`, `DIGITS_OF_3N §3`).

**⇒ `F(z)=Σ b_n z^n` satisfies NO Mahler functional equation.** The central hope is refuted directly, not by
absence of evidence. (Polynomial-coefficient-growth is necessary for `q`-regularity; the bounded word passes that
trivially, but fails the finite-kernel/automaticity test.)

**The carry/digit GF fares no better, and for the SAME proven reason.** The exact self-similar recurrence
(`NEWMATH_DIAGONAL_RENORM §2`) is
`d_{n+1}^{(k)} = d_n^{(k+1)} ⊕ d_n^{(k)} ⊕ γ_n^{(k)}` with an **unbounded-range carry** `γ` (the `c_n mod 2ⁿ` tail).
A Mahler equation is **base-`q` for a single integer `q`** (it relates `f(z),f(z^q),f(z^{q²})…`); the Antihydra
object is intrinsically a **mixed base-2 ⊗ base-3** structure (`×3` written in binary). That is the *several-variable*
Mahler regime (Adamczewski–Faverjon, *Mahler's method in several variables and finite automata*, Annals 2021;
arXiv:2012.08283) — but the several-variable theory **also** runs on regular/automatic linear representations, and the
unbounded non-Pisot carry is precisely the obstruction that prevents a finite linear representation. **No finite
Mahler system, single- or multi-variable, represents the moving diagonal.**

**Where a Mahler equation DOES hold — and why it is the wrong place.** A *fixed column* `n ↦ bit_k(3ⁿ)` (`k` fixed)
is eventually periodic (Rowland, arXiv:0902.3257) ⇒ automatic ⇒ its GF **is** a Mahler function. But the fixed-column
read is exactly the **already-equidistributed / Weyl-controlled top-bit part** (`EFFECTIVE_TOPDIGIT`), and Rowland's
regularity provably **misses the moving diagonal** that is (K). So Mahler structure exists for the easy read and
**vanishes at the hard one** — the same automatic-sequence boundary already closed under Mauduit–Rivat / the
certificate hierarchy (`2-automatic ⊊ CF ⊊ CS`, `LIMIT_THEOREM §2`).

---

## 3. IF an equation held, what would Mahler's method give? — transcendence, NOT frequency [honest]

Mahler's method (Mahler 1929; Nishioka's theorem; Adamczewski–Faverjon PLMS 2017, *relations linéaires, transcendance
et applications aux nombres automatiques*) transfers algebraic/linear independence of the **functions**
`f₁(z),…,f_m(z)` over `Q(z)` to independence of their **values** `f_i(α)` at algebraic `α` in the open unit disc. Its
outputs are:
- **transcendence** of the value `f(α)`;
- **algebraic independence** of several Mahler values (Philippon; Adamczewski–Faverjon several variables);
- the **rational–transcendental dichotomy**: a Mahler function is either rational or transcendental
  (Bell–Coons–Rowland, *The rational–transcendental dichotomy of Mahler functions*).

**None of these is a statement about digit frequencies.** Transcendence of a number says nothing about whether its
digits equidistribute (it is *open* whether any algebraic irrational is normal; conversely Liouville-type transcendentals
are wildly non-normal). The Thue–Morse / paper-folding GF values are transcendental, yet that fact is silent on the
density of `1`s. **(K) is a frequency/equidistribution statement; Mahler's method speaks only to arithmetic nature of
values.** So even in the counterfactual where an equation held, the method would land **orthogonal to the kernel** —
this is the cleanest "transcendence ≠ equidistribution" wall, distinct from but parallel to the program's Wall I/II.

---

## 4. Recent (2018–2026) results that touch DIGIT functions / FREQUENCIES — the only near-miss

The frequency-flavored corner of this circle is **asymptotic analysis of regular sequences**, not transcendence:
- **Heuberger–Krenn** (*Asymptotic analysis of regular sequences*, arXiv:1810.13178): the summatory function of a
  `q`-regular sequence decomposes as `Σ (periodic fluctuation)·(scaling factor)`, with exponents = eigenvalues of the
  linear representation exceeding the joint spectral radius. *This is the one machine in the area that would output a
  density* `Σ_{n<N} b_n ∼ C·N` — **but only for a `q`-regular sequence.**
- **Bell–Coons–Hare** minimal-growth / gap (arXiv:1410.5517): an unbounded `q`-regular sequence satisfies
  `|f(n)| > c·log n` infinitely often. Note this `log n` shape **coincides with the repo's banked floor**
  `#even(n) ≥ 0.89 log n` (`ANNEALED_PARTIAL_BANKED`) — a suggestive echo, but coincidental: Antihydra's parity is
  *not* regular, so the theorem does not apply, and `log n` is the same floor already far below the needed `εN`.

**Verdict on the near-miss.** This sub-thread is the closest the field comes to frequencies, but it is gated on the
exact property the orbit **provably lacks** (regularity ⇔ automaticity, §2). It is therefore a **[NEAR-MISS] that
collapses to [ALREADY-CLOSED-in-disguise]** = the automatic-sequence / Mauduit–Rivat / certificate-hierarchy wall the
program has documented. No 2018–2026 Mahler-method result bounds the digit frequency of a *non-automatic* deterministic
sequence.

---

## 5. Novelty vs the closed-routes list

Mahler's METHOD is **not** explicitly on the closed list (vdC/Weyl, Mauduit–Rivat, decoupling, sum-product, Baker/LMN,
transfer-operator, measure-rigidity, Rajchman, Hochman–Varjú, computability/normality, specification, Korobov–Bourgain).
But its applicability hypothesis (a finite Mahler system / regular linear representation) is **equivalent to
automaticity**, and automaticity for this word is the object already killed under (a) **Mauduit–Rivat / Konieczny–BKM**
Gowers-uniformity-of-automatic-sequences (`FRESH_ANGLES §4` notes the word is non-automatic, so those don't bite either),
(b) the **Schnorr–Stimm / finite-state-normality** route (`SELECTOR_COMPUTABILITY`: non-Pisot kills the finite-state
characterization), and (c) the **certificate hierarchy** (`LIMIT_THEOREM`). So Mahler's method is a **new entry that
reduces to an already-proven obstruction** — it is *named differently* but blocked by the *same* non-automaticity /
non-Pisot fact. Genuinely new as a checked field; not a new wall.

---

## 6. Verdict

| question | answer |
|---|---|
| Does a Mahler functional equation hold for the parity / carry / diagonal GF? | **NO** [PROVEN, via bounded-regular⇔automatic + proven non-automaticity] |
| Does it hold anywhere on the orbit? | only for **fixed-column** reads of `3ⁿ` (Rowland) = the already-equidistributed easy part |
| If it held, what would Mahler's method give? | transcendence / algebraic independence / rational–transcendental dichotomy of **values** |
| Does that reach the frequency kernel (K)? | **NO** — transcendence ≠ equidistribution (orthogonal) |
| Frequency-flavored sub-thread? | regular-sequence summatory asymptotics (Heuberger–Krenn) — needs regularity that **fails** |
| **Overall** | **[NOT-APPLICABLE]** to (K); the regular-sequence asymptotic sub-thread is **[NEAR-MISS] → [ALREADY-CLOSED-in-disguise]** (automaticity / non-Pisot wall) |

**Single most promising sub-thread (honest, [OPEN] only as a hypothetical):** *Heuberger–Krenn summatory asymptotics
for `q`-regular sequences* — the only tool in the Mahler-method orbit that outputs a density directly. It would apply
**iff** one could exhibit a finite linear representation of the moving diagonal, which is exactly the non-Pisot /
unbounded-carry obstruction (`NEWMATH_DIAGONAL_RENORM §3.2`). So it re-states the wall (finite-state ⇔ Pisot ⇔ would
already be decidable) rather than breaching it. Not worth a numerical probe: regularity is *proven* absent.

---

## Sources

- B. Adamczewski, *Mahler's method* (survey/selecta): http://adamczewski.perso.math.cnrs.fr/Mahler_selecta_new.pdf
- B. Adamczewski, C. Faverjon, *Méthode de Mahler: relations linéaires, transcendance et applications aux nombres
  automatiques*, Proc. LMS 2017; and *Mahler's method in several variables and finite automata*, Ann. of Math. 2021
  (arXiv:2012.08283; theory of regular singular systems arXiv:1809.04823).
- J. Bell, M. Coons, E. Rowland, *The rational–transcendental dichotomy of Mahler functions*, J. Integer Seq. 16 (2013):
  https://cs.uwaterloo.ca/journals/JIS/VOL16/Bell/bell2.pdf
- J. Bell, M. Coons, K. Hare, *The minimal growth of a `k`-regular sequence*, arXiv:1410.5517.
- C. Heuberger, D. Krenn, *Asymptotic analysis of regular sequences*, arXiv:1810.13178.
- P. Becker, *`k`-regular power series and Mahler-type functional equations*, J. Number Theory 1994; criteria for
  regularity / Becker's conjecture arXiv:1512.04326, arXiv:1802.08653; height gap for Mahler coefficients arXiv:2003.03429.
- J.-P. Allouche, J. Shallit, *The ring of `k`-regular sequences* (definition; bounded-regular ⇔ automatic).
- E. Rowland, *binary `3ⁿ` column regularity*, arXiv:0902.3257 (fixed columns automatic; moving diagonal missed).
- Repo: `NEWMATH_DIAGONAL_RENORM.md` (§2 exact recurrence, §3.2 non-Pisot no-automaton), `LIMIT_THEOREM.md`
  (non-automatic, subword floor, certificate hierarchy), `DIGITS_OF_3N.md`, `EFFECTIVE_TOPDIGIT.md`,
  `SESSION_2026-06-29_AEV_CORE.md`, `WEAPONS_AUDIT_2026-06-29.md`, `FRESH_ANGLES_SCOUT.md`,
  `BB6_OBSTRUCTION_DICHOTOMY.md`.

No machine decided. No label upgraded.
