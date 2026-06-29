# Can the Mauduit–Rivat carry lemma be extended to whole-history carry + closed-loop input? (2026-06-30)

*WEAPONS_AUDIT-style deep examination of the single sentence in `COMPLETE_PROOF_CAPSTONE.md`/`BB6_NO_STRUCTURE`:
the missing theorem is "exactly what the Mauduit–Rivat carry lemma does for BOUNDED carry and INDEPENDENT
input, extended to WHOLE-HISTORY carry and CLOSED-LOOP input." This file asks, with maximal concreteness:*
**what would that extension have to assert, where exactly does it break, is each break fundamental or
technical, do the 2019–2026 digit-method advances get closer, and is the MR-extension a real PATH or just
(K)/Mahler in disguise?** Builds on `ATTACK_MAUDUIT_RIVAT.md` (fit verdict = Mahler-equivalent) and
`DIGITS_OF_3N.md` (the object is the moving diagonal bit). Every line labelled. No proof claims. NOT committed.

---

## 0. One-paragraph verdict (up front)

The MR carry lemma is a **bounded-range, independent-input, average-over-detours** statement, and the
Antihydra target violates all three premises at once: the carry is **whole-history** (the `S_n` carry-sum,
the compounded `×3`), the input is **closed-loop** (the orbit feeds its own parity bits back via
`T_{n+1}=3T_n+2ⁿe_n`), and the object is the **moving middle digit**. Of the three required extensions, **(a)
unbounded carry** is *technical at the level of a single scale but fundamental once you sum scales*, because
**(b) the h-average collapse on the geometric ray** kills the saving at **every scale simultaneously**, and
**(c) the closed-loop input** is the **annealed→quenched gap**, which is fundamental and is *the same wall as
(K)*. The precise missing lemma — a power-saving, single-orbit ("quenched") bound on `Σ_{n<N} e(t·(3/2)ⁿ)` —
**is (K) itself** (= AEV Conj 1.6 / Mahler 3/2). So the MR-extension is **not an independent path**: it is
as-hard-as (K) directly. MR remains the right *language* (it names exactly which half — the multiplicative
`×3` — is the wall) but not a tool that closes it. `[OPEN]`. `[PROVEN-in-lit]` labels are attached only to the
published theorems cited.

---

## 1. The MR carry lemma, stated as the thing to be extended `[PROVEN-in-lit]`

From Mauduit–Rivat (Acta Math. 203, 2009; Ann. of Math. 171, 2010) and the DMRS exposition, the engine that
controls `Σ_{n≤x} e(α s(P(n)))` is:

1. **van der Corput differencing** (degree reduction): `P(n+r)−P(n)` has *lower degree* / *much smaller
   magnitude* than `P(n)`. `[PROVEN-in-lit]`
2. **Carry-propagation lemma (the object to extend).** *When a SMALL integer (`≈ μ+ρ` digits) is added to a
   LARGE integer (`≈ μ+ν` digits), the digits above index `λ := μ+2ρ` change ONLY by carry, and the number
   of summands whose carry reaches above `λ` is `O(q^{μ+ν−ρ})` — negligible.* Therefore `s` may be replaced
   by the **truncated, periodic detour** `s^{[μ,λ)}(n)=Σ_{μ≤j<λ} n_j`, of period `q^λ`. `[PROVEN-in-lit]`
3. **Discrete Fourier transform of the periodic detour** `F_λ(h)=q^{−λ}Σ_u e(α s_λ(u)−hu/q^λ)`; for `q=2`,
   `|F_λ(h)| = ∏_{i=1}^{λ} |cos π(α − h/2ⁱ)|`. `[PROVEN-in-lit]`
4. **The saving is an AVERAGE over the detour frequency `h`:** `Σ_{0≤h<q^λ} |F_λ(h)| = O(q^{η λ})` with
   `η < 1/2` (sub-square-root). `[PROVEN-in-lit]`

The lemma's three load-bearing premises (the things an Antihydra extension must drop):
- **(P1 bounded range)** the perturbation occupies `≪` digits, so carry reaches only `O(ρ)` positions and the
  truncation length `λ` is finite and *fixed*;
- **(P3 independent input)** `n` is a *free* variable on `[1,x]`; the type-II/Cauchy–Schwarz step averages
  over it;
- **(P4 genuine h-range)** step 4's saving is an *average* over many `h`, not a single value.

The "extended" lemma the spec asks for must hold when **(P1) fails (whole-history carry), (P3) fails
(closed-loop input), and the object is a single moving digit**. We take the three breaks in turn.

---

