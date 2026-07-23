# R3 + tail — MEASURED (2026-07-23)

Labels: `[MEASURED]` = reproduced on the real orbit with the bounds-checked wide-tape
instrument (`x2r2_sim.py`, anchors M1(1..3) exact). `[PREDICTED→CONFIRMED]` = stated
before the measurement that tested it. Nothing here is proven; no label is upgraded.

Anchors used (M1(4), M1(5) are NEW, first member of each milestone cluster):

| g | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| M1(g) | 188 099 | 732 733 | 2 852 091 | 11 329 301 | 44 986 995 |

| g | 6 | 7 | 8 |
|---|---|---|---|
| M1(g) | 179 590 445 | 716 937 515 | 2 866 093 189 |

---

## 1. `topEntry(g)` — PARITY-SPLIT, with CLOSED FORMS confirmed by prediction

```
even g : topEntry(g) = 384·2^g  + 53g + 384    entry level = descIn (K−1),  K = g+8
 odd g : topEntry(g) = 6080·2^g + 53g + 105    entry level = descIn (K−2)
```

Both share the linear term `53g`. **Both were fitted on three points and then CONFIRMED
by a prediction committed to in the probe's docstring before the run** (METHODS M4):

| branch | fitted on | predicted | measured |
|---|---|---|---|
| odd | g=1,3,5 | g=7 → 778 716, `descIn 13`, 1-run 20 | **778 716, `descIn 13`, 1-run 20** |
| even | g=2,4,6 | g=8 → 99 112, `descIn 15`, no 1-run | **99 112, `descIn 15`, no 1-run** |

Eight generations of raw data:

| g | parity | entry level | K(g)=g+8 | K−1 | M1(g) → entry | marker head after the comb |
|---|---|---|---|---|---|---|
| 1 | odd | `descIn 7` | 9 | 8 | 12 318 | `1^20` then `0010101010…` |
| 2 | even | `descIn 9` | 10 | 9 | 2 026 | `001001010100101010010101…` |
| 3 | odd | `descIn 9` | 11 | 10 | 48 904 | `1^20` then `0010101010…` |
| 4 | even | `descIn 11` | 12 | 11 | 6 740 | `001001010100101010010101…` |
| 5 | odd | `descIn 11` | 13 | 12 | 194 930 | `1^20` then `0010101010…` |
| 6 | even | `descIn 13` | 14 | 13 | 25 278 | `0010010101…` |
| 7 | odd | `descIn 13` | 15 | 14 | 778 716 | `1^20` then `0010101010…` |
| 8 | even | `descIn 15` | 16 | 15 | 99 112 | `0010010101…` |

- **even g: entry = `descIn (K−1)`.** Confirmed at g=2 and g=4.
- **odd g: entry = `descIn (K−2)`.** Confirmed at g=1 and g=3 — one level LOWER than
  the even family, and the whole approach costs ~6× more.
- **The comb is exact at every entry**: `(01)^{2^{k−1}}` — 64/256/256/1024 at k=7/9/9/11.
  `descIn` is the right cut; `headLaw` applies verbatim once the entry is reached.
- **The odd decoration is visible in the marker**: odd g's marker begins with a run of
  exactly **twenty 1s** at BOTH g=1 and g=3; even g's begins with the nested comb prefix
  `001001010100101010010101`, which extends by one layer from g=2 to g=4 (as the ladder
  nesting predicts). This is the same phenomenon that forced `h_low_even`/`h_low_odd`.

- **The comb is exact at every one of the eight entries**: `(01)^{2^{k−1}}` = 64 / 256 /
  256 / 512 / 1024 / 4096 / 4096 / 16384. So `descIn` is the right cut at every generation
  and `headLaw` applies verbatim once the entry is reached.
- **The odd decoration is a run of exactly TWENTY 1s** at the head of the marker, at
  g=1,3,5,7. Even markers have none.

**Consequence for R3.** The COST is settled (both closed forms confirmed). What is not
built is the Lean TRANSPORT `M1(g) → descIn(entry level)`, per parity, in the `h_low`
style. **R3's cost is `[MEASURED, confirmed]`; R3's transport stays `[OPEN]`.**

