# Joint / finite-family structure of the two needed α (α=8 and α*≈0.1358): does it give leverage the single instance lacks? (2026-06-29)

*Assigned angle: the Antihydra non-halt kernel (K) needs equidistribution of BOTH diagonals
`d_n = bit_k(⌊8(3/2)^n⌋)` (α=8) and `σ_n = bit_k(⌊α*(3/2)^n⌋)` (α*=(1/3)Σ b_j(2/3)^j ≈0.1358), via
`β_n = d_n⊕σ_n⊕ρ_n` (ρ finite-range, PROVEN `CARRY_COBOUNDARY §1a`). Two routes: (1) a SECOND-MOMENT /
large-sieve bound over a FINITE family of α (almost-orthogonality across α, not across frequencies);
(2) can INDEPENDENCE of (d_n,σ_n) be PROVEN, reducing (K) to a SINGLE diagonal? Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/two_alpha_joint.py, shift_identity.py`,
exact big-int, N=2·10⁴ (corr/2nd-moment), N=4·10³×8 resonances (identity), <5s each, 0 identity failures.
Every claim labelled. Zero false proofs. NOT committed.*

---

## 0. One-line verdict

**(c) — the joint/finite-family structure gives NO leverage the single instance lacks. NEW `[PROVEN]`: the
α-family carries an exact `ℤ²` shift symmetry `X_n(2^i3^jα,k)=X_{n+j}(α,k−i−j)` (0 failures, 8 cases), so
α=8 and α* lie in the SAME single orbit iff `α*/8 ∈ ⟨2,3⟩` — which (α* irrational) it does not, confirming
they are two genuinely distinct instances.** Route 1 FAILS: the family is near-orthogonal at matched `(n,k)`
(`|corr|≤floor` for all pairs, even ⟨2,3⟩-resonant ones), so a second-moment/large-sieve average bounds only
the AVERAGE over α (= the AEV/lacunary a.e.-normality result, already known) and never the two specific
measure-zero points 8, α*; max/avg energy is 1.14 — the variance does not bite for an individual. Route 2
FAILS as a *reduction*: `β=d⊕σ⊕ρ` makes β-equidistribution follow only from CONDITIONAL equidistribution of
one diagonal given the other, which is a 2-D Mahler statement that IMPLIES (is strictly HARDER than) a single
diagonal; mere decorrelation `corr(d,σ)→0` (observed ≤0.012, all k) is a cross-Mahler bilinear sum that is
itself unproven, and α* is ENDOGENOUS (defined by the orbit of 8), so "8, α* Diophantine-independent" is not
even a clean hypothesis. **No machine decided. No label upgraded.**

---

## 1. The α-family is one `ℤ²`-orbit: exact shift symmetry  `[PROVEN, 0 failures]`

Write `X_n(α,k) = bit_k(⌊α(3/2)^n⌋)`; for `α=p/q` this is `bit_{n+k}((p·3^n)//q)` exactly (`floor(α 3^n/2^n)
= ((p3^n)//q)>>n`). The two diagonals are `d_n=X_n(8,k)`, `σ_n=X_n(α*,k)` (`σ_n` computed exactly from the
orbit carry `S_n`, `TWO_DIAGONAL_COMPARISON §1a`).

> **`[PROVEN]` `ℤ²` shift action.** For `α' = 2^i 3^j α`,
> **`X_n(α',k) = X_{n+j}(α, k−i−j)`** whenever `k−i−j ≥ 0` (the low `i+j` bits are fresh).
> *Proof:* `α'(3/2)^n = 2^{i+j} α(3/2)^{n+j}`; `bit_k(⌊2^m y⌋) = bit_{k−m}(⌊y⌋)` for `k≥m` (multiplying by
> `2^m` shifts the binary point), with `m=i+j`, `⌊y⌋ = ⌊α(3/2)^{n+j}⌋ = `the integer whose bit `k−i−j` is
> `X_{n+j}(α,k−i−j)`. ∎
> **Verified 0 failures** across `α'∈{16,24,12,18,48,36,32,54}=2^i3^j·8` (`shift_identity.py`, N=4·10³,
> k<14, ≈5·10⁴ comparisons each).

**Consequence.** Multiplying the leading constant by `2^i3^j` is an *exact symmetry*: it merely translates
the diagonal in the `(n,k)` plane (`n→n+j`, `k→k−i−j`). So the whole one-parameter AEV family
`{bit_k⌊α(3/2)^n⌋}` collapses, under the group `⟨2,3⟩` acting on α, to **orbits**: two constants `α,α'`
generate the *same* digit array (up to an `(n,k)`-shift) **iff `α'/α ∈ ⟨2,3⟩ = {2^i3^j}`**. For the two
needed constants `α*/8 ≈ 0.016978…` — irrational (a transcendental-looking `(2/3)`-series), hence `∉ ⟨2,3⟩`
— so **`d_n` and `σ_n` belong to different `ℤ²`-orbits: there is no exact deterministic link**, they are two
distinct instances. (Exact resonance is *provably absent* under "α* irrational"; this is the rigorous core of
the `[OBSERVED] corr≈0` of `TWO_DIAGONAL_COMPARISON §2b`.)

---

## 2. Numerics — cross-α correlations vs the Diophantine relation  `[OBSERVED]`

### 2a. Same-`(n,k)` cross-α correlation matrix (`k=8`, `N=2·10⁴`, floor `1/√N=0.0071`)
Every off-diagonal entry is at the `√N` floor — **including the ⟨2,3⟩-resonant pairs** (8↔16, 8↔24,
8↔12, 8↔18) — because the resonance lives at *shifted* `(n,k)` (§1), not at matched indices. The single
visible structure is `corr(d,σ)` itself: `{k:2→−0.007, 4→+0.004, 6→+0.012, 8→+0.003}`, all `≤1.7/√N`.

| pair | a8·a24 | a8·a16 | a8·a12 | a8·a7 | a8·a81 | a8·**σ** |
|---|---|---|---|---|---|---|
| same-`(n,k)` corr | 0.334\* | −0.006 | −0.004 | 0.003 | 0.001 | **0.003** |

\*the 0.334 is the **adjacent-bit** correlation `corr(bit_8,bit_7)` of one `⌊8(3/2)^n⌋` surfacing because
a24/a16 need a `k`-shift not applied here — see §2b.

### 2b. Resonance detection: max `|lag-corr|` (n-lag ≤4) vs ratio to α=8
The Diophantine relation **controls** the correlation: ⟨2,3⟩-resonant pairs peak far above the floor (the
ones needing no `k`-shift hit **1.000**); a *near*-resonance (81/80 = 3⁴/(2⁴·5), detuned only by a factor 5)
gives a **partial 0.196**; genuinely generic ratios and the actual pair **8↔α\*** sit at the floor.

| pair | ratio/8 | max lag-corr | best lag | class |
|---|---|---|---|---|
| 8↔12 | 3/2 | **+1.000** | −1 | RESONANT ⟨2,3⟩ |
| 8↔18 | 9/4 | **+1.000** | −2 | RESONANT ⟨2,3⟩ |
| 8↔16 | 2 | +0.334 | +1 | RESONANT (needs k−1) |
| 8↔24 | 3 | +0.334 | 0 | RESONANT (needs k−1) |
| 8↔81/10 | 81/80 | +0.196 | −4 | NEAR-resonant (factor 5) |
| 8↔7 | 7/8 | −0.008 | +3 | generic |
| 8↔201/64 | ≈π·… | −0.015 | 0 | generic |
| **8↔σ** | **α\*/8≈0.0170** | **+0.018** | −1 | **generic (α\*/8 irrational)** |

This is the clean picture: **correlation is a step function of the Diophantine relation** — exactly 1 on the
⟨2,3⟩-resonant set, decaying through near-resonances, at the floor on generic ratios. `α*/8` is generic.

### 2c. Second moment over the α-family — the variance does NOT bite  `[OBSERVED]`
`E(α)·N := mean_{a odd}|Inj_a(α)|²·N`, `Inj_a(α)=(1/N)Σ_n(X_n(α)−½)χ_a(s_n)` (orbit phase `s_n=c_n mod 2^k`,
`k=8`, family of 11 α incl. 8 and α*):

| α | a8 | a16 | a24 | a7 | a81 | apiish | **σ(α\*)** | **family ⟨E⟩** | **max** |
|---|---|---|---|---|---|---|---|---|---|
| E·N | 0.242 | 0.297 | 0.272 | 0.248 | 0.257 | 0.288 | **0.255** | **0.259** | **0.297** |

`(1/m)Σ_α E(α)·N = 0.259`, `max=0.297`, **`max/avg=1.14`** — all individuals ride the same `O(1)·1/N` floor;
cross Inj-vector cosines `|⟨Inj_8,Inj_σ⟩|=0.08`, `|⟨Inj_8,Inj_7⟩|=0.018`, `|⟨Inj_8,Inj_16⟩|=0.016` — the
family is **near-orthogonal**. So the second moment averages to the floor with no individual exceeding it by
more than 14% — but this bounds only the *average*; see §3.

---

## 3. Honest verdict — the two routes

### 3a. Route 1: variance / large-sieve over a FINITE α-family  →  **does NOT bite for an individual**

The cross-α near-orthogonality (§2a, §2c) makes `(1/m)Σ_α|Inj(α)|² ≈` the *mean* of the individual energies
(off-diagonal cosines ≤0.08). A second-moment bound of this form controls the **average over α** (equivalently,
the *number* of "bad" α), **never a single fixed α**: the two constants 8 and α* are two specific measure-zero
points, and `max/avg=1.14` shows the average gives no nontrivial cap on the worst individual.

> **`[PROVEN-in-lit, structural]`** The large-sieve route is exponentially defeated: the natural Weyl sum
> `Σ_n a_n e(α·(3/2)^nθ)` has "frequencies" `(3/2)^nθ` spanning a range `~(3/2)^N`, so the large-sieve bound
> `(Y_max+δ^{-1})Σ|a_n|²` is useless. The *correct* unconditional output of an L²-over-α / lacunary method is
> **square-root cancellation for a.e. α** (Salem–Zygmund / Erdős–Gál for the lacunary `(3/2)^n`) — which is
> precisely AEV's a.e.-normality of `⌊α(3/2)^n⌋`, **already known and measure-zero-blind to the two needed
> points.** A finite family cannot upgrade an a.e. statement to two specific points.

**Verdict (c): variance over α gives only the (already-known) a.e./average statement; it does not control 8
or α* individually.**

### 3b. Route 2: provable independence  →  **NOT a reduction; independence is itself Mahler-hard**

The XOR `β=d⊕σ⊕ρ` (ρ tame) means `(K)` (β-equidistribution against every phase character) follows from
**conditional equidistribution of ONE diagonal given the other** — i.e. *joint* equidistribution of
`(d_n,σ_n)`. A 2-D joint equidistribution **implies each marginal**, hence is **strictly harder** than a
single diagonal: proving it would prove both `α=8` and `α=α*` AEV instances at once. So independence-as-needed
is the opposite of a reduction.

What about the *weaker* statement, mere decorrelation `corr(d_n,σ_n)→0` (observed ≤0.012)? Two facts kill it
as a route:
1. **Insufficient.** Decorrelation of the bits does NOT give `β`-equidistribution (one still needs a marginal,
   open). It is also not implied by, and does not imply, either single diagonal — an orthogonal, weaker fact.
2. **Itself unproven / Mahler-class.** `corr(d_n,σ_n) = (1/N)Σ(bit_k⌊8(3/2)^n⌋−½)(bit_k⌊α*(3/2)^n⌋−½)` is a
   cross-correlation of two deterministic Mahler sequences. Crucially **α\* is ENDOGENOUS** — defined by the
   parities `b_j=c_j mod 2` of the *same* orbit (α\*=(1/3)Σb_j(2/3)^j) — so the two sequences come from one
   dynamical source; "8 and α\* multiplicatively/Diophantine-independent" is not a clean hypothesis, and the
   only thing §1 delivers rigorously is the *exact*-resonance-free fact `α*/8∉⟨2,3⟩` (under "α\* irrational"),
   which forbids a *deterministic* link but not slow near-resonant correlation. Proving the bilinear sum →0 is
   a Sarnak/Chowla-type cancellation between two ⌊·⌋-orbits — unproven, no easier than the diagonals.

**Verdict (c): independence cannot be proven into a reduction — the conditional/joint version is strictly
harder than one diagonal, and the bare decorrelation is both insufficient and itself Mahler-hard.**

---

## 4. Genuinely new vs prior

- **vs `TWO_DIAGONAL_COMPARISON §2b`** (which *observed* `corr(d_n,σ_n)≈0`): this note supplies the
  **structural reason** as a `[PROVEN]` `ℤ²` symmetry `X_n(2^i3^jα,k)=X_{n+j}(α,k−i−j)` (0 failures) — the
  α-family is one `ℤ²`-orbit, two α link deterministically iff `α'/α∈⟨2,3⟩`, and `α*/8` is generic. The
  "asymptotic independence" is thus the absence of an exact shift-resonance, made precise; and the
  Diophantine dependence is exhibited (resonant→1, near-resonant 81/80→0.196, generic→floor).
- **vs `SECOND_DIAGONAL_RAJCHMAN.md`** (annealed σ closed by Rajchman, quenched = Mahler): consistent and
  complementary — this note works on the *joint* of the two quenched diagonals and the *family* over α, and
  finds the same wall from the cross-α / variance side: a.e.-over-α is all the L² method buys.
- **vs `ODD_ADDITIVE_ENERGY.md` / `ENERGY_ATTACK.md`** (2nd moment over FREQUENCIES `a`, sign-blind / only
  `M₂≥0` free): this is the orthogonal experiment — 2nd moment over the **α-family** instead of over
  frequencies. New finding: the family is near-orthogonal (cosines ≤0.08, `max/avg=1.14`), so the α-variance
  controls only the average = AEV a.e., never the two needed points. A *different* averaging axis, the *same*
  measure-zero/single-orbit wall.
- **New `[PROVEN]`:** the `ℤ²` shift symmetry of the AEV digit family and the exact rational reduction
  `X_n(p/q,k)=bit_{n+k}((p3^n)//q)`. **New `[OBSERVED]`:** cross-α correlation is a step function of the
  ⟨2,3⟩-Diophantine relation (with a measured near-resonance shoulder), and the α-family 2nd moment rides the
  floor with `max/avg=1.14`.

## 5. Exact residual

Unchanged and triangulated from the new axis: `(K)` still requires the equidistribution of the single
diagonal `d_n=bit_k⌊8(3/2)^n⌋` and/or `σ_n=bit_k⌊α*(3/2)^n⌋`, plus (for the XOR) their joint decorrelation —
all `= (K) =` Mahler 3/2 / AEV Conj 1.6 at the relevant constants. The joint / finite-family structure adds an
exact `ℤ²` symmetry (a genuine new characterization) but **no leverage**: variance-over-α buys only the
known a.e. statement, and independence is either strictly harder (conditional/joint) or insufficient-and-still-hard
(bare decorrelation, with α* endogenous to the orbit).

## Sources
- Repo: `TWO_DIAGONAL_COMPARISON.md` (§1a `σ_n=bit_k⌊α_n^σ(3/2)^n⌋`, α*=(1/3)Σb_j(2/3)^j; §2b corr≈0),
  `SECOND_DIAGONAL_RAJCHMAN.md` (annealed/quenched, single-orbit wall), `ODD_ADDITIVE_ENERGY.md` (2nd moment
  over frequencies; only `M₂≥0` free), `ENERGY_ATTACK.md` (sign-blindness, character-sum reduction),
  `CARRY_COBOUNDARY.md` (β=d⊕σ⊕ρ, ρ finite-range), `DIGITS_OF_3N.md` ((K)=AEV ⌊α(3/2)^n⌋).
- Literature (repo knowledge): Mahler 3/2 (1968, open); Andrieu–Eliahou–Vivion arXiv:2510.11723 (Conj 1.6,
  a.e./uniform-in-α normality); Salem–Zygmund / Erdős–Gál square-root cancellation for lacunary `(3/2)^n`
  (a.e. α); large-sieve (Montgomery–Vaughan); Sarnak/Chowla deterministic-sequence cross-correlations.
- Numerics: `scratchpad/two_alpha_joint.py` (N=2·10⁴: cross-α matrix, lag-resonance table, family 2nd moment,
  Inj cosines), `scratchpad/shift_identity.py` (N=4·10³: `ℤ²` shift identity, 8 resonance cases, 0 failures).

**No machine decided. No label upgraded.**
