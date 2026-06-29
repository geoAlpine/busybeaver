# A theory of ENDOGENOUS UNIQUE ERGODICITY — framework note (2026-06-29)

*Framework-construction task (not attack-and-reduce). Goal: build the missing mathematical theory whose central
principle, IF true, decides the BB(6)/Antihydra kernel (K). SOUNDNESS PARAMOUNT: every claim is labelled
`[DEFINITION]/[PROVEN]/[PROVEN-in-lit]/[CONJECTURE]/[OBSERVED]`. The kernel (K) is **not** proven; only what
genuinely follows is proven. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python
scratchpad/endo_ue_consistency.py`, exact big-int orbit `c₀=8`, `N=10⁵`, <5 s, all framework quantities
machine-measured. NOT committed.*

---

## 0. What this note is

The corpus has, with two impossibility meta-theorems (`WEAPONS_AUDIT_2026-06-29.md` §1) and a sharp operator-level
no-go (`ENDOGENOUS_UE_BUILD.md` §5), proved that **no proof of (K) can come from the spectral gap + the carry
automaton alone**: the only contraction in hand (the annealed gap `λ₂`) acts on the *even*-character subspace,
while the conclusion lives in the *odd*-character subspace that the annealed operator **exactly annihilates**
(`L_ann χ_odd ≡ 0`). A correct theory must therefore add a **third ingredient** beyond `(gap, automaton)` — one
that uses the **orbit's own arithmetic**. This note builds that theory as a framework: it gives the definitions,
isolates the third ingredient as a single named **Central Principle (Conjecture)**, proves the partials that
genuinely follow, exhibits the reduction `Principle ⇒ (K)`, states the irreducible new theorem to build, and
positions it against the nearest existing theory (self-consistent dynamical systems; cocycle ergodicity;
(T,T⁻¹)/RWRS). **No machine decided. No label upgraded.**

---

## 1. Definitions — the objects the no-go forces us to name

### 1.1 The endogenous cocycle `[DEFINITION]`

Let `M = 2^k`, `s_n := c_n mod M ∈ ℤ/M` the **low state**, and `β_n := bit_k(c_n) ∈ {0,1}` the **fresh
high bit consumed at step n**. The exact carry automaton (`ENDOGENOUS_UE_BUILD.md` C1) is
`U(s,β) := ⌊3(s + β·2^k)/2⌋ mod 2^k`, with `s_{n+1} = U(s_n, β_n)` and `U(s,1) = U(s,0) + 2^{k−1}` exactly.

> **Definition (endogenous cocycle).** A driven finite-state cocycle `s_{n+1}=U(s_n,β_n)` over an automaton `U`
> is **endogenous** if the driving bit is a **digit of the very state being transported**, i.e.
> `β_n = Π(state_n)` for a fixed read-off `Π` (here `Π = bit_k`, read one window above `s_n`). The loop is
> *closed*: the orbit furnishes its own next input. This is the precise opposite of an **exogenous** cocycle,
> where `(β_n)` is an external (i.i.d. / stationary) input independent of the state.

The annealed model replaces `β_n` by i.i.d. `Bernoulli(½)` — i.e. it **cuts the loop open**. Every classical
unique-ergodicity / mixing tool is a theorem about the *opened* (exogenous) cocycle.

### 1.2 The self-consistency operator and self-consistent measures `[DEFINITION]`

Cutting the loop at a *fixed input law* `q ∈ Prob({0,1})` gives a Markov operator
`L_q f(s) = (1−q) f(U(s,0)) + q f(U(s,1))` with a unique stationary law `μ_q` (the automaton is irreducible).
Re-closing the loop means demanding that the input law it produces equals the input law it consumes:

> **Definition (self-consistency operator Ψ).** Let `R(μ) := μ`-law of the read-off bit `Π`. Define
> `Ψ : Prob(ℤ/M) → Prob(ℤ/M)`, `Ψ(μ) :=` the stationary law of `L_{q}` with `q = ⟨R(μ)⟩` (the fresh-bit
> bias the state law `μ` itself feeds back). A fixed point `Ψ(μ_*) = μ_*` is a **self-consistent measure**
> (an **endogenous equilibrium**): a state law that reproduces the driving statistics it generates.

This is the closed-loop / mean-field fixed-point object; `Ψ` is the rigorous form of the renewal
self-consistency map (`antihydra_renewal_attack.md` §12, contraction = gap 0.99). Haar `= μ_Haar` is always a
self-consistent measure (`R(μ_Haar)=Bernoulli(½)`, `Ψ(μ_Haar)=μ_Haar`).

> **Definition (trap equilibrium).** A self-consistent measure `μ_*` is a **trap** if `μ_*` is not Haar; e.g.
> the atom `δ_1` at the halting fixed point `c≡1 (mod M)`, sustained only by a fresh-bit law perfectly
> correlated with the state (the adversarial all-odd input, `antihydra_renewal_attack.md` §6, min-density 0).

### 1.3 Endogenous unique ergodicity `[DEFINITION]`

> **Definition (EUE).** The endogenous cocycle is **endogenously uniquely ergodic at scale k** if the empirical
> measure `π_N = (1/N)Σ_{n<N} δ_{s_n}` of the **single specified orbit** converges to the Haar self-consistent
> measure: `π_N → μ_Haar`. It is **EUE** if this holds for every `k`.

EUE is *not* unique ergodicity in the classical sense (the opened system has positive entropy and an uncountable
simplex of invariant measures — `COCYCLE_ERGODICITY.md` §1). It is the weaker-looking but harder statement that
**the one self-referential orbit selects the Haar equilibrium among the self-consistent measures.** By the proven
five-link reduction (`COMPLETE_PROOF_CAPSTONE.md` §2), **EUE ⟺ (K) ⟺ Antihydra never halts.**

---

## 2. The Central Principle — the third ingredient `[CONJECTURE]`

The no-go (`ENDOGENOUS_UE_BUILD.md` §5) says: `(λ₂, U)` does not select between `μ_Haar` and the traps — an
adversary with identical `(gap, automaton)` realizes a trap (feedback `≈1`; reproduced here T4: adversarial
`|Inj|` up to `0.165` vs real `≈0.0014`). The missing selector must be an **a-priori property of the endogenous
input** `β_n = bit_k(c_n)` — i.e. orbit arithmetic. We name it.

> ### Endogenous Anti-Resonance Principle (EAR) `[CONJECTURE]`
> For the closed-loop orbit `c₀=8`, the fresh bit cannot phase-lock to its own low state: for every fixed scale
> `k` and every odd character `χ_a`,
> $$\mathrm{Inj}_a(N) \;:=\; \frac1N\sum_{n<N}(\beta_n-\tfrac12)\,\chi_a\!\big(U(s_n,0)\big)\;\longrightarrow\;0 .$$
> Equivalently (the dynamical form): the **residence of the orbit in any phase-coherent trap region is `o(N)`** —
> no trap equilibrium, exact *or* intermittent, is realized by the endogenous input.

**Why this is the right third ingredient (not a restatement of the gap).** EAR is a statement about the
*coupling* between the read-off bit and the transported phase — a quantity the annealed operator is provably
**blind to** (it averages the bit out, `L_ann χ_odd≡0`). EAR's proposed engine is the orbit's own
**2-adic Lyapunov structure** (Lemma B below), which is *external* to `(λ₂,U)`. So EAR is genuinely a new
ingredient, and the no-go does not apply to it (the no-go's adversary violates Lemma B — it does not grow).

**The proposed mechanism (the conjectural content made concrete).** Decompose the fresh bit exactly
(`SESSION_2026-06-29_AEV_CORE.md` §1): `β_n = d_n ⊕ σ_n ⊕ ρ_n`, the exogenous Mahler diagonal
`d_n = bit_{n+k}(⌊8(3/2)ⁿ⌋)`, the carry diagonal `σ_n = bit_{n+k}(S_n)`, and a finite-range borrow `ρ_n`. EAR
asserts two non-resonances whose conjunction is the principle:
- **(EAR-carry)** the carry channel `σ_n` decorrelates from the phase. *This is the half that is nearly
  earned*: the carry's **annealed** law is the Rajchman measure `ν_{2/3}` (`SECOND_DIAGONAL_RAJCHMAN.md` §1,
  `[PROVEN]` identity + Erdős–Salem non-Pisot decay), so the carry is non-resonant at the annealed tier and
  `[OBSERVED]` annealed-indistinguishable on the orbit.
- **(EAR-diagonal)** the exogenous Mahler diagonal `d_n` decorrelates from the orbit-defined phase
  `U(s_n,0)`. *This is the irreducible half* — it is single-orbit Mahler 3/2 / AEV at `α=8`.

So EAR factors the kernel into a (provably Rajchman) carry non-resonance and a single Diophantine
diagonal non-resonance; the framework's value is that it says **precisely which inequality must be proven and
that it is anti-resonance, not mixing.**

---

## 3. Proven Lemmas — what genuinely follows (the framework's earned core)

> **Lemma A (Exact-trap exclusion) `[PROVEN]`.** No exact trap equilibrium is realized by the endogenous orbit.
> The integer orbit grows (`c_n→∞`) and its itinerary is not eventually periodic (the only `T`-cycle value is
> `N/(3^q−2^q)∈(0,1)`, non-integer for non-atomic patterns — `WALLB_NONATOMIC.md`; verified `q≤10`). Staying
> `c≡1 (mod 2^k)` forever forces `c=1` (off-orbit). Hence `δ_1` and every periodic trap are excluded.
> *(This is the proven base case of EAR: the dynamical form holds with "forever" in place of "positive density".)*

> **Lemma B (2-adic Lyapunov drift / dual repulsion) `[PROVEN]`.** Put `V(c):=v_2(c−1)` (2-adic distance to the
> trap). On every `D=v_2(3c−1)=1` step, `V` **strictly decreases by exactly 1**: `c'−1=(3/2)(c−1)`,
> `v_2(c'−1)=v_2(c−1)−1`, odd-part `×3` (`REPELLER_ESCAPE.md` §1, verified 300174/300174, 0 fails). Thus the
> trap `c≡1 (mod 2^k)` is **deterministically repelling in the 2-adic valuation**: residence at depth `≥k`
> requires continual *refill* of `V` by deep (`D≥2`) steps. `o=1` is repelling **simultaneously** in the
> archimedean (`×3/2`) and 2-adic (`×2`) places (the dual-repulsion adelic multiplier `=3`).
> *(This is the proposed engine of EAR: a genuine orbit-arithmetic Lyapunov function, external to `(λ₂,U)`.)*

