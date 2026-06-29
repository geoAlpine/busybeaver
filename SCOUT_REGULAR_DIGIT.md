# Cross-disciplinary scout — k-regular sequences (Allouche–Shallit) + recent (2020–26) non-automatic digit machinery vs the Antihydra kernel (2026-06-30)

*Scouting brief. Field surveyed: **k-regular sequences** (Allouche–Shallit; Bell–Coons–Hare distribution theory; Charlier–
Cisternino–Stipulanti **p/q-regular** sequences in rational-base numeration; Akiyama–Frougny–Sakarovitch rational-base
number systems) and the **2020–2026 Gowers-norm / digit-distribution machinery for non-automatic sequences**
(Byszewski–Konieczny–Müllner; Müllner–Spiegelhofer; Drmota–Mauduit–Rivat; Jelinek 2025). GOAL: a genuinely new applicable
angle from a field NOT in the closed-routes list. Every claim labelled. WebSearch-driven. NOT committed.*

Kernel recall (`SESSION_2026-06-29_AEV_CORE.md`, `WEAPONS_AUDIT_2026-06-29.md`): the whole problem reduces to
**(K)** = single-orbit equidistribution of `c_n mod 2^k` for `c₀=8`, `c→⌊3c/2⌋` = base-3/2 normality of the orbit =
Mahler `{(3/2)ⁿ}` = AEV Conj 1.6 at α=8. The bare object is the **moving diagonal** `d_n = bit_{n+k}(⌊8(3/2)ⁿ⌋)`; the
carry is `S_n = Σ_{j<n} b_j 2^j 3^{n−1−j}` (`b_j = c_j mod 2`).

---

## 0. One-line verdict

**The orbit and the carry are NOT k-regular** — decisively, by the Allouche–Shallit **polynomial-growth theorem**: every
ℤ-valued k-regular sequence satisfies `lim sup log|a_n|/log n < ∞` (at most polynomial growth), whereas `c_n ≍ (3/2)ⁿ` and
`S_n` grow **exponentially**. Regular-sequence distribution theory (Bell–Coons–Hare mod-pᵏ) and the 2020–26 Gowers/digit
machinery (Byszewski–Konieczny–Müllner; Jelinek 2025) **require either k-regularity, k-automaticity, or a Pisot / linearly-
recurrent numeration** — the orbit has **none** of these (exponential growth, non-automatic full-complexity word, non-Pisot
base 3/2 with a **non-regular** representation language). So the machinery, if it applied, would deliver exactly the mod-2ᵏ
density = (K) — but it provably does not reach our object. **Verdict: NEAR-MISS that resolves to ALREADY-CLOSED**, via a
genuinely new *reason* (formal-language non-regularity of the base-3/2 system), and one genuinely new descriptive sub-thread
(the **p/q-regular decorated-tree** lens) that is fresh but re-derives the wall.

---

## 1. Is the orbit / carry k-regular? [ALREADY-CLOSED — decisive growth test]

**Test (Allouche–Shallit, 1992).** A k-regular sequence is one whose **k-kernel** `{(a(kᵉn+r))_n : e≥0, 0≤r<kᵉ}` spans a
**finitely-generated module** over ℤ (a finite-dimensional linear representation). Two proven consequences kill our object:

- **[PROVEN-in-lit] Polynomial growth.** Every ℤ-valued k-regular sequence has `|a_n| = O(n^c)` for some `c`
  (`lim sup log|a_n|/log n < ∞`; Allouche–Shallit; growth exponent = joint spectral radius of the kernel matrices,
  Coons–Tyler, arXiv:1511.07535). **`c_n = ⌊8(3/2)ⁿ⌋ ≍ (3/2)ⁿ` is exponential** ⇒ **not k-regular for any k.** Same for
  `S_n ≍ 3ⁿ`. *This is the decisive one-line obstruction.* The k-kernel cannot be finite-dimensional because `c_{2n}` is
  **quadratic** in `c_n` (`(3/2)^{2n}=((3/2)ⁿ)²`), not a linear combination of shifts — the defining linear recurrence over
  a finite module fails at the root.
