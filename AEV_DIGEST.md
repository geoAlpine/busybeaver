# AEV Digest — arXiv:2510.11723

**Digest produced 2026-06-28 for the BB6 / Antihydra complete-proof program.**
Source: arXiv abstract page, HTML5 (v2) full text, and PDF (downloaded). Quotes below are
verbatim from the arXiv HTML5 version v2; notation transcribed as faithfully as plain text allows.

---

## 1. Exact identity of the paper

- **Title:** *A Normality Conjecture on Rational Base Number Systems*
- **Authors:** **Mélodie Andrieu, Shalom Eliahou, Léo Vivion** — this is the "AEV" of our notes
  (A = Andrieu, E = Eliahou, V = Vivion). Confirmed.
- **arXiv:** 2510.11723. **v1:** 6 Oct 2025. **v2:** 7 Apr 2026.
- **Classes:** math.NT (primary), math.CO; MSC 11A67, 68R15 (primary); 11K16, 11J71 (secondary).
- **License:** CC-BY 4.0.

**What it is about.** Rational base number systems (Akiyama–Frougny–Sakarovitch 2008). In base
`p/q` two families of infinite words arise: the **minimal words** `wmin_{p/q}(u)` and **maximal
words** `wmax_{p/q}(u)`. The paper conjectures these words are **normal over an appropriate
subalphabet**, and shows this normality conjecture is **equivalent** to an **equidistribution mod
q^k** statement for orbits of the ceiling map `T_{p/q}(x) := ceil(p·x/q)`, and that it would resolve
several long-standing problems: Mahler's Z-numbers (1968), Flatto's Z_{p/q}-numbers (1992), Akiyama's
triple expansions, and the Dubickas–Mossinghoff "4/3 problem" (2009).

> **IMPORTANT correction to our prior notes.** Our memory called this the "AEV normality
> conjecture" and described Conj 1.6 as "single-orbit equidistribution mod 2^k of ceil((3/2)x)".
> The map and the mod-q^k framing are correct, BUT the paper's central object is **normality of the
> minimal/maximal words in the p/q number system**; equidistribution mod q^k (Conj 1.6) is the
> equivalent reformulation, not the primary statement. Also "single-orbit" is accurate in spirit:
> Conj 1.6 asserts equidistribution **for every starting integer n**, i.e. per-orbit.

**Map definition (verbatim):** `T_{p/q}(x) := ceil(p·x/q)` — the **CEILING** map (not floor).

---

## 2. Main results actually PROVEN

The paper's proven content is a chain of **implications/equivalences**, plus extensive numerics.
It proves **no new unconditional facts about distribution of (3/2)^n orbits**.

### Theorem 1.5 [PROVEN]
> "The veracity of Conjecture 1.2 implies that of Conjecture 1.4."

(I.e. the normality conjecture for minimal/maximal words implies the non-existence of
Z_{p/q}-numbers, **under the standing hypothesis p < q²** carried in Conjecture 1.4.)

### Theorem 1.7 [PROVEN] — the equivalence
> "Conjectures 1.2 and 1.6 are equivalent."

This is the load-bearing structural theorem: **normality of minimal/maximal words ⟺
equidistribution mod q^k of the ceiling-map orbits**. This matches our note "Thm 1.7: normality ⟺
T_{3/2} equidistribution"; the "⟹ Mahler when p<q²" half of our note is really **Theorem 1.5**
(Conj 1.2 ⟹ Conj 1.4 ⟹, specialized, Mahler).

**So the proven boundary is: equivalence (1.2 ⟺ 1.6) and implication (1.2 ⟹ 1.4). Everything
downstream — Mahler, Z_{p/q}, triple expansions, 4/3 — is CONDITIONAL on the unproven Conj 1.2/1.6.**

---

## 3. Main CONJECTURES (verbatim)

### Conjecture 1.2 [CONJECTURED] — the normality conjecture (primary object)
> "For all rational bases p/q with p>q≥1 coprime, and for all integer expansions u∈ℒ_{p/q}, the
> infinite word 𝚠𝚖𝚊𝚡_{p/q}(u) is normal over the subalphabet {p−q,…,p−1}. For all integer
> expansions u∈ℒ_{p/q} except for the empty word ϵ, the infinite word 𝚠𝚖𝚒𝚗_{p/q}(u) is normal
> over the subalphabet {0,…,q−1}."

### Conjecture 1.4 [CONJECTURED] — non-existence of Z_{p/q}-numbers (this is the Mahler generalization)
> "Let p>q>1 be coprime integers such that p<q². There exists no positive real number x (called
> Z_{p/q}-number) such that the sequence of fractional parts ({x(p/q)ⁿ})_{n∈ℕ} is contained in the
> subinterval [0,1/q)."

Note the explicit hypothesis **p < q²**.

### Conjecture 1.6 [CONJECTURED] — equidistribution mod q^k of the ceiling orbits
> "Let p>q≥1 be coprime integers. For every n∈ℕ>0 and for every nonnegative integer k, the integer
> sequence (T^l_{p/q}(n))_{l∈ℕ}, obtained by iterating the operator T_{p/q}(x):=⌈p·x/q⌉, is
> equidistributed in the residue classes modulo qᵏ."

This is the statement our program cares about: **per-orbit (every starting n) equidistribution mod
q^k of the ceiling-`(p/q)` map.** For `p=3, q=2` it is exactly: every orbit of `x ↦ ceil(3x/2)` is
equidistributed mod `2^k` for all k.

---

## 4. The precise equivalence / role of p<q²

