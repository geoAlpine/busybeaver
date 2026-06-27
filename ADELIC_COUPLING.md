# Adelic / product-formula coupling and Furstenberg ×2,×3 for the induced odd map (2026-06-28)

*Angle: the induced Antihydra-Syracuse map `o ↦ o' = 3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`, integer orbit
`o0=27`, lives simultaneously in `R` (archimedean, `|o|_inf` grows like `(3/2)^{time}`) and `Z_2`
(2-adic, depth `D`). Question: does the product formula / adelic structure, or Furstenberg ×2,×3 rigidity,
give a single-orbit constraint on the `D`-sequence (target `freq(D=1) ≤ 1/2`) that is NOT available from
either valuation alone? Numerics `.venv` only (`adelic_coupling.py`, exact big-int, 2·10^5 induced steps).
Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

The product formula gives **NO** non-trivial constraint on the `D`-sequence: the only adelic identity is
the single scalar `log|N|_inf = D·log2 + Σ_p v_p·log p` per step, which sums to the **first-moment**
renewal identity `log o_n ≈ (Σ D_j)·log(3/2)` (verified to 8 digits) — it pins the mean and nothing about
the distributional shape (`freq(D=1)`). **But** the product-formula bookkeeping does yield one genuinely
new exact arithmetic identity, a clean **2-adic↔3-adic coupling**:

> **`[PROVEN]` `v3(o_{j+1}) = D_j − 1`** exactly, every step.

This re-encodes the entire 2-adic depth statistic as a **3-adic divisibility density** of the orbit:
`freq(D=1) = density{ 3 ∤ o_{j+1} }`, so the target `freq(D=1) ≤ 1/2` ⟺ **at least half the induced orbit
terms are divisible by 3**. The obstruction lives at the 2-adic place of `o_j` and the 3-adic place of
`o_{j+1}` *simultaneously and locked together* — but controlling the 3-adic density of an explicit orbit is
the **same single-orbit genericity** wall, now relabelled in `Z_3`. Furstenberg/Rudolph/Lindenstrauss ×2,×3
theory classifies **invariant measures** (and only under positive joint entropy); it gives **no** pointwise
single-orbit statement, and the relevant measure conjecture is itself open. The irreducible obstruction is
**exactly** the open Mahler 3/2 / ×2,×3-independence: a.e.-equidistribution (ergodic theorem) vs.
this-explicit-orbit equidistribution.

---

## 1. Adelic setup and the product formula `[PROVEN, but trivial for the D-sequence]`

For odd `o>1` set `N = 3o−1 > 0`. The product formula `∏_v |N|_v = 1` reads
> `|N|_inf · |N|_2 · ∏_{p odd} |N|_p = (3o−1) · 2^{−D} · ∏_{p odd} p^{−v_p(N)} = 1`,
i.e. `2^D = (3o−1)/m`, where `m = ∏_{p odd} p^{v_p(N)}` is the odd part of `N`.

**This is literally the fundamental theorem of arithmetic** (`N = 2^D·m`) and holds for every nonzero
integer; it carries **no information about the `D`-sequence beyond the per-step definition** `D=v2(3o−1)`.
Numerics: `N = 2^D·m` every step (sanity, ✓).

**Taking `log|·|_inf`** gives the only continuous shadow of the finite data:
`log(3o−1) = D·log2 + Σ_{p odd} v_p(N)·log p` (one scalar per step). The induced map is
`o' = 3^{D−1}m`, so `log o' = (D−1)log3 + log m = log o + D·log(3/2) + log((3 − 1/o)/3)`, i.e.

> `log o_n = log o_0 + (Σ_j D_j)·log(3/2) + (bounded correction)`. `[PROVEN]`

Since the gap lemma gives `Σ_j D_j = micro-time = n`, this is the archimedean↔renewal **first-moment**
identity: it ties the **sum** `Σ D_j` to `log o_n`, and nothing more. **Verified** (2·10^5 steps):
`Σ D_j = 399254`, `log o_end = 161886.845`, `log o0 + (Σ D)log(3/2) = 161886.862`, **ratio 0.99999989**.

> **`[PROVEN]` The product formula constrains the `D`-sequence only through the single scalar log identity
> per step (= first moment / renewal). The distribution of `D` — hence `freq(D=1)` — is left completely
> free. There is NO non-trivial product-formula constraint linking `Σ D_j` to the 2-adic digit pattern.**

### 1a. The genuinely new fact — 2-adic↔3-adic coupling `[PROVEN]`

