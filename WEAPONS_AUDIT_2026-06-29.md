# Total weapons audit toward a complete BB(6)/Antihydra proof — all past data (2026-06-29)

*Full-corpus sweep: 6 read-only cluster audits (reductions/cryptids · analytic/exp-sum · dynamics/transfer-operator ·
Wall-B/selector · integrality/limit-theorems · meta/new-math) + this session's 3-angle frontier assault. Goal: find any
underexploited weapon — a proven partial that could combine, a cross-route hybrid, an unfollowed OPEN sub-lemma — toward a
complete proof; if none, specify the new mathematics precisely. SOUNDNESS: every claim labelled
[PROVEN]/[PROVEN-in-lit]/[OBSERVED]/[OPEN]; zero false proofs; no label upgraded. Core numerics re-verified here with exact
big-int (`scratchpad/quick_anchor.py`): even-density 0.50018, worst running `(1/N)Σ(−1)^{c_n}` = −0.0407 at n=122 (margin
0.293 above the H₂ floor −1/3), N=2·10⁵. NOT committed.*

---

## 0. One-line verdict

**There is no unconditional weapon, and — newly — the absence is PROVEN, not merely observed.** Every one of ~14 attack
routes funnels to a single point (K)/H₂, and two **impossibility meta-theorems** (ergodic-optimization β=+½ at the halting
fixed point; specification realizing every Birkhoff value on a full-dimension set) prove that **no structure-only / all-orbits
/ finite-certificate argument can ever decide it**. The kernel is therefore genuinely orbit-specific and equals a named
generational open problem (Mahler 3/2 = base-3/2 normality = AEV Conj 1.6 = special case of the Algom–Baker–Shmerkin
theorem, Adv. Math. 2022 — exposition Algom arXiv:2504.18192 — Problems 1+3).
**New mathematics is required; this audit specifies it (§5) and records that this session closed the last two structural
escape hatches (Naud-via-conjugacy, Korobov-via-slack).**

---

## 1. The funnel — every route lands on ONE kernel [PROVEN, this is the central structural fact]

**Kernel (K)/H₂** (sharpest form, `WEAKEST_SUFFICIENT.md`): for `c₀=8`, `c→⌊3c/2⌋`,
> **liminf_N (1/N) Σ_{n<N} (−1)^{c_n} ≥ −1/3**  ⟺  even-density ≥ 1/3  ⟺  mean `D=v₂(3o−1)` ≥ 3/2  ⟺  single-orbit
> equidistribution of `c_n mod 2^k`  ⟺  base-3/2 normality of the orbit  = **Mahler 3/2 / AEV Conj 1.6 (rational base)**.

Five-link reduction chain, each link [PROVEN] and bb_sim-cross-checked (`BB6_STRUCTURAL_LIMIT_THEOREM.md` §3–4,
`COMPLETE_PROOF_CAPSTONE.md` §2): halt ⟺ `balance_n=3E_n−n<0` ⟺ `mean D≥3/2` ⟺ even-density≥1/3 ⟺
`∃n: v₂(c_n−1)≥balance_n+1`.

**Why the funnel is not a coincidence — two impossibility meta-theorems [PROVEN]:**
- **Ergodic-optimization barrier** (`MINPROP_COBOUNDARY_LP.md`, `COMPLETE_PROOF_CAPSTONE.md`): `β = max_μ ∫(θ−ϕ)dμ = +1/2 > 0`,
  attained at the atomic measure δ₁ on the **halting fixed point o=1**. The sub-action LP is infeasible at every level k=3..12.
  ⇒ **no bounded coboundary / structure-only certificate exists**; the halting orbit shares all available structure.
- **Specification / multifractal** (`MINPROP_COUPLING.md`): orbits realizing **every** interior Birkhoff value of `1{D≥2}`
  exist on a full-Hausdorff-dimension set (Dirac at o=1 → 0; Dirac at o=3/5 → 1; interval interior dense). ⇒ the bound is
  **non-universal**; any valid argument for the seed 8 is **forced** to use that seed's specific arithmetic = single-orbit
  equidistribution = (K).

These two are the reason every weapon below stops at the same wall: the wall is provably orbit-specific.

---

## 2. The banked weapons [PROVEN] — what survives even if the wall never breaks

