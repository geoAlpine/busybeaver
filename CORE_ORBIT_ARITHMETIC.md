# The orbit arithmetic that would solve (K) — deepest examination (2026-06-30)

*Not a tool-survey (those are exhausted): a deep examination of the **actual arithmetic content** a proof of the
generational core `(K)` = Mahler 3/2 / AEV must exploit, and the most plausible SHAPE of such a proof. Synthesizes four
deep probes: the exogenous digits-of-3ⁿ frontier (`CORE_DIGITS3N_FRONTIER.md`), the self-referential carry as
obstacle/lever (`CORE_CARRY_LEVER.md`), the Mauduit–Rivat carry-lemma extension (`CORE_MR_EXTENSION.md`), and the
specified-point methods' extra input (`CORE_SPECIFIED_POINT_INPUT.md`). SOUNDNESS: no proof claims; (K) is [OPEN]; one
citation correction banked (§5). NOT committed by default.*

---

## 0. One-line synthesis

Every concrete path to `(K)` — extending Mauduit–Rivat's carry lemma, supplying a Bailey–Crandall finite-group model,
or closing the self-referential bootstrap — funnels to **one** arithmetic statement: **effective single-orbit (quenched)
equidistribution of the depth sequence `D_n = v₂(3c_n−1)`** (equivalently the quenched Weyl sum
`(1/N)Σ_{n<N} e(t·(3/2)ⁿ) = o(1)` = annealed→quenched transfer of the Bernoulli-convolution `ν̂_{2/3}` decay). **No
sub-statement strictly below `(K)` supplies the needed saving.** The one route the proven no-gos do **not** pre-empt is a
**Kac-type return-time / Lyapunov sub-action on the proven 2-adic potential `V=v₂(c−1)`** — not a spectral contraction
(forbidden by the L_ann odd-blindness no-go) and not structure-only (forbidden by the No-Structure theorem), but a
**quenched excursion argument** whose decrease must live in the *conditional return-time law*, not a per-step drift (the
per-step feedback is provably white). Whether that argument can be made non-circular (the return-time law *is* the
D-statistics) is the generational frontier.

---

## 1. The exogenous core: moving diagonal of 3ⁿ (`CORE_DIGITS3N_FRONTIER`)

`(K)` splits [PROVEN] as `β_n = bit_{n+k}(8·3ⁿ − S_n)`; the exogenous part is `d_n = bit_{n+k}(8·3ⁿ)` = the binary digits
of `3ⁿ` on a **moving diagonal** (index-dependent position ~0.63·(bit-length)).
- **Nothing unconditional touches a moving digit position of 3ⁿ.** Every proven positive-density fact is at a **fixed**
  position (Benford leading band, Weyl; Rowland column-periodicity `2^{j−2}`, which provably misses the diagonal); every
  moving/global fact is a sublinear count (`nonzero digits = Θ(log n/log log n)`) or a vanishing-density run bound. Even a
  single one-sided `freq{d_n=0} ≤ 1−c`, `c>0`, is beyond the frontier.
- **AEV (arXiv:2510.11723) prove no unconditional 3/2 distribution fact** — Thm 1.5/1.7 are *equivalences* (normality
  ⟺ equidistribution-mod-`q^k`; normality ⟹ no `Z_{p/q}`-numbers for `p<q²`). They **reframe** the wall; `(K)` = their
  Conj 1.6 at α=8.
- **Missing exogenous input:** cancellation in the single lacunary geometric sum `(1/N)Σ e(h·8·(3/2)ⁿ/2^{k+3}) = o(1)`,
  i.e. a power-saving on the *quenched* Weyl sum.

## 2. The Mauduit–Rivat carry lemma: three breaks, one funnel (`CORE_MR_EXTENSION`)

The No-Structure spec named the missing theorem "MR's carry lemma extended to whole-history carry and closed-loop input."
The three breaks:
- **(a) whole-history carry** (`×3` gives `3ⁿ(3ʳ−1)`, same order as `3ⁿ`; truncation discards the moving middle bit) —
  *technical at one scale, fundamental across scales* (the multi-scale escape is killed by (b)).
- **(b) h-average collapse on the geometric ray** — MR's saving `Σ_h|F_λ(h)|=2^{ηλ}` (η<½) is an average over the detour
  frequency `h`; a geometric sequence has no finite degree to linearize, so `h` is pinned to the single ray `h~(3/2)ʲ`,
  leaving the lone lacunary product = the annealed Rajchman fact. **FUNDAMENTAL.**
- **(c) closed-loop input** — MR averages over free `n`; here the bits are self-generated. **FUNDAMENTAL** (= the
  annealed→quenched gap = No-Structure (C3)).
All three funnel to the **quenched Weyl-sum power-saving = (K)**. MR's value is *diagnostic*: the additive injection
`+2ⁿe_n` is MR-tame; the wall is the multiplicative `×3`. Recent advances (Spiegelhofer *cubes* arXiv:2308.09498, closest
in spirit; BKM/Konieczny Gowers; Jelinek numeration) move the polynomial-degree/numeration axes with **free** input, never
the geometric/closed-loop axis.

## 3. The self-referential carry: a lever on the wrong subspace (`CORE_CARRY_LEVER`)

