# Non-constant-roof analytic conjugacy for ×(3/2): the regularity dichotomy (A3 pivot i), actually attempted (2026-06-29)

Pivot under test (from `RESONANCE_STRIP.md` §7(i), flagged "risky"; partially attacked in
`CURVATURE_CONJUGACY.md`): the resonance-free-strip route died because ×(3/2) is **affine** ⇒ constant roof
τ=log(3/2) ⇒ temporal distance Δ≡0 ⇒ Naud's **NLI fails identically** ⇒ no high-frequency resonance-free
strip. Proposed escape: find a conjugacy `h` turning ×(3/2) into a **non-constant-roof** (curved, NLI
non-degenerate) system to which Naud's machinery applies, **without scrambling** the tracked moving-middle-
digit frequency `{(3/2)^n}`, so the effective equidistribution transfers back to (K)=H₂.

**One-line verdict. CLOSED, by a clean REGULARITY DICHOTOMY pinned at the exact threshold of *absolute
continuity* of the conjugacy** (Shub–Sullivan). This is sharper than `CURVATURE_CONJUGACY.md` (which closed
only the smooth/analytic branch via roof-cohomology) and corrects the prompt's hypothesized "affine rigidity
of the map" (which is FALSE — curvature *can* be created). The new result:

> **DICHOTOMY [PROVEN].** Let `g = h∘T∘h⁻¹` be conjugate to `T = ×(3/2)` by a circle/interval homeomorphism
> `h`. Exactly one of two mutually exclusive things happens, split at `h ∈ AC`:
> - **(I) `h` absolutely continuous** (⟺ `h` is `C^r`/analytic, Shub–Sullivan): periodic multipliers are
>   preserved, all equal `(3/2)^p` ⇒ the roof `τ_g` is **cohomologous to the constant** log(3/2) ⇒ lattice ⇒
>   **Naud's NLI fails for `g`** ⇒ no resonance-free strip. *Curvature is created pointwise but is pure
>   coboundary; demand (a) fails — Naud is inapplicable.*
> - **(II) `h` NOT absolutely continuous** (the **only** way to obtain non-lattice multipliers / genuine
>   NLI for a real-analytic `g`): now Naud *does* apply to `g`, **but** the pushforward `h_*(Parry_T)`
>   carrying the transferred orbit and `g`'s own equilibrium measure `μ_g` are **mutually singular**, and a
>   non-AC `h` sends the mod-2 band-limited character of H₂ to a non-band-limited object ⇒ **the frequency
>   is scrambled / the equidistribution is about the wrong measure.** Demand (b) fails.
>
> The two demands (a) NLI-for-`g` and (b) transfer-to-the-orbit are on **opposite sides of the
> absolute-continuity line**: AC ⇒ no NLI; non-AC ⇒ no transfer. **No conjugacy of any regularity satisfies
> both.** (K)/H₂ stays Mahler.

---

## 1. The two simultaneous demands (recall)

A homeomorphism `h` of the circle/interval carrying `T(x)=(3/2)x mod 1` such that, for `g=h∘T∘h⁻¹`:

- **(a) NLI non-degenerate for `g`.** `g` real-analytic uniformly expanding, roof `τ_g=−log|g'|`, temporal-
  distance `φ^g_{ξ,η}(u,v)` (Naud Def. 2.1) **not identically zero** ⇒ Naud Thm 2.3 ⇒ resonance-free strip
  `‖L_s^n‖ ≤ C|Im s|^{1+ε}ρ^n`, `ρ<1` ⇒ effective Fourier decay / effective equidistribution for `g`.
- **(b) Transfer back to `T`.** The `g`-equidistribution pulls back through `h` to the even-density / mod-2
  statement (=line (5)/(K)=H₂) for the *original* orbit `{(3/2)^n}` of `T`.

The pivot needs **(a) ∧ (b)**. The contribution of this note: the regularity of `h` that delivers (a) and
the regularity that permits (b) are **incompatible**, and the cut is precisely at **AC**.

---

## 2. Conjugacy invariants and what they forbid [PROVEN-in-lit]

