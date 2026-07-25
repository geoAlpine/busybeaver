# x2 — closure and audit record (2026-07-25)

Machine `x2 = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`, blank tape.

**AUDIT COMPLETE — PASSED.** Cold full build from scratch: **63/63, `sorryAx` 0,
`Classical.choice` 0**, `T7Entry` rebuilt in 570 s.  `#print axioms x2_nonhalt_blank` =
`[propext, Quot.sound]` — none of the 11 custom `axiom` declarations in `Completion.lean` is in
its dependency cone.

> ### `x2` DOES NOT HALT FROM THE BLANK TAPE.  [PROVEN]
> Machine-checked, unconditional, Mathlib-free.

## The theorem

    x2_nonhalt_blank : ∀ N : Nat, steps N init ≠ none        [propext, Quot.sound]

## The chain (every link machine-checked)

| link | theorem | axioms |
|---|---|---|
| entry, `init → M1(2)`, 732 733 steps in 8 kernel-`rfl` chunks | `entryM12` | `[propext, Quot.sound]` |
| the canonical milestone word is the reached tape + blanks | `hsplitM12` | **axiom-free** |
| depth-`d` chain of `2d` milestone cycles, cost `≥ d`, `∀h` | `chainE` | `[propext, Quot.sound]` |
| the depth-`d` tail is ONE block of blanks | `tailE_zeros` | `[propext, Quot.sound]` |
| reverse right-boundary congruence | `steps_runpad_zeros` | `[propext]` |
| the even / odd milestone cycles | `cycleEven` / `cycleOdd` | `[propext, Quot.sound]` |
| obligation H, both parities | `hlowDoubEven` / `hlowDoubOdd` | `[propext, Quot.sound]` |
| both doubling phases | `doubPhaseEvenL` / `doubPhaseOdd` | `[propext, Quot.sound]` |

## Instrument audit (all clean)

    step table read back cell by cell : 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE
    x2 spec                           : 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE
    init                              : (A, 0, [], false, [])   -- state A, pos 0, blank tape
    halting transitions               : [(B, true)] only        -- exactly the `---` field
    halt reachable, none propagates   : steps 1 and steps 400 from (B reading 1) are `none`

The last line matters: `≠ none` is a genuine non-halting claim, not a statement about a `step`
function that can never return `none`.

## Anti-vacuity (M4) — the family is ON THE ORBIT

| check | expected (MEASURED) | Lean |
|---|---|---|
| M1(2) → M1(3) span | 2 119 358 | `hlowDoubEven_cost0`, axiom-free |
| M1(3) → M1(4) span | 8 477 210 | `hlowDoubOdd_cost0`, axiom-free |
| milestone translation | −6 per milestone (`M1(2)@−31`, `M1(3)@−37`, `M1(4)@−43`) | `cycle_q_h0`, axiom-free; `#eval` −6 at `h = 0,1,2` |
| `(MEven 0 []).right` vs the real M1(2) right tape | prefix match, remainder all zeros | `x2h_orbit_match.py`: TRUE, 2057 zeros |
| right-frontier advance | `2^11`, `2^12` | `x2h_frontier.py` |

## Red-team

* `chainE` has **no hypotheses** — it cannot be a vacuous implication; `steps n C = some C'` is a
  positive fact about the machine.
* `steps_runpad_zeros` is used in the correct direction: proven WITH pads ⟹ holds on the trimmed
  tape, and `e8` (the actual reached config) is the trimmed side.
* It uses the RIGHT bisimulation `steps_crtail`, not the left one.
* The family is connected to the actual orbit by `hsplitM12` (**axiom-free** `rfl`) and `entryM12`
  (kernel `rfl` from `init`) — machine-checked, not asserted.
* Independent simulator: x2 has been run to 11 329 301 steps with no halt, and the Lean and Python
  instruments agree on every anchor (`check_anchors`).

## Cross-instrument check (Lean vs the Python simulator)

| step | Lean `#eval` | simulator |
|---|---|---|
| 732 733 | `(E, −31)` | `(E, −31)`, right frontier 2073 |
| 2 852 091 | `(E, −37)` | `(E, −37)`, right frontier 4127 |
| 11 329 301 | `(E, −43)`, left 1, right 8229 | `(E, −43)`, right frontier 8229 |

Exact agreement at three independent large step counts.

## What this decides, precisely

`Completion.lean` states the BB(6) obligation as **1104 holdouts = 17 named cryptids + 1087
residual**, with the residual carried as the axiom `holdouts1087_nonhalt` and the note: *"our
certified suite is a subset of the community decider class (0/300 decided), so this is not
internally reducible to the named 17."*

`x2` is **not** one of the 17 named cryptids (its spec is absent from `catalogue_finish.py`'s named
list).  **VERIFIED (2026-07-25) by the novelty oracle `bb6_holdouts.py`**, which matches up to TNF
plus left–right reversal against `_bbdata/bb6_holdouts_1104.txt` (April 2026, 1104 canonical
classes):

    x2 canonical = 1LB0LC_1LD---_1LE0RD_0RF1RC_0LA1LC_0LC1RF
    is_holdout(x2) = True

(all 18 named cryptids also return `True`, so the oracle is not vacuously accepting).  So:

> **This decides one member of the 1087 residual block — the first, unconditionally, in Lean.**

**Caveat kept explicit:** the 1104 list is the curated April-2026 snapshot; newer/larger community
lists exist.  Membership is asserted against that snapshot, nothing more, and no external claim is
made.

It does not decide any of the 17 named cryptids, and it does not touch `(K)`.  What it does is
convert the template method from a design into a **worked, audited end-to-end example**, and it is
direct evidence for the analysis in `ANALYSIS_2026-07-25.md` §III: the residual block is where the
template island lives.

**LABEL UPGRADED: `x2` = [PROVEN non-halting].**  Audit of record: this file.
