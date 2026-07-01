# BB(6) / Antihydra — Literature Check, July 2026

Kernel (K) = Mahler 3/2 / AEV Conjecture 1.6 = single-orbit equidistribution of ⌊(3/2)ⁿ⌋.
Scope: 2024–2026 priority. Ethos: verify every citation (arXiv/DOI), flag [UNVERIFIED], reject crank/LLM preprints.
Verification key: [VERIFIED-fetch] = abstract fetched and read this session; [VERIFIED-listing] = arXiv id appeared in a live search result, abstract not individually fetched; [UNVERIFIED] = could not confirm id/abstract.

---

## (A) PROBLEM-POINT PAPERS
(Targeting: effective single-specified-orbit equidistribution for a rank-1 / amenable / hyperbolic action; log-vs-linear digit depth; annealed→quenched bridge.)

### A1. Fan, Fan, Ye — "Non-Archimedean Koksma Theorems and Dimensions of Exceptional Sets"
- arXiv:2512.05690, submitted 5 Dec 2025. [VERIFIED-fetch]
- Proves: for local fields F of char 0, (αxⁿ) is uniformly distributed in the valuation ring O for **almost every** x with |x|>1; positive-characteristic analogue under a weighted measure. The set of exceptional x has **full Hausdorff dimension** with q-homogeneous fractal structure.
- Assessment: **Closest in spirit to (K)** of everything found — it is literally the metric (Koksma) theory for (αxⁿ), the family containing (3/2)ⁿ. But it is (i) **almost-every-x**, not a single specified x, and (ii) it explicitly proves the exceptional set is **full-dimensional**, i.e. it does NOT and structurally cannot pin down one named orbit. Same wall as Tao-a.e., Algom–Baker–Shmerkin, Varjú–Yu. Does NOT reach the quenched/single-specified-orbit requirement. Useful only as confirmation that the metric route remains a.e.-bound.

