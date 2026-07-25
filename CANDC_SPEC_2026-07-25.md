# Deciding `C` = `x2` from state `B` — the exact specification (2026-07-25)

`C = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` is `x2`'s transition graph started in `x2`'s
state `B` (verified: `σ(x2) = C` on all six rows, `σ : A→F, B→A, C→B, D→C, E→D, F→E`).

So **`C` never halts ⟺ `x2`'s own `step` never halts from `⟨B, 0, blank⟩`** — one statement about
the machine `x2` is already fully developed for.  This file pins the milestone family that
statement needs.

## The `B`-orbit milestone family (MEASURED in Lean)

`#eval` of `steps n ⟨.B, 0, ⟨[],false,[]⟩⟩`, at the milestone times `+1`:

| `n` | state | pos | `|left|` | right-tape RLE prefix |
|---:|---|---:|---:|---|
| 14 563 | E | −15 | 1 | `0^17 1^125 0^2 1^61 0^2 1^29 0^2 1^13` |
| 49 470 | E | −18 | 1 | `0^3 1 0 1 0 1 0 1 …` |
| 192 509 | E | −21 | 1 | `0^25 1^509 0^2 1^253 0^2 1^125 0^2 1^61` |
| 727 067 | E | −27 | 1 | `0^21 uUnits 0  (1 :: 0^4  ++ pow10 6 ++ …)` |
| 2 866 581 | E | −33 | 1 | `0^21 uUnits 1  (1 :: 0^10 ++ ones 2045 ++ m1casc …)` |
| 11 302 995 | E | −39 | 1 | `0^21 uUnits 2  (1 :: 0^4  ++ pow10 6 ++ …)` |

* state `E`, `|left| = 1`, head position stepping by a uniform `−6` — **the same milestone shape as
  the `A`-orbit's `M1`**;
* the descending blocks are `2^k − 3` throughout — `m1casc`, as for `x2`.

## The index relation — this is the whole content

The `A`-orbit family, as defined in `T7OddBridge`:

    MEven h : uUnits (2h+1),  ones (2^(2h+10) − 3)
    MOdd  h : uUnits (2h+2)

The `B`-orbit shows `uUnits 1` paired with `ones 2045 = 2^11 − 3`, whereas `MEven 0` pairs
`uUnits 1` with `ones (2^10 − 3) = 1021`.  So:

> **The `B`-orbit family is NOT `MEven h` / `MOdd h` for any `h`.**  It is the parallel family with
> the `(uUnits count, block index)` pairing shifted by one:
>
>     MEven' h : uUnits (2h+1),  ones (2^(2h+11) − 3)     -- one power higher
>     MOdd'  h : uUnits (2h)                              -- one uUnits lower

## Why this is a re-instantiation, not a re-proof

Every ingredient of the `x2` phase assembly is `∀` in exactly these indices:

* `h_low_even_core k TAIL`, `h_low_odd_core k FRAME` — `∀k`, `∀`tail;
* the descent `descLaw`/`headLaw`, the ladder `ladderToCascade`, the rung `topRung`/`RegenLawGen`,
  the tail `frameFold`/`tailLaw` — all `∀k`, `∀`marker;
* `TapeCalc` — machine-independent, so untouched;
* `chainE` / `nonhalt_of_invariant` — `∀` in the family.

What changes is the index ARITHMETIC that glues them (`2h+1` vs `2h`, `2^(2h+10)` vs `2^(2h+11)`),
and with it **which phase plays the "even" role** — the parity swaps.  That is real work, but it is
bounded, and none of it is new dynamics.

## Checklist for the `C` derivation

1. define `MEven'` / `MOdd'` and re-derive `hlowDoubEven'` / `hlowDoubOdd'` at the shifted indices;
2. re-derive the two seam identities (`evenOut_is_oddIn`, `oddOut_is_evenIn`) with the shifted
   `uUnits` count — the `uUnits_frameZ` collapse itself is index-free and reused verbatim;
3. `cycleEven'` / `cycleOdd'`, then `chainE'` (identical shape);
4. entry segment `⟨B, 0, blank⟩ → M1'(…)` by chunked `rfl` (the `B`-orbit reaches its 4th milestone
   at 727 067 steps, cheaper than `x2`'s 732 733);
5. `x2_nonhalt_of_entry`-style assembly, then translate to `C` by the state relabelling `σ`.

**No machine decided beyond `x2`.  No label upgraded.  Push HELD.**
