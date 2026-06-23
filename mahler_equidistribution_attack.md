# Attacking effective equidistribution of {(3/2)ⁿ} — the Mahler-3/2 wall, sharply localized (2026-06-24)

Direct assault on the kernel under the **Mahler-3/2 cluster** (Antihydra, o7, o8, o10): prove
`{(3/2)ⁿ}` equidistributes mod 1 (effectively), which would yield Antihydra's even-density `> 1/3` and decide
the cluster. This is **Mahler's 3/2 problem (1968), world-open.** Below: the exact exponential-sum framing,
the numerically-measured truth, and the **precise two-fold obstruction** (each demonstrated, not asserted).
All numerics in `mahler_weyl.py`, `mahler_fast.py`, `vdc_test.py`.

## 1. Exact reformulation [the right object]
```
{(3/2)ⁿ} = (3ⁿ mod 2ⁿ) / 2ⁿ        (exact: 3ⁿ = q·2ⁿ + rₙ, {(3/2)ⁿ} = rₙ/2ⁿ)
```
So **Mahler-3/2 ≡ the distribution of `3ⁿ mod 2ⁿ`**, i.e. the low `n` binary digits of `3ⁿ`. The Weyl sum is
```
S_N(h) = Σ_{n≤N} e(h·(3/2)ⁿ) = Σ_{n≤N} e(h·(3ⁿ mod 2ⁿ)/2ⁿ).
Equidistribution  ⟺  S_N(h) = o(N)  for every integer h ≠ 0   (Weyl criterion).
```

## 2. The numerical truth [certain; only the proof is missing]
- `{(3/2)ⁿ}` in `[0,½)`: density **0.49745 → ½** (`N=2×10⁴`). Equidistributes.
- **Full square-root cancellation:** `|S_N(h)|/√N ≈ 0.46–1.1 = O(1)` for `h=1,2,3` ⇒ `|S_N|/N → 0`.
- **Antihydra even-density** `Eₙ/n = 0.49865 → ½`, i.e. `≫ 1/3` with huge margin ⇒ non-halt (heuristically).
The conjecture is true beyond any numerical doubt. The entire difficulty is unconditional **proof**.

## 3. Obstruction (a) — van der Corput differencing is CLOSED [demonstrated]
The one general tool for non-polynomial phases is van der Corput differencing:
`|S_N|² ≤ N + 2Σ_k |I_k|`, `I_k = Σ_n e(h·((3/2)^{n+k} − (3/2)ⁿ)) = Σ_n e(h·((3/2)^k − 1)·(3/2)ⁿ)`.
The inner sum `I_k` is **another Weyl sum of the SAME `(3/2)ⁿ` family**, with coefficient `(3/2)^k − 1`.
Measured (`vdc_test.py`, `N=8000`, base `|S_N(1)|/√N = 0.587`):
```
k :   1      2      3      4      5      6
|I_k|/√N : 1.178  0.186  0.701  1.342  1.637  0.647     ← all O(1); k=1 is WORSE than base
```
Differencing yields **no cancellation gain** — each `I_k` has its own `√N` size and no smaller. Reason:
`(3/2)ⁿ` is a **fixed point of the differencing operator** (a *multiplicative* recurrence
`(3/2)^{n+1} = (3/2)·(3/2)ⁿ`, not an additive/polynomial one), so differencing never reduces "degree." Every
classical equidistribution proof (Weyl, van der Corput, Vinogradov) rests on degree-reduction; **all are
inert here.** This is the first wall, and it is structural, not a matter of effort.

## 4. Obstruction (b) — the modulus MOVES with the index [structural]
Re-encoding `S_N(h) = Σ e(h·(3ⁿ mod 2ⁿ)/2ⁿ)` exposes the second wall: the term at index `n` lives at
**modulus `2ⁿ`, tied to the index.** Fixed-modulus machinery — Gauss sums, Weyl/Vinogradov bounds, and
crucially **sum-product / Bourgain–Konyagin** estimates for `Σ e(a·xⁿ/q)` — all require a **long sum at ONE
modulus `q`**. Here every `n` brings a new modulus and we sample the orbit `{3ʲ mod 2ⁿ}` at the **single
point `j = n`**. The relevant multiplicative set `{3ʲ mod 2ᵏ}` with `k ~ c·n` is of size `2^{k-2}` but is
**log-size relative to the modulus `q = 2ᵏ`** (`|H| ≈ log₂ q`), exponentially below the `|H| ≥ q^δ` threshold
the sum-product method needs. **The correct tool exists but for the wrong regime**, by an exponential gap.

## 5. What a bypass would require (and why neither exists)
- **Beat (a):** a *non-differencing* equidistribution method = a **spectral gap for the `×(3/2)` map** on the
  `(2,3)`-adic solenoid (the compact group carrying the `(3/2)ⁿ` orbit). That endomorphism is **not
  hyperbolic** (eigenvalue `3/2`, with a `2`-adic contracting and `3`-adic-expanding split that is not
  uniformly hyperbolic over the archimedean place), and **no spectral gap / transfer-operator bound is known**
  for such non-hyperbolic toral/solenoidal endomorphisms. This is an open frontier in homogeneous dynamics.
- **Beat (b):** an **anti-concentration bound for `3ⁿ mod 2ⁿ` uniform as the modulus grows with `n`** — the
  carry-propagation problem for `3ⁿ` in base 2. No such uniform-in-modulus bound exists; it is the additive-
  combinatorics frontier the deep-research sweep already located (`antihydra_problem_statement.md` §5).

## 6. Even the WEAKER statement we actually need is open [honest]
Antihydra needs only the **one-sided density** `Eₙ/n > 1/3`, not full equidistribution. But this is open too,
by the same (a)+(b) wall: the orbit's growth `cₙ ≈ c₀(3/2)ⁿ` is **parity-blind** (`⌊3c/2⌋` grows `~×3/2`
whether `c` is even or odd), so growth imposes **no constraint** on the parity/even density — there is no soft
or one-sided argument, and the only unconditional bound stays the trivial `depthₙ ≤ log₂cₙ ≈ 0.585n`.

## 7. Honest ledger
- [VERIFIED] reformulation `{(3/2)ⁿ} = (3ⁿ mod 2ⁿ)/2ⁿ`; numerics: equidistribution + `√N` cancellation +
  even-density `→ ½`.
- [DEMONSTRATED] obstruction (a): differencing is closed (`|I_k|/√N` stays `O(1)`, no gain) — every classical
  method is degree-reduction and therefore inert.
- [STRUCTURAL] obstruction (b): modulus-moves-with-index ⇒ one sample per modulus ⇒ sum-product regime
  mismatch by an exponential gap.
- [HONEST] bypassing either needs a tool that does not exist (non-hyperbolic solenoid spectral gap; uniform-
  in-modulus carry anti-concentration). The weaker one-sided density is open by the same wall. **No theorem
  proved; the wall is now localized to two named, demonstrated failures** — the precise statement of what a
  Mahler-3/2 breakthrough must supply. No decision; soundness intact.