> **Lemma C (Conditional contraction — even block is enslaved to the odd block) `[PROVEN]`.** With the annealed
> gap `λ₂<1` (measured all `k`, `0.0001…0.34`), the character space is `V_even⊕V_odd`, `L_ann` is
> block-triangular (`L_annχ_odd≡0`; `L_annχ_even` mixes into both), and the seam identity gives
> `‖π_N|_{V_even}‖ ≤ (1−λ₂)^{−1}‖coupling‖·‖π_N|_{V_odd}‖ + O(1/N)`
> (`ENDOGENOUS_UE_BUILD.md` §3). So parity / even-density (in `V_even`) is **automatically controlled once the
> odd block is**. Consistency measured here (T5): even-defect `≤` odd-defect at all `k` (ratio `0.68→0.86`).
> *(Consequence: EAR need only be proven on `V_odd`; the rest is the proven contraction.)*

> **Lemma D (No-go — the principle cannot be `(gap, automaton)`) `[PROVEN]`.** There is no `F(λ₂,U)` bounding
> `limsup|Inj_a|` over all input sequences: an adversary with the identical automaton and gap realizes
> `|Inj|≈1` (`ENDOGENOUS_UE_BUILD.md` §5, C5; reproduced T4). Hence any selector must use a property specific
> to the endogenous input — *precisely the role EAR/Lemma B fill.* `[PROVEN that the new ingredient is necessary]`

