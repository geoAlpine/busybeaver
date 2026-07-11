# The integer-×2 base-2 odometer — INDEPENDENT arithmetic-reduction cross-check (2026-07-11)

*Independent (arithmetic-route) cross-check of the non-halting question for
`M = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`, the cleanest integer-×2 frontier machine.
A different route than the tape-template proof (which a parallel agent runs), so the two
cross-validate. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact
bytearray/int. Scripts `x2a_odometer.py`, `x2a_eraser.py` (+ prior `x2_*`, `x2c_*`). Builds on
`X2_DECIDABILITY_2026-07-10.md`, `X2_CLOSURE_2026-07-10.md`, `lean/Suffix.lean`. SOUNDNESS:
`[PROVEN]` = exact enumeration / proven Lean lemma; `[OBSERVED]` = measured, exact, no
generality claimed. ZERO false proofs. Not committed.*

## 0. Verdict (headline)

**NO certified decision — but the arithmetic route CONVERGES on the exact same open core as
the tape-template route, and supplies the arithmetic REASON the halt gate is (empirically)
never armed.** The reduction is airtight down to one lemma; that lemma is a head-phase
statement, not a bit-property of the odometer value, so the machine is `[DECIDABLE-class;
non-halt to ≥10⁸ steps; NOT certified-decided]`.

The task's central bet — *"×2 is a clean binary shift, so the halt-arming bit-pattern of the
closed-form value `vₙ` either always or never appears, decidably"* — is **REFUTED, and the
refutation is the interesting content**: the halt does **not** live in the bits of `vₙ`. It
lives in the *carry/gap dynamics* and the *head phase*, which the clean shift does **not**
make predictable.

## 1. Exact arithmetic reduction — the milestone form `[PROVEN structure / OBSERVED stream]`

