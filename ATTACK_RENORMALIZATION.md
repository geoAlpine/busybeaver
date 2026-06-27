# The 0.7748 constant, the annealed→quenched renormalization, and what it does (and does not) buy

Attack on Link B of `NONPISOT_FOURIER_CHAIN.md`: understand the constant ratio
`|ν̂_{2/3}((3/2)^N/8)| / Φ(N) ≈ 0.7748` and turn the annealed↔quenched correspondence into a
functional equation / transfer bound. Numerics: `renorm_attack.py` (mpmath, 60 digits). Zero false proofs;
every line labelled. **Not committed.**

---

## 0. Setup (exact)
`ν̂_{2/3}(ξ) = Π_{j≥0} cos(2π ξ (2/3)^j)`. At the sparse geometric frequency `ξ_N = (3/2)^N/8`,
`ξ_N (2/3)^j = (3/2)^{N−j}/8`, so
```
ν̂_{2/3}(ξ_N) = Π_{j≥0} cos( (π/4)(3/2)^{N−j} ) = Π_{k=−∞}^{N} cos( (π/4)(3/2)^k )   (k = N−j).
```
This is the whole game: the **head** `k = 0..N` is the annealed carry product Φ; the **tail** `k ≤ −1`
is an N-independent convergent product — that is why the ratio is constant.

---

## 1. The 0.7748 constant — closed form [PROVEN, verified to 60 digits]

The tail is exactly
```
C := Π_{m≥1} cos( (π/4)(2/3)^m )           (all factors positive: argument < π/8)
   = √2 · ν̂_{2/3}(1/8)
   = ν̂_{2/3}(1/8) / cos(π/4)
   = 0.774846171700205441444752...    (← the measured "0.7748")
```
**Why the second equality.** `ν̂_{2/3}(1/8) = Π_{j≥0} cos((π/4)(2/3)^j) = cos(π/4) · Π_{m≥1} cos((π/4)(2/3)^m)
= (1/√2)·C`. So `C = √2·ν̂_{2/3}(1/8)`. Numerically `C − √2·ν̂_{2/3}(1/8) = −4.7e-61` (round-off at 60 dps).

**Interpretation (clean and useful).** The "mystery constant" is *not* mysterious: it is the value of the
Bernoulli-convolution Fourier transform itself at the **base frequency** `ξ_0 = 1/8` of the geometric ladder
`ξ_N = (3/2)^N/8`, normalised by the single `k=0` carry factor `cos(π/4)`. The constant *is the tail of the
same cascade*, anchored at the bottom rung. No new transcendental — it is `ν̂_{2/3}` re-used.

**Φ convention pinned down [verified].** The ratio is *exactly* `C` (to 8 digits, all N=5..80) **only** for
`Φ(N) := Π_{k=0}^{N} |cos((π/4)(3/2)^k)|` (i.e. through `k=N` inclusive). The `k<N` convention oscillates
(0.20–0.75). So the correct, constant-ratio identity is
```
|ν̂_{2/3}((3/2)^N/8)| = Φ(N) · C ,   Φ(N) = Π_{k=0}^{N} |cos((π/4)(3/2)^k)| ,   C = √2·ν̂_{2/3}(1/8).   [PROVEN]
```

---

## 2. The renormalization — what the self-similarity actually delivers

### 2.1 The self-similarity is the carry recursion, *exactly* [PROVEN, diff = 0]
BC self-similarity `ν̂(ξ) = cos(2πξ)·ν̂((2/3)ξ)` applied at `ξ = ξ_{N+1} = (3/2)ξ_N` gives
`ν̂(ξ_{N+1}) = cos(2πξ_{N+1})·ν̂(ξ_N)`, i.e.
```
Φ(N+1)/Φ(N) = |cos(2π ξ_{N+1})| = |cos((π/4)(3/2)^{N+1})|.     [verified diff = 0.0 at N=10,25,50]
```
So the Bernoulli-convolution renormalization and the annealed carry-product recursion are the **same
identity**. This is a genuine structural confirmation that Link B is exact (not a numerical coincidence) —
**but it is a tautology**: an identity carries no information beyond the `cos` factors it is built from.
A renormalization/transfer bound that is an *identity* cannot manufacture a decay rate.

### 2.2 The decay rate of Φ [the real finding]
Two regimes, cleanly separated by the numerics (`renorm_attack.py §2`, N up to 32768):

| quantity | N=64 | N=1024 | N=32768 | limit |
|---|---|---|---|---|
| `−lnΦ(N)/N`   | 0.775 | 0.691 | 0.687 | **→ ln 2 = 0.6931…** |
| `−lnΦ(N)/lnN` | 11.9  | 102   | 2166  | **→ ∞** |

- **Observed (deterministic / "quenched phases"):** `Φ(N) ≈ 2^{−N}` — **exponential in N**, slope → `ln 2`
  exactly. This is the equidistribution value `E[log|cos(πU)|] = −ln 2`: the deterministic phases
  `{(3/2)^k/4}` *behave as if equidistributed*. **[OBSERVED; the equidistribution that would make it a
  theorem is Mahler — OPEN.]**
