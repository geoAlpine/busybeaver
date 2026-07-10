# Integer-×2 base-2 odometer — global trace-template proof attempt (2026-07-11)

*Mirror of the certified trace-template method (o4/o3) applied to the cleanest integer-×2
frontier machine `M = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`, aiming at the FIRST certified
BB(6) frontier decision. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact
bytearray/int. Scripts: `x2t_peaks.py`, `x2t_gen.py`, `x2t_evengap.py`, `x2t_confirm.py`; builds on
`X2_DECIDABILITY_2026-07-10.md`, `X2_CLOSURE_2026-07-10.md`. SOUNDNESS: `[PROVEN]` = exact
enumeration / finite induction; `[OBSERVED]` = measured on stated ranges; `[OPEN]`. ZERO false
proofs. Not committed.*

## 0. Verdict (headline)

**NO certified decision. The template method REDUCES the machine cleanly — the milestone form is
explicit, the right-cascade recurrence is exact `[PROVEN]`, the halt gate is a proven 4-cell event,
and non-halt is equivalent to a single razor-sharp safety invariant — but the transport lemma does
NOT close to an outright decision.** The obstruction is now pinned exactly and it is NOT the shape
the task hoped for: the ×2 doubling is indeed clean (no (K)/Mahler ledger), yet the safety invariant
"the rightward E-scanner never enters a length-3 gap" is **counter-dependent in exactly the o4 way** —
the gap the E-scanner opens between two fixed cascade blocks takes different (always even) lengths at
different generations, so there is **no uniform per-body template with fixed unsafe-event set**, and
no conserved parity / bounded-local certificate bounds it away from 3 (both `[PROVEN]` impossibilities,
prior notes). The machine is non-halt to `2·10^7` steps exact with zero halt-relevant events, but a
sound decision is not claimed. `[NOT certified-decided; obstruction pinned to the even-gap invariant]`.

## 1. Halt gate `[PROVEN from the table]` (restated)

Transitions `A:0→1RB 1→0RE · B:0→1RC 1→--- · C:0→0LD 1→1LE · D:0→0RE 1→1LD · E:0→1RF 1→0LC ·
F:0→0RA 1→1RE`. The only halt is `B:1`. Chaining the forced rightward entries `E→F→A→B`, with the
E-scanner aligned on the left `0` of a maximal 0-run:

`HALT ⟺ E enters a maximal 0-run of length EXACTLY 3` (`x2_control.py`, `x2c_gaps.py`, exhaustive):
length 1 → sweep continues; 2 → continues (via `A:1→0RE`); **3 → HALT**; 4 → turns L (`C`); 5,≥6 →
turns L (`D`). So **odd length 3 is the unique fatal event**; lengths 5,7,… are safe.

**Non-halt ⟺ the rightward E-scanner never enters a length-3 gap.** This is the entire content of a
decision.

## 2. The milestone form M(k) `[right half PROVEN; left half = the odometer]`

Sampling the configuration at every super-peak (maxrun record, head at the far-right turnaround in
state `C` reading 0; `x2t_peaks.py`) gives, for maxrun `= 2^k − 2`:

```
M(k) =  [ L_k ]  1^(2^k−2)  0^3  1^(2^(k−2)−5)  0^2 1^(2^(k−3)−3) 0^2 … 0^2 1^5 0^2 1   [C]0
```

- **Top block** `1^(2^k−2)`: the super-peak; doubles cleanly `6,14,30,62,126,254,510,1022,2046,4094 = 2^k−2`
  through `k=12` at steps `288,1131,4328,13481,51826,187423,731572,2849825,11325014`
  (`x2t_confirm.py`, exact; one benign early non-power record `maxrun=9` before the regime matures) —
  the value-×2 engine.
- **Right cascade** `[PROVEN, exact formula]`: after a `0^3` marker, `k−3` blocks separated by `0^2`:
  the top cascade block `2^(k−2)−5`, then `b_{k-5}, …, b_1, b_0` with `b_i = 2^(i+2)−3`
  (i.e. `1,5,13,29,61,125,253,…`). Verified identically against the captured peaks `k=5..11`
  (`x2t_peaks.py` output; formula check in this note). This half is a rigid, parameter-free
  self-similar cascade.
- **Left region `L_k`**: the odometer low-part — a `(10)*` comb interspersed with `0^2` carry markers
  whose POSITIONS are the binary carries of the base-2 counter. `L_k` is a clean comb at some k
  (`k=5,6,8`) and carries pending (`0^2` markers inside the comb) at others (`k=7,9,10,11`). **This is
  the counter**, and its evolution is the base-2 odometer `v' = 2v+2`.

