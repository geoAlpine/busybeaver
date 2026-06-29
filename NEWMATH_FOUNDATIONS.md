# The PROVEN foundations a new tool to crack (K) gets to build on (2026-06-30)

*Program specification, NOT a proof. This is the inventory of "inputs in hand" — every genuinely
[PROVEN] / [PROVEN-in-lit] structural fact the missing theory may use as an axiom. (K) itself remains
[OPEN] = Mahler 3/2 / AEV Conj 1.6 at α=8. Each item: exact statement, source, what it provides. Items
whose label was corrected/retracted this session are flagged in §8 and must NOT be used in their old form.
SOUNDNESS: only verified [PROVEN]/[PROVEN-in-lit] items are listed; nothing here is upgraded.*

---

## 0. The target the foundations support

> **Kernel (K) [OPEN].** For the induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `D(o)=v₂(3o−1)`, seed `o₀=27`:
> `liminf_N (1/N)#{n<N : D(o_n)≥2} ≥ 1/2`. Equivalently `mean D ≥ 3/2` ⟺ even-density of `c₀=8` orbit
> `≥1/3` ⟺ single-orbit equidistribution of `c_n mod 2^k` ⟺ base-3/2 normality of the seed-8 orbit.
> A new tool must *select the orbit of o₀* from the violating orbits; the items below are what it may assume.

---

## 1. REDUCTION-CHAIN foundations (the observable, the criterion, the equivalences)

All [PROVEN], machine-checked (`COMPLETE_PROOF_CAPSTONE.md` §1–2, `KERNEL_FINAL.md`).