The natural milestone (the analogue of o4's `M(G,a)` in `lean/Suffix.lean`) is: **head in
state `E`, reading `0`, strictly left of every `1` on the tape** — the `A1D0` eraser has just
finished and the head sits at the left frontier about to sweep right. At every such milestone
the tape is exactly

```
        0^∞  [E] 0^G  1^b  0^2 1^(2^k−3) 0^2 … 0^2 1^5 0^2 1 0  0^∞
              └gap┘ └lead┘ └────── settled cascade tail ──────┘
```

with `G` the **leading gap** and `1^b` the leading block. The rightward `E`-scanner
immediately reads the *left end of the maximal `0`-run `0^G`*. By the **PROVEN halt gate**
(`X2_CLOSURE §1`, forced chain `E→F→A→B`, all rightward reads: `HALT ⟺ E meets a maximal gap
of length EXACTLY 3`, positive/negative control `x2_control.py`, `L=1..6 ⟹ halt iff L=3`),

> **HALT ⟺ `G = 3`** (at this milestone, or at any interior `E`-meet).

This is the exact arithmetic halt condition: *the arming event is `met-gap = 3`.*

**The base-2 doubling engine `[PROVEN]`.** The super-blocks are `b = 2^k − 3`, obeying
`b′ = 2b + 3` (closed form, algebraic identity, all `k`); the leading-block `maxrun`
super-peaks are `2^k − 2`, obeying `v′ = 2v + 2` (closed form `vₖ = 2^k − 2`). Both verified
exactly (`x2_reset.py`: peaks `6,14,30,62,126,254,510,1022,2046,4094`; `x2a_odometer.py`:
blocks `5,13,29,61,253`). The doubling is the phase-locked comb-repack sweep `E:0→1RF,
F:1→1RE` over `(01)^k → 1^{2k}` (`[PROVEN]` by 2-transition induction, `X2_CLOSURE §2`;
Lean `sweepBF/sweepDE`). This is a **clean binary shift**: `vₖ = 2^k − 2 = 111…10₂` — no bit
mixing, the exact structural opposite of o7/Space-Needle (`⌊m/2^{v+1}⌋` mixes all bits).

## 2. The halt condition is never met — and WHY (the arithmetic parity) `[PROVEN reason / OBSERVED to ≥10⁸]`

`x2a_odometer.py` extracts the exact milestone stream. Over `[0, 4·10⁷]` (48 milestones):

```
leading-gap G histogram:  G=1:8   G=2:17   G=4:15   G=8:1   G=12:1   G=18:1   G=22:4   G=26:1
G == 3 ever armed?  NO.       any odd G ≥ 3 ever met?  NO.
first 48 G:  2,4,1,2, 8,4,2, 12,4,2,1,2, 18,4,2,4,1,2, 26,4,2,4,1,2, 22,4,2,4,1,2, 22,…
```

The leading-gap stream is verified `G ∈ {1}∪{even}`, never 3, to **10⁸ steps** (54
milestones, `x2a_odometer.py`, exact, 0 counterexamples). Interior (transient) `E`-meets
agree: `x2c_ctxrule.py` (every `E`-met gap `≥2` even, 0 odd) and `X2_CLOSURE §3` /
`x2c_probe.py` (full `E`-meet histogram to `2·10⁷`: lengths `{1,2,4,6,8,10,14,18,22,26}`, `0`
odd, `0` of length 3). **The gate is never armed on the observed orbit.**

**The arithmetic reason the met gaps are even (this is the new content):** every gap the
`E`-scanner meets is opened one of exactly two ways —

- **(a) comb separator:** inside a live comb `(01)^k` the sweep sits at single `0`s ⟹ `G = 1`;
- **(b) eraser gap:** the leading gap is *opened by the `A1D0` eraser* (2-cycle `A:1→0LD,
  D:0→0LA`). Lean **`sweepAD` PROVES** `(01)^j → 0^{2j}`: the eraser zeros an **EVEN** number
  of cells. `x2a_eraser.py` re-derives the parity independently (isolated combs `j=1..40`,
  every opened gap even). So **every eraser-opened gap has even length**.

Both channels give `G ∈ {1} ∪ {even}` — **never 3**. This is a genuine arithmetic mechanism,
proven at the local level (`sweepAD` even; comb separators unit).

## 3. The reset structure — it does NOT couple to deep bits (but see §4) `[OBSERVED]`

The task's "resets to 9/21/31" is a **coarse observable** (the max 1-run length between
super-peaks; `x2_reset.py` gives `6,11,29,14,31,9,21,9,21…`, irregular). It is **not** the
odometer state. The true state is the full nested cascade; its **leading gap `G` is the active
low-digit carry**, and the **settled tail has all gaps `= 0^2`** (even, fixed) — the tail
never contributes an odd gap. The reset value is thus a red herring: it does not gate the
halt, and the resets keep every *rest* gap in `{1,2}` (`X2_DECIDABILITY §2`, `[OBSERVED
exact]`). The finite-state block routing (parity-only, `X2_DECIDABILITY §3`, `[PROVEN-from-
table]`) is the reason the *control* carries only bounded information — genuinely unlike the
`(K)`/×p/q wall. So on every axis the machine is decidable-*class*.

## 4. The exact arithmetic gap — the task's bet, refuted precisely `[PROVEN obstruction]`

The bet was: if `vₙ` has a clean closed form, its binary is a clean shift, so a fixed
halt-arming bit-pattern is decidable. **Two facts kill it:**

1. **The halt pattern is absent from the value yet dense on the tape.** `vₖ = 2^k−2 =
   111…10₂` contains no `000` at all — a naive "does `vₙ` contain `0001`" test says *never
   halt* trivially, but that test is simply **not the halt condition**. Meanwhile gap-`3`
   (`0001`) is **dense on the actual tape** — present at `≈2.4 %` of steps (`x2c_census.py`,
   `[OBSERVED exact]`). The odd gaps `3,5,7,…` form **transiently**: while the eraser zeros a
   block it passes through `0^1, 0^2, 0^3, …, 0^{2j}`, momentarily creating odd gaps.

