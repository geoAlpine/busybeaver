# Quantitative escape from the repelling fixed point o=1 — dual-valuation repulsion (2026-06-28)

*Angle: o=1 is a REPELLING fixed point of the induced odd map `T(o)=3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`,
`o_0=27`. Make the repulsion **quantitative in BOTH valuations** (archimedean × 2-adic), build an adelic
"distance-to-1" height, and ask whether escape forces a one-sided bound on `freq(D=1)` WITHOUT genericity,
or reduces to occupancy = Mahler. Numerics `.venv` only (`repeller_escape.py`), exact big-int orbit of 27,
N=600000. Zero false proofs. Every line labelled. NOT committed.*

Recall: `D=1 ⟺ o≡1 mod4 ⟺ v2(o−1)≥2` (SHALLOW, `T(o)=(3o−1)/2`); `D≥2 ⟺ o≡3 mod4 ⟺ v2(o−1)=1` (DEEP).

---

## 0. One-line answer

The repulsion is **exact and two-sided-clean**: on every `D=1` step `|o−1|_∞ ×3/2` and `|o−1|_2 ×2`
(equivalently the **odd part of `o−1` triples**), so the adelic height to 1 grows by **exactly `log3` per
`D=1` step** — escape from `o=1` is unconditional and monotone along `D=1` runs. `[PROVEN]`. **But this
does NOT give a one-sided `freq(D=1)` bound.** Two reasons, both `[PROVEN]`:

1. The archimedean height balance is **degenerate with** the 2-adic `φ`-balance: the 2-adic identity
   `Σ_deep(r'−1)=#{D=1}` collapses the adelic telescoping to the trivial total `Σ D` identity. The two
   valuations are **NOT independent constraints** at the height level — combining them adds nothing.
2. Both valuations **repel**, so any **positive-weight** adelic distance-to-1 *increases* on `D=1`; an
   escape-detecting sub-action needs a **negative** archimedean weight (penalise size) = the
   magnitude-aware Lyapunov `α log o + h(o mod 2^k)`, `α<0`, which **reintroduces size-drift genericity**.

Where it lands: the density `freq(D=1)=1−1/E_deep` is fixed by the **refill law** `r'=v2(o_next−1)` after
deep steps (`E_deep`=mean refill, Haar value 2) — the 2-adic re-approach to 1 — which is **exactly the
occupancy/genericity = Mahler** quantity. **Quantitative escape confirms `o=1` is repelling but does NOT
breach: it reduces to occupancy.** The genuine valuation-independence (the Mahler core) lives in the
refill law, not in the height drift. `[PROVEN reduction; OBSERVED no margin]`

---

## 1. DUAL-REPULSION LEMMA `[PROVEN]` (verified 300174/300174 D=1 steps, 0 failures)

> **Lemma (dual repulsion).** Let `o` be odd with `D=v2(3o−1)=1` (i.e. `o≡1 mod4`, `v2(o−1)=a≥2`). Then
> `o' = T(o) = (3o−1)/2` and:
> - **(archimedean)** `o'−1 = (3/2)(o−1)` exactly, so `|o'−1|_∞ = (3/2)|o−1|_∞` — multiplier **3/2**.
> - **(2-adic)** `v2(o'−1)=a−1` (Countdown Lemma), so `|o'−1|_2 = 2·|o−1|_2` — multiplier **2**.
> - **(odd part)** the odd part of `o−1` multiplies by exactly **3**:
>   `oddpart(o'−1) = 3·oddpart(o−1)`.
> - **(adelic)** `|o'−1|_∞·|o'−1|_2 = 3·|o−1|_∞·|o−1|_2` — multiplier **3 = (3/2)·2**.

**Proof.** `o'−1 = (3o−1)/2 − 1 = (3o−3)/2 = (3/2)(o−1)` (archimedean, exact). Write `o−1=2^a w`, `w` odd,
`a≥2`. Then `o'−1=(3/2)2^a w = 3·2^{a−1}w`, and `3w` is odd, so `v2(o'−1)=a−1` and `oddpart(o'−1)=3w
=3·oddpart(o−1)`. The adelic product multiplier is `(3/2)·2=3`. ∎

**Both valuations leave the neighbourhood of 1.** Archimedean: `o−1` moves away from 0 at rate `3/2`
(real expansion, multiplier `3/2` of the linear map `o↦(3o−1)/2` fixing `o=1`). 2-adic: `v2(o−1)` drops
by 1, so `o` moves *away* from `1` in `Z_2`. So a `D=1` step is repulsion **in both places at once**.