- **R1. Halting criterion.** `c₀=8`, `c_{n+1}=⌊3c_n/2⌋`; `balance_n:=3E_n−n` (`E_n`=#even so far).
  Antihydra **halts iff `balance_n<0` for some `n`** ⟺ even-density `<1/3` at some `n`. Threshold `1/3` exact.
  *Provides:* the all-n target; the converse (halt if `liminf` even-density `<1/3`).
- **R2. GAP LEMMA (induced odd map).** For odd `c_i`, `D:=v₂(3c_i−1)` = exact #steps to next odd value;
  collapses the orbit to `T(o)=3^{D−1}(3o−1)/2^D`, `o₀=27`. *Provides:* the clean map to work on.
- **R3. Renewal / Kac identity.** even-density `= 1 − 1/(mean D)`, so even-density `≥1/3 ⟺ mean D ≥ 3/2`.
  *Provides:* the conversion density↔mean depth.
- **R4. Valuation formula.** `D≥k ⟺ o≡3⁻¹ mod 2^k`; `mean D = Σ_{k≥1} freq(o≡3⁻¹ mod 2^k)`; `D=1⟺o≡1 mod4`,
  `D≥2⟺o≡3 mod4`. *Provides:* the one-sided cylinder form `freq(o≡3 mod4)≥1/2`.
- **R5. The observable ψ and the criterion.** `ψ(o):=½−1{D≥2}−1{D≥3}` (function of `o mod 8`: `+½,−½,−3/2`).
  `(1/N)Σψ = ½ − (1/N)Σ[1{D≥2}+1{D≥3}]`; Haar mean `∫ψ dHaar=−1/4` (margin 1/4). The robust SUFFICIENT
  criterion is `limsup_N (1/N)Σψ ≤ 0 ⟹ mean D ≥ 3/2`. *Provides:* the exact test function for ergodic-opt /
  sub-action arguments, with a 1/4 Haar margin.
- **R6. Equivalent forms (all [PROVEN]-equivalent to (K)).** mean D≥3/2; even-density≥1/3; `freq(o≡3 mod4)≥1/2`
  (zero-margin); `freq(D≥2)+freq(D≥3)≥1/2` (robust, margin 1/4); 3-adic `density{3|o}+density{9|o}≥1/2`;
  3-free-cofactor independence. *Provides:* multiple equivalent surfaces to attack.
- **R7. Literature placement.** (K) is the floor-mirror, one-sided, single-level (k=2), single-orbit fragment
  of AEV Conj 1.6 (arXiv:2510.11723); AEV Thm 1.7 ⟹ normality Conj 1.2, Thm 1.5 (p<q², holds at 3/2) ⟹
  Mahler 1968. *Provides:* the named open problem (K) closes the instant of.
- **R8. Exact halt predicate (certificate side).** Antihydra HALTS ⟺ `∃n: v₂(c_n−1) ≥ balance_n+1`
  (`LIMIT_THEOREM.md` §3, `antihydra_attack.md` §3c). *Provides:* the 2-adic-proximity-to-1 form of halting.

## 2. OPERATOR-ANALYTIC foundations (the induced map, the annealed operator, the seam identity)

- **O1. Induced map is exact Bernoulli [PROVEN].** `T` is Haar-preserving, exact, Bernoulli on `ℤ₂^*`; cylinders
  `A_d={v₂(3o−1)=d}` (Haar `2^{−d}`) each map *onto* `ℤ₂^*` (full-branch); symbols `D_j` i.i.d. geometric
  `P(D=d)=2^{−d}`, mean 2; Haar `mean D=2>3/2` with CLT + exponential large deviations. (`COMPLETE_PROOF_CAPSTONE.md` §3.)
  *Provides:* the a.e. truth of (K) with room to spare; the measure side is COMPLETE.
- **O2. Carry automaton (exact finite-state, one fresh bit/step) [PROVEN].** With `s_n=c_n mod 2^k`,
  `β_n=bit_k(c_n)`: `s_{n+1}=U(s_n,β_n)`, `U(s,β)=⌊3(s+β·2^k)/2⌋ mod 2^k`, and `U(s,1)=U(s,0)+2^{k−1}` exactly
  (fresh bit flips bit `k−1` of next state). (`ENDOGENOUS_UE_BUILD.md` §2.1.) *Provides:* the exact closed-loop
  dynamical system; the self-reference is `β_n=bit_k(c_n)` (a digit of the state being transported).
- **O3. Carry recursion / diagonal split [PROVEN].** Self-referential carry `S_{n+1}=3S_n+2^n b_n` (`b_n`=parity);
  the fresh bit splits exactly `β_n = d_n ⊕ σ_n ⊕ ρ_n`, `d_n=bit_{n+k}(8·3^n)` (exogenous Mahler diagonal),
  `σ_n=bit_{n+k}(S_n)` (carry diagonal), `ρ_n` finite-range borrow. (`SESSION_2026-06-29_AEV_CORE.md`,
  `CORE_ORBIT_ARITHMETIC.md` §1.) *Provides:* the exogenous/endogenous decomposition of the parity bit.
- **O4. Annealed transfer operator + spectral gap [PROVEN].** `L_ann f(s)=½[f(U(s,0))+f(U(s,1))]`, stationary
  = uniform, spectral gap `1−λ₂(k)>0` (`λ₂=0.0001…0.34`, also the low-bit chain gap `≈0.99`). (`ENDOGENOUS_UE_BUILD.md`
  §2.2, `ANNEALED_PARTIAL_BANKED.md` item 13.) *Provides:* the only contraction in hand (acts on even block — see N3).
- **O5. Exact seam identity [PROVEN].** `((I−L_ann^*)π_N)(f)=Feedback_N(f)+O(1/N)`,
  `Feedback_N(f)=(1/N)Σ(β_n−½)Δf(s_n)`, `Δf(s)=f(U(s,1))−f(U(s,0))`. For odd characters `π_N(χ_a)=Feedback_N(χ_a)+O(1/N)`.
  (`ENDOGENOUS_UE_BUILD.md` §2.3.) *Provides:* the exact (not heuristic) endogeneity recursion; the kernel = "fresh
  bit decorrelates from low-state characters."
- **O6. Conditional contraction (even enslaved to odd) [PROVEN].**
  `‖π_N|_{V_even}‖ ≤ (1−λ₂)^{−1}‖coupling‖·‖π_N|_{V_odd}‖ + O(1/N)`; the recursion `Def(k+1)≤ρDef(k)+Inj(k)`
  derived exactly with `ρ=λ₂`. (`ENDOGENOUS_UE_BUILD.md` §3, `NEWMATH_ENDOGENOUS_UE.md` Lemma C.) *Provides:* you
  only need to control the ODD block; parity/even-density follow for free.

## 3. POTENTIAL / LYAPUNOV foundations (the 2-adic potential and the drifts)

- **P1. Countdown Lemma [PROVEN].** `φ(o):=v₂(o−1)`; each `D=1` step does `φ→φ−1` exactly. Hence a run of `m`
  consecutive `D=1` steps ⟺ `o≡1 mod 2^{m+1}` (cylinder measure `2^{−(m+1)}`); maximal run `L=v₂(o_start−1)−1`.
  Self-limiting: infinite `D=1` run only at off-orbit `o=1`. (`MINPROP_RUNS.md` §1–2, verified 75139/75139.)
  *Provides:* the deterministic 2-adic potential `V=φ` with drift `−1` on `D=1`.
- **P2. Dual-Repulsion Lemma [PROVEN].** On a `D=1` step: `o'−1=(3/2)(o−1)`, so `|o−1|_∞×3/2`, `|o−1|_2×2`,
  oddpart(o−1)×3, adelic `|o−1|_∞|o−1|_2 ×3`. `o=1` repels simultaneously in archimedean AND 2-adic places.
  (`REPELLER_ESCAPE.md` §1, verified 300174/300174.) *Provides:* the halting fixed point is escaped unconditionally;
  the candidate Lyapunov engine `V=v₂(c−1)`.
- **P3. Renewal closed form for the shallow set [PROVEN].** `freq(D=1)=1−1/E_deep`, `E_deep`=mean over deep
  (`D≥2`) steps of `v₂(o_next−1)`; tight target `freq(D=1)≤1/2 ⟺ E_deep≤2`. (`MINPROP_RUNS.md` §3, `REPELLER_ESCAPE.md` §2.)
  *Provides:* the sharpest localization of the tight target — a conditional mean over the sparse deep substeps.
- **P4. Lyapunov exponents [PROVEN].** Per `D=1` step the three local multipliers are `(3/2, 2, 1/3)` at places
  `(∞,2,3)` (so `log(3/2)`, `log2`, `−log3`); product `=3` (the adelic distance-to-1 multiplier). For the solenoid
  automorphism `A=×(3/2)` the dilations are exactly `(3/2,2,1/3)`, product 1 (hyperbolic, no neutral direction).
  (`REPELLER_ESCAPE.md` §1, `NEWMATH_ADELIC_RIGIDITY.md` §1.) *Provides:* the hyperbolic structure and the stable
  (3-adic) leaf to disintegrate along.
- **P5. Adelic-height degeneracy [PROVEN].** `H(o)=log oddpart(o−1)` jumps `+log3` per `D=1` step but its full
  telescoping collapses to the trivial `ΣD` identity (the 2-adic φ-balance `Σ_deep(r'−1)=#{D=1}` absorbs the
  archimedean side). (`REPELLER_ESCAPE.md` §3.) *Provides:* a PROVEN no-go — the two valuations are NOT independent
  constraints at the height level; the genuine valuation-independence lives in the refill law `E_deep`.

## 4. ADELIC / SOLENOID foundations (the host realization, product formula, 2↔3 coupling)

- **A1. Solenoid host realization [PROVEN].** On `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`, `M_2=×2`, `M_3=×3 ∈ Aut(X)` commute and
  are hyperbolic; `A=×(3/2)=M_3 M_2⁻¹` is a **rank-1 line in the rank-2 host `Φ=⟨×2,×3⟩`**. The seed `8∈ℤ[1/6]⊂X`.
  Slope `log(3/2):log2` is irrational. (`NEWMATH_ADELIC_RIGIDITY.md` §1, `NEWMATH_SYNTHESIS.md` §3.1.) *Provides:*
  the Rudolph–Johnson / Furstenberg ×2,×3 world genuinely acts on this space (the old "rank-2 unavailable" was wrong).
- **A2. Z² shift symmetry of the digit family [PROVEN].** `X_n(2^i 3^j α,k)=X_{n+j}(α,k−i−j)`; the group `⟨×2,×3⟩≅ℤ²`
  acts on the bit-grid by `(n,k)`-shifts; `×(3/2)` = the time-step `(i,j)=(−1,1)`. (`NEWMATH_DIAGONAL_RENORM.md` §1.2,
  verified 0/168000.) *Provides:* the renormalization-group action structure.
- **A3. Product formula = first-moment identity [PROVEN].** `∏_v|N|_v=1` gives only the single scalar
  `log o_n ≈ (ΣD_j)log(3/2)` per orbit (verified ratio 0.99999989). (`ADELIC_COUPLING.md` §1.) *Provides:* pins the
  MEAN `ΣD`, and nothing about the distribution — a clean ceiling for adelic methods.
- **A4. Exact 2↔3 coupling [PROVEN].** `v₃(o_{j+1})=D_j−1=v₂(3o_j−1)−1` every step (since `3o−1≡−1 mod3`; 0 exceptions
  /2·10⁵). Hence `freq(D≥2)=density{3|o}`, `freq(D≥3)=density{9|o}`; the orbit's 3-adic law is `P(v₃=k)=2^{−(k+1)}`
  (NOT ℤ₃-Haar). (`ADELIC_COUPLING.md` §1a.) *Provides:* an exact isomorphism of the obstruction (2-adic depth =
  3-adic divisibility density), product-formula-locked — a dual attack surface.
- **A5. Rank-2 host orbit is dense [PROVEN-in-lit].** `{2^a 3^b·8 : a,b∈ℤ}` is dense in `X` (Berend topological
  set-rigidity, totally-irreducible rank-2 hyperbolic). (`NEWMATH_ADELIC_RIGIDITY.md` §3.2.) *Provides:* the only
  proven topological-density fact (NB: applies to the rank-2 host orbit, NOT the rank-1 A-orbit — see N4/§8).
- **A6. Conditional rigidity finish [PROVEN-in-lit].** A `⟨×2,×3⟩`-invariant, ergodic, **positive-entropy** measure
  on this solenoid is Haar (Rudolph 1990 / Johnson). (`NEWMATH_ADELIC_RIGIDITY.md` §3.2.) *Provides:* the closing
  theorem — IF a new tool supplies host-invariance (AIU) AND positive entropy (ENT), Haar follows.

## 5. RENORMALIZATION foundations (the diagonal transducer, annealed gap, no-atom, coisometry)

- **N0. Exact diagonal recurrence [PROVEN].** `d_{n+1}^{(k)}=d_n^{(k+1)}⊕d_n^{(k)}⊕γ_n^{(k)}` (the ×3 binary-adder
  transducer), `d_n^{(k)}=bit_{n+k}(8·3^n)=bit_k(⌊8(3/2)^n⌋)`. (`NEWMATH_DIAGONAL_RENORM.md` §2, verified 0/35988.)
  *Provides:* an exact quenched self-similar recurrence for the moving diagonal (the carry `γ` is the hard term).
- **N1. Annealed renormalization gap 1/2 [PROVEN-numeric].** Randomizing the carry (Bernoulli ½) gives a finite
  Markov transducer with spectrum `{1,½,½,0,…}`, spectral gap `=½`, unique uniform/Haar fixed point `P(bit=1)=0.5`.
  (`NEWMATH_DIAGONAL_RENORM.md` §3.1.) *Provides:* the annealed `R` provably CONTRACTS to equidistribution at rate `2^{−n}`.
- **N2. Non-Pisot ⇒ no atomic/Pisot/sofic fixed point [PROVEN].** Places `|3/2|_∞=3/2, |3/2|_2=2(>1), |3/2|_3=1/3`,
  product 1; the bit-bearing 2-adic place EXPANDS, so there is no contracting direction for an atomic invariant
  measure; `R*:ξ↦(3/2)ξ` on `ℤ[1/6]` has no nonzero periodic point ⟹ purely Lebesgue/Haar spectrum, diagonal
  non-automatic. (`NEWMATH_DIAGONAL_RENORM.md` §3.2.) *Provides:* there is NO atomic/sofic shortcut and NO atomic
  obstruction to genericity — consistent with the (K)-target being Haar.
- **N3. L_ann annihilates odd characters [PROVEN].** `L_ann χ_a≡0` for every odd `a` (verified ≤1e-13); `L_ann χ_a=χ_a∘U(·,0)`
  for even `a`. (`ENDOGENOUS_UE_BUILD.md` §2.2.) *Provides:* the gap acts only on the even block; the odd block
  (where the conclusion lives) is invisible to it — forces a non-spectral third ingredient (also a proven-negative, N3).
- **N4. Cross-scale cocycle is a COISOMETRY [PROVEN].** `R_k:O^{(k+1)}→O^{(k)}` (odd→odd, exact `d^{(k)}=R_k d^{(k+1)}+O(1/N)`)
  satisfies `R_k R_k^*=I`, all singular values `=1`, `dim ker R_k = 2^{k−1}` (half); operator-norm Lyapunov of the
  cocycle `Φ` is EXACTLY 0. (`NEWMATH_ODD_CALCULUS.md` §2.) *Provides:* a sharp PROVEN no-go — no operator-norm/spectral
  contraction can ever exist across scales; (K) must be a quenched/Oseledets (data-direction) statement.
- **N5. Carry semiconjugacy [PROVEN].** `V^{(k+1)}(s) mod 2^k = U^{(k)}(s_low,bit_k)` — the top bit of scale `k+1`
  IS the fresh input of scale `k`; the infinite regress becomes a renormalization step. (`NEWMATH_ODD_CALCULUS.md` §1.2.)
  *Provides:* the scale-tower structure that turns self-reference into a cocycle over scales.

## 6. PROVEN PARTIALS (unconditional / annealed / a.e. results the tool may quote)

From `ANNEALED_PARTIAL_BANKED.md` (all re-verified at N=3·10⁵), `VALUATION_BUDGET.md`, `LIMIT_THEOREM.md`:

- **Q1. Non-Pisot ⇒ ν_{2/3} Rajchman [PROVEN-in-lit]** (Erdős–Salem): `|ν̂_{2/3}(ξ)|→0`. *Annealed mean only.*
- **Q2. Effective log decay of ν_{2/3} [PROVEN-in-lit]** (Varjú–Yu; Kershner): `≥ logarithmic` in `|ξ|`, sharp.
  *Power rate (`a≈1.71`) is itself (K)/Mahler.*
- **Q3. Annealed carry product Φ(N)=∏|cos(π{(3/2)^k/4})|→0 [PROVEN]**, with exact identity
  `|ν̂_{2/3}((3/2)^N/8)|=Φ(N)·C`, `C=0.774846171700205…`. *Ensemble only; quenched weights don't factor.*
- **Q4. Top-digit equidistribution [PROVEN]:** top `Θ(log N)` binary digits of `c_n` equidistribute (Weyl + Erdős–Turán,
  finite irrationality measure of `log₂3`). *Reaches depth `Θ(log N)`; the parity bit is the diagonal at depth `Θ(n)`.*
- **Q5. Salem–Zygmund + twisted-RPF CLT [PROVEN-in-lit, a.e.]:** `|Σ_{n<N}e(ξ(3/2)^n)|=O(√(N log log N))` for a.e. ξ;
  quenched CLT for a.e. sequence. *a.e. ξ, not specializable to seed-8.*
- **Q6. Vaaler L¹ minorant ceiling [PROVEN]:** H2 needs only `J=5` circle frequencies; rigorous crude-bound ceiling
  `θ*≤1/6`, LP-optimal `≈0.043` (≥96% per-frequency cancellation needed). *Reduces frequency count to finite.*
- **Q7. FLP spread [PROVEN-in-lit]:** `Ω(3/2)=limsup−liminf{ξ(3/2)^n}≥1/3`. *Support/range, not frequency.*
- **Q8. Zudilin/Padé [PROVEN-in-lit]:** `‖(3/2)^n‖>0.5803^n` for `n≥K`. *Pointwise single-term, no density.*
- **Q9. Longest run [PROVEN-in-lit, citation-pending]:** `L(8·3^n)=o(n)` (Schlickewei p-adic subspace theorem).
  *See §8 — do NOT cite arXiv:2501.00850.*
- **Q10. #even ≥ 0.89 log n [PROVEN]** (tightest unconditional density-style fact; from orbit growth
  `bitlen(c_p)=0.585p+O(1)`). *`log n` vs needed `εn` — the whole wall is the `log n→n` factor.*
