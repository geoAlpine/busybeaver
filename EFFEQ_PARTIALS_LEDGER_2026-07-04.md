# Known-partials ledger for the unified EFF-EQ object (floor-orbit equidistribution) (2026-07-04)

*Systematic inventory of what is **proven** toward the unified EFF-EQ hypothesis (`P1PRIME_EFFEQ_LEVERAGE_2026-07-04.md`
§10): an **effective single-specified-orbit** equidistribution rate for the 2-adic-driven floor-orbit
`x_{n+1}=⌊(p/q)x_n⌋+c`, at **linear** depth. Every known result is tiered by **(single-orbit vs a.e./annealed) ×
(depth reached) × (frequency vs spread)**, and the exact stopping point recorded. SOUNDNESS: `[PROVEN]` /
`[PROVEN-in-lit]` / `[OBSERVED]` labels; no machine decided; the target stays `[OPEN]` = Mahler 3/2 / AEV.
The literature rows (§B) are WebSearch-verified (agent probe, 8 threads, 21 tool-uses); the internal rows (§A) are
the program's banked partials. **Result: no result reaches the target; the "empty toolbox" is sharpened to "empty
of frequency/linear-depth weapons, with two building blocks (Stewart's shape, Fan–Fan–Ye's object).**

## 0. The tier ladder (what "reaching the object" means)

The unified EFF-EQ object needs, simultaneously: **single specified orbit** (not a.e./ensemble), an **effective
rate**, at **linear 2-adic depth** (`~n` digits after `n` steps), controlling **frequency** (not spread/range). The
tiers, weakest-to-target:

`[density-0/count]` ⊂ `[annealed]` ⊂ `[a.e./metric]` ⊂ `[single-orbit topological]` ⊂ `[single-orbit
magnitude/log-depth]` ⊂ **`[single-orbit, effective, linear-depth, frequency]` = the target**.

## A. Internal banked partials `[the program's proven results]`

| result | statement | tier | why it stops |
|---|---|---|---|
| **`#even(n) ≥ 0.89 log₂ n`** (`EVEN_COUNT_FLOOR.md`) | the tightest unconditional density-style fact | **single-orbit, log-depth, frequency** | uses ONLY the magnitude ceiling (one deep run `≤ log₂ c_n`); improving = cylinder-visit frequency = `(K)`. **Fresh check:** at `n=2·10⁵`, `#even=100037` vs floor `15.67` — **6383× loose**; truth `#even/n→0.50`, target `≥1/3`. |
| **Top-digit equidistribution** (`EFFECTIVE_TOPDIGIT.md`) | the top `Θ(log N)` binary digits of `c_n` equidistribute, rate via `log₂3` (Weyl + Erdős–Turán) | **single-orbit, log-depth, frequency** `[PROVEN baseline]` | reaches only the top `Θ(log N)` digits — the pigeonhole depth ceiling; the kernel bit is at linear depth. |
| **Subword-complexity floor `p(ℓ) ≥ 1.71ℓ`** | parity word has `≥1.71ℓ` factors of length `ℓ` | **single-orbit, topological** `[PROVEN airtight]` | complexity ≠ frequency; the jump to `2^ℓ` (positive entropy) is `(K)`. |
| **Valuation budget** `Σv₂(3c_i−1)=n+v₂(c_n)−v₂(c_0)`, `v₂(c_n)∈[0,0.585n]` | 2-adic accumulator range | **single-orbit, growth/topological** `[PROVEN]` | controls first moment / max only; the 2nd moment (tail) is `(K)`. |
| **Non-periodicity (C3)**, **`3/2` non-sofic** (Frougny) | the orbit/`β`-shift is aperiodic, not sofic | **single-orbit, topological** `[PROVEN-in-lit]` | no finite-state structure ⇒ no automatic-sequence frequency tool. |
| **Non-Pisot ⇒ `ν_{2/3}` Rajchman** (Varjú–Yu) | `ν̂_{2/3}(ξ)→0` | **annealed** `[PROVEN-in-lit]` | it is the measure over iid digits; the orbit is one point (dim 0); Archimedean not 2-adic. |
| **`dim ν_{2/3}=1`** (Hochman) | annealed measure full-dimensional | **annealed** `[PROVEN-in-lit]` | annealed-only; two gaps (ensemble→orbit, Archimedean→2-adic) to quenched entropy. |

