# Cross-disciplinary scout — ARITHMETIC DYNAMICS (Skolem–Mahler–Lech / dynamical Mordell–Lang / p-adic interpolation / height-equidistribution) vs the Antihydra kernel (2026-06-30)

*Scouting a genuinely new attack angle from arithmetic dynamics. SOUNDNESS: every angle labelled
[APPLICABLE-NEW] / [NEAR-MISS] / [ALREADY-CLOSED] / [NOT-APPLICABLE]. This note does NOT claim to solve (K).
Honest verdicts only. NOT committed.*

Kernel **(K)** (recap, `WEAPONS_AUDIT_2026-06-29.md`, `SESSION_2026-06-29_AEV_CORE.md`): single-orbit equidistribution
of `c_n mod 2^k` for `c₀=8`, `c_{n+1}=⌊3c_n/2⌋` (= base-3/2 normality = Mahler 3/2 = AEV Conj 1.6 at α=8).
Halting ⟺ the orbit's **return set** to a target (a 2-adic ball `{c_n≡1 mod 2^k}` / `{balance_n<0}`) has the wrong
**frequency**. The closed routes (verified read here): measure rigidity Furstenberg/Rudolph/Lindenstrauss
(`ADELIC_COUPLING.md`), adelic product-formula coupling + dual-repulsion height (`ADELIC_COUPLING.md`,
`REPELLER_ESCAPE.md`), transfer-operator/specification/ergodic-optimization, Rajchman/Hochman/Baker-Diophantine,
computability. **None of the four arithmetic-dynamics tools below appears in that list** — so the *novelty* test is met;
the question is *applicability*.

---

## 0. One-line verdict

Arithmetic dynamics is a genuinely **new toolbox** here (not in the closed list), but it is structurally aimed at the
wrong invariant: **Skolem–Mahler–Lech / dynamical Mordell–Lang control the *structure* of a return set (finite union of
arithmetic progressions, plus a Banach-density-ZERO remainder), never its *frequency/density*** — and indeed the sharp
"weak DML" result is a density-**zero** statement, the opposite régime from the positive-density `1/2^k` the kernel needs.
**p-adic interpolation of the orbit is impossible** (the floor map is non-analytic and 2-adically *expanding/repelling*,
the régime where interpolation provably fails), though there is a genuine p-adic-analytic **skeleton** `8·3ⁿ` and the
non-interpolable part is *exactly* the carry `S_n` = the known obstruction. **Baker–Rumely / Yuan–Zhang adelic
equidistribution does not apply** (needs a degree-≥2 *algebraic* map and Galois conjugates of *small-height* points;
Antihydra is a degree-1 non-algebraic floor map on one rational point of *growing* height with trivial Galois orbit).
Net: every arithmetic-dynamics route reduces to, or is blind to, the **same single-orbit frequency wall**. The one thread
genuinely outside the closed list and worth a probe is **Siegel's (p,q)-adic Fourier / non-archimedean spectral theory +
Wiener Tauberian theorem for Collatz-type maps** — [NEAR-MISS, new formalism].

---

## 1. Can the orbit be p-adically interpolated? — [NEAR-MISS for the skeleton; NOT-APPLICABLE for the orbit]

**The interpolation theorem and its hypothesis.** Bell (after Skolem–Mahler–Lech) and Poonen (arXiv:1307.5887) interpolate
iterates of a **p-adic analytic** self-map `f`: if every coefficient of `f(x)−x` has valuation `> p^{1/(p−1)}` (i.e. `f` is
analytically *close to the identity* / sits at an **indifferent or attracting** fixed point — Rivera-Letelier's trichotomy
indifferent/attracting/superattracting), then there is an analytic `g(x,n)` on `ℤ_p` with `g(x,n)=fⁿ(x)`. This is precisely
the machine that powers the p-adic (SMLC) proof of dynamical Mordell–Lang.

**Why it fails for `T(c)=⌊3c/2⌋`. Two independent obstructions, both fatal:**
1. **Non-analyticity.** `T` is not a p-adic analytic (nor even continuous) self-map of any single `ℚ_p`: the floor mixes the
   archimedean order with the 2-adic carry. The induced odd map `T(o)=3^{D−1}(3o−1)/2^D` has `D=v₂(3o−1)` *varying* over the
   orbit, so it is a *different* analytic branch on each cylinder — not one analytic germ.