- **Q11. Valuation budget [PROVEN]:** `Σ_{i<n, c_i odd} v₂(3c_i−1) = n + v₂(c_n) − v₂(c_0)` (exact); third criterion
  form `avgD_odd≥3/2`; unconditional FLP-type range `n−v₂(c_0) ≤ Σ ≤ 1.585n−3`. (`VALUATION_BUDGET.md`.) *Provides:*
  the first-moment seed for any second-moment/energy attack; cleanest lower-bound criterion form.
- **Q12. Subword-complexity floor [PROVEN]:** parity sequence `r_n=c_n mod2` has `p(ℓ)≥1.71ℓ` (slope `log_{3/2}2`,
  matching Dubickas), capped by `p(ℓ+1)≤2p(ℓ)`; not eventually periodic, not Sturmian. (`LIMIT_THEOREM.md` §3″.)
  *Provides:* an elementary complexity floor; `p(ℓ)=2^ℓ` (max) ⟺ (K).
- **Q13. Certificate-complexity tower [PROVEN]:** five strict separations
  `star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ CF ⊊ CS`, each with explicit verified TM witnesses (Squeeze Lemma).
  (`LIMIT_THEOREM.md` §2–5.) *Provides:* the rigorous descriptive-complexity anchor; the cryptid sits on the
  orthogonal over-approximation axis (= (K)).

