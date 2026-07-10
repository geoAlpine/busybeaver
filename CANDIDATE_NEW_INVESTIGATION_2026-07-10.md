# The 60 candidate-NEW-engine machines from the 1104 census — deep-dive and honest tally

*Follow-up to `MILESTONE_EXTRACTOR_2026-07-10.md`. The mse census flagged **60 candidate-new
multipliers ≥1.3** (of 109 candidate-new; 49 sit <1.3 and were pre-discounted as fit-curvature),
including **~21 near ×2** ("possible genuine binary-doubling class"). This note determines, per
machine, whether the extracted multiplier is (a) a genuine ×(p/q) engine, (b) a mis-extracted KNOWN
engine, or (c) an artifact of the sawtooth estimator's transient. STRICT: every claim is
`[OBSERVED-extractor]`; **no halting is decided; no label is upgraded.** Interpreter
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact big-int. Scripts:
`cni_x2_probe.py`, `cni_x2_discriminate.py`, `cni_geom_saw_test.py`, `cni_x2_final.py`,
`cni_nonx2_final.py` (rows regenerable from `mse_census.py`).*

## 0. Method — the geometric-sawtooth discriminator (validated on the 17-named gate)

The census reported all 60 candidate-new via the **sawtooth** estimator (0/60 had a transfer signal,
all `conf=med(peak~sqrt-step)` or `low` — never the strong "2-estimator-agree"). The sawtooth's
`peak~√step` self-consistency gate, it turns out, **passes spuriously on the transient startup** of a
plain linear counter (a maxrun climbing 1→2→4 in the first few milestones looks like a ×2 doubling).
So a stable reported label is **necessary but not sufficient** for a genuine engine.

The decisive, transient-immune test: a genuine value-×(p/q) odometer shows a **growing geometric
sawtooth** — its segment **peaks** (in total1 or maxrun) grow by ≈p/q across *many* macro-periods and
span a large range, forever; a linear/bounded counter shows peaks that are flat, erratic, or saturate.
`cni_geom_saw_test.py gate` was validated to **FIRE with the correct multiplier** on every
sawtooth-caught named engine — o4 (1.315≈4/3), o5 (1.331≈4/3), o15 (2.666≈8/3), o18 (2.693≈8/3),
o10 (1.463≈3/2) — and to stay silent on flat observables (the transfer-caught o7/o8/o13/o14/Antihydra
correctly show geomsaw=None, transfer=3/2). No false positive on a constant observable. All results
below are at cap **12–60 M** (multiple caps for robustness).

## 1. The ×2 cluster (21 machines) — HETEROGENEOUS: ~7 genuine, 14 artifact

Applying an affine-doubling fit `v' = 2v + c` to the full-run peak sequence (`cni_x2_final.py`, cap 30 M):

**7 machines show clean geometric ×2 doubling** (peak-ratio 1.94–2.01, low cv, affine fit):

| observable | value map (OBSERVED) | resid | tail peaks | spec |
|---|---|---|---|---|
| maxrun | `v'=2v+2` | **0.000** | 126,254,510,1022,2046,4094 (=2ᵏ−2) | `1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` |
| maxrun | `v'=2v+2` | 0.003 | 126,254,510,1022,2046,4094 | `1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` |
| total1 | `v'=2v−28.5` | 0.004 | 255,478,925,1820,3611,7194 | `1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC` |
| total1 | `v'=2v−28.5` | 0.005 | 222,413,796,1563,3098,6169 | `1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD` |
| total1 | `v'=2v−7` | 0.05 | 329,618,1246,2495,4989 | `1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE` |
| maxrun | `v'=2v+1` | 1.23 (noisy) | 71,143,287,575,1151 | `1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD` |
| total1 | `v'=2v+5` | 0.21 (noisy) | 197,399,594,1193,1693,3391 | `1RB0RB_1LC0LF_1RD0LB_1RE1RC_0RA---_1LA1RE` |

The top 5 are clean (resid ≤ 0.05); rows 1–2 and 3–4 are peak-identical pairs (likely closely related /
TNF-adjacent). **≈5–7 genuinely distinct integer-×2 engines.**

**The remaining 14** near-×2 machines have erratic or saturating peak sequences (cv 0.4–90; e.g.
maxrun peaks `[176,704,61,19,7]`, or total1 flat at a constant): these are **linear-growth (sqrt-t)
polynomial counters or bounded/bouncer structures** whose "×2" was a startup-transient artifact of the
sawtooth. `[artifact]`

### 1a. What the genuine ×2 machines actually are — base-2 ODOMETERS, not pure doublers

Tracing the cleanest one (`1RB0RE_1RC---…`) to 60 M (`cni_x2_probe.py`): the tape builds a **nested
binary cascade** `… 0 1²⁵⁴ 0 1¹²⁶ 0 1⁶² 0 1³⁰ 0 1¹⁴ 0 1⁶ 0 1²` — blocks `1^(2ᵏ−2)`. The maxrun
climbs `14,30,62,126,254,…` to a super-peak that **doubles exactly** (`62,126,254,510,1022,2046,4094,
8190 = 2ᵏ−2`), then **resets to a small value (9, 21, or 31)** and re-climbs. Halt gate: state B
reading a 1 (`1RC---`); **no halt observed to 6·10⁷ steps.**