- **The x3/2-adder transducer does NOT make it regular.** Yes, `c↦⌊3c/2⌋` is a finite letter-to-letter transducer on
  binary, and (Akiyama–Frougny–Sakarovitch) addition in base 3/2 is a finite right-transducer. But k-regularity/automaticity
  comes from a finite machine reading the **base-k expansion of the INDEX n**, not from a transducer **iterated n times**.
  Iterating a finite transducer is precisely what manufactures the full-complexity, non-finite-kernel behaviour. The
  transducer's finiteness controls only a **bounded** carry window; the kernel bit `d_n` has **unbounded memory**
  `d*(k)=1.71k+2.7` (`CARRY_BOUNDED_MEMORY.md`, `CARRY_*.md`) — exactly the part no finite transducer sees.

**The bounded sub-object (parity bit) is the only candidate left, and it is non-automatic.** `b_n = c_n mod 2 ∈ {0,1}` is
bounded, and *bounded k-regular = k-automatic*. But (a) k-automatic ⇒ subword complexity `O(ℓ)` and the program's word has a
proven floor `p(ℓ)≥1.71ℓ` with conjectured full complexity `2^ℓ` (`LIMIT_THEOREM.md §3″`); (b) automaticity needs a finite
2-kernel `{b(2ᵉn+r)}`, which the (3/2)-recurrence does not produce; (c) the program already lists Gowers/automatic-sequence
as CLOSED (orbit non-automatic). So the parity word is **not 2-automatic**, hence not bounded-2-regular.

**Conclusion §1:** neither the orbit, the carry `S_n`, nor the parity word is k-regular/automatic. The growth theorem is a
clean, decisive, *new-phrasing* restatement of the already-known exponential growth + full complexity.

---

## 2. What regular-sequence + recent digit machinery WOULD give — and why it cannot fire here

| Tool (field) | What it would deliver for (K) | Hypothesis it needs | Status on our object |
|---|---|---|---|
| **Bell–Coons–Hare** distribution of regular seqs mod pᵏ | density/equidistribution of `c_n mod 2^k` = **literally (K)** | sequence is **k-regular** | fails (§1, exponential growth). [NOT-APPLICABLE] |
| Bell–Coons–Hare lower bound `|f(n)|>c log n` i.o. | growth-type fact | k-regular | n/a (and weaker than proven `#even≥0.89 log n`) |
| **Byszewski–Konieczny–Müllner** Gowers norms for automatic seqs (Discrete Analysis 2023, arXiv:2002.09509) | structured⊕uniform split ⇒ all-order Gowers uniformity ⇒ equidistribution of blocks | sequence **k-automatic** + orthogonal to periodics | fails — word non-automatic. [ALREADY-CLOSED] |
| **Jelinek 2025**, *Gowers norms for linearly recurrent numeration systems* (arXiv:2510.16947) | block uniformity in non-standard numeration | **linearly recurrent / Pisot** numeration (Zeckendorf-type) | fails — **3/2 is non-Pisot**, NOT linearly recurrent. [ALREADY-CLOSED, = non-Pisot wall] |
| **Drmota–Mauduit–Rivat / Müllner–Spiegelhofer** digits of `n²`, primes, subsequences | uniform distribution of a digit function along a subsequence | digit function of a **fixed** automatic/q-ary base; index is the polynomial/prime | wrong object — controls digits of `n` along sparse index, not the moving diagonal of `3ⁿ`. = `ATTACK_MAUDUIT_RIVAT.md` [ALREADY-CLOSED] |
| **Müllner** automatic⇒Sarnak / zero entropy | Möbius orthogonality | zero topological entropy automatic seq | n/a; Sarnak already closed (needs zero entropy; we have full complexity) |

**The pattern is uniform and proven:** every one of these reaches the mod-2ᵏ density (= (K)) **only after** assuming a
finiteness the orbit lacks — finite k-kernel (regular), finite automaton (automatic), or a Pisot/linearly-recurrent
recurrence (Jelinek, Drmota–Mauduit–Rivat). The orbit fails all three, for the *same* root reason isolated across the
corpus: the (3/2)-iteration has **unbounded carry memory** and base 3/2 is **non-Pisot**. Jelinek 2025 is the freshest
candidate and is killed by exactly the SELECTOR_COMPUTABILITY §5 non-Pisot obstruction — it is the *numeration-systems
mirror* of "Schnorr–Stimm needs Pisot".

---

## 3. Does it reach the moving-diagonal frequency (the kernel)? [NO]

