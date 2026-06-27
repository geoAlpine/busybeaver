# The 2-adic→3-adic skew product of the induced map: explicit fiber, but the target is base-measurable (2026-06-28)

*Angle: track the induced odd map `o ↦ o' = 3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`, orbit `o0=27`,
JOINTLY in 2-adic and 3-adic coordinates via CRT, looking for a SKEW-PRODUCT structure with a
PROVABLY equidistributed base (rotation/Bernoulli) driving the other coordinate, and asking whether
the skew offers a provable base→fiber transfer for the SPECIFIC orbit or merely relabels the wall.
Also: reduced 6-coprime map `u = o/3^{v3(o)}`. Numerics `.venv` only (`threeadic_skew.py`), exact
big-int, 2·10^5 induced steps. Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

There **is** a genuine, clean skew product: the **2-adic dynamics on `Z_2^*` is the autonomous base**
(the `[PROVEN]` exact Bernoulli system, `INDUCED_RESIDUE_STRUCTURE.md`), and the **3-adic coordinate is
a driven fiber with an explicit affine fiber map** `o' mod 3^b = 3^{D-1}·(2^{-D} mod 3^b)·(3o-1) mod 3^b`,
a function of `(o mod 3^b, D)` only — confirmed deterministic numerically (`[S1c]`, 0 multi-image over
937 sampled `(residue,D)` classes) and the 3-adic side is **not** autonomous (`o mod 3^b` alone fails:
all 81 classes have ≥2 images, `[S1c]`). **But the skew offers NO provable base→fiber transfer for the
target — it relabels the wall.** The reason is sharp and `[PROVEN]`: the only fiber data the target reads
is the **valuation channel** `v3(o_{j+1}) = D_j − 1`, which is an **invertible re-encoding of the entire
base itinerary** (`D_j = v3(o_{j+1}) + 1`), NOT a coarser factor. So "3-adic density `{3|o_j} ≥ 1/2`" is
**literally** the base statement `freq(D≥2) ≥ 1/2`. The richer fiber object that a skew product *could*
have synchronized for free — the 3-adic **unit** part `u mod 3^c` — is **orthogonal to the target**
(the target is a function of the valuation alone). The reduced 6-coprime map
`u_{j+1} = (3^{D_{j-1}} u_j − 1)/2^{D_j}` is a clean delay-feedback recursion but reveals **no new
structure**: `u_j` is always 6-coprime, equidistributes mod small primes (χ²/dof ≈ 1), mixes fully, no
periodicity, no one-sided drift. The 3-power injected each step (`e_j = D_{j−1}−1`) is the previous depth
relabelled, carrying the same itinerary, not new information.

---

## 1. The skew-product structure, precisely `[PROVEN]`

State the joint coordinate `(o mod 2^a, o mod 3^b)` (CRT lift of `o`). Under `T`:

**Base (2-adic), autonomous.** The induced map descends to a well-defined map on `Z_2^*` (odd 2-adic
units); `o' mod 2^k` is a function of `o mod 2^{k+D}` and of nothing 3-adic. It is the `[PROVEN]` exact,
Haar-preserving, full-branch **Bernoulli** system (`INDUCED_RESIDUE_STRUCTURE.md §2`), measure-isomorphic
to the shift on the itinerary `(D_j)`, `D_j` i.i.d. geometric `P(D=d)=2^{-d}`. This is the only place the
"hardness" lives.

**Fiber (3-adic), driven — with an EXPLICIT fiber map `[PROVEN]`.** Because `3o−1 ≡ −1 (mod 3)`, the odd
part `m=(3o−1)/2^D` is coprime to 3, so
> `o' = 3^{D-1} m`, hence `v3(o') = D − 1`, and for any precision `b`:
> `o' mod 3^b = 3^{D-1} · (2^{-D} mod 3^b) · ((3o−1) mod 3^b)  (mod 3^b)`,

where `2` is a unit mod `3^b` so `2^{-D}` is well defined. **Every ingredient is a function of
`(o mod 3^b, D)` alone.** Thus the fiber update is

> `Φ_D : Z_3 → Z_3,  Φ_D(y) = 3^{D-1} · 2^{-D} · (3y − 1)`  (3-adically),  driven by the base symbol `D`.

This is a **skew product / random affine cocycle on `Z_3` over the Bernoulli base**: the base emits the
symbol `D_j`, and the fiber applies the affine map `Φ_{D_j}` (multiplier `3^{D_j-1}2^{-D_j}`, contraction
by `3^{D_j-1}` in `|·|_3`). `[PROVEN]`

**Numerical confirmation `[OBSERVED, exact]` (`threeadic_skew.py`).**
- `[S1a]` `v3(o_{j+1}) = D_j − 1` for all `j < 2·10^5` (0 exceptions). ✓
- `[S1b]` `e_j := v3(o_j) = D_{j-1} − 1` for all `1 ≤ j < 2·10^5`. ✓ (injected 3-power = previous depth−1)
- `[S1c]` 3-adic **non-autonomy**: sampling odd `o` (200k), fixing `o mod 3^4` gives **≥2 values** of
  `o' mod 3^4` for **all 81** classes ⟹ `o mod 3^b` alone does NOT determine `o' mod 3^b`.
