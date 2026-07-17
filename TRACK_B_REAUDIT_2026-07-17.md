# Track B re-audit — the instrument audit and the island-wide braid verdict (2026-07-17)

*Re-audit of the carry-transparent island (`TRACK_B_ROADMAP_2026-07-16.md`) after the B5
measurement scandal (`885f6de` → corrected by `6b6d739`). READ-ONLY analysis of the machines;
**no Lean file was touched**. Probes: `x2tb_sim.py`, `x2tb_braid.py`, `x2tb_phase.py`,
`x2tb_reset14.py`, `x2tb_pairs.py`. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`,
exact big-int, on-path from each machine's real blank-tape orbit.
**This document decides no halting and upgrades no label.***

---

## 0. Summary of what changed

| # | finding | status |
|---|---|---|
| 1 | The `lo`/`hi` truncation bug (F1) exists in **no live probe**. It never touched the roadmap's `[OBSERVED]` rows — `mse_extract`/`cd_probe`/`cni_*` all maintain both bounds. | **[SETTLED]** |
| 2 | The roadmap's B5 **"CONSTANT reset 14" is REAL** — dense stride-1 verified, gens 1–5, out-of-sample confirmed. Its origin is `cd_probe2.py`, a *correct-extent* instrument. | **[SETTLED]** |
| 3 | `6b6d739`'s "14 is REFUTED / origin UNEXPLAINED" compared **two incommensurable statistics**. Both readings are true of different quantities. The "half-tape bug made 14" lead is a **red herring**. | **[SETTLED]** |
| 4 | A **second, distinct fault class (F2)** — minima taken over sparse samples — underlies the roadmap's *entire* "reset structure" column. Not a truncation; a reading error. | **[OPEN]** for B3/B4/W1 |
| 5 | **B3/B4 are NOT peak-identical.** The roadmap's pairing (and "one analysis covers both") is unsupported. | **[OBSERVED]** |
| 6 | **B1/B2 pairing survives**, and B2 is **not** a TNF/mirror relabeling of B1. | **[OBSERVED]** |
| 7 | Island count is **≈4 distinct structural problems, not 3** — it went **up**, not down. | **[OBSERVED]** |
| 8 | **Island-wide: every member with a genuine doubling register shows Θ(v²) per-doubling cost.** Track B's founding premise has no surviving support. | **[OBSERVED]** |
| 9 | **W1's register is an arithmetic ramp, not a doubler** — its "×2 envelope" row is unsupported. | **[OBSERVED]** |

---

## 1. THE INSTRUMENT AUDIT

### 1.1 Fault F1 — truncated extent (the x2b5 bug). Scope: contained, and never load-bearing.

The bug of `885f6de`: maintain `lo` at left-record milestones, never update `hi`, so every scan
runs over `range(lo, 0+1)` — the left half-tape. B5's tape is mirror-symmetric about the origin, so
the reading looked coherent.

**Repo-wide sweep** (automated, over all 197 tape-scanning probes; the scan is reproducible — it
flags any file that updates `lo` from the head position without a matching `hi`):

| probe family | extent handling | F1? |
|---|---|---|
| `mse_extract.py` (`simulate`, lines 106–121) | maintains **both** `lo` and `hi`; `_feats(tape, lo, hi)` scans the full extent | **NO** |
| `cd_probe.py`, `cd_probe2.py` | delegate to `mse_extract.simulate` | **NO** |
| `cni_x2_final.py`, `cni_geom_saw_test.py`, `cni_nonx2_final.py`, `mse_census.py` | delegate to `mse_extract.simulate` | **NO** |
| `cni_x2_probe.py` (l.18–19), `cni_x2_discriminate.py` (l.25–26) | maintain **both** bounds in their own loops | **NO** |
| `x2b5_braid/_sawtooth/_invariant/_rle/_sweep/_mod3` | **HAD F1**; now derive extent via `extent(cells)`/`maxrun_full(cells)` (`6b6d739`) | **FIXED** |
| `x2b5_reg.py`, `x2b5_records.py`, `x2b5_shape.py`, `x2b5_halt.py` | both bounds / no extent scan | **NO** |

**Conclusion.** F1 was confined to the `x2b5_*` family and is fixed in all six. **Zero live
instances.** Decisively: **the roadmap's `[OBSERVED]` rows for B1–B5 and W1–W3 do not rest on a
truncated scan** — their instrument (`mse_extract`) was correct on extent all along. The worry that
"the same instrument error may have manufactured other `[OBSERVED]` rows" is **ruled out**.

*(The six `x2b5_*` files still update `lo` and are flagged by the mechanical sweep. This is a false
positive: `lo` survives only as a sampling **trigger**, which is legitimate — deciding *when* to
sample is not deciding *how far* to scan. `x2tb_sim.py` uses the same design.)*

### 1.2 Fault F2 — minima over sparse samples. Scope: the whole "reset structure" column.

The instrument that *did* mislead is different and was not previously named.
`mse_extract.simulate` records a milestone **only at record-extreme excursions**
(`mse_extract.py:99–122`). `cd_probe.peak_reset` and `cd_probe2.peaks_resets` then take

```python
rs = [min(v[a:b]) for a, b in segs]      # min over a BIASED SPARSE SUBSAMPLE
```

The extent is correct and every sampled value is a true full-tape value — but a `min` over a
subsample is **not the minimum over the macro-period**. It is only an **upper bound** on it.

This is the same *consequence* as F1 (max/timing statistics survive, min statistics do not) from a
completely different *cause*. It feeds the roadmap's **entire "reset structure" column**: B1's
"data-dependent 9/21/31", B3/B4's "arithmetic drain 26,22,18,14,10 (−4/gen)", B5's "CONSTANT 14",
W1's "resets +3/gen".

**Dense re-measurement is the only sound test** (`x2tb_reset14.py`, stride-1: maxrun can drop by an
arbitrary amount in a single step when a write splits a run, so *no* stride >1 sample is sound for a
minimum).

| machine | sparse (roadmap) | dense stride-1 truth | verdict |
|---|---|---|---|
| **B5** | floors `4,8,14,14,14,14` | `7,14,14,14,14,14` — floor ≡ **14**, gens 1–5 | **SURVIVES** (gen 0: sparse 8 vs dense 7 — the predicted strict upper bound) |
| **B1** | "data-dependent 9/21/31" | true minima include **9** and **21** | **CONSISTENT** (not overturned) |
| **B3, B4, W1** | drain `26,22,18,14,10`; `+3/gen` | *not re-measured* | **UNSUPPORTED** — an upper-bound statistic, never established as a floor |

**Honest reading:** F2 is a real methodological hazard, but in both cases actually re-measured it
did **not** overturn the sparse reading. The reset column is therefore **not shown to be wrong** —
it was simply never *established*, and three of its rows still aren't.

### 1.3 Fault F3 — a ratio of 4 proves nothing about a register that does not double. *(found in my own first instrument)*

My first pass reported "**W1: BRAID**". It was an artifact, and it is worth recording because it is
the same disease in a new organ:

> For **any** machine whose step count grows like width², the cost to "double" an observable is 4×
> **automatically** — that is every ordinary quadratic bouncer, with no braid anywhere.

A ratio of 4 is evidence only for a register that **genuinely doubles once per macro-generation**.
`x2tb_braid.doubling_gate` now enforces this and **refuses to report a verdict** where it fails
(counting distinct records in the top octave: a doubler sets O(1) of them, a ramp sets ~7·top/8).
W1 fails it outright; the gate is what turned "W1: braid" into "W1: inapplicable".

---

## 2. THE ORIGIN OF "14" — **SETTLED** (and it is real)

**Where it came from.** `cd_probe2.py`, whose docstring asks the question verbatim:

```
(2) 1RB0LB (noisy-maxrun x2): is peak law EXACTLY v'=2v+1 (peaks 9*2^k-1) with constant reset 14?
```

Reproduced exactly with the roadmap's own instrument (`x2tb_reset14.py` pass 1, cap 12 M):

```
peaks  : [19, 37, 71, 143, 287, 575]
resets : [4, 8, 14, 14, 14, 14]      <-- the roadmap's "CONSTANT 14"
```

**It is not the x2b5 bug.** `cd_probe2` → `mse_extract.simulate`, which maintains **both** bounds.
The scan extent was never truncated. **The lead is a red herring:** that the half-tape bug also
produced `floor_2 = 14` is a coincidence of a mirror-symmetric tape, not a shared cause.

**Is 14 real?** It is an F2 sparse-min, so it needed a dense test. Dense stride-1, full-tape,
tape-derived extent:

```
 gen  from peak   to peak   TRUE min maxrun (dense)
   0        19        37                          7
   1        37        71                         14
   2        71       143                         14
   3       143       287                         14
   4       287       575                         14
   5       575      1151                         14      <-- OUT-OF-SAMPLE (cap 16 M)