**Best internal single-orbit FREQUENCY partial: `#even ≥ 0.89 log₂ n`** — Θ(log n) depth, and `EVEN_COUNT_FLOOR`
proves this log-floor is **sharp** (no unconditional rung between it and `(K)`).

## B. Literature ledger `[WebSearch-verified]`

Eight threads, every paper verified live (arXiv abstract or bibliographic record). **Target = `[single-orbit,
effective, linear-depth, frequency]` — reached by NONE.**

**Thread 1 — Mahler 3/2 & Z-numbers.**
| result | citation | statement | tier | stops |
|---|---|---|---|---|
| Mahler | *J. Austral. Math. Soc.* 8 (1968) 313–321 | Z-numbers set is countable (density 0); conjectures none exist | `[density-0/count]` | rules out a measure-0 pathology, no orbit frequency |
| FLP | Flatto–Lagarias–Pollington, *Acta Arith.* 70 (1995) 125–147 | `Ω(p/q) > 1/q` (range of `{ξ(p/q)ⁿ}`) | `[single-orbit, ineffective — spread]` | a *range/spread* bound, not equidistribution, no rate (see §C) |
| Dubickas | *Math. Nachr.* 281 (2008) | gaps/spacing of `‖(3/2)ⁿ‖` | `[single-orbit, ineffective]` | Diophantine spacing, not frequency |

**Thread 2 — AEV / rational-base normality.**
| result | citation | statement | tier | stops |
|---|---|---|---|---|
| **AEV normality conj.** | Andrieu–Eliahou–Vivion, **arXiv:2510.11723** (Oct 2025) | Conj 1.6: base-`p/q` seed words are **normal**; implies Akiyama 2008 + Dubickas–Mossinghoff 2009; support: 10⁶ letters | **CONJECTURE** (= the named kernel) | no rate, no proof — it *is* the gap |
| Akiyama–Frougny–Sakarovitch | *Israel J. Math.* 168 (2008) 53–91 | base-`p/q` numeration: non-regular language, finite addition transducer | `[topological/complexity]` | digit equidistribution left open (= AEV) |

**Thread 3 — `(p/q)ⁿ mod 1` discrepancy.**
| result | citation | statement | tier | stops |
|---|---|---|---|---|
| Aistleitner | **arXiv:1210.4215** (*Israel J. Math.* 2015) | exact discrepancy order of `{ξ x^{sₙ}}` for **a.e.** `x` | `[a.e./metric]` | exceptional set contains every rational-base orbit |
| Neeley et al. | **arXiv:1806.03559** | `(3/2)ⁿ mod 1` to `n=10⁸`, "agrees with uniform" | computational | empirical, no theorem |

**Thread 4 — digits of `2ⁿ` base 3 / `3ⁿ` base 2.**
| result | citation | statement | tier | stops |
|---|---|---|---|---|
| **Stewart** | *J. Reine Angew. Math.* 319 (1980) 63–72 | #nonzero base-3 digits of `2ⁿ` is `≫ log n/(log log n + c)`, `c` **effective** | **`[single-orbit, EFFECTIVE — count, log-size]`** | the **only** single-orbit+effective row; but a *count* not a frequency, and `log n/log log n` ≪ linear (near-miss §D) |
| Roettger–Ren | **arXiv:2511.03861** (Nov 2025) | ternary digit UD of `2ⁿ` **unknown**; to `n=10⁶` | comp. + conj. | UD unproven |
| Erdős ternary | Erdős 1979 (status per 2511.03861) | only `2⁰,2²,2⁸` lack digit 2 base 3 — **open** | CONJECTURE | weakest form still open |
| Drmota–Spiegelhofer | **arXiv:2501.00850** (2025) | `(s₂(n),s₃(n))` attains a.a. values; ∞ `s₂=s₃` collisions | `[annealed/ensemble]` | `n` over ℕ, not moving digits of one orbit |

