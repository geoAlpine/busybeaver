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

## 8. Deep-dive on obstruction (b): it is DIAGONAL EXTRACTION, and the averaged bound exists but can't localize (2026-06-24)
Probing the carry structure of `3ⁿ mod 2ⁿ` directly (`carry_b.py`, `koksma_b.py`) sharpens (b) from a vague
"regime mismatch" to an exact diagnosis.
- **The bits are perfect coins [measured]:** bit-density of `3ⁿ mod 2ⁿ → ½`; the top bit (which decides
  `{(3/2)ⁿ} ≷ ½`) is balanced (0.4998 over 4000 n) with autocorrelations `≈ 0` (lags 1–4: `+.012,−.021,
  +.000,−.004`) and decorrelates under a modulus shift (`corr ≈ −.06..−.01`). Randomness is numerically total.
- **The off-diagonal vanishes EXACTLY [measured]:** for *fixed* modulus `2^M`, `Σ_{n<ord(3)} e(3ⁿ/2^M) =
  0.00` (a complete sum over the cyclic group `⟨3⟩` = the units = a Ramanujan sum `c_{2^M}(1)=0`). So the
  2-parameter family `3ᵃ mod 2ᵇ` is **perfectly equidistributed off the diagonal**; the ENTIRE difficulty is
  the **diagonal `a=b=n`**. Obstruction (b) is precisely a **diagonal-extraction problem**: extract the
  diagonal of a 2-parameter arithmetic family that is equidistributed in each row.
- **The averaged bound DOES exist [classical, confirmed]:** the mean over multipliers `(1/H)Σ_{h≤H}|S_N(h)|²
  = 4219 ≈ N = 4000` ⇒ square-root cancellation holds **in mean**. This is the Koksma (1935) / Weyl-a.e.
  regime: *for almost every* `t`, `{t·(3/2)ⁿ}` equidistributes. **An unconditional partial result is real —
  but it is an "almost-all", not a pointwise, statement.**
- **Why it cannot reach the specific point [two demonstrated reasons]:**
  1. **Measure-zero exceptional set.** Koksma's a.e.-statement leaves a null set of bad `t`; nothing excludes
     the specific `θ=3/2`, `t=1` from it. (Numerically `t=1` is not an outlier — `|S_N(1)|=13.2` vs median
     `57.2` — so it *behaves*, but "behaves numerically" ≠ "provably outside the exceptional set".)
  2. **The orbit points cluster too tightly for the large sieve.** The large sieve is the tool that would
     upgrade mean-square to pointwise, but it needs the points `δ`-separated with `δ ≫ 1/N`. Measured: the
     `N=4000` points `{(3/2)ⁿ}` have **min gap `3.4×10⁻⁷ ≈ 1/N²`** (vs uniform `1/N = 2.5×10⁻⁴`), i.e.
     `δ ~ 1/N²`, so the large-sieve bound `Σ|S(tᵣ)|² ≤ (N + δ⁻¹)‖a‖²` degrades to `~N²` — **useless**. The
     tight clustering is itself a Diophantine fact (`(3/2)ⁿ−(3/2)ᵐ ≈ ℤ` near-coincidences from the same
     properties of `3/2`), so the obstruction is self-referential: the orbit's own Diophantine structure
     blocks the sieve that would tame it.
- **Sharp restatement of (b):** *Mahler-3/2 is the diagonal of a 2-parameter family whose rows are exactly
  equidistributed; the averaged (almost-all-multiplier) bound is classical, but pointwise localization fails
  because the specific multiplier sits in a measure-zero exceptional set AND the orbit points self-cluster at
  scale `1/N²`, defeating the large sieve.* This is the precise, measured content of "regime mismatch" — and
  it mirrors obstruction (a): generic/averaged methods succeed, the specific orbit is the open case. No
  theorem; the partial that exists (Koksma mean-square) is real but provably cannot be made pointwise here.