### 2A. Structural / integrality (exact, machine-verified) — the durable core
| Weapon | Statement | Controls | Source |
|---|---|---|---|
| Valuation budget identity | `Σ_{odd i<n} v₂(3c_i−1) = n + v₂(c_n) − v₂(c_0)` (exact) | first moment only (renewal tautology) | `VALUATION_BUDGET.md`, `M4_P2_RESULT.md` |
| Induced map = exact Bernoulli | `T(o)=3^{D−1}(3o−1)/2^D` Haar-preserving, exact; under Haar `D_j` iid geom(2^{−d}), mean 2 | a.e./Haar genericity (NOT seed 8) | `BB6_STRUCTURAL_LIMIT_THEOREM.md` §4.2 |
| GAP / Countdown / Dual-Repulsion | gap to next odd = D; D=1 ⇒ `o−1 ×(3/2)`, `|o−1|₂ ×2` (o=1 repelling in both valuations) | exact orbit mechanics; verified 300174/300174 | `MINPROP_RUNS.md`, `REPELLER_ESCAPE.md` |
| ψ = function of D | D=1⟺o≡1(4); D=2⟺o≡7(8); D≥3⟺o≡3(8) (elementary proof) | closes β=+½ computation airtight | `BB6_STRUCTURAL_LIMIT_THEOREM.md` §4.5 |
| Non-periodicity (C3) | integer orbit grows past all cycles `N/(3^q−2^q)∈(0,1)`; itinerary not eventually periodic | eliminates structured exceptional set | `WALLB_NONATOMIC.md`, verified q≤10 (2046 cycles) |
| Floor-mirror conjugacy | `T_ceil(x)=−T_floor(−x)`; depth sequences identical | floor 3/2 ≡ ceiling 3/2 ≡ AEV 1.6 (PROVEN equiv) | `FLOOR_MIRROR_CONJECTURE.md` |
| Family classification | `v_p(μ)=−1` ⇒ clean p-to-1 exact endomorphism of ℤ_p; one obstruction map | unifies Antihydra,o10,o15,o18,o5,o7,o8,o11–16 | `CRYPTID_KERNEL.md` |
| 2-adic FLP range | `n−v₂(c₀) ≤ Σ_{odd} v₂(3c_i−1) ≤ 1.585n−3` (unconditional two-sided) | unconditional range (not density) | `VALUATION_BUDGET.md` |
| Certificate hierarchy | 5 strict separations star-free⊊REG⊊SLIN⊊2-automatic⊊CF⊊CS, each with witness | conjecture-independent complexity result | `LIMIT_THEOREM.md` §2,5–6 |
| Subword-complexity floor | `p(ℓ) ≥ (ℓ−3)/log₂(3/2) ≈ 1.71ℓ` | linear (entropy 0); far below normality | `LIMIT_THEOREM.md` §3″ |

### 2B. Analytic / Fourier (unconditional but **annealed / a.e. only**)
- **Non-Pisot ⇒ Rajchman** [PROVEN-in-lit, Varjú–Yu 2020 arXiv:2004.09358]: `|ν̂_{2/3}(ξ)|→0`, **effective LOG rate**;
  polynomial rate [OPEN]. Annealed carry product `Φ(N)=Π|cos(π(3/2)^k/4)|→0`. Constant `√2·ν̂_{2/3}(1/8)=0.7748…`.
- **Top-digit equidistribution** [PROVEN]: top `Θ(log N)` binary digits of `c_n` equidistribute, discrepancy `≪1/N`, via
  irrationality measure of `log₂3` (`EFFECTIVE_TOPDIGIT.md`). Reaches only depth `Θ(log N)`; kernel bit is at depth `Θ(n)`.
- **Salem–Zygmund** [PROVEN-in-lit]: for a.e. ξ, `|Σ e(ξ(3/2)^n)| = O(√(N log log N))` — **not specializable** to seed 8.
- **Vaaler L¹ ceiling** [PROVEN]: H₂ needs only **J=5 circle frequencies**, per-frequency cancellation `≥96%` (θ*≈0.043);
  quantifies exactly what the factor-2 slack buys (`ONECHAR_CANCELLATION.md`).
- **FLP spread** [PROVEN-in-lit, 1995]: `Ω(3/2)≥1/3` — **support/range only**, says nothing about frequency.
- **Zudilin/Padé** [PROVEN-in-lit]: `‖(3/2)^n‖>0.5803^n` — pointwise, no density (beats Baker here).
- **Longest run** [PROVEN-in-lit, arXiv:2501.00850]: `L(8·3^n)=o(n)` (subspace theorem) — horizontal, two-sided → 0.
- **Tightest unconditional density-ish result** [PROVEN]: `#even(n) ≥ c·log n`, `c≈0.89` (`EVEN_DENSITY_PARTIAL.md`).
  Even-density → 0 is *marginally* consistent with this — i.e. it does NOT give positive even-density.