No. The chain is: regular/automatic/Pisot finiteness → finite linear representation → transfer-operator/Gowers control →
mod-2ᵏ equidistribution = `freq(d_n=0)` density = (K). The **first arrow is false** for the orbit (§1), so the chain never
starts. Concretely the diagonal bit `d_n = bit_{n+k}(⌊8(3/2)ⁿ⌋)` sits at depth `Θ(n)` with carry memory `≈1.71k` — the
unbounded-memory zone a finite kernel/automaton/transducer cannot represent. This is the SAME wall as `DIGITS_OF_3N.md`
(diagonal density, not a fixed column / leading band / count) seen through the regular-sequence lens: a k-regular sequence's
digits *are* eventually a fixed finite-state column structure (Rowland column-periodicity is the k-automatic shadow of
fixed columns of `3ⁿ`), and the diagonal provably escapes every fixed column (samples each column once, below its period).

---

## 4. Novelty assessment — the one genuinely fresh sub-thread

Most of §1–§3 re-derives closed walls. **The genuinely new material from this field:**

- **(NEW reason, not new theorem) Formal-language non-regularity of base 3/2.** Akiyama–Frougny–Sakarovitch (*On the
  representation of numbers in a rational base*; *Powers of rationals modulo 1 and rational base number systems*): the set
  of base-3/2 representations of the integers is **not a regular language** and "defeats every iteration lemma" (not even a
  clean place in the Chomsky hierarchy), yet addition is a finite transducer. This is the **formal-language-theory mirror**
  of the program's non-Pisot / full-complexity / unbounded-memory wall — a new vocabulary for *why* every finiteness
  hypothesis fails. Notably AFS's "powers of rationals mod 1" paper is **literally about `{(3/2)ⁿ}`** = the kernel; the
  rational-base number system is the kernel's native home, and its representation language being non-regular is exactly the
  obstruction restated.
- **(NEW lens, fresh but re-derives the wall) p/q-regular sequences via decorated trees** (Charlier–Cisternino–Stipulanti,
  *Regular sequences and synchronized sequences in abstract numeration systems*, Eur. J. Combin. 2022, arXiv:2012.04969;
  *Revisiting regular sequences in light of rational base numeration systems*, arXiv:2103.16966). Because the base-3/2
  language is non-regular, they **bypass** language-regularity and define **p/q-regularity** = "the numeration tree
  decorated by the sequence is **linear** (each node's decoration is a linear combination of its ancestors')," with a
  graph-directed linear representation. This is a genuinely different descriptive criterion not used anywhere in the corpus.
  **The fresh, concrete, decidable-flavoured question it poses:** is the carry `S_n` (or the diagonal indicator) a
  **p/q-regular decoration of the base-3/2 tree**? If YES, the graph-directed linear representation would give a finite
  spectral object → mod-2ᵏ density → (K). **But the obstruction transfers:** linear tree-decoration is precisely a finite
  linear representation, which (growth, §1) the exponential `S_n` cannot have, and the bounded diagonal indicator would, if
  p/q-regular, be eventually finite-state-structured = automatic-like = contradicting full complexity. So the lens is new
  but lands on the same proven floor. It is the **correct new home to *state* the obstruction**, not a way past it.

**Net novelty:** no new applicable tool; one new *reason* (non-regular base-3/2 language) and one new *descriptive lens*
(p/q-regular decorated trees) — both fresh to the program, both re-deriving the established wall.

---

## 5. Verdict table

| Question | Label | Reason |
|---|---|---|
| Orbit / carry `S_n` k-regular? | **[ALREADY-CLOSED]** | polynomial-growth theorem vs exponential growth — decisive |
| Parity word k-automatic (bounded k-regular)? | **[ALREADY-CLOSED]** | non-automatic, full complexity; no finite 2-kernel |
| Bell–Coons–Hare mod-pᵏ distribution applies? | **[NOT-APPLICABLE]** | needs k-regularity (absent) |
| BKM 2023 Gowers-norm split applies? | **[ALREADY-CLOSED]** | needs k-automatic (= Gowers/automatic route, closed) |
| Jelinek 2025 Gowers for numeration systems applies? | **[NOT-APPLICABLE / = non-Pisot wall]** | needs linearly-recurrent/Pisot; 3/2 non-Pisot |
| Drmota–Mauduit–Rivat / Müllner–Spiegelhofer digit UD applies? | **[ALREADY-CLOSED]** | wrong object (digits of index, not moving diagonal of `3ⁿ`) = Mauduit–Rivat route |
| AFS rational-base / non-regular language | **[NEAR-MISS — new reason]** | formal-language mirror of the wall; home of `{(3/2)ⁿ}` but restates obstruction |
| p/q-regular decorated-tree lens (Charlier et al.) | **[NEAR-MISS — new lens]** | genuinely fresh criterion; linearity = finite representation, blocked by growth/complexity |

