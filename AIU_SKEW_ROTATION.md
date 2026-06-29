# AIU via skew-product over the uniquely-ergodic fiber rotation R_2 (2026-06-30)

*WEAPONS_AUDIT style. NEW angle on AIU (`NEWMATH_ADELIC_RIGIDITY` §2, `AIU_JOININGS`): treat A on the
A-stable F_3=Q_3 leaf as a SKEW PRODUCT over the within-leaf rotation R_2: x->2x on Z_3^* (uniquely ergodic
because 2 is a topological generator of Z_3^*). Ask whether A-invariance + unique ergodicity of the fiber
rotation FORCES the F_3-leaf conditionals to be Haar (= AIU), or whether the adelic coupling (renewal
cocycle, v_3=D-1) blocks it. This is a fibered-system / Anzai-Furstenberg question, NOT the
disintegration/EKL/joinings approach already exhausted. SOUNDNESS PARAMOUNT: every claim labelled; no claim
to prove (K); no label upgraded. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`. NOT committed.*

---

## 0. ONE-LINE VERDICT

**A genuinely IS a skew product over the within-leaf rotation R_2 -- but the base of that skew product is
the A-CONTRACTING (dissipative) radial direction, so the unique ergodicity of R_2 is INERT and does NOT
force Haar fibers; the adelic coupling blocks it, and the block is exactly (K).** Precisely `[PROVEN]`: in
the coordinates `Q_3^* = 3^Z x Z_3^*` (radius `v=v_3`, angle `u in Z_3^*`), `A=x(3/2)` acts as the skew
product `A(v,u)=(v+1, R_2^{-1}u)` with `R_2: u->2u` (the M_2 rotation, `|2|_3=1`) and a CONSTANT cocycle.
The fiber rotation `R_2` is uniquely ergodic (2 is a topological generator of `Z_3^*`, Weyl) `[PROVEN-in-lit]`.
The Anzai/Furstenberg/Veech theorem that "skew product over a (uniquely ergodic, measure-preserving) base
with an ergodic compact-group fiber action has Haar fibers" requires a FINITE INVARIANT MEASURE ON THE
BASE. Here the base map `v->v+1` is the A-contraction of `F_3` (`|3/2|_3=1/3`): A sends each 3-adic sphere
`|y|_3=3^{-k}` strictly to the next sphere `k+1` and NEVER returns -- a dissipative `Z`-translation with NO
invariant probability measure. So A iterates `R_2` on a fixed sphere exactly ZERO times; the `n->infty`
unique-ergodicity payoff of `R_2` is never invoked. The only thing that returns the orbit to a sphere is the
global renewal `Gamma=Z[1/6]` translation (3-adic addition `y->y+r`, the denominator-clearing), whose
angular action is a LEAF-DEPENDENT additive shift `c(b)` -- NOT a rotation -- governed by the exact coupling
`v_3(o_{j+1})=D_j-1`. That `c(b)` is the 2-adic depth `D` = the (K) data. Verdict (c): the skew-product /
unique-ergodicity route **reduces AIU to (K)** via a new, sharp mechanism (dissipative base kills the
isometric-extension theorem; recurrence is supplied only by the D-coupled renewal cocycle). No machine
decided. No label upgraded.

---

## 1. The within-leaf skew-product coordinates [PROVEN]

The A-stable leaf is `F_3=Q_3` (A contracts it, dilation `|3/2|_3=1/3`). Split the multiplicative structure
`Q_3^* = 3^Z x Z_3^*` by `y = 3^v u`, `v=v_3(y) in Z` (radius), `u in Z_3^*` (angle = the unit / sphere
coordinate). The three host maps act on `(v,u)` as `[PROVEN]`:

| map | `|.|_3` | radius `v` | angle `u in Z_3^*` |
|---|---|---|---|
| `x2 = M_2`   | `1`   | `v` (fixed) | `u -> 2u   = R_2 u`    (rotation; `2 in Z_3^*`) |
| `x3 = M_3`   | `1/3` | `v -> v+1`  | `u` (fixed)            (pure radial shift; `3=3*1`) |
| `A = x(3/2)` | `1/3` | `v -> v+1`  | `u -> 2^{-1}u = R_2^{-1}u` |

So with `S: v->v+1` on the base `Z` and `R_2: u->2u` on the fiber `Z_3^*`,
> **`A(v,u) = (Sv, R_2^{-1} u)` -- a skew product over the radial base, with CONSTANT cocycle** (it is
> literally the product `S x R_2^{-1}`; the within-leaf cocycle is leaf-INdependent). `[PROVEN]`

`R_2` is the neutral M_2 rotation (the AIU direction, `AIU_JOININGS` §1(N)). It is **uniquely ergodic**: 2
is a primitive root mod `3^k` for all `k`, so `<2>` is dense in `Z_3^*`, and rotation of a compact abelian
group by a topological generator is uniquely ergodic with unique invariant measure = Haar on `Z_3^*` (Weyl
equidistribution). `[PROVEN-in-lit]` AIU (`AIU_JOININGS` §2) = "the F_3-leaf conditionals are
`Z_3^*`-rotation-invariant = Haar on each sphere" = "the fiber conditionals of `mu` are Haar." So AIU is
**exactly** the assertion that this skew product has Haar fibers.

---

## 2. THE QUESTION: does A-invariance force Haar fibers?

**2.1 When unique ergodicity DOES force Haar fibers (the theorem we hoped to invoke).** Let `T(b,y)=(Sb,
phi(b)+R y)` be a skew product on `(B,nu) x G`, `G` a compact group, `R` a fixed rotation, `(B,S,nu)` a
probability-preserving (ideally uniquely ergodic) base. The Anzai / Furstenberg / Veech isometric-extension
theory `[PROVEN-in-lit]`: every `T`-invariant measure disintegrates over the base ergodic components with
fibers that are translates of Haar on a closed subgroup `H<=G`; if additionally the fiber rotation is
ergodic (here `R_2` uniquely ergodic on `G=Z_3^*`) and the cocycle is not reducible into a proper subgroup,
the fibers are FULL Haar. The crisp degenerate case (constant cocycle, fiber-PRESERVING base `S=id`):
`T=id x R_2`, and unique ergodicity of `R_2` forces every invariant `mu` to have `mu_b = Haar` for a.e. `b`
(disintegrate over the preserved fibers; each fiber-conditional is `R_2`-invariant hence Haar). **This is a
real theorem and it WOULD give AIU -- if its hypothesis held.**

**2.2 Why the hypothesis FAILS here (the decisive obstruction) `[PROVEN]`.** The hypothesis is a FINITE
INVARIANT MEASURE ON THE BASE. Our base is `(Z, S: v->v+1)` -- the radial coordinate `v=v_3` -- and this is
the A-CONTRACTING direction of the hyperbolic A: `|3/2|_3 = 1/3`, so A maps the sphere `{|y|_3=3^{-k}}`
strictly onto the sphere `{|y|_3=3^{-(k+1)}}` and never back. The base shift `v->v+1` is a translation of
`Z` -- **dissipative, with NO invariant probability measure** and not uniquely ergodic. Two equivalent ways
to see the failure:
- **(i) Base has no invariant probability.** There is nothing to disintegrate over; the Anzai/Furstenberg
  conclusion ("a.e.-base fiber is Haar") is vacuous because there is no base measure.
- **(ii) The fiber rotation is iterated ZERO times on any sphere.** Unique ergodicity of `R_2` is an
  `n->infty` statement on a FIXED sphere `Z_3^*` (`(1/n)sum_{k<n} f(R_2^k u) -> int f dHaar`). But A leaves
  every sphere immediately (`v->v+1`); the A-orbit visits each sphere exactly once. So A never accumulates
  iterates of `R_2` on a sphere, and the unique-ergodicity equidistribution is **never triggered**. The
  isometric/uniquely-ergodic structure is genuinely present and genuinely INERT. `[PROVEN]`

So: **A-invariance ALONE does NOT force Haar fibers via the skew-product / unique-ergodicity route.** The
neutral rotation that AIU needs is autonomous and uniquely ergodic, but A rides it while simultaneously
contracting the base, so the standard isometric-extension theorem has no purchase. (This is the
fibered-system shadow of `AIU_JOININGS` §3.3: the AIU direction is neutral, but here we see *why* even its
unique ergodicity cannot be cashed -- A spends no recurrent time on any fiber.)

---

## 3. The honest crux: the renewal cocycle is the (K) data

The finite A-invariant `mu` does not come from the single-leaf action (dissipative, §2); it comes from the
GLOBAL renewal-normalized orbit (Krylov-Bogolyubov, `NEWMATH_ADELIC_RIGIDITY` §1.3). The mechanism that
returns the orbit to a sphere -- the only source of recurrence -- is the `Gamma=Z[1/6]` translation
`y -> y+r` that clears denominators at each induced step. Two `[PROVEN]` facts pin its nature:

1. **The renewal acts on the angle as a leaf-DEPENDENT additive shift, not a rotation.** 3-adic addition
   `3^v u + r` does not respect the `3^Z x Z_3^*` splitting: the new angle depends nonlinearly on `(v,u,r)`.
   Exact within-step law (numerics §4, 100% match): the angle update over one induced step is
   `u_{j+1} = (3 o_j - 1) * 2^{-D_j}  (mod 3^k)`, i.e. **rotation by `2^{-D_j}` (a power of `R_2`) COMPOSED
   with the additive renewal term `-1+3o_j`**. The `+3o_j` term is the leaf-dependent cocycle `c(b)` the
   skew-product question asks about; numerics show it is felt beyond `mod 3` (pure-rotation match decays
   `1 -> 1/2 -> 1/4 -> 1/8` at `mod 3,9,27,81`). So `c(b)` is genuine and leaf-dependent. `[PROVEN/OBSERVED]`
2. **The rotation EXPONENT is the 2-adic depth `D`, and the radial return is `v_3=D-1`.** The number of
   `R_2`-clicks the orbit takes per induced step is exactly `D_j=v_2(3o_j-1)` (geometric, mean 2), and the
   sphere it lands on is `v_3(o_{j+1})=D_j-1` (`ADELIC_COUPLING` §1a). So **both the angular rotation amount
   and the radial return are slaved to `D`** -- the 2-adic depth, which is the (K) statistic. `[PROVEN]`

**Conclusion `[PROVEN-reduction]`.** The skew-product picture localizes AIU to: "do the fiber conditionals
of `mu` come out Haar?" The fiber rotation `R_2` would force this **iff** it were autonomously iterated
under a finite base measure -- but it is not (§2); the actual iteration count and the base recurrence are
both the cocycle `D=v_2(3o-1)`. Equidistribution of the fiber conditional to Haar is therefore EQUIVALENT to
the orbit's `D`-sequence (equivalently its 2-adic cylinder frequencies / 3-adic divisibility densities)
equidistributing -- which is exactly (K) / the open Mahler-3/2 statement (`ADELIC_COUPLING` §3). The
autonomous uniquely-ergodic `R_2` is real but cannot act autonomously: A binds its iteration count to `D`.
**The coupling blocks the route, and the block IS (K).** No reduction in difficulty; a sharp new
identification of *where* unique ergodicity fails to bite.

**Honest danger checked (item 3 of the brief).** Is the fiber action the autonomous uniquely-ergodic `R_2`
(=> AIU) or non-autonomous (=> (K))? Answer: **non-autonomous.** The fiber map per induced step is
`R_2^{D_j}` with `D_j` the 2-adic depth -- a `D`-driven, hence (K)-driven, rotation-time -- composed with
the additive renewal `c(b)`. It is NOT the autonomous `R_2` whose unique ergodicity could be cashed.

---

## 4. NUMERICS [OBSERVED] (`skew_rot.py`, exact big-int, N=1e5 induced steps, seed o_0=27)

- **Coupling / depth law:** `freq(D=k)` = `0.4995, 0.2504, 0.1252, 0.0629,...` (geometric `2^{-k}`, mean 2);
  `freq(v_3(o_j)=k)` identical shifted by one -- confirms `v_3(o_{j+1})=D_j-1` and that the radial return is
  `D`-driven. `[OBSERVED]`
- **Within-leaf transition law (the skew-product cocycle):** the prediction
  `u_{j+1} == (3 o_j - 1)*2^{-D_j} (mod 3^k)` matches **100000/100000 = exact** for `k=1,2,3,4`. So the angle
  update is rotation by the `R_2`-power `2^{-D_j}` COMPOSED with the additive renewal term. `[OBSERVED, exact]`
- **The additive shift `c(b)` is leaf-dependent (not a pure rotation):** dropping the `+3o_j` term
  ("pure-rotation" prediction `-2^{-D_j}`) matches `100%` at `mod 3` (the `3o_j` term vanishes `mod 3`) but
  only `50052, 25011, 12488` (`~1/2,1/4,1/8`) at `mod 9,27,81`. So `c(b)` genuinely depends on the base
  point beyond the trivial residue -- confirming a leaf-DEPENDENT cocycle, not the autonomous `R_2`.
  `[OBSERVED]`
- **Orbit-point angular marginal is NON-Haar, slaved to `D`:** pooled 3-adic unit part `u(o_j)` over the
  orbit is far from uniform on `(Z/3^k)^*`: `mod 3` gives frequencies `~(2/3, 1/3)` (not `1/2,1/2`), `chisq`
  enormous (`1.1e4` at `mod 3`, growing). The `mod 3` ratio equals `P(D odd):P(D even) = 2:1` (since
  `u(o_{j+1}) = -2^{-D} mod 3` and `2^{-D} mod 3` alternates with parity of `D`). The angular coordinate of
  the orbit POINTS is dictated by `D`. `[OBSERVED]`

**Honest caveat (pointwise vs. measure).** This non-Haar marginal is for the diagonal-embedded integer
orbit points (a `Haar`-null set; the (T1)-(T2) pointwise lock, `NEWMATH_ADELIC_RIGIDITY` §3.3), NOT for the
ambient limit measure `mu`'s fiber conditionals. It does **NOT** disprove AIU; it CONFIRMS the mechanism --
the orbit never freely rotates within a leaf, so the unique ergodicity of `R_2` is bypassed and the angular
data is the `D` (=(K)) data. No one-sided margin; decides nothing about (K). `[OBSERVED]`

---

## 5. HONEST VERDICT

| question | verdict | label |
|---|---|---|
| Does A act on F_3 as a skew product over `R_2`? | **YES**, `A(v,u)=(v+1, R_2^{-1}u)` in `Q_3^*=3^Z x Z_3^*`; constant within-leaf cocycle (literally `S x R_2^{-1}`) | `[PROVEN]` |
| Is the fiber rotation `R_2` uniquely ergodic? | **YES** (2 a topological generator of `Z_3^*`; Weyl) | `[PROVEN-in-lit]` |
| Does A-invariance + UE of `R_2` force Haar fibers (= AIU)? | **NO.** The skew-product base `v->v+1` is the A-contraction of `F_3`: dissipative, no invariant probability, A iterates `R_2` zero times on any sphere -- UE is INERT | `[PROVEN -- obstruction]` |
| Is the fiber action autonomous `R_2` or non-autonomous? | **Non-autonomous:** per-step rotation is `R_2^{D_j}` with `D_j=v_2(3o_j-1)`, composed with a leaf-dependent additive renewal `c(b)` | `[PROVEN]` |
| Does the adelic coupling block it? what is the block? | **YES.** Recurrence comes only from the renewal `Gamma`-translation; both the rotation amount and the radial return are the depth `D` = the (K) statistic | `[PROVEN]` |
| Net | **(c) reduces to (K)** -- via a NEW, sharp mechanism: dissipative base kills the isometric-extension theorem, recurrence is the `D`-coupled renewal cocycle | `[honest]` |

**Outcome = (c) reduces to (K).** Not (a) (no AIU and no partial unconditional advance via unique
ergodicity -- the route is structurally inert), not (b) (the characterization "AIU <=> fiber conditionals
Haar" was already in `AIU_JOININGS` §2; what is new is the *reason* it cannot be cashed). The genuinely new,
`[PROVEN]` contribution: **the AIU direction's unique ergodicity fails to force Haar not because of low
entropy (EKL story, `AIU_JOININGS` §3) but because A binds the fiber rotation's iteration count to the
contracting base -- the orbit spends bounded (`~D`, geometric mean 2) time per fiber and never realizes the
`n->infty` equidistribution, and the only recurrence (the renewal cocycle) carries exactly the `D`=(K)
data.** Two independent obstructions to the same target now isolated: (neutral=>no entropy leverage)
[joinings note] and (contracting base=>no isometric-extension leverage) [this note]; both say the missing
invariance lives on the one direction A cannot recur on.

**Exact gap.** AIU = "the skew product `A(v,u)=(v+1,R_2^{-1}u)` has Haar fibers for the limit measure." The
skew-product/UE theory delivers Haar fibers only over a finite-invariant-measure base; A's base is its own
contraction, so the theory is silent, and the substitute recurrence (renewal cocycle, rotation-time `D`) is
the open (K)/Mahler-3/2 equidistribution. Unproven and (K)-hard, unchanged.

---

## Sources
- S. Anzai, *Ergodic skew product transformations on the torus*, Osaka Math. J. **3** (1951) -- invariant
  measures of skew products over rotations have homogeneous (Haar-coset) fibers. `[PROVEN-in-lit]`
- H. Furstenberg, *Strict ergodicity and transformation of the torus*, Amer. J. Math. **83** (1961) -- unique
  ergodicity of skew products over a uniquely ergodic base; cocycle/coboundary criterion; base+Haar measure.
  `[PROVEN-in-lit]`
- H. Furstenberg, *The structure of distal flows* (1963) / isometric (compact-group) extensions: invariant
  measures of an isometric extension disintegrate with Haar-coset fibers over each base ergodic component
  -- REQUIRES a probability-preserving base. `[PROVEN-in-lit]`
- W. Veech, *Strict ergodicity in zero dimensional dynamical systems and the Kronecker-Weyl theorem mod 2*,
  Trans. AMS **140** (1969) -- minimal/uniquely-ergodic skew products, Veech criterion. `[PROVEN-in-lit]`
- H. Weyl, equidistribution: rotation of a compact abelian group by a topological generator is uniquely
  ergodic (Haar the only invariant measure). `[PROVEN-in-lit]`
- Repo: `AIU_JOININGS.md` (AIU <=> F_3 conditionals `Z_3^*`-rotation-invariant; neutral direction; §3
  entropy obstruction), `NEWMATH_ADELIC_RIGIDITY.md` (§1.3 KB limit, §3.3 pointwise vs measure),
  `ADELIC_COUPLING.md` (`v_3(o_{j+1})=D_j-1`, §3 Mahler-3/2 = (K)), `INTRATERM_ADELIC_MINING.md` (T1-T2).
- Numerics: `skew_rot.py` (exact big-int, N=1e5): within-leaf law `u_{j+1}=(3o_j-1)2^{-D_j}` exact (100%);
  leaf-dependent cocycle (pure-rotation match decays `1->1/2->1/4->1/8`); angular marginal non-Haar (`mod 3`
  ratio `2:1` = `P(D odd):P(D even)`).

No machine decided. No label upgraded.