## 2. Obstruction (a): WHOLE-HISTORY carry — truncation to `λ` digits loses the tail

**What breaks.** The MR truncation `s ↦ s^{[μ,λ)}` is licensed *only* because the perturbation `mr` is
digit-localized (P1): carry from a small addend dies out within `O(ρ)` digits. The Antihydra step has **two**
operations, `T_{n+1}=3T_n+2ⁿe_n`:
- the **additive injection `+2ⁿe_n`** is a single localized digit — its carry *is* MR-bounded; `[PROVEN-in-lit
  applies verbatim]` the detour `s^{[μ,λ)}` controls it (`ATTACK_MAUDUIT_RIVAT.md §3`);
- the **multiplicative `×3`**, iterated, composes to the `3ⁿ` argument; `3^{n+r}−3ⁿ = 3ⁿ(3^r−1)` is the **same
  order of magnitude** as `3ⁿ` (measured ratio `→1.00` vs `→0.53` for `n²`, `ATTACK_MAUDUIT_RIVAT.md §4 STEP
  i`). The carry from `×3` is **whole-history**: it reaches across *all* `≈1.585n` digits. There is no finite
  `λ=μ+2ρ` that contains it; truncating at `λ` discards exactly the moving middle band (column `n−3`) where
  the target bit lives (`DIGITS_OF_3N.md §1,§3`).

**Could a multi-scale / renormalized MR recover it?** This is the sharpest form of the question. The natural
fix is to NOT fix `λ`, but **sum over scales**: write the saving as `Σ_{λ} (contribution of digit band at
scale λ)`, a renormalization-group / Littlewood–Paley decomposition of the digit axis. At a *single* scale
`λ`, treating the order-`λ` window as if the addend were localized there is **technically** defensible (this
is exactly what the cubes proof does — see §5, it opens a *window* where lower-degree behaviour survives and
detects it with a trig polynomial). **But the multi-scale sum does not save**, for the reason in §3: the
geometric ray pins the detour frequency to `h~(3/2)ʲ` at *every* scale, so each scale contributes the *same*
single-term (no per-scale `h`-average), and summing single terms gives no power saving. **Classification:
TECHNICAL at one scale, FUNDAMENTAL across scales** — the multi-scale escape is closed precisely by (b).

---

## 3. Obstruction (b): the h-AVERAGE COLLAPSES on the geometric ray (the decisive break)

**What breaks.** MR's entire *saving* (step 4) is the **average** `Σ_h |F_λ(h)| = 2^{ηλ}`, `η<1/2`. For a
polynomial `P`, vdC differencing linearizes the phase and the resulting detour frequency `h` **sweeps a full
range** `[0,qᵇ)` — there is something to average. For the **geometric** argument the differencing produces no
new degree; the relevant frequency is pinned to the **single resonant ray** `h~(3/2)ʲ`, and `F_λ` along it is
the **lacunary single product**

> `F_λ((3/2)ʲ) = ∏_{i=1}^{λ} |cos π(α − (3/2)ʲ/2ⁱ)|`   (= the `exp_sum.py` product).

Measured (`ATTACK_MAUDUIT_RIVAT.md §4 STEP iii`): the **averaged** bound exists (`η≈0.35–0.38<1/2` over
`L=6..14`) — MR's saving is real *in aggregate*; but the **single ray** is one term (`6.96e−22` at `λ=60`),
which *decays* yet is **not an average**, so it yields no sub-square-root *power* of `N`. A single decaying
term is the **annealed / Rajchman** statement (non-Pisot of `3/2` ⟹ `ν̂_{2/3}(t)→0`), the *already-provable
easy tier* (`COMPLETE_PROOF_CAPSTONE.md §6`; `NONPISOT_FOURIER_CHAIN` Link A/B).

**Why no h-range exists (root cause).** The `h`-range is *created* by degree reduction: a degree-`d`
polynomial linearizes after `d−1` vdC steps, and the intermediate frequencies fill `[0,qᵇ)`. A geometric
sequence has **no finite degree to lower** (it is the fixed point of `×θ`); differencing returns a constant
multiple, not a lower-degree object (`ATTACK_MAUDUIT_RIVAT.md §4 STEP ii-vdC`: differenced parity is WHITE for
`r=1..21`). With no degree, there is no linearization, hence no `h`-sweep, hence no average. **Classification:
FUNDAMENTAL.** This is the same structural wall as Mahler/AEV: the lacunary product `∏|cos π θ^j ·…|` carries
no *power* saving that the literature can extract for an individual `θ` (lacunary trigonometric products,
`arXiv:1502.06738`; lacunary Weyl sums have Gaussian fluctuations but **no per-realization power cancellation**
proved, `arXiv:2107.12860`, `arXiv:2310.20257`).