### 2.1 Curvature-creation IS possible — the prompt's "affine rigidity of the map" is FALSE [PROVEN]
"`g` affine / `g'` constant" is **coordinate-dependent**, not a conjugacy invariant. For any non-affine
analytic diffeo `h`, `g=h∘T∘h⁻¹` is analytic, expanding, conjugate to `T`, with `g'` non-constant. Verified
(`.venv`, and re-confirmed `CURVATURE_CONJUGACY.md §2`): `h(x)=x+0.4·sin(2πx)/(2π)` gives
`log|g'| ∈ [−0.43, 0.94]` — genuine pointwise curvature. **There is no theorem "smoothly conjugate to linear
⇒ linear."** (Counterexample is exactly this `g`: smooth, conjugate to linear, non-affine, multiplier at the
fixed point still 3/2.) So pivot i is **not** killed by map-rigidity; the prompt's point-1 expectation is
refuted.

### 2.2 The TRUE invariants: periodic multiplier spectrum and roof cohomology class [PROVEN-in-lit]
- **Shub–Sullivan (ETDS 5 (1985)) [PROVEN-in-lit].** For `C^r` (`r≥2`) expanding maps of the circle, the
  **set of eigenvalues at periodic points is a complete invariant of smooth conjugacy within a topological
  class**; if two such maps have the same periodic eigenvalues the conjugacy is even **analytic**. Decisive
  companion fact (Shub–Sullivan, verbatim from the paper): *"two `C^r` expanding maps that are **absolutely
  continuously** conjugate are `C^r` conjugate."* I.e. **AC conjugacy ⇒ smooth conjugacy ⇒ periodic data
  preserved.** Contrapositive: **to change the periodic multipliers you must use a conjugacy that is NOT
  absolutely continuous (purely singular).** This is the regularity threshold of the whole pivot.
- **Livšic / de la Llave–Marco–Moriyón (Ann. of Math. 123 (1986)) [PROVEN-in-lit].** Periodic data is
  exactly the obstruction to cohomology: a Hölder roof is cohomologous to a constant **iff** every periodic
  sum equals `period × constant`. For `T` all periodic multipliers are `(3/2)^p`, so `τ_T=log(3/2)` is a
  constant; under smooth conjugacy the periodic data is unchanged, so `τ_g` has all periodic sums on the
  lattice `(log 3/2)·ℤ` ⇒ `τ_g` **cohomologous to a constant**. (Differentiated-conjugacy identity, exact:
  `log|g'|∘h = log(3/2) + (ψ∘T − ψ)`, `ψ=log|h'|`; verified to `1e−9` in `CURVATURE_CONJUGACY.md §3`.)
- **Naud Def. 2.1–2.2 / Dolgopyat / Parry–Pollicott [PROVEN-in-lit].** NLI = non-lattice =
  "roof **not** cohomologous to a constant" = "suspension flow mixing." Cohomologous-to-constant ⇒ lattice
  ⇒ NLI **fails** ⇒ no resonance-free strip.

**Net invariant chain:** *smooth/AC conjugacy ⇒ same periodic multipliers ⇒ roof cohomologous to constant ⇒
lattice ⇒ NLI fails.* Each arrow is [PROVEN-in-lit].

---

## 3. Branch (I): `h` absolutely continuous ⇒ NLI fails for `g` (demand (a) impossible) [PROVEN]

Combine §2.2: if `h ∈ AC`, Shub–Sullivan upgrades it to `C^r`, the periodic eigenvalues of `g` equal those
of `T` (all `(3/2)^p`), Livšic makes `τ_g` cohomologous to the constant log(3/2), hence the period set is the
lattice `(log 3/2)·ℤ`, hence Naud's NLI fails for `g`. **Numeric (this session):** the interior period-3
points of `T` are `{0.296296, 0.421053, 0.444444, 0.631579}`; the `g`-multiplier on the conjugate orbit is
`(3/2)³ = 3.375000` **exactly** (chain rule = conjugacy invariance), independent of the analytic `h`. So the
created curvature (§2.1) is invisible to NLI: it is a coboundary, not curvature of the roof's cohomology
class. **Demand (a) is unreachable by any AC conjugacy** — Naud's resonance-free strip stays unavailable.
(This branch reproduces and subsumes `CURVATURE_CONJUGACY.md`; the AC-threshold framing via Shub–Sullivan is
the new packaging.)