```

**The true per-generation floor of B5's full-tape maxrun is CONSTANT 14.** `[OBSERVED,
dense-verified k=1..5, out-of-sample confirmed at gen 5]`

**So `6b6d739` over-corrected.** Its claim — *"true floor_2 is 28, so the mechanism is GONE and the
origin of the roadmap's 14 is now UNEXPLAINED"* — compares **two different quantities**:

- **roadmap / `cd_probe2`**: the **minimum of maxrun over the macro-generation** → **14**.
- **`x2b5_braid`**: `traj[i][1]`, the maxrun at the **next state-C left-record milestone after the
  peak** → 16, 28, 46, 88, 166, 328, 646.

Both are true. They are not in conflict, and neither refutes the other. Consequently:

- The roadmap's B5 "CONSTANT 14" is **restored to `[OBSERVED]`**, now dense-verified.
- `6b6d739`'s floors `5·2^k+6/+8` are **not withdrawn** — they remain `[OBSERVED]` *as the
  post-peak milestone value*, which is what they measure. Their unexplained parity split is a
  property of that statistic, not of the floor.
- `885f6de`'s headline mechanism — *"reset 14 = the k=2 tooth recurring verbatim"* — remains
  **[OPEN]**: 14 is now a confirmed constant, but **no mechanism for it is re-derived here**, and
  none is asserted.

---

## 3. THE ISLAND-WIDE BRAID TABLE

**The test** (the one that settled B5): `t_k` = first step the register reaches `V0·2^k`;
`ratio = t_k/t_{k−1}`. **2 = linear (braid-free); 4 = Θ(v²) per doubling** = the B1/x2 cost signature.
Every observable comes from `x2tb_sim.feats()`, whose extent is derived from the tape by
`find`/`rfind` — **F1 is not expressible in the API** (there is no `lo`/`hi` parameter to pass).

**Positive control:** B1's Θ(4^k) doubling wall is independently established (the TOPGRIND,
`ebec409`/`6d8d692`). An instrument that cannot recover it on B1 is not trusted elsewhere. It does.

| machine | register | ratio/doubling | exponent | verdict |
|---|---|---|---|---|
| **B1** *(control)* | maxrun | **3.968** | 1.988 | **QUADRATIC Θ(v²)** — matches its known wall |
| **B2** | maxrun | **3.942** | 1.979 | **QUADRATIC Θ(v²)** |
| **B3** | total1 | **3.985** | 1.994 | **QUADRATIC Θ(v²)** |
| **B4** | total1 | **3.982** | 1.993 | **QUADRATIC Θ(v²)** |
| **B5** | maxrun *(phase-conditioned)* | **4.145** | 2.052 | **QUADRATIC Θ(v²)** |
| **W2** | total1 | **3.944** | 1.980 | **QUADRATIC Θ(v²)** |
| **W1** | total1 | — | — | **INAPPLICABLE** — register is an arithmetic ramp |
| **W3** | total1 | — | — | **INDETERMINATE** — clustered quasi-doubler |

*(cap 40 M; B1–B4/W1–W3 via `x2tb_braid.py`, B5 via `x2tb_phase.py`.)*

**B5 needed a second instrument.** B5's *global* maxrun record is an arithmetic ramp
(…1634, 1637, 1640, 1643, step +3) and **fails the doubling gate** — its doubling register is
**phase-conditioned**, visible only in state C at a left-extent record. Read there, with a
tape-derived extent, `x2tb_phase.py` recovers the register exactly and independently:

```
peak 17, 35, 71, 143, 287, 575, 1151   = 9*2^k - 1  EXACT, k=1..7
ratio  4.119, 4.142, 4.158, 4.145, 4.130, 4.111     median 4.145
```

This is a **third independent reproduction** of B5's braid (`885f6de` 4.10, coordinator 4.09, here
4.145), on an instrument that shares no code with the broken one. *My own first B5 reading of "4.15"
on the global record was itself the F3 artifact — a ramp with steps ∝ v² gives 4 for free. It is not
cited as evidence.*

**W1 is not a doubler.** Its total1 is an arithmetic ramp — 206 → 653 → 1098 → 1545 (step ≈ +446),
reset to 449, climb to 2680, reset to 55 — with maxrun bounded at 5 and ~4050 distinct records in
its top octave. This is exactly the failure mode `CANDIDATE_NEW` itself warned of: *"the sawtooth's
peak~√step gate passes spuriously on the transient startup of a plain linear counter."* The
roadmap's W1 row (*"peak ratio 1.878→1.977→2 → ×2 envelope"*) is therefore **UNSUPPORTED** — its
`[OBSERVED]` ×2 envelope is not visible to a correct full-tape instrument. **W1 is not decided
here**; it needs a re-measure, not a ruling.

---

## 4. THE RE-DERIVED ISLAND COUNT

`59749fb`: *"5 firm candidates (B1–B5) ≈ 3 distinct structural problems (B1/B2, B3/B4, B5)."*
That count rests entirely on **two asserted peak-identical pairs**. Both are re-tested here
(`x2tb_pairs.py`), rather than inherited.

**B1 vs B2 — pairing SURVIVES.**

```
B1 maxrun records: [30, 62, 126, 254, 510, 1022, 2046, 4094]
B2 maxrun records: [30, 62, 126, 254, 510, 1022, 2046, 4094]    IDENTICAL (2^k - 2)
B1 record steps  : [153443, 597615, 2318803, 9212415]
B2 record steps  : [157966, 591922, 2333374, 9186082]           DIFFER
```

Peak values identical across all 8; **step-times differ**. This also settles the roadmap's §2.1
first action: **B2 is NOT literally B1 under a TNF/mirror normalization** — a relabeling would
preserve step counts exactly. B1 and B2 are genuinely distinct machines with an identical register
law. One structural problem. `[OBSERVED]`

**B3 vs B4 — pairing REFUTED.**

```
maxrun records:  B3 [447, 448, 895, 896, 1791, 1792, 3583, 3584]   = 7*2^k
                 B4 [767, 768, 1535, 1536, 3071, 3072, 6143, 6144] = 3*2^k