---

## 4. Obstruction (c): CLOSED-LOOP (non-independent) input — the annealed→quenched gap

**What breaks.** MR sums over `n` *free* on `[1,x]` (P3); the bilinear "type-II" decomposition needs `n`
independent to apply Cauchy–Schwarz and create the detour ensemble. Antihydra's input is **self-referential**:
`e_n = bit_n(8·3ⁿ)⊕bit_n(T_n)` and `T_{n+1}=3T_n+2ⁿe_n` — the orbit *generates its own* input bits. There is
**no free `n` to average over**; there is **one** deterministic orbit (`o₀=27`). MR produces an **annealed**
(ensemble-averaged, "for a.e. start / on average over `n`") conclusion; the Antihydra kernel needs a
**quenched** (single-realization) one. This is identical to:
- the `No-Structure` theorem class **(C3)**: Haar/Bernoulli ergodicity gives (K) for `μ`-a.e. orbit, but
  `{o₀}` is `μ`-null (`BB6_NO_STRUCTURE_THEOREM.md §3`); `[PROVEN]`;
- the capstone's **"broken link C"**: `ν̂_{2/3}` decay is annealed (i.i.d. weights), the orbit needs the
  quenched Weyl sum `Σ e(h·4·(3/2)ⁿ)` of the orbit itself (`COMPLETE_PROOF_CAPSTONE.md §6`). `[OPEN]`.

**Classification: FUNDAMENTAL.** Removing the free input removes the averaging that *is* the MR method; what
remains is exactly single-orbit equidistribution. (The recent automatic-sequence machinery — Müllner; BKM
Gowers — is also intrinsically an ensemble theory: it bounds correlations of `a(n)` over `n≤N`, never the
output of a closed feedback loop.)

---

## 5. Recent digit-method advances (2019–2026): how close do they get? `[PROVEN-in-lit]`

The frontier has moved, but **always along the polynomial-degree / numeration-system axis with free
independent input** — never toward geometric/lacunary `θⁿ`, never toward closed-loop input. Each advance
*confirms* the diagnosis (degree-reduction is the engine) rather than relaxing premise (P1)/(P3)/(P4).

| Advance | What it extends | Distance to the geometric/closed-loop target |
|---|---|---|
| **Mauduit–Rivat 2009/2010** (`s_q(n²)`, `s_q(p)`; Acta Math. 203; Ann. 171) | the base carry lemma, degree 2 + primes | baseline; needs P1+P3+P4 |
| **Drmota–Mauduit–Rivat / Müllner** *Normality along squares* (arXiv:1704.06472) | TM/automatic normal along `n²` | still degree 2, free input |
| **Spiegelhofer 2020** *Level of distribution of Thue–Morse* (Compositio 156; arXiv:1803.01689; arXiv:2504.02784) | level of distribution **= 1** for TM | sharpest equidistribution-in-AP for a *digit* function — still a fixed/free-`n` object, not a moving digit of `θⁿ` |
| **Spiegelhofer 2023** *Thue–Morse along cubes* (arXiv:2308.09498) | **degree 3**: `density{t(n³)=0}=1/2`, via **iterated vdC + carry lemma**, opening a *window* where quadratic behaviour survives and detecting it with a trig polynomial | **CLOSEST in spirit** to a multi-scale carry lemma — it *does* sum/iterate vdC and localize a digit *window*. But it reaches degree 3 *at great cost, one degree at a time*; `θⁿ` is "degree ∞" — outside any finite iteration. **Confirms** §2: multi-scale works only where a finite degree remains to lower |
| **Konieczny 2019** (AIF 69; arXiv:1611.09985); **Byszewski–Konieczny–Müllner** *Gowers norms for automatic sequences* (Discrete Analysis 2023; arXiv:2002.09509) | `U^k`-uniformity of *every* automatic sequence orthogonal to periodic | gives uniformity along **all polynomial patterns** for automatic seqs; `3ⁿ`-digit object is **not automatic** in `n` (it is the digit of a *growing* number), and the input is free, not closed-loop |
| **Toumi 2025** | generalizes level-of-distribution + Gowers results to `s_q` in **any base** | widens base, not argument type |
| **Jelinek 2025** *Gowers norms for linearly recurrent numeration systems* (arXiv:2510.16947) | Gowers framework to **non-standard (linearly recurrent) numeration systems** | changes the *numeration system*, still polynomial/automatic input |
| **Spiegelhofer–Wallner 2025** *joint binary/ternary digit sums* (arXiv:2501.00850, Lemma 4.1, Schlickewei subspace thm) | **unconditional** longest-run `L(M·3ᴷ) ≤ ηK+o(K)` — applies verbatim to `8·3ⁿ` | the **only** recent unconditional fact touching `M·3ᴷ`, but it is a *run-length* (horizontal), giving only two-sided density `≥1/o(n)→0`; **no positive density at the moving diagonal** (`DIGITS_OF_3N.md §2.4`) |

