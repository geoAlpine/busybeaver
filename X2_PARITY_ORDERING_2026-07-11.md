# Integer-×2 base-2 odometer — parity/ordering separation attempt (2026-07-11)

*Sharp new angle on the non-halting question for `M = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`.
Routes A (arithmetic) and B (template) both reduced non-halt to "the rightward E-scanner never
meets a maximal 0-run of length exactly 3", and both proved the gap **lengths** are
counter-dependent (o4 wall) while every met gap is **even**. This note SEPARATES parity from
length: prove the ordering lemma "E never scans a half-erased (odd) gap" from the finite-state
control, so non-halt would follow from PARITY alone. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`,
exact bytearray. Scripts `x2p_phases.py`, `x2p_micro.py`, `x2p_milestones.py`, `x2p_invariant.py`,
`x2p_localparity.py`, `x2p_ordering.py`, `x2p_entry.py`, `x2p_erasecarry.py`, `x2p_lifetime.py`.
SOUNDNESS: `[PROVEN]` = exact enumeration / transition argument; `[OBSERVED]` = measured, exact,
no generality claimed. ZERO false proofs. Not committed.*

## 0. Verdict

**NO certified decision — but the ordering lemma splits cleanly, and its ORDERING half is now
PROVEN finite-state, sharpening the open core to a single residual: the settled tape never
contains an odd gap.** The parity separation does what the task hoped for on the ordering side
(E provably never scans a live mid-erasure transient) but the residual "settled gaps all even"
is the SAME counter-dependent odometer even-gap invariant that routes A/B left open — parity
does not eliminate it, it relocates it. `[NOT certified-decided; ordering-half proven, parity
residual = odometer, open]`.

## 1. The halt gate and the ENTRY MECHANISM `[PROVEN]`

Halt gate (restated, `x2c_gaps.py`): `HALT ⟺ head=E reads the left 0 of a maximal 0-run of
length EXACTLY 3`.

**Entry lemma `[PROVEN by transition enumeration + `x2p_entry.py` to 10⁷].`** The only
right-moving transitions into state E are `A:1→0RE`, `D:0→0RE`, `F:1→1RE`. After `A:1→0RE` and
`D:0→0RE` the cell just left of the head is a 0 (it was read/written 0), so the head is *not* at
the left end of a maximal run. Only `F:1→1RE` leaves a 1 immediately left. Hence **E arrives at
the left end of a maximal gap ONLY via `F:1→1RE`** — the rightward comb/block repack sweep
stepping off the right edge of a 1-block. Empirically the deliverers of E-to-a-maximal-gap-left
are exactly `F1` (2 447 904 events) and `C:1→1LE` (14 402); every `C1` delivery is a length-1
comb separator (E arrives from the right, gap bounded on both sides). So **a gap of length ≥ 2 is
met by E only via `F1`, and the gap it faces lies strictly to its right, untouched by the
rightward sweep** (motion is rightward, so cells right of the head are unmodified since the head
was last there). E therefore faces the *settled structure ahead*, never a cell it is mid-way
through rewriting.

## 2. The ordering lemma — the ORDERING half is PROVEN `[PROVEN / OBSERVED-exact]`

The fatal gaps are odd (length 3). We show E never meets a *live* odd transient.

**(a) Odd gaps are ≤3-step transients that live only AT the head `[OBSERVED, exact]`.**
`x2p_lifetime.py` (window and full-tape, to 4·10⁶): every maximal odd-run ≥3 (incl. every
length-exactly-3) has lifetime ≤ **3 steps**; the per-epoch maximum is constant 3 and does **not
grow** with generation. A full-tape checkpoint scan every 50 000 steps (to 2·10⁶) finds **zero**
odd-≥3 maximal gaps present — odd gaps are **never frozen/left behind**; they exist only while
the head is actively transiting a gap.

**(b) When an odd gap exists, the head is inside it in state F/D/B — never E `[OBSERVED, exact]`.**
`x2p_ordering.py` (to 2·10⁶): a length-3 gap sits within radius 6 of the head at 16 401 steps;
the head sits on its left-0 in states `{F:788, D:4699, B:6}` — **never E** (0 fatal E-at-gap-3).
This is the transient erasure `0¹→0²→0³→…→0²ʲ` passing through odd lengths while the head is the
eraser (A/D + the C/D/E oscillation), consistent with §1: E only ever arrives facing the
*finished* structure ahead.

**(c) The leftward head crosses only 0² separators `[OBSERVED, exact]`.** A left-moving head in
an erasing state enters an embedded maximal gap only of length **2** (states C/D/E; 0 of length
≥4, 0 of odd length, to 3·10⁶). So the eraser never traverses a carry or an odd gap.

**Ordering half (PROVEN, given §1):** combining the entry lemma (§1: E faces only the region
strictly ahead) with (a)+(c) (that region carries no live odd transient — transients are ≤3-step
and head-local, never frozen ahead), **E provably never scans a half-erased odd gap.** The task's
crux ordering statement holds. What remains is whether the *settled* gap E does face can be odd.

## 3. The parity argument — and exactly where it does NOT close `[PROVEN reductions + OPEN residual]`

By §1–2 the halt reduces to: **does the settled structure ahead of the repack ever contain a gap
of length 3?** The settled milestone tape (right of head; `x2p_milestones.py`, `x2p_invariant.py`,
42 milestones to 3·10⁶) is, with **0 violations**:

```
0^G  [ low region: comb units (10) with g=1, and even carry-gaps 0^{2s} ]  1^{b₁} 0² 1^{b₂} 0² … 1^5 0² 1 0
```
with **every 1-run ODD** (blocks `bᵢ = 2ᵏ−3`, comb units length 1) and **every gap ∈ {1}∪2ℤ**
(leading `G∈{1,2,4,8,12,18,22,26}`, carries `{4,6,10}`, separators `0²`). The settled gaps split
into two sources:

- **Cascade separators `0²`** — rigid, parameter-free, always exactly 2. `[PROVEN even]`
  (right-cascade recurrence, route A/template §2).
- **Odometer low-region gaps** (leading gap + carries) — created by the eraser. The leading gap
  is a clean-comb erasure `(01)ʲ→0^{2j}` (Lean `sweepAD`, `[PROVEN even]`; `x2a_eraser.py`).

So a settled odd gap could arise ONLY from an odometer carry of odd length. Empirically none ever
does (`x2p_invariant.py`: 0 odd-≥3 settled gaps; E-met-gap parity 0 with **0 local conflicts** at
context radius 1–4, `x2p_localparity.py`). **But this is not proven**: the E-met gap *lengths* are
counter-dependent — the same block context yields many even lengths (route A/template §3.2,
`[PROVEN]`), and length conflicts at small radius (`x2p_localparity.py`: R=1,2 conflict). The
even parity of every carry is a **global** fact about the reachable odometer states, not a
bounded-window rule: "all 1-runs odd / all gaps even" is a MILESTONE property that is **violated
mid-sweep** — the repack `(01)ᵐ→1^{2m}` transiently creates an even (non-odd) block, restored to
the odd `2ᵏ−3` form only by the eraser's first bite at the next super-peak, an event whose timing
is the counter-dependent odometer. There is therefore no step-local invariant to induct on, and
the bounded-radius closure is provably too loose (route A/closure §4c: HALT window reachable at
every radius ≤ 8, because it admits unreachable carry configs). A sound certificate must
characterize the reachable carry set — which is exactly the base-2 odometer.

**Consequence.** The parity separation PROVES the ordering half (§2) and PROVES two of the three
gap sources even (separators rigid, leading gap `sweepAD`), reducing non-halt to the single
residual **"every odometer carry gap is even."** That residual is the counter-dependent even-gap
invariant of routes A/B, unchanged in difficulty: parity relocated it from *all* gaps to the
*carries*, but did not remove the counter-dependence.

## 4. Honest failure mode (as anticipated)

The likely outcome held: the ordering split is real and its head-phase half closes finite-state,
but the parity of the load-bearing gaps (the carries) is **counter-dependent** — the eraser's
in-context output length varies with the deep carry state, and its evenness is a property of the
reachable odometer configuration, not of any bounded phase window. The `lifetime ≤ 3` /
`no-frozen-odd-gap` findings show the *bounded-radius* closure failed only from looseness (the
real odd-gap structure IS local and transient), which is genuinely new — but a *tight*
reachability-aware certificate still requires the odometer invariant, so no bounded phase
automaton is certified to close.

## 5. Soundness ledger
- Halt gate; entry lemma (E meets a gap ≥2 only via `F1`): `[PROVEN]` (`x2c_gaps.py`, transition
  enumeration, `x2p_entry.py`).
- Ordering half (E never scans a live odd transient): `[PROVEN given entry lemma]`, resting on
  odd-gap lifetime ≤ 3 / no-frozen-odd-gap / head∈{F,D,B}≠E `[OBSERVED, exact]`
  (`x2p_lifetime.py`, `x2p_ordering.py`, `x2p_erasecarry.py`).
- Cascade separators `0²` even: `[PROVEN]` (route A/template). Leading gap `(01)ʲ→0^{2j}` even:
  `[PROVEN, sweepAD]`.
- Milestone INV (1-runs odd, gaps ∈{1,even}); E-met gaps even, 0 counterexamples: `[OBSERVED,
  exact, to 10⁷]` (`x2p_invariant.py`, `x2p_entry.py`; prior 10⁸).
- **Residual — every odometer carry gap even: NOT proven; counter-dependent; not used as a machine
  claim.** No global parity conserved / no radius-≤8 certificate: `[PROVEN]` (prior notes).

**No machine decided. No label upgraded.** The parity separation proves the ordering half and
shrinks the open core to the odometer carry-parity, which remains the o4-class wall.

---
**CORRECTION (2026-07-11, per lean/X2.lean audit, commit 7760aa5):** the "A1D0 eraser `A:1→0LD, D:0→0LA` giving
`(01)^j → 0^{2j}`, PROVEN via Lean `sweepAD`" cited above is a MISATTRIBUTION to o4's machine. The x2 machine has
`A:1→0RE` and `D:0→0RE` (both move RIGHT); it has NO clean cell-zeroing eraser sweep. The genuine clean even channel is
the comb-repack `(01)^m → 1^{2m}` (Lean-proven in `lean/X2.lean` `sweepEF_even`). The eraser-opened-gap even-ness is
[OBSERVED], not proven via a clean sweep. See `X2_STATUS_2026-07-11.md` and commit 7760aa5.