2. **Halt is avoided by head PHASE, not by the value.** The `E`-scanner meets a gap only
   *after* the eraser has finished it at even length `2j`, or as a comb unit `1` — **never
   mid-erasure at odd length**, because when the odd transient exists the head is the eraser
   itself (states `A/D`, which do not halt), not `E`. This is the head-phase coupling.
   `X2_CLOSURE §4` **PROVES** the consequence: no bounded-radius local head-window closure
   certifies non-halt (halt window reachable at every radius `≤ 8`), and `X2_CLOSURE §4b`
   shows **no global mod-2 parity is conserved** (7 candidates all split 50/50). So the
   even-gap property is **not** a static bit-invariant of `vₙ`.

**Therefore the clean-shift bit test does NOT decide the gate.** The clean ×2 shift makes the
*value* `vₙ` exactly predictable, but the halt lives in the *carry/gap structure and the
head's phase relative to it*, which the shift does not linearise. This is the honest failure
mode the task anticipated ("the halt condition depends on a … property [that is] not as clean
as hoped").

**What remains to close (the one lemma):** *the `E`-scanner never scans a half-erased odd
gap* — equivalently *every `E`-met gap is `1` or even (`sweepAD`-produced)*. The two local
channels of §2 are proven; the missing step is the **global structural invariant** that the
tape is, at every `E`-meet, in "comb + finished-eraser-gap" form (no third gap type, correct
phase). This is a **packed-macro reachability** statement over the parity-routed finite-state
control — decidable in principle, `[OBSERVED, 0 counterexamples to 10⁸ steps]`, but not
formally closed here. **It is exactly the open core the tape-template route also leaves**
(`X2_CLOSURE §6`: "`E` never arrives at a length-3 gap"). The two routes AGREE.

## 5. Soundness ledger
- Milestone form + `HALT ⟺ met-gap = 3`: `[PROVEN]` (`X2_CLOSURE §1`, `x2_control.py`).
- Doubling closed forms `b=2^k−3` / `v=2^k−2`: `[PROVEN]` (algebra + `sweepBF/DE`; `x2_reset.py`).
- Eraser opens even gaps `(01)^j→0^{2j}`: `[PROVEN]` (Lean `sweepAD`; parity re-derived
  `x2a_eraser.py`).
- leading-gap `G ∈ {1}∪{even}`, never 3: `[OBSERVED, exact, 0 c.ex. to 10⁸ steps]`
  (`x2a_odometer.py`); every interior `E`-met gap even, never 3: `[OBSERVED, exact, to 2·10⁷]`
  (`X2_CLOSURE §3`, `x2c_probe.py`, `x2c_ctxrule.py`).
- Gap-3 dense on tape (~2.4 %); no global parity conserved; no radius-≤8 local certificate:
  `[PROVEN/OBSERVED]` (`x2c_census.py`, `x2c_phase.py`, `x2c_closure.py`).
- The global even-gap invariant (the one lemma): **NOT proven; not used as a machine claim.**

**No machine decided. No label upgraded.** Cross-checkable with the tape-template route:
both reduce non-halt to the identical head-phase lemma "`E` never meets a length-3 gap".

---
**CORRECTION (2026-07-11, per lean/X2.lean audit, commit 7760aa5):** the "A1D0 eraser `A:1→0LD, D:0→0LA` giving
`(01)^j → 0^{2j}`, PROVEN via Lean `sweepAD`" cited above is a MISATTRIBUTION to o4's machine. The x2 machine has
`A:1→0RE` and `D:0→0RE` (both move RIGHT); it has NO clean cell-zeroing eraser sweep. The genuine clean even channel is
the comb-repack `(01)^m → 1^{2m}` (Lean-proven in `lean/X2.lean` `sweepEF_even`). The eraser-opened-gap even-ness is
[OBSERVED], not proven via a clean sweep. See `X2_STATUS_2026-07-11.md` and commit 7760aa5.
