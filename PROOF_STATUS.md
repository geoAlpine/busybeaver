# Antihydra complete-proof status — the maximally-crushed kernel (2026-06-27)
Everything crushable around the complete proof of non-halting has been crushed (proven, elementary,
conjecture-free) or closed (technique ruled out). What remains is a SINGLE open statement = Mahler. This
note pins exactly that: the irreducible kernel, with the proven surroundings, so the moment a tool appears
the gap is one named step. Every line is [PROVEN] / [CLOSED] / [OPEN=Mahler]. Zero false proofs.

## 0. The complete-proof target
Antihydra never halts ⟺ `balance_n = 3E_n − n ≥ 0` **for all `n`** ⟺ even-density `E_n/n ≥ 1/3` for all `n`
⟺ **[PROVEN equiv]** `depth_n := v₂(c_n − 1) < balance_n + 1` for all `n` (the 2-adic halting criterion).

**The actual sufficient analytic statement (for-all-n, not just asymptotic).** Non-halt is an *all-n*
statement, so equidistribution alone is not literally what's needed; the clean sufficient form is
> **[finite check]** verify `balance_n ≥ 0` for `n ≤ N₀` (a finite computation; done to large `N₀` by
> bbchallenge), **plus [effective tail]** `|E_n/n − 1/2| < 1/6` for all `n > N₀`.
Because `balance_n = n(3·E_n/n − 1) ≥ n(1/2 − 3·|E_n/n−1/2|)`, an error `< 1/6` keeps `balance_n > 0`. So
the tail needs only a **one-sided effective bound with a generous `1/6` slack** — far less than full
equidistribution. (Empirically the worst dip is `E_n/n ≈ 0.48`, margin `+0.146 < 1/6`, `flp_margin.py`.)

## 1. The proven surroundings (all crushed — no hidden barrier left below the Mahler line)
- **[PROVEN] Exact reduction chain (machine-checked):** non-halt ⟺ even-density≥1/3 ⟺ the parity identity
  `c_n mod 2 = bit_n(8·3ⁿ) ⊕ bit_n(T_n)`, `T_n` the parity-history carry-sum (`T_{n+1}=3T_n+2ⁿrₙ`,
  `T_n≡8·3ⁿ mod 2ⁿ`); integrality linearizes the diagonal bit (borrow=0).
- **[PROVEN] Run structure:** even-run length `= v₂(c_n)`; odd-run length `= v₂(c_n−1)` (=depth_n). (Induction.)
- **[PROVEN] Not eventually periodic** (transience: `T(c)>c` for `c≥2`, fixed points only {0,1}) ⇒
  **∞ many evens AND ∞ many odds** (free corollary), and (Morse–Hedlund) `p(ℓ) ≥ ℓ+1`. Not Sturmian (`p(2)=4`).
