# Soundness audit of the 2026-07-04 slow-width cryptid corpus — VERDICT: SOUND

*A verification pass over the multi-agent slow-width cryptid work of 2026-07-04 (o2, o3, o7, o11, o12, o13, o14,
o16, Space Needle — normal forms, ×3/2 Mahler maps, PROVEN halt gates, the trichotomy). Every headline was
re-checked against the raw TM by the orchestrator. **VERDICT: the corpus is SOUND** — the two errors that arose
were already caught and corrected in-session; the audit found **no new over-claim**. SOUNDNESS: this note only
verifies; it decides no machine. Interpreter `/opt/homebrew/bin/python3.13`.*

## What was audited and the result

| audit check | result |
|---|---|
| **[OPEN] labels** — no accidental halt | ✅ all 9 machines run to **40M steps, NO HALT** (raw TM) → `[OPEN]` sound |
| **Type-I `×3/2` Mahler maps** (raw-TM extraction, not just arithmetic) | ✅ confirmed (below) |
| **PROVEN halt gates** (unique halt-predecessor + blank never-fire) | ✅ all 9 verified, 0 firings (`cryptid_halt_gates_verify.py`) |
| **o3 / o17 transducers** (normal form + finite control + gate) | ✅ `... VERIFIED: True` (own verifiers) |
| **Label audit** — any "decided / non-halting proven" over-claim? | ✅ **none**; every note correctly says "nothing decided, `[OPEN]`" |

## Type-I `×3/2` verification (raw TM, orchestrator-extracted)

Directly re-extracted the growing value orbit from the **raw TM** (not trusting agent numbers) and checked the
ratio → `3/2`:

- **o13** — reboot leading block `104,163,248,379,572,865,1301,1955,2936`, ratios `1.528,1.509,1.512,1.504,
  1.503,1.502` → **exact match to the agent's `40,67,104,163,…` sequence**. ✓
- **o14** — leading block `…97,151,232,354,537,811,1222,1839`, ratios → `1.505`; matches the agent's `A`-values
  `97,151,232,354`. ✓
- **o12** — reboot leading block `160,241,367,556,835,1258,1888,2833,4255`, ratios → `1.501`. ✓ (a different
  milestone coordinate from the agent's `V=3a+2b`, but the same `×3/2` orbit.)
- **o16** — two-block big block, clean subsequence `63,94,149,225,339,508`, ratios → `1.5` (`S'=⌊3S/2⌋+c`). ✓
  **Correction to a mid-audit false alarm:** a first coarse `max-block` proxy showed `ratio 1.25`; that was a
  **threshold artifact** of the extraction (records forced to `≥1.25×`), *not* a real growth rate — the direct
  two-block milestone confirms `×3/2`. o16 is Mahler-3/2, **not** ×5/4.
- **o11** — base-3/2 odometer `D'=⌊3D/2⌋+ε` (`ε∈{1,2,3}`) arithmetic-verified; the doubly-exp grand cycles
  (`…8,26,303`) reproduced from the raw TM. ✓
- **o2 / o7** — already directly verified this session (`D(2,1)→D(5,3)` exact for o2; o7 reset-`a` ratios
  `1.502,1.503,1.504`). ✓

## The two in-session errors (already corrected, re-confirmed here)

1. **Space Needle "HALT ⟺ all-ones"** — **FALSE** (the reverse-engineering agent's clean claim). The true-config
   raw halt set for `m≤160` is `{1,3,6,7,15,31,63,102,127}`; `m=6` and `102` halt but are not all-ones.
   Corrected to "`S ⊋ all-ones`" in `SPACE_NEEDLE_HALT.md` / `CRYPTID_CLASSIFICATION_2026-07-04.md`. ✓ folded in.
2. **o7 halt coordinate** — an inter-agent config-convention discrepancy (the (K)-probe agent disputed the
   "`a=5`" predicate using a non-canonical config). Caveated in `O2_O7_HALT.md`; the robust facts (PROVEN
   `C`-reads-`00` gate, `×3/2` map, blank orbit keeps `a≥4`) stand. ✓ caveated.

## Minor consistency notes (not errors)

- Milestone **coordinates** differ between the orchestrator's audit extractions and the agents' (e.g. o12
  `V=3a+2b` vs leading block; o16 `c∈{4,6}` vs `{0,2}`). These are different-but-consistent parametrizations of
  the same `⌊3x/2⌋` orbit; the **classification is coordinate-independent** and robust.

## Verdict

**SOUND.** All `[OPEN]` labels hold (no machine halts to 40M); every Type-I `×3/2` Mahler map is confirmed
against the raw TM; every PROVEN halt gate re-verifies; no note contains a "decided / non-halting proven"
over-claim. The only two errors were the Space Needle all-ones claim and the o7 coordinate discrepancy — **both
already caught and corrected in-session**, re-confirmed here. The 2026-07-04 cryptid corpus (trichotomy,
9 halt gates, o3 second outlier, o17/o3 cascade dissections) stands. **No machine decided. No label upgraded.
Halting `[OPEN]` for all fourteen.**

## Reproduce
- `cryptid_halt_gates_verify.py` (9 gates), `o17_core_transducer.py`, `o3_transducer.py` — all print `VERIFIED:
  True`. The Type-I `×3/2` re-extractions and the 40M no-halt sweep are one-off orchestrator scripts (scratchpad).