- `[S1c]` adding the base symbol: `(o mod 3^4, D) → o' mod 3^4` is **deterministic** (937 classes, 0 with
  >1 image) ⟹ the explicit fiber map `Φ_D` is correct: the 3-adic coordinate is **fully driven by the
  2-adic base symbol `D`**.

> **`[PROVEN]` Genuine skew product: 2-adic base (autonomous, exact Bernoulli) → 3-adic fiber (driven by
> the base symbol `D` via the explicit affine map `Φ_D(y)=3^{D-1}2^{-D}(3y-1)`).**

---

## 2. Does the skew give a provable base→fiber transfer, or relabel the wall? `[PROVEN]` — relabel

This is the decisive ask. Two routes a skew product could offer:

**(a) Asymmetry hope: "provable base a.e.-equidistribution pushed onto the fiber for THIS orbit."**
The base is exact Bernoulli, but its equidistribution is **a.e.** (Birkhoff under Haar); `o0=27` is a
single point (measure zero). A skew product can sometimes synchronize a **contracting fiber** to a unique
stationary measure *regardless of the base orbit* (a pathwise/quenched statement), which would be a
genuine bypass. Here the fiber `Φ_D` is a `|·|_3`-contraction (multiplier `3^{D-1}`, `D≥1`), so its
**unit-part** coordinate does synchronize. **But this transfer is useless for the target** — see (b).

**(b) The target observable is BASE-measurable; the fiber valuation channel is a FULL re-encoding, not a
coarser factor `[PROVEN]`.** The target (`KERNEL_FINAL`, `MINPROP`) is
`density{3|o_j} + density{9|o_j} ≥ 1/2`, i.e. a function of the **3-adic valuation** sequence
`v3(o_j)`. But `[S1a]/[S2]`:
> `v3(o_{j+1}) = D_j − 1` is **invertible**: `D_j = v3(o_{j+1}) + 1`. `[S2]` verified for all `j<2·10^5`.

So the 3-adic valuation sequence is **not a proper (coarser) factor** of the base — it carries the
**entire** itinerary `(D_j)`, the full generating partition of the Bernoulli base. Consequently
`[S2]`:
- `density{3|o_j} = freq(D≥2)` (measured `0.49966 = 0.49966`, identical),
- `density{9|o_j} = freq(D≥3)` (measured `0.24888 = 0.24888`, identical),
- minimal prop `density{3|o}+density{9|o} = 0.74854` = `freq(D≥2)+freq(D≥3)`.

The fiber object that synchronizes for free (route (a), the 3-adic **unit** part `u mod 3^c`) is
**orthogonal** to this target: the target reads only the valuation, and the valuation = the base
itinerary. There is **nothing to transfer**: a fiber statement that helps would have to be about the unit
part, which the target never queries; the part the target queries is, verbatim, a base statement.

> **`[PROVEN]` The skew product is an ISOMORPHISM of the obstruction, not a reduction. The 2-adic base is
> the entire hard part; the 3-adic fiber's only target-relevant channel (the valuation) is the full base
> itinerary re-encoded. Base→fiber transfer offers no gain: it relabels `freq(D≥2)≥1/2` (single-orbit
> 2-adic equidistribution = AEV/Mahler wall) as the identical 3-adic density statement. The contracting
> fiber's free synchronization concerns the 3-adic UNIT part, which is orthogonal to the target.**

This sharpens `ADELIC_COUPLING.md §1a` ("isomorphism of obstructions") with the structural *reason*: the
valuation channel is a generator (full re-encoding), so no compression to a coarser, possibly-easier
factor exists.

---

## 3. The reduced 6-coprime map — no new structure `[PROVEN]/[OBSERVED]`

Factor `o = 3^e u`, `u` coprime to 6, `e = v3(o) = D_{prev}−1`. Since `o' = 3^{D-1} m` with `m` 6-coprime,
the reduced map is the clean **delay-feedback** recursion (`[S3]` verified, 0 exceptions):

