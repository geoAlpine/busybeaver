# `C` — closure and audit record (2026-07-26)

Machine `C = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD`, blank tape.
A member of the 1104-holdout residual, found by the pre-flight screen.

**LABEL HELD until the cold build passes.**

## The theorem

    CIso.C_machine_nonhalt : ∀ N : Nat, stepsC N ⟨.A, 0, ⟨[], false, []⟩⟩ ≠ none
                                                              [propext, Quot.sound]

## The route — and why it was cheap

`C` is `x2`'s transition graph with the states cyclically renamed
(`σ : A→F, B→A, C→B, D→C, E→D, F→E`).  So `C` never halts from the blank tape **iff** `x2`'s own
`step` never halts from `⟨B, 0, blank⟩`, and the whole `x2` development applies to that orbit.

| link | theorem | axioms |
|---|---|---|
| both low phases apply VERBATIM (`∀TAIL` / `∀FRAME`) | `hlowB_core`, `hlowBodd_core` | `[propext, Quot.sound]` |
| both doubling-phase entries, re-instantiating `p1tLL`, `rUnitsFold`, `bridge`, `crossCarry`, `odTurn`, `eChewFold` | `topEntryB`, `topEntryOddB` | `[propext, Quot.sound]` |
| both doubling phases, reusing `x2`'s OWN `evenSpine` / `oddSpineFull` at `n = 2h+6` | `doubPhaseB`, `doubPhaseOddB` | `[propext, Quot.sound]` |
| both seams and both frame identities | `evenSeamB_oddInB`, `oddSeamB_evenInB`, `evenOutB_is_oddInB`, `oddOutB_is_evenInB` | `[propext, Quot.sound]` |
| obligation H, both parities | `hlowDoubB`, `hlowDoubOddB` | `[propext, Quot.sound]` |
| the two cycles and the depth-`d` chain | `cycleBEven`, `cycleBOdd`, `chainB` | `[propext, Quot.sound]` |
| non-halting from one entry hypothesis | `C_nonhalt_of_entry` | `[propext, Quot.sound]` |
| the entry segment, 2 866 581 steps in 29 kernel-`rfl` chunks | `entryB` | `[propext, Quot.sound]` |
| the milestone-word split | `hsplitB` | **axiom-free** |
| **the state-relabelling isomorphism** | `stepC_rl`, `stepsC_rl` | **axiom-free** |

> **New dynamics required for the second machine: ZERO.**  Every lemma was applied verbatim or
> re-instantiated at shifted indices, because `x2`'s development is parametric in exactly the
> indices that differ.

## Instrument audit — clean

    table read back cell by cell : 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD
    C's spec                     : 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD
    halting transitions          : [(A, true)] only — exactly the `---` field
    halt reachable, none propagates : stepsC 1 and stepsC 400 from (A reading 1) are `none`
    cross-instrument (Lean `stepsC` vs the Python milestones):
        49 469   → (C, −19, left 0, right 522)
        192 508  → (C, −22, left 0, right 1037)
        727 066  → (C, −28, left 0, right 2067)
        2 866 580 → (C, −34, left 0, right 4121)
      exactly the measured values

## Anti-vacuity — the family IS the orbit

`#eval` with decidable equality on `Cfg`, all four TRUE:

    steps 2866581  ⟨B,0,blank⟩ == ⟨E,−33,⟨zeros 1, false, (MEvenB 0 (zeros 1)).right⟩⟩
    steps 45042285 ⟨B,0,blank⟩ == ⟨E,−45,⟨zeros 1, false, (MEvenB 1 (zeros 1)).right⟩⟩
    steps 727067   ⟨B,0,blank⟩ == ⟨E,−27,⟨zeros 1, false, (MOddB  0 (zeros 1)).right⟩⟩
    steps 11302995 ⟨B,0,blank⟩ == ⟨E,−39,⟨zeros 1, false, (MOddB  1 (zeros 1)).right⟩⟩

and `hsplitB` (axiom-free `rfl`) certifies the entry landing.

## Outstanding

* **Cold full build from scratch** — running.  Until it passes, the result is not audited.

**No label upgraded in this file.**
