# Remaining tasks — organized inventory (2026-07-04)

*Task map after the 2026-07-03/04 cryptid campaign. Supersedes nothing in `PROBLEM_LIST.md` (P0–P13); it
records what is **DONE**, what is **ACTIONABLE**, and what is **GENERATIONAL** (no internal route). SOUNDNESS:
nothing here is claimed solved.*

## DONE (this campaign) ✅

- **o17 core** — full `[PROVEN]`-level characterization: finite-control base-3 digit-string transducer; the
  unbounded-digits + polynomial-growth obstruction unified as a free-running LSB counter; **halt predicate
  `[PROVEN]`-reduced to one parity bit** (leading block ever even); the no-jump residual dissected and shown
  **core-hard**. (`O17_CORE_TRANSDUCER.md`.)
- **o3** — brought to o17's standard; the **second Type-II structural outlier** (bounded `{0,1}` digits, PROVEN
  halt gate, carry cascade dissected to the no-jump analogue). (`O3_TRANSDUCER.md`.)
- **9 slow-width cryptids reverse-engineered & classified** into a machine-verified **trichotomy** (Type I
  Mahler-3/2 ×11; Type II outliers o17, o3; Type III scalar-Collatz Space Needle). `√t` shown non-diagnostic.
  (`CRYPTID_CLASSIFICATION_2026-07-04.md`, `CRYPTID_SLOWWIDTH_2026-07-04.md`.)
- **All 9 halt predicates `[PROVEN from table]`** (unique-predecessor gates, blank never-fire verified).
  (`MAHLER_HALT_GATES_2026-07-04.md`, `SPACE_NEEDLE_HALT.md`, `O2_O7_HALT.md`, `o3_transducer.py`.)
- **(K) fresh-angle probe** — verdict (c): the two-counter/reachability framing gives **no new handle**.
- **Soundness audit** — VERDICT **SOUND**; 2 in-session errors (Space Needle all-ones; o7 coordinate) caught &
  corrected. (`CRYPTID_AUDIT_2026-07-04.md`.)

## ACTIONABLE — status

- **A1. Space Needle halt-set `S`** ✅ DONE. `S = {2^k−1} ∪ {sporadic}`; `sporadic∩[1,255]={6,102}` (`6=2·3`,
  `102=2·3·17`), very sparse. Blank orbit avoids all of `S`. Exact sporadic rule = small `[OPEN]` sub-curiosity.
  (`SPACE_NEEDLE_HALT.md` §3.)
- **A2. 1104-holdout frontier census** ✅ DONE. Structurally homogeneous: 1104 slow polynomial counters (√t 665,
  sub-√t 399; 0 halt, 0 exp-width); bounded-digit (o3-class) ~522 (~half; proxy split ~183 kernel-less / ~176
  odometer); sound suite 0/15. (`BB6_FRONTIER_CENSUS_2026-07-04.md`, `holdout_census*.py`.)
- **A3. External packaging** ✅ DONE. `BB6_CRYPTID_PACKAGE.md` — trichotomy + 9 PROVEN halt gates + Type-II
  dissections + census + the two walls, shareable alongside `BB6_FRAMEWORK_PACKAGE.md`.
- **A4. o4 TM** ✅ DONE (found in repo, not missing): `o4 = 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`
  (`cryptid_map.py`). Not yet reverse-engineered (a follow-up if wanted).

### Remaining actionable follow-ups
- **A5. Reverse-engineer o4** (`[small]`, TM now in hand) + fold into the trichotomy.
- **A6. Per-machine Type-I/II split of the ~522 bounded-digit band** (`[substantial]`) — the proxy gives
  ~183 o3-like / ~176 odometer; a clean split needs per-machine reverse-engineering (extend the halt-gate +
  kernel detection over the band).

## GENERATIONAL — no internal route (documented, not action items)

- **B1. (K) / P1 — the Mahler-3/2 kernel.** Unlocks **all 11 Type-I cryptids at once** (Antihydra, o2, o7, o10,
  o11, o12, o13, o14, o15, o16, o18) — each Type-I halt gate reduces to single-orbit equidistribution of a
  `⌊3x/2⌋` (or `⌊8x/3⌋`) orbit. Proven internal barriers (No-Structure, Coverage No-Go, decider-preemption,
  even-count floor); needs generational new math (`PROBLEM_LIST.md` P1/P1′) or external movement on AEV/Mahler.
- **B2. Generalized-Collatz for Type II/III.** o17, o3 (Type II) and Space Needle (Type III) reduce to
  generalized-Collatz reachability over their own carry cascade / scalar orbit — a Collatz-type statement with
  **no bounded predictor** (verified core-hard). Distinct from (K); each needs a Collatz-class breakthrough.

## CLOSED / not-independent

- **P8–P13** (`PROBLEM_LIST.md`): proven `(K)`-hard/equivalent (`#even`, drift>0, quenched Cramér) or dead ends
  (independence question). Not separate handles.

## Suggested next (highest leverage among ACTIONABLE)

**A2 (1104-holdout census)** maps the real BB(6) frontier and is genuinely new; **A3 (packaging)** is the
memory's stated priority and banks the durable contribution; **A1 (Space Needle `S`)** is the quick clean win.
B1/B2 remain the walls — external, generational.