2. **Wrong fixed-point régime.** Even on a fixed branch the multiplier is `3/2`, and `|3/2|₂ = 2 > 1`: the map is 2-adically
   **expanding / repelling** at `o=1` (confirmed independently — the Dual-Repulsion Lemma, `REPELLER_ESCAPE.md`:
   `|o−1|₂ ×2` each `D=1` step). Interpolation requires `|λ|_p ≤ 1` (indifferent/attracting); the **repelling** case is
   exactly where the analytic uniformization does **not** extend to `ℤ_p`. The very repulsion the program already proved is
   the structural reason p-adic interpolation cannot reach this orbit.

**The genuine skeleton (the [NEAR-MISS] content).** The closed form `2ⁿc_n = 8·3ⁿ − S_n` (`SESSION_2026-06-29_AEV_CORE.md`)
*does* split off a p-adic-analytic part: since `3 ≡ 1 (mod 2)` is a 1-unit in `ℤ₂`, `n ↦ 3ⁿ` **is** 2-adically analytic
(`3ⁿ = exp_2(n·log_2 3)` on `ℤ₂`), so `8·3ⁿ` is a clean p-adic analytic skeleton in `n`. **But the orbit equals
skeleton − carry**, and the carry `S_n = Σ_{j<n} b_j 2^j 3^{n−1−j}` is exactly the **non-interpolable** piece (it is the
second AEV diagonal, `σ_n`, already identified as the obstruction). So p-adic interpolation cleanly *re-derives* that all the
hardness sits in `S_n` — it does not interpolate the orbit, it confirms the carry is the irreducible non-analytic residue.
Same conclusion as `INTRATERM_ADELIC_MINING.md` reached arithmetically, now from the interpolation side.

*Sources:* Poonen, *p-adic interpolation of iterates* (arXiv:1307.5887); Bell–Ghioca–Tucker monograph; *p-adic interpolation
of orbits under rational maps* (arXiv:2202.01673).

---

## 2. Does Skolem/Mordell–Lang reach the return-set FREQUENCY (= K), or only its STRUCTURE? — [NOT-APPLICABLE to K / ALREADY-CLOSED in effect]

**What the theorems deliver.** For an endomorphism `f:X→X` over a char-0 field and subvariety `V`, the **dynamical
Mordell–Lang conjecture** asserts the return set `{n : fⁿ(x)∈V}` is a **finite union of arithmetic progressions**. The proven
**Weak DML** (Bell–Ghioca–Tucker): if the orbit is Zariski-dense, the return set has **Banach density ZERO**; in general it
is a finite union of APs *plus a set of Banach density zero*.

**Why this is the wrong invariant for (K), three ways:**
1. **Structure, not frequency.** DML/SML describe the return set *combinatorially* (which `n`), giving its density only as
   "0 or trivially-AP-periodic". The kernel needs the **precise positive density** `freq{c_n≡1 mod 2^k} = 1/2^k`
   (equidistribution). No SML/DML theorem produces a non-trivial *positive* density — the entire framework files
   positive-density returns under the "structured AP" bucket and only sharpens the *sparse* remainder.
2. **Wrong régime (density zero).** The sharp Weak-DML output is *Banach density zero*. Our return set has **positive**
   density `1/2^k`. Arithmetic-dynamics return-set theory has literally no machinery for the positive-density case — it is
   designed to prove returns are *rare or periodic*, the exact opposite of an equidistribution (density-exactly-`1/2^k`)
   statement.
3. **The map is non-algebraic, and the AP-structure conclusion is already DISPROVEN.** DML/SML require an algebraic (poly /
   rational / étale) `f`; `⌊3c/2⌋` is none. Moreover, *if* DML's conclusion held the return set would be a finite union of
   APs ⇒ the itinerary eventually periodic — which the program has **proven false** (non-periodicity C3,
   `WALLB_NONATOMIC.md`). So the orbit lives precisely *outside* the algebraic régime where SML/DML bites; the floor's
   non-algebraicity is what *permits* an infinite, aperiodic, positive-density return set, and is the same feature that
   denies the machinery traction.

**Verdict:** SML / dynamical Mordell–Lang reach only return-set **structure** (and in the proven direction, density-zero
rarity); they are blind to the **frequency** that is (K). This is the same single-orbit-vs-structure boundary as the
closed measure-rigidity route, reached from a new direction.