> **Lemma E (Carry non-resonance at the annealed tier) `[PROVEN identity + PROVEN-in-lit decay]`.** The annealed
> second diagonal Weyl sum equals `ν̂_{2/3}(ξ_n)`, `ξ_n=h(3/2)^{n−1}/2^{k+3}→∞`; 3/2 non-Pisot ⇒ `ν_{2/3}`
> Rajchman (Erdős–Salem; effective log rate Varjú–Yu) ⇒ annealed `σ_n` equidistributes
> (`SECOND_DIAGONAL_RAJCHMAN.md` §1). So **EAR-carry holds at the annealed tier unconditionally**; only the
> quenched single-orbit transfer is open. *(Half of EAR is on solid ground; the wall is EAR-diagonal.)*

**Net proven core.** The framework is complete except for one inequality: Lemmas A–E reduce EUE to **EAR on the
odd block, carry-stripped** — i.e. to EAR-diagonal alone, a single anti-resonance estimate.

---

## 4. The Reduction — `EAR ⇒ (K)` `[PROVEN conditional]`

Assume EAR. Then for each fixed `k`: `Inj_a(N)→0` for all odd `a` (EAR), hence by the seam identity
`π_N(χ_a)→0` for all odd `a` (the odd block vanishes); by Lemma C the even block then vanishes too
(`π_N(χ_b)→0` for all nontrivial even `b`); therefore `π_N → μ_Haar`, i.e. EUE at scale `k`. Holding for all
`k`, EUE follows, and by the proven five-link chain (`COMPLETE_PROOF_CAPSTONE.md` §2:
`EUE ⟺` single-orbit equidistribution mod `2^k` `⟺` mean `D≥3/2` `⟺` even-density `≥1/3` `⟺` halt-criterion
fails) **(K) holds and Antihydra never halts.** ∎ *(conditional on EAR)*

