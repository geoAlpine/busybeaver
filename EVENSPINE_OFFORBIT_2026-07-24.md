# `evenSpine`'s marker is OFF-ORBIT — a measured retraction (2026-07-24)

**Retraction (METHODS M5/M7).** Commit `422fde1` closed the marker glue (`S1`) generically —
that part stands — but then claimed `evenSpine` composes the whole even phase "for the orbit".
It does **not**. `evenSpine` is a GREEN, TRUE theorem, but the specific marker it feeds to
`descIn` is a config the real orbit never visits. Found by `#eval` + orbit measurement before
any label was upgraded. No theorem is deleted; the on-orbit *reading* is withdrawn.

## What is still true (unchanged, GREEN)

- `descMarkStep_layer`, `ladderMarker_snoc`, **`descMarkInner_eq_ladderMarker`** — S1's marker
  identity, generic in the base marker `M`. Correct.
- `headToLadder`, `topRungToMilestone`, `headLaw`, `ladderToCascade`, `tailLaw`, `topRung`,
  `seam74` — all general in their marker/tail. Correct.
- `evenSpine`'s **step-count** anti-vacuity `decide`s (2 117 332 at g=2, 33 650 954 at g=4) —
  these are pure `Nat` and independent of the marker; correct.

## What is wrong: the marker instantiation

`evenSpine` instantiates the base marker as `frameL j (turnWord ++ endWord ++ zeros 11 ++ L)`
— i.e. it threads `tailLaw`'s IN-register **backward** through `topRung`/ladder/`headLaw` as an
inert free variable. The `#eval` test at g=2 (`n=5, j=1`) against `steps 1683 (M6 2)` shows the
real `descIn 9` marker is **10 cells shorter** and structurally different:

| | real orbit `descIn 9` marker | `evenSpine` requires |
|---|---|---|
| cells (after comb) | 44 | 54 |
| deep tail | `… 1^9 … 0^~2` | `… (no block) … 0^11 ++ L` |

## The decisive measurement: the frame register is ACTIVE, not inert

Tracking the register's `1^{≥6}` block across the g=2 phase (after each config's leading comb):

| milestone | step | `1^{≥6}` block in the register |
|---|---|---|
| `descIn 9` (entry) | 734 759 | **`1^9` present** (turnWord's block) |
| `regenIn 5` | 739 656 | **gone** — chewed to comb by `headLaw` |
| `cascadeReg 10` (ladder top−1) | 1 270 303 | gone |
| tail-IN | 2 851 954 | **`1^9` reappears** — rebuilt near the tail |

So a `1^9` block sits in the register at descent entry, is **consumed by `headLaw`**, stays
comb through the ladder, and is **rebuilt** by the time `tailLaw` reads it. The register is not
a free marker threaded unchanged — it is **active tape the machine reads and rewrites**. My
free-marker threading (`evenSpine`, and the marker' I fed `headToLadder`) models an inert
marker, which the orbit contradicts.

## Consequence for the architecture

The clean picture "descent marker = ladder marker = tail register, threaded once" is **too
simple**. The true decomposition of the even phase is:

- The **base marker** `marker'` that threads inertly is the OUTER decoration (`m1casc` frame /
  milestone scaffolding), NOT the frame odometer register.
- The **frame odometer register** (`frameL j`) that `tailLaw` consumes is **built by the
  ladder/topRung dynamics**, not carried from `descIn`. The `1^9` blocks of `turnWord` are
  active blocks the ladder chews and the exit rebuilds.

So `evenSpine`'s job must be redone with the register produced *in place* by the exit dynamics,
not fed in as `descIn`'s marker. Concretely: identify what `marker'` (the true inert base) is on
the orbit — strip the ladder layers AND the active frame region from the real `descIn` marker —
and re-instantiate `headToLadder`/`topRungToMilestone` with that, letting `frameL j` emerge from
`topRung`'s OUT rather than from `descIn`'s IN.

## Discipline note

This is exactly the failure mode METHODS M7 (composition-scope audit) exists to catch, and it
was caught **before** any label moved: a green theorem whose endpoint family does not appear on
the orbit at full shape. The `S1` marker identity (`descMarkInner_eq_ladderMarker`) is real and
useful; the `evenSpine` *orbit* composition is retracted pending the active-register model.

No machine decided. No label upgraded. `x2` remains `[OPEN]`.
