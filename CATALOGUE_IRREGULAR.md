# Frontier catalogue — the 5 "irregular" cryptids o11,o12,o13,o14,o16 are all NESTED Mahler 3/2 (2026-06-29)

*Re-attack of the catalogue's remaining gap: the five machines previously logged as "irregular geometric
content, no clean scalar map" (`CATALOGUE_O7_O12.md` §3–4, `CATALOGUE_O13_SN.md` §2–4). Soundness paramount;
labels `[PROVEN]`/`[VERIFIED]`/`[OBSERVED]`/`[OPEN]` enforced and never upgraded. **No machine is decided; no
non-halting is asserted.** All numerics use `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (exact Python
big-ints), produced by faithful blank-tape simulation with the identical parse/step semantics of `bb_sim.py`,
cross-checked against `bb_sim.run` (all five non-halting to 10M, halt-read never fires; consistent with the
prior 50M checks).*

## Headline result

> **All five "irregular" machines have a CLEAN inner Mahler **μ = 3/2** engine** that the previous
> auto-milestone analysis missed. Each is a **nested counter** in the o10 mould: an **inner clean ×3/2 orbit**
> (the "sea" / mass block) wrapped in an **outer leading-counter countdown** whose roll-over triggers a
> doubly-exponential refill. The famous "irregular collapse orbit" (o11 `3,9,26,303`; o12 `4,10,28,370`;
> o13 `3,6,10,64`; …) is the **outer**, doubly-exponential refill orbit — irregular because each outer step
> is ≈`(3/2)^{k/Δ}` of the previous; the **inner** orbit is clean ×3/2. **No new multiplier appears; all five
> join the existing Mahler-3/2 / Antihydra family (o7,o8,o10,Antihydra).** None is decidable.

So the catalogue's "(d) too irregular for a clean reduction" verdict for these five is **superseded**: they are
**(b) nested Collatz-kernel `T_μ`, μ = 3/2**, the same family as o10 (`CRYPTID_REDUCTIONS.md`: o10 = inner
`⌈3m/2⌉` + irregular doubly-exp outer refill). The nested-counter hypothesis in the task brief is **confirmed
for all five**.

## Summary table

| machine | grind milestone | structure | inner ×3/2 engine `[VERIFIED]` | outer (irregular) | new μ? | decidable? |
|---|---|---|---|---|---|---|
| **o11** | R-extreme, state B | leading counter `1^k` + `(10)^m` sea | sea `m → ⌊3m/2⌋+4` **exact** (12/12 in-epoch) | `k→k−4` countdown; refill orbit `3,9,26,303` | no (3/2) | **HOLDOUT** |
| **o12** | L-extreme, state C | two-counter `1^a 0 1^b` + sea | `a → ⌊3a/2⌋+3δ−1`, ratios→1.500 | `b→b+3,a→a−2`; sea countdown; refill `4,10,28,370` | no (3/2) | **HOLDOUT** |
| **o13** | L-extreme, state C | two-counter `1^a 0 1^b` + sea | a-start ratios `1.521…1.500→3/2` | sea countdown; refill `3,6,10,64` | no (3/2) | **HOLDOUT** |
| **o14** | L-extreme, state E | two-counter `1^a 0 1^b` + `(…4,4,2)` marker tail + sea | a-start ratios `1.510…1.503→3/2` | sea countdown + marker accretion | no (3/2) | **HOLDOUT** |
| **o16** | R-extreme, state A | leading counter `1^k` + defect block + `(10)^m` sea (T2) | sea `s → ⌊3s/2⌋+2` (consec. exact) ratios→1.50 | `k→k−1` countdown; doubly-exp refill | no (3/2) | **HOLDOUT** |

`δ ∈ {1,2}` for o12 is the per-sub-cycle sea consumption; the correction term equals `3δ−1` exactly (the
irregularity lives entirely in δ, not in the ×3/2 multiplier).

---

## §0. Lottery check — all five HOLDOUT (sound tools, this run)

Re-run with generous parameters (`far_dfa` N≤8000/m≤8; `far_finder` N≤5000/k≤6; `far_cegar` N=2000/120 rounds).
Every result HOLDOUT; the soundness gate held (no false `NEVER_HALTS`); the cryptid gate is not reached.

```
o11/o12/o13/o14/o16:  far_dfa = HOLDOUT   far_finder = HOLDOUT   far_cegar = HOLDOUT (not closed, |negs|=120)
```

**Verdict [PROVEN, this run]: none of o11,o12,o13,o14,o16 is decidable by our sound tools.** Consistent with
the prior §0 of `CATALOGUE_O7_O12.md` / `CATALOGUE_O13_SN.md`. The regular-envelope-with-irregular-content
signature is exactly why bouncer/FAR correctly hold out: the inner ×3/2 is clean, but the **outer** refill is
doubly-exponential and not eventually periodic, so no finite-state / semilinear over-approximation closes.

---

## §1. o11 — `1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF` — nested Mahler 3/2, INNER MAP EXACT

**Mechanism `[VERIFIED vs raw TM]`.** Tape at the R-extreme in state B is `0 1^k 0 (10)^m`: a leading unary
counter `1^k` and a `(10)^m` "sea". Per B-visit the leading counter loses 4 (`k→k−4`, the **outer** countdown)
while the sea executes a **clean inner Mahler step**:

> **Inner map `[VERIFIED, exact]`:** `m → ⌊3m/2⌋ + 4`. In the epoch opened by the `k=303` collapse the sea runs
> `2, 7, 14, 25, 41, 65, 101, 155, 236, 358, 541, 815, 1226` and **every step satisfies `m' = ⌊3m/2⌋ + 4`
> exactly** (12/12; verified with exact big-ints). Ratios `3.5, 2.0, 1.79, 1.64, 1.585, 1.554, 1.535, 1.523,
> 1.517, 1.511, 1.507, 1.504 → 3/2`.