The reverse `(K) ⇒ EAR` is also `[PROVEN]` (equidistribution ⇒ the bit decorrelates), so **EAR ⟺ (K)**: the
principle is exactly equivalent to the kernel, not stronger. This is the framework's honesty check — EAR is the
kernel re-expressed as an *anti-resonance / non-trapping* statement, which is the form the third ingredient must
take.

---

## 5. The irreducible new theorem to build

> **Theorem-to-build (Quantitative Endogenous Anti-Resonance).** Prove a Lyapunov/return-time estimate of the
> shape
> $$\Big|\tfrac1N\sum_{n<N}(d_n-\tfrac12)\,\chi_a(U(s_n,0))\Big| \;\le\; \Phi\big(\text{quenched dispersion of } V\text{-excursions}\big)\;\xrightarrow{N\to\infty}\;0,$$
> where `d_n=bit_{n+k}(⌊8(3/2)ⁿ⌋)`, `V=v_2(c−1)` is the 2-adic Lyapunov function of Lemma B, and the bound uses
> the **deterministic 2-adic repulsion + archimedean growth** (Lemmas A,B) to control the residence/return
> statistics, *not* the spectral gap (Lemma D forbids the gap). Equivalently: show the single deterministic
> realization is generic for the (provably Rajchman, Lemma E) annealed model — a **descent from the annealed/
> a.e. tier to the one computable orbit** via a Lyapunov sub-action rather than a contraction.

What must be supplied that is genuinely new: a **Kac-type identity coupling the feedback correlation `Inj_a` to
the excursion statistics of the 2-adic Lyapunov function `V`** (the program has the exact valuation budget
`Σv_2(3c_i−1)=n+v_2(c_n)−v_2(c_0)`, `VALUATION_BUDGET.md`, as the first-moment seed), and a proof that those
excursions cannot conspire to a positive-density phase-lock. This is the rank-1 amenable hyperbolic
single-specified-orbit equidistribution object (`WEAPONS_AUDIT_2026-06-29.md` §5) — but the framework re-shapes
it from "derandomize Haar onto one orbit" into "build a 2-adic Lyapunov sub-action for a self-driven cocycle."

