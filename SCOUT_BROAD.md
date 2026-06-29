# Broad cross-disciplinary scout for the BB(6)/Antihydra kernel (2026-06-30)

*A wide scan of fields NOT yet tried by the program, hunting for any near-miss tool that could bound
single-orbit cell-frequencies / mean `D` / the moving diagonal — i.e. reach the HARD side of the
obstruction dichotomy. SOUNDNESS: each lead labelled [APPLICABLE-NEW] / [NEAR-MISS] / [ALREADY-CLOSED] /
[NOT-APPLICABLE]; honest, no over-claim, no label upgraded. WebSearch used heavily. NOT committed.*

---

## 0. The bar a lead must clear (so "new" and "reaches the kernel" are judged correctly)

The kernel (K) = effective equidistribution of **one specified** orbit `c_n = ⌊8·(3/2)ⁿ⌋ mod 2ᵏ`
= mean `D = v₂(3o−1) ≥ 3/2` = base-3/2 normality of the orbit = **Mahler 3/2 / AEV Conj 1.6 at α=8**.
By the program's two impossibility meta-theorems (`BB6_OBSTRUCTION_DICHOTOMY.md` §2,
`WEAPONS_AUDIT_2026-06-29.md` §1): the HARD side is any functional that **separates Haar from the other
feasible invariant measures** on the orbit closure (cell-frequency / 2nd-or-higher moment / measure-entropy
/ occupancy-tail / specified-Haar). Everything PROVEN sits on the FREE side
(orbit-closure/topology/tail/first-moment/annealed/a.e.). **A lead clears the bar only if it can act on a
single specified orbit AND separate Haar within the feasible-measure set** — i.e. a quenched,
specified-point, frequency-level statement. Anything a.e.-in-parameter, annealed/ensemble, extremal/optimised,
first-moment, or support/range-level hits the SAME wall as the closed list.

Closed already (not recounted): vdC/Weyl, Mauduit–Rivat, Baker/Padé/Zudilin, Bernoulli-conv/Rajchman/
Varjú–Yu, twisted transfer operator/thermo, ergodic a.e./Salem–Zygmund, decoupling (BD/BDG), sum-product/
measure-Fourier-decay (Li, Streck, L²-flattening), entropy decrement (Tao), nilsequences/Host–Kra/
Frantzikinakis–Host, effective ×2×3/homogeneous (LM, Datta–Jana, effective Ratner, EMV), BFLM, Algom–Baker–
Shmerkin, AEV, Eliahou–Verger-Gaugry base-3/2, LABS/merit-factor, Gibbs–Markov 2-adic, self-referential
2-adic digit, Mahler-method/arithmetic-dynamics/regular-sequences (sibling scouts).

---

## 1. Ranked table (by promise = genuinely-new × nearness to the frequency kernel)

| Rank | Field | Candidate tool | Genuinely new? | Reaches frequency kernel? | Verdict | Nearest result / citation |
|---|---|---|---|---|---|---|
| 1 | **Arithmetic dynamics / Berkovich potential theory** | canonical-height equidistribution of orbits/Galois-orbits (Baker–Rumely, Favre–Rivera-Letelier, Chambert-Loir) | **YES** — never tried; a bona-fide single-"orbit" equidistribution engine in dynamics | **No** — object & quantifier mismatch (see §2.1) | **NEAR-MISS** | Favre–Rivera-Letelier (Brolin p-adic, arXiv:math/0407469); Baker–Rumely, Ann. Inst. Fourier 2006 |
| 2 | **Math-physics: non-Pisot diffraction / aperiodic-chain spectral theory** | diffraction = single-sequence autocorrelation; non-Pisot ⇒ singular-continuous multifractal spectrum | **YES (framing)** — only framework whose native object is one deterministic sequence's 2nd moment | **No** — needs substitution/model-set structure we lack; spectral measure = annealed | **NEAR-MISS** | non-Pisot self-similar diffraction singular-continuous (Phys. Rev. B 45 (1992) 176); aperiodic Schrödinger spectra |
| 3 | **Probabilistic NT: large-deviation / renewal model of the D-sequence** | Erdős–Kac/Kubilius/Cramér heuristic + discrete-renewal LDP for `D=v₂(3o−1)` | **YES (framing)** — D-sequence statistics not posed this way before | **No** — a model (needs independence), not a theorem for one orbit = annealed tier | **NOT-APPLICABLE** | discrete-time renewal LDP (arXiv:1903.03527); Kubilius models (Erdős–Kac) |
| 4 | **Non-Pisot β-expansion / univoque combinatorics** | Erdős–Joó–Komornik lexicographic / univoque characterisations in base 3/2 | partly | **No** — structural/combinatorial, no digit-frequency theorem | **ALREADY-CLOSED** (in kind) | Komornik–Loreti; Eliahou–Verger-Gaugry arXiv:2504.13716 (already cited) |
| 5 | **o-minimality / Pila–Wilkie** | sub-polynomial counting of algebraic points on transcendental sets | **YES** — never tried | **No** — upper bound on *algebraic* points, wrong direction; mod-1 wrap not o-minimal | **NOT-APPLICABLE** | Pila–Wilkie counting; Wilkie's conjecture for `R_exp` |
| 6 | **Sarnak / Möbius disjointness** | disjointness of zero-entropy systems from μ(n) | partly | **No** — needs zero *topological* entropy (ours = log 2); and bounds correlation with μ, not self-frequency | **NOT-APPLICABLE** | Sarnak conj.; arbitrarily-slow-decay arXiv:2406.06956 (already cited) |
| 7 | **3-distance / Ostrowski for log₂3; inhomog. Diophantine** | Ostrowski numeration, three-gap for `{n log₂3}` | partly | **No** — controls only the leading/foothold phase (depth Θ(log N)) | **ALREADY-CLOSED** (=top-digit) | `EFFECTIVE_TOPDIGIT.md`; Ostrowski–Diophantine surveys |
| 8 | **Additive comb. inverse theorems / higher-order Fourier (GTZ)** | inverse Gowers-norm theorem on the carry | No | **No** — structure theorem returns a *nilsequence* (polynomial); same as §4 of FRESH_ANGLES | **ALREADY-CLOSED** (=nilsequence wall) | Green–Tao–Ziegler, Ann. Math. 176 (2012) |
| 9 | **Condensed math / perfectoid / p-adic Hodge / tropical** | — | YES (untried) | **No** — cohomological/geometric, carry no orbit-statistics functional | **NOT-APPLICABLE** | (no dynamical-frequency content) |