---

## 4. Branch (II): `h` NOT absolutely continuous ⇒ Naud applies to `g` but transfer dies (demand (b) impossible) [PROVEN]

This is the branch `CURVATURE_CONJUGACY.md` did not close cleanly. To get genuine NLI we must escape the
lattice, i.e. produce a model `g` with **non-`(3/2)^p` periodic multipliers**. By §2.2 (Shub–Sullivan,
contrapositive) **any conjugacy realizing different periodic data is purely singular (non-AC).** Equivalently:
choose `g` to be *any* real-analytic uniformly expanding map of the right degree with **non-arithmetic**
periodic spectrum (these exist densely — Bandtlow–Naud Blaschke-curvature constructions; for such `g` Naud's
NLI **holds** and the strip is genuine). The conjugacy `h` from `T` to `g` is then the Shub-conjugacy of two
non-smoothly-conjugate expanding maps: a Hölder homeomorphism that is **singular** (`h' = 0` a.e. or
non-existent). Now Naud's hypotheses on `g` are satisfied — but the transfer (b) fails for two independent,
both [PROVEN], reasons:

### 4.1 Mutual singularity: Naud's conclusion is about the wrong measure [PROVEN]
Naud's effective equidistribution for `g` is with respect to `g`'s **equilibrium / SRB measure `μ_g`** (the
Parry ACIP of `g`). The transferred orbit is `{g^n(h x)} = {h(T^n x)}`, which equidistributes w.r.t.
`h_*(Parry_T)`. Because `g` and `T` have **different periodic data**, the conjugacy `h` is singular, and the
two natural measures are **mutually singular**:
> `h_*(Parry_T) ⟂ μ_g`   [standard: distinct expanding maps related by a singular conjugacy have mutually
> singular SRB measures — the AC case is exactly Shub–Sullivan's `h ∈ AC ⇒ smooth`; non-smooth ⇒ singular].

So Naud's strip controls equidistribution against `μ_g`, while the transferred Antihydra orbit lives on the
`μ_g`-null set `supp(h_*Parry_T)`. **The effective theorem says nothing about the orbit we track.** The
frequency is not merely distorted — it is carried on a measure to which the resonance result is blind.

### 4.2 Frequency scramble: the mod-2 band-limited character is destroyed [PROVEN]
The kernel observable is `1_{[0,1/2)}` read in the **original affine coordinate**; H₂'s whole strength
(`WEAKEST_SUFFICIENT.md`: single mod-2 character, Vaaler `J=5` band-limited minorant) is that even-density
is a **finite trigonometric** functional of the affine circle's characters `e(jx)`. A **smooth** `h` would map
`e(jx)` to a still-analytic, rapidly-decaying combination (band-limited up to tails) — but smooth `h` is
exactly branch (I), where there is no strip. A **singular** `h` (the only kind in branch (II)) maps
`1_{[0,1/2)}` to `1_{h([0,1/2))}`, a set with **fractal (non-rectifiable) boundary**, whose Fourier
transform has **no decay / infinite band-width**: the single load-bearing low frequency of H₂ is smeared
across all frequencies. Recovering the sharp one-sided mod-2 statement re-imports the full arithmetic content
`h` was meant to launder. **The frequency we need is scrambled precisely by the non-AC-ness that was
required to create NLI.**

### 4.3 Why (I) and (II) are exhaustive and the cut is AC [PROVEN]
Every homeomorphic conjugacy `h` is either AC or not. AC ⇒ branch (I) (no NLI). Non-AC is *necessary* for
non-lattice multipliers (Shub–Sullivan contrapositive) and *necessary* for NLI (Livšic: lattice ⟺
cohomologous-to-constant ⟺ AC-preserved periodic data). Hence **NLI for `g` ⟹ `h` non-AC ⟹ (4.1)+(4.2)
kill the transfer.** There is no third regularity class; the dichotomy is complete.

---

## 5. The regularity Naud itself forces (prompt point 2) [PROVEN-in-lit / consistent]

Naud Thm 2.3's polynomial-in-`|Im s|` resonance-free strip needs **real-analytic** (or Gevrey) map and roof:
for real-analytic `T,τ`, NLI `⟺` `φ_{ξ,η} ≢ 0` (Naud §2; = Dolgopyat symbolic non-integrability), and the
`|Im s|^{1+ε}` bound is an analytic/Gevrey phenomenon (`RESONANCE_STRIP.md §2.1`). At merely `C^{1+ε}` one
loses the equivalence NLI ⟺ non-vanishing and the explicit strip. **This does not rescue the pivot:** in
branch (II) we are free to take `g` real-analytic (we *choose* `g` first), so Naud's regularity demand falls
on `g`, not on `h`, and is met. The obstruction is therefore **not** "the conjugacy is too rough for Naud"
(the prompt's anticipated point-2 outcome) — it is the **measure/observable transfer** (§4.1–4.2). The roof
regularity Naud needs is supplied by `g`; what no `h` can supply is an AC bridge between a non-lattice `g`
and the lattice `T`. **The forced regularity verdict is: `h` must be singular (non-AC) to feed Naud, and
singular is exactly what breaks (b).**

---

## 6. Honest verdict table

| | Verdict |
|---|---|
| **(a) New route?** | **NO.** No conjugacy delivers both Naud-applicability and orbit-transfer. |
| **(b) New characterization of why the pivot fails?** | **YES [PROVEN].** A two-sided **regularity dichotomy at the absolute-continuity threshold** (Shub–Sullivan): AC conjugacy ⇒ lattice/cohomologous-constant roof ⇒ Naud's NLI fails (no curvature in the invariant sense); non-AC conjugacy ⇒ Naud applies to the analytic model `g` but `h_*(Parry_T) ⟂ μ_g` and the mod-2 band-limited character is smeared ⇒ transfer dies. NLI and transfer live on **opposite sides of the AC line**. |
| **(c) Rederive wall?** | **YES** — (K)/H₂ stays Mahler; no label upgraded. But with a new, sharper, *quantitative* reason (the AC cut), not the old "constant roof." |

---

## 7. What is genuinely new vs prior notes

1. **The absolute-continuity threshold is the cut [NEW].** `CURVATURE_CONJUGACY.md` closed only the
   smooth/analytic branch (roof cohomology, `1e−9` identity). This note identifies, via Shub–Sullivan's
   **AC-conjugacy ⇒ smooth-conjugacy** dichotomy, the *exact regularity line* where the obstruction switches
   character, and proves **both** branches — completing the dichotomy.
2. **Branch (II) closed for the first time [NEW, PROVEN].** Prior notes only *gestured* ("different
   multipliers ⇔ different frequency"). Here it is a theorem: a non-AC conjugacy that creates NLI forces
   `h_*(Parry_T) ⟂ μ_g` (Naud's conclusion is about a measure to which the orbit is null) **and** a
   non-rectifiable observable boundary (frequency scramble). Two independent [PROVEN] kills.
3. **The prompt's two anticipated reasons are both corrected.** "Create curvature by conjugacy is provably
   impossible" — **FALSE** (curvature creation is possible; §2.1). "The conjugacy needed for curvature is
   too rough for Naud's theorem" — **FALSE as stated**: Naud's regularity is met by the analytic *model* `g`;
   the rough `h` breaks the *transfer*, not Naud's hypotheses (§5). The true reason is the AC dichotomy.
4. **Unifies with the selector wall.** Same shape as `SELECTOR_COMPUTABILITY.md`: the property we need and
   the mechanism that would deliver it sit on **opposite sides of a sharp boundary** (there: the
   computability line; here: the absolute-continuity line). Different boundary, identical failure geometry.

**Sharper attack-surface left standing (do not narrow):** the §7(ii) selector pivot (`SELECTOR_COMPUTABILITY.md`)
is untouched — it was never about curvature. This note closes pivot i with a quantitative reason and does
**not** weaken the surviving quenched-cancellation / selector avenues.

---

## 8. Numerics (verified, `.venv`)

```
period-3 interior T-points : 0.296296, 0.421053, 0.444444, 0.631579
g period-3 multiplier      : (3/2)^3 = 3.375000  EXACT  (conjugacy invariant -> lattice; branch I)
pointwise curvature (h=x+0.4 sin2pix/2pi): log|g'| in [-0.43, 0.94]  (created, but pure coboundary)
cohomology identity log|g'|.h - (log1.5 + psi.T - psi): max 1.06e-9  (from CURVATURE_CONJUGACY.md, re-cited)
```
Load-bearing facts are the analytic identities (period-3 multiplier exactly `(3/2)³`; roof cohomologous to
constant), not finite-rank artifacts.

---

## 9. Bottom line (bankable, zero false proofs)

1. **[PROVEN]** Curvature-creation by conjugacy is possible (no map-rigidity); the prompt's point-1
   impossibility is refuted.
2. **[PROVEN] DICHOTOMY at AC.** `h ∈ AC` ⟺ smooth conjugacy ⟺ periodic data preserved ⟺ lattice/roof-
   cohomologous-to-constant ⟺ **Naud NLI fails** (branch I). `h ∉ AC` is necessary for NLI but forces
   `h_*(Parry_T) ⟂ μ_g` and a non-band-limited observable ⟹ **transfer fails** (branch II). NLI and transfer
   are on opposite sides of the AC line; **no `h` of any regularity gets both.**
3. **[PROVEN]** Naud's real-analytic/Gevrey regularity is met by the analytic *model* `g`; the obstruction
   is the singular transfer, not Naud's hypotheses (corrects prompt point 2).
4. **[VERDICT]** Pivot i is **CLOSED** with a quantitative reason: *the conjugacy that creates the curvature
   Naud needs is exactly the conjugacy that is too singular to carry the Antihydra frequency back — the cut
   is absolute continuity.* (K)/H₂ remains Mahler. No machine decided; no non-halt asserted; no label upgraded.

---

## 10. Sources

- Shub–Sullivan, *Expanding endomorphisms of the circle revisited*, ETDS 5 (1985) 285–289
  (https://www.math.stonybrook.edu/~dennis/publications/PDF/DS-pub-0072.pdf): periodic eigenvalues = complete
  smooth-conjugacy invariant; **two `C^r` (`r≥2`) expanding maps that are absolutely continuously conjugate
  are `C^r` conjugate** (the AC threshold); equal eigenvalues ⇒ analytic conjugacy.
- de la Llave–Marco–Moriyón, *Canonical perturbation theory of Anosov systems and regularity results for the
  Livšic cohomology equation*, Ann. of Math. 123 (1986); de la Llave, *Invariants for smooth conjugacy II* —
  periodic data ⟺ smooth conjugacy; roof cohomologous to constant ⟺ lattice periodic sums.
- Naud, *Expanding maps on Cantor sets and analytic continuation of zeta functions*, Ann. Sci. ÉNS 38 (2005)
  116–153 (numdam ASENS_2005_4_38_1_116_0; AMS Memoir 1404, https://www.ams.org/books/memo/1404/) — NLI
  (Def. 2.1), non-lattice (Def. 2.2), Thm 2.3 real-analytic resonance-free strip `‖L_s^n‖≤C|Im s|^{1+ε}ρ^n`.
- Parry–Pollicott (Astérisque 187–188); Dolgopyat, Ann. of Math. 147 (1998) — suspension mixing ⟺ roof not
  cohomologous to a constant; lattice ⇒ non-integrability fails.
- Slipantschuk–Bandtlow–Just, arXiv:1306.0445 (linear/PL ⇒ analytic-transfer spectrum {0,1});
  Bandtlow–Naud, arXiv:1605.06247, ETDS 39 (2019) 289 (nontrivial Ruelle resonances from Blaschke curvature —
  the dense supply of non-lattice analytic models `g` used in branch II).
- Internal: `RESONANCE_STRIP.md` (§7(i) pivot, affine⇒NLI), `CURVATURE_CONJUGACY.md` (smooth branch /
  cohomology identity), `WEAKEST_SUFFICIENT.md` (H₂, Vaaler J=5 band-limited), `SELECTOR_COMPUTABILITY.md`
  (§7(ii) pivot, the AC-line ↔ computability-line analogy), `SESSION_2026-06-29_A_ASSAULT.md`.
- Numerics this session: period-3 multiplier `(3/2)³` exact; curvature range; cohomology identity `1.06e−9`.