total1 records:  B3 [..., 1819, 1820, 3610, 3611]   B4 [..., 3097, 3098, 6168, 6169]
step-times differ by ~3x on both observables.
```

**They are not peak-identical on either observable.** What they actually share is a *fit shape*
(both fit `total1: v'=2v−28.5`) — which is a far weaker statement and must not be reported as
identity. The roadmap's *"same as B3 (peak-identical pair) — one analysis covers both"* is
**UNSUPPORTED**: nothing here shows one analysis covers both. **They split into two problems.**

**B5 — a difficulty-class merge, not a structural merge.** B5 shares B1's cost signature, but its
register law (`9·2^k−1` vs `2^k−2`) differs and its register is **phase-conditioned** where B1's is
global. "Same difficulty class" is supported; **"same structural problem" is not established.** B5
subtracts nothing from the structural count.

### The count

| | `59749fb` | this audit |
|---|---|---|
| firm candidates | 5 | **5** (unchanged) |
| distinct structural problems | ≈3 — {B1,B2}, {B3,B4}, {B5} | **≈4 — {B1,B2}, {B3}, {B4}, {B5}** |
| distinct difficulty classes | (not stated) | **1** — all five share the Θ(v²) cost signature |

**The count went UP, not down.** B5's merge removes nothing structural, while the B3/B4 split adds
one. The island is *less* consolidated than `59749fb` claimed, and simultaneously *more* uniform in
difficulty than anyone hoped.