**Net of §5.** The community's reach now includes degree-3 polynomials (cubes), arbitrary bases (Toumi), and
non-standard numeration (Jelinek), and the *sharpest* equidistribution (level 1, TM). **None** drops the
finite-degree (P1) or free-input (P3) premise. The cubes paper is the nearest thing to the "multi-scale carry
lemma" the extension would need — and it shows the cost grows steeply with degree and **requires a residual
finite degree to detect in the window**, which `θⁿ` does not provide. The subspace-theorem run bound is the
nearest *unconditional* `3ⁿ` fact and provably stalls at vanishing density. **Distance to target: not closed
by any of them; all are on the wrong side of the polynomial/geometric divide.**

---

## 6. The precise missing lemma (the "whole-history-carry, closed-loop-input carry lemma")

Spelling out what an MR-extension would have to *assert*, and reducing it:

> **Wanted (the extended carry lemma).** There exist `θ_0<1/2` and an effective constant such that for the
> single Antihydra orbit (closed-loop input), the quenched, multi-scale digit sum satisfies a **power saving**
> `|Σ_{n<N} (−1)^{e_n}| ≤ C·N^{1−δ}` (some `δ>0`), obtained by (i) a renormalized sum over digit scales `λ`
> replacing the fixed truncation, (ii) a per-scale saving that survives the collapse of the `h`-average to the
> single ray `h~(3/2)ʲ`, and (iii) validity for the self-generated input sequence, not an average over free `n`.

Each of (i),(ii),(iii) reduces, on inspection, to the **same** object:
- (i) multi-scale carry ⇒ needs a per-scale power saving from the **single lacunary product**
  `∏_i|cos π(α−(3/2)ʲ/2ⁱ)|` — but §3 shows there is **no `h`-average** at any scale, so the only available
  bound is the single-term decay = **annealed Rajchman**, not a power of `N`;
- (ii),(iii) ⇒ an **effective, power-rate, quenched** statement about `(3/2)ⁿ mod 1`.

Therefore the missing lemma **collapses to one concrete analytic statement**:

> **THE EXACT TECHNICAL LEMMA needed (exogenous part).** `[OPEN]` A **power-saving bound on the single-orbit
> (quenched) Weyl sum** of the actual orbit:
> > `|Σ_{n<N} e(t·4·(3/2)ⁿ)| = o(N)` (ideally `≤ C·N^{1−δ}`), **uniformly for the relevant `t`**, for the
> > specific orbit `o₀=27` — equivalently, transfer of an **effective power Fourier decay**
> > `|ν̂_{2/3}(t)| ≤ C|t|^{−a}` of the Bernoulli convolution `ν_{2/3}` (annealed) to the **single orbit**
> > (quenched).
>
> This is **exactly** the kernel (K): the one-sided single-orbit equidistribution of `{(3/2)ⁿ}`-type =
> floor-mirror, level-2 fragment of **AEV Conj 1.6** (arXiv:2510.11723) ⟹ **Mahler 1968 3/2**
> (`COMPLETE_PROOF_CAPSTONE.md §6`). Candidate analytic inputs for the *annealed* half exist (effective
> Bernoulli-convolution decay: Streck, Varjú–Yu, Brémont, Bourgain–Dyatlov); **the annealed→quenched transfer
> is the broken link and is itself (K)**.

So the "extended carry lemma" is not a *new* lemma sitting *below* (K) that one could prove first and then
deduce (K): proving it **is** proving (K). MR gives no leverage on the transfer because its leverage *is* the
free-input average it no longer has.

---

## 7. Honest assessment — path or as-hard-as-(K)?

- **Is the MR-extension a plausible independent PATH (with a clearly-stated missing lemma below (K))?** **No.**
  The missing lemma (§6) is **(K) itself**, on all three axes: the unbounded-carry fix needs a per-scale power
  saving that does not exist without the `h`-average (§3); the `h`-average cannot be recreated for a geometric
  argument (no degree to linearize); and the closed-loop input removes the very ensemble that MR averages
  over, leaving the quenched single-orbit statement (§4). There is **no sub-lemma strictly weaker than (K)**
  whose proof would supply the saving.