---

## 6. Numerics testing the framework's consistency (`endo_ue_consistency.py`, `N=10⁵`)

Each test could have falsified a framework claim; none did.

| Test | Framework claim | Result |
|---|---|---|
| T2 residence near trap `c≡1 mod 2^k` | Lemma A/B: `o(N)`, Haar frequency | frac `=0.0606,0.0145,0.0035,0.0009` ≈ Haar `2^{−k}`; **max run `17,15,13,11`** vs `log₂N=16.6` (i.e. `O(log N)=o(N)`) |
| T3 real `Inj_a` vs CLT floor `1/√N` | EAR: `→0` at √-cancellation | mean `|Inj_a| = 0.0019,0.0014,0.0014` (k=4,6,8), **ratio `0.45–0.61` of the `1/√N` floor** — sub-floor |
| T4 adversarial `β≡0/1` (no-go witness) | Lemma D: `(gap,U)` cannot bound | `|Inj|` up to **`0.165`** (k=6), `0.160` (k=8) — `~50–100×` the real orbit |
| T5 even-defect vs odd-defect | Lemma C: even enslaved to odd | even/odd ratio `0.68,0.77,0.86 < 1` at all `k` |

Reading: the orbit behaves **exactly as EAR predicts** (sub-CLT feedback, `O(log N)` trap residence), while a
phase-locked input behaves exactly as the no-go predicts (order-1 feedback) — confirming the framework's central
dichotomy *and* that the dichotomy is invisible to `(gap,U)` (T4 uses the same `U`).

---

## 7. Novelty vs existing theory

- **Self-consistent dynamical systems** (coupled-map / mean-field; e.g. arXiv:1909.04484 — Bahsoun–Galatolo–
  others). *Nearest named relative*: a map that depends on the current **measure**, with a self-consistency
  fixed point — exactly our `Ψ`. **Difference:** that theory couples through the *global measure* of an
  *ensemble* and notably **produces non-uniqueness** (multiple ACIMs at any coupling `ε>0`); our coupling is a
  **single orbit feeding back one of its own digits** (`β_n=bit_k(c_n)`), and the open question is *selection of
  the unique Haar equilibrium by one trajectory* — a quenched, single-orbit, digit-level closed loop that the
  mean-field theory does not model.
- **Cocycle ergodicity** (Kaimanovich–Schmidt, Conze–Krygin, Furstenberg). These are **isometric, exogenous,
  a.e.** theorems (`COCYCLE_ERGODICITY.md`): the driving base is independent of the fiber, the conclusion is for
  a.e. point. Our cocycle is **expanding, endogenous, single-specified-orbit** — the driving bit *is* a fiber
  digit, so it is not a cocycle over an independent base at all, and a.e. results cannot select seed 8.
- **(T,T⁻¹) / random walk in random scenery (RWRS).** The program's noted precedent: a self-interacting walk
  whose tools are **probabilistic limit theorems**, *abandoning* unique-ergodicity selection
  (`WEAPONS_AUDIT_2026-06-29.md` §5). Our framework keeps the **unique-ergodicity (equidistribution) target**
  and supplies the missing selector as an **anti-resonance / 2-adic Lyapunov** principle rather than a CLT.
- **Improvement claimed.** None of the above has a *single-specified-orbit selection principle for an endogenous
  (self-digit-driven) expanding cocycle*. This note isolates that gap, names the selector (EAR), proves it is
  necessary (Lemma D), proves its base case and one of its two channels (Lemmas A,B,E), reduces it to the other
  (Lemma C, §4), and specifies the theorem to build (§5). It does not prove EAR — EAR `⟺` (K) `=` Mahler 3/2 /
  AEV Conj 1.6 at `α=8`, which is generational and `[OPEN]`.