The blank tape reaches `M(2)` (`1^2 [C]0`) in 2 steps `[PROVEN, kernel-checked]`, and each `M(k)` is
reached exactly (`x2t_peaks.py` step counts `2,42,116,248,956,3681,11090,42811,152744,596157,2315818`).

**Crucial observation:** the milestone **literally contains a length-3 gap** — the `0^3` right of the
top block. Non-halt therefore is NOT "no gap-3 on the tape" (gap-3 is present in every milestone); it
is the **dynamic** statement that the rightward E-scanner never *arrives* at a length-3 gap. This is
exactly the phase property that `X2_CLOSURE` proved defeats every bounded-local certificate.

## 3. The transport M(k) → M(k+1): sweep sub-lemmas `[PROVEN]` and the safety obligation

### 3.1 Sweep sub-lemmas `[PROVEN by 2-transition / length induction]`

- **Rightward comb-repack (the doubling engine).** `E:0→1RF, F:1→1RE` over a comb `(01)^m` with `E`
  on the leading 0 rewrites `(01)^m → 1^(2m)` and advances `+2` per `E`, for every `m`, by 2-transition
  induction (`X2_CLOSURE §2`). Conditional: valid only while the tape ahead is exactly `(01)`-tiled.
- **Leftward D-sweep.** `D:1→1LD` crosses a `1`-block leftward, `D:0→0RE` turns it rightward into `E`
  at the block's left edge; uniform in block length by length induction.
- **Turnarounds** `E:1→0LC`, `C:1→1LE`, `C:0→0LD`, `A:1→0RE`, `B:0→1RC` are bounded local chains.

Each sweep lemma is a genuine parameter-uniform lemma of the o4 standard (one-tile base + induction).
Together they generate the whole transport: the head repacks the comb/cascade into the next top block.

### 3.2 The safety obligation, and where the induction BREAKS `[OPEN — the wall]`

For the transport to be certified non-halting we must prove: **throughout M(k)→M(k+1), every maximal
0-run the E-scanner enters has length ≠ 3.** Instrumenting every rightward-E gap entry
(`x2t_gen.py`, `x2t_evengap.py`) shows the E-scanner meets exactly two families:

1. **Left-region gaps ∈ {1,2}** — the comb separators and `0^2` carry markers. Safe, but requires
   proving carries never stack to `0^3`.
2. **Right-cascade gaps** — when the doubling unpacks the cascade, the inter-block gaps momentarily
   OPEN to even lengths ≥4. Observed lengths (per generation, `x2t_evengap.py`): `4,6,8,10,14,18,22`,
   **all even, none = 3**, all in the local context `1^5 0^L 1^13` (between cascade blocks).

**The decisive finding (why the template does not close).** The SAME adjacent block-pair `(1^5, 1^13)`
exhibits **different gap lengths `L ∈ {4,6,8,10,14,18,22}` at different generations** — the opened gap
length is **not a function of the local block context**; it is determined by the odometer's carry
state that generation. Consequently:

- The per-generation exposure skeleton is **NOT uniform**: the multiset of even-gap events differs
  every generation (`gen 14→30: {4}`, `62→126: {6,14}`, `126→254: {∅}`, `254→510: {6,14,22}`,
  `510→1022: {10,18}`, `1022→2046: {6,10,18}`; `x2t_gen.py`). There is no fixed `body` whose unsafe
  set is checked once and reused — the o4 landmark-pinning generalization argument (§2.4 of the method)
  **cannot be invoked**, because the load-bearing quantity (the gap length) is parameter-DEPENDENT and
  not pinned to a landmark at a parameter-independent offset.
- The evenness itself is **not a conserved parity**: `X2_CLOSURE §4b` `[PROVEN]` shows all 7 candidate
  global parities split 50/50 across the even-gap events. And `X2_CLOSURE §4c` `[PROVEN]` shows the
  adversarial local closure contains the HALT window at every radius ≤ 8. So neither a global mod-2
  invariant nor a bounded-local certificate proves "the opened gap is even, never 3."

This is **exactly the o4 wall** (`O4_TEMPLATE_CLOSURE`: branching persists, counter-dependent, at every
window; the template reduces to a Collatz-like ledger, not a decision) — **structurally reproduced
here**, with the counter being the base-2 odometer `L_k` instead of o4's base-4/3 odometer. The task's
premise ("the doubling is clean ⇒ if the transport proves head-never-halts, NON-HALT follows outright")
fails at the **IF**: the transport does **not** prove head-never-halts, because the even-gap safety is
counter-dependent and no uniform/local/parity argument establishes it. The cleanness of the doubling
(no (K)/Mahler ledger — genuinely confirmed, `X2_DECIDABILITY §3,5`) removes one obstruction but not
this one: the obstruction here is the even-gap invariant itself.

