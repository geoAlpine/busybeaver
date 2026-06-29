# Entropy of the Antihydra limit measure — the make-or-break crux, settled in DIRECTION (2026-06-29)

*Decisive audit of whether the empirical limit measure `μ` of the single `⟨3/2⟩`-orbit on the `(2,3)`-solenoid
`X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` has ZERO measure-theoretic entropy — the hypothesis on which framework (I)
(`NEWMATH_SYNTHESIS`, `NEWMATH_ADELIC_RIGIDITY`) turns. SOUNDNESS PARAMOUNT: every claim labelled
[PROVEN]/[PROVEN-in-lit]/[OBSERVED]/[OPEN]; zero false proofs; the kernel (K) is NOT proven and NO label is
upgraded. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact big-int, N=10⁵, <1s
(`scratchpad/entropy_probe.py`). NOT committed.*

---

## 0. One-line verdict

**The limit measure is NOT provably zero-entropy — and it CANNOT be, because zero entropy is *equivalent to
disproving* (K).** The candidate "linear complexity ⟹ topological entropy 0 ⟹ variational principle ⟹ measure
entropy 0" argument is **INVALID** (it misuses a lower bound as an upper bound, and the orbit's complexity is in
fact full, `2^ℓ`). The correct statement reverses the program's hedge: **(K) ⟺ `μ`=Haar ⟹ `μ` has POSITIVE
entropy** (`h_Haar(M₂)=log2`, `h_Haar(A)=log3`). So Rudolph–Johnson's positive-entropy hypothesis is *satisfied
under (K)*, not violated; the route is **not killed by zero entropy**. What blocks it is the pair {host-invariance
(AIU) + positive entropy}, and **positive entropy is itself (K)-hard / [OPEN]** — necessary for (K), not provably
present, and provably-zero would *refute* (K). The honest target sharpens to **prove `h_μ(M₂)>0`** (then AIU + the
PROVEN Rudolph–Johnson ⟹ (K)); the zero-entropy regime is the **(K)-false** regime, not a Furstenberg corner that
proves (K).

---

## 1. The candidate zero-entropy argument is INVALID [PROVEN — soundness correction]

`NEWMATH_SYNTHESIS` §2 (lines 67–69) hedges: *"the orbit's subword complexity is only linear, `p(ℓ)≥1.71ℓ`,
topological entropy 0 … so RJ is inapplicable."* This is a genuine error, in three independent ways:

1. **A lower bound is not an upper bound.** `LIMIT_THEOREM` §3″ proves `p(ℓ) ≥ (ℓ−3)/log₂(3/2) ≈ 1.71ℓ` — a
   **lower** bound. Topological entropy `h_top = lim (1/ℓ)log p(ℓ) = 0` requires a **sub-exponential UPPER** bound
   `p(ℓ)=2^{o(ℓ)}`. `p(ℓ)≥1.71ℓ` is logically consistent with `h_top=0` AND with `h_top=log2`; it decides nothing.
   [PROVEN]
2. **The actual complexity is FULL, `h_top=log2>0`.** The same note (§3″, and re-verified here) proves the coding
   bijection `p(ℓ)=#{c_n mod 2^ℓ}` and *measures* `p(ℓ)=2^ℓ` to ℓ=16. The orbit-closure subshift therefore has
   **positive topological entropy `log2`** — exactly the regime where the variational principle gives **no** upper
   bound on any measure's entropy. The premise "topological entropy 0" is **contradicted by the data**. [PROVEN that
   the proposed premise fails; the exact value `h_top=log2` is [OBSERVED]/(K)-equivalent.]
3. **Even granting `h_top=0`, the conclusion would be self-defeating.** The variational principle
   `h_top=sup_ν h_ν` only *upper*-bounds measure entropy when `h_top=0`. But proving `h_μ=0` is **not what the
   program wants** — see §2.