---

## 2. The top genuinely-new leads (the only ones worth a second look) — one sentence each on why

**2.1 Arithmetic-dynamics / Berkovich canonical-height equidistribution [NEAR-MISS, best long-shot].**
This is the one genuinely-new field that *natively* proves equidistribution of a dynamically-defined orbit to a
canonical measure (Favre–Rivera-Letelier's p-adic Brolin theorem; Baker–Rumely / Chambert-Loir adelic
equidistribution of small points) — so conceptually it is the closest "new equidistribution engine" the
program has not tried. **Why it does not reach the kernel:** it equidistributes (i) *backward* orbits /
preimages or *Galois orbits* of a sequence of points whose canonical **height → 0**, under (ii) a map of
**degree ≥ 2** with a genuine canonical height; Antihydra is the **forward** orbit of a **single** point of
**growing** height under the **degree-1 affine** map `×(3/2)` — every one of the three hypotheses fails, so
the theory's measure is the wrong object. (The S-arithmetic solenoid reframing in `EMPTY_TOOLBOX_QUESTION.md`
is exactly the attempt to manufacture the missing height/degree structure, and it remains amenable+rank-1 =
empty toolbox.)

**2.2 Non-Pisot diffraction / aperiodic-chain spectral theory [NEAR-MISS, most thought-provoking].**
Diffraction theory is the unique surveyed framework whose object is literally a *single deterministic
sequence's autocorrelation* (a second-moment, single-orbit quantity — exactly the HARD-side type), and the
established fact "non-Pisot self-similar ⇒ singular-continuous, multifractal diffraction (no Bragg peaks)"
sits on our two axes. **Why it does not reach the kernel:** the computable diffraction theory requires
substitution / cut-and-project (model-set) structure to identify the spectral measure, whereas our parity
word is provably irregular (only a subword-complexity floor `p(ℓ)≥1.71ℓ`, non-automatic); and the resulting
spectral measure is the **annealed/ensemble** autocorrelation — it coincides with the already-mined Rajchman
`ν_{2/3}` picture and says nothing about the quenched cell-frequency. It re-frames the "self-induced disorder"
metaphor with rigorous vocabulary but imports no specified-orbit theorem (consistent with the LABS verdict in
`EMPTY_TOOLBOX_QUESTION.md` §1).

**2.3 Probabilistic-NT large-deviation / renewal model of the D-sequence [NOT-APPLICABLE, sharpest heuristic].**
Casting `D_j=v₂(3o_j−1)` as a renewal-reward process gives the cleanest *prediction* (mean `D=2`, Gaussian
Erdős–Kac-type fluctuations, an LDP rate function pinning even-density at 1/2) and is a new way to organise the
statistics. **Why it does not reach the kernel:** every such theorem assumes independence / a sieve /
Cramér-model randomness; for the one deterministic seed-8 orbit there is no independence to invoke, so it
reproduces precisely the annealed renewal attack already banked (spectral gap 0.99, a.e./annealed only,
`antihydra_renewal_attack.md`) — a model, not a proof.

