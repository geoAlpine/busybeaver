# Twisted Ruelle–Perron–Frobenius operator L_t — construction, ρ(L_t), and verdict (2026-06-28)

Attack **d** of `SESSION_2026-06-28_QUENCHED_ATTACK.md`: build the twisted transfer operator
`L_t` and test the thesis

> quenched (3/2)^j Korobov cancellation = exp. decay of `E[e(T_n/2^{n+1})]` = `ρ(L_t)^n`,
> and `ρ(L_t)<1 ⇔ quenched cancellation ⇔ ‖F‖<1 ⇔ Mahler`.

Code: `busybeaver/twisted_rpf.py`. All numerics with `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`
(numpy 2.4.4). **Zero false proofs**; every number below is labelled [OBSERVED]/[PROVEN]/[OPEN].

---

## 1. Construction of L_t

**Base dynamics (verified closed form).** The carry phase `φ_n = T_n/2^{n+1} mod 1` of
`T_{n+1}=3T_n+2^n e_n` obeys the ×(3/2) map with a Bernoulli bit injected at 1/4:

    φ_{n+1} = (3/2) φ_n + e_n/4   (mod 1).

`next_state(s,b,k)` of `mckean_contraction.py` is **exactly** this map discretised to `k` bits
([PROVEN by exhaustive check, k=4,6,8]):

    next_state(s,b,k) = ( floor(3s/2) + b·2^{k-1} ) mod 2^k.

So **`s/2^k` is the discretised phase φ (the leading bits), not the low bits.** The untwisted
operator `L_op` is row-stochastic, λ₁=1, λ₂ = 0.00008 / 0.0017 / 0.008 / 0.021 at k=4/6/8/10.

**The twist (derived from `exp_sum.py`).** Per step the character contributes the factor
`(1/2)(1+e((3/2)^j/4))`, `|·| = |cos(π{(3/2)^j/4})|`; their product is the annealed sum
`E[e(φ_N)] = ∏_j (1/2)(1+e((3/2)^j/4))`, `|·| = Φ(N)`. I built **three** twisted operators on Z/2^k:

- `Lt_inject`: `L_t[s,next(s,b,k)] += (1/2)·e(b/4)` — per-step bit-injection character.
- `Lt_diag`: `L_t = D·L_op`, `D = diag(e(s/2^{k+1}))` — literal "twist the Markov operator" by the
  character that should reproduce Φ.
- `Lt_ruelle`: Ruelle operator of the angle map `θ→(3/2)θ` with complex weight `g(θ)=(1/2)(1+e(θ))`,
  `(L_g f)(θ)=Σ_{(3/2)η=θ} g(η) f(η)`; ρ = exp(pressure), the textbook twisted-RPF object.

---

## 2. ρ(L_t) vs k — CONVERGES (no drift to 1), but to the WRONG rate [OBSERVED]

| k  | ρ(Lt_inject) | ρ(Lt_diag) | ρ(Lt_ruelle) |
|----|-------------|-----------|-------------|
| 4  | 0.7538      | 0.7885    | 1.000000    |
| 6  | 0.7227      | 0.7508    | 1.000000    |
| 8  | 0.7278      | 0.7259    | 1.000000    |
| 10 | 0.7179      | 0.7138    | 1.000000    |
| 12 | 0.7173      | 0.7136    | 1.000000    |

- `Lt_inject`, `Lt_diag` **converge** to ≈ **0.717 ≈ cos(π/4)=0.707** as k→∞. Unlike the contraction
  audit (which drifted ρ → 1 with resolution), these do **not** drift — but they converge to the
  **single first factor** `|cos(π·{(3/2)^0/4})| = cos(π/4)`, i.e. a **frozen angle θ=1/4**.
  `−log₂(0.717) ≈ 0.48`, giving decay `2^{−0.48 n}`, **not** `2^{−n}`.
- `Lt_ruelle = 1.000000` exactly for all k: the leading eigenvalue comes from the **atomic fixed
  point θ=0** (0↦0, weight `g(0)=(1/2)(1+1)=1`) — the same δ₀ spurious fixed point the contraction
  audit flagged. No spectral gap on the finite grid.

**Why a fixed operator must give the wrong rate [PROVEN, structural].** The true decay is
`(1/N)log Φ(N) = (1/N) Σ_j log|cos(π{(3/2)^j/4})|`, a sum over the **moving** angle `θ_j=(3/2)^j/4 mod 1`.
A fixed operator's `ρ^N` produces a **constant** per-step factor, so it can only reproduce a single
frozen angle (→ 0.717) or an atomic orbit (→ 1). It is **structurally incapable** of encoding the
per-step changing angle `(3/2)^j`. The Mahler rate `1/2` would require averaging over the
*equidistributed* angle: `ρ = exp(∫₀¹ log|cos πx| dx) = exp(−log 2) = 1/2`. The fixed twisted operator
on Z/2^k does not see that average.

---

## 3. Cross-check vs Φ — the finite operator does NOT even carry the annealed Φ [OBSERVED, falsified shortcut]

I tested whether the matrix-vector iteration `(L_op^N v)_0` with `v_s=e(s/2^{k+1})` reproduces `Φ(N)`:

| N | `|(M^N v)_0|` | Φ(N) | ratio |
|---|---|---|---|
| 1 | 7.07e-1 | 7.07e-1 | 1.00 |
| 2 | 6.53e-1 | 2.71e-1 | 2.41 |
| 4 | 6.38e-1 | 4.66e-2 | 13.7 |
| 10| 6.37e-1 | 1.70e-3 | 375 |
| 16| 6.37e-1 | 1.29e-6 | 4.9e5 |