- **Normality ⟺ equidistribution:** `Conj 1.2 ⟺ Conj 1.6` (**Theorem 1.7**, proven). Normality of
  the minimal/maximal words over the subalphabet is the symbolic-dynamics face; equidistribution of
  `(T^l_{p/q}(n)) mod q^k` is the number-theoretic face. They are the same statement.
- **Equidistribution ⟹ no Z_{p/q}-numbers (Mahler-type):** `Conj 1.2 ⟹ Conj 1.4` (**Theorem 1.5**,
  proven), under **p < q²**.
- **Role of p < q²:** it is the hypothesis under which the normality conjecture yields the
  non-existence of Z_{p/q}-numbers (Conj 1.4). It is the regime where the "forbidden" half-interval
  `[0,1/q)` has measure `1/q` large enough that normality/equidistribution rules out an orbit staying
  inside it. **For 3/2: p=3, q=2, p=3 < 4 = q² — the hypothesis HOLDS**, so the chain applies and
  `Conj 1.2/1.6 ⟹ ` (the original) **Mahler Z-number conjecture**.

**Mahler / 3-2 specialization:** the paper recalls Mahler's 1968 question (Z-numbers x with
`{x(3/2)^n} ∈ [0,1/2)` for all n) and "In 1968, Mahler conjectured that the answer is negative:
Z-numbers do not exist." Conjecture 1.4 is the `Z_{p/q}` generalization; at `p=3, q=2` (interval
`[0,1/q)=[0,1/2)`) it **is** Mahler's original conjecture.

---

## 5. Methods, and the proven/open boundary

**Methods used:**
- **Symbolic dynamics / combinatorics on words** — normality, subalphabets, minimal/maximal words of
  the Akiyama–Frougny–Sakarovitch rational base system; this is the proof engine for the
  equivalence (Thm 1.7) and implication (Thm 1.5).
- **Extensive computer experiments** — richness threshold and deviation-from-normality measurements.
- **NOT used:** no ergodic-theory / transfer-operator / exponential-sum / Fourier / Bernoulli-
  convolution machinery. The hard analytic equidistribution (the actual content of Conj 1.6) is
  **left entirely open**; the paper contributes the *equivalences* and *numerical support*, not an
  analytic attack. (This is the complementary half to our own commit 984f70f Fourier-decay /
  Rajchman line: AEV do not pursue that route.)

**Proven vs open boundary:**
- PROVEN: Thm 1.5 (1.2 ⟹ 1.4 under p<q²), Thm 1.7 (1.2 ⟺ 1.6). These are purely structural.
- OPEN: Conj 1.2, Conj 1.4, Conj 1.6 themselves — for **all** bases including 3/2. Mahler's
  Z-number conjecture remains open and is *not* proven here; it is shown to *follow from* the
  unproven normality/equidistribution conjecture.

---

## 6. Anything UNCONDITIONAL for 3/2 (p=3, q=2)?

**No.** The paper proves **no unconditional distribution result for 3/2** — no density result, no
single proven orbit, no effective discrepancy bound, no one-sided/partial statement. Every 3/2
claim is either (a) conditional on Conj 1.2/1.6, or (b) numerical/empirical.

**Numerical findings for 3/2 (empirical only, not theorems):**
- Studied `wmin_{3/2}(2)`, computing the first **1,000,000** letters.
- **Richness thresholds** (least length at which all subwords of a given length have appeared):
  reported as `2, 6, 51, 54, 123, …` for subword-lengths 1–5.
- All `2^16` subwords of length 16 appear within the first 1M letters; about **63 subwords of length
  17 are still missing** at 1M.
- **Deviation from uniformity** decreases at a rate comparable to a random binary word — i.e. the
  word "looks normal" numerically, consistent with (but not a proof of) Conj 1.2.

---

## 7. Relevance to BB6 / Antihydra (why this paper matters to us)

- **Same map family.** `T_{3/2}(x) = ceil(3x/2)` is precisely the ceiling-`(3/2)` map at the heart
  of our `(5)` orbit Haar-genericity / Mahler-AEV obstruction in `PROOF_STATUS.md`. Conj 1.6 (mod
  `2^k` equidistribution of every orbit) is essentially the statement our skeleton reduction needs.
- **It is conjectural, not a theorem.** The thing our reduction bottoms out on (equidistribution mod
  `2^k` of `ceil(3/2)`-orbits) is, in the current literature, an **open conjecture (AEV Conj 1.6 =
  Conj 1.2 via Thm 1.7)**, itself strictly stronger-feeling than (and implying) Mahler's 53-year-old
  open Z-number conjecture. This pins down *why* handle (5) resisted all our soft/coupling/phase
  attacks: closing it unconditionally for 3/2 would imply Mahler — a hard open problem.
- **Collatz tie-in (relevant to Antihydra).** The paper explicitly draws "the *similarity* between
  the Collatz operator F and the operator T_{3/2}", and discusses the Dubickas–Mossinghoff "4/3
  problem" (Question 3.12) as the same Collatz-flavored family. This is the same complexity class our
  notes place Antihydra in (Collatz-type, IRREGULAR cryptid).

**Take-away for the proof program:** AEV converts our needed analytic input into a clean
combinatorial-normality *equivalent* and supplies strong numerics, but supplies **no unconditional
3/2 distribution theorem**. So any BB6 complete-proof route that depends on unconditional
equidistribution-mod-`2^k` of `ceil(3/2)`-orbits is, as of this paper, leaning on an open conjecture
that subsumes Mahler. Routes should either (i) target a *weaker* per-orbit invariant than full
equidistribution, or (ii) exploit the AEV equivalence to recast the needed input as a normality /
richness statement where partial combinatorial progress may be cheaper.
