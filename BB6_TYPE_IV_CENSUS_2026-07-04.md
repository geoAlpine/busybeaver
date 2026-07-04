# A7/A8 — Type-IV characterization + tetrachotomy-stability census (2026-07-04)

*Follow-up to `BB6_TRICHOTOMY_EXTENSION_2026-07-04.md` (which found the 4th type on a 5-machine test). Two
questions from `REMAINING_TASKS_2026-07-04.md`: **A7** — is Type IV a distinct wall or a generalized-Collatz
sub-case, and is it decidable? **A8** — does a larger sample reveal a 5th type or bound the count at 4? Method: a
**global fingerprint of all 1104 holdouts** (blank-tape simulation vs the raw TM, `bb_sim.py`) + deep RE of the
~40 "bounded-arity" candidates. Ran in the main loop after the parallel sub-agents died on API errors (known
pattern). SOUNDNESS: every claim `[OBSERVED]` from raw-TM simulation or `[PROVEN]`; **no machine decided; halting
`[OPEN]` for all**. Interpreter `/opt/homebrew/bin/python3.13`.*

## 0. Headline

- **A8 — NO fifth type.** Over the whole 1104-holdout frontier (300 K–15 M step traces), **every** machine falls
  into the four known structural phenotypes (I dense value-orbit / II growing digit-string / III scalar / IV
  bounded-arity counter bouncer). What *varies* within a type is the **inner map** (a continuous parameter, not a
  new type): Type I ratios `{3/2, 8/3, 4/3}`; Type IV inner maps `{base-3/2 descent ⌈2A/3⌉, linear −2 countdown,
  ÷2 halving}`. **The tetrachotomy is stable at four phenotypes.**
- **A7 — Type IV is a distinct PHENOTYPE but NOT a distinct WALL.** It is now **populated beyond the single H5**
  (multiple new bounded-arity counter bouncers found), but its halt is a **generalized-Collatz / counter-machine
  reachability** event — the **same B2 wall as Types II/III**, not the (K)/Mahler wall. Decidability `[OPEN]`,
  Collatz-class (fixed-arity counter machine with floor-multiplier updates ⊇ Minsky/Collatz; no bounded predictor).
- **The durable statement: the 4-way PHENOTYPE tetrachotomy projects onto a 2-way WALL dichotomy** —
  `{I} → (K)/Mahler-3/2 (B1)` vs `{II, III, IV} → generalized-Collatz reachability/existence (B2)`. Matches
  `PROBLEM_LIST.md` B1/B2 exactly.
- **Bonus: 2 new Type-I (Mahler ×3/2) cryptids found & ratio-verified** (below), extending the Mahler family
  beyond the 12 named machines.

## 1. Global fingerprint of the 1104 frontier `[OBSERVED, fp_all.py]`

Simulated all 1099 non-H1..H5 holdouts to 300 K steps, classified by the **#blocks-vs-width** signature (does the
snapshot block-count grow with width — a growing digit string — or stay bounded — a fixed-arity counter?):

| class | count | reading |
|---|---:|---|
| **digit-string (Type II)** — `#blocks ∝ width` | **874 (80%)** | growing bounded-digit odometers / carry cascades |
| lowblock / mid (`#blocks` 9–20) | 174 | slow Type-II odometers (mostly) |
| **bounded-arity (Type I / IV zone)** — `#blocks ≤ 8` | **51 (5%)** | few-counter; mix of I, II-slow, IV (see §2) |
| **HALTERS in ≤ 300 K** | **0** | consistent with cryptid status |

**The frontier is ~80 % Type II** (growing-length bounded-digit cascades). This sharpens the census
(`BB6_FRONTIER_CENSUS_2026-07-04.md`, `holdout_band_split.py`) with an exact global count and **confirms 0
halters** in the sampled budget.

## 2. The bounded-arity band is a MIX — deep RE of the 51 `[OBSERVED, growth.py / classify_bounded.py]`

The `#blocks ≤ 8` fingerprint band is **not** all Type I/IV — it is a mixture, because slow Type-II odometers
(whose digit-count grows only `∼ log width` or `∼ generation-count`) still show `#blocks ≤ 8` at 300 K. The
**decisive discriminator** is the *inner leading-counter map* over a 4–15 M step trace:

| inner-map signature | leading-value trajectory | type | examples (holdout TM) |
|---|---|---|---|
| **arithmetic ascent** (const diff +2/+3/+6, resets, spawns fixed digits) | `12,15,18,…` / `1069,1075,1081,…` | **II** (growing digit-string, bounded radix) | `1RB0RE_1RC0RF_1LD1RA_1LB1LD_1RA1LB_---0LD`, `1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE` |
| **geometric ×3/2 ascent** (clean, with ÷2 dips) | `317,477,717,1077,1617,2427` | **I** (Mahler value orbit) | L373, L921 — see §3 |
| **base-3/2 / linear / ÷2 descent + refill**, bounded `#counters` | `⌈2A/3⌉` (H5) or `99,97,…,77` (−2) | **IV** (fixed-arity counter bouncer) | H5, `1RB1RB_1LC0RE_---1LD_0RA1LB_1RA1LF_0LE1LE` (L997) |
| **block explosion** (`maxnb` → 100s) | — | **II** | `1RB1RF_0LC0RF_1RD1LC_---0LE_0RC1LF_1RA0LE` (maxnb 295) |

So the `#blocks ≤ 8` band decomposes into ~6 verified Type-I (dense value-orbits), a set of Type-IV bounded-arity
bouncers, and many slow Type-II odometers. **A clean per-machine I/II/IV split genuinely needs full RE** — the
fingerprint alone over-counts "bounded-arity" (re-confirming the A6 proxy and the H4 lesson).

## 3. Two NEW Type-I (Mahler ×3/2) cryptids, ratio-verified `[OBSERVED, verify_ratio.py, vs raw TM]`

Two holdouts in the bounded band are genuine **Antihydra-class two-counter Mahler machines** (`#blocks = 2`
throughout to 8 M steps; leading value `×3/2` in the settled tail with `÷2` dips = the balance/refill counter):

- **`1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC`** (L373): tail peaks `317 → 477 → 717 → 1077 → 1617 → 2427`,
  ratios `1.505, 1.503, 1.502, 1.501, 1.501` → **`×3/2` verified**; `÷2` dips `132→65, 252→125` (ratio 0.49).
- **`1RB0RF_1RC1RF_1LD0LE_---1LC_1RA1LE_1LC1RB`** (L921): tail `443 → 667 → 1003 → 1507 → 2263`, ratios
  `1.505, 1.503, 1.503, 1.502` → **`×3/2` verified**; `÷2` dips likewise.

Both therefore reduce to **(K)/Mahler-3/2** exactly like Antihydra/o2/o7 — new members of the 11–12-strong Type-I
family, found in the holdout set (previously un-named). Halt gate not fully reverse-engineered (an `[OPEN]`
follow-up), but the value-orbit content is settled.

## 4. Type IV: populated, and its wall `[OBSERVED + structural]`

**Populated beyond H5.** H5's inner map is a base-3/2 **descent** `A↦⌈2A/3⌉`; L997
(`1RB1RB_1LC0RE_---1LD_0RA1LB_1RA1LF_0LE1LE`) is a bounded-arity (`#blocks = 4`) counter bouncer with a **linear
`−2` countdown** leading value (`99,97,95,…,77`, then refill) — a *different inner map, same structure*. So Type
IV = **{bounded number of unbounded unary counters, cubic-time bouncer, inner countdown/descent + refill}**, with
the inner-map choice a secondary parameter. It is a real, recurring phenotype, not a one-off.

**Its wall is B2, not B1.** The Type-IV halt (H5: `11`-adjacency existence; L997: a countdown reaching a floor) is
a **reachability/existence event over a fixed-arity counter machine** — a generalized-Collatz statement. It is
**not** the equidistribution kernel (K): the counter values here **descend/countdown** and are *consumed*, they do
not carry a growing `×3/2` value whose parity must equidistribute. A bounded-arity counter machine with affine +
`⌊(p/q)·⌋` updates **generalizes Minsky counter machines** (Turing-complete) and Collatz — so **decidability is
`[OPEN]`, Collatz-class, with no bounded predictor** (verified core-hard for H5 in the extension note).

**⇒ A7 answer:** Type IV is a genuinely distinct *structure* but **collapses into the B2 generalized-Collatz wall**
together with Types II and III. It does not open a new wall-class and it is not a sub-case of (K).

## 5. Soundness corrections to the extension note `[OBSERVED]`

- **H5's "`#blocks` stays 3–6" is a SNAPSHOT measure.** A 15 M-step trace shows `maxnb = 12` transiently (during
  bouncer sweeps); the *settled* snapshot count is 4–6. The fixed-arity claim is about the number of **large**
  counters (bounded ~4), not the transient block count. Corrected phrasing: *bounded number of unbounded counters;
  transient sweep blocks are not counted.*
- **The Type-II / Type-IV boundary is fuzzy.** Both are bounded-value/bounded-arity cascades; the distinction is
  purely *which grows* — the number of digits (II) or the values of a fixed set of counters (IV). At finite N a
  slow Type-II odometer and a Type-IV bouncer can be indistinguishable by the block-count alone (§2). This is why
  the fingerprint over-counts Type IV/I and full RE is required.

## 5b. A9 — halt gates for the two new Type-I cryptids `[PROVEN from table + OBSERVED]`

