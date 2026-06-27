# Soundness audit — the self-consistency-contraction route (`mckean_contraction.py`)

Adversarial audit of the claim: *the self-consistency map `S: ν ↦ L_ν ν` is a CONTRACTION
(constant ≈ `λ₂(L)+‖F‖ ≈ 0.048 < 1`) with a UNIQUE fixed point = Haar, which sidesteps the
variational-principle obstruction because self-consistency is strictly stronger than invariance
(only Haar is self-consistent).*

Every claim labelled **[PROVEN] / [CONDITIONAL] / [OPEN] / [REFUTED]**. Zero false proofs. All
numerics reproduced with `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (numpy 2.4.4); probe
scripts in the session scratchpad.

**VERDICT: the sidestep, as written, is UNSOUND.** Two independent load-bearing claims fail under
audit. The route is not dead — a *much weaker* local statement may survive — but the headline
("unique self-consistent measure = Haar, contraction constant 0.048") is not supported and one of
its two pillars is outright false.

---

## 1. The sidestep argument: "self-consistency ⊋ invariance, only Haar is self-consistent"

### 1a. The counterexample in the script is computed with the WRONG operator. **[REFUTED]**
The script (lines 49–57) "checks the sidestep" by computing `‖δ₁·L − δ₁‖₁` where `L = L_op(k)` is
the **Haar / fair-coin** operator `L_Haar`. But self-consistency of `δ₁` is the equation
`δ₁ = L_{δ₁} δ₁` — it must use `L_{δ₁}`, the operator built from **`δ₁`'s own conditional incoming-bit
law**, not `L_Haar`. What the script actually computes (`‖δ₁ L_Haar − δ₁‖₁ = 1.0`) only tests whether
`δ₁` is invariant under the *fair-coin* operator, which is trivially false and is **not** the
self-consistency test. The "delta_1 is NOT self-consistent (spreads)" conclusion does not follow from
the displayed computation.

### 1b. Done correctly, δ₁ IS self-consistent — so the uniqueness claim is FALSE. **[REFUTED]**
Computing the actual operator `L_{δ₁}`: under `δ₁` (point mass at the 2-adic integer `1 = …0001`) the
high bit is deterministically `0`, so `P_{δ₁}(b=0 | s)=1`. The step from low-state `1` with `b=0` is
`next_state(1,0,k) = ((3·1 − 1)/2) mod 2ᵏ = 1`. Hence
> `L_{δ₁} δ₁ = δ₁`,  i.e. `‖L_{δ₁}δ₁ − δ₁‖₁ = 0.000` (probe verified, all k).

`δ₁` is a *genuine fixed point of the self-consistency map* `S`. (Likewise `δ₀`, since `T(0)=0`.) These
are exactly the integer fixed points of `T` (`T(c)=(3c−(c mod 2))/2`, fixed points `{0,1}`) re-appearing
as atomic self-consistent measures. **Therefore self-consistency does NOT single out Haar: `S` has at
least three fixed points (Haar, δ₀, δ₁).** The variational-principle multiplicity is *reproduced*, not
sidestepped. The sentence "only Haar is self-consistent; atomic invariant measures spread" is false as
the operator is defined.

### 1c. Hidden circularity in the closure. **[OPEN]**
`L_ν` is *defined* by replacing the orbit's actual incoming high bit with its `ν`-conditional law
`P_ν(high bit = b | low state = s)`. That this mean-field closure is the correct description of the
orbit's self-generated scenery is precisely the propagation-of-chaos assumption — the very thing the
route must prove. So "Haar solves (SC)" is **[PROVEN]** (when `ν=Haar` the conditional is fair and
independent, `L_Haar = L`, the one-step-exact operator, and `Haar = L_Haar·Haar`), but it is *not*
evidence that the orbit's empirical measure obeys (SC). The definition does not assume the bit law one
wants to derive (no logical circularity there), but it *does* presuppose the closure whose validity for
a single deterministic trajectory is the open problem.

**Conclusion §1:** the "self-consistency ⊋ invariance" sidestep is **not rigorous and its concrete
witness is false**. Self-consistency is at best *locally* more selective near Haar; globally it admits
the same atomic fixed points. Any surviving argument must be a **local** statement (Haar is one of
several fixed points and is locally attracting), not a global-uniqueness statement.

---

## 2. The contraction constant `λ₂(L) + ‖F‖ ≈ 0.048`

### 2a. Spectral-radius subadditivity is invalid here; `L` is maximally non-normal. **[REFUTED as a bound]**
The claimed bound is `ρ(L+F)|_{mean-zero} ≤ λ₂(L) + ‖F‖`. Spectral radius is **not subadditive**
(`ρ(A+B) ≤ ρ(A)+ρ(B)` is false in general; it needs commuting/normal/simultaneously-triangularizable
operators). Here the two ingredients are wildly mismatched:
- On the mean-zero complement `V`, `L|_V` has spectral radius `ρ = 0` (genuinely: probe shows `L|_V` is
  **nilpotent**, `(L|_V)^m = 0` exactly for `m ≥ 12` at `k=10`), **but operator norm `‖L|_V‖₂ = 1.000`
  exactly for every `k`, and `‖(L|_V)^m‖₂ = 1` for all `m ≤ 8` before collapsing to 0** (extreme
  non-normality / long transient — a large Jordan block).
- The only *valid* triangle-type bound is via norms: `ρ(L+F) ≤ ‖L+F‖ ≤ ‖L|_V‖ + ‖F‖ = 1 + 0.04 = 1.04`
  — **useless** (`> 1`, predicts no contraction).

### 2b. Pseudospectral reality: a perturbation of norm 0.04 moves ρ to ≈0.5, growing with resolution. **[PROVEN numerically]**
For a nilpotent non-normal operator a perturbation of size `ε` moves eigenvalues by `~ε^{1/d}` (`d` =
Jordan size), not by `ε`. Direct test — add random perturbations of operator-norm `ε=0.04` to `L|_V`
and measure `ρ(L+F)`:

| k | dim(V) | ρ(L\|V) | claimed λ₂+‖F‖ | actual ρ(L+F), ‖F‖=0.04 (mean / max over 40 trials) |
|---|---|---|---|---|
| 6 | 63 | 0.002 | 0.048 | **0.40 / 0.48** |
| 8 | 255 | 0.010 | 0.048 | **0.47 / 0.50** |
| 10 | 1023 | 0.021 | 0.048 | **0.52 / 0.55** |

The realized spectral radius is `~10×` the claimed `0.048` **and grows monotonically with `k`** (the
2-adic resolution). In the infinite-dimensional limit (`d → ∞`, `ε^{1/d} → 1`) this heuristic pushes
`ρ → 1`. So the scalar estimate `λ₂+‖F‖` provides **no valid upper bound on the contraction constant**;
the true generic value is order `0.5` and resolution-dependent.

### 2c. `F` is never built as an operator; "`‖F‖`" is a scalar finite-difference slope. **[OPEN]**
`mckean_contraction.py` does not assemble any matrix `F`; it inserts the scalar `0.04` from
`perturbation_F.py` (a `d(output density)/d(input density)` slope, open-loop / a correlation panel) and
adds it to `λ₂`. "Spectral radius of `L+F`" is therefore never computed as a matrix object. Because of
2a–2b, the actual contraction constant depends on the **operator structure of the real `F`**, not on its
scalar norm. The random-perturbation test (2b) is a *generic* bound, not the real `F`; it is conceivable
the true `F` has special structure landing below the generic `~0.5` — but that is unproven, and even the
generic answer is far from `0.048`.

### 2d. The reported `λ₂(L)` numbers are themselves spurious. **[CONDITIONAL note]**
The script reports `λ₂(L)` growing `0.00008 (k=4) → 0.008 (k=8)` and takes the "sup over k". Extending to
`k=13` gives a monotone climb to `0.050`. This is **numerical noise from diagonalising a defective
(nilpotent) matrix** (eigensolvers return spurious magnitudes `~machine-ε^{1/d}` for large Jordan blocks);
the *true* spectral radius on `V` is `0` (confirmed by the exact nilpotency `(L|_V)^m=0` in 2a). So the
qualitative claim "`ρ(L|_V)=0`" is **[PROVEN]** (good for the route), but the printed `λ₂≈0.008` and its
use as a contraction-budget term are meaningless, and — crucially — `ρ=0` with `‖·‖=1` is exactly the
configuration that makes the perturbation bound in 2a–2b fail.

**Conclusion §2:** the contraction constant `≈0.048` is **not a valid bound**. The valid norm bound is
`≥1` (useless); the realized spectral radius under a 0.04-perturbation is `~0.5` and grows with
resolution. At most one can hope for a *conditional, local* statement `ρ(L+F_real) < 1` once the actual
operator `F` is constructed and its structure controlled — which has not been done.

---

## 3. The exact remaining gap (one precise lemma)

Even granting (which is not established) a local linearized contraction `ρ((L+F)|_V) = κ < 1` making
Haar a **locally attracting** self-consistent fixed point, the complete proof still requires:

> **LEMMA (orbit → mean-field tracking / quenched propagation of chaos).**
> Let `μ_N := (1/N) Σ_{n<N} δ_{c_n mod 2^∞}` be the empirical measure of the single deterministic orbit
> `c₀ = 8`, `c_{n+1} = ⌊3c_n/2⌋`, on `ℤ₂`. Then `μ_N ⇒ Haar` (weak-*), with an effective rate
> `|E_n/n − 1/2| ≤ f(n)`, `f(n) → 0`, `f < 1/6`. Equivalently: the orbit's self-generated incoming-bit
> conditional law converges to the fair-independent law, i.e. the orbit lies in the basin of the Haar
> fixed point of `S` and is not attracted to the atomic fixed points `δ₀, δ₁`.

This is the only line that, combined with the (still unproven) local contraction, would close the proof.
It is **[OPEN]** and is identical to the line `(5)` of `gm_skeleton.py` / the Mahler–AEV kernel of
`PROOF_STATUS.md`: single-orbit equidistribution of `{(3/2)ⁿ}`-type data. The contraction framework, even
if its pillar §2 were repaired, would supply *uniqueness/attractivity of the limit*, never *that this one
Haar-null trajectory realizes it*.

---

## 4. Net assessment

| Claim | Status |
|---|---|
| `Haar` solves (SC); `L_Haar = L` is one-step exact; `ρ(L\|_V) = 0` | **[PROVEN]** |
| "Only Haar is self-consistent" / sidesteps variational principle | **[REFUTED]** — `δ₀, δ₁` are also self-consistent fixed points of `S`; script's witness uses the wrong operator |
| Contraction constant `≈ λ₂+‖F‖ ≈ 0.048` | **[REFUTED]** — non-subadditive + non-normal nilpotent `L`; valid norm bound `≥1`; realized `ρ(L+F)≈0.5`, growing with `k` |
| `‖F‖ ≈ 0.04` as a scalar slope (open-loop/panel) | measured, but **not** an operator-norm bound on the contraction; insufficient |
| Local linear stability of Haar (`ρ((L+F_real)|_V)<1`) | **[OPEN / CONDITIONAL]** — needs the real `F` assembled as an operator and controlled |
| Orbit tracks the mean field (§3 lemma) | **[OPEN = Mahler/AEV]** — the genuine remaining gap |

**What is rigorous:** Haar is a self-consistent fixed point; `L` is one-step exact with `ρ=0` on
mean-zero (and is exactly nilpotent in finite truncations). That's it.

**What is not:** (i) the global-uniqueness "sidestep" — false, atomic self-consistent measures exist;
(ii) the contraction constant `0.048` — invalid bound; the operator's extreme non-normality makes the
scalar `λ₂+‖F‖` heuristic break, with the realized perturbed spectral radius `~0.5` and rising with
resolution.

**Correct path forward (if the route is pursued):** drop the global-uniqueness language; aim only at a
**local** statement and build it correctly — (1) assemble `F` as an actual operator on `V` (not a scalar),
(2) bound `ρ((L+F)|_V)` or its pseudospectrum directly (the relevant object for a non-normal `L` is the
`ε`-pseudospectrum / Henrici departure-from-normality, not `λ₂+‖F‖`), (3) the §3 tracking lemma remains
the irreducible Mahler/AEV kernel regardless. The route does not sidestep the variational obstruction; it
relocates the same open kernel into mean-field language.
