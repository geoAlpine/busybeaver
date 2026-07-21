# o17 Myhill–Nerode gate analysis — independent re-verification (2026-07-22)

*Task E1: re-verify the o17 gate-decision analysis of `O17_GATE_DECISION_ATTEMPT_2026-07-10.md`,
which `ROADMAP_COMPLETE_PROOF_2026-07-10.md` §3 flagged as "verification suspended, uncommitted".
Discipline: ZERO false proofs; every claim carries `[PROVEN]` / `[OBSERVED]` / `[OPEN]`.
Instrument-first, per the 2026-07-16 broken-instrument incident (commit `6b6d739`).
Scripts added: `o17_ref_audit.py`, `o17_nerode_scan.py`, `o17_scalar_scan.py`.*

o17 = `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` (halt = F reads 0).

---

## 0. Headline

**The 2026-07-10 analysis is SOUND. Its instrument is clean. Every substantive number
reproduces. The conclusion (o17's gate-safety is not scalar-residue-decidable and its
gate-state shows no finite-automaton saturation) stands, and is now *stronger* than recorded.**

Three defects found, all bookkeeping/labelling rather than mathematical:

| # | Defect | Severity |
|---|---|---|
| **D1** | The recorded Nerode sequences are **not reproducible from the documented command** — they require an undocumented suffix-battery parameter (`sufdig=2`, not the script default `3`). The default gives `1,2,6,19,60,153`, not `1,2,6,19,54,132`. | **Reproducibility (fixed below)** |
| **D2** | The scan count "**0/112**" matches no actual quantity in the sweep. The true sweep is 7 bases × 2 orders × 63 moduli = **882** (base, order, M) triples, or 14 (base, order) settings. | Bookkeeping |
| **D3** | §3 line "a growing lower bound **refutes** finiteness" is an **overstatement**. A finite scan of 7 points cannot refute finiteness; it lower-bounds it. (The document's own "Honest scope" §hedges correctly — the two passages conflict.) | **Label discipline** |

Also: the roadmap's "**未コミット** / uncommitted" flag is **stale** — the document and both
scripts were committed on 2026-07-10 in **`e59df36`**. Nothing was left dangling.

---

## 1. Instrument check `[PASSED]` — the 2026-07-16 failure mode is NOT present

The 2026-07-16 incident was a *decisive probe with a silently truncating tape* (`lo`/`hi`).
The o17 oracle `Fmu(5, d⃗) ∈ {3, 8}` is exactly that class of object, so it was re-implemented
from scratch before any number was trusted.

**Reference implementation (`o17_ref_audit.py`) shares no code with `o17d_*.py`:**

| Aspect | `o17d_finite_state.py` (under test) | reference (independent) |
|---|---|---|
| tape | fixed `bytearray(SZ)`, offset `SZ//3`, **no bounds check** — a negative index would silently wrap | `dict` over unbounded ℤ — truncation structurally impossible |
| frontier ("all-0 to the left") | incremental `L1` heuristic with a rescan branch | exactly-maintained set of 1-positions, `min` recomputed on removal |
| transition table | parsed from the `SPEC` string | transcribed **by hand from `lean/O17.lean` `step`** (machine-checked source) |

**Results — four independent checks, all green:**

1. **Lean anchors `[PROVEN, kernel-checked source]`.** The reference's blank-orbit true-frontier
   A-gates are `(step, pos) = (5,−1), (22,−2), (44,−2), (101,−3), (314,−4), (724,−4), (2005,−5)`
   — **identical** to the `#eval` anchors in `lean/O17.lean` §4. Full configurations at steps
   5 / 100 / 300 match `sanity5` / `sanity100` / `sanity300` exactly.
   *(One cosmetic difference: Lean's `tape.left` retains visited-but-0 cells past the leftmost 1;
   the reference reconstructs from the leftmost 1. Contents agree after trimming.)*
2. **Oracle cross-check `[PROVEN, exhaustive]`.** `o17d_finite_state.Fmu` vs the reference on the
   **full 780-config ensemble** (μ=5, length ≤4, digits 0..4): **0 mismatches**.
3. **Cap headroom.** Max excursion actually observed: **4,009 steps** against a cap of
   **20,000,000** — ~5000× headroom. Across all runs in this verification, **0 of 390,861**
   oracle calls returned a capped or off-language result. There is no truncation artifact
   anywhere in the data.
4. **`o17d_probe.py` re-run** reproduces the §1 orbit table byte-exactly, including the gate
   steps `5, 22, 44, 101, 314, 724, 2005, 1072566`, the digit vectors, and max-digit growth
   `0,0,2,4,6,16,512`.

**Verdict: the instrument is correct.** No truncation, no wraparound, no cap contamination.

---

## 2. Reproduced numbers vs the record

### 2a. TEST 1 — scalar-residue scan `[CONFIRMED, strengthened]`

Is `b(d⃗)` a function of `N = Σ dᵢ·baseⁱ mod M`?

| Sweep | Settings tested | Deciding settings found |
|---|---|---|
| recorded range (base 2..8, M ≤ 64, LSB+MSB) | 882 (base, order, M) triples | **0** |
| **extended** (base 2..12, M ≤ 256, LSB+MSB) | 5,610 triples | **0** |

Confirmed on **both** ensembles (len ≤4 / dig 0..4, and len ≤5 / dig 0..3).
**D2:** the recorded figure "0/112" is wrong — the natural counts are 882 (triples) or 14
(base × order settings). The *result* is unaffected and the extended sweep makes it stronger.

### 2b. Halt fraction `[CONFIRMED, but ensemble-specific]`

- μ=5, length ≤4, digits 0..4: **605 / 780 HALT = 77.6 %**, safe = 175 = **22.4 %**.
  This reproduces the recorded "78 % / 22 %" exactly.
- **Caveat not in the record:** the fraction is *not* an invariant of the machine. On the other
  ensemble the same analysis uses (μ=5, length ≤5, digits 0..3) it is **584 / 1364 = 42.8 % HALT**.
  The "78 %" is a property of one digit/length window, not of "μ=5 configs" in general.
  The qualitative point survives — *safe* is an uncharacterized proper subset — but the
  specific number should not be quoted as a machine constant.

### 2c. TEST 2 — Myhill–Nerode index `[CONFIRMED after locating the missing parameter]`

**D1.** The recorded sequences do not come out of the documented command. Scanning the
suffix-battery parameter space located the actual run: **`suflen=3, sufdig=2`** (40 suffixes).

| ensemble | battery | index sequence (|prefix| = 0,1,2,…) | vs record |
|---|---|---|---|
| dig 0..3, len ≤5 | **40** (`suflen=3, sufdig=2`) | `1, 2, 6, 19, 54, 132` | **EXACT MATCH** |
| dig 0..3, len ≤5 | 85 (`3,3` — the script **default**, i.e. the documented command) | `1, 2, 6, 19, 60, 153` | ≠ record |
| dig 0..4, len ≤4 | **40** (`suflen=3, sufdig=2`) | `1, 2, 7, 25, 77` | **EXACT MATCH** |
| dig 0..4, len ≤4 | 85 (default) | `1, 2, 7, 26, 88` | ≠ record |

So the recorded numbers are **genuine and exactly reproducible** — the `## Reproduce` section of
the 2026-07-10 document is simply missing the argument. It should read
`o17d_finite_state.py 5 3 3 2` and `o17d_finite_state.py 4 4 3 2`.

**Extension (new work).** The record's own sequence continues; larger batteries give strictly
larger counts (a bigger battery resolves more classes, so this is the expected direction):

| ensemble | battery | index sequence | ratios |
|---|---|---|---|
| dig 0..3, len ≤**6** | 40 | `1, 2, 6, 19, 54, 132, **298**` | 2.0, 3.0, 3.17, 2.84, 2.44, 2.26 |
| dig 0..3, len ≤5 | **156** | `1, 2, 6, 20, **81, 260**` | 2.0, 3.0, 3.33, 4.05, 3.21 |
| dig 0..4, len ≤4 | **156** | `1, 2, 7, 29, **142**` | 2.0, 3.5, 4.14, 4.90 |

**A caution the record does not state.** At a *fixed* battery the measured count is capped by the
battery's resolving power, so it *must* eventually flatten regardless of the true automaton.
The declining ratio in the 40-suffix row (3.17 → 2.84 → 2.44 → 2.26) is therefore **an artifact of
the battery, not evidence of saturation** — confirmed by the fact that widening the battery to 156
lifts the same lengths from `54, 132` to `81, 260`. Any future saturation claim from this method
must vary the battery, not just the length. (The recorded "ratio ≈ 2.5–3" was read off the
battery-limited row.)

---

## 3. Claims with strict labels

| # | Claim | Label |
|---|---|---|
| C1 | The gate map `F(μ, d⃗)` as parameterized reproduces the blank orbit's gate census `5,22,44,101,314,724,2005,1072566` and agrees with `lean/O17.lean`'s kernel-checked anchors. | **`[PROVEN]`** (exact finite computation, two independent implementations, Lean-anchored) |
| C2 | On the 780-config ensemble, no residue of `N = Σ dᵢ·baseⁱ` for any base ∈ 2..12, any `M ≤ 256`, either digit order, determines `b(d⃗)`. | **`[PROVEN]`** as a *finite* statement (exhaustive over the stated range) |
| C3 | *Therefore* no scalar gate-value exists for **any** base/modulus, so the symbolic-mod tower weapon has no target. | **`[OBSERVED]`** — the range is finite; unbounded bases/moduli are untested. The independent structural argument (digits grow unboundedly ⇒ no fixed base is a numeral) is the real support, and it is `[OBSERVED]` from the orbit, not proved. |
| C4 | Any DFA reading `d⃗` left-to-right over alphabet {0,1,2,3} and computing `b` has **≥ 298 states**; over {0,…,4}, **≥ 142 states**. | **`[PROVEN]`** as a finite statement. *(Distinct signatures on a finite suffix battery is a valid lower bound on reachable DFA states — two prefixes in the same state agree on all suffixes.)* Not Lean-certified; rests on the cross-validated oracle. |
| C5 | The Nerode index **grows without saturating** across the measured range (7 lengths × 3 batteries). | **`[OBSERVED]`** |
| C6 | **No finite automaton computes `b`** / the gate-state is genuinely unbounded. | **`[OBSERVED]`** — and *only* `[OBSERVED]`. A finite scan cannot exclude a DFA of ≥ 299 states; growth over 7 points is consistent with saturation at any larger value. **The record's §3 wording "refutes finiteness" is not defensible and should be softened to "lower-bounds any automaton at 298 states and shows no saturation over the measured range".** |
| C7 | ~78 % of μ=5 configs HALT; "safe" is an uncharacterized 22 % minority. | **`[OBSERVED, ensemble-specific]`** — exact for (len ≤4, dig 0..4); it is 42.8 % on (len ≤5, dig 0..3). Quote the ensemble whenever quoting the number. |
| C8 | o17's non-halting is decided. | **`[OPEN]` — unchanged. Nothing here decides o17.** |

**Why C6 cannot be upgraded.** This is the repo's standing discipline: a finite computation
cannot certify an infinite closure. The Myhill–Nerode *theorem* gives "regular ⟺ finite index",
but the index is only measurable here as a **lower bound over a finite window**. A growing lower
bound is evidence against regularity; it is a proof of regularity's failure only if the growth is
shown to be unbounded, which requires an argument about `F`, not a table. **`[OBSERVED]` is the
correct and final label** — exactly as the 2026-07-10 "Honest scope" paragraph already said, and
in contradiction to its own §3 sentence.

---

## 4. Verdict

**The 2026-07-10 o17 gate analysis is verified.** Its instrument is sound (0/780 oracle
mismatches, Lean-anchored, 0/390,861 cap events), its scalar-residue negative is confirmed and
extended, its halt fraction is exact for the stated ensemble, and its Nerode sequences
`1,2,6,19,54,132` and `1,2,7,25,77` are reproduced exactly once the missing `sufdig=2` argument is
supplied. The analysis's own conclusion — o17's wall is `(K)`-shaped gate-timing, with no scalar
and no demonstrated finite gate-state — **stands and is strengthened**.

Three corrections belong in the record: the undocumented battery parameter (**D1**), the wrong
scan count "0/112" (**D2**), and the over-strong word "refutes" in §3 (**D3**). None of them
changes a mathematical conclusion.

**o17 remains `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce

- `o17_ref_audit.py [maxlen] [maxdig]` — independent dict-tape reference; Lean-anchor check,
  full oracle cross-check vs `o17d_finite_state.Fmu`, cap/None accounting.
- `o17_scalar_scan.py` — TEST 1 at the recorded range and extended (base ≤12, M ≤256).
- `o17_nerode_scan.py` — Nerode index at the documented default battery, the battery-parameter
  scan that locates the recorded run, and the strengthened lower bounds.
- Original scripts, corrected invocations:
  `o17d_finite_state.py 5 3 3 2` → `1,2,6,19,54,132`;  `o17d_finite_state.py 4 4 3 2` → `1,2,7,25,77`.