### 2C. Dynamics (annealed / Haar only)
- Renewal **spectral gap 0.99**; self-consistency operator contracts to `(E,ρ)=(½,0)` (`antihydra_renewal_attack.md` §12).
- Transfer-operator gap `ρ(L_t)<1` ⇒ annealed decay (= Rajchman) + quenched CLT **for a.e. sequence** — NOT single orbit
  (`THERMO_FORMALISM.md` §2.2; the a.e. tier is completed cleanly by twisted Gibbs–Markov / Aaronson–Denker–Gouëzel).
- **Endogeneity-defect localization** (`ENDOGENEITY_DEFECT.md`): recursion `Def(k+1) ≤ ρ(k)Def(k)+Inj(k)`; measured
  `ρ(k)<1` all k (0.0001..0.34), carried defect negligible (~3e−4), **injection Inj(k) dominates** and is empirically
  indistinguishable from i.i.d. — wall **localized** to "prove `Inj(k)→0`", but still anchored on the Mahler phase.

### 2D. Wall B (selector) — proven eliminations of the a.e.→specific gap
- Atomic exceptional set **eliminated** (orbit grows; `WALL_B_SELF_SELECTION.md`).
- Structured/periodic exceptional set **eliminated** (proven non-periodic; `WALLB_NONATOMIC.md`).
- Aperiodic exceptional set **= reduces to (A)** = Mahler (`WALLB_VALUATION_SHARP.md`).
- **Computability line** [PROVEN, `SELECTOR_COMPUTABILITY.md`]: every effective-randomness selector (ML/Schnorr/UD/Kurtz;
  effective-Birkhoff good set = Schnorr randoms) excludes all computable points; the orbit is computable; the only randomness
  rung compatible with computability is finite-state randomness = normality = the kernel itself. Non-Pisot kills the
  finite-state characterization (Schnorr–Stimm needs Pisot/sofic).
- **Bailey–Crandall Stoneham** [PROVEN-in-lit]: the *closest proven* specific-point normality theorem — needs **integer
  base** for the `b^k mod c^n` finite-group reduction; fails at base 3/2.
- **B_k autonomy** [OBSERVED, `Bk_AUTONOMY.md`]: middle digit decoupled from the foothold (σ(k)≈0); no inter-scale bridge.

---

## 3. The cross-route hybrids and unfollowed sub-lemmas — honestly assessed

The audits surfaced the candidate combinations. Each is evaluated for whether it **escapes** the §1 funnel. **None does**,
but two are the genuinely-underexploited leverage points and are recorded as the live frontier.

| # | Candidate hybrid / sub-lemma | Status | Why it does / doesn't escape |
|---|---|---|---|
| 1 | **Intra-term adelic coupling** `v₂(3o−1)=D` AND `v₃(o)=D_prev−1` on the **same** term (cross-term correlation ≈0, intra-term never mined) | **[OPEN, live]** | The one place a constraint might live that "single-orbit equidistribution" doesn't already capture — but currently an **exact identity** = isomorphism of obstruction, not reduction (`ADELIC_COUPLING.md`). Highest-novelty unexplored. |
| 2 | **Factor-2 slack + Vaaler J=5, one-sided** | **[OPEN, live]** | Slack relaxes frequency-**count** (J=5) and is orthogonal to the per-frequency wall; but per-frequency still needs `≥96%` single-orbit Weyl cancellation = (K). This session proved Korobov–Bourgain dies on the orthogonal **length-1-per-modulus** axis (§4). |
| 3 | Endogeneity `Inj(k)→0` (more tractable than global equidist.) | reduces to (A) | `log₂3` foothold controls top bits; `Inj(k)` is the fresh middle bit — opposite ends of `c_n`; bridging them **is** Mahler (`ENDOGENEITY_DEFECT.md` caveat). |
| 4 | Gap-lemma one-sided cylinder target `freq(o≡3 mod4)≥½ ⇒ E[D]≥3/2` | reduces to (A) | one-sided single-cylinder, but oscillates at Haar value with **zero structural margin** (`INDUCED_COLLATZ_CONJUGACY.md`). |
| 5 | 2-adic shift-renewal bootstrap (the gap-0.99 mechanism) | reduces to (A) | the incoming high bits that would close it **are the orbit's own high bits** — self-reference = (K) (`antihydra_renewal_attack.md` §6). |
| 6 | Anisotropic resonance-free strip for full twisted ×(3/2) operator | **CLOSED this session** | even if a strip exists it delivers only Haar tier; and §4 (NONCONSTANT_ROOF) proves no conjugacy supplies Naud's curvature without scrambling the kernel frequency. |
| 7 | Erdős-ternary cluster (o5,o15,o18) — cleaner *existence* halt, named problem, Narkiewicz upper bound | **best cross-family target** | deciding any one decides all three; but lower bound/finiteness is the same shape of open problem (a *different* generational wall, not easier in kind). `CRYPTID_KERNEL.md`. |