*Sources:* Bell–Ghioca–Tucker, *The Dynamical Mordell–Lang Conjecture* (book); arXiv:1401.6659; Scanlon, *A Euclidean
Skolem–Mahler–Lech–Chabauty method*; arXiv:1610.00367 (positive char.: APs + density-0 + p-arithmetic sequences).

---

## 3. Canonical/dynamical heights, Baker–Rumely / Yuan–Zhang adelic equidistribution, arboreal Galois — [NOT-APPLICABLE]

**Baker–Rumely / Favre–Rivera-Letelier / Chambert-Loir / Yuan–Zhang.** For a rational map `φ` of **degree ≥ 2** on `ℙ¹`
over a number field, there is a canonical measure `μ_{φ,v}` on the Berkovich line at each place `v` such that the **Galois
conjugates of any sequence of points whose `φ`-canonical height → 0** equidistribute to `μ_{φ,v}` (Yuan–Zhang generalises to
higher dimension / small points; Baker–Hsia the polynomial case).

**Why it cannot touch Antihydra.** Every structural hypothesis fails:
- **Degree.** `×(3/2)+floor` is degree 1 and **not algebraic** — there is no `φ` of degree ≥2, hence no canonical height
  and no canonical measure to equidistribute toward.
- **Small points vs growing height.** The theorem equidistributes points of canonical height **→ 0**; the Antihydra orbit
  has archimedean size `≈(3/2)ⁿ` — height **→ ∞**, the opposite limit.
- **Galois conjugates vs one rational point.** It averages over the **Galois orbit** of *algebraic* points; the seed `8` is
  rational with **trivial** Galois orbit and the iterates are rational integers. There is nothing to average over.
- **"All small points" = annealed, not single-orbit.** Even granting an algebraic model, the equidistribution is of a
  *family* (small-height points / their conjugates), i.e. an averaged/"a.e." object — exactly the annealed tier the program
  has already shown is reachable (Rajchman `ν_{2/3}`) but does **not** descend to one orbit (`SECOND_DIAGONAL_RAJCHMAN.md`).

**Arboreal Galois / dynamical degree.** Same gate: arboreal representations and the dynamical-equidistribution theorem
require an *algebraic* rational map and an infinite sequence of *distinct algebraic* points / preimage trees. Antihydra
supplies neither (no algebraic map; one rational forward orbit). Dynamical degree is `1` (affine), carrying no positive-entropy
height machinery. [NOT-APPLICABLE].

*Sources:* Baker–Rumely, *Equidistribution of small points, rational dynamics, and potential theory* (Ann. Inst. Fourier
2006; numdam aif.2196); Baker–Rumely, *Potential Theory and Dynamics on the Berkovich Projective Line* (2010); Yuan,
*Algebraic dynamics, canonical heights and Arakelov geometry*; arXiv:0710.3957 (non-arch. equidistribution); Silverman,
survey on arithmetic dynamics (EMS); arXiv:2407.17415 (arboreal/PCF).

---

## 4. The one thread outside the closed list worth a probe — [NEAR-MISS, genuinely new formalism]

**Siegel's (p,q)-adic analysis / non-archimedean spectral theory for Collatz-type maps** (M.C. Siegel, USC PhD 2022;
*The Collatz Conjecture & Non-Archimedean Spectral Theory* Parts I–III, arXiv:2007.15936, 2111.07883, 2208.11082; Springer
*p-Adic Numbers, Ultrametric Analysis and Applications* 2024–25). This builds a **Fourier theory of functions `ℤ_p → ℤ_q`**
(distinct primes `p≠q`), a "Numen" function `χ_H` encoding a Collatz-type map `H`, a Correspondence Principle relating the
map's dynamics to that object, and a **(p,q)-adic Wiener Tauberian theorem**. It is:
- **Genuinely new here:** not (p,q)-adic, not Numen, not the (p,q)-Wiener Tauberian theorem appears anywhere in the closed
  routes. It is a purpose-built non-archimedean toolkit for exactly `qx+1`-type maps — our induced map is one.
- **Honestly likely to reduce.** The Numen / `χ_H` is a (p,q)-adic *measure/Fourier* object; a Tauberian theorem converts
  decay of its transform into asymptotics — structurally the same *annealed/measure-tier* move as the Rajchman/transfer
  routes already shown not to descend to one orbit. The Antihydra base is `3/2` (non-integer), where the integer-base
  finite-group reductions (cf. Bailey–Crandall, already noted in `WEAPONS_AUDIT`) tend to break.