---

## 3. Honest bottom line

**No cross-field tool escapes the HARD side of the dichotomy.** Across nine additional fields the outcome is
uniform and matches the meta-theorem's prediction: each genuinely-new field is either (a) **structurally about
a different object** — degree-≥2 Galois/preimage orbits with vanishing height (arithmetic dynamics),
zero-topological-entropy μ-disjointness (Sarnak), polynomial nilsequences (GTZ), or upper bounds on *algebraic*
points (Pila–Wilkie) — or (b) lands squarely on the **same annealed / a.e. / extremal / structural / leading-phase
tier** that the program's impossibility theorems prove cannot separate Haar from the other feasible invariant
measures (diffraction → annealed spectral measure; renewal/Kubilius → independence model; β-expansion/univoque
→ combinatorial complexity floor; Ostrowski → foothold only). The recurrence is not bad luck: any tool that
does not consume the seed's own arithmetic is constant on `M_feas` and therefore blind to the kernel
(`BB6_OBSTRUCTION_DICHOTOMY.md` §2). The single most interesting near-miss is **arithmetic-dynamics /
Berkovich equidistribution** — it is the only new field that proves orbit-equidistribution as a theorem — but
it is built for the degree-≥2, small-height, Galois-orbit world and cannot be specialised to a forward orbit of
the degree-1 map `×(3/2)`. The diffraction lead is the most conceptually apt (native single-sequence second
moment) but is exactly the annealed Rajchman object in physics vocabulary. **Net: no label upgraded; the
empty-toolbox verdict stands and is now stress-tested against nine further fields.**

---

## Sources

- C. Favre, J. Rivera-Letelier, *Théorème d'équidistribution de Brolin en dynamique p-adique*, arXiv:math/0407469.
- M. Baker, R. Rumely, *Equidistribution of small points, rational dynamics, and potential theory*, Ann. Inst. Fourier 56 (2006).
- A. Chambert-Loir, *Dynamique analytique sur Z. I*, arXiv:2201.08480; *Mesures et équidistribution* (adelic equidistribution).
- L. De Marco, *Critical orbits and arithmetic equidistribution* (ICM lecture notes).
- Non-Pisot self-similar diffraction is singular-continuous/multifractal: *Indexing the diffraction spectrum of a non-Pisot self-similar structure*, Phys. Rev. B 45 (1992) 176; *Inflation vs projection sets / role of the window* (PMC7459767); Pisot conjecture for β-substitutions arXiv:1505.04408.
- Aperiodic-chain spectral theory / Lyapunov exponents: Fibonacci & substitution Hamiltonians, arXiv:cond-mat/0001060; aperiodic photonic bandgap Lyapunov exponents.
- Discrete-time renewal large deviations, arXiv:1903.03527; LDP for renewal-reward, arXiv:2111.01679; Erdős–Kac / Kubilius models (Springer; Wikipedia *Erdős–Kac theorem*).
- V. Komornik et al., univoque / non-Pisot β-expansions (arXiv:math/0610681, arXiv:0805.2047); Eliahou–Verger-Gaugry arXiv:2504.13716 (base-3/2 ↔ 3x+1, already in corpus).
- Pila–Wilkie counting / o-minimality: J. Pila, *O-minimality and Diophantine geometry*; Scanlon, *Counting special points*.
- Sarnak / Möbius disjointness: *Sarnak's conjecture — what's new* arXiv:1710.04039; arbitrarily-slow-decay arXiv:2406.06956 (already in corpus).
- Green–Tao–Ziegler, *An inverse theorem for the Gowers U^{s+1}[N]-norm*, Ann. of Math. 176 (2012) 1231–1372.
- Three-distance / Ostrowski / inhomogeneous Diophantine: Berthé et al. (DMTCS); arXiv:2410.04257; arXiv:2108.06780.
- Effective equidistribution 2025–26 (all rank-≥2/unipotent/semisimple, confirming no rank-1 amenable): arXiv:2601.09983, arXiv:2503.21064, arXiv:2407.12760.
- (repo) `BB6_OBSTRUCTION_DICHOTOMY.md`, `WEAPONS_AUDIT_2026-06-29.md`, `FRESH_ANGLES_SCOUT.md`, `EMPTY_TOOLBOX_QUESTION.md`, `SESSION_2026-06-29_AEV_CORE.md`.

*Convention: literature labelled [PROVEN-in-lit]/[OPEN]; repo facts machine-checked per program policy. No proof
claimed, no label upgraded, not committed.*

**No machine decided. No label upgraded.**