The carry `S_{n+1}=3S_n+2ⁿb_n` (`b_n` the orbit's own parity) is what makes Antihydra *not* pure Erdős/Mahler.
- **It self-corrects DENSITY but is blind to the COUPLING.** [OBSERVED+structural] the renewal map pulls a biased fed-back
  bit back to ½ on the *even-character* channel (a genuine self-correcting contraction — but density was never in danger);
  on the *odd-character* channel `V_odd` where `(K)` lives, the feedback is **white noise** (autocorr ≤0.006 all lags;
  `I(β;state)=3·10⁻⁵` bits) and the contraction is provably **blind** (L_ann annihilates odd characters). *Obstacle-leaning.*
- **Discipline catch:** a tempting block mean-reversion signal (−0.14) was killed by a shuffle control (−0.06±0.12, <1σ) —
  artifact, rejected (the §13/§14 unfaithful-model trap avoided).
- **Where the bootstrap fails:** §12's conditional theorem assumes `bit_k ⊥ low-state` (= (K), circular); the scale `k→k+1`
  bootstrap regresses infinitely (the gap never reaches the fresh end).

## 4. Specified-point methods: the common missing input (`CORE_SPECIFIED_POINT_INPUT`)

Every method that proves equidistribution/normality of a **specified** (not a.e., not constructed) point needs a **fixed
finite/sofic multiplicative model in which the orbit's increments act as one fixed group element** (a pure power-orbit):
- **Bailey–Crandall** (Stoneham `b`-normal): needs **integer base** `b` (reduces to `b^k mod c^n` in the fixed group
  `(ℤ/c^nℤ)^*`). The closest method (same map family `y_{n+1}=b y_n + r_n mod 1`). Seed-8 supplies the *multiplier* half
  (`3∈(ℤ/2^kℤ)^*`) but the action is **twisted by `÷2^{D_n}`** (`D_n=v₂(3c_n−1)`, orbit-dependent, non-unit, couples
  high↔low bits), so it **does not descend to a finite quotient** — the modulus `2ⁿ` grows. That non-descent *is* the
  non-integrality of 3/2.
- **Tao 2019** (a.e. Collatz): needs **averaging over the starting point** (ensemble). No single-orbit partial extractable.
- **Constructed normals** (Champernowne, Becher–Heiber–Slaman): need **construction freedom**.
Seed-8 is non-integer, non-Pisot, single, and given — so integrality, Pisot-soficity, ensemble-averaging, and
construction-freedom are **all four absent**. Supplying the finite-group surrogate = `D_n` equidistributes = `(K)`.

## 5. The unified picture & the most plausible shape of a proof

**All four probes converge:** the orbit arithmetic a proof must exploit is the **single-orbit equidistribution of
`D_n = v₂(3c_n−1)`** (= the quenched Weyl sum = annealed→quenched transfer of `ν̂_{2/3}`). There is **no sub-(K) statement**
that supplies it; the exogenous (digits-of-3ⁿ) and endogenous (carry) parts both reduce to it; the No-Structure theorem
forbids any structural/coboundary/measure certificate; the cross-field sweep + the magnitude/adelic no-gos forbid the
spectral and unbounded-Lyapunov routes.

**The one un-pre-empted shape.** What remains *not* ruled out is a **quenched return-time / Lyapunov sub-action argument on
the proven 2-adic potential `V = v₂(c−1)`** (deterministic drift `−1` per `D=1` step; `o=1` dual-repelling). It is:
- **not a spectral contraction** (the L_ann no-go forbids the gap from reaching `V_odd`);
- **not structure-only** (the No-Structure theorem forbids certificates constant on `M_feas`);
- but a **Kac-type identity coupling the odd-character feedback `Inj_a` to the excursion statistics of `V`** across the
  renewal countdowns (iid-geometric jumps of the induced first-return map `F`). The numerics sharpen the target: since the
  per-step feedback is **white**, any decrease must live in the **conditional return-time law**, not a per-step drift.

**The circularity to break.** The conditional return-time law of `V` *is* the `D`-statistics, which *is* `(K)`. A genuine
proof must extract a return-time decrease from the orbit's specific 2-adic arithmetic **without** assuming the D-law — an
*a-priori* excursion estimate. No known method does this for a single non-Pisot orbit; it is the precise generational gap.

## 5′. Citation correction [SOUNDNESS]

The repo (`DIGITS_OF_3N.md`, and `BB6_FRAMEWORK_PACKAGE.md` §8) attributes the longest-run bound `L(M·3ⁿ)=o(n)` to
"Spiegelhofer–Wallner, arXiv:2501.00850, Lemma 4.1." A direct fetch shows **arXiv:2501.00850 is Drmota–Spiegelhofer on
digit-*sum* normality (via Baker's theorem), not a run lemma.** The run bound is real (Schlickewei p-adic subspace theorem)
but its exact reference is **unverified** — relabel `[PROVEN-in-lit, citation-pending]` and do not cite 2501.00850 for it.
(Fixed in §6 / the package; flagged here.)

---

## 6. Net

The deepest examination confirms — from four independent directions, each landing on the same point — that `(K)` has **no
proper sub-problem**: the exogenous moving diagonal, the endogenous carry, the MR carry lemma, and every specified-point
method all reduce to single-orbit equidistribution of `D_n=v₂(3c_n−1)`. The most plausible un-pre-empted route is a
**quenched Kac/Lyapunov return-time argument on `V=v₂(c−1)`** with the decrease in the conditional return-time law; its
circularity (the return-time law = the D-statistics) is the exact generational frontier. This is the sharpest available map
of *what a proof must do*. **No machine decided. No label upgraded.** `(K)` remains [OPEN] = Mahler 3/2 / AEV.