**Why still worth a probe (the [NEAR-MISS] reason):** Siegel's framework natively carries a *single specified map* and asks
existence/value-distribution questions in a `(2,3)`-adic Fourier dictionary that the program has **not** instantiated. The
sharp question to ask it: does the (2,3)-adic Wiener Tauberian theorem convert decay of the Numen transform into a
**single-orbit** Cesàro density (= K), or — like every other Fourier handle here — only an annealed average? If the latter
(expected), it is one more incarnation of the wall; if the Numen genuinely localizes to the seed-8 trajectory, it would be
the first non-spectral handle on the odd-character subspace the `ENDOGENOUS_UE_BUILD.md` no-go demands. Low prior, but it is
the only arithmetic-dynamics object not yet mapped to the funnel.

---

## 5. Verdict table

| Angle | Reaches return-set FREQUENCY (= K)? | Label |
|---|---|---|
| p-adic interpolation of the orbit (Bell/Poonen) | No — floor map non-analytic & 2-adically *repelling*; only the `8·3ⁿ` skeleton interpolates, carry `S_n` is the non-analytic obstruction | [NEAR-MISS skeleton / NOT-APPLICABLE orbit] |
| Skolem–Mahler–Lech / dynamical Mordell–Lang | No — gives STRUCTURE (finite ∪ of APs) + density-**zero** remainder; never positive density; needs algebraic map; AP-conclusion already disproven (non-periodicity) | [NOT-APPLICABLE / ALREADY-CLOSED in effect] |
| Baker–Rumely / Yuan–Zhang adelic equidistribution | No — needs degree-≥2 algebraic map, small-height points, Galois conjugates; averages a family (annealed), not one orbit | [NOT-APPLICABLE] |
| Arboreal Galois / dynamical degree | No — needs algebraic map + preimage trees; dyn. degree 1 | [NOT-APPLICABLE] |
| Siegel (p,q)-adic Fourier / Wiener Tauberian (Collatz) | Open probe — new formalism for `qx+1` maps; likely annealed-tier (reduces) but native single-map and unmapped | [NEAR-MISS, genuinely-new formalism] |

**Overall:** Arithmetic dynamics is a real new toolbox absent from the closed list, but its return-set theorems control
**structure, not frequency**, and its equidistribution theorems are **algebraic / small-point / averaged** — so every route
either is structurally inapplicable to the non-algebraic floor map or reduces to the **same single-orbit frequency wall**.
The most promising sub-thread is the **Siegel (2,3)-adic Fourier + Wiener-Tauberian** program, the one object not yet tested
against the funnel; the sharpest question to put to it is whether its Tauberian step yields a *single-orbit* Cesàro density
or merely an annealed average (the prior is annealed = reduces).

---

## Sources

- B. Poonen, *p-adic interpolation of iterates*, arXiv:1307.5887.
- *p-adic interpolation of orbits under rational maps*, arXiv:2202.01673.
- J. Bell, D. Ghioca, T. Tucker, *The Dynamical Mordell–Lang Conjecture*, AMS monograph; survey arXiv:1401.6659.
- T. Scanlon, *A Euclidean Skolem–Mahler–Lech–Chabauty method* (Berkeley).
- *The dynamical Mordell–Lang conjecture in positive characteristic*, arXiv:1610.00367.
- M. Baker, R. Rumely, *Equidistribution of small points, rational dynamics, and potential theory*, Ann. Inst. Fourier 56 (2006), numdam aif.2196; and *Potential Theory and Dynamics on the Berkovich Projective Line*, AMS Surveys 159 (2010).
- *Non-archimedean equidistribution on elliptic curves with global applications*, arXiv:0710.3957.
- X. Yuan, *Algebraic Dynamics, Canonical Heights and Arakelov Geometry* (ICCM 2010).
- J. Silverman, survey lecture on arithmetic dynamics (EMS).
- arXiv:2407.17415 (arboreal Galois / PCF rational maps).
- M.C. Siegel, *The Collatz Conjecture & Non-Archimedean Spectral Theory*, Parts I/I.5/II, arXiv:2007.15936, 2111.07883, 2208.11082; USC PhD thesis *(p,q)-Adic Analysis and the Collatz Conjecture* (2022); Springer *p-Adic Numbers, Ultrametric Analysis and Applications* (2024–25).

No machine decided. No label upgraded.
