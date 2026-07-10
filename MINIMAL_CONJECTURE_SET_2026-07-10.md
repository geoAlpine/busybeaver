# The minimal distinct-conjecture set of the BB(6) completion frame (2026-07-10)

*How few genuinely-distinct arithmetic conjectures the 17 named BB(6) protections reduce to, and
how that collapse is reflected — machine-checked — in `lean/Completion.lean`. Basis:
`RELOAD_MAP_UNIFIED_2026-07-09.md`, `PAPER_MIRROR_LADDER.md`, `PAPER_CENSUS.md`,
`COMPLETION_SKELETON_2026-07-10.md`. Numerics re-verified `scratchpad/reload_unified.py`
(interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact big-int). No machine decided.*

---

## 1. The headline

The 17 named protection conjectures are **not 17 unrelated problems**. They are instances of
**5 conjecture SCHEMAS**; the three normality schemas are one **meta-schema** `NormalityPQ p q seed`
at three genuinely-distinct p-adic places. So the minimal structure is:

- **3 meta-schemas** — base-p/q normality (`NormalityPQ`), generalized-Collatz 2^k-avoidance
  (`TwoPowerAvoidance`), o17 gate-timing;
- **5 named schemas** — `Normality32`, `Normality43`, `Normality83`, `TwoPowerAvoidance`, o17;
- **17 seed-instances** — one genuinely-distinct per-seed open problem per machine.

The collapse is of **conjecture FORM (shape), not of difficulty.** Two seeds of the *same* reload
map give statistically unrelated reload-unit sequences (measured cross-correlation ≈ 0), so
identity of the schema **transfers no bound** (reload doc §3.3). There remain ~17 distinct open
problems; what is unified is their shape, now exhibited as a single Lean symbol applied at seeds.

---

## 2. The grouping (which machine instantiates which schema)

| schema | engine | place | machines (seeds) | # |
|---|---|---|---|---|
| **`Normality32`** = `NormalityPQ 3 2` | ×3/2 | ℤ₂ | Antihydra, o10, o2, o11, **o13**, o14, o16, o12, o8 | 9 |
| **`Normality43`** = `NormalityPQ 4 3` | ×4/3 | ℤ₃ | **o4** (Lean-literal), o3, o5 | 3 |
| **`Normality83`** = `NormalityPQ 8 3` | ×8/3 | ℤ₃ | o15, o18 | 2 |
| **`TwoPowerAvoidance`** | gen-Collatz 2^k | — | o7 (`o7orbit`), Space Needle (`snOrbit`) | 2 |
| **o17** (own form) | gate-timing | — | o17 | 1 |

Total: 9 + 3 + 2 + 2 + 1 = **17**.

### Internal structure of the ×3/2 band (verified 2026-07-10)
- **Gap-1 canonical class** — Antihydra, o10, o11, o14, o16 are the *identical* engine
  `W ↦ ⌊3W/2⌋` in mirror coordinates `W = v − x_even`. Numerics: **20000/20000 exact**. They are
  the SAME dynamical system at different seeds — the purest case of "one conjecture, many machines."
- **o2 (ceiling)** — gap-1 with flipped sign; the negation-conjugate `w ↦ −w` of the canonical
  engine. Numerics: `o2T(v) = −canon(−v)`, **4000/4000 exact**. Same schema, negated seed.
- **o13** — fixed points (−14,−7), **gap 7**: a *genuinely different* reload map (not
  shift/negation-conjugate to gap-1). Numerics: **2020/4000 mismatch** to the canonical engine.
  Still base-3/2 normality (place ℤ₂), so it shares the `Normality32` FORM, but it is honestly
  a **distinct instance / variant**, not "the same engine." Kept separate in spirit, unified only
  at the level of "base-3/2 normality of its seed."
- **o12, o8** — ×3/2 sea / nested-reset, same fixed-point structure ([OBSERVED], catalogue).