The `+4` is conserved feed: the leading counter donates its 4 lost cells to the sea each step. When `k` hits 0
the sea is re-absorbed into a new leading block (collapse), and a new epoch opens — the **outer refill orbit
`3,9,26,303`** (pure `0 1^k 0` configs at `t=10,47,272,28101`; the catalogue's "irregular" orbit). The refill
is **doubly-exponential** in `k`: an epoch with leading counter `k₀` runs ≈`k₀/4` inner ×3/2 steps, so the next
collapse ≈`(3/2)^{k₀/4}` — which is why `26→303` jumps ×11.6 and the 5th collapse is `> 10¹³` steps away
(unreachable). The inner engine is clean; the outer orbit is irregular **for the same reason o10's is**.

- **Classification: (b) nested Collatz-kernel, μ = 3/2, p = 2** — Antihydra/o10 family (was "(d) irregular").
- **Halt discriminator `[PROVEN from spec]`:** C reads 0 (C entered only `B:0→1LC`); head-local defect/boundary
  alignment of the nested `(3/2)ⁿ` orbit. Exact 2-adic predicate not separately derived (as for o7/o8/o10).
- **Status [OPEN], Mahler-3/2-hard (nested).** Not decidable by sound tools (§0).

## §2. o12 — `1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB` — nested Mahler 3/2, inner clean mod sea-coupling

**Mechanism `[VERIFIED]`.** Tape at the L-extreme in state C is `0 1^a 0 1^b 0 (10)^m`: a **two-counter head**
`1^a 0 1^b` over a `(10)^m` sea. The inner sub-cycle is the Antihydra-type exchange `a→a−2, b→b+3` (total
`a+b` grows +1/step); when `a` bottoms out the two blocks **merge** and a new sub-cycle starts at `[a',4]`,
consuming `δ` cells of sea. The sub-cycle-start block `a` is the inner orbit:

> **Inner orbit a-start `[VERIFIED]`:** `44, 68, 104, 158, 242, 368, 554, 836, 1256, 1886, 2834, 4256, 6386,
> 9584` with ratios `1.545, 1.529, 1.519, 1.532, 1.521, 1.505, 1.509, 1.502, 1.502, 1.503, 1.502, 1.500,
> 1.501 → 3/2`. The exact step is `a' = ⌊3a/2⌋ + (3δ − 1)`, where `δ ∈ {1,2}` is the sea consumed that
> sub-cycle (verified: correction `2 ⟺ δ=1`, correction `5 ⟺ δ=2`, perfectly correlated).

The **outer** orbit is the sea countdown; when the sea empties, the head collapses to a pure `0 1^k` block —
the catalogue's irregular orbit `4,10,28,370` (`t=17,95,565,58083`). The ×3/2 multiplier is clean; the
irregularity is the δ-coupling (how much sea each sub-cycle eats) — a genuine carry/parity defect like o15's.

- **Classification: (b) nested Collatz-kernel, μ = 3/2, p = 2** (was "(d) irregular").
- **Halt discriminator `[PROVEN from spec]`:** F reads 0 (F entered only `E:0→1RF`).
- **Status [OPEN], Mahler-3/2-hard (nested).** Not decidable (§0).

## §3. o13 — `1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA` — nested Mahler 3/2

**Mechanism `[VERIFIED]`.** Same two-counter `1^a 0 1^b` + sea as o12 (L-extreme, state C): inner exchange
`a→a−2, b→b+3`, merge, restart `[a',4]`, sea consumed. Inner a-start orbit:

> **Inner orbit a-start `[VERIFIED]`:** `40, 67, 104, 163, 248, 379, 572, 865, 1301, 1955, 2936, 4411` with
> ratios `1.675, 1.552, 1.567, 1.521, 1.528, 1.509, 1.512, 1.504, 1.503, 1.502, 1.502 → 3/2`. (The exact
> correction is again sea-coupled; the multiplier is clean 3/2.)

Outer refill orbit (pure `0 1^k` collapses) `3,6,10,64` (`t=20,51,122,3519`) — doubly-exponential, irregular.

- **Classification: (b) nested Collatz-kernel, μ = 3/2, p = 2** (was "(d→b) irregular").
- **Halt discriminator `[PROVEN from spec]`:** E reads 0 (E entered only `D:1→1LE`).
- **Status [OPEN], Mahler-3/2-hard (nested).** Not decidable (§0).

## §4. o14 — `1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE` — nested Mahler 3/2 + accreting marker tail

**Mechanism `[VERIFIED]`.** Two-counter `1^a 0 1^b` (L-extreme, state E) over a sea, **plus an accreting marker
tail** (`…, 4, 4, 2` — one extra `4`-block per outer epoch, the source of the catalogue's `4,4,2` marker).
Inner exchange `a→a−2, b→b+3`, restart at `[a', 7, 4(,4)*, 2]`. Leading-block a-start orbit:

> **Inner orbit a-start `[VERIFIED]`:** `3, 10, 21, 37, 61, 97, 151, 232, 354, 537, 811, 1222, 1839, 2764` with
> ratios `…, 1.557, 1.536, 1.526, 1.517, 1.510, 1.507, 1.505, 1.503 → 3/2`.

Outer structure: sea countdown (−2/sub-cycle) + marker accretion; o14 never forms a pure single block (the
`4,2` tail is always present), which is why the §0 `analyze` pure-block scan finds none — the inner ×3/2 is
nonetheless clean.

- **Classification: (b) nested Collatz-kernel, μ = 3/2, p = 2** (was "(d→b) irregular").
- **Halt discriminator `[PROVEN from spec]`:** F reads 0 (F entered only `C:0→1LF`).
- **Status [OPEN], Mahler-3/2-hard (nested).** Not decidable (§0).

## §5. o16 — `1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE` — nested Mahler 3/2 (T2 single-defect)

**Mechanism `[VERIFIED]`.** The T2 template (distinct head shape, same kernel): tape at the R-extreme in state
A is `1^k 0^2 (10)^m` with a **leading counter `1^k` decaying by 1 per outer step** (`k = 25,24,23,…`) and a
roaming defect block + `(10)^m` sea that **grows ×3/2 per outer step**:

> **Inner sea orbit `[VERIFIED]`:** at sub-cycle starts (defect block = 4) the sea reads, against the decaying
> leading `k`: `k=17:73, k=16:111, k=15:168 …  k=11:871, k=10:1308 … k=7:4426`. Consecutive steps are clean:
> `73→111 = ⌊3·73/2⌋+2`, `111→168 = ⌊3·111/2⌋+2`, `871→1308 = ⌊3·871/2⌋+2`; ratios `1.521, 1.514, …, 1.502 →
> 3/2`.

The leading counter `k→k−1` is the outer countdown; its roll-over triggers a doubly-exponential refill (≈
`(3/2)^k`). This is structurally **o11 with step −1 instead of −4** — the same nested 3/2 engine in the T2
costume.

- **Classification: (b) nested Collatz-kernel, μ = 3/2, p = 2 (T2 single-defect costume)** (was "(d→b)").
- **Halt discriminator `[PROVEN from spec]`:** F reads 0 (F entered only `E:0→1RF`).
- **Status [OPEN], Mahler-3/2-hard (nested).** Not decidable (§0).

---

## §6. Catalogue placement & consequences

| machine | facet | kernel `q` (μ,p) | inner engine (genuine) | outer (irregular) | discriminator |
|---|---|---|---|---|---|
| **o11** | density-type | q=2 (μ=3/2,p=2) | sea `⌊3m/2⌋+4` **exact** | `k→k−4` refill `3,9,26,303` | C reads 0 |
| **o12** | density-type | q=2 (μ=3/2,p=2) | `⌊3a/2⌋+3δ−1` (δ∈{1,2}) | sea-countdown refill `4,10,28,370` | F reads 0 |
| **o13** | density-type | q=2 (μ=3/2,p=2) | a-start ×3/2 | refill `3,6,10,64` | E reads 0 |
| **o14** | density-type | q=2 (μ=3/2,p=2) | a-start ×3/2 | sea-countdown + marker accretion | F reads 0 |
| **o16** | density-type | q=2 (μ=3/2,p=2) | sea `⌊3s/2⌋+2` | `k→k−1` doubly-exp refill | F reads 0 |

**What changed.** The Stage-1 verdict (`CRYPTID_REDUCTIONS.md` "all slow-width content IRREGULAR") was an
**envelope/outer-orbit** observation; the auto-milestone read the per-sweep `(10)*` reshuffling (o11/o16) or
the two-counter exchange snapshots (o12/o13/o14), i.e. the wrong event — exactly the failure mode flagged for
o7 ("auto-tag IRREGULAR is the wrong event"). Reading the correct **inner** milestone (the sea / mass block at
the sub-cycle boundary) exposes a **clean ×3/2 Mahler engine in all five**. They are therefore **(b)
nested-Mahler-3/2**, not "(d) structureless".

**No new multiplier.** All five are μ = 3/2 (p=2), the Antihydra family — joining Antihydra, o7, o8, o10-inner.
The BB(6) cryptid families remain {Mahler 3/2: Antihydra, o7, o8, o10, **o11, o12, o13, o14, o16**}, {Erdős
ternary 2^a/3: o5(4/3), o15, o18(8/3)}, {base-3 odometer: o17}, {μ=5/2: Space Needle}. The "~2–3 named families,
not 19 separate problems" picture is **strengthened**: 9 machines now sit explicitly in the Mahler-3/2 family.

**Why still irregular / why HOLDOUT.** The clean inner ×3/2 does **not** give an exact halt criterion or a
decision: the **outer** refill orbit is doubly-exponential and not eventually periodic (each outer step is
≈`(3/2)^{k/Δ}` of the last), so no finite-state / semilinear over-approximation closes — the same obstruction
as o10's outer orbit (`CRYPTID_REDUCTIONS.md` o10: "outer orbit doubly-exp & irregular"). The reduction is
"reduced to family + inner multiplier (nested)", **not** an exact criterion; these five are therefore
**in-family by multiplier but not in-scope** for the exact reductions of `BB6_STRUCTURAL_LIMIT_THEOREM.md`
(scope = {Antihydra, o18, o15, o10-inner}).

## §7. Soundness statement
Every orbit is machine-checked with exact big-ints by faithful blank-tape simulation (identical parse/step
semantics to `bb_sim.py`), cross-checked against `bb_sim.run` (all five non-halting to 10M, halt-read never
fires). The inner ×3/2 maps are `[VERIFIED]` (o11: `⌊3m/2⌋+4` exact 12/12; o16: `⌊3s/2⌋+2` exact on consecutive
observed steps; o12/o13/o14: ratios converging to 3/2 to ≤0.003, exact correction sea-coupled) — **not promoted
to `[PROVEN]`** (the outer refill is not fully modelled, exactly as for o10/o8-nested). The three sound
verifiers returned HOLDOUT on all five with generous parameters; the soundness gate held. **No machine is
decided; no non-halting is asserted; no new multiplier is claimed.**