- **Provable (Rajchman, Varjú–Yu):** `|ν̂_{2/3}(ξ)| ≤ C/(log|ξ|)^a` (logarithmic in ξ). Along the ladder
  `log ξ_N ≈ N·ln(3/2)`, so **the provable bound, in the natural step variable N, is**
  ```
  Φ(N) ≲ N^{-a}   — POLYNOMIAL in N.     [PROVEN modulo citing Varjú–Yu]
  ```

**Answer to the payoff question.** The correspondence *does* give a modest but real upgrade: it converts the
"logarithmic-in-ξ" Rajchman statement into a **polynomial-in-N** floor `Φ(N) ≲ N^{−a}` (because `ξ_N` grows
geometrically, log-in-ξ = poly-in-N). That is strictly better than the naive "logarithmic-in-N" one might
fear. **But the self-similarity itself yields no further improvement** — it is an identity (§2.1). The huge
remaining gap is `provable N^{−a}` vs `observed 2^{−N}`, and closing it = proving equidistribution of
`{(3/2)^k}` = the Mahler core. The renormalization relocates, it does not shorten.

---

## 3. Annealed vs quenched, and the suggested quenched transfer operator [honest gap]

**Everything above is ANNEALED.** Φ is the i.i.d.-weight product; equivalently `|E[e(T_n/2^{n+1})]|` for
fair Bernoulli inputs. The factorisation into a product of `cos` is *exactly* the statement that the annealed
transfer operator is **rank-1 / multiplicative** (independent weights ⇒ characteristic function factors).
The actual Antihydra object is the **quenched** sum `Σ_j e_j (3/2)^j` with the orbit's own self-generated,
**correlated** parity weights `e_j`; this does **not** factor (Mahler).

**Does the renormalization suggest a quenched analogue? Yes — a twisted transfer operator.**
The annealed product `Π cos((π/4)(3/2)^k)` is the spectral data of a *rank-1* operator. Replace the i.i.d.
weights by the deterministic parity dynamics that generates `e_j` (the Antihydra skew-product over the
doubling/`×3/2` map). The natural quenched object is then a **twisted Ruelle–Perron–Frobenius operator**
```
(L_t f)(x) = Σ_{preimages} e( (1/4)(3/2)^{·} ) · f(·) ,
```
i.e. the transfer operator of the parity dynamics weighted by the character `e((3/2)^k/4)`. The annealed C is
the degenerate (independent) case where `L_t` collapses to scalar multiplication by `cos`. A **spectral gap
`ρ(L_t) < 1`** for the genuine (correlated) operator would give the quenched `Σ e_j (3/2)^j` exponential
cancellation — the analogue of the observed `2^{−N}`. This is precisely the `‖F‖`-contraction /
self-consistent-transfer-operator picture of `NEW_FRAMEWORK.md`, and establishing the gap **is** the open
Mahler/AEV core (`PROOF_STATUS.md` line (5)). So the renormalization gives the *right shape* of the quenched
target (a twisted transfer operator with a spectral gap), not a proof of it.

---

## 4. Bankable bottom line
- **[PROVEN, 60-digit]** `0.7748… = C = √2·ν̂_{2/3}(1/8) = Π_{m≥1} cos((π/4)(2/3)^m)` — the BC transform at the
  base frequency `1/8`; the constant ratio is forced because the tail `k≤−1` is N-independent.
- **[PROVEN]** Exact identity `|ν̂_{2/3}((3/2)^N/8)| = Φ(N)·C` with `Φ(N)=Π_{k=0}^{N}|cos((π/4)(3/2)^k)|`;
  the BC self-similarity reproduces the carry recursion `Φ(N+1)/Φ(N)=|cos((π/4)(3/2)^{N+1})|` exactly (an
  identity, diff = 0).
- **[PROVEN modulo Varjú–Yu citation]** Effective rate: `Φ(N) ≲ N^{−a}` (polynomial in N) — the log-in-ξ
  Rajchman bound upgraded by the geometric ladder. This is the honest improvement over "logarithmic".
- **[OBSERVED, = Mahler, OPEN]** True rate is `Φ(N) ≈ 2^{−N}` (slope → ln 2 = equidistribution). The
  self-similarity, being an identity, does **not** bridge `N^{−a} → 2^{−N}`.
- **[STRUCTURAL]** The annealed product = rank-1 transfer operator; the quenched analogue is a **twisted RPF
  operator** whose spectral gap would give the quenched exponential cancellation — same target as `‖F‖<1` /
  the Mahler core. Suggested, not proven.

Net: the 0.7748 constant is fully demystified and the correspondence is rigorously exact, giving a clean
polynomial-in-N provable floor; but the renormalization is a tautology that cannot, by itself, reach the
observed exponential rate — that remains the quenched Mahler core, now sharply framed as a twisted-transfer
spectral-gap problem.