### A2. Andrieu, Eliahou, Vivion — "A Normality Conjecture on Rational Base Number Systems" (the "AEV" paper)
- arXiv:2510.11723, submitted 6 Oct 2025, revised 7 Apr 2026. [VERIFIED-fetch]
- States (conjecture, not theorem) that every minimal/maximal word is normal over an appropriate subalphabet in rational base p/q systems; ties it to Z-numbers (Mahler '68), Z_{p/q}-numbers (Flatto '92), Akiyama triple expansions (2008), the 4/3 problem (Dubickas–Mossinghoff '09).
- Assessment: This IS the conjecture the program already logged as kernel-equivalent input. **No new theorem**; the April 2026 revision adds numerics (richness thresholds, deviation-from-normality), not a proof. Confirms the target is live and still open; contributes no weapon.

### A3. Effective equidistribution "higher-rank / unipotent" front (all structurally off-target)
- Yang, "Effective version of Ratner's equidistribution theorem for SL(3,ℝ)," Annals of Math 2025. [UNVERIFIED-id] — result is real and well known; requires **unipotent** dynamics + higher rank.
- Lindenstrauss–Mohammadi–Wang–Yang, "Effective equidistribution in rank 2 homogeneous spaces and values of quadratic forms," arXiv:2503.21064. [VERIFIED-listing] — explicitly **rank 2**.
- Einsiedler–Lindenstrauss–Mohammadi–Wieser, "Effective equidistribution of semisimple adelic periods…," arXiv:2503.21068. [VERIFIED-listing] — semisimple, higher rank.
- "Polynomially effective equidistribution for unipotent orbits in products of SL₂ factors," arXiv:2601.09983. [VERIFIED-listing] — unipotent.
- Assessment: The entire 2025–26 effective-equidistribution wave is **semisimple / higher-rank / unipotent**. Our action is **rank-1, abelian/amenable, hyperbolic (diagonal ×3/2), single orbit** — none of these hypotheses match. This is exactly the gap the program already isolated (need rank≥2 for rigidity, need unipotent for effective Ratner). Nothing here crosses to rank-1 amenable single-orbit.

### A4. Toral-automorphism density (adjacent, not effective-single-orbit)
- "Density of finitely supported invariant measures for automorphisms of compact abelian groups," arXiv:2507.14113 (Jul 2025). [VERIFIED-listing] — density of periodic/invariant measures, not effective single-orbit equidistribution.
- Assessment: adjacent geometry (compact abelian group automorphism = our solenoid flavor) but produces measure-density statements, not a quenched digit/equidistribution rate. Off-target.

---

## (B) THEORY-BUILDING PAPERS
(Tools to assemble the new number theory: effective Diophantine, large deviations + equidistribution, β/metallic dynamics.)

### B1. Calegari, Dimitrov, Tang — "Arithmetic holonomy bounds and effective Diophantine approximation"
- arXiv:2510.04156, submitted 5 Oct 2025. [VERIFIED-fetch]
- Proves: quantified arithmetic-holonomy bounds giving **effective irrationality measures / linear independence** for high-order roots of an algebraic number; effective irrationality for L(2,χ₋₃) and 2-adic ζ(5); new proof of transcendence of π; algorithmic S-unit / Thue–Mahler / (hyper/super)elliptic resolution; Baker–Feldman power-sharpening of Liouville.
- Assessment: **Strongest genuinely-new 2025 tool found, and the best "building block" candidate.** It is a new, non-Baker (hypergeometric/holonomy) route to *effective* Diophantine constants. BUT: it targets algebraic roots and specific L-values — it does **not** deliver an improved effective irrationality measure for log3/log2 (the quantity the depth-gap in problem-point 2 would need), and it says nothing about equidistribution of a lacunary orbit. Keep on the shelf as the leading effective-Diophantine machine; no direct hook to (K) yet. The exact missing hypothesis: our obstruction needs *linear-in-n digit control of 3ⁿ*, which is a moving-diagonal statement, not an irrationality-measure statement.

### B2. Khayutin — "Large Deviations and Effective Equidistribution"
- arXiv:1511.03452 (2015; not new). [VERIFIED-listing]
- Uses large-deviation estimates for averaging operators (Hecke, higher-rank S-arithmetic) to prove effective equidistribution.
- Assessment: methodologically the closest template for "LDP ⇒ effective equidistribution," which resonates with the program's exact Cramér exponent θ*=log φ finding. But it lives on **higher-rank S-arithmetic quotients with spectral gap**; our rank-1 amenable orbit has no gap to feed it. Structural template only, not applicable as-is. Not new.

### B3. β-shift / metallic-ratio large-deviation literature (background, no 2025 breakthrough)
- "On involution kernels and large deviations principles on β-shifts," arXiv:2101.11814; large-deviation-for-continued-fraction-denominators arXiv:1904.06531; Q-bonacci words/numbers arXiv:2201.00782. [VERIFIED-listing]
- Assessment: confirms LDP machinery on β-shifts and the n-bonacci/metallic constant xᵏ−xᵏ⁻¹−…−1 exists, matching the program's (x−1)(x²+x−1) golden factorization. Useful reference scaffolding for the renormalization/LDP angle, but none is a 2024–26 result that connects a renormalization fixed-point line to arithmetic equidistribution. No new usable theorem.

### B4. Self-similar-measure Diophantine (a.e.-in-support class — already-covered flavor)
- "Khintchine dichotomy for self-similar measures," arXiv:2409.08061; "Khintchine dichotomy and Schmidt estimates for self-similar measures on ℝᵈ," arXiv:2508.09076. [VERIFIED-listing]
- Assessment: same a.e.-in-support character as Algom–Baker–Shmerkin, already assessed insufficient. No single-specified-point escape. Building block only in the weakest sense.

---

## (C) REJECTED CRANK / LLM / WITHDRAWN PREPRINTS
- **arXiv:2411.03468** — N. S. Kumar, "Mahler's 3/2 problem in ℤ⁺." [VERIFIED-fetch] **WITHDRAWN 18 Jun 2025**; author's own comment notes "there are trivial ways to prove the same." Rejected (withdrawn, trivial restricted claim).
- **arXiv:2603.25753** — E. Y. Chang, "A Structural Reduction of the Collatz Conjecture to One-Bit Orbit Mixing" (24 Mar 2026). [VERIFIED-fetch] Reduces (does not prove) Collatz to a "residue-balance mod 32" mixing claim; uses standard math.DS terminology but the core "Map Balance" step is an unproven heuristic reduction. Not a crank per se, but **no rigorous new content usable here**; rejected as non-load-bearing.
- **arXiv:2603.11066** — "Exploring Collatz Dynamics with Human-LLM Collaboration." [VERIFIED-listing] LLM-assisted heuristic exploration. Rejected.
- **arXiv:2601.06208** — "An Extension of the Collatz Conjecture modulo 2ᵖ+2�q." [VERIFIED-listing] Rejected (no equidistribution content, generic Collatz-variant).
- **arXiv:2511.17650** — "A note on two Collatz evolution flows." [VERIFIED-listing] Rejected (heuristic).

---

## (D) NET VERDICT

**The frontier is still empty for the problem points.** No 2024–2026 paper delivers effective, single-specified-orbit equidistribution for a rank-1 / amenable / hyperbolic action, controls the linear-depth (moving-diagonal) binary digits of 3ⁿ, or provides an annealed→quenched derandomization for one deterministic orbit. Every effective-equidistribution advance this cycle (Yang SL₃; Lindenstrauss–Mohammadi–Wang–Yang rank 2; ELMW adelic periods; SL₂-product unipotent orbits) lives in the semisimple/higher-rank/unipotent regime the program already ruled off-target, and the one metric result on (αxⁿ) itself (Fan–Fan–Ye Koksma) is a.e.-with-full-dimensional-exceptional-set — the same a.e. wall as Tao/ABS/Varjú–Yu.

**Single closest problem-point hit:** Fan–Fan–Ye, arXiv:2512.05690 [VERIFIED-fetch] — it is exactly the non-Archimedean Koksma theory for (αxⁿ), so it is the right family and the newest, but it proves uniform distribution only for a.e. x and *explicitly* that the exceptional set is full-dimensional, so it cannot certify the one named orbit (K) needs.

**Single closest theory-building hit (and the only genuinely new, high-quality tool):** Calegari–Dimitrov–Tang, arXiv:2510.04156 [VERIFIED-fetch] — a new hypergeometric/holonomy route to *effective* irrationality measures and linear independence. It is the strongest new machine in effective Diophantine approximation, but it targets algebraic roots and specific L-values and yields no improved effective measure for log3/log2 and no lacunary-orbit equidistribution; it does not touch the moving-diagonal digit obstruction. Worth tracking for a future depth-gap attack, but not presently a weapon against (K).

Bottom line: **no new usable paper for either goal.** Toolbox unchanged; CDT (2510.04156) is the one addition worth shelving for the effective-Diophantine angle, and Fan–Fan–Ye (2512.05690) is the sharpest confirmation that the a.e./quenched gap is exactly where the wall stands.