- **Is it as-hard-as (K) directly?** **Yes**, with a precise reason: the three breaks are not independent
  difficulties to be patched one by one — they **funnel into the single quenched-Weyl-sum / quenched-Fourier
  statement**, which is (K) = AEV/Mahler. This is fully consistent with the two `No-Structure` meta-theorems:
  MR is a *finite-window / free-ensemble* tool (it lives in registers R1 annealed and R2 all-orbits/free), and
  those registers are **proven** unable to reach the tail-average that distinguishes halting from non-halting
  (`BB6_NO_STRUCTURE_THEOREM.md §3`, (C2)/(C3); `COMPLETE_PROOF_CAPSTONE.md §5`).
- **What MR genuinely contributes (not nothing).** It is the **correct language** and a **precise localizer**:
  it proves the additive injection `+2ⁿe_n` is MR-tame (detour `s^{[μ,λ)}`) and pins the wall to the
  **multiplicative `×3`** = the Mahler map (`ATTACK_MAUDUIT_RIVAT.md §3`); and it identifies the exact missing
  ingredient (a quenched power Fourier rate) rather than a vague "it's hard." That diagnostic value is real;
  the *closure* value is nil.

**Bottom line.** The spec's framing is accurate as a *description* of the gap (whole-history carry + closed-loop
input vs MR's bounded carry + independent input) but **misleading as a roadmap**: the "extension" is not a
detour around (K); the three premises (P1,P3,P4) each fail in a way that re-expresses (K). The exogenous part
cracks **iff** someone proves the quenched, power-rate Weyl-sum/Fourier statement of §6 — i.e. iff the AEV/Mahler
line moves. Far in calendar time; the path is already the shortest known (one open point).

---

## Sources

**Repo (cross-refs):** `ATTACK_MAUDUIT_RIVAT.md` (fit verdict, numerics STEP i–iii), `DIGITS_OF_3N.md`
(moving-diagonal object, run bound), `COMPLETE_PROOF_CAPSTONE.md §6` (kernel (K), annealed/quenched broken
link C), `BB6_NO_STRUCTURE_THEOREM.md §2–3` (C1/C2/C3 structural-register no-go), `NONPISOT_FOURIER_CHAIN`
(Rajchman links A/B/C).

**Literature `[PROVEN-in-lit]` / `[OPEN]` as labelled:**
- Mauduit, Rivat, *La somme des chiffres des carrés*, Acta Math. 203 (2009) 107–148.
- Mauduit, Rivat, *Sur un problème de Gelfond: la somme des chiffres des nombres premiers*, Ann. of Math. 171 (2010) 1591–1646.
- Drmota, Mauduit, Rivat; Müllner, *The Rudin–Shapiro sequence … normal along squares*, arXiv:1704.06472; *Normality along squares*.
- Spiegelhofer, *The level of distribution of the Thue–Morse sequence*, Compositio Math. 156 (2020); arXiv:1803.01689; arXiv:2504.02784.
- Spiegelhofer, *Thue–Morse along the sequence of cubes*, arXiv:2308.09498 (2023) — iterated vdC + carry lemma, degree 3.
- Konieczny, *Gowers norms for the Thue–Morse and Rudin–Shapiro sequences*, Ann. Inst. Fourier 69 (2019); arXiv:1611.09985.
- Byszewski, Konieczny, Müllner, *Gowers norms for automatic sequences*, Discrete Analysis (2023); arXiv:2002.09509.
- Toumi (2025) — level of distribution / Gowers for `s_q` in arbitrary base (via Spiegelhofer program).
- Jelinek, *Gowers norms for linearly recurrent numeration systems*, arXiv:2510.16947 (2025).
- Spiegelhofer, Wallner et al., *The joint distribution of binary and ternary digit sums*, arXiv:2501.00850 (2025), Lemma 4.1 (Schlickewei subspace theorem, longest-run bound).
- Andrieu, Eliahou, Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (2025) — Conj. 1.6 / Thm 1.5,1.7.
- Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. 8 (1968).
- Lacunary context: *On parametric Thue–Morse sequences and lacunary trigonometric products*, arXiv:1502.06738; *The large deviation behavior of lacunary sums*, arXiv:2107.12860; *Diophantine conditions in the LIL for lacunary systems*, arXiv:2310.20257.
- Bernoulli-convolution decay (annealed candidates): Streck; Varjú–Yu; Brémont; Bourgain–Dyatlov (as catalogued in `COMPLETE_PROOF_CAPSTONE.md §6`).

No machine decided. No label upgraded.