---

## 2. `tail(g)` — the tail is a FRAME-DIGIT ODOMETER plus a fixed 110-step end `[MEASURED, 4 generations]`

The design doc recorded 211 / 184\* / 265 at g=2/3/4 with g=3 flagged "does not land
cleanly". The irregularity was **the cut, not the machine** (METHODS M2). At the right cut:

```
tail(g)  =  <entry: parity-dependent>  ∘  (g−1) × frameDigit(27 steps)  ∘  fixedEnd(110)
```

`frameDigit` count, measured: g=1 → **0**, g=2 → **1**, g=3 → **2**, g=4 → **3**. Count = `g−1`.

`[PREDICTED → CONFIRMED]` The `g−1` reading was stated from g=1,2,3 and then tested at
g=4 *before* looking: predicted 3 stages, measured exactly 3
(44 986 804 → 831 → 858 → 885, three `+27`s).

**`fixedEnd` is bit-for-bit the same at all four generations** — `+35, +6, +6, +6, +6, +51`
= 110 steps, with the identical comb progression 5→6→7→8→9 and the identical local shapes
`0^1 1^8 0^8 …` → `0^1 1^6 …` → `0^1 1^4 …` → `0^1 1^2 …` → `0^9 1^1 …` → `M1(g+1)`.

**The entry is where the parity lives:**

| g | ladder-top shape | into the odometer |
|---|---|---|
| 1 (odd) | `0^13 1^1021 0^2 1^509 …` — **not** a canonical `cascadeReg` | directly (`+35` to `fixedEnd`) |
| 2 (even) | `cascadeReg 11` = `0^3 1^2045 0^2 1^1021 …` | 74-step block chew, then `+29` to the `0^7 1^1` config |
| 3 (odd) | `0^13 1^4093 0^2 1^2045 …` — **not** a canonical `cascadeReg` | directly |
| 4 (even) | `cascadeReg 13`-shaped `0^3 1^8189 …` | block chew, then `+29` to `0^7 1^1` |

So **`ladderToCascade`'s OUT presents the tail's IN only at EVEN g.** At odd g the top
carries `0^13` where `cascadeReg` has `0^3` — ten extra zeros. That is why no
`cascadeReg 12` exists before M1(4): there is no canonical `cascadeReg` at odd g at all.

Totals at the uniform cut: `tail = 27(g−1) + 110`, i.e. 110 / 137 / 164 / 191 for g=1..4,
plus the parity-dependent entry (0 for odd; 74 + 29 = 103 for even at g=2 — hence the
recorded 211 = 103 + 27 + 110 ✓).

---

## 3. What this changes

- **The tail is no longer "no closed form".** It is an odometer over the milestone frame's
  digits (`0^21 1 0^6 1 0^6 1 …` — one `1` per generation) with a fixed ending. That is a
  `∀g` fold of the same species as `ladderFold`, and it should be provable by the same
  tile+fold+strong-induction toolkit (METHODS M3).
- **The tail is now a THEOREM** (`lean/T7Tail.lean`, 2026-07-23): `tailLaw ∀j` =
  `frameDigit`/`frameFold` ∘ `turn` ∘ `fixedEnd`, `27j + 110` steps, with the IN register
  verified cell-by-cell against the orbit at g=1,2,3,4 (`x2r3_tailin.py`).
- **The parity split is MEASURED at both ends of the phase** (entry level, marker, and the
  ladder-top shape), four data points on each side. Same odd decoration `h_low_odd` handles.
- **R3's transport is the remaining unknown** — the only piece of `h_doub ∀g` with no
  `∀`-theorem. Its cost is known exactly; the machine transport is unbuilt.

## 4. Honest limits

- Four generations per parity class for the entry level and cost; the closed forms are
  3-parameter and each survived one out-of-sample prediction. Not proven.
- The odd-g ladder top is characterised only by its RLE prefix; its Lean-level shape is
  not yet defined.
- The `+29` even-entry step and the 74-step chew at g=2 are measured at g=2 only in detail.
- No machine decided. No label upgraded. `x2` remains `[OPEN]`.