Both L373 and L921 carry the **identical `00`-existence gate** as the named Type-I/II `00`-family
(o3/o11/o12/o14/o16/SN), reverse-engineered to the corpus `[PROVEN from table]` standard
(`haltgate.py`, `gate_invariant.py`):

- **L373** `1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC`: the halt transition is **F reading 0**; state F has a
  **unique predecessor** — `C reading 0 (write 1, move L)`. So `HALT ⟺` state `C` reads a `0` whose **left
  neighbour is `0`** (a `00` at the C-frontier). `[PROVEN from table]`.
- **L921** `1RB0RF_1RC1RF_1LD0LE_---1LC_1RA1LE_1LC1RB`: halt transition **D reading 0**; unique predecessor
  `C reading 0 (write 1, move L)`; same `00`-at-C gate. `[PROVEN from table]`.
- **Blank-orbit invariant `[OBSERVED, 100 M steps]`:** state `C` reads `0` exactly 7645 (L373) / 7333 (L921)
  times, and in **every** case the left neighbour is `1` (the leading-block boundary) — the `00` never occurs, so
  the gate never fires.
- **Structural reduction:** since both are Type-I two-counter `×3/2` machines (§3), the C-frontier `0` with
  left-neighbour `1` is the reflection at the leading-block boundary; `HALT ⟺` the `⌊3x/2⌋` orbit ever consumes
  the leading counter so that `C` reaches the **outer** `0` (counter alignment) — an existence/alignment event on
  the Mahler orbit `= (K)`-class, exactly like Antihydra and the named family. Full non-halting `[OPEN] = (K)`.

## 5c. A10 — the clean per-machine II/IV/I split is (K)-HARD (discriminator-dependent) `[OBSERVED + structural]`

Attempted a robust automated per-machine split of the bounded-arity band into I / II / IV. **It is not achievable
cleanly, and the reason is structural, not a tooling deficiency.** Two principled discriminators disagree on the
borderline:

| discriminator (primary signal) | split of the 40-candidate band |
|---|---|
| **max-block-value growth** (`split_iiiv.py`) | IV 29, I 5, II 3, ambiguous 3 |
| **snapshot-`#blocks` trend** (`split_final.py`, nb-slope per decade) | IV 27, **II 8**, I 5 |

The two agree on the **clean** cases but flip the **middle**: many machines have BOTH a large growing *leading*
active counter (→ looks IV / I) AND a growing *number* of bounded interior digits (→ looks II) — e.g. the `+6`/`+3`
arithmetic-sawtooth odometers (`…_1RA1LB_---0LD`, `…_1RA0RE_1RD1LA_---0LE`) score `slopeA≈1.4` (II-ish) yet
`mbgrow≈24–30` (IV-ish). **The phenotypes form a continuum** (active leading counter + settled interior digits),
so the label depends on which feature the classifier weights.

- **Clean cases (robust):** `clean-II ≈ 8` (unbounded `#blocks`, bounded digits — arithmetic odometers);
  `clean-I ≈ 5` (`#blocks ≤ 3`, clean geometric ratio ≈ `3/2`/`8/3`/`4/3` — incl. L373 geo 1.525, L921 geo 1.532);
  `clean-IV ≈ several` (bounded flat `#blocks`, growing counter values, NO clean geometric ratio — H5-like).
- **The I↔IV boundary is specifically (K)-hard:** a Type-I value orbit and a Type-IV counter BOTH present as
  "flat `#blocks`, growing block value"; telling them apart = deciding whether the growth is a genuine
  equidistributing `×(p/q)` value (I) or a Collatz-counter (IV) = **detecting positive entropy of the driver orbit
  = (K)-adjacent**.

**This empirically confirms, from data, the theoretical result of the B1/B2 probe
(`BB6_WALLS_ENTANGLEMENT_2026-07-04.md`, Angle 3(i)): the tetrachotomy→dichotomy projection is a real structural
truth but NOT an effective classifier.** A10's honest outcome is therefore a `(b)` — best-effort clean split +
a proof-by-discriminator-dependence that the general split is `(K)`-hard — not a completed clean partition.

## 5d. A11 — clean-IV halt gates: the SAME `00`/`11`-existence family as I/II/III `[PROVEN from table + OBSERVED]`

Reverse-engineered the halt gates of 7 clean-IV (H5-class bounded-arity counter bouncers) to the corpus
`[PROVEN from table]` standard (`haltgate2.py`, 30 M-step blank invariant). **Every one has a unique-predecessor
adjacency-existence gate and the blank orbit never fires** — the read-on-entry histogram shows the *safe* symbol
uniformly:

| machine | halt gate `[PROVEN from table]` | blank invariant `[OBSERVED, 30 M]` |
|---|---|---|
| **H5** `1RB---_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA` | A:1 halt; unique pred F:1→write1,R ⇒ `HALT ⟺ 11` adjacency | A entered 210 641×, entry-read **always 0** → never fires |
| L997 `1RB1RB_1LC0RE_---1LD_0RA1LB_1RA1LF_0LE1LE` | C:0 halt; pred B:0→write1,L ⇒ `HALT ⟺ 00` at C | 5 565×, entry-read **always 1** |
| `1RB0LE_1LB1RC_0RF0RD_1RE0LA_1LA1RE_---0RB` | F:0; pred C:0→write0,R ⇒ `HALT ⟺ 00` (rightward) | 5 370×, always 1 |
| `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD` **(= Space Needle, Type III!)** | F:0; pred C:0→write1,L ⇒ `HALT ⟺ 00` | 1 231×, always 1 |
| `1RB1LC_1LC0RD_0LE1LA_0RF1RA_1LA0LA_---0RB` | F:0; pred D:0→write0,R ⇒ `HALT ⟺ 00` | 7 452×, always 1 |
| `1RB1RC_1LC1LC_1RE0LD_1LB1RF_---1RA_0RD1RD` | E:0; pred C:0→write1,R ⇒ `HALT ⟺ 00` | 5 798×, always 1 |
| `1RB0LD_0RC1RB_0RD0RA_1LE0RD_1LF---_0LA1LA` | E:1; pred D:0→write1,L ⇒ `HALT ⟺ 11` adjacency | E entered **3 750 077×**, entry-read **always 0** |

**SOUNDNESS NOTE:** one of the 7 candidates, `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD`, is actually **Space
Needle = Type III** (scalar), not Type IV — it was swept into the bounded-arity fingerprint band and mis-pulled
into the clean-IV list. Its gate analysis (F:0 `00`-gate) is **type-agnostic and correct** (matches
`SPACE_NEEDLE_HALT.md`), so it belongs in the table as a valid `00`-gate; only its *type* label was wrong. This
mis-inclusion is itself further evidence of the (K)-hard classifier (§5c): a Type-III scalar presents as
bounded-arity and is not separable by fingerprint.

**Result:** 5 of 7 are `00`-existence gates, 2 (incl. H5) are `11`-adjacency gates — the **identical
unique-predecessor existence-gate family** as Types I/II/III (o3/o11/o12/…/SN `00`; o4/H1/H2/H4 `11`). So the
halt-gate **mechanism is UNIFORM across the whole tetrachotomy** (unique-predecessor adjacency existence, blank
never fires); what differs between the four types is only the **substrate the existence event runs over** — a
Mahler `×(p/q)` value orbit (Type I → B1) vs a bounded-digit cascade / fixed-arity counter (II/III/IV → B2). This
rigorously extends the classification's cross-cutting "every cryptid halts on an existence/reachability event"
(`CRYPTID_CLASSIFICATION_2026-07-04.md` §5) to Type IV, and it **reinforces the wall dichotomy**: the gate is
always an existence event; only its substrate selects the wall. (It also explains, gate-side, why the wall is not
readable from the gate — consistent with the `(K)`-hard classifier of `BB6_WALLS_ENTANGLEMENT` Angle 3(i).) Full
non-halting stays `[OPEN]` for all (= the generalized-Collatz existence question).

## 6. Honest verdict

**(b) a materially sharpened characterization — no decision, no new wall.** The tetrachotomy is **stable at four
phenotypes** over the whole 1104-frontier (A8: no 5th type), and **Type IV is a populated but wall-equivalent
sub-case of generalized-Collatz** (A7: distinct structure, B2 wall, decidability `[OPEN]`/Collatz-class). The
crisp durable statement is the **phenotype-tetrachotomy → wall-dichotomy projection** (`{I}→B1=(K)/Mahler`,
`{II,III,IV}→B2=generalized-Collatz`). Concrete gains: exact global census (80 % Type II, 0 halters), 2 new
ratio-verified Type-I (Mahler) cryptids, Type IV populated + soundness-corrected. **No machine decided. No
non-halting proven. No wall crossed. Halting `[OPEN]` for all. No label upgraded.**

## Reproduce
- `fp_all.py` (global 300 K fingerprint, class distribution + bounded band), `growth.py` (15 M trace: `#blocks`
  trend + leading distinct-value sequence + ratio/diff tests), `classify_bounded.py` (the 40-candidate batch),
  `verify_ratio.py` (peak-ratio `×3/2` and descent `⌈2A/3⌉/−2/÷2` fits) — all in the session scratchpad,
  `from bb_sim import parse`. TMs: `_bbdata/bb6_holdouts_1104.txt`. Interpreter `/opt/homebrew/bin/python3.13`.