> **Correct chain.** `h_μ(M₂) ≤ h_top(orbit-closure under ×2)`; here the RHS is `log2`, so the bound is vacuous.
> Measure entropy is the exponential growth rate of the **frequency-weighted** cell count
> `h_μ(M₂)=lim_ℓ (1/ℓ) Σ_a −f_ℓ(a)log f_ℓ(a)` (`f_ℓ(a)=` asymptotic frequency of `c_n≡a mod 2^ℓ`), NOT of the raw
> count `p(ℓ)`. The variational principle never sees the frequencies, so it cannot deliver `h_μ=0` here. [PROVEN]

---

## 2. The entropy of `μ` is (K)-equivalent in direction: zero entropy ⟺ (K) FALSE [PROVEN]

The three entropies the task asks to link:

- **(i) subshift (topological) entropy** of the parity/digit sequence: `h_top = lim(1/ℓ)log p(ℓ)`. Proven lower
  part only (`p(ℓ)≥1.71ℓ`); observed full (`=2^ℓ`); `h_top=log2 ⟺` maximal complexity `⟺` (K) (`LIMIT_THEOREM`
  §3″). Governs the *sup* over invariant measures, **not** `μ` itself.
- **(ii) `h_μ(M₂)`** (entropy under the host element `×2`): the entropy Rudolph–Johnson actually needs. On the
  solenoid `h_·(×u)=Σ_v log⁺|u|_v`, so for Haar `h_Haar(M₂)=log⁺|2|_∞=log2 > 0`. [PROVEN-in-lit, Lind–Schmidt–Ward
  / Yuzvinskii entropy formula]
- **(iii) `h_μ(A)`** (entropy under the iterated map `A=×(3/2)`): for Haar `h_Haar(A)=log⁺|3/2|_∞+log⁺|3/2|_2
  =log(3/2)+log2=log3 > 0`. The **bit/2-adic information** (the (K) object) lives in the `ℚ₂`-factor, which `A`
  EXPANDS (`|3/2|_2=2`) and `×2` CONTRACTS — so the (K)-relevant entropy is carried by `h_μ(A)` via `ℚ₂`, while
  RJ reads it off the archimedean place of `M₂`; on a host-invariant ergodic measure these vanish together.
  [PROVEN-in-lit]

> **Key dichotomy [PROVEN].** Haar is the unique (K) target and has **positive** entropy under every nontrivial
> host element and under `A`. Hence:
> ```
>   h_μ(M₂)=0  ⟹  μ ≠ Haar  ⟹  c_n mod 2^k NOT equidistributed  ⟹  (K) FALSE.
> ```
> Therefore **`h_μ=0` is not provable** without simultaneously *refuting* (K)/equidistribution (a generational
> result, numerically refuted — §4). Conversely **`h_μ(M₂)>0` is a NECESSARY condition for (K)**, is [OPEN], and is
> no easier than the partial-complexity question.

**Single-orbit-ness gives nothing.** Empirical limits of one orbit can have full entropy: a base-2 normal number's
shift-orbit has empirical measure Bernoulli(½), entropy `log2`. (Indeed *(K) itself asserts seed 8 is such a
"normal" orbit.*) So there is **no** single-orbit theorem forcing `h_μ=0`. [PROVEN — counterexample]

**Net.** The program's "zero-entropy catch" had the sign backwards. The make-or-break entropy fact is settled in
*direction*: not zero, can't be zero without killing (K); the open content is whether it is *positive* (≈(K)).

---

## 3. Consequence for framework (I): Rudolph–Johnson is NOT dead; the correct two-hypothesis reduction [PROVEN reduction structure]

Let `μ` be any weak-* limit of the orbit's empirical measures. Proven input: `μ` is `A`-invariant
[PROVEN, Krylov–Bogolyubov]. **[SOUNDNESS CORRECTION 2026-06-29, `ENT_NONATOMIC.md`]** An earlier version asserted `μ`
**non-atomic [PROVEN]** "via 2-adic repulsion" — that is an **over-claim, retracted.** What is [PROVEN] is only that the
*orbit avoids periodic points per-visit* (growth + non-periodicity + countdown); since an `A`-invariant measure's atoms
sit on periodic orbits, `μ` non-atomic ⟺ `μ` charges no periodic point ⟺ `sup_a μ₂(a+2^kℤ₂)→0` (vanishing occupancy),
which is **[OPEN]** (one run of length ≈0.585N is permitted by the proven budgets; vanishing occupancy = single-orbit
genericity = (K)-hard). So `{orbit avoids periodic}[PROVEN] ⊊ {μ non-atomic}[OPEN] ⊊ (K)`. Then the **entropy is the fork
between a PROVEN finish and an OPEN one**:

| if we also had … | the finishing theorem | status of theorem |
|---|---|---|
| **AIU** (host `⟨×2,×3⟩`-invariance) **+** `h_μ(M₂)>0` | **Rudolph 1990 / Johnson** ⟹ `μ`=Haar ⟹ (K) | **[PROVEN-in-lit]** |
| **AIU + non-atomicity[OPEN] +** Furstenberg's conjecture | non-atomic ergodic `⟨×2,×3⟩`-inv ⟹ Haar | **[OPEN]** (Furstenberg; + non-atomicity now open) |

- **Positive-entropy branch [the live, correctly-stated target] — UNAFFECTED by the correction.** The gap to using the
  **proven** Rudolph–Johnson is {AIU, `h_μ(M₂)>0`}. Note `h_μ(M₂)>0 ⟹ μ` non-atomic automatically, so this branch does
  **not** rely on the retracted non-atomicity claim. The "modulo positive entropy" hedge is removed by **proving positive
  entropy** (a necessary consequence of (K) that, combined with AIU, lets PROVEN RJ finish).
- **Furstenberg branch.** Furstenberg's conjecture: the only ergodic `⟨×2,×3⟩`-invariant measures are Haar and the atomic
  (finite-orbit) ones. So **AIU + non-atomicity + Furstenberg ⟹ μ=Haar ⟹ (K)** with no entropy hypothesis — but now
  **non-atomicity is itself [OPEN]** (corrected above), so this branch needs THREE open inputs (AIU, non-atomicity,
  Furstenberg), not two. The live route remains the positive-entropy branch via the proven RJ.

> **Honest placement.** (K) follows from `AIU ∧ (h_μ(M₂)>0 ∨ Furstenberg)`. Entropy is exactly the **RJ-vs-Furstenberg
> selector**: positive 2-adic entropy buys the *proven* Rudolph–Johnson; its absence forces the *open* Furstenberg.
> So framework (I) is best read as: **(K) reduces to AIU + positive-2-adic-entropy**, both [OPEN], with positive
> entropy a *necessary* (hence not-strictly-easier) sub-fact of (K). The "Furstenberg zero-entropy corner" framing
> of `NEWMATH_SYNTHESIS` §0/§4 is **misleading** and is corrected here: the zero-entropy regime is the (K)-FALSE
> regime, not a corner from which (K) is proved.

---

## 4. Numerics — `μ` looks FULL-entropy (corroborates "not zero"; consistent with Haar) [OBSERVED]

`scratchpad/entropy_probe.py`, exact big-int, `c_{n+1}=c+⌊c/2⌋`, `c₀=8`, `N=10⁵`, residues mod `2^k`, empirical
Shannon entropy `H_k` (bits), per-bit increment `h_k=H_k−H_{k−1}`:

```
 k  distinct  2^k     H_k(bits)  h_k    distinct/full
 8      256      256    7.9981   0.9991   1.0000
10     1024     1024    9.9924   0.9963   1.0000
12     4096     4096   11.9700   0.9850   1.0000
13     8192     8192   12.9391   0.9691   1.0000     <- last fully-resolvable level
14    16356    16384   13.8756   0.9365   0.9983
16    51205    65536   15.4499   0.7114   0.7813
18    83067   262144   16.2544   0.3046   0.3169
```
- **`h_k ≈ 1 bit = log2` per bit** through every level the sample size resolves: the per-bit (conditional) entropy
  shows **no deficit** — the signature of FULL / positive entropy (2-adic dimension 1), the *opposite* of zero.
