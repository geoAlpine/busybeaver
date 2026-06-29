# Cross-field number-theory scout — does any other field give a new angle? (2026-06-30)

*Broad cross-disciplinary survey (4 parallel scouts) asking whether number theory from fields NOT in the program's
closed-routes list gives a genuinely-new attack on the kernel (K) = single-orbit equidistribution of `c_n mod 2^k` /
moving-middle-digit / `mean D ≥ 3/2` = Mahler 3/2 / AEV. SOUNDNESS: every assessment labelled; no claim that any tool
solves (K). Result: the empty-toolbox verdict is robustly confirmed across ~17 fields; 2–3 genuinely-new FORMALISMS exist
that restate the obstruction in a fresh language but, on honest prior, reduce. NOT committed by default.*

---

## 0. One-line verdict

**No new field reaches the frequency kernel.** Every cross-disciplinary tool either is structurally about a *different
object* (degree-≥2 Galois/backward orbits; automatic/Pisot/regular sequences; zero-entropy μ-disjointness; algebraic
points) or lands on the same annealed / a.e. / first-moment / structural tier the impossibility meta-theorems
(`BB6_NO_STRUCTURE_THEOREM.md`) prove cannot separate Haar from `M_feas`. The obstruction dichotomy is now stress-tested
against ~17 fields and stands. **But** the survey surfaced 2–3 genuinely-new *formalisms* — the most natural new languages
to state the obstruction to the relevant communities, each meriting at most one honest probe.

---

## 1. The four scouts — verdicts [all NOT-APPLICABLE / NEAR-MISS→CLOSED to (K)]

| Field (scout) | Tool | Why it fails / reduces | Verdict |
|---|---|---|---|
| Mahler's METHOD (`SCOUT_MAHLER_METHOD`) | functional equations f(z^k)=R(z,f) ⇒ transcendence | no Mahler equation holds (non-automatic, non-Pisot, unbounded carry); even if it did, transcendence ≠ digit frequency | NOT-APPLICABLE |
| Arithmetic dynamics (`SCOUT_ARITH_DYNAMICS`) | Skolem–Mahler–Lech, dyn. Mordell–Lang, p-adic interpolation, Baker–Rumely/Yuan–Zhang | floor map non-algebraic & 2-adically expanding (no p-adic interpolation); SML/DML give only AP-structure + density-ZERO (disproven: non-periodic); height-equidist needs degree≥2/small-height/Galois | NOT-APPLICABLE |
| Regular sequences + recent digit machinery (`SCOUT_REGULAR_DIGIT`) | k-regular (Allouche–Shallit), Bell–Coons–Hare, Byszewski–Konieczny–Müllner Gowers, Jelinek 2025 | not k-regular (exponential growth, infinite kernel); all tools need regularity/automaticity/Pisot the orbit provably lacks; would give mod-2^k density = (K) *if* applicable | NEAR-MISS→CLOSED |
| Broad scan, ~13 fields (`SCOUT_BROAD`) | Berkovich/adelic equidist., non-Pisot diffraction, probabilistic-NT renewal LDP, GTZ nilsequences, Sarnak, Pila–Wilkie, … | each about a different object or on the annealed/a.e./structural tier | NOT-APPLICABLE / NEAR-MISS |

---

## 2. The genuinely-NEW formalisms (fresh languages for the obstruction; honest priors)

These are *not* in the closed-routes list and are the natural homes/communities for the problem. None is expected to crack
(K) (honest prior in brackets), but each restates the wall in a community's native language:

1. **Siegel's (p,q)-adic Fourier analysis / Wiener Tauberian theorem for `qx+1` maps** (arXiv:2007.15936, 2208.11082).
   The only arithmetic-dynamics object that **natively carries a single specified map** in a **(2,3)-adic dictionary the
   program has not instantiated**. [Honest prior: the Tauberian step yields an *annealed* average, reducing like Rajchman;
   but "single-orbit Cesàro density vs annealed" is a sharp, un-probed question.] — the **most genuinely-unexplored** lead.
2. **Akiyama–Frougny–Sakarovitch base-3/2 numeration tree + the p/q-regular decorated-tree criterion**
   (Charlier–Cisternino–Stipulanti, arXiv:2103.16966). Native to `{(3/2)^n}` ("powers of rationals mod 1" *is* the
   kernel); gives a **new formal-language reason for the wall** — the base-3/2 integer language is provably non-regular,
   "defeating every iteration lemma." [Honest prior: linearity = finiteness, blocked by the same growth/complexity; a
   future "almost-linear / graph-directed" relaxation is the only probe spot.]
3. **Non-Pisot diffraction / aperiodic-chain spectral theory** (math-physics). **Conceptually aptest**: diffraction is
   natively a *single deterministic sequence's autocorrelation* — a single-orbit second moment, exactly the HARD-side
   *shape*; and "non-Pisot ⇒ singular-continuous/multifractal spectrum" sits on our two axes. [Honest prior: the computable
   theory needs substitution/model-set structure the irregular orbit lacks; its spectral measure is the already-mined
   annealed `ν_{2/3}`.]
4. **Berkovich / adelic equidistribution** (Favre–Rivera-Letelier, Baker–Rumely, Chambert-Loir). The only new field that
   **proves orbit-equidistribution as a theorem** — but for *backward/Galois* orbits of *small-height* points under
   *degree-≥2* maps; Antihydra is the *forward* orbit of one *growing-height* point under *degree-1* ×(3/2). All three
   hypotheses fail; not currently specialisable. [Honest prior: structurally inapplicable to degree-1.]

---

## 3. Net and recommendation

The cross-field sweep **confirms the empty-toolbox / generational status with much higher confidence** (the dichotomy holds
across ~17 fields, each failing for its own structural reason — a strong robustness check, valuable for the framework
package's "where every method breaks" section). It found **no tool that escapes the dichotomy's HARD side.**

The actionable residue: **the conceptually aptest genuinely-new framing is non-Pisot diffraction** (single-orbit
autocorrelation = the right shape) and **the most genuinely-unexplored formalism is Siegel's (p,q)-adic Wiener Tauberian**
(native single-map, un-instantiated (2,3)-adic). Either merits **at most one honest probe** of its sharp question
(single-orbit vs annealed); both are also the right communities to add to the expert-outreach list in
`BB6_FRAMEWORK_PACKAGE.md` / `EMPTY_TOOLBOX_QUESTION.md`.

**No machine decided. No label upgraded.** (K) remains [OPEN] = Mahler 3/2 / AEV; the empty-toolbox verdict is robustly
cross-field-confirmed.