### Why the three normality schemas are NOT one conjecture
×3/2 depth reads the 2-adic place (v₂); ×4/3 and ×8/3 read the 3-adic place (v₃). There is **no
ring map ℤ₂ → ℤ₃**, so the ×3/2 and ×4/3/×8/3 conjectures have no functional relation (reload doc
§3.1). ×4/3 vs ×8/3 share q=3 but differ in the unit multiplier (4 ≡ 1 vs 8 ≡ 2 mod 3) — different
base-p/q expansions. Hence 3 genuinely-distinct places/schemas, not one.

### Why o7/SN and o17 stay their own forms
o7 and Space Needle are **reachability** walls (halt ⟺ orbit hits a `2^k`-thin target), not
density/normality statements; they carry different multipliers (o7 two-multiplier ×3/2 & ×1/2; SN
×5/2) and are two distinct instances of the one avoidance schema. o17 has genuinely unbounded
gate-state (Nerode index 1,2,6,19,54,132 — no finite automaton), a Collatz-type gate-timing
conjecture with no scalar residue — its own irreducible form.

---

## 3. What changed in `lean/Completion.lean`

New **§1.5**: the schema layer.
- `axiom NormalityPQ : Nat → Nat → Int → Prop` — one symbol carrying the whole (K)/AEV
  Conj 1.6 / Mahler-3/2 open content; docstring pins its meaning (ℤ_q^×-equidistribution of the
  reload units of the ×(p/q) orbit at the seed). `abbrev Normality32/43/83` specialize it.
- `inductive Machine` (13 constructors) + `axiom seed : Machine → Int` — per-machine seeds, opaque
  but distinct (so instances never collapse accidentally).
- `def TwoPowerAvoidance (orbit) : Prop := ∀ n k, orbit n ≠ 2^k` — **literal** thin-set schema;
  `axiom o7orbit, snOrbit : Nat → Nat` the two orbit maps.
- The **16 opaque `axiom *_nonhalt : Prop`** are replaced by **defs**: `oX_nonhalt := schema (seed X)`.
  o4 stays literal (`∀ n, Template.steps n Template.init ≠ none`); o17 stays its own `axiom`.
- **`rfl`-checked collapse**: `example : antihydra_nonhalt = NormalityPQ 3 2 (seed .antihydra) := rfl`
  (+ 10 more) — Lean machine-verifies that the conjuncts ARE their schemas at seeds.

`AllHoldoutsNonHalt` and `BB6_eq_championSteps` are unchanged in statement and still assemble by
`Nat.le_antisymm`. Full project green (19 jobs), no new `sorry`/`sorryAx`.

### The axiom audit now shows the collapse
`#print axioms BB6_eq_championSteps`:
```
[BB6, NormalityPQ, championSteps, champion_lower, enumeration_upper,
 holdouts1087_nonhalt, o17_nonhalt, o7orbit, seed, snOrbit]
```
The **16 opaque `*_nonhalt` axioms are gone**. The entire 13-machine (K)-band contributes the
**single symbol `NormalityPQ`** (applied via `seed`); the thin-set band contributes `o7orbit`,
`snOrbit` (through the `TwoPowerAvoidance` def); o17 keeps its own form. `antihydra_nonhalt` audits
as `[NormalityPQ, seed]`, `o7_nonhalt` as `[o7orbit]`.

---

## 4. Honest scope — what stays opaque, what is overclaim-free

- `NormalityPQ` is **uninterpreted** (exactly as the 16 Props were): the file does not formalize
  the reload-unit equidistribution; it names it once and shares it. Its docstring states its meaning.
- The definitional identities `oX_nonhalt := schema (seed X)` **encode** the machine⟺arithmetic
  reductions, which are `[PROVEN-in-lit]` / `[PROVEN on grid]` / `[OBSERVED]` per machine (Mirror /
  RunStructure run-law corollaries; catalogue for o5/o8/o12; automata for o7/SN). **Only o4 is Lean
  end-to-end** (kept literal, reduction `o4_reduction` PROVEN). The enumeration bridge folds the
  other 15 reductions into its hypothesis; this is documented, not silently assumed.
- **Not overclaimed:** o13 is documented as the gap-7 variant, not asserted identical to the gap-1
  engine; the three normality schemas are kept at distinct places (not merged into one conjecture);
  o7/SN/o17 stay their own forms. Per-seed instances stay distinct — the collapse is of shape only.

---

No machine decided. No label upgraded.