- The rolloff for `k≥14` is a **pure finite-sample artifact**, not an entropy deficit: for `N` uniform draws over
  `2^k` cells the expected fill is `1−e^{−N/2^k}`. Predicted vs observed:
  `k=16: 0.7826 vs 0.7813`, `k=17: 0.5337 vs 0.5334`, `k=18: 0.3171 vs 0.3169` — **agreement to ≤0.2%**. The orbit's
  residue distribution mod `2^k` is **statistically indistinguishable from exactly uniform (Haar) sampling** at
  every level. [OBSERVED] This corroborates `h_μ(M₂)=log2>0` (and `μ=`Haar / (K)); it is **not** a proof — it is the
  same equidistribution evidence the program already has, now read on the entropy axis.
- **Dimension.** Full per-bit entropy `⟹` (empirically) 2-adic local dimension of `μ₂` `=1` (`μ₂`= Haar on `ℤ₂`),
  i.e. no fractal/atomic concentration — consistent with the PROVEN non-Pisot no-atom spectrum
  (`NEWMATH_DIAGONAL_RENORM` §3.2). [OBSERVED + PROVEN no-atom]

---

## 5. Which conditional rigidity result is nearest, and the exact missing hypothesis [PROVEN-in-lit hypotheses]

| result | what it gives | EXACT missing hypothesis here |
|---|---|---|
| **Rudolph 1990 / Johnson 1992** (solenoid form, arXiv:2101.11120) | pos-entropy ergodic `⟨×2,×3⟩`-inv ⟹ Haar | **(1) `⟨×2,×3⟩`-invariance (AIU)** [OPEN]; **(2) `h_μ(M₂)>0`** [OPEN, (K)-necessary]. *Nearest — and PROVEN.* |
| **Host 1995** (`×p`-normality from `×q`-ergodicity) | a.e. point `×q`-normal | needs `h_μ>0` **and** ergodicity under a *second* multiplicatively-independent map — same two gaps |
| **Lindenstrauss 2006 / Einsiedler–Katok–Lindenstrauss** | low-entropy + extra invariance ⟹ rigidity | designed for **positive-entropy** + higher-rank diagonal; we have neither extra invariance nor proven positivity |
| **Furstenberg conjecture** (open) | ergodic `×2,×3`-inv ⟹ Haar or finite | needs **AIU + non-atomicity** (the latter [OPEN], §3); the theorem itself is also **[OPEN]** |
| **Hochman–Shmerkin 2012 / Shmerkin 2014 / Wu 2019 / Shmerkin–Wu** | dimension/`L^q`, `×2,×3`-measures, some without pos-entropy | all assume invariance under a **single** host map (`×2` or `×3`) and self-similar/CP structure; our `μ` is a priori only **`A`-invariant** — missing the single-host invariance (a weak form of AIU) |
| **BFLM / BLMV** | individual-orbit equidistribution | needs **non-abelian** acting semigroup with **spectral gap**; ours is abelian, no gap — *not applicable* (already in `NEWMATH_ADELIC_RIGIDITY` §5) |

**Sharpest reading.** The nearest *proven* theorem is **Rudolph–Johnson**, missing exactly **two** hypotheses:
host-invariance (AIU) and `h_μ(M₂)>0`. The nearest theorem needing *only* AIU is **Furstenberg's conjecture**, but
that one is open. There is **no** conditional result in the literature that closes (K) from `A`-invariance +
non-atomicity alone — confirming `NEWMATH_ADELIC_RIGIDITY` §5's novelty claim, now sharpened: the missing input is
not "a second direction" generically but specifically **{AIU} ∪ {positive 2-adic entropy *or* Furstenberg}**.

---

## 6. Honest ledger