`3o−1 ≡ −1 (mod 3)` for all `o`, so `3 ∤ (3o−1)`, hence `3 ∤ m`. Then `o' = 3^{D−1}m` gives
`v3(o') = D−1 + v3(m) = D−1`. **Exactly.**

> **Lemma (2↔3 coupling).** `v3(o_{j+1}) = D_j − 1 = v2(3o_j−1) − 1`, every step. `[PROVEN]`
> Verified exactly over 2·10^5 induced steps from `o0=27` (0 exceptions); `3 | (3o−1)` and `3 | m`
> occur 0 times, as required by the proof.

**Consequences.**
- `freq(D=1) = density{ 3 ∤ o_{j+1} }`; `freq(D≥2) = density{ 3 | o_{j+1} }`;
  `freq(D≥3) = density{ 9 | o_{j+1} }`. The minimal proposition `freq(D≥2)+freq(D≥3) ≥ 1/2`
  (`SESSION_2026-06-28_MINPROP.md`) becomes **`density{3|o_j} + density{9|o_j} ≥ 1/2`** — a purely
  **3-adic divisibility-density** statement about the orbit.
- The orbit is **not** 3-adically Haar: `v3(o_{j+1})` is distributed as `D−1`, i.e.
  `P(v3 = k) = 2^{−(k+1)}` (geometric base 2), **not** the natural `Z_3`-Haar `(2/3)3^{−k}`. The 3-adic
  valuation distribution of the orbit is **dictated by the 2-adic structure of the predecessor** — the
  adelic coupling made concrete and quantitative.
- This is the **crispest expression of "the obstruction lives at two places at once"**: the *same*
  arithmetic event is a 2-adic depth of `o_j` and a 3-adic valuation of `o_{j+1}`, product-formula-locked.

**Why it does not breach (honest).** Controlling `density{3 | o_j}` for the *explicit* orbit is single-orbit
equidistribution in `Z_3`, exactly as hard as the `Z_2` cylinder-frequency wall (A). The coupling is an
**isomorphism of obstructions, not a reduction in difficulty**. (It is, however, a new and citable exact
identity, and it confirms that the two-valuation entanglement is genuine rather than heuristic.)

---

## 2. Furstenberg ×2,×3 — what is proven, what it gives us `[survey + honest verdict]`

The independence "archimedean fractional parts of `(3/2)^n` vs. 2-adic digits of the orbit" is precisely the
×2/×3 (equivalently ×(3/2)) joint-structure phenomenon. State of the art:

- **Furstenberg 1967 (topological).** The only closed `{×2,×3}`-invariant subsets of `R/Z` are finite
  (rationals) or all of `R/Z`. → an **orbit-closure dichotomy**, NOT equidistribution of any *specified*
  orbit. Gives nothing about Cesàro frequencies of our `o0=27`.
- **Furstenberg's measure conjecture.** The only `{×2,×3}`-invariant ergodic measures on `R/Z` are Lebesgue
  and atomic-on-rationals. **OPEN** in the needed generality.
- **Rudolph 1990 / Johnson.** If a measure is jointly `×2,×3`-invariant, ergodic for the semigroup, and has
  **positive entropy** (for `×2` or `×3`), then it is Lebesgue (Johnson: any multiplicatively independent
  `p,q`). This is a **measure-classification / rigidity** theorem.
- **Host 1995, Lindenstrauss 2006.** Host: `×p`-normality and equidistribution results under an invariance/
  ergodicity hypothesis; Lindenstrauss: measure rigidity for higher-rank diagonal actions on homogeneous
  spaces (arithmetic QUE) — again *measure* statements, requiring positive entropy / recurrence inputs and
  set in `SL` quotients, not single-orbit semigroup actions on a point.

**Does any of it give a single-orbit statement for us? NO — for two compounding reasons.** `[PROVEN-honest]`

1. **Measure vs. orbit.** Rudolph/Johnson/Host/Lindenstrauss **classify invariant measures**. To use them
   one must already know the orbit's empirical (Cesàro) measure **is** the relevant invariant measure — that
   is the genericity assumption itself. Birkhoff gives equidistribution only for **μ-a.e.** point; our `o0`
   is one specified point (measure zero). The a.e.→this-point upgrade is exactly the wall.
2. **No positive-entropy jointly invariant measure is supplied by our orbit.** Rudolph *needs* a single
   measure invariant under **both** generators with **positive** entropy. A single orbit under the **one**
   induced map produces (at best) weak-* limits invariant under that one map only; there is no jointly
   `{×2,×3}`-invariant measure attached to `o0`, and the induced map's Haar invariant measure on `Z_2^*`
   (Bernoulli, positive entropy — `INDUCED_RESIDUE_STRUCTURE.md §2`) is again the **a.e.** object, not the
   orbit's. So Rudolph's hypothesis is **not met** by our single orbit even though the ambient invariant
   measure has positive entropy.