**Numerics (N=600000).** Of 300174 `D=1` steps: `fail (o'−1)=3(o−1)/2: 0`, `fail v2(o'−1)=v2(o−1)−1: 0`,
`fail oddpart(o'−1)=3·oddpart(o−1): 0`. Exact.

---

## 2. The re-approach requirement and the refill law `[PROVEN reduction; OBSERVED]`

A run of `m` consecutive `D=1` steps needs (Countdown) `v2(o_start−1)≥m+1`, i.e. `o_start≡1 mod 2^{m+1}`
(2-adically **very close** to 1). After the run `v2(o−1)=1` (2-adically *far*, `|o−1|_2=1/2`, the boundary
of `Z_2^*`). To start another long `D=1` run the orbit must **re-approach** `o=1` 2-adically — only deep
(`D≥2`) steps can *refill* `v2(o−1)` to a large value, since `D=1` steps only ever *decrement* it.

> **Refill law `[OBSERVED]`.** After a deep step, `r' := v2(o_next−1)` is fresh. Distribution on the orbit
> matches Haar `P(r'=k)=2^{-k}` to 3 dp (`0.4993, 0.2499, 0.1259, 0.0620,…`), `E_deep=2.0012 ≈ 2`.

> **Renewal closed form `[PROVEN]` (reconfirmed from `MINPROP_RUNS.md`).**
> `freq(D=1) = 1 − 1/E_deep`,  `E_deep =` mean deep-step refill.  `freq(D=1)≤1/2 ⟺ E_deep≤2`.
> Numerics: `freq(D=1)=0.50029`, `1−1/E_deep=0.50029` (exact identity). No one-sided margin.