| item | label |
|---|---|
| "`p(ℓ)≥1.71ℓ ⟹ h_top=0 ⟹ h_μ=0`" (the candidate argument) | **[DISPROVEN as an argument]** — lower bound misused; `h_top=log2` observed |
| `h_μ(M₂) ≤ h_top` (variational direction); vacuous here since `h_top=log2` | [PROVEN] |
| Haar has positive entropy: `h_Haar(M₂)=log2`, `h_Haar(A)=log3` | [PROVEN-in-lit] |
| `h_μ(M₂)=0 ⟹ μ≠Haar ⟹ (K) false` (so zero entropy not provable w/o refuting (K)) | **[PROVEN]** |
| `h_μ(M₂)>0` is NECESSARY for (K), [OPEN], (K)-hard | [PROVEN that necessary; positivity OPEN] |
| `μ` non-atomic | **[OPEN]** — orbit avoids periodic points per-visit [PROVEN], but `μ` charging them zero mass (vanishing occupancy) is open, §3; CORRECTED from an earlier "[PROVEN]" over-claim (`ENT_NONATOMIC.md`) |
| AIU + `h_μ(M₂)>0` + RJ ⟹ (K) | [PROVEN reduction, modulo the two OPEN inputs]; note `h_μ>0 ⟹` non-atomic, so this MAIN branch needs no separate non-atomicity |
| AIU + non-atomicity + Furstenberg ⟹ (K) (no entropy needed) | [PROVEN reduction, modulo THREE OPEN inputs: AIU, non-atomicity, Furstenberg] |
| Empirical `h_k≈log2` per bit; residues mod `2^k` ≡ uniform-sampling to ≤0.2% | [OBSERVED] (consistent with full entropy/Haar; not a proof) |
| (K) itself | **[OPEN]** = Mahler 3/2 / AEV Conj 1.6 at α=8 |

**Make-or-break disposition.** The entropy crux is *settled in direction and corrected*: the limit measure is **not
zero-entropy** (that would refute (K), and the data shows full per-bit entropy). Rudolph–Johnson is therefore **not
killed by zero entropy**; the program's hedge is reversed. The live, correctly-stated sub-targets are **(a) AIU**
and **(b) `h_μ(M₂)>0`** (positive 2-adic entropy), the latter a necessary, (K)-hard consequence of (K). Since
`h_μ(M₂)>0 ⟹ μ` non-atomic, this main branch invokes the **proven** Rudolph–Johnson without needing a separate
non-atomicity input (μ non-atomicity is itself [OPEN], §3). The zero-entropy/Furstenberg "corner" is a misframing — it is
the (K)-false regime.

---

## Sources
- Rudolph, *×2 ×3 invariant measures and entropy*, ETDS (1990); Johnson, *Measures on the circle invariant under
  multiplication by a non-lacunary subsemigroup* (1992). [PROVEN-in-lit]
- *Rigidity properties for commuting automorphisms on tori and solenoids*, arXiv:2101.11120 (solenoid RJ form).
  [PROVEN-in-lit]
- Furstenberg, *Disjointness in ergodic theory…* (1967) — the `×2,×3` conjecture. [OPEN]
- Host, *Nombres normaux, entropie, translations*, Israel J. Math. (1995). [PROVEN-in-lit]
- Lindenstrauss, *Invariant measures and arithmetic QUE*, Ann. Math. (2006); Einsiedler–Katok–Lindenstrauss,
  *Invariant measures and the set of exceptions to Littlewood* (2006). [PROVEN-in-lit]
- Hochman–Shmerkin (Ann. Math. 2012); Shmerkin (2014); Wu (Ann. Math. 2019); Shmerkin–Wu — `×2,×3`-measure
  projections/dimensions. [PROVEN-in-lit]
- Lind–Schmidt–Ward, entropy of solenoid/`ℤ^d` automorphisms (`h(×u)=Σ_v log⁺|u|_v`). [PROVEN-in-lit]
- Repo: `NEWMATH_SYNTHESIS.md`, `NEWMATH_ADELIC_RIGIDITY.md`, `NEWMATH_DIAGONAL_RENORM.md`, `LIMIT_THEOREM.md` §3″
  (subword complexity floor + coding bijection), `SESSION_2026-06-29_AEV_CORE.md`, `REPELLER_ESCAPE.md`,
  `WEAPONS_AUDIT_2026-06-29.md`.
- Numerics: `scratchpad/entropy_probe.py` (exact big-int, N=10⁵, <1s): `h_k≈log2` per bit through k=13;
  distinct/full matches uniform-sampling `1−e^{−N/2^k}` to ≤0.2% at k=16,17,18.

No machine decided. No label upgraded.
