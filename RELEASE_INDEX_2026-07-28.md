# Release index — what exists, what is current, what is gated (2026-07-28)

The harvest pass. This is the single page to read before deciding what, if anything, leaves the
repository. It states for every external-facing artifact: its scope, its date, whether it is
**current**, and what gate applies.

**Publication decision, owner, 2026-07-28: everything known to date is published to the public git
repository and archived on Zenodo**, on the reasoning that it should save the next person the work.
This supersedes the 2026-07-07 hold on releasing the material.

Two things are *not* covered by that decision and remain gated:

* **Community posting** (bbchallenge forum / Discord / wiki edits) — a different channel; not
  authorised here. Publishing the archive is not the same as announcing it.
* **Academic outreach by email** — still requires an explicit per-send go-ahead, and
  `OUTREACH_EMAIL_DRAFT.md` still lacks recipient and signature fields.

No one has been contacted. The only external access made during the harvest pass was *reading* the
public bbchallenge wiki index to confirm the current holdout list.

---

## 1. The two deliverables, by audience

### A. The unconditional result — two holdouts decided

| | |
|---|---|
| artifact | **`PAPER_TWO_HOLDOUTS_DECIDED.md`** (new, 2026-07-28) |
| claim | `x2` and `C` never halt from the blank tape. Unconditional, Lean 4, `[propext, Quot.sound]` |
| novelty | **verified 2026-07-28** against `BB6_holdouts_1094.txt` (2026-06-29, sha256 `9764…dbdd4`): both STILL OPEN, two distinct canonical classes |
| audience | bbchallenge community; anyone who wants to verify |
| gate | **released** (git + Zenodo, 2026-07-28). Announcing it to the community is a separate, ungranted decision |
| currency | **current**. Re-run the §2 novelty check before *citing* it — lists appear ~monthly and `1094` is now ~1 month old |

This is the only thing in the program that is unconditional and checkable end to end.

### B. The characterisation — why the Collatz core resists

| | |
|---|---|
| artifacts | `PAPER_MAIN.md` (arXiv draft), `BB6_FRAMEWORK_PACKAGE.md`, `OUTREACH_ABSTRACT.md`, `OUTREACH_EMAIL_DRAFT.md` |
| claim | The named cryptids reduce, by exact machine-verified reductions, to a single-orbit equidistribution kernel — the floor-mirror single-orbit fragment of Andrieu–Eliahou–Vivion (arXiv:2510.11723) — plus **proven** barriers ruling out structure-only, all-orbits and finite-certificate proofs |
| audience | homogeneous dynamics / measure rigidity / number theory (AEV authors; Einsiedler–Lindenstrauss–Host circle) |
| gate | **per-send go-ahead required.** `OUTREACH_EMAIL_DRAFT.md` still needs (1) recipient address, (2) sender name/affiliation to sign with, (3) an explicit "send it" |
| currency | **substantively current, formally stale** — see §2 |

This is the program's defensible original contribution: it required deciding no cryptid.

---

## 2. Currency audit

Every external artifact was checked today for statements that are now false. Result: **one was
actively wrong, one was stale, the rest are sound.**

| document | date | verdict | action taken |
|---|---|---|---|
| `PAPER_TWO_HOLDOUTS_DECIDED.md` | 07-28 | current | *(new this pass)* |
| `PAPER_X2_INTEGER_DOUBLER.md` | 07-13 | **was WRONG** — its banner said the machine is *not decided* and that `carry_step` is the open gap | **SUPERSEDED banner added**; it now points to A and explains that it documents an abandoned first construction |
| `BB6_CRYPTID_PACKAGE.md` | 07-04 | **was stale** — "the frontier is 1104 undecided holdouts" | dated currency note added (list is now 1094; two decided) |
| `PAPER_MAIN.md` | 06-29 | **sound** — its "no machine decided" is explicitly scoped to the *Collatz core*, and `x2`/`C` are template-island machines, not core machines | none |
| `BB6_FRAMEWORK_PACKAGE.md` | 07-04 | sound (Antihydra-scoped) | none |
| `OUTREACH_ABSTRACT.md` | 07-05 | sound (Antihydra-scoped) | none |
| `OUTREACH_EMAIL_DRAFT.md` | 07-07 | sound; still explicitly marked NOT SENT | none |
| `PAPER_TEMPLATE_METHOD.md` | — | sound (o4-scoped, "no machine is decided" holds there) | none |

**Closed, 2026-07-28.** `lean/X2.lean` carries ~12,000 lines of prose from the abandoned first
construction, calling the machine `[OPEN]` with a `[DESIGN ONLY]` `carry_step` gap. Since the file
is bundled in the archive, a reader meeting it cold would have been misled, so **a STATUS banner was
added at the head of the file** pointing at `T7Entry.x2_nonhalt_blank`. The body is left intact as a
record of the route that did not close. `PAPER_X2_INTEGER_DOUBLER.md` and §4.3 of artifact A carry
the same warning.

---

## 3. What changed since the artifacts were written, and is now captured

Everything below post-dates `PAPER_MAIN.md` (06-29) and was not in any external artifact until this
pass:

* **`x2` and `C` decided** (07-25 / 07-26) — now artifact A.
* **`RungCalc`** — the comb-doubler mechanism factored out machine-independently; six `rfl`s per
  machine; 18 of the 1104 tiled (`lean/IslandTiles.lean`). Captured in artifact A §7.
* **The census caution** — an exact structural test finds machines that 5·10⁶-step simulation cannot
  classify (14 of the 18 are `UNRESOLVED` under the epoch-ratio census). The inference "the residual
  is dominated by carry-opaque ratios" is **withdrawn**. Captured in artifact A §7 and in
  `STOCKTAKE_2026-07-28.md` §3.
* **`D`** reduced to a single named obligation (`DCascade.EpochLaw`), with entry and assembly proven.
  Internal only — `D` is not decided, so it does not belong in an external artifact yet.

---

## 4. Recommended decision, stated plainly

1. **Artifact A is finished and released** (git + Zenodo, 2026-07-28). Announcing it on the
   bbchallenge community channels remains a separate, ungranted decision.
2. **Artifact B is finished and released as part of the same archive.** Sending it to named
   researchers by email still needs a per-send go-ahead plus the three missing fields in the email
   draft. No further research is required for it.
3. **No further research is recommended.** The complete BB(6) proof needs every holdout; the ~17
   named cryptids sit behind an open equidistribution conjecture, and structure-only / all-orbits /
   finite-certificate arguments are *proven* not to reach them. See `STOCKTAKE_2026-07-28.md`.

---

## 5. Reproduction, for whoever picks this up

```
lean/                 Lean 4 v4.31.0, zero-Mathlib.  `lake build` → EXIT 0, 95 targets
                      2,026 theorem declarations, sorryAx 0, Classical.choice 0
bb6_holdouts.py       novelty check (TNF + left–right reversal)
_bbdata/              the holdout lists checked against
```

Build discipline worth knowing: `DEntry` and `DEpoch` are kernel-evaluation-heavy and must **not**
build in parallel — together they exhaust memory and the machine thrashes (measured: CPU 9 % vs
750 % when run alone). Run `lake build DEntry`, then `lake build DEpoch`, then `lake build`.

---

**No machine is decided by this index. No label is upgraded. Nothing was sent to any individual or
community channel; the material was published to the public repository and archive.**