## 7. PROVEN NEGATIVES the tool can RELY ON as structure

These are PROVEN no-gos — facts the tool may treat as fixed structural truths (they say where the answer is NOT).

- **N3 (above) — gap blindness.** `L_ann χ_odd≡0` and an adversary with identical `(gap, automaton)` realizes
  feedback `≈1` (`ENDOGENOUS_UE_BUILD.md` §5): **no bound `Inj(k)≤F(λ₂,γ)` exists**; any selector must use the
  endogenous input's arithmetic. *Reliable structure: the third ingredient is mandatory and non-spectral.*
- **N4 (above) — coisometry.** Cross-scale renormalization has operator-norm Lyapunov ≡ 0; **no spectral contraction
  across scales**. *Reliable structure: (K) is a data-direction (Oseledets) negativity, provably not an operator norm.*
- **NEG1. Ergodic-optimization β=+½ [PROVEN]** (`MINPROP_COBOUNDARY_LP.md`, `BB6_NO_STRUCTURE_THEOREM.md` §3):
  `β(ψ)=max_{T-inv μ}∫ψ dμ = +½>0`, attained at the atom `δ₁` (fixed point `o=1`, `D=1` forever). The coboundary-LP
  is infeasible at every level `k=3..12` (exact `Fraction`, level-independent, tail-audited). **Extended this session
  to unbounded magnitude-aware / adelic sub-actions** (product-formula sign tension forces `α_∞≥0`, antipodal to useful).
  *Reliable structure: NO bounded (or magnitude-aware/adelic) residue sub-action can prove (K).*
