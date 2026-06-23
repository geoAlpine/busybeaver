# The BB(6) cryptid kernel — a self-contained equidistribution problem

**One-line statement.** Deciding the halting of the Busy-Beaver(6) "cryptids" reduces, by an exact and
machine-verified chain, to a single number-theoretic question: *does the diagonal base-`p` digit of an
exponentially growing `2^a/3^b`-orbit equidistribute?* This note states that question self-containedly, lists
the equivalent forms, and records exactly what is proved and what is open. (Companion derivations:
`antihydra_attack.md`, `antihydra_renewal_attack.md`, `o18_attack.md`, `mahler_equidistribution_attack.md`,
`BB6_OPEN_CORE.md`; all numerics reproducible from the cited scripts.)

## 1. Motivation (Busy Beaver)
`BB(6)` is the maximum number of steps a halting 6-state 2-symbol Turing machine makes from the blank tape.
Computing it exactly requires deciding halting for every 6-state machine. The community has reduced the open
set to ~19 "cryptids." This programme reverse-engineered all 19 against the raw machines and found each one's
halting is governed by one arithmetic event of the following uniform shape.

## 2. The kernel problem
Fix coprime-ish integers via a multiplier `μ = 2^a / 3^b > 1` (the cryptids realise `μ ∈ {3/2, 8/3, 4/3}`).
Let `p` be the *shrinking base*: `p = 3` if `b ≥ 1` with `a` the larger power... concretely
- `μ = 3/2`: numerator orbit `3ⁿ`, shrinking base `p = 2`;
- `μ = 8/3 = 2³/3`, `4/3 = 2²/3`: numerator `8ⁿ` resp `4ⁿ`, shrinking base `p = 3`.

Define the **diagonal digit**
```
δ_n  :=  ⌊ μ^n ⌋  mod p      ( equivalently the n-th base-p digit of the integer numerator μ^n·(den)^n ).
```

> **Kernel Conjecture (equidistribution).** `δ_n` equidistributes over `{0,1,…,p−1}`; quantitatively the
> empirical frequencies converge to `1/p`, with no residue class over-represented along the orbit.

For the Busy-Beaver application one needs only the **weak one-sided form**:

> **Weak form (sufficient to decide the cryptid as NON-HALTING).** Two bounds on the same orbit:
> (i) the digit-`(p−1)` run-length / 2-adic depth `d_n := v_p(μ^n − c₀)`-type quantity satisfies `d_n = o(n)`;
> (ii) the relevant residue is hit with average frequency bounded away from the halting threshold
> (for `μ=3/2`: the orbit `c_{n+1}=⌊3c_n/2⌋, c₀=8` has even-density `> 1/3`, equivalently the renewal jump
> heights average `< 2`).

## 3. Equivalent formulations (all proved equivalent here)
For the flagship case `μ = 3/2`, `c_{n+1} = ⌊3c_n/2⌋`, `c₀ = 8` (the machine "Antihydra"):
1. **Arithmetic (diagonal digit).** `bit_n(3ⁿ) = ⌊(3/2)ⁿ⌋ mod 2` equidistributes (density of 1s `→ ½`).
2. **Dynamical (exact `ℤ₂` endomorphism).** `T(x)=⌊3x/2⌋` is a measure-preserving 2-to-1 **exact** (mixing)
   endomorphism of `ℤ₂` (PROVED: every residue mod `2^k` has exactly two preimages, each branch
   `x=(2y+ε)/3` contracting 2-adic measure by `½`). The conjecture ⟺ the *specific* seed `8 ∈ ℤ` (a Haar-null
   point) is non-exceptional for `T`.
3. **Renewal (jump heights).** The depth `d_n=v₂(c_n−1)` is a renewal process: PROVED to count down
   deterministically (`d≥1 ⇒ d↦d−1`) and to jump at even-steps (`c=2c'`) to `D = v₂(3c'−1)`. The conjecture
   ⟺ the even-subsequence `c'_j` equidistributes mod `2^k` (i.e. `c'_j ≡ 3⁻¹ (mod 2^k)` with density `2^{−k}`).

The `μ=8/3` case ("Erdős cluster", machines o5,o15,o18) is identical with `p=3`, and there `δ_n=2` is exactly
**Erdős's 1979 ternary-digit-of-`2^{m}` event**.

## 4. What is PROVED (unconditional, verified)
- The reduction BB(6)-cryptid `→` kernel, for all 19 machines (mechanism + exact halting predicate).
- `T(x)=⌊3x/2⌋` is a measure-preserving exact endomorphism of `ℤ₂`; the `p=3` analogue `×2^a` on `ℤ_p` is a
  **zero-entropy isometry** (`|2^a|_p=1`), with fixed base-`p` digits **periodic in `n`** (periods `2^{k−1}`
  resp `2·3^{k−1}`).
- The renewal skeleton: deterministic depth countdown + geometric jumps (the only randomness).
- **Robustness:** modelling the incoming high bits as Bernoulli(`q`), the stationary even-density exceeds the
  halting threshold `1/3` for **all** `q ∈ [0.01, 0.99]` — full uniformity is *not* required, only
  non-degeneracy + decorrelation.
- The off-diagonal of the 2-parameter family `(2^a)ⁿ mod (p)^M` (fixed modulus, full period) **cancels
  completely** (complete subgroup / Ramanujan sums); the *averaged*-over-multipliers bound holds
  (Koksma/Weyl-a.e.).

## 5. What is OPEN (the one kernel)
Equidistribution of the **specific** orbit's diagonal digit. Every standard tool controls a generic / averaged
/ fixed slice and fails identically on the specific diagonal:
- van der Corput differencing is **closed** on `μⁿ` (multiplicative recurrence = fixed point) — no
  degree reduction;
- the modulus moves with the index (`3ⁿ mod 2ⁿ`), so fixed-modulus sum-product (`|H|≥q^δ`) sees only a
  `log`-size set — exponentially below threshold;
- `(×2,×3)` measure rigidity (Furstenberg/Rudolph/Host/BLMV) needs an invariant positive-entropy measure,
  which a single zero-entropy orbit does not furnish;
- the orbit self-clusters at scale `1/N²`, defeating the large sieve that would upgrade the mean-square bound.

This is the same class as named open problems: **Mahler's 3/2 problem (1968)** and **Erdős's
ternary-digit-of-`2ⁿ` problem (1979)**. A breakthrough on the kernel — even the weak one-sided averaged form
(`avg jump height < 2`, or `depth = o(n)`) for *one* `μ` — would decide an entire cryptid cluster and is the
single missing ingredient for the corresponding part of `BB(6)`.

## 6. The cleanest open statement (for a number theorist)
> Let `c₀ = 8`, `c_{n+1} = ⌊3c_n/2⌋`. At each `n` with `c_n` even write `c_n = 2c'`. Prove that the
> subsequence `(c')` does not satisfy `c' ≡ 3⁻¹ (mod 2^k)` with density exceeding `2^{−k}` (equivalently:
> the renewal jump heights `v₂(3c'−1)` average below `2`). This single bound proves Antihydra never halts,
> deciding one Busy-Beaver(6) cryptid.
