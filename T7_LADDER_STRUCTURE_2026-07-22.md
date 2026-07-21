# T7's bulk is the alternating composition of TWO already-∀-proven transports (2026-07-22)

Third T7 document today, and the sharpest. `T7_RECON` found the doubling phase is a RegenLaw
ladder; `T7_GAPLAW` found the gaps obey `gap(k) = 4^k − 3·2^k + 7`. This document identifies **what
that gap law IS** and shows the whole ladder is a composition of theorems already in the
development.

## The finding

**`gap(k) = 4^k − 3·2^k + 7` is not a new fit — it is `topGrindSteps(k)`, an existing Lean
definition (`X2.lean:5291`), the step count of `braid_topgrind`.**

```lean
def topGrindSteps (a : Nat) : Nat := 2 ^ (2 * a) + 7 - 3 * 2 ^ a          -- = 4^a − 3·2^a + 7
theorem topGrindSteps_grounds : topGrindSteps 5 = 935 ∧ … 6 = 3911 ∧ … 7 = 16007
theorem braid_topgrind (N Lc : Nat) (p : Int) (marker casc : List Bool) :
    steps (7 + braidRunSteps 0 N + (4*N+4)) ⟨.E, p, ⟨…, ones (2*N+1) … ⟩⟩
      = some ⟨.E, p + 5 + 2*N, ⟨ones (4*N+4) ++ …⟩⟩         -- prepends the doubled top block
theorem topGrindSteps_split (a) (2 ≤ a) :                    -- ties the two together at N = 2^{a−1}−2
    topGrindSteps a = 7 + braidRunSteps 0 (2^{a−1}−2) + (4·(2^{a−1}−2)+4)
```

`braid_topgrind`, `topGrindSteps_split`, `regenLaw_closed` — all `[propext, Quot.sound]`,
re-verified today. `braid_topgrind` is **fully `∀ N Lc p marker casc`**.

So the doubling-phase ladder is:

```
regenIn k ──RegenLaw (exitSteps k)──▶ cascadeReg k ──braid_topgrind (topGrindSteps k)──▶ regenIn (k+1)
   └──────────────── proven ∀k (2026-07-21) ───────┘  └──────────── proven ∀N Lc (banked) ────────────┘
```

**Both rails of the ladder are already theorems.**

## The g=2 verification `[MEASURED — exact, config-level]`

The full g=2 ladder closes using ONLY the two proven step counts. Starting from the measured
`s₅ = 739 656` and iterating `s_{k+1} = s_k + exitSteps(k) + topGrindSteps(k)`:

| k | s_k (chain) | s_k (measured) |
|---|---|---|
| 6 | 740 809 | 740 809 ✓ |
| 7 | 745 442 | 745 442 ✓ |
| 8 | 763 979 | 763 979 ✓ |
| 9 | 838 036 | 838 036 ✓ |
| 10 | 1 133 853 | 1 133 853 ✓ |
| 11 | 2 315 814 | 2 315 814 ✓ |

Every rung start is reproduced to the step. And the gap episode is `braid_topgrind` **at the config
level**, not just by step count — verified for k=7:

- **gap IN** (step 747 972): state E, head 0, right `= 0³ 1¹²⁵ 0² 1⁶¹ …` = `cascadeReg 7`
  (`2^7−3 = 125`), which is exactly `braid_topgrind`'s IN shape `0³ 1^{2N+1} 0² casc`, `N = 61 =
  2^6−2`.
- **gap OUT** (step 763 979): state E, head 0, **left block `1²⁵³ = 1^{2^8−3}`**, right
  `= 0 1⁶¹ 0² 1²⁹ …` = `descCascade 4` — i.e. **exactly `regenIn 8`**. The gap built the level-8
  top block `1^{2^8−3}` from the level-7 cascade. **This is the `Θ(4^k)` top-block doubling in the
  flesh.**

## Why this matters — T7 is an ASSEMBLY, not new mathematics

This is the `RegenLaw ∀k` closure pattern repeating exactly. That crux closed because `trailFold`
was **banked long before anyone recognised it as the induction step**. Here the situation is even
better: **both** ingredient transports of the doubling phase are already proven `∀`:

- the RegenLaw rung: `regenLaw_closed` (∀k≥4, 2026-07-21);
- the topgrind rung: `braid_topgrind` (∀N Lc, banked — it was §3′'s predicted `Θ(4^k)` mechanism
  all along, just filed under the wrong obligation).

**T7's bulk needs no new transport.** What remains is genuinely three smaller things:
1. **the assembly** — a `∀k` induction composing `[RegenLaw(k) ∘ braid_topgrind(k)]` up the ladder
   for one generation (the same kind of strong-induction assembly that `regenLaw_all_of_trailLaw_all`
   already is);
2. **the boundary** — the entry head (6 580 at g=2, 53 382 at g=3 — g-dependent), the top-rung exit,
   and the `+80` correction at `gap(11)` seen at g=3 (under measurement at g=4 now: is it a stable
   correction or does it drift?);
3. **the `∀g` step** — that each generation's phase is one such ladder with the top level rising by
   one (M6(g)→M1(g+1) has levels k=5…g+9).

## Honest caveats

- The step-level closure is exact and Lean-backed; the config-level identification is `[MEASURED]`
  at g=2 (one full ladder) and the endpoints are the named shapes. The **reconciling seam** between
  `braid_topgrind`'s literal OUT (pure ones-run `4N+4 = 2^{k+1}−8`) and `regenIn (k+1)`'s left block
  (`2^{k+1}−3`, differ by 5, absorbed by the marker region) is not yet written — the same kind of
  `List`-identity reconciliation that `leadOut_all`/`trailOut_all` needed. Do not claim the assembly
  is done; claim the ingredients are banked and the composition closes numerically.
- The `+80` at `gap(11)` means the pure `topGrindSteps` law is not the whole gap at the top of the
  ladder — there is a boundary term. Resolving it is exactly the point of the g=4 measurement, and
  until then the `∀g` ladder is `[MEASURED at g=2,3]`, not proven.

## Next

1. **g=4** (running) — pin the `+80`: stable correction or drift?
2. **Write the seam** `braid_topgrind` OUT → `regenIn (k+1)` IN as a `List` identity (the missing
   reconciliation), mirroring `leadOut_all`'s marker-wrap lemma.
3. **State the one-generation assembly** `doubStep g : M6 g → M1 (g+1)` as
   `head_g ∘ (∏_{k=5}^{g+9} [braid_topgrind_k ∘ regenLaw_k]) ∘ tail_g`, conditional on the boundary
   objects, and run it — if it elaborates, `h_doub` for one generation is done and `∀g` is the
   remaining induction.

**No machine is decided. No label is upgraded.** Step counts are Lean theorems; the ladder
composition and config shapes are `[MEASURED]` on g=2 (and g=3 for the interior gap law).