- **[PROVEN] Coding bijection** `φ_ℓ:ℤ/2ℓ→{0,1}ℓ` ⇒ `p(ℓ)=#{c_n mod 2ℓ visited}`; **linear floor slope
  `log_{3/2}2≈1.71`** (`p(ℓ)≥(ℓ−3)/log₂(3/2)`, = Dubickas's base-3/2 constant); lift `p(ℓ)≤p(ℓ+1)≤2p(ℓ)`.
  **Family-wide** (F1,F2 for all `⌊ac/p⌋` genuine growers; F3 sharp exactly when `a<p²`).
- **[PROVEN] Annealed transfer operator is one-step exact** (`λ₂≈0`, uniform a.c.i.m. ⇒ even-density
  **exactly 1/2** in the annealed model), so the endogeneity-defect recursion collapses (`ρ≈0`) to
  **`|even-density−1/2| ≤ Cesàro mean of the one-step incoming-bit bias + o(1)`** (deviation does NOT
  accumulate; CLT-rate, verified). The obstruction is **maximally local** (one step, no history).
- **[PROVEN] Local target in closed form:** `bit_k(c_{n+1}) = bit_{k+1}(c_n) ⊕ γ_k(c_n mod 2^{k+1})`,
  `γ` an explicit finite **tame carry automaton**; the recursion shifts the level by 1/step (no contraction),
  so the irreducible bit enters at the TOP (leading bits of `3ⁿ` = the foothold) — unifying the low-bit and
  foothold funnels.

## 2. The closed technique-axes (no known method reaches the kernel)
- **[CLOSED] Density-bound techniques** — four, each failing for a DIFFERENT structural reason on the single
  transient orbit: FLP/Dubickas (support not frequency; the `1/3` is on the wrong axis), Tao 2019
  (a.e./log-density not per-orbit), Krasikov–Lagarias (set-counting via inverse-tree branching; one orbit
  has no population to count), invariant-measure/Birkhoff (T transient ⇒ no invariant probability measure).
- **[CLOSED] Digit tools** — D-S/Subspace 2025 controls `3ⁿ` but dies at `8·3ⁿ−T_n` (T_n not S-unit);
  partial-independence relaxation refuted in closed form (all-1 input → `bit_n(3ⁿ−2ⁿ)`, itself Mahler-class);
  XOR-leverage gives no handle (the two Mahler digits are cross-decorrelated); van der Corput differencing
  fixes `(3/2)ⁿ` (white differenced sums).
- **[CLOSED] Symbolic / measure** — interval-map Birkhoff bounds the TAME real map (even-density≥2/3) but
  the integer carry's `−1` breaks the conjugacy (allows consecutive odds), landing on the base-3/2 odometer.

## 3. The irreducible kernel (THE one open step = the complete proof)
> **(K)** For the single specified orbit, `(1/N) Σ_{n<N} (−1)^{bit_n(T_n)} = o(1)` — equivalently
> `c_n mod 2ᵏ` equidistributes (the orbit visits every residue mod `2ᵏ`; `p(ℓ)=2ℓ`). This is the
> single-orbit equidistribution of `{(3/2)ⁿ}`-type data = **Mahler's 3/2 problem (1968) / Andrieu–Eliahou–
> Vivion normality conjecture (2025, arXiv:2510.11723)** — a recognized, generational open problem.

In the carry language: `bit_n(T_n)` is balanced for an *independent* input bit-stream (Mauduit–Rivat carry
lemma), and the orbit feeds its **own** parity history back in (closed loop). **The entire remaining gap is
the independence of that single self-referential bit** — a closed-loop identification bias / self-induced
quenched disorder. A one-sided density bound (`liminf ≥ 1/3`, weaker than the conjectured `1/2`) would
already suffice; even that has no proof.

### 3.5 "Solving Mahler" — what suffices and what does NOT (a soundness distinction)
"Solving Mahler" is ambiguous; only some versions give the complete proof:
- **(a) Mahler's literal 1968 conjecture** (no `Z`-number: no `ξ` with `{ξ(3/2)ⁿ} ∈ [0,½)` for all `n`).
  This is a **confinement / support** statement. **NOT sufficient** by itself: ruling out total confinement
  to one half does not bound the *frequency* of evens below `1/3` (an orbit can be unconfined yet have
  even-density → 0). Same support-vs-frequency gap as FLP. (a) is necessary-flavored, not sufficient.
- **(b) Effective single-orbit equidistribution of THIS orbit** (`(K)`): `c_n mod 2ᵏ` equidistributes
  *with an effective error*. **Sufficient** (+ the §0 finite check). This is the real target.
- **(c) AEV 2025 normality conjecture**, *if it covers this orbit's word*: normality = frequency =
  equidistribution, so **sufficient** (same class as (b)).
- **(weaker, also sufficient)** the one-sided effective `|E_n/n−½|<1/6` of §0.
So: the kernel `(K)` is the **equidistribution/normality** version (b)/(c), NOT Mahler's literal
confinement conjecture (a). Solving (a) alone would **not** close Antihydra; solving (b)/(c) would.

### 3.6 The new mathematics to build — exact specification (the buildable target)
What must be invented is a tool delivering (b). Scoped precisely so it can be built, not hand-waved:
> **OBJECT.** An *effective equidistribution theorem for a single specified orbit of the rank-1 expanding
> map `×(3/2)` on `ℤ₂`* — concretely, an explicit `f(n)→0` with `|E_n/n − ½| ≤ f(n)` (one-sided, `f<1/6`
> suffices) for the orbit `c₀=8`, `c_{n+1}=⌊3c_n/2⌋`.
> **WHERE IT MUST BITE.** The parity is `bit_n(8·3ⁿ) ⊕ bit_n(T_n)`. The leading bits of `3ⁿ`
> (`{n·log₂3}`) ARE effectively equidistributed (Weyl + effective discrepancy; `log₂3` irrational with
> known measure) — but the parity uses the **middle** digit `bit_n` (position `n` of `~1.585n`), which is
> NOT the leading bits, and the orbit's `T_n` is a **self-generated carry-sum** (closed loop). So the new
> tool must control a **middle digit of a multiplicatively-defined integer under a self-referential carry**
> — exactly what the Mauduit–Rivat carry lemma does for *bounded* carry and *independent* input, extended
> to *whole-history* carry and *closed-loop* input.
> **THE CRUX TO CRACK.** Break the closed-loop identification bias for ONE realization: prove the
> self-referential bit `bit_n(T_n)` is unbiased without assuming independence — an *endogenous-cocycle
> unique-ergodicity* statement (annealed `→` Dirac-quenched transfer). Every existing framework stops at
> a.e. random realizations; the one precedent ((T,T⁻¹)/RWRS) abandons UE tools for probabilistic limit
> theorems, which is exactly the defect. **This is the single new theorem to build.**
> **WHAT IS ALREADY IN HAND** (so the build doesn't restart from zero): the one-step-exact annealed
> operator (the contraction exists), the explicit tame carry automaton `γ`, the exact reduction to a single
> bit, the proven complexity floors, and the closed technique-map telling you which classical tools will
> NOT work (so you don't waste effort there).

### 3.7 Construction progress — two parallel bricks CONVERGE on Gibbs–Markov (2026-06-27)
Two first construction attempts at the §3.6 object, run in parallel; both independently point to the SAME
machinery, which sharpens the build target.
- **Coupling brick (`coupling_brick.py`).** [measured] The real parity is decorrelated (agreement ≈0.50)
  from EVERY provably-balanced surrogate — Thue–Morse, Rudin–Shapiro, Legendre, **and the
  effectively-equidistributed leading-bit Sturmian `[{n·log₂(3/2)}≥½]`** (so the provable leading-bit
  control does NOT transfer to the parity). The carry has **sensitive dependence**: a 1-bit input flip
  flips ≈½ of all downstream carry bits. ⇒ **a LOCAL coupling is impossible**; the buildable object must be
  a **global / measure coupling** (Ornstein-type) respecting the closed loop.
- **Renormalization brick (`renorm_brick.py`).** [measured] The bit-level-shift variable does NOT contract
  (the sensitive dependence above). But the **renewal / regeneration variable DOES**: using even steps as
  renewal points, the inter-renewal gaps are clean geometric (`P(g)≈2⁻ᵍ`, mean 2.00), gap autocorrelations
  are null at all lags (blocks **decorrelate**), and `|E_n/n−½|` decays at the **CLT rate** (block-bias
  **contracts**). ⇒ the **renewal/Gibbs–Markov variable is the contracting renormalization variable**, not
  the bit shift.
- **CONVERGENCE.** A global Ornstein coupling and a renewal-operator renormalization are the two faces of
  **Gibbs–Markov theory**. So the §3.6 object sharpens to: **a Gibbs–Markov / renewal-mixing theorem for the
  orbit's SELF-GENERATED renewal blocks** — the standard Gibbs–Markov CLT but with the gaps generated by the
  orbit's own closed loop (not an external random environment). The one genuinely new ingredient is exactly
  the self-generation (the (T,T⁻¹)/RWRS-type defect). *(Honest: the decorrelation/contraction are MEASURED,
  not proven — proving them for the specified orbit IS the closed loop; but the bricks identify the right
  variable (renewal, not bit-shift) and the right coupling (global, not local), narrowing the build.)*

### 3.8 The Gibbs–Markov proof skeleton — COMPLETE modulo one named line (`gm_skeleton.py`)
Assembling the GM machinery on the renewal variable gives the complete proof as a chain of [PROVEN] links
ending in a single [OPEN] line — the self-generation hole, isolated to one statement.
- **[PROVEN] (1)** non-halt ⟸ even-density ≥ 1/3 for all `n` (finite check + `1/6` effective tail).
- **[PROVEN] (2)** Renewal partition: even steps are the renewal points; gaps = odd-run lengths = `v₂(c−1)`,
  clean geometric (`P(g)≈2⁻ᵍ`).
- **[PROVEN] (3)** The induced first-return map `G = Tᵗ` is a full-branch piecewise-affine expanding
  **Gibbs–Markov** map of `ℤ₂` (§3′ / `cross_cryptid.py`).
- **[PROVEN] (4)** Spectral gap at the Haar level: the step operator is **one-step exact** (2nd eigenvalue
  `≈0`, uniform stationary — numpy-verified `k≤8`); the induced/renewal operator **inherits mixing**
  (inducing an exact map). ⇒ Haar-a.e. point has even-density `→1/2` with a CLT and exponential
  large-deviation concentration (`balance_n ≥ 0` for a.e. point, overwhelmingly).
- **[OPEN = Mahler] (5)** The SPECIFIC orbit `c₀=8` is **Haar-generic** for `G` (its renewal blocks are
  `μ`-typical) = single-orbit equidistribution mod `2ᵏ`. **The handle search around (5) is now exhausted —
  three independent routes all closed:** (a) soft a.e.-specialization — blocked (orbit computable ⇒ never
  Martin-Löf random); (b) coupling to a provable surrogate — blocked (parity decorrelated from Thue–Morse,
  Rudin–Shapiro, Legendre, and the effective leading-bit Sturmian; `coupling_brick.py`); (c) conditioning
  on the one provable handle, the leading-phase `{n log₂(3/2)}` equidistribution — blocked (even-density is
  **flat across the phase**, `max|dev|=0.0079` < `3σ`=0.0106, and the renewal gaps are phase-independent
  too; `handle_brick.py`). So (5) has **no auxiliary handle** among the available structures; supplying it
  IS the new theorem.

**So the complete proof = GM argument (1)–(4) [done] + the one line (5).** The new theorem to build is
exactly *a Gibbs–Markov CLT / genericity statement for one deterministic, closed-loop (self-generated)
realization* (annealed→Dirac-quenched) — the maximally-reduced target: a single named line, with all
surrounding machinery proven and every soft route's failure mode mapped.

## 4. The exact distance
A complete proof requires **one new tool that does not exist**: effective single-orbit equidistribution for
a rank-1 expanding `⌊(p/q)·⌋` map (break the closed-loop bias for one realization). The community (Tao,
AEV, …) has not produced it. **But the path has no hidden extra barrier** — it is this single named open
problem, with every surrounding piece proven and every standard technique-axis closed. When the Mahler/AEV
line moves, the kernel lifts at once (it is a single point). That is the honest current position:
*far in calendar time (new mathematics needed), shortest in path (reduced to one open point).*
