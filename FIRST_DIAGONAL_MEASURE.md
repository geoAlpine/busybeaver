# Can ANY non-degenerate measure / renormalization be attached to the single orbit 8·3ⁿ to give a handle on the BARE FIRST DIAGONAL d_n = bit_{n+k}(⌊8(3/2)ⁿ⌋)? (2026-06-29)

*Assigned task: the second diagonal σ_n carries the Rajchman measure ν_{2/3} (sum-structure ⇒ annealed
control); the first diagonal d_n = bit_{n+k}(8·3ⁿ) = bit_k(⌊8(3/2)ⁿ⌋) is the DEGENERATE b_j≡0 corner with
attached measure δ₀ (ν̂≡1, no decay). Decisive question: can the **rotation/renormalization structure**
(3/2)^{n+1}=(3/2)(3/2)ⁿ attach a NON-DEGENERATE measure to replace the missing ν — a partial — or is the δ₀
degeneracy INTRINSIC (any attached measure is Haar=open or δ₀=trivial)? Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/first_diag_measure.py`, exact big-int orbit +
mpmath(dps≤200), N≤5·10⁴, ≈70s. Every claim labelled. Zero false proofs. NOT committed.*

---

## 0. One-line verdict

**A non-degenerate Rajchman measure CAN be attached — but only by SMEARING the fixed constant 8, which gives
exactly the a.e.-α (Koksma/AEV) partial and never localizes to the single orbit. So the δ₀ degeneracy is
REMOVABLE at the family/annealed tier and INTRINSIC at the single-orbit tier, with a precise reason: among the
natural attachable measures, BIT-SENSITIVITY and SINGLE-ORBIT LOCALIZATION are mutually exclusive.** `[OBSERVED
synthesis + PROVEN parts]` The 2nd diagonal's measure ν_{2/3} comes from a **sum** that varies the parities; the
1st diagonal has no sum — its only non-trivial measure comes from the **multiplier/rotation** axis, namely the
law ρ of α in the family α(3/2)ⁿ. For any absolutely-continuous ρ the annealed first-diagonal Weyl sum is
`ρ̂(h(3/2)ⁿ/2^{k+1}) → 0` by **Riemann–Lebesgue** `[PROVEN, this note]`, upgrading (Koksma 1935) to a.e.-α
equidistribution of `{α(3/2)ⁿ}` hence a.e.-α balance of **every** diagonal bit `[PROVEN-in-lit]` — the
rotation-structure counterpart of ν_{2/3}. **But this decay is base-independent (it needs only that ρ is a.c.,
NOT that 3/2 is non-Pisot), precisely because the constant has been smeared: freezing ρ→δ₈ kills it.** Every
measure that genuinely localizes to the one orbit α=8 is either δ₀ (sum axis, ν̂≡1, no decay), the Parry/β-map
eigenmeasure (renormalization axis — non-degenerate WITH a spectral gap 0.27 but **bit-blind**, it is the
real-place projection that discards the carry), or the orbit's own empirical/scenery measure, **whose being
non-trivial = Haar is literally (K) = Mahler** (circular/open). Numerics confirm all four: T2 δ₀ stays exactly
1.000 while the multiplier-annealed sum falls to the grid floor; T1 the quenched (α=8) empirical Fourier rides
the √N floor (Mahler); T3 ν̂_{2/3} shows genuine (non-Pisot) exponential Rajchman decay that T2 mimics only by
smearing. **No machine decided. No label upgraded.**

---

## 1. The two attachment axes — the first diagonal lives on the rotation axis, not the sum axis

The shared family is `bit_k(⌊α(3/2)ⁿ⌋)` (the AEV/Mahler digit object, `DIGITS_OF_3N §1`, AEV Conj 1.6;
`TWO_DIAGONAL_COMPARISON §1a`). Two distinct ways a **measure** can enter:

- **SUM axis (the 2nd diagonal's axis).** `σ_n = bit_k(⌊α_n^σ(3/2)ⁿ⌋)`, `α_n^σ = (1/3)Σ_{j<n} b_j(2/3)^j`.
  Varying the parities `b_j` makes `α_n^σ` sweep the **support of the Bernoulli convolution ν_{2/3}**; iid `b_j`
  realises ν_{2/3} itself, whose `ν̂_{2/3}(ξ)→0` is PROVEN Rajchman because **1/λ = 3/2 is non-Pisot**
  (Erdős–Salem; `SECOND_DIAGONAL_RAJCHMAN §1`, `NONPISOT_FOURIER_CHAIN` Link B). The 1st diagonal is the
  **b_j≡0 vertex** of this same family: the sum collapses, `α_n^σ → 0`, ν_{2/3} → **δ₀**, `δ̂₀≡1`, no decay.
  This is the established degeneracy (`SECOND_DIAGONAL_RAJCHMAN §2`). On the sum axis the first diagonal is
  irreparably measure-free.

- **ROTATION / MULTIPLIER axis (the new axis for the 1st diagonal).** The first diagonal's constant is the
  *leading* one, `α = 8`, and the only nontrivial way to attach a measure is to put a law **ρ on α itself** in
  the family `α(3/2)ⁿ`, exploiting the renormalization `(3/2)^{n+1} = (3/2)·(3/2)ⁿ` (a **fast rotation in α**).
  This is the axis the task asks about. It is genuinely different from the sum axis and it is **non-empty**.

> **The structural point:** ν_{2/3} comes from the 2nd diagonal's *sum* over parities; the 1st diagonal has no
> sum to vary, so its measure must come from the *rotation* over multipliers. §2 shows that measure exists and
> is Rajchman; §5 shows why it cannot be localized to α=8.

---

## 2. `[PROVEN]` A non-degenerate Rajchman measure DOES attach via the rotation axis — the a.e.-α partial

Fix an absolutely-continuous probability measure ρ on multipliers (e.g. `ρ = Unif[4,8]`, density bounded).
The annealed first-diagonal pure-phase Weyl sum is, by definition of the pushforward and Fubini,

> **`[PROVEN]` Rotation-annealed identity.**
> `E_{α∼ρ}[ e(h·α(3/2)ⁿ) ] = ρ̂( h(3/2)ⁿ )`, the Fourier transform of ρ at the geometric frequency
> `h(3/2)ⁿ → ∞`. Since ρ is absolutely continuous, **Riemann–Lebesgue ⇒ `ρ̂(h(3/2)ⁿ) → 0`** for every
> integer `h≠0`. (For `Unif[A,B]`: `|ρ̂(ξ)| = |sin(π(B−A)ξ)/(π(B−A)ξ)| ≲ 1/((B−A)|ξ|)`, i.e.
> **polynomial-in-ξ = exponential-in-n** decay `∼ (3/2)^{−n}`.)

This is a **genuine non-degenerate measure attached to the first-diagonal family**, replacing the missing ν: ρ
is any a.c. law, `ρ̂` is Rajchman, and the resulting annealed diagonal equidistributes. The standard
variance + Borel–Cantelli upgrade of these Weyl sums is **Koksma's theorem (1935)**:

> **`[PROVEN-in-lit]` a.e.-α equidistribution.** For every fixed `θ>1` and **Lebesgue-a.e.** `α`, the sequence
> `{α θⁿ}` equidistributes mod 1; hence for a.e. α **every** diagonal bit `bit_k(⌊α(3/2)ⁿ⌋)` is asymptotically
> balanced. (Andrieu–Eliahou–Vivion arXiv:2510.11723 prove the stronger a.e.-α **normality** of `⌊α(3/2)ⁿ⌋`;
> Conj 1.6 = the all-α statement that would include α=8.)

So the rotation axis converts "no measure / δ₀" into a **real Rajchman handle and a real (a.e.-α) partial** —
the precise rotation-structure analog of the sum-structure ν_{2/3}.

> **CRUCIAL caveat that makes it only a.e. (the key new observation).** The decay `ρ̂(h(3/2)ⁿ)→0` uses **only
> that ρ is absolutely continuous**. It is **base-independent**: it would hold verbatim for `θ=golden ratio`
> (Pisot!) or any `θ>1`. It does **NOT** use that 3/2 is non-Pisot. Contrast the 2nd diagonal, where the decay
> of ν̂_{2/3} is **forced by the arithmetic of 3/2** (non-Pisot) on a **fixed** measure. The 1st-diagonal
> measure decays for a *trivial* reason (we smeared the constant) — and smearing the constant is exactly the
> step that detaches the result from the single orbit. **The arithmetic of 3/2 has been bypassed, not used —
> which is the signature of an a.e., not a pointwise, statement.**

---

## 3. The renormalization axis taken literally: Parry/β-map measure — non-degenerate, has a gap, but BIT-BLIND `[PROVEN-in-lit]`

The most literal "renormalization" reading of `(3/2)^{n+1}=(3/2)(3/2)ⁿ` is the **β-transformation**
`T_β x = (3/2)x mod 1`, whose transfer (Perron–Frobenius) operator has a **non-degenerate** invariant
eigenmeasure — the **Parry/Gel'fond measure** (a.c., explicit density) — and a genuine **spectral gap**
(`|λ₂|=0.730`, gap 0.27; `mahler_equidistribution_attack §9`). This is exactly a "transfer operator with a
non-degenerate spectral measure." Why it gives no handle on `d_n`:

- The orbit `{8(3/2)ⁿ}` is **NOT** a `T_β` orbit: the exact recurrence is the **skew product**
  `x_{n+1} = {(3/2)x_n + ½·ε_n}`, `ε_n = ⌊8(3/2)ⁿ⌋ mod 2` = the **carry/diagonal bit itself**
  (`mahler §9`, generalising `{(3/2)ⁿ}`). The β-map is the **real-place projection that discards the carry**.
- Two-place picture (`mahler §9`): `×(3/2)` factors as (real β-map: **has the gap, bit-blind**) × (2-adic
  isometry `×3`, `|3|₂=1`: **carries every bit, zero entropy, no gap**). The Parry measure lives on the
  gap-bearing real factor and **says nothing about the diagonal bit** read off the rigid 2-adic factor.

> So the renormalization axis **does** supply a non-degenerate measure with a spectral gap — but it is the
> WRONG coordinate: bit-blind. The Parry measure is non-degenerate and localized to the dynamics, yet
> orthogonal to `d_n`. (Same conclusion as `THERMO_FORMALISM §2.1`: the flow/β operator is the lattice/blind
> one; the bit-sensitive operator is the self-similar Fourier one of §2, whose decay is the annealed/a.e. tier.)

---

## 4. The scenery / empirical measure of the single orbit = (K) (circular) `[OPEN]`

The one measure truly attached to the single orbit is its **empirical (scenery) measure**
`μ_N = (1/N) Σ_{n<N} δ_{{8(3/2)ⁿ}}`. Its weak-* limit points are `T_β`-skew-invariant; the β-shift has a huge
simplex of invariant measures (Parry/MME, periodic-orbit point masses, …). **Which one μ_N converges to is the
entire problem:** `μ_N → Lebesgue` (equiv. the diagonal bit equidistributes) **IS** statement (K) = Mahler 3/2
/ AEV at α=8. Asserting the empirical measure is non-trivial-and-Haar to get a handle is **circular**
(`mahler §10`: the orbit-closure measure being Haar is the open object). T1 below shows μ_N *numerically*
approaches Lebesgue (Fourier coeffs ride the √N floor) — but "numerically Haar" ≠ "provably Haar" = the wall.

---

## 5. Removable or intrinsic? The trichotomy and the bit-sensitivity ⊥ localization dichotomy `[OBSERVED synthesis]`

Collecting the natural attachable measures for `d_n`:

| axis | measure attached to the *family* | non-degenerate? | decays (Rajchman)? | **bit-sensitive?** | **localizes to α=8 / one orbit?** |
|---|---|---|---|---|---|
| SUM (b_j) | ν_{2/3} → **δ₀** at the vertex | δ₀: no | δ̂₀≡1: **no** | yes | yes (but δ₀, vacuous) |
| ROTATION (ρ on α) | **ρ̂** (any a.c. ρ) `[§2]` | **yes** | **yes** (Riemann–Lebesgue) | **yes** | **no** (smears the constant) |
| RENORMALIZATION (β-map) | **Parry/Gel'fond** `[§3]` | **yes** (gap 0.27) | yes (gap) | **NO** (bit-blind) | yes (the dynamics) |
| SCENERY (empirical) | `lim μ_N` `[§4]` | =Haar ⟺ (K) | =(K) | yes | yes, **but = the open object** |

> **The dichotomy (the precise reason the degeneracy is intrinsic at the orbit tier).** Read the last two
> columns: **no row is simultaneously bit-sensitive, decaying, AND localized to the single orbit.** Every
> measure that *sees* the diagonal bit and *decays* (ROTATION ρ̂; ν_{2/3}) achieves it by **varying the orbit**
> (smearing α, or varying the parities), so it controls a *positive-measure family* of orbits and is silent on
> any single Haar-null one. Every measure *localized* to the one orbit is either **δ₀** (no decay), the
> **Parry measure** (decays but bit-blind), or the **empirical measure** (bit-sensitive and localized, but its
> decay = Haar-ness = (K), the open object). **Bit-sensitivity + decay forces de-localization; localization
> forces δ₀ / bit-blindness / circularity. The two are mutually exclusive among the natural measures.**

**Hence:**
- **REMOVABLE at the family/annealed tier:** YES — the ROTATION axis attaches a genuine non-degenerate
  Rajchman measure ρ̂, upgrading the old "δ₀, no measure" verdict (which only examined the SUM axis) and
  yielding the a.e.-α partial. This is a real, citable advance in framing.
- **INTRINSIC at the single-orbit tier:** YES — by the dichotomy above. Any measure carrying *both* decay and
  bit-information necessarily smears the orbit (a.e.), and any measure localized to α=8 collapses to δ₀ (sum
  axis), to a bit-blind gap (Parry), or to the open empirical measure. **The δ₀-degeneracy on the sum axis is
  the shadow of a deeper intrinsic fact: the single orbit is genuinely measure-free *as a bit-sensitive
  decaying object*.**

---

## 6. Numerics `[OBSERVED]`  (`scratchpad/first_diag_measure.py`)

**T1 — Quenched (real α=8) empirical-measure Fourier `(1/N)Σ e(h{8(3/2)ⁿ})`, scaled by √N.** Rides the √N
floor (Mahler), drifting up only slowly — the open equidistribution:

| N | h=1 | h=2 | h=3 |
|---|---|---|---|
| 2 000 | 0.068 | 1.041 | 1.028 |
| 10 000 | 0.432 | 1.276 | 1.260 |
| 50 000 | 0.873 | 1.429 | 1.421 |

**T2 — SUM-axis δ₀ vs ROTATION-axis ρ̂ (decisive contrast), h=1, ρ=Unif[4,8], grid M=4000.** The δ₀ "measure"
never decays (vacuous, as predicted); the rotation measure decays to the grid floor:

| n | SUM-axis `|δ̂₀|` | ROTATION-axis `|E_{α}[e(·)]|` |
|---|---|---|
| 20 | 1.000 | 0.00002 |
| 60 | 1.000 | 0.00024 |
| 100 | 1.000 | 0.00035 |
| 140 | 1.000 | 0.00006 |

(The ≈10⁻⁴ floor is the **grid resolution**, not the true value: at fixed n=20, refining M=1.5k→96k drives
`|E|` 1.4e-4 → 2.1e-6 ∝ 1/M — the continuous `ρ̂(h(3/2)ⁿ)` is → 0, confirming §2.)

**T3 — SECOND-diagonal annealed `ν̂_{2/3}((3/2)^{n-1}/8)` (Rajchman, REAL non-Pisot decay).** Genuine
exponential decay that T2 reproduces *only by smearing*:

| n | 10 | 20 | 40 | 60 | 80 |
|---|---|---|---|---|---|
| `|ν̂_{2/3}(ξ_n)|` | 1.3e-3 | 2.9e-8 | 1.5e-15 | 5.4e-22 | 1.9e-26 |

**T4 — Bit balance (quenched α=8 vs rotation-annealed over α).** Both → ½; the quenched is the single orbit
(Mahler), the annealed is the a.e.-α partial:

| k | QUENCHED `P(d_n=1)` (N=2·10⁴) | ROTATION-annealed `P_α(bit=1)` (n=120) |
|---|---|---|
| 0 | 0.5014 | 0.5003 |
| 2 | 0.5026 | 0.4997 |
| 4 | 0.5057 | 0.5007 |

**Reading.** T2+T3: a non-degenerate decaying measure attaches to the 1st diagonal **only on the rotation
axis**, and its decay is the *trivial* Riemann–Lebesgue kind (grid-limited to 0), in pointed contrast to the
2nd diagonal's *arithmetic* (non-Pisot) Rajchman decay. T1+T4: the single orbit α=8 equidistributes only at the
√N/Mahler floor — exactly what the dichotomy of §5 predicts (the localized object is the open empirical measure).

---

## 7. Honest verdict (the three asks)

| ask | answer | label |
|---|---|---|
| **(a) does a non-degenerate measure attach (partial)?** | **YES, on the rotation/multiplier axis.** Any a.c. ρ on α gives `E_α[e(h α(3/2)ⁿ)] = ρ̂(h(3/2)ⁿ)→0` (Riemann–Lebesgue), the rotation-counterpart of ν_{2/3}; upgrades (Koksma) to **a.e.-α equidistribution / AEV-a.e. normality** of `bit_k⌊α(3/2)ⁿ⌋`. **But base-independent (uses a.c. of ρ, NOT non-Pisot of 3/2): the constant 8 is smeared, so it is an a.e.-α, not a single-orbit, partial.** | `[PROVEN]` (identity) + `[PROVEN-in-lit]` (Koksma/AEV-a.e.) |
| **(b) intrinsic-degeneracy characterization?** | **YES.** Trichotomy of natural measures (sum=δ₀ / rotation=ρ̂ / renormalization=Parry / scenery=empirical) ⇒ the **bit-sensitivity ⊥ single-orbit-localization dichotomy** (§5): no attachable measure is simultaneously bit-sensitive, decaying, and orbit-localized. Hence δ₀ is **removable at the family/annealed tier (into ρ̂) but intrinsic at the single-orbit tier**. The Parry measure is non-degenerate with a gap but **bit-blind** (real-place projection); the empirical measure is bit-sensitive+localized but its decay **= (K)**. | `[OBSERVED synthesis]` over `[PROVEN]`/`[PROVEN-in-lit]` parts |
| **(c) reduces?** | **YES — the quenched single orbit reduces to (K) = Mahler/AEV at α=8**, untouched by any attached measure. The rotation measure controls Lebesgue-a.e. α; α=8 is Haar-null; localizing to it is exactly the open object (the empirical measure being Haar). | `[PROVEN reduction]` to `(K)` |

**Exact residual (sharpened).** Show the **single Haar-null orbit α=8 is generic** for the (provably Rajchman)
rotation-annealed model — i.e. `{8(3/2)ⁿ}` equidistributes mod 1 — equivalently that the empirical measure
`(1/N)Σδ_{{8(3/2)ⁿ}} → Lebesgue`. This is (K) = Mahler 3/2 / AEV Conj 1.6 at α=8, the single-orbit wall. The
attached measure (ρ̂ on the family) gives the a.e. tier; pulling it down to the one orbit is precisely what no
measure can do (§5).

---

## 8. Genuinely new vs prior

- **vs `SECOND_DIAGONAL_RAJCHMAN §2` / `TWO_DIAGONAL_COMPARISON §3` (1st diagonal = δ₀, "no measure").** Those
  examined **only the SUM axis** and correctly found δ₀. This note adds the **ROTATION axis**: a genuine
  non-degenerate Rajchman measure ρ̂ (the multiplier law) **does** attach to the first-diagonal family, giving
  the a.e.-α partial — so the degeneracy is **removable at the family tier**, a strictly more favorable (and
  honest) framing than "no measure exists." The new content is the explicit `E_α[e(hα(3/2)ⁿ)]=ρ̂(h(3/2)ⁿ)`
  identity and the observation that its decay is **base-independent** (the smoking gun that it is a.e., not
  pointwise).
- **vs `THERMO_FORMALISM §2.1` (operator A flow=lattice/blind; operator B self-similar=annealed).** Those
  framed the dichotomy via two transfer operators. This note recasts it as a **measure trichotomy on the first
  diagonal specifically** and isolates the new **bit-sensitivity ⊥ localization** principle (§5): it explains
  *why* operator B (bit-sensitive) is annealed-only and operator A / Parry (localized) is bit-blind — they are
  the two horns of one dichotomy. The Parry measure's non-degeneracy-with-gap-but-bit-blindness is stated
  cleanly as a measure (not just an operator) fact.
- **vs `mahler §10` (empirical measure = (K)).** Consistent and placed: the scenery measure is exactly the
  ONE localized + bit-sensitive object, and its decay being (K) is the circular corner of the trichotomy — this
  note shows it is *forced* to be the corner by the dichotomy, i.e. there is no fourth, better measure.
- **Net new statement:** *the first diagonal is not measure-free after all — it carries the rotation/multiplier
  Rajchman measure ρ̂ and hence the a.e.-α (Koksma/AEV) partial — but it is **bit-sensitive-decaying-measure-free
  at the single orbit**, because attaching a decaying bit-sensitive measure provably requires de-localizing the
  fixed constant 8. The δ₀ degeneracy is the sum-axis shadow of this intrinsic single-orbit fact.* No label on
  (K) is upgraded.

## Sources
- Repo: `SECOND_DIAGONAL_RAJCHMAN.md` (ν_{2/3} sum-axis Rajchman, δ₀ vertex), `TWO_DIAGONAL_COMPARISON.md`
  (both diagonals = `bit_k⌊α(3/2)ⁿ⌋`, α=8 vs α*, ν_{2/3} degenerate for one orbit), `THERMO_FORMALISM.md`
  (operator A flow=constant roof=lattice/blind, operator B self-similar Fourier=annealed/a.e.; single-orbit
  wall §2.2), `NONPISOT_FOURIER_CHAIN.md` (Link A Erdős–Salem, Link B annealed=ν̂_{2/3}, Link C broken),
  `mahler_equidistribution_attack.md` (§9 two-place skew β-map⋉2-adic isometry, β-map has gap 0.27 but
  bit-blind; §10 empirical measure = (K)), `DIGITS_OF_3N.md` (AEV digit), `CARRY_EXOGENIZATION.md`.
- Literature (repo knowledge): Erdős (1939)/Salem (1944) Rajchman ⇔ 1/λ non-Pisot; Koksma (1935) a.e.-θ
  equidistribution of `{tθⁿ}`; Weyl (1916); Varjú–Yu (arXiv:2004.09358) / Kershner (1936) log rate for ν_{2/3};
  Parry/Gel'fond β-measure; Peres–Schlag–Solomyak "Sixty Years of Bernoulli Convolutions"; Li–Sahlsten
  (arXiv:1910.03463); Mahler 3/2 (1968, open); Andrieu–Eliahou–Vivion (arXiv:2510.11723, Conj 1.6 + a.e.-α
  normality).
- Numerics: `scratchpad/first_diag_measure.py` (exact big-int orbit 8·3ⁿ + mpmath dps≤200, N≤5·10⁴, ≈70s):
  T1 quenched empirical Fourier rides √N floor; T2 δ₀≡1.000 vs rotation-annealed → grid floor (∝1/M ⇒ →0);
  T3 ν̂_{2/3} non-Pisot exponential decay; T4 quenched & rotation-annealed bits both → ½; refinement check
  `|E_α|∝1/M` confirms the continuous rotation-annealed Weyl sum → 0.

**No machine decided. No label upgraded.**
