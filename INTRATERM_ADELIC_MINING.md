# Mining the intra-term adelic coupling — the complete joint Z2×Z3 local law of one term, and why it is density-null (2026-06-29)

*Angle: WEAPONS_AUDIT_2026-06-29 §3 hybrid #1 — the one live hybrid with genuine novelty. Orbit `c0=8`,
`c→⌊3c/2⌋`; induced odd map `o↦o'=3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`; induced seed `o0=27` (= first odd
term of the `c`-orbit, confirmed). Two exact per-step identities hold on the SAME term: (i) `v2(3o-1)=D`
and (ii) `v3(o')=D-1`. Question: does the JOINT `Z2×Z3` (S-arithmetic `Z[1/6]`) constraint on a single
term yield ANY local fact about `density{3|o_j}` (= mean `D`) NOT already equivalent to single-orbit
equidistribution? Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`
(`scratchpad/intraterm_mining.py`, exact big-int, `N=10^5` induced steps, runs ≈24s). Every line labelled.
Zero false proofs. NOT committed.*

---

## 0. One-line verdict

**Hybrid #1 is CLOSED as a TAUTOLOGY — and this note gives the sharpest possible reason.** The complete
joint local law collapses the shallow/deep dichotomy to a **deterministic 4-cell function**

> **`[PROVEN]` `D_j = 1 ⟺ o_j ≡ 1 (mod 4) ⟺ u_j ≡ (−1)^{e_j} (mod 4)`,** where `o_j = 3^{e_j}u_j`,
> `gcd(u_j,6)=1`, `e_j = v3(o_j) = D_{j−1}−1` (verified 0 failures / 10^5 steps; all four cells `P∈{0,1}` exactly).

Writing the density out, `freq(D=1) = E[ 1{u_j ≡ (−1)^{e_j} mod 4} ]`, and because the 3-adic exponent
enters only through the unit rotation `3^{e_j} ≡ (−1)^{e_j} (mod 4)` — a **Haar-preserving permutation of
the two mod-4 unit classes** — the *entire 3-adic structure cancels* against the cofactor's mod-4 balance:
the density depends **only on `density{u_j ≡ 1 mod 4}` and on `u_j mod 4 ⊥ e_j`**, observed `χ²=0.06`
(`dof=1`). The 3-adic exponent law `e_j` — however structured (geometric, mean 1, full complexity) —
contributes **literally zero** to `freq(D=1)`. So the joint constraint pins / one-sided-bounds **nothing**:
the residual is the single mod-4 cofactor density `= 2-adic level-2 cylinder = wall (A) = Mahler/AEV`.
Verdict **(b) + (c)**: no new density bound; a sharp new proof of the tautology; the wall re-derived in its
crispest one-cylinder form. **No machine decided. No label upgraded.**

---

## 1. The complete joint Z2×Z3 local picture of a single term `[PROVEN]`

For odd `o>1` write `N = 3o−1`, `D = v2(N)`, `m = N/2^D` (odd part), and factor `o = 3^e u` with
`e = v3(o)`, `gcd(u,6)=1`. Every congruence below is exact (all verified, 0 failures / 10^5 steps):

| # | law | status |
|---|---|---|
| L1 | `N = 3o−1 ≡ −1 ≡ 2 (mod 3)`, hence **`v3(3o−1) = 0`** (the 3-adic place of `N` is always inert) | `[PROVEN]` |
| L2 | `m` is coprime to 3, and `m ≡ (−1)^{D+1} (mod 3)` (`m≡1` if `D` odd, `m≡2` if `D` even) | `[PROVEN]` (THREEADIC_ROTATION §4) |
| L3 | **`v3(o') = D−1`** (the *only* source of 3-divisibility in `o'` is the factor `3^{D−1}`) | `[PROVEN]` (ADELIC_COUPLING §1a) |
| L4 | along the orbit `e_j = v3(o_j) = D_{j−1}−1` (the 3-adic valuation IS the previous 2-adic depth) | `[PROVEN]` |
| L5 | `o ≡ 3^e u ≡ (−1)^e u (mod 4)` since `3 ≡ −1 (mod 4)` | `[PROVEN]` (elementary) |
| L6 | `D = 1 ⟺ 3o−1 ≡ 2 (mod 4) ⟺ o ≡ 1 (mod 4)` | `[PROVEN]` (WEAKEST_SUFFICIENT §1) |
| **L7** | **`D = 1 ⟺ u ≡ (−1)^e (mod 4)`** (combine L5+L6) — the joint `Z2×Z3` shallow/deep law | **`[PROVEN]`** |
| L8 | `o_j mod 3 ∈ {0,1}` for `j≥1` (residue 2 impossible); `3|o_{j+1} ⟺ D_j ≥ 2` | `[PROVEN]` (THREEADIC_ROTATION §4) |

**The single-term state is `(e, u mod 2^k)`** with `e` the inherited 3-adic exponent and `u` the
6-coprime 2-adic cofactor. L7 is the new content: the 2-adic depth bit `1{D=1}` is an **exact Boolean
function of `(e mod 2, u mod 4)`**, the simultaneous 3-adic-exponent-parity and 2-adic-cofactor-residue.
This is the most explicit form of "the obstruction lives at two places at once."

**Numerical confirmation of L7 (the 4-cell truth table, `N=10^5`):**

| `(e mod 2, u mod 4)` | count | `P(D=1)` | `o mod 4` |
|---|---|---|---|
| `(0, 1)` | 33240 | **1.0000** | `1` (shallow) |
| `(0, 3)` | 33334 | **0.0000** | `3` (deep) |
| `(1, 1)` | 16717 | **0.0000** | `3` (deep) |
| `(1, 3)` | 16708 | **1.0000** | `1` (shallow) |

Perfectly deterministic — `D=1` exactly on the two cells where `u ≡ (−1)^e mod 4`. L1–L8 all 0 failures.

---

## 2. The decisive question — does the joint law pin or bound the density? `[PROVEN: NO]`

The kernel (K)/H₂ is `mean D ≥ 3/2 ⟺ freq(D≥2) ≥ 1/2 ⟺ freq(D=1) ≤ 1/2`. By L7,

> **`[PROVEN identity]` `freq(D=1) = E[ 1{u_j ≡ (−1)^{e_j} (mod 4)} ] = Σ_{p∈{0,1}} P(e_j ≡ p) · P(u_j ≡ (−1)^p mod 4 | e_j ≡ p)`.**

This is the self-consistency equation the prompt asks for, written exactly. Read it carefully — it is the
crux:

- The 3-adic factor `3^{e_j}` acts on `u_j mod 4` only as `(−1)^{e_j}`, i.e. as a **measure-preserving
  permutation of the two residue classes `{1,3}` of `(Z/4)^*`**. Multiplication by a unit cannot change a
  class's measure; it only relabels which class counts as "shallow."
- Therefore `freq(D=1)` is a function of **two** statistics only: the conditional balances
  `P(u_j ≡ 1 mod 4 | e_j even)` and `P(u_j ≡ 3 mod 4 | e_j odd)`. **The distribution of `e_j` itself does
  not appear except as a convex weight** — and if both conditional balances equal `1/2`, the weights
  cancel: `freq(D=1) = ½·P(e even) + ½·P(e odd) = 1/2`, *independent of the entire 3-adic exponent law*.

**Measured (`N=10^5`):** `P(u≡1 mod4)=0.49957`, `P(u≡3)=0.50042`; `P(D=1|e)` is flat across `e=0..8`
(`0.497, 0.499, 0.502, 0.499, …`, drift only at small-sample tails `e≥4`, `n<3100`); the independence test
`χ²(e parity vs u mod 4) = 0.06` on `dof=1` (`u mod 4 ⊥ e`). Hence `freq(D=1)=0.49948 ≈ 1/2`.

> **`[PROVEN]` Why the coupling transfers NO density information.** The 3-adic exponent `e_j` enters
> `freq(D=1)` **only through the unit `(−1)^{e_j}`, a Haar-preserving permutation of `(Z/4)^*`**, so it is
> *additively annihilated* in the density: `freq(D=1) = 1/2` whenever the cofactor `u_j` is balanced mod 4
> and `⊥ e_j`. The orbit's rich, full-complexity 3-adic structure (geometric `e`-law,
> `THREEADIC_ROTATION`) contributes **exactly zero** to the kernel density. The kernel depends on a
> **single bit of the cofactor**, `density{u_j ≡ 1 mod 4}`, and on nothing 3-adic. There is no second,
> independent constraint to combine: by L4 the "3-adic place" is a time-shifted copy of the 2-adic
> itinerary (`e_j = D_{j−1}−1`, invertible — THREEADIC_SKEW §2), so it carries identical information,
> never more.**

**No one-sided bound either.** `freq(D=1) = P(u≡(−1)^e mod 4)`. There is no arithmetic asymmetry making
the matched class rarer (or commoner) than the unmatched one: multiplication by the unit `(−1)^e` is a
bijection of `{1,3}`, perfectly symmetric, so neither `freq(D=1)≤1/2` nor `≥1/2` is forced. **No forbidden
combination, no parity lock with a sign, no inequality.** (Consistent with REPELLER_ESCAPE §3–4: both
valuations repel symmetrically; no positive-weight adelic height yields one-sided drift.)

---

## 3. Why the product formula / S-arithmetic self-consistency is a tautology `[PROVEN-characterization]`

The orbit embeds diagonally in the `S`-arithmetic line `R × Q_2 × Q_3` (`S={∞,2,3}`), `Z[1/6]`-integral,
under the hyperbolic solenoid automorphism `×(3/2)`. The candidate "self-consistency" mechanisms and why
each is density-null:

- **Product formula `∏_v |N|_v = 1`.** This is the fundamental theorem of arithmetic `N = 2^D · m`
  (ADELIC_COUPLING §1): a **single scalar** (codimension-1) condition per step. Taking `log|·|_∞` gives the
  first-moment renewal identity `log o_n = log o_0 + (Σ_j D_j)·log(3/2) + O(1)` — verified here
  `ratio = 0.99999979`, `Σ D = 200069`. One scalar per step controls one scalar (`Σ D ↔ log o_n`); it
  **cannot constrain a distribution** (the codimension-∞ family of cylinder frequencies). The product
  formula's "self-consistency" is, by dimension count, mean-only. `[PROVEN]`
- **Strong approximation / Hasse principle.** `Z = R ∩ ∏_p Z_p` (integrality = adelic diagonal) is the
  only global-from-local input; for a *single* orbit it reproduces exactly the per-step renewal identity
  above. Strong approximation is a statement about the *closure* of `Z[1/6]` in the adeles, not about the
  Cesàro distribution of one specified orbit — it gives no pointwise equidistribution. `[PROVEN-honest]`
- **Hilbert-symbol / Artin reciprocity `∏_v (a,b)_v = 1`.** A `±1`-valued *quadratic* reciprocity law; any
  symbol built from `(3o−1, ·)` constrains **quadratic-residue parity**, an object orthogonal to the
  *valuation* `D = v2(3o−1)` and hence to the density target (which reads valuations, L1–L8). Reciprocity
  transfers no `D`-density information. `[PROVEN-honest]` (analytic; not load-bearing).

> **`[PROVEN]` The S-arithmetic self-consistency is exactly the first-moment identity (one scalar/step).**
> It is codimension-1; the kernel is codimension-∞ (a density / all-window liminf). The product formula
> therefore pins `Σ D ↔ log o_n` and leaves the shape — `freq(D=1)` — completely free. This is the precise,
> dimension-theoretic reason the adelic coupling is a tautology: **a global product = 1 is one equation;
> equidistribution is infinitely many.**

---

## 4. The wall, re-derived in its crispest one-cylinder form `[PROVEN reduction]`

Chaining L7 with §2, the open kernel becomes a single mod-4 **cofactor** density statement:

> **`[PROVEN]` (K) `⟺ mean D ≥ 3/2 ⟺ freq(D≥2) ≥ 1/2 ⟺ density{ u_j ≡ (−1)^{e_j+1} (mod 4) } ≥ 1/2`**,
> and (given `u_j ⊥ e_j`, itself part of the residual) `⟺ density{ o_j ≡ 3 (mod 4) } ≥ 1/2`.

This is identical to the WEAKEST_SUFFICIENT §3 one-character form `liminf avg χ₄(o_n) ≤ 0` and to the
THREEADIC_SKEW §2 base statement `freq(D≥2) ≥ 1/2`, now exhibited as a property of the **6-coprime cofactor
mod 4 alone**. The exact gap to a proof: establish, for the single orbit `o0=27`, that the cofactor bit
`u_j mod 4` is balanced and independent of its own 3-adic exponent — i.e. **2-adic single-orbit
equidistribution at level `k=2`** = AEV Conj 1.6 (rational base) / Mahler 3/2. No tool reaches even this one
one-sided cylinder for the deterministic `(3/2)`-orbit (WEAPONS_AUDIT §2–4). **Isomorphism of the
obstruction, not a reduction in difficulty.**

---

## 5. Numerics table `[OBSERVED, exact big-int, N=10^5]`

| quantity | value | Haar / target | reading |
|---|---|---|---|
| L1–L8 law failures | **0** | — | the entire joint local law is exact |
| `mean D` | `2.00069` | 2 | first moment Haar-consistent |
| `freq(D=1)` | `0.49948` | `≤1/2` (K) | shallow density |
| `density{3\|o_j}=freq(D≥2)` | `0.50052` | `≥1/2` (K) | matches `o%3==0` exactly |
| `density{9\|o_j}=freq(D≥3)` | `0.25011` | `1/4` | matches `o%9==0` exactly |
| `P(u≡1 mod4)`, `P(u≡3 mod4)` | `0.49957`, `0.50042` | `1/2` | cofactor mod-4 balance = the sole residual |
| `χ²(e parity vs u mod4)` | `0.06`, `dof=1` | — | `u_j mod 4 ⊥ e_j` (channel null) |
| `P(D=1 \| e)` , `e=0..3` | `.497, .499, .502, .499` | `1/2` | flat — 3-adic exponent gives no `D`-bias |
| 4-cell `P(D=1\|(e mod2,u mod4))` | `{1,0,0,1}` exactly | — | L7 deterministic |
| first-moment ratio | `0.99999979` | 1 | product formula = renewal, verified |

---

## 6. Verdict (the three asks)

| ask | answer | label |
|---|---|---|
| (a) new density bound from the joint constraint? | **No.** `freq(D=1)=E[1{u≡(−1)^e mod4}]`; the 3-adic factor acts as a Haar-preserving permutation of `(Z/4)^*`, so the `e`-law is annihilated and the density depends only on the cofactor mod-4 balance — symmetric, hence no one-sided bound. | `[PROVEN]` |
| (b) new characterization of WHY the coupling is tautological? | **Yes (sharper than prior).** New exact law L7 `D=1 ⟺ u≡(−1)^e mod4` makes `1{D=1}` a deterministic function of `(e mod2, u mod4)`; the 3-adic exponent enters only via the unit `(−1)^e`, which **cancels in the density**, leaving a single cofactor bit. The product formula is codimension-1 (first moment); the kernel is codimension-∞. | `[PROVEN]` |
| (c) re-derive the wall? | **Yes.** (K) `⟺ density{u_j ≡ (−1)^{e_j+1} mod 4} ≥ 1/2 ⟺ density{o_j≡3 mod4} ≥ 1/2` = 2-adic level-2 cylinder = AEV/Mahler. Gap to proof = single-orbit equidistribution of `o0=27` at mod 4. | `[PROVEN reduction]` |

### New asset banked `[PROVEN]`
**Joint `Z2×Z3` shallow/deep law:** `D_j = 1 ⟺ u_j ≡ (−1)^{e_j} (mod 4)` with `o_j=3^{e_j}u_j`,
`gcd(u_j,6)=1`, `e_j=D_{j−1}−1`. Equivalently `1{D_j=1}` is the deterministic 4-cell function of
`(e_j mod 2, u_j mod 4)`. **Density decomposition:** `freq(D=1) = Σ_{p} P(e≡p) P(u≡(−1)^p mod4 | e≡p)`, in
which the 3-adic exponent law is *additively annihilated* by the cofactor mod-4 balance — so the kernel
density is a single cofactor bit, the 3-adic place contributing zero.

### Genuinely new vs prior notes
- ADELIC_COUPLING / THREEADIC_SKEW established the coupling is an **isomorphism** of the obstruction
  (invertible valuation channel). THREEADIC_INTRATERM established `u_j ⊥ e_j` via a Haar-preserving
  **rotation** `3^{e+1} mod 2^k`. **This note sharpens both** to the *exact level-2 truth table* L7 and the
  *explicit density decomposition* showing the 3-adic exponent is not merely "isomorphic difficulty" but
  **additively null in the kernel density formula** — the cleanest possible statement that the 3-adic place
  carries zero density information. It also re-derives the wall as a **single cofactor mod-4 cylinder** and
  gives the dimension-count reason (codim-1 product formula vs codim-∞ kernel) the S-arithmetic
  self-consistency is a tautology, and disposes of the Hilbert-symbol/reciprocity route (quadratic, orthogonal).

### Why this confirms rather than breaches (honest)
The intra-term `Z2×Z3` data of one term is fully `[PROVEN]`-characterized (L1–L8), and the joint law is
*more* explicit than any prior note — yet it tightens the obstruction to a single cofactor bit whose
balance is exactly the open single-orbit equidistribution. The coupling that *exists* is annihilated by an
independence/balance that *is* the open core. Fully consistent with WEAPONS_AUDIT §1 (orbit-specific wall),
the β=+½ / specification impossibility meta-theorems (no structure-only certificate), REPELLER_ESCAPE
(symmetric repulsion, no one-sided drift), and the AEV/Mahler anchor.

## Sources
- Repo: `ADELIC_COUPLING.md` (§1a coupling, §1 product-formula = first moment), `THREEADIC_INTRATERM.md`
  (channel real but Haar-null, `u⊥e`), `THREEADIC_SKEW.md` (§2 invertible valuation channel = generator),
  `THREEADIC_ROTATION.md` (§4 3-adic congruence laws, `o mod3∈{0,1}`), `REPELLER_ESCAPE.md` (symmetric
  dual repulsion), `WEAKEST_SUFFICIENT.md` (§1,§3 one-character / mod-4 reductions), `WEAPONS_AUDIT_2026-06-29.md`
  (§3 hybrid #1, §5 S-arithmetic spec).
- Literature (repo knowledge, WebSearch not invoked): Furstenberg ×2,×3 (orbit-closure dichotomy, not
  pointwise); Rudolph–Johnson / Host / Lindenstrauss (measure rigidity, need positive-entropy *jointly*
  invariant measure our single orbit does not supply); Mahler 3/2 / Flatto–Lagarias–Pollington (gap ≥1/3,
  not density); AEV 2025 (arXiv:2510.11723, Conj 1.6 rational base) and Algom–Baker–Shmerkin 2025
  (arXiv:2504.18192) — the named open anchors, both one inch short on the two relevant axes. No
  "adelic/S-arithmetic self-consistency" mechanism (product formula / strong approximation / Hasse / Hilbert
  reciprocity) yields pointwise single-orbit density for a hyperbolic solenoid orbit; the amenable acting
  group `Z[1/6]⋊⟨3/2⟩` sits in the empty spot between the rigidity and the rotation/Weyl toolboxes
  (WEAPONS_AUDIT §5).

**No machine decided. No label upgraded.**