- **NEG2. Specification full-dimension [PROVEN]** (`MINPROP_COUPLING.md`): `T` full-branch ⟹ specification; by
  multifractal analysis every interior Birkhoff value of `1{D≥2}` is realized on a **full-Hausdorff-dimension** set;
  extrema `0` (at `δ₁`) and `1` (at `o=3/5`). *Reliable structure: (K) is non-universal — a full-dimension set of
  orbits violates it; the tool MUST single out o₀ by magnitude/arithmetic.*
- **NEG3. a.e.-true but o₀-null [PROVEN]:** exact+Bernoulli gives (K) for Haar-a.e. start, but `{o₀}` is null and lies
  in the full-dimension non-generic set (Barreira–Schmeling). *Reliable structure: measure-level/annealed arguments
  give nothing about the specified orbit.*
- **NEG4. The obstruction dichotomy (HARD direction) [PROVEN]** (`BB6_OBSTRUCTION_DICHOTOMY.md` §2): any bounded
  functional of the empirical measure that is not constant on `M_feas` and whose Haar-value is a (K)-target cannot
  be established from closure/topological/first-moment/annealed data — that data is constant on `M_feas`, which
  provably contains non-Haar measures (β=+½ off Haar; specification). *Reliable structure: ~20 routes stop at the same
  proven boundary (topological-closure-determined vs Haar-selecting).*
