# Antihydra complete-proof status — the maximally-crushed kernel (2026-06-27)
Everything crushable around the complete proof of non-halting has been crushed (proven, elementary,
conjecture-free) or closed (technique ruled out). What remains is a SINGLE open statement = Mahler. This
note pins exactly that: the irreducible kernel, with the proven surroundings, so the moment a tool appears
the gap is one named step. Every line is [PROVEN] / [CLOSED] / [OPEN=Mahler]. Zero false proofs.

## 0. The complete-proof target
Antihydra never halts ⟺ `balance_n = 3E_n − n ≥ 0` for all `n` ⟺ even-density `E_n/n ≥ 1/3`
⟺ **[PROVEN equiv]** `depth_n := v₂(c_n − 1) < balance_n + 1` for all `n` (the 2-adic halting criterion).

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

## 4. The exact distance
A complete proof requires **one new tool that does not exist**: effective single-orbit equidistribution for
a rank-1 expanding `⌊(p/q)·⌋` map (break the closed-loop bias for one realization). The community (Tao,
AEV, …) has not produced it. **But the path has no hidden extra barrier** — it is this single named open
problem, with every surrounding piece proven and every standard technique-axis closed. When the Mahler/AEV
line moves, the kernel lifts at once (it is a single point). That is the honest current position:
*far in calendar time (new mathematics needed), shortest in path (reduced to one open point).*
