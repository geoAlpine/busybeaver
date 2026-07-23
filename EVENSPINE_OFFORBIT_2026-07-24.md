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

---

# CORRECTION TO THE RETRACTION (same day, later) — it is a BLANK-NORMALIZATION boundary, not an active register

The retraction above **over-corrected**. Two of its claims were themselves wrong, caught by
re-measurement (METHODS M1 — re-derive, do not trust the first read):

1. **"the `1^9` block is chewed by `headLaw` and rebuilt"** — a MEASUREMENT ARTIFACT. At
   `regenIn 5` the marker is `ladderMarker 5 5 ++ M` (1979 cells of ladder comb, then `M`), so
   the first-60-cells window I read was the ladder layers, not `M`. The `1^9` block lives at
   depth ~1979 and was never chewed. The register content threads **inertly**, as `evenSpine`
   assumes.

2. **"the marker is off-orbit / a family the orbit never visits"** — WRONG. The real g=2
   `descIn 9` marker is EXACTLY `001 · (9-seam) · frameL 1 (turnWord ++ endWord ++ zeros 1)`
   (44 cells, `#eval` `true`) — i.e. `evenSpine`'s word with `zeros 1` in place of `zeros 11`.

## The actual gap: finite-list trailing blanks

The tape model reads `0` past the end of a finite list (`mvL ⟨[], h, r⟩ = ⟨[], false, …⟩`).
So the orbit's marker `… zeros 1` **followed by blank** is the *same abstract tape* as
`evenSpine`'s `… zeros 11`, but a **different finite list**, and Lean's `=` distinguishes them.
As the phase runs, the machine writes zeros into that trailing blank region, so by tail-entry
the register carries `zeros 11` **explicitly** (verified: `x2r3_tailin.py` matched). The
content is inert; only the trailing-blank *representation* grows from `zeros 1` to `zeros 11`.

**Decisive check (`#eval` `true`):** `land.left ++ zeros 10 = evenSpine.IN.left` at g=2. So the
orbit's `descIn` config differs from `evenSpine`'s IN by exactly `zeros 10` of trailing left
blank — precisely what **`BlankNorm`** (`steps_lpad_zeros`, already in the repo, GREEN) exists
to reconcile.

## Corrected status

- `evenSpine` is the RIGHT composition target, not off-orbit. `topEntry` produces the same
  marker with `zeros 1`; the two are `BlankNorm`-equivalent.
- The retraction banner on `evenSpine` should be read as: "needs a `BlankNorm` bridge at the
  marker boundary," **not** "models the wrong dynamics."
- This is `S5`/obligation-H tooling (`realizeM1_port` + `BlankNorm`), the same mechanism that
  reconciles the milestone families to `init`. It was always going to be needed; it simply
  shows up at this seam too.

**Lesson (METHODS):** measuring the first-N-cells of a marker that begins with a huge
generated prefix (`ladderMarker`) reads the prefix, not the payload. When a config's left
starts with `pow01`/`ladderMarker` of length `Θ(2^k)`, strip it by its known length before
reading the marker. Both the "active register" error and its detection came from this.

No machine decided. No label upgraded. `x2` remains `[OPEN]`.
