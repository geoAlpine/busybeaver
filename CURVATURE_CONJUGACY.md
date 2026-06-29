# Frequency-preserving curvature-creating conjugacy for ×(3/2) (A3 pivot i), actually attempted (2026-06-29)

Pivot under test (from `RESONANCE_STRIP.md` §7(i)): the resonance-free-strip route died because ×(3/2)
is **affine** ⇒ constant roof τ=log(3/2) ⇒ temporal distance Δ≡0 ⇒ Naud's **NLI fails identically** ⇒ no
high-frequency resonance-free strip. The proposed escape: find an **analytic conjugacy** `h` making
`g = h∘T∘h^{-1}` **non-affine** (curved, NLI non-degenerate, Naud applies) **without scrambling** the
tracked frequency `{(3/2)^n}`, so the effective equidistribution for `g` transfers back to (K).

**One-line verdict.** **CLOSED — but by a sharper mechanism than the prompt's menu.** Curvature-creation
is *trivially possible* (affine maps are **not** rigidly affine: any non-affine analytic `h` makes `g'`
non-constant — verified, log|g'|∈[−0.43, 0.94]). So the pivot is **not** killed by "affine rigidity of the
map." It is killed by **cohomological rigidity of the ROOF**: Naud's NLI / the lattice property is a
**conjugacy invariant**, and conjugacy moves the pointwise curvature of `g` into a **coboundary that NLI
cannot see**. The roof of `g` stays **cohomologous to the constant** log(3/2) ⇒ still lattice ⇒ NLI still
fails ⇒ Naud still inapplicable. Pointwise curvature ≠ the curvature Naud needs (curvature of the roof's
**cohomology class**, which is rigid). The curved-observable variant fails for the dual reason (a strip is a
property of the operator, not the test function). **Mahler-in-disguise survives the conjugacy.**

---

## 1. What is precisely needed (the two simultaneous demands)

A real-analytic diffeomorphism `h` (of the circle/interval carrying T) such that:

- **(a) NLI non-degenerate for `g = h∘T∘h^{-1}`.** `g` real-analytic, and its temporal-distance function
  `φ^g_{ξ,η}(u,v)` (Naud Def. 2.1, built from the roof `τ_g = −log|g'|` along inverse branches) is **not
  identically zero** ⇒ Naud Thm 2.3 ⇒ resonance-free strip `‖L_s^n‖ ≤ C|Im s|^{1+ε}ρ^n` ⇒ effective
  Fourier decay / effective equidistribution for `g`.
- **(b) Transfer back to T.** The `g`-equidistribution pulls back through `h` to the even-density / mod-2
  statement for the original orbit `{(3/2)^n}` of T (= line (5)/(K) = H₂).

The pivot needs **(a) ∧ (b)**. We show they are not simultaneously achievable, and pin exactly why.

---

## 2. Can an analytic conjugacy make ×(3/2) non-affine at all? — YES (no affine rigidity)

**[PROVEN] Curvature-creation is possible; affine maps are NOT rigidly affine under analytic conjugacy.**
"`g` is affine / `g'` constant" is a **coordinate-dependent** (non-invariant) property. Take any non-affine
analytic diffeo `h`; then `g = h∘T∘h^{-1}` is analytic, expanding, conjugate to T, and `g'` is generically
non-constant.

**Numeric (`.venv`, this session).** `h(x)=x+a·sin(2πx)/(2π)`, `a=0.4` (analytic circle diffeo, `h'>0`,
`h(x+1)=h(x)+1`), `g=h∘T∘h^{-1}` with `T(x)=(3/2)x mod 1`:
```
g'(y) samples : [1.498 1.396 1.171 1.097 2.500 2.548 1.496 0.876 0.648]
log|g'| range : −0.4347 .. 0.9352        => NON-CONSTANT: pointwise curvature CREATED
T' constant   : log(3/2) = 0.4055
```
So `g` is genuinely non-affine. The naive hope ("non-affine ⇒ NLI holds") is geometrically licit at the
**pointwise** level. The kill is at the **invariant** level (§3).

---

## 3. The decisive obstruction: NLI is a COHOMOLOGY invariant; the roof stays cohomologous to a constant

**The differentiated conjugacy gives the roof's cohomology class for free.** Differentiate
`g(h(x)) = h(T(x))`: `g'(h(x))·h'(x) = h'(T(x))·T'(x)`, hence with `ψ := log|h'|`,
> **log|g'| ∘ h = log|T'| + ψ∘T − ψ = log(3/2) + (ψ∘T − ψ).**  [exact identity]

So **`τ_g = −log|g'|` is cohomologous to the constant `−log(3/2)`** (coboundary `−(ψ∘T−ψ)`, transported by
`h`). The curvature created in §2 is **entirely a coboundary**.

**Numeric confirmation.** `max | log|g'|∘h − ( log(3/2) + ψ∘T − ψ ) | = 1.06e−9` over interior samples
(machine-exact; the residual is finite-difference error in `g'`).

**Why this kills NLI.** Naud's non-lattice / NLI condition is exactly "roof **not** cohomologous to a
constant" (the suspension flow is mixing ⟺ roof not cohomologous to a constant; cohomologous-to-constant ⇒
**lattice** ⇒ Dolgopyat/Naud non-integrability **fails** ⇒ no resonance-free strip). Concretely:

- **Periodic periods stay on a lattice.** On any combinatorial period-`p` orbit the coboundary telescopes
  to 0, so `τ_g`-period `= p·log(3/2) ∈ (log 3/2)·ℤ`. The period set is a **lattice** regardless of `h`.
  *Numeric:* clean interior period-3 orbit `x₀=0.421053` gives `g`-multiplier `= 3.375000 = (3/2)³`
  **exactly** (the spurious huge values in the run are at the β-map discontinuity `x=2/3` and `x=0`, not
  genuine smooth orbits). This is Shub–Sullivan / de la Llave–Marco–Moriyón **periodic-data rigidity**:
  for 1-D expanding maps the periodic multipliers are a **complete smooth-conjugacy invariant**, and for the
  affine T they are all `(3/2)^p` — any smooth conjugate inherits exactly these, i.e. the lattice.
- **Temporal distance still vanishes in the NLI sense.** `Δ^g_ξ(u,v)` built from `τ_g = const +
  coboundary` reduces (telescoping along inverse branches) to a difference of the coboundary potential `ψ`
  at the two limit endpoints; the cross-difference `φ^g_{ξ,η} = Δ^g_ξ − Δ^g_η` that NLI tests is a **pure
  coboundary artifact** carrying no `(ξ,η)`-dependent curvature. NLI = "`φ_{ξ,η} ≢ 0`" **still fails.**

**[PROVEN] Conclusion.** Conjugacy creates pointwise curvature in `g'` but **cannot** change the cohomology
class of the roof; Naud's NLI depends **only** on that class; so **NLI still fails for `g`**, and Naud's
resonance-free strip is **still unavailable**. Curvature-creation and NLI-creation are **different things**:
the first is possible, the second is conjugacy-rigid. **Demand (a) is unreachable by any analytic conjugacy.**

---

## 4. Does `h` preserve the tracked frequency? (the secondary tension — not even reached)

Even granting (a), demand (b) has its own tension, worth recording:

- **Equidistribution transfers cleanly** (good news): `{T^n x}` equidistributes w.r.t. `μ` ⟺
  `{g^n(h(x))} = {h(T^n x)}` equidistributes w.r.t. `h_*μ`. So an a.e./effective equidistribution statement
  for `g` does pull back.
- **But the observable is distorted** (the real cost): the even-density observable is the indicator
  `1_{[0,1/2)}` read in the **original affine coordinate**. In the `g`-coordinate it becomes
  `1_{h([0,1/2))}` — a **curved set**, still well-defined but no longer the clean dyadic/mod-2 character.
  And the tracked points become `{h((3/2)^n)}`, a different sequence. The mod-2 / Vaaler J=5 band-limited
  structure of H₂ (`WEAKEST_SUFFICIENT.md`) lives on the **affine** circle's characters; `h` smears it
  across all frequencies. So even a working strip for `g` would deliver equidistribution against
  **`h`-distorted** test functions, and recovering the *sharp* mod-2 one-sided statement re-introduces the
  arithmetic content `h` was supposed to launder away.

This is the prompt's "(c)" failure mode, but it is **subordinate** to §3: we never get a usable strip in
the first place, because NLI is cohomology-rigid. (b)'s tension is real but moot.

---

## 5. Curved-observable / nonlinear-weight alternative — also fails

Put the curvature in the **test function / weight** instead of the map:

- **A resonance-free strip is a property of the operator `L_s`, not of the test function you pair it
  against.** `L_s` is fixed by the map and the roof. A curved observable changes the **numerator**
  (projection onto resonances / the correlation you read off) but **cannot manufacture a spectral gap /
  strip** where the operator has none. NLI failure is intrinsic to `L_s`; no weight repairs it.
- **The relevant oscillatory twist is the Fourier one** `L_ξ f = (2/3)Σ_b e(ξ φ_b(x)) f∘φ_b`. Its
  high-`ξ` Dolgopyat-type decay needs **non-affineness of the phase** `x∘(inverse branches)`. For affine T
  the phase is affine ⇒ `L_ξ` = the Bernoulli-convolution operator ⇒ decay = Rajchman = **annealed = Link
  B** (already owned). To curve the phase is to **replace the tracked linear coordinate `x`** by a curved
  function = **scramble the very frequency** (same §4 tension). So curvature-in-observable either (i) does
  not touch the (affine) operator's lack of a strip, or (ii) changes the frequency. No free lunch.