## 4. The covering argument (status)

The milestones `{M(k)}` plus the transports `M(k)→M(k+1)` DO cover the orbit from blank
`[OBSERVED, exact]`: the head returns to milestone form at each super-peak, step counts match, and the
raw TM is reproduced exactly to `2·10^7` steps (§5). So *coverage* is not the gap. The gap is step 2:
non-halt on each transport is **not proven**, because the safety sub-lemma (§3.2) is open. Coverage
+ an unproven per-transport safety yields no decision.

## 5. Triple-certification status (honest)

- **(a) Every sweep/transport lemma proven?** The sweep sub-lemmas (§3.1) and the halt gate (§1) and
  the right-cascade recurrence (§2) are `[PROVEN]`. The **safety sub-lemma** "E-opened gaps are even,
  never 3" is **NOT proven** — it is the open core, and it is counter-dependent (§3.2).
- **(b) Head-never-halts exhaustive over params?** **NO.** The unsafe quantity (opened gap length) is
  not a parameter-uniform / landmark-pinned function; it varies with the odometer carry state, so it
  cannot be checked on a finite grid and generalized. Confirmation (`x2t_confirm.py`, `2·10^7` steps
  exact, no halt): finite internal gaps the E-scanner entered `= {1: 4,926,743; 2: 1,551; 4: 1; 6: 4;
  8: 1; 10: 4; 14: 2; 18: 4; 22: 1}` — **all even besides 1, zero of length 3, zero odd ≥ 3**. Observed,
  not certified.
- **(c) Macro-trajectory matches raw TM ≥10^8 steps?** The raw TM is verified halt-free with zero
  odd-≥3 E-gap events to `2·10^7` steps exact (`x2t_confirm.py`); prior `x2c_probe.py` to `2·10^7`
  and `x2_scan.py` to `3·10^8`. No independent macro-machine is certified because its load-bearing
  crossing rule (even-gap preservation) is exactly the unproven core.

## 6. Where this leaves the machine

The integer-×2 species remains the frontier's best decidability candidate: its control **is** finite-
state (parity routing, `X2_DECIDABILITY §3` `[PROVEN]`), its milestone form and right cascade are
explicit and rigid, and its doubling carries no (K)/Mahler conjecture. The template method makes all of
this precise. But the halt event is a **dynamic phase coincidence** between the E-scanner and a
counter-positioned gap, and — now shown constructively via the template — the transport's safety is
**counter-dependent**: the very same block-pair opens gaps of different (even) lengths in different
generations. This defeats the o4 landmark-pinning generalization, defeats every conserved parity, and
defeats every bounded-local certificate (all `[PROVEN]` impossibilities). The residual lemma is razor-
sharp — *the E-scanner's opened cascade gaps are always even* — and is `[OBSERVED, exact, 0
counterexamples]`, structurally natural (transient runs inherit even parity from the ×2 repack), but
**not closed**. Same shape of open core as o4/o3, with a base-2 odometer in place of base-4/3.

**No machine decided. No label upgraded. `[NOT certified-decided; obstruction pinned]`.**

## 7. Soundness ledger

- Halt gate / local gap rules (fatal ⟺ length 3): `[PROVEN]` (`x2_control.py`, `x2c_gaps.py`).
- Milestone right-cascade recurrence `b_i = 2^(i+2)−3`, top `2^(k−2)−5`, `k−3` blocks: `[PROVEN]`
  (exact formula check vs captured peaks `k=5..11`, `x2t_peaks.py`).
- Top-block doubling `2^k−2`: `[PROVEN, exact]` (`x2t_confirm.py`).
- Sweep sub-lemmas (comb-repack, D-sweep, turnarounds): `[PROVEN]` by 2-transition/length induction.
- E meets only `{1, even}`, never 3; opened cascade gaps counter-dependent (same block-pair → many
  even lengths): `[OBSERVED, exact, 0 counterexamples]` (`x2t_gen.py`, `x2t_evengap.py`, `x2t_confirm.py`).
- No conserved parity; no radius-≤8 local certificate: `[PROVEN]` (`x2c_phase.py`, `x2c_closure.py`).
- The even-gap safety invariant (the whole decision): **NOT proven; not used as a machine claim.**