- **NEG5. Coupling is first-moment only [PROVEN]** (`ADELIC_COUPLING.md`, `VALUATION_BUDGET.md`): product formula,
  valuation budget, adelic coupling all pin only `ΣD` / first moments; the distribution (`freq(D=1)`) is left free;
  the EK2-second-budget mechanism — degree-1 depth potential telescopes to a count `≤N` (free), degree-≥2 to a tautology.
  *Reliable structure: first moments are free, second+ moments are the conclusion not a usable input.*
- **NEG6. Excursion drift is linear in K [PROVEN]** (`CORE_ORBIT_ARITHMETIC.md` §5 update, `EXCURSION_SYNTHESIS.md`):
  every candidate excursion-drift reads only `E[K]` (first moment); forcing `~K²` (what `E[K²]<∞` needs) is the
  degree-2 potential that telescopes to `0=0`; a heavy-tailed adversary (`E[K²]=∞`, white, first-moment-matched)
  satisfies every proven fact and is drift-indistinguishable. *Reliable structure: the second moment is the
  conclusion; the proven facts are consistent with both (K) and its negation.*
- **NEG7. Furstenberg/Rudolph rigidity needs a jointly-invariant positive-entropy measure the orbit does not supply
  [PROVEN-honest]** (`ADELIC_COUPLING.md` §2): ×2,×3 theory classifies invariant MEASURES, not single orbits; our
  orbit gives only an `A`-invariant limit, no positive-entropy jointly-invariant measure. *Reliable structure: rigidity
  applies only after host-invariance (AIU) + entropy (ENT) are independently supplied.*