---

## 6. Honest verdict (bankable, zero false proofs)

The prompt's menu was (a) real lead / (b) impossible by affine rigidity / (c) possible but scrambles
frequency. The true answer is a **refinement of (b)** that is **stronger and cleaner**:

- **NOT (a).** No real lead. The conjugacy cannot deliver Naud's NLI.
- **NOT (b) as stated.** It is **false** that affine maps are rigidly affine under analytic conjugacy —
  curvature-creation IS possible (§2, verified). So "affine rigidity of the map" is the **wrong** reason.
- **The correct closure = COHOMOLOGICAL rigidity of the ROOF** [PROVEN]: `log|g'|∘h = log(3/2) + (ψ∘T−ψ)`
  exactly (verified 1e−9); NLI / non-lattice depends **only** on the roof's cohomology class; that class is
  conjugacy-invariant and stays "cohomologous to a constant" = lattice. Hence **demand (a) is impossible
  for every analytic `h`** — independently of (b)/frequency issues.
- **(c) is also true but subordinate**: a curvature-creating `h` distorts the mod-2 observable and the
  tracked sequence (§4); but this never matters because (a) already fails.

**Net:** the frequency-preserving curvature-creating conjugacy is **CLOSED**. The pointwise curvature one
can create is **pure coboundary**; Naud needs curvature of the roof's **cohomology class**, which is
**rigid under conjugacy**. The curved-observable variant fails dually (strip = operator property, not
observable property). **(K)/H₂ remains Mahler.** Banked negative: *"analytic conjugacy creates pointwise
curvature but not cohomological curvature; NLI is a conjugacy invariant; affine ⇒ lattice is
conjugacy-stable."* — the sharp reason the §7(i) pivot of `RESONANCE_STRIP.md` does not bypass Mahler.

**Sharper attack-surface left standing (do not narrow):**
- The §7(ii) pivot survives untouched: **a.e.→specific selector** attacked *independently* of any strip
  (effective/computable-point equidistribution for the computable orbit `c₀=8`). This pivot was never about
  curvature, so the present closure does not touch it.
- Restated cleanly: the obstruction is now **cohomology of the roof**, not soficity, not pressure, not
  pointwise affineness. The only way to make NLI hold is a roof **not** cohomologous to a constant — which
  requires a genuinely **non-conjugate** (different periodic multiplier spectrum) expanding model, i.e. a
  model whose orbit is no longer `{(3/2)^n}`. That is the precise statement of why "curvature" and
  "frequency" are mutually exclusive **here**: same multipliers (frequency) ⇔ same cohomology class ⇔ no
  NLI; different cohomology class ⇔ different multipliers ⇔ different frequency.

## 7. References
- Shub–Sullivan, *Expanding endomorphisms of the circle revisited*, ETDS 5 (1985) — periodic multipliers
  are a complete smooth-conjugacy invariant for 1-D expanding maps.
- de la Llave, Marco, Moriyón, *Canonical perturbation theory of Anosov systems and regularity results for
  the Livšic cohomology equation*, Ann. of Math. 123 (1986); de la Llave, *Invariants for smooth conjugacy
  of hyperbolic dynamical systems II* — eigenvalues at periodic orbits = complete moduli. Recent:
  Gogolev–Rodriguez Hertz (higher-dim expanding maps); *Unmarked spectral rigidity of expanding circle
  maps*, arXiv:2511.17452.
- Naud, *Expanding maps on Cantor sets and analytic continuation of zeta functions*, Ann. Sci. ÉNS 38
  (2005) — NLI (Def. 2.1), Thm 2.3 strip (the NLI = non-lattice = roof-not-cohomologous-to-constant).
- Parry–Pollicott (Astérisque 187–188); Dolgopyat, Ann. of Math. 147 (1998) — suspension mixing ⟺ roof not
  cohomologous to a constant; lattice ⇒ non-integrability fails. (Avila–)Forni / time-changes literature:
  roof cohomologous to constant ⇒ non-mixing (e.g. arXiv:1706.09385).
- *Nonlinearity, Fractals, Fourier decay — Harmonic analysis of equilibrium states for hyperbolic
  dynamical systems*, arXiv:2410.15476 — Fourier decay needs non-cohomological (nonlinear) roof/phase.
- Internal: `RESONANCE_STRIP.md` (§7(i) the pivot tested here), `WEAKEST_SUFFICIENT.md` (H₂ / Vaaler J=5),
  `THERMO_FORMALISM.md`, `NONPISOT_FOURIER_CHAIN.md`, `SESSION_2026-06-29_A_ASSAULT.md`; numerics this
  session (curvature-creation + cohomology identity 1e−9 + period-3 multiplier 3.375 exact).