It matches Φ **only at N=1**, then **plateaus at 2/π = ∫₀¹|cos πx| dx = 0.6366** (the L¹ mean of the
character), while Φ(N)→0. **The finite mod-2^k operator cannot carry the (3/2)-escaping product:**
the frequency `(3/2)^N` aliases immediately under the `floor(3s/2)` truncation. This is the
**non-Pisot obstruction in operator form** — the very reason no finite twisted transfer operator
captures the cancellation.

**Φ itself does decay like 2^{−N} [OBSERVED, = Mahler].** `−log₂Φ(N)/N`: 0.73 (N=8) → 1.00 (N=128) →
1.00 (N=1024). The limit slope **1** is exactly `∫₀¹ log|cos πx| dx = −log 2`, i.e. the
**equidistribution of {(3/2)^j} = Mahler**. So `Φ ~ 2^{−n}` ⇔ Mahler, but this lives in the
infinite-frequency (escaping) picture, not in any finite operator.

---

## 4. Annealed vs quenched — which did I reach?

- **ANNEALED reached, but only as a product, not a finite-operator eigenvalue.** `Φ(N)=∏_j(1/2)(1+e((3/2)^j/4))`
  is exact and decays 2^{−N} (Mahler). It is *rank-1 along an escaping frequency orbit* — there is no
  recurrence, hence no eigenvalue. The finite mod-2^k truncation destroys even this (§3 plateau).
- **QUENCHED: there is no twisted-transfer spectral radius.** The real single orbit
  (`a→floor(3a/2)`, fully self-generated parity) gives [OBSERVED, N up to 256000]:
  parity density → 0.5; Birkhoff cancellation `|(1/N)Σ(−1)^{r_n}| ~ N^{−1/2}` (α = 0.52, 0.51, 0.52,
  0.56). The quenched object is a **Birkhoff average decaying N^{−1/2}** (random-like), a *different*
  object from the single-time `E[e(φ_n)] ~ 2^{−n}`. Along one orbit `|e(φ_n)|≡1`; decay only appears
  in expectation/averaging, which re-introduces the escaping frequency = annealed.

**Plainly: I built the ANNEALED object (and showed even it resists the finite operator). The quenched
spectral gap `ρ(L_t)<1` does NOT exist as a finite twisted-transfer eigenvalue.**

---

## 5. Soundness verdict

- **Is `ρ(L_t)<1` measured or proven?** For the fixed operators `Lt_inject`/`Lt_diag`, ρ≈0.717<1 is
  [OBSERVED] and converges — but it is the **wrong quantity** (frozen-angle rate, not the Mahler rate),
  so it does **not** prove quenched cancellation. `Lt_ruelle` has ρ=1 (no gap). **Attack d's thesis —
  that quenched cancellation = a finite twisted-RPF spectral gap — is NOT realised; the gap is an
  artifact-free convergent number that nonetheless measures the wrong thing.**
- **Is the k→∞ limit controlled?** Yes for `Lt_inject`/`Lt_diag` (clean convergence to ≈cos(π/4); **no**
  drift-to-1, so this is *not* the contraction-audit failure mode). But controlled convergence to the
  wrong value is not progress on Mahler.
- **Finite-size artifact?** Different from the contraction audit. There ρ drifted to 1 (non-normal
  pseudospectrum). Here ρ converges cleanly; the failure is **structural, not finite-size**: a
  time-homogeneous operator cannot represent the inhomogeneous `(3/2)^j` angle sequence. The §3
  plateau (2/π) and the `Lt_ruelle=1` (δ₀) are the genuine finite manifestations of non-Pisot escape.

### Bankable conclusions (0 false proofs)
1. **[PROVEN]** `next_state` = discretised ×(3/2) phase map; `s/2^k` = phase φ, not low bits.
2. **[OBSERVED/clean]** Fixed twisted operators converge (no drift to 1) but to cos(π/4)≈0.717 (frozen
   angle) or 1 (δ₀) — the **wrong** rate; the Mahler rate 1/2 = `exp(∫log|cos πx|dx)` requires the
   equidistributed angle a fixed operator cannot encode.
3. **[OBSERVED]** The finite mod-2^k operator does not carry Φ (plateaus at 2/π) — non-Pisot escape.
4. **[OBSERVED]** `Φ ~ 2^{−n}` ⇔ slope→1 ⇔ equidistribution of {(3/2)^j} = Mahler; quenched single
   orbit cancels only `N^{−1/2}` (Birkhoff, random-like).
5. **[VERDICT]** Attack d does **not** reduce Mahler to a finite-operator spectral gap. The honest
   restatement: the quenched/Mahler core is a property of an **escaping (non-recurrent) frequency
   orbit**, which by construction has **no finite transfer operator with a spectral gap**. Thermodynamic
   formalism applies only after passing to the equidistribution (Mahler) one is trying to prove —
   confirming the annealed[PROVEN]/quenched[OPEN]=Mahler split, now with the operator-theoretic reason
   the gap cannot exist finitely. The relevant operator is the *infinite-dimensional* ×(3/2) transfer
   operator on the circle (Bernoulli-convolution / `ν_{2/3}` operator), whose spectral theory is the
   non-Pisot Fourier-decay problem itself — not shortened by twisting a finite carry matrix.