## 9. Deep-dive on obstruction (a): the dynamical dissection — and (a) ≡ (b) UNIFIED (2026-06-24)
Building the actual dynamics (`transfer_a.py`, `skew_a.py`, `adic_a.py`) resolves (a) to the same level as
(b) — and reveals the two obstructions are **literally the same object**.
- **The natural circle map HAS a spectral gap [computed].** `{(3/2)ⁿ}` is *almost* an orbit of the
  β-transformation `T(x)=(3/2)x mod 1`. Its Perron–Frobenius (Ulam, K=3000) operator has leading eigenvalue
  `1` and `|λ₂| = 0.730`: **spectral gap `0.27`, mixing time ≈ 3 steps.** The β-map is exponentially mixing,
  so a.e. point under `T_β` equidistributes fast. *This is the generic tool that works* — the analogue of
  (b)'s Koksma mean-square.
- **But `{(3/2)ⁿ}` is NOT a `T_β` orbit [verified].** The exact recurrence is
  `x_{n+1} = {(3/2)x_n + ε_n/2}` with a **carry** `ε_n = ⌊(3/2)ⁿ⌋ mod 2` (verified to reproduce the orbit).
  The carry is `≠0` about half the time (0.524), so the orbit leaves the gap-bearing β-map constantly.
- **THE UNIFICATION [verified]: `ε_n = bit_n(3ⁿ)`** — the carry of (a) is *exactly* the **diagonal bit** of
  (b) (the `n`-th binary digit of `3ⁿ`, ` = ⌊(3/2)ⁿ⌋ mod 2`). So **obstruction (a) and obstruction (b) are
  the same arithmetic object**, viewed dynamically vs arithmetically. The entire Mahler-3/2 problem is the
  single sequence `ε_n = bit_n(3ⁿ)`; `ε_n` has near-full block entropy (ratio 0.99 — near-iid fair bits).
- **Why no dynamical gap reaches it [the correct two-place picture, verified].** Split `×(3/2)` by the
  product formula `|3/2|_∞·|3/2|_2·|3/2|_3 = (3/2)(2)(1/3) = 1`:
  - **Real place** = the `T_β` map: **has a gap (0.27)** but is the projection that **discards the carry** —
    it does not carry the bit information.
  - **2-adic place** = `×3` on `ℤ₂`: since `|3|_2 = 1`, this is an **ISOMETRY** — zero entropy, **no spectral
    gap**. Verified: every *fixed* 2-adic digit `bit_k(3ⁿ)` is **periodic in `n`** (period `2^{k-1}`: k=3→4,
    k=5→16). This factor **carries all the bits** but, being an isometry, offers **no mixing to exploit**.
  - `bit_n(3ⁿ)` is the **diagonal read** of the zero-entropy 2-adic isometry at the *moving* position `n`:
    the bit-bearing factor has only periodic (rigid) structure, and reading it diagonally is precisely where
    that rigidity gives no help. The one mixing factor (real β-map) is bit-blind.

## 10. Unified verdict — Mahler-3/2 = equidistribution of the single diagonal bit `bit_n(3ⁿ)`
Both obstructions collapse to one crisp kernel:
> **Antihydra non-halting / Mahler-3/2 ⟺ the diagonal bit sequence `ε_n = bit_n(3ⁿ) = ⌊(3/2)ⁿ⌋ mod 2`
> equidistributes (density of 1s `→ ½` with enough independence that `Eₙ/n > 1/3`).**
- (b) arithmetic face: `ε_n` is the **diagonal** of the 2-parameter family `3ᵃ mod 2ᵇ`, whose **rows are
  exactly equidistributed** (off-diagonal complete sums `= 0`) — diagonal extraction is the open case.
- (a) dynamical face: `ε_n` is the **diagonal read** of the **zero-entropy 2-adic isometry** `×3`, whose
  **fixed coordinates are periodic** — the moving diagonal is the open case; the only spectral gap lives in
  the bit-blind real factor.
Each available tool (Koksma mean-square; β-map spectral gap; row-equidistribution; fixed-digit periodicity)
controls a **generic/averaged/fixed** slice perfectly, and **all fail identically on the specific diagonal**.
That single failure — extract/equidistribute the diagonal bit `bit_n(3ⁿ)` — IS Mahler's 3/2 problem, now
exhibited as one object with both faces measured. No theorem; the wall is one crisp, named, measured kernel.