---

## 5. THE ISLAND-WIDE BRAID VERDICT

> **Is the quadratic braid a property of B1, or of the whole island?**
> **On all current evidence: of the whole island.** `[OBSERVED]`

Every island member with a genuine doubling register — **B1, B2, B3, B4, B5, and W2** — pays
**Θ(v²) per doubling**. **Not one ratio-2 machine was found.** B5 was supposed to be the
counter-example and was not; B3/B4, whose arithmetic `−4/gen` resets made them the best remaining
hope for a digit-read-free core (roadmap §2.2), pay the same 4.

**Track B's founding premise — that a friendlier transparent machine dodges B1's braid — has no
surviving support.** The de-risking front does not exist at B5 *or anywhere else on the island*.
The transparent island is not a set of easier problems; it is B1's difficulty, repeated.

### What this verdict is NOT

- **A cost signature is not a mechanism.** Ratio 4 shows a doubling costs Θ(v²) — it is not a
  single-sweep repack but Θ(v) passes over the register. That is the signature the shrinking-comb
  braid *produces*; it does **not** prove the same combinatorial object (the growing-arity digit
  tree / `carry_step`) lives in B2–B5. **No mechanism is asserted for any machine but B1**, where
  it was independently derived.
- **Not a decision.** Nothing here bears on halting for any machine.
- **Not a proof.** An exact envelope does not prove a register law — the roadmap says so, and today
  proved it right twice.