## 8. CORRECTED / RETRACTED this session — do NOT use in old form

- **[RETRACTED] "Rank-2 dichotomy lemma: A-invariance is the only gap."** Over-claimed: Berend gives only topological
  full SUPPORT, not Haar. **Correct:** there are TWO gaps to Haar — **(AIU)** A-invariant ⟹ Φ-invariant, AND **(ENT)**
  `h_μ(M₂)>0`; with both, proven Rudolph–Johnson gives Haar. (`NEWMATH_ADELIC_RIGIDITY.md` §3.2, `DICHOTOMY_LEMMA_AUDIT.md`,
  `NEWMATH_SYNTHESIS.md` §0/§3.)
- **[RETRACTED] "Limit measure is plausibly zero-entropy (Furstenberg corner)."** Sign error: `p(ℓ)≥1.71ℓ` is a LOWER
  bound; measured complexity is full (`p(ℓ)=2^ℓ` to ℓ=16, `h_top=log2`). **Zero entropy is the (K)-FALSE regime**
  (Haar has `h(M₂)=log2>0`), not a tractable corner. (`LIMIT_MEASURE_ENTROPY.md`, `NEWMATH_SYNTHESIS.md` §0.)
- **[CORRECTED] "Periodic 2-adic repulsion proves μ non-atomic."** It does not (an atom needs only positive-density
  re-entry = vanishing occupancy = (K)-hard); **μ non-atomicity is [OPEN]**, only implied by the positive-entropy
  hypothesis. (`ENT_NONATOMIC.md`, `NEWMATH_ADELIC_RIGIDITY.md` §2.3.)
- **[CORRECTED] Citation for the longest-run bound.** The run bound `L(M·3^n)=o(n)` is real (Schlickewei subspace
  theorem) but arXiv:2501.00850 is Drmota–Spiegelhofer on digit-SUM normality, NOT a run lemma. Relabel
  **[PROVEN-in-lit, citation-pending]**; do NOT cite 2501.00850 for it. (`CORE_ORBIT_ARITHMETIC.md` §5′.)
- **[CORRECTED] Naive dichotomy "FREE ⟺ constant on M".** Falsified as a literal biconditional (`#even≥0.89 log n`
  is FREE yet not constant on `M_sys`). The FREE side is a superset (closure/tail/topological register); only the
  HARD direction is a theorem. (`BB6_OBSTRUCTION_DICHOTOMY.md` §1, `DICHOTOMY_REDTEAM.md`.)

---

## 9. The most load-bearing inputs (what the missing tool most likely leans on)

1. **The exact reduction chain (§1) + the exact carry automaton/seam identity (§2).** These make (K) a precise
   single-orbit equidistribution statement with an exact closed-loop model — the indispensable scaffold.
2. **The 2-adic Lyapunov potential `V=v₂(c−1)` with proven drift `−1` and dual-repulsion (§3, P1–P2).** This is the
   candidate ENGINE every un-pre-empted route (quenched Kac/Lyapunov return-time / EAR / CR) is built on.
3. **The solenoid host + Rudolph–Johnson finish (§4, A1/A6).** The one bridge to a powerful PROVEN external theory;
   reduces (K) to the two named inputs AIU + ENT.
4. **The proven no-gos (§5 N3/N4, §7 NEG1–NEG6).** They are not just walls — they are reliable structural truths that
   FORCE the shape of any proof: non-spectral, data-direction/Oseledets, second-moment-as-conclusion, orbit-arithmetic
   selection. A new tool must respect all of them.

**No machine decided. No label upgraded.**
