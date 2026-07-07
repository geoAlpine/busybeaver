# Mahler-sea census — o11/o12/o13/o14/o16 + Space Needle brought onto the species map (2026-07-07)

*Extends the GATE + STRUCTURE + PROTECTION classification (`BB6_CRYPTID_SPECIES_2026-07-07.md`,
`PAPER_SPECIES_SURVEY.md`) to the unclassified remainder: the five nested-Mahler-3/2 "sea" machines and
Space Needle (×5/2). Survey depth (not full template ports). o15 — which sits inside the o11–o16 label
range — is NOT re-run here: it is already fully classified (string-ledger; one table with o18 per
`O15_O18_IDENTITY_2026-07-07.md`) and is quoted, not re-derived. SOUNDNESS: labels
`[PROVEN]`/`[PROVEN by run]`/`[OBSERVED]`/`[MODEL]`/`[OPEN]`; fatal configs were re-confirmed by an
independent second simulator (`msea_replay.py`, 6/6 step-exact). **No machine decided.**
Scripts: `msea_gate.py`, `msea_struct.py`, `msea_struct2.py`, `msea_struct3.py`, `msea_fatal.py`,
`msea_fatal_map.py`, `msea_o11_residue.py`, `msea_replay.py`.
Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`.*

## 0. Headline

> All six machines fit the decomposition with no NEW species shape required. The five sea machines are
> **(K)-seeded (×3/2) residue-ledger machines with RESETTING ledger memory** (each doubly-exponential
> outer refill re-seeds the epoch — the o15/o18 memory class, not the o4/o3 class), o16 additionally in
> the **tower-sparse-gate costume** (gate touched 15 times in 12M steps, only at refills). **Space Needle
> is a string-ledger machine over its own ×5/2 kernel — NOT (K)-seeded** (5/2 ∉ 2^a/3^b), with fatal set
> = near-cylinder in the base-2 digit string, and CUMULATIVE value memory (annealed non-halt-leaning).
> **Fatal sets are `[PROVEN nonempty by run]` for all six** — new concrete halting standalone configs for
> o11, o12, o13, o14, o16 (none was previously exhibited for these five; their gates were only known
> never to fire from blank). The sharpest new handle: **o11's fatality is a clean residue condition**
> (below). Blank-tape reachability of any fatal config is in every case exactly the open protection.

## 1. GATE stage `[PROVEN from table]` + census `[OBSERVED, 12M steps]` (`msea_gate.py`)

Unique halt-predecessor re-verified from each table (forced chain printed by the script); radius-4
window census at every gate-trigger event, checkpoints 2M/6M/12M:

| machine | forced chain | halt ⟺ | \|S\| | saturated by | triggers (12M) | unsafe |
|---|---|---|---|---|---|---|
| o11 | C only via `B,0→1LC` | B reads 0 with left nbr 0 | **6** | step 191 | 3,546 | **0** |
| o12 | F only via `E,0→1RF` | E reads 0 with right nbr 0 | **7** | step 233 | 5,238 | **0** |
| o13 | E only via `D,1→1LE` | D reads 1 with left nbr 0 | **11** | step 11,510 | 3,493 | **0** |
| o14 | F only via `C,0→1LF` | C reads 0 with left nbr 0 | **7** | step 789 | 3,010 | **0** |
| o16 | F only via `E,0→1RF` | E reads 0 with right nbr 0 | **7** | step 453 | **15** | **0** |
| SN  | F only via `C,0→1LF` | C reads 0 with left nbr 0 | **13** | step **6,663,348** | 684 | **0** |

The universal pattern holds: every gate is small, local, saturating, and safe. Two flags: **o16's gate
is tower-sparse** (15 exposures in 12M — only at sea-collapse refills, o17-flavor timing), and **SN is
the slowest saturator** of the whole analyzed family (13th window appears at 6.66M — window classes
track the ×5/2 epoch ladder, so slow late arrivals are expected and the census label stays `[OBSERVED]`
with less force than the others).

## 2. STRUCTURE stage `[OBSERVED, numeric-exact on stated generations]` (`msea_struct2.py`, `msea_struct3.py`)

Milestones = the documented extreme+state events (raw gate-triggers are mid-sweep reshuffles — re-hit
and avoided, matching the catalogue's "wrong event" warning). Template test = run-compressed RLE shape
classes (no sweep-period cap, so the o4-era period ≤ 8 detector limitation does not apply to SN's ×5/2
sweeps).

| machine | template | counter law (this survey) | outer orbit |
|---|---|---|---|
| o11 | **RIGID** (6 shapes/26 gens) | sea `m′=⌊3m/2⌋+4` exact **20/22** (2 misses = epoch boundaries); `k→k−4` (20/22) | refills; collapse `3,9,26,303` (prior) |
| o12 | **RIGID** (24/6000) | in-epoch `(Δa,Δb)=(−2,+3)` 5945/6000; a-start `⌊3a/2⌋+c`, `c∈{2,5}=3δ−1` **25/27** | pure collapses `4,10,28,370` @ t=17/95/565/58083 ✓ |
| o13 | **RIGID** (22/4666) | `(−2,+3)` 4627; a-start `⌊3a/2⌋+c`, **`c∈{7,4}=3δ+1`** 17/19 — NEW: two-valued correction mirroring o12's `3δ−1` | collapses 9,19,63 @ t=93/372/3328 (doubly-exp ✓) |
| o14 | **RIGID** (31/3857) | counters at RLE blocks (0,2): `(−2,+3)` 3821/3825; a-start `⌊3a/2⌋+6` **15/18, single correction** (NEW: c=+6); restart b=7; marker tail `(4,4,2)` stable | sea countdown + marker accretion |
| o16 | **RIGID** (18/5804) | `[k | 1^m sea | defect]`; `k→k−1` (18 events) + one refill `+24`; sea `⌊3s/2⌋+2` on the clean defect-4 pairs (5; rest are boundary jumps) | `k` countdown, doubly-exp refill ✓ |
| SN  | **RIGID** (15/1081, 0 new in 2nd half) | in-epoch `(−1,+2)` 704/713; clean resets `[1,b]`: `b = 12,36,96,246,621` each **`b′=⌊5b/2⌋+6` exact**, interleaved 3-block configs `[1,b,b/2+2]` (4/4 exact) | reset times 226 → 2.5k → 31k → 434k → 6.5M → 18.3M |

**SN survey finding `[OBSERVED]`:** the clean ×5/2 scalar chain **breaks at the first odd b**: 621 → next
2-block reset is 1090, not ⌊5·621/2⌋+6 = 1558, and the preceding 3-block config is `[1,308,470]` — not
the `[1,b,b/2+2]` shape (b odd makes b/2 non-integral). So SN's reset recursion is **parity-branching**
(genuine 2-adic generalized-Collatz structure, not a single affine law) — this sharpens, and is
consistent with, the B2/reachability call of `CRYPTID_2D_CLASSIFICATION_2026-07-05.md` and the
"irregular off the clean phase" caveat of `CATALOGUE_O13_SN.md`.

**o13 margin census `[OBSERVED]`:** sweep-start run parity safe in **4654/4654** events (convention: run
including the D-entry cell always even ⟺ `REDUCE_O11_O16.md`'s run-excluding convention always odd =
safe; the two counts agree).

## 3. FATAL sets — `[PROVEN nonempty by run]` for all six (`msea_fatal.py`, replay `msea_replay.py`)

Standalone configs in the reachable-form family (captured real milestone state + head placement + gap
structure; block lengths mutated). **A halting mutant is a concrete fatal-set member; blank-tape
reachability is NOT claimed** — it is exactly the open protection.

| machine | family | halted / tried | smallest examples (independently replayed ✓) |
|---|---|---|---|
| o11 | `1^k 0 (10)^m`, state B @ R | **94/168** | `[2,(10)^1]` halts @19; `[2,(10)^4]` @81 |
| o12 | `1^a 0 1^b 0 (10)^m`, C @ L | **119/280** | `[2,1,1]` @50 |
| o13 | same, C @ L | **156/280** | `[2,1,1]` @171 |
| o14 | `[a,1,b,1^m,4,4,2]`, E @ L | **93/210** | `[2,1,1,1,1,4,4,2]` @222 |
| o16 | `[k,0²,1^m,d]`, A @ R | **162/250** | `[1,1,4]` @160 |
| SN  | `1^m`, C right of block | m ∈ **{1,3,6,7,15,31}** ≤ 32 | = binary all-ones ∪ {6} (re-confirms `cryptid_halt_gates_verify.py`) |

The contrast is the story: mutant fatality is **dense** (40–65%) while the blank orbits are perfectly
safe over every measured event — protection is seed-specific, as everywhere else in the family.

**o11's residue map `[OBSERVED]` (`msea_fatal_map.py`, `msea_o11_residue.py`) — the sharpest new
handle.** In the standalone family, rows **k ≡ 2 (mod 4) are fatal at every m tested (m=1..16)**;
k ≡ 3 rows tested are safe; k ≡ 0,1 rows are quasi-periodically mixed in m. The real orbit's clean
milestones (40M steps, 24 events): epoch residues are locked by the −4 countdown, and the orbit has
visited **only k mod 4 ∈ {3, 0, 1} — never the all-fatal residue 2**. Milestone start = pure-collapse
value − 2 (26→24, 303→301), so on this data: **fatal refill draw ⟺ collapse value ≡ 0 (mod 4)**;
observed collapses 3,9,26,303 ≡ 3,1,2,3 — none ≡ 0. Within mixed rows the safe cells are threaded by
the sea's own `⌊3m/2⌋+4` residues (checked at the three real in-epoch points that land in mixed rows:
(4,65),(8,41),(12,25) all fall on observed-safe cells). Protection statement sketch: *the ×3/2 sea
orbit's residue itinerary and the doubly-exp refill orbit never jointly enter the fatal residue class* —
the (K)-species in refill-residue coordinates.

## 4. Species table (the deliverable rows)

| machine | species | (K)-seeded? | LEDGER MEMORY | protection sketch `[OPEN]` | margin snapshot |
|---|---|---|---|---|---|
| **o11** | **residue-ledger** (refill-residue variant) | **yes** (×3/2 inner, exact +4 feed) | **RESETTING** (each refill re-seeds sea m=2; epoch residue = fresh draw) | collapse value never ≡ 0 (mod 4), and in-epoch (k,m) joint residues stay in safe cells | 4 refill draws observed, all safe; naive annealed p* ~ 1/4 per refill `[MODEL]` — but refills doubly-exp sparse (5th at ≳10¹³ steps) |
| **o12** | residue-ledger (joint (a,b) residues, no single fatal row) | yes (×3/2, c=3δ−1) | RESETTING (collapse re-seeds `[a′,4]`) | the (a,b,δ)-itinerary avoids the quasi-periodic fatal cells | 0/5,238 gate exposures unsafe; interior 00 exists (max 1) — protection strictly head-local |
| **o13** | residue-ledger, **parity-gate variant** (o10-twin) | yes (×3/2, c=3δ+1 — NEW) | RESETTING | every eat-sweep run lands safe-parity (4654/4654) | distance-to-fatal = one parity flip at every sweep (o17-like in value, per-sweep) |
| **o14** | residue-ledger (+ accreting marker) | yes (×3/2, c=+6 single — NEW) | RESETTING | joint (a,b) residues; marker tail `(4,4,2)` stable in 3750/3857 gens | permanent interior 00 (min=max=1) sits off the sweep path — head-locality is the whole protection |
| **o16** | residue-ledger in the **tower-sparse-gate costume** | yes (×3/2 sea) | RESETTING | gate touched only at doubly-exp refills (15/12M); refill phase race won by the leading-block exit every time | rarest exposure in the family; k-countdown −1 with one observed +24 refill |
| **SN** | **string-ledger** (cylinder avoidance in **base-2**) over a ×5/2 scalar | **NO** — own kernel μ=5/2 ∉ 2^a/3^b ((K)-species-*shaped*, not (K)-seeded) | **CUMULATIVE** (the scalar persists across resets; no re-seed) | the parity-branching reset orbit never enters the all-ones-adjacent binary cylinder {1,3,6,7,15,31,…} | fatal set is measure-thin in value space: P(fatal) per reset decays ~2^−b `[MODEL]` — annealed **non**-halt-leaning, o4-side of the memory axis |
| *(o15)* | *string-ledger — already classified; one table with o18* | *(×8/3 family)* | *RESETTING* | *quoted from `O15_TEMPLATE_PORT` / `O15_O18_IDENTITY` — not re-run* | — |

## 5. Consequences for the map

1. **The LEDGER-MEMORY axis extends cleanly and non-trivially.** The five sea machines all land on the
   RESETTING side (o15/o18's side): every refill wipes the epoch, so the annealed model gives a constant
   per-refill fatal probability ⇒ **annealed halt-leaning** `[MODEL, never a machine claim]` — with o11's
   naive p* ~ 1/4 the largest in the analyzed frontier (vs o18's 3.9×10⁻⁴²). What saves them
   observationally is the OTHER axis: refills are doubly-exponentially sparse in time, so the annealed
   horizon is tower-scale. SN lands alone on the CUMULATIVE side among the new six: its growing scalar
   suppresses fatality geometrically — the annealed lean splits exactly along the memory axis, as it did
   for o4/o3 vs o15/o18.
2. **(K)-seeding census:** o11, o12, o13, o14, o16 are (K)-seeded (Mahler-3/2 inner engines — with the
   sea/refill costume on top, they stand or fall with ×3/2 residue equidistribution). SN is the family's
   one non-(K) kernel (μ=5/2): the same species *shape* (string-ledger) instantiated on a different
   Mahler orbit — evidence that the five-shape species set is kernel-independent.
3. **Decision-adjacency:** none is decision-adjacent in o18's sense (no closed rewrite grammar). The two
   most attackable handles found: **o11's refill-residue condition** (a single mod-4 statement about an
   explicit doubly-exp orbit — but that orbit is itself Mahler-hard, so this is a re-coordinatization,
   not a reduction in difficulty) and **o13's parity predicate** (the cleanest scalar-free gate, o10's
   structural twin). SN's parity-branching reset recursion (§2) makes it strictly generalized-Collatz —
   B2 confirmed, no decidability route visible.
4. **Everything found matches the meta-facts of the species synthesis:** gates never the obstruction;
   fatal sets real and dense in the standalone family; protections orbit-specific quenched statements —
   now in two more coordinates (refill residues; binary cylinders at multiplier 5/2).

## 6. Honest scope

- Gate reductions `[PROVEN from table]` (re-verified mechanically); censuses/laws `[OBSERVED]` on the
  stated runs and generation grids — the counter laws are exact on 15–25 consecutive generations with
  the misses at epoch boundaries, and are NOT promoted (no certified templates were built here; this is
  survey depth, the o4 pinning standard was not run).
- Fatal configs `[PROVEN by run]` (concrete halts, independently replayed 6/6); **blank-tape
  reachability is not claimed for any**. o11's "k≡2 (mod 4) all-fatal" is `[OBSERVED]` on m=1..16, not a
  theorem; the collapse-offset (−2) rests on 2 observed refills.
- Annealed leans are `[MODEL]` heuristics, cited only as model facts.
- **All six protections are `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
`msea_gate.py [N]` (gate + window census) · `msea_struct.py` (v1, trigger-event granularity — kept as
the negative control showing the wrong-event failure) · `msea_struct2.py [N]` / `msea_struct3.py [N]`
(milestone templates + laws) · `msea_fatal.py` (fatal probe) · `msea_fatal_map.py` (residue maps) ·
`msea_o11_residue.py [N]` (o11 real-orbit residues) · `msea_replay.py` (independent confirmation).
Basis: `MAHLER_HALT_GATES_2026-07-04.md`, `CATALOGUE_IRREGULAR.md`, `CATALOGUE_O7_O12.md`,
`CATALOGUE_O13_SN.md`, `REDUCE_O11_O16.md`, `CRYPTID_2D_CLASSIFICATION_2026-07-05.md`,
`BB6_CRYPTID_SPECIES_2026-07-07.md`.