So these are **genuine integer-×2 engines, structurally base-2 odometers** — the ×2 analog of the
base-3 `×8/3` odometers o15/o18. The doubling **envelope** is a clean `v→2v+c`, but the resets are
**data-dependent** (they vary 9/21/31), i.e. the machine reads digits; it is **not** a pure
deterministic `v→2v+c` orbit.

### 1b. Decidability assessment — `[DECIDABLE-candidate / OPEN]`, NOT decided

The hypothesis was that an integer ×2 might be decidable ("×2 mod M is eventually periodic, unlike the
×3/2 Collatz type"). **This is only half-borne-out and is NOT confirmed:**
- **For decidability:** the multiplier is an *integer* (q=1). A pure deterministic `v→2v+c` orbit
  `v_k=(v₀+c)2ᵏ−c` triggers a fixed-modulus residue gate iff `2ᵏ≡r (mod M)` for some k — **decidable**
  (2ᵏ mod M is eventually periodic). The uniform `v_q`-depth framework (`PAPER_CENSUS.md §2`) degenerates
  at q=1 (2 is not a unit mod 1), so these fall *outside* the (K)/Mahler ×p/q-normality wall.
- **Against:** the observed structure is a base-2 **odometer with data-dependent resets**, not a pure
  orbit — so its protection could still be a base-2 return-frequency statement, the ×2 sibling of the
  o15/o18 base-3 odometer conjectures, and thus (K)-adjacent OPEN.

**Verdict:** the ~5–7 genuine ×2 machines are the **strongest decidability candidates found** and are
**flagged for a per-machine certified proof** (value-map from the transition table + exact halt gate +
reachability, red-teamed 3 ways, exactly the treatment the 17 named received). Until that proof exists
**no decision is claimed.** `[DECIDABLE-candidate]`

## 2. The other 39 candidate-new (non-×2) — mostly artifact; a few genuine

`cni_nonx2_final.py`, cap 30 M (36 of 39 returned a verdict; 3 gave too few segments = undetermined):

- **Mis-extracted KNOWN engine (collapse): 2** — clean geometric →×3/2 (rho 1.428→peak 1.48 cv 0.025;
  rho 1.445→1.48). Plus the robustness cross-check (4 M→12 M) caught **more label→known drifts**
  (`~11/8→×4/3`, `~14/9→×4/3`, `~11/5→×3/2`), which the strict 30 M peak test files under artifact:
  ~2–5 collapse to a known engine.
- **Genuine geometric, non-standard multiplier (candidate-new): 5** — real growing odometers whose
  multiplier does **not** cleanly land on {3/2,4/3,8/3,5/2} but is not robustly pinned to a single new
  rational (cv 0.10–0.24): rho 1.579→1.596, 1.590→1.577, 1.400→1.398, 1.850→1.878, 3.299→3.270. These
  warrant hand follow-up (could be genuine new species, or noisy reads of a known engine). `[OPEN]`
- **Artifact: ~29+3** — no clean geometric peaks (linear/bounded/noisy).

## 3. The honest tally

Of the **60 candidate-new (≥1.3)**:

| class | count | note |
|---|---|---|
| **Genuine geometric ×2 engines** (base-2 odometers) | **~7** (≈5 distinct) | NEW integer-multiplier species; `[DECIDABLE-candidate/OPEN]` |
| **Genuine geometric, other multiplier** | **5** | non-standard ratio, not robustly pinned; `[OPEN]` |
| **Mis-extracted → KNOWN {3/2,4/3,8/3,5/2}** | **~2–5** | collapse (chiefly →×3/2, ×4/3) |
| **Artifact** (linear/bounded/noisy, transient ×n) | **~43–46** | the sawtooth `peak~√step` gate fooled by startup |

Plus the **49 candidate-new <1.3** (pre-discounted): all fit-curvature-near-1 artifacts, confirmed
(none show a growing geometric sawtooth). **Net genuine engines among all 109 candidate-new: ≈12.**

## 4. What this refines about the [C] picture

- The census's headline "~21 near-×2, possible genuine binary-doubling class" is **two-thirds artifact,
  one-third real**: there **is** a genuine binary-doubling species (~5–7 machines, integer ×2, base-2
  odometers), but the sawtooth over-counted it 3×.
- This is the **first genuinely-new engine multiplier** beyond {3/2,4/3,8/3,5/2} to survive scrutiny:
  an **integer ×2**. It is qualitatively distinct — it lives *outside* the (K)/Mahler ×p/q-normality
  wall (q=1 degenerates the unit-depth framework) — so it either (i) forces a **new schema** (a base-2
  return-frequency conjecture, sibling to `NormalityPQ 8 3`), or (ii) is genuinely **DECIDABLE** if its
  reset structure collapses to a pure `2ᵏ mod M` gate. Resolving that dichotomy per-machine is the
  open follow-up and the highest-value decidability target on the frontier.
- The bulk of the 60 (~43–46) are artifacts of the sawtooth transient, and ~2–5 collapse onto known
  engines. So the conjecture set is **not** blown open by scattered new rationals; the only coherent
  new signal is the single **integer-×2** species.

**No machine decided. No label upgraded.**