**Overall: NEAR-MISS resolving to ALREADY-CLOSED.** Regular-sequence theory and 2020–26 digit machinery would, if they
applied, deliver exactly the mod-2ᵏ density that IS the kernel — but every variant requires a finiteness (finite k-kernel /
finite automaton / Pisot recurrence) that the (3/2)-orbit provably lacks (exponential growth, full complexity, non-Pisot,
non-regular representation language). No reduction; no easier neighbour; consistent with `DIGITS_OF_3N.md`,
`SELECTOR_COMPUTABILITY.md §5`, `WEAPONS_AUDIT_2026-06-29.md`.

**Most promising residual sub-thread:** the **p/q-regular decorated-tree** criterion of Charlier–Cisternino–Stipulanti on
the **AFS base-3/2 tree** — the one descriptive framework native to `{(3/2)ⁿ}` and untried in the corpus. It will not break
(K) (linearity ⇒ finite representation ⇒ contradicts growth/complexity), but it is the most natural *new language* in which
to state the obstruction to an expert, and the only place a future "almost-linear / graph-directed" relaxation might be
worth a single honest probe.

---

## Sources

- Allouche, J.-P., Shallit, J., *The ring of k-regular sequences*, Theoret. Comput. Sci. 98 (1992); II, TCS 307 (2003)
  (definition; **polynomial growth** `O(n^c)`). k-regular sequence overview: https://en.wikipedia.org/wiki/K-regular_sequence
- Coons, M., et al., *Regular sequences and the joint spectral radius*, arXiv:1511.07535 (growth exponent = JSR of kernel
  matrices).
- Bell, J., Coons, M., Hare, K., distribution / lower bounds for k-regular sequences (unbounded ⇒ `|f(n)|>c log n` i.o.);
  Coons–Spiegelhofer chapter https://mcoons-math.github.io/CoonsSpiegelhoferBRchap27Jan2017.pdf
- Byszewski, J., Konieczny, J., Müllner, C., *Gowers norms for automatic sequences*, Discrete Analysis 2023,
  arXiv:2002.09509, https://discreteanalysisjournal.com/article/75201-gowers-norms-for-automatic-sequences
- Jelinek, P., *Gowers norms for linearly recurrent numeration systems*, arXiv:2510.16947 (2025) — Pisot/Zeckendorf only,
  **not** rational base.
- Drmota, M., Müllner, C., Spiegelhofer, L., *Subsequences of automatic sequences and uniform distribution*
  (https://www.dmg.tuwien.ac.at/drmota/drmota-automatic.pdf); Müllner–Spiegelhofer, normality of Thue–Morse along
  Piatetski-Shapiro / squares.
- Akiyama, S., Frougny, C., Sakarovitch, J., *On the representation of numbers in a rational base*
  (https://www.irif.fr/~cf/publications/AFSwords05.pdf); *Powers of rationals modulo 1 and rational base number systems*
  (https://perso.telecom-paristech.fr/jsaka/PUB/Files/RBNS-rev.pdf) — base-3/2 integer language **non-regular**; addition
  is a finite transducer; "powers of rationals mod 1" = the kernel object.
- Charlier, É., Cisternino, C., Stipulanti, M., *Regular sequences and synchronized sequences in abstract numeration
  systems*, Eur. J. Combin. 2022, arXiv:2012.04969; *Revisiting regular sequences in light of rational base numeration
  systems*, arXiv:2103.16966 (**p/q-regular** = decorated numeration tree is **linear**; graph-directed linear
  representation).
- (cross-refs) `DIGITS_OF_3N.md`, `SELECTOR_COMPUTABILITY.md`, `WEAPONS_AUDIT_2026-06-29.md`,
  `SESSION_2026-06-29_AEV_CORE.md`, `LIMIT_THEOREM.md`, `BB6_OBSTRUCTION_DICHOTOMY.md`, `CARRY_BOUNDED_MEMORY.md`.

No machine decided. No label upgraded.