**Thread 5 — metric normality of `⌊(p/q)ⁿα⌋`.**
| result | citation | statement | tier | stops |
|---|---|---|---|---|
| **Fan–Fan–Ye** | **arXiv:2512.05690** (Dec 2025) | `(⌊αxⁿ⌋)` UD in the valuation ring for **a.e.** `x`, `|x|_p>1`; exceptional set **full Hausdorff dim** | `[a.e./metric]` | the p-adic mirror of *exactly* our object — but a.e., full-dim exceptions (near-miss §D) |
| de Mathan–Pollington | (Bugeaud tract) | lacunary `{α rᵢ}` non-dense set has **dim 1** | `[a.e./metric]` | makes the a.e.→every failure explicit (max exceptions) |

**Thread 6 — annealed measure `ν_{2/3}`.**
| result | citation | statement | tier | stops |
|---|---|---|---|---|
| Varjú–Yu | (self-similar Fourier decay, 2020–21) | `r⁻¹` non-Pisot/Salem ⇒ **log** Fourier decay ⇒ Rajchman; applies `ν_{2/3}` | `[annealed]` | ensemble measure, not one orbit; log rate |
| Li–Sahlsten | **arXiv:1910.03463** (*Ann. H. Lebesgue* 2021) | non-atomic self-conformal ⇒ Rajchman (non-Pisot) | `[annealed]` | measure-level |

**Thread 7 — effective equidist. for expanding/affine maps.**
| result | citation | statement | tier | stops |
|---|---|---|---|---|
| transfer-operator | spectral-gap theory (e.g. arXiv:2606.12081) | gap ⇒ effective equidist. of the invariant measure + **a.e.** orbit | `[a.e./annealed]` | one specified point is measure-0; `⌊3x/2⌋+c` **not uniquely ergodic** |
| effective Ratner/unipotent | (homogeneous-dyn program) | polynomial-rate for unipotent flows | `[a.e./homogeneous]` | no bridge to a non-homogeneous floor-orbit |

**Thread 8 — 2022–2026 single-orbit digit frequency.** None. AEV (2510.11723) + ternary-digits (2511.03861) =
conjecture+computation; Fan–Fan–Ye + self-similar decay = a.e./annealed; base-3/2↔3x+1 (arXiv:2504.13716) =
structural. **No paper proves a single-specified-orbit digit-frequency statement.**

## C. The critical distinction — FLP's `1/3` is a SPREAD, not the density `(K)` needs `[PROVEN-in-lit + clarified]`

The literature's strongest *single-orbit* result on `(3/2)^n` is **Flatto–Lagarias–Pollington (Acta Arith. 70
(1995) 125–147):** `Ω(3/2) = limsup_n{ξ(3/2)^n} − liminf_n{ξ(3/2)^n} ≥ 1/3` for every `ξ≠0`. **This shares the
number `1/3` with `(K)` but is a fundamentally different, weaker, orthogonal statement:**

- **FLP `1/3`** bounds the **spread/range** (support of limit points) — it gives **no** upper bound on
  `#{n≤N : {ξ(3/2)^n}∈ arc}` beyond the trivial `N`. A **range** fact.
- **`(K)` `1/3`** is a **frequency/density** — `liminf (1/N)#{even steps} ≥ 1/3`. A **Cesàro** fact.

Spread `⇏` density (an orbit can range over an interval while spending density-0 time in a sub-arc). So the famous
`1/3` coincidence is a **false friend**: the best proven single-orbit result and the target are numerically equal
but logically distinct, and no transfer exists (`FLP` §5, `WEAPONS_AUDIT`). Likewise **Mahler (1968)**: Z-numbers
below `x` number `≤ x^{0.7}` (density 0, countable) — a **support/confinement count**, not a frequency; and
**Dubickas–Mossinghoff (Math. Comp. 78 (2009))** lower-bound Z-numbers — still support, not frequency.

## D. Synthesis — the verdict is "empty of WEAPONS," with two BUILDING BLOCKS `[the sharpened conclusion]`

Every proven result (internal §A + literature §B) sits strictly below the target tier; they cluster at three walls:
**(i) log-depth** (`#even ≥ 0.89 log n`, top-digit `log₂3`, foothold `0.85 log₂N`, Stewart `log n/log log n` — the
pigeonhole ceiling, `6383×` short of the truth at `n=2·10⁵`); **(ii) topological / spread / count** (subword
`1.71ℓ`, non-sofic, FLP `Ω≥1/q` range, Mahler Z-count) ; **(iii) a.e./annealed** (Aistleitner & Fan–Fan–Ye metric
with full-dim exceptions, Varjú–Yu Rajchman, transfer-operator). **The single-orbit / effective / linear-depth /
frequency corner is reached by NONE.**