> **`[PROVEN-honest]` Furstenberg/Rudolph/Lindenstrauss ×2,×3 theory gives measure rigidity, not pointwise
> single-orbit equidistribution. It does not apply to `o0=27`: our orbit supplies no positive-entropy
> jointly invariant measure, and the relevant pointwise / measure-conjecture statements are themselves open.**

---

## 3. The decisive question — adelic equidistribution, and the irreducible obstruction `[PROVEN-characterization]`

The integer orbit embeds diagonally `o_j ↦ (o_j ∈ R, o_j ∈ Z_2, o_j ∈ Z_3, …)`. Under the induced map the
archimedean coordinate expands by `≈(3/2)^{D_j}` while the 2-adic coordinate **shifts** (discard low `D`
bits, pull in fresh high bits; `INDUCED_RESIDUE_STRUCTURE.md §1`). The needed conclusion is **joint
equidistribution of `(archimedean position, 2-adic digits)` along the one orbit** — equivalently, that the
`(3/2)`-driven orbit has its 2-adic depths Cesàro-equidistributed (geometric, mean 2).

**Is there an adelic equidistribution theorem that pins this specific orbit?** No. The available diagonal-
action / solenoid equidistribution theorems are either (a) **measure classification** (Rudolph-type;
inapplicable, §2), or (b) **a.e. statements** (ergodic theorem under the Haar/Bernoulli measure of the
induced map; `INDUCED_RESIDUE_STRUCTURE.md` — excludes a null set, not `o0`). The gap between (b) and "this
explicit point" is exactly the open content.

**Mahler 3/2 connection (literature).** Mahler's 3/2 problem — whether `{ξ(3/2)^n}` can stay in `[0,1/2)`,
or more generally how `{ξ(3/2)^n}` distributes — is **open**; it is not even known that `{(3/2)^n}` is
dense. The best unconditional fact (Flatto–Lagarias–Pollington) is `limsup{ξ(3/2)^n} − liminf ≥ 1/3` for all
`ξ>0` (a *gap*, not a density; curiously the same `1/3` as our even-density target, but not load-bearing).
Our archimedean coordinate growing as `(3/2)^{time}` with 2-adic digits read off is **structurally the same
unsolved ×2,×3-independence**.

> **`[PROVEN]` Irreducible obstruction, crispest form.** The target reduces to: *the single explicit orbit
> `(o_j)` from `o0=27` equidistributes in the 2-adic cylinders `{o ≡ 3^{−1} mod 2^k}` (equivalently — by the
> §1a coupling — has 3-adic divisibility densities `density{3^a | o_j} = 2^{−a}`).* This is a **pointwise /
> single-orbit** joint-equidistribution statement for a `×2,×3`-type (Mahler 3/2) system. Every available
> tool gives strictly less: the **product formula** gives only the **first moment** (one scalar log identity
> per step, §1); **measure rigidity** (Furstenberg/Rudolph/Lindenstrauss) classifies invariant measures and
> needs a positive-entropy *jointly* invariant measure our orbit does not supply (§2); the **ergodic
> theorem** gives equidistribution for Haar-a.e. point but not `o0` (`INDUCED_RESIDUE_STRUCTURE.md`). The
> archimedean–2-adic independence is exactly the open Mahler 3/2 statement, and the adelic coupling, while it
> ties the 2-adic and 3-adic places together exactly (§1a), is an isomorphism of the obstruction, not a
> reduction of its difficulty.**

---

## 4. Numerics `[OBSERVED, exact]` (`adelic_coupling.py`, 2·10^5 induced steps, `o0=27`)

- **(1) Product formula sanity:** `N = 2^D·m` every step; `3|(3o−1)` 0 times; `3|m` 0 times.
- **(2) 2↔3 coupling `v3(o_{j+1}) = D_j−1`:** holds **every** step (0 exceptions over 2·10^5). `[PROVEN, confirmed]`
- **(3) First-moment log identity:** `Σ D_j = 399254`; `log o_end = 161886.845`;
  `log o0 + (Σ D)log(3/2) = 161886.862`; **ratio 0.99999989**. Mean `D = 1.99627` (Haar 2);
  `freq(D=1)=0.50034` (Haar 1/2). The only adelic constraint = this first moment; shape free.