**The honest landing (prompt #3).** The escape/re-approach argument says: long `D=1` runs are 2-adically
rare *if* the refills `r'` are not persistently large. But the **density** of `D=1` steps is
`1−1/E_deep`, controlled **entirely by the refill law `E_deep`**, which is `v2(o_next−1)` after a deep
step — a 2-adic-digit quantity = **conditional cylinder occupancy = single-orbit genericity = Mahler/AEV
= wall (A)**. The escape (`v2` drops on `D=1`) is self-limiting and proven, but the *fraction* is set by
how high deep steps refill, not by the escape itself. **No one-sided bound without genericity.**

---

## 3. The adelic height has NO independent one-sided drift `[PROVEN structural]`

Adelic height to 1: `H(o) := log oddpart(o−1) = log|o−1|_∞ + v2(o−1)·log2`
(`= −log(|o−1|_∞·|o−1|_2)^{-1}`, the archimedean size of the odd part).

- **On `D=1`:** `ΔH = +log3` **exactly** (§1, odd part ×3). `[PROVEN]` (fails=0).
- **On deep:** `ΔH = D·log(3/2) − (r'−1)·log2 + o(1)`; mean `+0.5213`, **not one-sided** (78.6% positive,
  21.4% negative, range `[−12.36, +8.23]`). `[OBSERVED]`

Telescoping `H_N−H_0 = #{D=1}·log3 + Σ_deep ΔH` verified exact (`486073.04 = 486073.04`), and
`H_N ≈ ΣD·log(3/2)` (size growth). So `H` is monotone-up on `D=1` and up-on-average on deep steps:
**everything escapes `o=1`; nothing drifts toward it.**

> **Degeneracy theorem `[PROVEN]`.** The archimedean balance of `H` is **not independent** of the 2-adic
> `φ`-balance. Indeed at the start of every deep step `φ=v2(o−1)=1`, so the 2-adic balance is
> `Σ_deep(r'−1) = #{D=1}` (the renewal identity; numerics `300175.9` vs `300174`, diff `=φ_N−φ_0` bounded).
> Substituting the deep `ΔH = D log(3/2)−(r'−1)log2` and using this balance, the adelic telescoping
> collapses to the **trivial total identity** `#{D=1} + Σ_deep D = Σ_all D`. Hence the height combining
> the two valuations imposes **no constraint beyond `Σ D`** — it is degenerate.

**Consequence.** The hope "link archimedean escape to 2-adic proximity to get a one-sided density bound"
**fails at the height level**: the natural adelic height is degenerate (the two balances are the same
balance). Any genuine valuation-independence must constrain the **refill law itself** (`E_deep≤2`), which
is precisely genericity/Mahler — not recoverable from the height drift.

---

## 4. No positive-weight escape sub-action `[PROVEN]`; sub-action needs `α<0` = genericity

Try a magnitude-aware Lyapunov `L(o) = a·log|o−1|_∞ − b·v2(o−1)·log2` and ask for an
**escape-detecting sub-action**: `ΔL < 0` on `D=1` (so `L` decreases as the orbit leaves the
`D=1`-dominant region) plus non-positive mean drift.

- On `D=1`: `Δlog|o−1|_∞=log(3/2)>0`, `Δv2=−1`, so `ΔL = a·log(3/2) + b·log2`. For **any** `a,b≥0` this is
  `>0`: **both valuations repel**, so a positive-weight adelic distance-to-1 *increases* on `D=1`. There
  is **no positive-weight `L` that decreases toward `o=1`** — consistent with `o=1` being repelling.
- A sub-action with `ΔL<0` on `D=1` requires `a<0` (penalise archimedean **size**). That is exactly the
  **non-bounded magnitude-aware Lyapunov `α log o + h(o mod 2^k)`, `α<0`**, of `MINPROP §F1` — which
  couples to the size drift `D·log(3/2)` and **reintroduces avoidance/genericity**. `[OPEN]` residual,
  not breached here.

This explains structurally why the coboundary LP (`MINPROP_COBOUNDARY_LP.md`) is INFEASIBLE with bounded
`g`: the `o=1` self-loop has `ψ(1)=+1/2>0`, and **no bounded adelic height can decrease toward a repelling
fixed point**. Escape is real, but it is "outward," giving no bounded sub-action.

---

## 5. Verdict (the prompt's asks)

| ask | answer | label |
|---|---|---|
| PROVEN dual-repulsion lemma (×3/2 arch, ×2 2-adic per `D=1`) | **`|o−1|_∞×3/2`, `|o−1|_2×2`, oddpart `×3`, adelic `×3`, all exact** (§1). Verified 300174/300174, 0 fails. | `[PROVEN]` |
| Does re-approach/refill give a one-sided `freq(D=1)` bound without genericity, or reduce to occupancy? | **Reduces to occupancy.** `freq(D=1)=1−1/E_deep`; density fixed by the refill law `E_deep=`mean `v2(o_next−1)` after deep steps = 2-adic digit = genericity = Mahler. Escape is self-limiting & proven but does not bound the fraction. No margin (oscillates across ½). | `[PROVEN reduction; OBSERVED no margin]` |
| Does a combined adelic-height Lyapunov have one-sided drift? | **No.** `H=log oddpart(o−1)` jumps `+log3` on `D=1` (escape, monotone up) and up-on-average on deep steps — everything escapes `o=1`. The archimedean balance is **degenerate** with the 2-adic `φ`-balance (both collapse to `ΣD`), so combining valuations adds **no independent constraint**. No positive-weight distance-to-1 decreases on `D=1` (both repel); a sub-action needs `α<0` = magnitude-aware = genericity (F1 OPEN). | `[PROVEN structural]` |

### Banked `[PROVEN]`
- **Dual-Repulsion Lemma.** On a `D=1` step: `o'−1=(3/2)(o−1)` and `v2(o'−1)=v2(o−1)−1`; hence
  `|o−1|_∞×3/2`, `|o−1|_2×2`, `oddpart(o−1)×3`, adelic `|o−1|_∞|o−1|_2 ×3`. `o=1` repels in **both**
  valuations simultaneously.
- **Adelic-height degeneracy.** The combined height `H=log oddpart(o−1)` increases by exactly `log3` per
  `D=1` step but its drift telescopes to the trivial `ΣD` identity (the 2-adic `φ`-balance
  `Σ_deep(r'−1)=#{D=1}` absorbs the archimedean side). The two-valuation combination is **not** an
  independent one-sided constraint.

### Honest: confirms, does not breach — and pins the link precisely
Quantitative dual repulsion is a clean new PROVEN fact and verifies that `o=1` is repelling in both
places. But the **only** un-reduced micro-target stays `E_deep≤2` (the refill law), i.e. single-orbit
genericity. The valuation-link hope (`MINPROP §5/6`) **does not survive at the height level** (degenerate),
which is itself informative: the Mahler obstruction is not bridged by an adelic distance-to-1 — the
independence of the two valuations is concentrated in the refill digit law, exactly where genericity lives.

Script: `repeller_escape.py` (scratchpad). Not committed.