**But the verdict is sharper than "empty toolbox."** The inventory turns up **two genuine building blocks** (not
weapons) that were under-credited by the flat "empty" framing:

1. **Stewart (1980) — the right SHAPE.** It is the *only* row that is simultaneously **single-orbit AND effective
   AND unconditional**: a computable lower bound on the base-3 digits of the actual sequence `2ⁿ`. It fails the
   target on two axes — it bounds a **count** (not a frequency) and only at **`log n/log log n`** (not linear
   depth) — but it proves that *a deterministic-orbit, effective, unconditional digit theorem is not impossible in
   principle*. So the honest reading is **"empty of frequency/linear-depth weapons," not literally empty.**
2. **Fan–Fan–Ye (arXiv:2512.05690, 2025) — the right OBJECT.** It proves uniform distribution of `⌊αxⁿ⌋` in the
   `p`-adic **valuation ring** — exactly the non-Archimedean, floor-orbit, linear-digit object of the unified
   EFF-EQ hypothesis — but for **a.e.** `x`, with an explicit **full-Hausdorff-dimension fractal exceptional set**.
   It is the **closest existing framework**; if the a.e. could ever be removed at a specified `x` (an
   inclusion/exclusion on its exceptional-set structure), it would be the arena. **AEV (arXiv:2510.11723)** is the
   third block — for the *statement*: it collapses Akiyama-2008 and Dubickas–Mossinghoff-2009 into one normality
   conjecture, so a single weapon there cascades.

**Net.** The log→linear single-orbit-frequency gap is the same wall every route hits (`P1PRIME §7.4`, §9.3); the
literature confirms it from the outside (metric with full-dim exceptions, annealed, or count/spread), and the AEV
conjecture is the crisp published statement of exactly this gap (conjecture + 10⁶ letters). The two building blocks
(Stewart's shape, Fan–Fan–Ye's object) are where a future tool would attach. **No result reaches the target. No
machine decided. No label upgraded.**

**Bridge attempt (`BLOCK_BRIDGE_2026-07-04.md`).** Trying to *connect* the two blocks — feed Stewart's single-orbit
arithmetic into Fan–Fan–Ye's a.e.-removal — **fails and reduces to `(K)`:** excluding `3/2` from Fan–Fan–Ye's
exceptional set needs "equidistributed," Stewart certifies only "not-too-sparse" (a count at log-size), and the
implication between them *is* the count→frequency / log→linear barrier. Stewart and Fan–Fan–Ye are the **count-side
and object-side of one missing theorem**; each has exactly what the other lacks, and their meeting region
(single-orbit ∧ distributional ∧ linear-depth ∧ effective) is the empty target. A bridging theorem = the `(K)`-grade
upgrade. (`p`-adic Baker/Yu variant closes identically — still count/magnitude, still log.)

## Reproduce / basis
- Fresh numeric: `#even/n→0.50` vs floor `0.89 log₂ n` (`6383×` loose at `2·10⁵`), Antihydra `c→⌊3c/2⌋` seed 8.
- Internal: `EVEN_COUNT_FLOOR.md`, `EFFECTIVE_TOPDIGIT.md`, `CITATIONS.md`, `WEAPONS_AUDIT_2026-06-29.md`,
  `BB6_CROSSFIELD_SCOUT.md`.
- Verified literature (§B): Mahler *JAMS* 8 (1968); FLP *Acta Arith.* 70 (1995); Dubickas *Math. Nachr.* 281 (2008);
  AEV **arXiv:2510.11723**; Akiyama–Frougny–Sakarovitch *Israel J. Math.* 168 (2008); Aistleitner **arXiv:1210.4215**;
  Neeley et al. **arXiv:1806.03559**; **Stewart** *J. Reine Angew. Math.* 319 (1980); Roettger–Ren **arXiv:2511.03861**;
  Drmota–Spiegelhofer **arXiv:2501.00850**; **Fan–Fan–Ye arXiv:2512.05690**; Li–Sahlsten **arXiv:1910.03463**;
  base-3/2↔3x+1 **arXiv:2504.13716**.
