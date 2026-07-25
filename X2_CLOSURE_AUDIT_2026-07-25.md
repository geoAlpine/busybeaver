# x2 — closure and audit record (2026-07-25)

Machine `x2 = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`, blank tape.

**LABEL HELD.** This file records the proof and the audit. The label is NOT upgraded here; it is
upgraded only after the cold full build and the red-team both pass, and only by explicit decision.

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

## Outstanding

* **Cold full build from scratch** — running.  Until it passes, the result is not audited.
* Whether `x2` is among the community's current open holdouts is **unverified** (it was drawn from
  the historical 1104-holdout frontier, and its spec is not in `catalogue_finish.py`'s named list).
  That question does not affect the theorem; it affects only what the theorem is worth externally.

**No label upgraded in this file.**