> **`[PROVEN]` `u_{j+1} = (3^{D_{j-1}} u_j − 1) / 2^{D_j}`,**  `u_j` always coprime to 6
> (`[S3]`: # `u_j` divisible by 3 = **0**).

The injected 3-power exponent is exactly the **previous depth** `D_{j-1}` (since `e_j+1 = D_{j-1}`), and the
division is by the **current depth** `2^{D_j}`. The feedback is real but information-free: `D_{j-1}` is the
prior base symbol, so the recursion just re-expresses the same Bernoulli itinerary; it does **not** create
an autonomous lower-complexity system (`D_j` still depends on the 2-adic data of `o_j = 3^{e_j}u_j`).

**Probes of the reduced orbit `[OBSERVED]` (`[S3]`, 2·10^5 steps):**
- Uniformity mod small primes: χ²/dof = 0.485 (`mod 5`), 0.960 (`mod 7`), 0.765 (`mod 11`), 1.245
  (`mod 13`) — consistent with equidistribution, **no bias**.
- `u mod 7` transitions: 45/49 ordered pairs realized — **full mixing**, no forbidden-transition / hidden
  1-D dynamics.
- No periodicity found; `mean e_j = 0.99628 = mean D − 1`; `mean D = 1.99627` (Haar 2).
- No one-sided drift: `Σ D = 399254`, `log o_n ≈ log o0 + (ΣD)log(3/2) = 161886.86` (first-moment
  identity, unchanged).

> **`[OBSERVED, consistent]` The 6-coprime reduced map equidistributes and mixes exactly as a generic
> orbit would — but this is OBSERVED for `o0=27`, not forced by the structure (the reduced map is still a
> shift driven by the same base; uniformity is the genericity statement, not a proof of it). No periodicity,
> bias, one-sided invariant, or drift. No new attack surface.**

---

## 4. Verdict (the three asks)

| ask | answer | label |
|---|---|---|
| Precise skew-product structure? | **Genuine skew product**: 2-adic base on `Z_2^*` is **autonomous** (exact Bernoulli, `[PROVEN]`) and emits symbol `D`; 3-adic fiber is **driven** by the explicit affine cocycle `Φ_D(y)=3^{D-1}2^{-D}(3y-1)`, with `o' mod 3^b = F(o mod 3^b, D)` deterministic (`[S1c]`) and `o mod 3^b` alone NOT autonomous (`[S1c]`). | `[PROVEN]` |
| Provable base→fiber transfer for `o0=27`, or relabel? | **Relabel — no gain.** The target reads only the valuation channel `v3(o_{j+1})=D_j−1`, an **invertible re-encoding of the full base itinerary** (NOT a coarser factor), so `density{3|o}≥1/2 ⟺ freq(D≥2)≥1/2` verbatim. The contracting fiber's free synchronization is about the 3-adic **unit** part, **orthogonal** to the target. Isomorphism of the obstruction, not a reduction. | `[PROVEN]` |
| Does the 6-coprime reduced map `u_{j+1}=(3^{D_{j-1}}u_j−1)/2^{D_j}` reveal new structure? | **No.** Clean delay-feedback (3-power injected = previous depth), `u_j` always 6-coprime, but equidistributed/mixing with no periodicity, bias, invariant, or drift — generic behavior OBSERVED, not forced; same base, same wall. | `[PROVEN]`/`[OBSERVED]` |

### New asset banked `[PROVEN]`
*Explicit 3-adic fiber cocycle over the exact-Bernoulli 2-adic base:*
`o' mod 3^b = 3^{D-1}·(2^{-D} mod 3^b)·(3o−1)  (mod 3^b)`, `Φ_D(y)=3^{D-1}2^{-D}(3y−1)`, a `|·|_3`-contraction
driven by the base symbol `D`. *Reduced 6-coprime recursion* `u_{j+1}=(3^{D_{j-1}}u_j−1)/2^{D_j}`. *And the
structural reason the 3-adic re-encoding gives no compression:* the valuation channel `v3(o_{j+1})=D_j−1` is
**invertible**, hence a generating (full) factor, not a coarser one.

### Why this confirms rather than breaches (honest)
A skew product helps only when the target observable is fiber-measurable and the fiber synchronizes
regardless of the base orbit. Here the synchronizing fiber object (3-adic **unit** part) is orthogonal to
the target, while the target's actual channel (the **valuation**) is the full base itinerary. So the only
hard input is the base's **single-orbit** equidistribution of `o0=27` — the a.e. (Birkhoff) result is
available, the this-point upgrade is exactly the AEV/Mahler 3/2 wall (`KERNEL_FINAL.md`,
`ADELIC_COUPLING.md`). The skew structure is a sharper, citable identification (explicit fiber cocycle),
not a bypass.

### Live next angle (not yet mined)
The fiber cocycle `Φ_D` is a `|·|_3`-contraction with multiplier `3^{D-1}2^{-D}`; its **unit-part**
stationary law on `Z_3^*` may be provably equidistributed for `o0=27` *independently of base genericity*
(quenched synchronization of a contraction over any base orbit). That would be a genuine pathwise transfer
— but it certifies the 3-adic UNIT part, which is orthogonal to the valuation target. The only way it
becomes load-bearing is if some equivalent of the stopping criterion can be rewritten as a **unit-part**
(not valuation) statement. Current framing says it cannot (target = valuation = base itinerary); whether a
*different* sufficient criterion exists that is unit-part-measurable is the one un-mined micro-question.

Script: `threeadic_skew.py`. Not committed.