**Net:** the hybrids confirm the funnel rather than bypassing it. #1 and #2 are the only avenues not yet proven-closed; both
are recorded as live but currently reduce to single-orbit Weyl cancellation.

---

## 4. This session's three-angle frontier assault — two more escape hatches closed [PROVEN]

- **Non-constant-roof conjugacy (A3 pivot i) → `NONCONSTANT_ROOF_CONJUGACY.md` — CLOSED.** New [PROVEN] dichotomy at the
  **absolute-continuity threshold** (Shub–Sullivan, ETDS 5 1985): h∈AC ⇒ smooth ⇒ periodic multipliers all `(3/2)^p` ⇒ roof
  cohomologous to constant ⇒ lattice ⇒ Naud NLI fails; h∉AC (only way to non-lattice) ⇒ Naud applies to the analytic model
  but `h_*(Parry)⊥μ_g` (orbit is null) and the singular h scrambles the band-limited H₂ character. NLI-for-g and
  transfer-to-orbit sit on opposite sides of the AC line.
- **H₂-specialized Korobov cancellation (live move #2) → `H2_ONESIDED_CANCELLATION.md` — sub-route CLOSED.** New [PROVEN]
  negative: the Korobov–Bourgain geometric sum `Σ e_m(g^n)` is identically trivial along the H₂ diagonal — its saving needs
  within-modulus length `N≥t^ε`, but H₂ reads modulus `2^{n−2}` at **exactly one index per modulus** (length 1). The
  one-sided/factor-2 slack is **orthogonal** to this length obstruction. Self-generated carry also breaks the `g^n mod m`
  group structure (no-carry idealization agrees only 49% = chance).
- **Annealed-tier banking (live move #4)** — agent died on a `/login` tool-auth error; the banked partials are nonetheless
  fully captured in §2B above (Varjú–Yu log rate, top-digit `≪1/N`, `#even≥0.89 log n`, Φ(N) constant 0.7748…). A clean
  standalone note can be regenerated without WebSearch.

---

## 5. There is no weapon → the new mathematics, specified precisely

Because §1 proves the obstruction is orbit-specific and §§2–4 show every tool stops at the a.e./annealed tier or is
proven-closed, **a complete proof requires a genuinely new theorem.** The program has already specified it; this audit
confirms and sharpens it.

**OBJECT** (`COMPLETE_PROOF_CAPSTONE.md` §, the definitive spec): *an effective equidistribution theorem for a **single
specified** orbit of the rank-1 expanding map ×(3/2) on ℤ₂* — explicit `f(n)→0` with `|E_n/n − ½| ≤ f(n)`, one-sided,
`f<1/6` suffices, for `c₀=8`.

**THE CRUX TO CRACK.** Break the closed-loop identification bias for **one** realization: prove the self-referential bit
`bit_n(T_n)` is unbiased **without assuming independence** — an **endogenous-cocycle unique-ergodicity** statement (annealed
→ Dirac-quenched transfer). Every existing framework stops at a.e. random realizations; the one precedent ((T,T⁻¹)/RWRS)
abandons unique-ergodicity tools for probabilistic limit theorems — exactly the defect.

**INPUTS IN HAND** (so the build doesn't start from zero): one-step-exact annealed operator (contraction exists, gap 0.99);
explicit tame carry automaton γ; exact reduction to a single bit; complexity floors; the **closed technique-map** (this
audit) telling you which classical tools provably will not work.

**INPUTS NOT AVAILABLE** (the reason it is new math): a 2nd independent direction / rank-2 structure; Hecke symmetry;
unipotent structure; zero entropy; any randomness/genericity hypothesis on the seed.

**ISOMORPHISM STATUS — is it new math or a new bridge?** The needed object is *specified-orbit genericity for a hyperbolic
automorphism of the S-arithmetic solenoid `(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` with the **amenable** acting group `ℤ[1/6]⋊⟨3/2⟩`*
(`EXPERT_ASK_HOMOGENEOUS.md`, `TRACTABILITY_MAP.md`). This intersection appears to be an **empty spot in the toolbox**:
amenability blocks the rigidity engines (Ratner/ELV need rank≥2 or unipotent); hyperbolicity blocks the rotation/Weyl
engines. Candidate near-isomorphic homes to check before declaring it new: Gibbs–Markov decay-of-correlations on the 2-adic
Lipschitz space; effective rank-1 S-arithmetic equidistribution; low-autocorrelation binary sequences / self-induced
disorder (statistical physics); self-referential 2-adic digit fixed points. The program's named-special-case anchors are
**alive in current research**: AEV 2025 (Andrieu–Eliahou–Vivion, arXiv:2510.11723, Conj 1.6, rational base) and the
Algom–Baker–Shmerkin theorem (Adv. Math. 2022; exposition Algom arXiv:2504.18192, Problems 1+3 = effective rate +
non-integer base) — both stop one inch short on exactly our two axes. Closest published base-3/2↔Collatz bridge:
Eliahou–Verger-Gaugry, arXiv:2504.13716 (structural, no density theorem). Closest dynamical near-miss: BFLM (JAMS 2011) —
single-orbit torus equidistribution but for a **non-abelian** semigroup, failing precisely on amenability.

---

## 6. Recommended next moves (priority order)

1. **Mine the intra-term adelic coupling (hybrid #1)** — the single avenue carrying genuine novelty not yet proven to reduce:
   does the simultaneous `v₂(3o−1)` / `v₃(o)` constraint on one term yield a local arithmetic fact invisible in either place
   alone? (Currently an identity; test whether a joint ℤ₂×ℤ₃ self-consistency tightens it.)
2. **Attempt the endogenous-cocycle unique-ergodicity statement (§5 crux) directly** as the one new theorem — the annealed
   contraction is in hand; the missing step is the Dirac-quenched transfer for one seed.
3. **Bank the annealed partials** into a clean standalone note (no WebSearch needed; data in §2B).
4. **Pose the empty-toolbox question to experts** (AEV authors / Tao-circle / homogeneous-dynamics): is rank-1 amenable
   hyperbolic specified-orbit genericity a known concept, or genuinely new?

**No machine decided. No non-halt asserted. No label upgraded.** (K) remains [OPEN] = Mahler 3/2 / AEV. This audit
establishes, with two impossibility meta-theorems, that no recombination of the proven weapons can close it — the proof
needs the new theorem specified in §5.

---

## 7. Addendum — all four "next moves" executed (2026-06-29 PM)

All four §6 moves were run in parallel. Three close avenues with new [PROVEN] reasons; one (#4) confirms the diagnosis;
none cracks (K). Net: the new-math spec is now **sharpened to the operator level** (§7.5).

### 7.1 Intra-term adelic coupling (hybrid #1) → `INTRATERM_ADELIC_MINING.md` — **CLOSED as tautology** [PROVEN]
New joint ℤ₂×ℤ₃ law, verified exactly (0 failures, N=10⁵): with `o_j = 3^{e_j} u_j`, `gcd(u_j,6)=1`, `e_j = D_{j−1}−1`,
> **`D_j = 1 ⟺ u_j ≡ (−1)^{e_j} (mod 4)`.**
So `1{D_j=1}` is a deterministic 4-cell function of `(e_j mod 2, u_j mod 4)`. In the density decomposition
`freq(D=1)=Σ_p P(e≡p)·P(u≡(−1)^p mod 4 | e≡p)`, the 3-adic exponent enters **only** through `(−1)^{e_j}`, a Haar-preserving
permutation of `(ℤ/4)*` — **additively annihilated**. The full-complexity 3-adic structure contributes literally zero to the
kernel density; everything rides on one cofactor bit `density{u_j≡1 mod 4}`, with `u_j ⊥ e_j` (χ²=0.06). Dimension count
seals it: the product-formula/S-arithmetic self-consistency is **codimension-1** (first moment, ratio 0.99999979) while the
kernel is **codimension-∞**. No one-sided inequality (×(−1)^e is a symmetric bijection of {1,3}). The most-novel hybrid is an
**isomorphism of obstruction, not a reduction**.

### 7.2 Endogenous-cocycle UE (the new-math crux, §5) → `ENDOGENOUS_UE_BUILD.md` — **SHARP NO-GO** [PROVEN]
Target (EUE): empirical measure of `s_n=c_n mod 2^k` → uniform for every k, with **no** genericity hypothesis (≡ (K)).
Construction reached an **exact seam identity**: with carry automaton `U(s,β)=⌊3(s+β·2^k)/2⌋ mod 2^k` driven by the
endogenous bit `β_n=bit_k(c_n)`, `((I−L_ann*)π_N)(f) = Feedback_N(f) + O(1/N)`. The decisive new [PROVEN] fact (verified to
1e−13):
> **L_ann annihilates every ODD character (`L_ann χ_a ≡ 0` for a odd).**
Hence the feedback localizes **exactly** to the odd-character subspace and equals the equidistribution defect itself. The
operator is **block-triangular**: the even block (which holds parity / even-density) is gap-controlled with `ρ=λ₂`, **but is
driven by the odd block, which the gap does not touch.** This upgrades the measured recursion `Def(k+1)≤ρDef(k)+Inj(k)` to an
exact operator identity. **No-go:** an adversary with the *identical* `(automaton, gap)` data realizes feedback ≈0.9998, so
**no a-priori bound `Inj(k)≤F(ρ,γ)` from contraction+automaton alone can exist.** Irreducible open lemma: for each odd a,
`(1/N)Σ(β_n−½)χ_a(⌊3s_n/2⌋ mod 2^k) → 0` (= (K)/Mahler). Side results: a conditional bound (even-defect ≤ contraction ·
odd-defect) [PROVEN], and the exact-identity reframing.

### 7.3 Annealed partials → `ANNEALED_PARTIAL_BANKED.md` — banked, all constants reproduced (exact big-int, <1s)
Tightest unconditional result: **`#even(n) ≥ 0.89 log n`** (the only quantitative count for the specified orbit; gap to H₂ =
the whole `log n → εn` factor). Constant `C=√2·ν̂_{2/3}(1/8)=0.774846171700205…` exact; mean D=2.006→2; Φ slope →ln2,
power a→1.71 (OBSERVED). No soundness incident (one verifier wobble was an mpmath-dps artifact, fixed; data intact).

### 7.4 Empty-toolbox question → `EMPTY_TOOLBOX_QUESTION.md` — **empty-toolbox CONFIRMED** (HIGH ~85%)
No field has *specified-orbit* (not a.e., not extremal) genericity for a rank-1 amenable hyperbolic system. Nearest:
Algom–Baker–Shmerkin (Adv. Math. 2022; exposition Algom arXiv:2504.18192) = a.e.-in-support normal. Dynamical near-miss BFLM
(JAMS 2011) = single-orbit torus equidistribution but **non-abelian** semigroup — fails precisely on amenability. New bridge
found: Eliahou–Verger-Gaugry arXiv:2504.13716 (base-3/2 number system ↔ 3x+1; structural, no density theorem). Verdict: new
math, framed as a *missing descent bridge* from a.e./homogeneous equidistribution to one computable trajectory.
**Citation fix banked:** arXiv:2504.18192 is Algom solo (exposition), NOT "Algom-Baker-Shmerkin"; AEV =
Andrieu–Eliahou–Vivion arXiv:2510.11723 (confirmed).

### 7.5 The sharpened new-math spec (what §7.2 changes)
The endogenous-UE no-go converts the §5 spec from "we lack a derandomization principle" into a **precise operator-level
requirement**: the spectral gap lives in the **even** subspace, but the obstruction (K) lives in the **odd** subspace that
the annealed operator **provably annihilates** (`L_ann χ_odd ≡ 0`). Therefore **the new theorem cannot come from the
annealed contraction at all** — no amount of mixing/gap touches the odd block. The required tool must inject control into the
**odd-character subspace by a non-spectral mechanism** (the odd block carries the self-reference; the gap is structurally
blind to it). This is strictly sharper than "derandomize Haar onto one orbit": it names *which subspace* the new mechanism
must act on and proves the *existing* mechanism cannot reach it.

**Session net:** 4 routes addressed; hybrid #1 closed (tautology, dimension count); the new-math build produced a sharp
no-go that pinpoints the odd-character subspace as the irreducible target; annealed partials banked; empty-toolbox confirmed
with corrected citations. (K) still [OPEN] = Mahler 3/2 / AEV. Zero false proofs; no label upgraded.