- **(4) Odd-prime structure of `3o−1` carries no usable structure correlated with `D`:**
  `v5`, `v7` distributions match `Z`-Haar geometric `(1−1/p)p^{−k}` to 3 dp;
  `corr(D_j, v5(3o_j−1)) = +0.0004 ≈ 0` (independence). The only non-trivial coupling is the **3-adic** one
  (`v3`, forced by `3o−1 ≡ −1 mod 3`); all other primes are inert/independent.
- **(5) `D` is i.i.d.-geometric along the orbit:** `corr(D_j, D_{j+1}) = −0.006 ≈ 0`;
  `P(D=k)` matches `2^{−k}` to 3 dp for `k=1..8` — consistent with (but not proof of) genericity.

---

## 5. Verdict (the three asks)

| ask | answer | label |
|---|---|---|
| Does the product formula give a non-trivial constraint on the `D`-sequence (beyond the trivial log identity)? | **No.** Only the single scalar `log(3o−1)=D log2+Σ_p v_p log p` per step, summing to the first-moment renewal `log o_n ≈ (Σ D_j)log(3/2)` (verified). Distribution / `freq(D=1)` left free. **Bonus exact identity:** `v3(o_{j+1})=D_j−1`, re-encoding the 2-adic depth as a 3-adic divisibility density — an isomorphism of the obstruction, not a reduction. | `[PROVEN]` |
| What does Furstenberg/Rudolph/Lindenstrauss ×2,×3 give for our single orbit? | **Measure rigidity only**, not single-orbit equidistribution. Inapplicable to `o0`: needs a positive-entropy *jointly* `×2,×3`-invariant measure our orbit does not supply; ambient Haar/Bernoulli positivity is the **a.e.** object, not the orbit's empirical measure; Furstenberg's measure conjecture is itself open. | `[PROVEN-honest]` |
| Crispest irreducible obstruction? | **Single-orbit pointwise** joint equidistribution of the explicit orbit `(o_j)` in `Z_2` cylinders `{o≡3^{−1} mod 2^k}` (≡ 3-adic densities `density{3^a|o_j}=2^{−a}`) — a `×2,×3`/Mahler-3/2 statement. Product formula → first moment only; rigidity → measures only; ergodic theorem → a.e. only. The archimedean–2-adic independence **is** the open Mahler 3/2 problem. | `[PROVEN]` |

### New asset banked `[PROVEN]`
*Exact 2-adic↔3-adic product-formula coupling `v3(o_{j+1}) = v2(3o_j−1) − 1` (since `3o−1 ≡ −1 mod 3`).
Hence the minimal proposition `freq(D≥2)+freq(D≥3) ≥ 1/2` is identical to the 3-adic density statement
`density{3|o_j} + density{9|o_j} ≥ 1/2`, and the orbit's 3-adic valuation law is `P(v3=k)=2^{−(k+1)}`
(forced by the 2-adic predecessor, not `Z_3`-Haar). The archimedean place adds only the first-moment
identity `log o_n ≈ (Σ D_j) log(3/2)`.*

### Why this confirms rather than breaches (honest)
The adelic apparatus makes the two-valuation entanglement **exact and citable** but **does not lower the
difficulty**: the product formula is a first-moment-only constraint, ×2,×3 rigidity is a measure (not orbit)
theorem whose hypotheses our single orbit fails, and the residual statement is pointwise single-orbit
equidistribution = the open Mahler 3/2 / wall (A). Consistent with `SESSION_2026-06-28_MINPROP.md`'s
meta-theorem (open core is irreducibly orbit-specific) and `INDUCED_RESIDUE_STRUCTURE.md` (a.e. vs.
this-point gap).

### Live next angle (not yet mined)
The 3-adic re-encoding (§1a) opens a **dual** attack surface: instead of 2-adic cylinder frequencies, bound
the **3-adic divisibility density** `density{3|o_j}` of the explicit orbit. Same wall in principle, but the
3-adic side carries an asymmetry worth probing — `3o−1 ≡ −1 mod 3` forces `3∤(3o−1)` *deterministically*,
so the factor `3^{D−1}` in `o'` is the **only** source of 3-divisibility, and 3-adic and 2-adic data of a
single term `o_j` are NOT independent of each other (unlike across terms). Whether a *combined* `Z_2×Z_3`
self-consistency (the term must simultaneously satisfy `v2(3o−1)=D` and carry `v3(o)=D_{prev}−1`) yields a
local arithmetic constraint not visible in either place alone is the one un-mined micro-question; current
numerics show the cross-prime correlation is 0, so it is a long shot.

Script: `adelic_coupling.py`. Not committed.