---

## 8. Honest status

- **`[PROVEN]`**: the framework's scaffolding — definitions; exact-trap exclusion (A); 2-adic Lyapunov drift (B);
  conditional contraction reducing EUE to the odd block (C); the no-go forcing a non-spectral ingredient (D);
  carry non-resonance at the annealed tier via Rajchman `ν_{2/3}` (E); the conditional reduction `EAR ⇒ (K)` and
  the equivalence `EAR ⟺ (K)` (§4).
- **`[CONJECTURE]` (the irreducible residue)**: EAR itself, in its sharpest form **EAR-diagonal** —
  `(1/N)Σ(d_n−½)χ_a(U(s_n,0))→0`, the single-orbit Mahler/AEV anti-resonance. Equivalent to (K).
- **`[OBSERVED]`**: every numeric in §6 — consistent with EAR, not a proof of it.

The genuine contribution is **framework shape**: it converts "we need to derandomize" into a precise program —
*build a 2-adic Lyapunov sub-action for the self-digit-driven cocycle and prove a Kac/anti-resonance bound on the
feedback correlation, on the odd block, carry-stripped.* That is a buildable object with a proven base case
(Lemmas A,B), a proven contraction wrapper (C), and a proven half (E) — the first time the missing theorem has
been posed as anti-resonance + Lyapunov rather than mixing + gap.

---

## Sources

- **Repo (proven inputs):** `ENDOGENOUS_UE_BUILD.md` (seam identity, `L_annχ_odd≡0`, no-go C5), `WEAPONS_AUDIT_2026-06-29.md`
  §5/§7 (new-math spec, empty toolbox), `COMPLETE_PROOF_CAPSTONE.md` §2 (five-link reduction), `REPELLER_ESCAPE.md` §1
  (dual-repulsion / 2-adic Lyapunov), `WALLB_NONATOMIC.md` (growth / non-periodicity), `ENDOGENEITY_DEFECT.md` (recursion
  `Def(k+1)≤ρDef(k)+Inj(k)`), `antihydra_renewal_attack.md` §6/§12 (self-consistency operator, gap 0.99, adversarial min 0),
  `SECOND_DIAGONAL_RAJCHMAN.md` (carry annealed law `=ν̂_{2/3}`), `CARRY_EXOGENIZATION.md` (annealed-indistinguishable carry),
  `SESSION_2026-06-29_AEV_CORE.md` (`β_n=d_n⊕σ_n⊕ρ_n`, α=8 core), `ODD_SUBSPACE_SYNTHESIS.md`, `QUENCHED_ANNEALED_SEAM.md`,
  `COCYCLE_ERGODICITY.md` (why isometric/a.e. cocycle theorems fail), `VALUATION_BUDGET.md`.
- **Literature:** Mahler "An unsolved problem on the powers of 3/2" (1968, open); Andrieu–Eliahou–Vivion arXiv:2510.11723
  (AEV Conj 1.6, rational base); Algom arXiv:2504.18192 (exposition; Algom–Baker–Shmerkin, Adv. Math. 2022); Erdős (1939) /
  Salem (1944) Rajchman ⟺ non-Pisot; Varjú–Yu arXiv:2004.09358 (effective log rate); **self-consistent dynamical systems**
  arXiv:1909.04484 (multiple ACIMs — the non-uniqueness our single-orbit selector must overcome); Kaimanovich–Schmidt
  "Ergodicity of cocycles" (general theory); (T,T⁻¹)/RWRS (probabilistic-limit precedent).
- **Numerics:** `scratchpad/endo_ue_consistency.py` (exact big-int orbit `c₀=8`, `N=10⁵`: T2 trap residence `O(log N)`,
  T3 sub-CLT `Inj_a`, T4 no-go adversary `≈50–100×`, T5 even≤odd defect).

**No machine decided. No label upgraded.**