- **B3/B4's `d_k ≡ 0` and arithmetic resets remain real** and remain the island's cleanest
  observables. What died is the *inference* from "cleaner envelope" to "cheaper core."

### Bearing on the roadmap

The `[OBSERVED]` labels for B2/B3/B4 **survive on extent** (their instrument was never truncated),
but the roadmap's structural reading of them does not: the B3/B4 pairing is refuted, W1's ×2
envelope is unsupported, and the reset column for B3/B4/W1 rests on an upper-bound statistic.
**No label is upgraded or downgraded here** — that is the owner's call.

---

## 6. METHOD NOTE — what actually generalizes

`6b6d739` concluded: *"the register law and braid ratio survived only because they are max/timing
statistics; every min-statistic built on the same scan was wrong. That is luck, not method."*
This audit **sharpens that and partly contradicts it**:

1. **The rule is right and generalizes** — but not for the stated reason. The dividing line is
   **max/timing vs. min**, and it cut the same way under *two unrelated causes* (F1 truncation, F2
   sparse sampling). A min is fragile under **any** partial view of the orbit; a max/timing is not.
   That is structural, not luck.
2. **But the min-statistics were not all wrong.** Both dense re-measurements (B5→14, B1→9/21)
   **confirmed** the sparse reading. F2 makes a min *unsupported*, not *false* — and `6b6d739`
   itself then made the mirror-image error, declaring "14 REFUTED" from a statistic that never
   measured the floor. **Over-correction is a measurement error too.**
3. **The new rule this audit adds:** a probe must **gate its own applicability**. My W1 "braid" was
   a correct measurement of a quantity that meant nothing, and no extent-discipline would have
   caught it. `doubling_gate` refusing to answer is the only reason W1 isn't in the table.
4. **Structural defence beats vigilance.** `x2tb_sim.feats()` takes only the tape; F1 cannot be
   written against it. That is why the F1 sweep is now a *closed* question and F2 is not — F2 is
   still a discipline, and disciplines fail.

---

*Probes: `x2tb_sim.py` (tape-derived extent), `x2tb_braid.py` (generic cost ratio + doubling gate),
`x2tb_phase.py` (B5's phase-conditioned register), `x2tb_reset14.py` (dense floor / the 14),
`x2tb_pairs.py` (pairing tests). All results `[OBSERVED, exact simulation, cap 12–40 M]`.
No Lean file was touched.*

**No machine decided. No label upgraded.**
