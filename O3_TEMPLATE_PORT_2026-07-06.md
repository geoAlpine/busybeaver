# o3 template port — the o4 pipeline replicates FULLY; o3's generation is a rigid certified template; the counter system is a DETERMINISTIC (a,k) arithmetic map with genuine halting configs at the small-k floor (2026-07-06)

*Porting the o4 certified trace-template method (`O4_TEMPLATE_CLOSURE_2026-07-06.md`) to **o3**
(`1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC`, blank tape; halt = state F reads 0; spec confirmed identically in
`o3_transducer.py`, `cryptid_halt_gates_verify.py`, `suite.py`, `catalogue_finish.py`). **Verdict (a): the template
closes, the ledger is extracted** — and it is *sharper* than o4's: the whole generation map collapses to a
deterministic integer map on two counters `(a,k)`, with an explicit fatal set and standalone HALTING configurations
(the `Z(41,3,0)` analogues). A previous `[OBSERVED]` claim (`O3_TRANSDUCER.md` §4: Δk "core-hard, history-dependent")
is **CORRECTED**: Δk is exactly determined by `a mod 3` (resp. `a mod 9` at the k=1 floor). o3 stays `[OPEN]` — the
residual is the same species as o4's: a one-sided ledger over the residue sequence of a base-4/3 odometer, with an
enormous empirical margin. No machine decided.*

## 0. Ground truth `[PROVEN from table / verified concrete]` (`o3_ground_truth.py`)
- **Halt gate:** F is entered ONLY by `E,0→1RF`; `F,0`=HALT, `F,1→0RC`. So **HALT ⟺ E reads a 0 whose right
  neighbour is 0** `[PROVEN from table]` (confirms `O3_TRANSDUCER.md`). o3's local safety condition = "E-reads-0
  always has right neighbour 1" (the analogue of o4's "F never reads 1").
- **Window saturation (concrete, 50M steps, no acceleration):** 1,666,179 E-reads-0 events, **0 unsafe**; window
  sets saturate at radius 3/4/5 with **3/5/6** windows, the last new window at step **1,370** (0.00% of the run),
  all safe. Saturation is even sharper than o4's.

## 1. Structure discovery `[OBSERVED]` (`o3_structure.py`, `o3_template_scan.py`, `o3_chunk_geometry.py`)
- **Sweep cycles differ from o4's p=2** (detected from microstep logs, as required): rightward crawl **p=10,
  D=+6** (`A0 B0 C1 B1 E1 A0 B1 E0 F1 C0` — contains one safe E-reads-0 per unit), leftward crawl **p=20, D=−6**,
  zigzag **p=6, D=−2**, plus two p=3 transients. (A first scan with p≤6-only compression made every chunk hash
  distinct; raising to minimal-period p≤24 collapsed 2,135 hashes → **11**. The apparent "self-similar, non-periodic
  template" was an artifact of missing the super-cycles.)
- **Milestone form (exact, from raw dumps):** `M(a,k) = 0^∞ [head, state A] 0 0 (10)^a (110)^k 0^∞` — the digit
  string `0^a 1^k` of `O3_TRANSDUCER.md`; `a` = #single-1 blocks, `k` = trailing marker of 11-blocks. Width
  `2(a+k)+k+2` ✓.
- **Generation mechanics:** the marker emits one defect (`11` block) which is transported LEFT 3 digits per
  milestone chunk (tape: defect −8 cells/chunk, frontier −2/chunk, T(chunk)=10j+4 at defect distance j); the head
  shuttles frontier↔defect only; the right side is untouched all generation.
- **Template:** every generation's chunk-hash sequence is EXACTLY **prefix(class) · body^r · suffix(3 fixed
  chunks)** — body hash `e95b0216a8` = 6,914 of 7,025 chunks over 120M steps; prefix classes are pinned to
  `a mod 3`; `r=(a−11)/3` (a≡2) / `(a−9)/3` (a≡0), exact over all 33 observed generations.

## 2. The certified BODY lemma `[PROVEN]` (`o3_body_proof.py`)
For all `j ≥ 12`, `j ≡ 0 (mod 3)` (the reachable transport phase; emission aligns the crawl phase — the analogue of
o4's odd-k cone):
> `B(j): 0^∞ [A] 0 0 (10)^j 1 1 …  →  shift(−2) of B(j−3)` with the vacated 8 cells becoming gap fabric, in
> **exactly 10j+4 steps**, head span `⊆ [−2, 2j+3]`, every E-reads-0 safe, no halt.
Verified by the full o4 method on j ∈ {12,…,33,51,99,150,249,**501**}: compressed **skeleton identical** (6 episodes,
3 sweeps), **sweep lengths exactly affine** (j/3, 3, j/3−1), **episode-landmark pinning** (all episode steps at
offsets ≤7 from frontier/defect, offset vectors identical across the grid — the red-team lemma), **cycle
certificates** for all three sweep cycles (2-cycle translation-invariance verified by construction — sound induction
for a deterministic TM), and exact landing/step-count/safety. **LOCALITY:** span ≤ [−2, 2j+3] means nothing right of
the defect block is ever read ⇒ the lemma composes under arbitrary right context (gap+marker). The j≡1/j≡2 phases
are NOT reachable mid-generation; they are the marker-meeting chunks (cascade/deposit) — measured separately.

## 3. The generation law — verified exactly; the DERIVED odometer `[PROVEN on grid + template]` (`o3_gen_proof.py`)
Standalone `M(a,k)` run pure-concrete to the next milestone, grid a=12..302 (all residues), k=1,2,3,5,8
(+ large-k spot checks k=50 at a=150..152 and k=120 at a=60..62, incl. k≫a — all exact):
| class | law | grid result |
|---|---|---|
| `a≡1 (mod 3)` | `M(a,k) → M(a−1, k+2)` (marker cascade, ONE chunk) | exact, 0 exceptions |
| `a≡2 (mod 3)` | `M(a,k) → M((4a+4)/3, k+1)` | exact, 0 exceptions (k≥1) |
| `a≡0 (mod 3)`, k≥2 | `M(a,k) → M(4a/3+3, k−1)` | exact, 0 exceptions |
| `a≡0`, **k=1** | a≡3 (9): `→M(4a/3+2, 2)`; a≡0 (9): `→M(4a/3+3, 1)`; **a≡6 (9): HALTS** | exact, a=12..129, 300, 999–1005 |
| **k=0** | a≡0: `→M(a,1)`; a≡1: `→M(a−1,2)`; **a≡2: HALTS** | exact, a=6..59, 300–302 |
All non-halting runs: **unsafe=0**; chunk-hash signature = prefix(class)·body^r·suffix with r exactly affine
(`r=(a−11)/3` / `(a−9)/3`). **Template uniformity (measured exactly):** at fixed k the signature is a single fixed
word per class across a=22..302 (a≡2: `6fe78392ca·body^r·suffix4`; a≡0: `body^r·suffix4`, same 4 suffix chunks;
a≡1: one chunk `f9fc752fc7`); across k=2..12 the signatures are k-INDEPENDENT except one k=2 prefix variant at a≡2
(landing law identical) — exactly o4's per-small-parameter restatement. `a′=⌊4a/3⌋+c` **derives** from the template
velocities (defect −3 digits/chunk, gap +4 digits/chunk), exactly as o4's odometer fell out of its templates.
**Boundary-chunk landmark pinning `[VERIFIED]` (`o3_boundary_pinning.py`):** every episode step of every boundary
chunk (cascade a≡1: 5 episodes; a≡2 prefix+suffix: 136; a≡0 suffix: 107) sits at a grid-INDEPENDENT offset (≤10)
from a structural landmark (frontier / defect / marker start / right end), with the (landmark,offset) vectors and
skeletons IDENTICAL across a=22..302, k=2..12 — the o4 red-team generalization step, applied to the boundary
pieces. Labels: law rows `[PROVEN]` on the grids by exact concrete simulation; parameter-uniformity by body lemma
`[PROVEN]` + certified sweep cycles + pinned episode skeletons — the same closure standard as
`O4_TEMPLATE_CLOSURE`.

## 4. THE DISCOVERY — genuine halting configs + a CORRECTION to the prior census
- **Standalone halting configurations (o4's `Z(41,3,0)` analogues), `[verified concrete]`:**
  `M(a,0)` HALTS for every tested `a≡2 (mod 3)` (a=8,…,29: halt in ~10a/3 steps, one unsafe E-read);
  `M(a,1)` HALTS for every tested `a≡6 (mod 9)` (a=15,24,…,123 — 13/13 — **plus the a-priori PREDICTED halts
  M(1005,1) at step 1,694,235 and M(302,0), both confirmed exactly**). The small-k floor is genuinely fatal; the
  safety condition is NOT vacuous. (Standalone; NOT claimed reachable from blank tape.)
- **CORRECTION of `O3_TRANSDUCER.md` §4 `[OBSERVED]` claim:** Δk is **not** history-dependent/core-hard — it is
  **exactly `δ(a mod 3) = {1:+2, 2:+1, 0:−1}`** (and `a mod 9` at k=1). The earlier ambiguity came from testing only
  `(k mod 2, len mod 2)`-type features, never `a mod 3`, and from mixing cascade and emission events in one marker
  sequence. o3's counter map IS a base-4/3 odometer variant (as `CRYPTID_BOUNDARY_GRAPH_CENSUS` suspected) — with
  the roles swapped vs o4: **`a` is the odometer, `k` is the ledger.**

## 5. The ledger `[the irreducible core]` (`o3_ledger.py`)
The full system is a **deterministic integer map** on `(a,k)` (table above). `(a,k)` is a COMPLETE state: the
milestone tape is exactly `build_M(a,k)` — verified on the real orbit (blank-tape step 8,188 equals constructed
`M(60,6)` cell-for-cell), so there is no hidden state. The real orbit joins the map at `(6,2)` (concretely
verified; arithmetic iteration reproduces **all 30** concretely observed generations exactly).
- **o3 halts ⟺ the orbit of the map from (6,2) hits the fatal set** `{k=1 ∧ a≡6 (mod 9)} ∪ {k=0 ∧ a≡2 (mod 3)}`
  (⟸ direction `[PROVEN on the verified-law region]`; ⟺ modulo the same grid-uniformity caveat as §3).
- **Iterated exactly for 200,000 generations** (a reaches ~10^18,743): **no fatal hit**; min k at a drain event = 2
  (at generation 0); k drifts UP strongly (k≈49,658 at gen 200k). Exact orbit statistics: residue frequencies
  (a≡0,1,2) = (0.5009, 0.2500, 0.2492) — ½,¼,¼ (structural: every a≡1 cascade lands on ≡0) — giving net drift
  `−1·½ + 2·¼ + 1·¼ = +0.248/generation` (measured 0.24828); the longest ≡0-drain run in 200k generations is **10**,
  vs the k≈10⁴–10⁵ reservoir — failure needs a drain run of length ≈ k. Same species as o4's ledger; margin enormous.
- The residual `[OPEN]` conjecture: *the base-4/3 orbit `a ↦ ⌊4a/3⌋ + c(a mod 3)` (with the a≡1 cascade step) from
  a=6 never accumulates enough ≡0-drains to push k below 2* — Collatz-like, checkable, one-sided, with drift.

## 6. Macro-machine port `[tool, validated]` (`o3_bouncer_macro.py`)
Generic verified p-cycle jump engine (o4's p=2 jump generalized: state-return + word-repeat certificate on the live
tape, offline steady-state analysis → fresh-demand pattern / settled |D|-cell tiling / leading-edge profile with
steadiness check, margin, per-cycle event bookkeeping; refuses to jump on any anomaly). Validation battery:
**V1 PASSED** — exact tape/state/head/e0/unsafe equality vs concrete at 0.2M/1M/5M; **V2 PASSED** — E-reads-0
window-set (r=5) equality over 32M steps (6 windows, e0=1,066,338 exact, unsafe 0==0); **V3** — blank-tape milestone
stream (a,k) vs the arithmetic ledger orbit over a 200M-step run. Honest tool note: the generic-cycle engine's
speedup over concrete is modest (~5-10x; per-cycle Python bookkeeping), unlike o4's p=2 segment machine — adequate
for validation, not for deep-orbit exploration (the arithmetic ledger covers that). Used ONLY for discovery/
large-scale checks — every proof-path claim above is from pure concrete simulation on standalone configs.

## 7. Soundness ledger `[discipline]`
- All §2 lemma content: exact concrete simulation on constructed configs; no acceleration in the proof path.
- §3 laws: exact concrete on standalone milestone configs (grids as listed); §4 halts: exact concrete (each a
  standalone config, halt step observed); §5: exact bigint arithmetic of the verified map.
- Known gaps (honest): (i) the boundary-chunk pinning grids stop at a=302/k=12 (law spot-checked beyond: k=50,120,
  a to 1005); (ii) the k=1 law grid stops at a=1005; (iii) the blank-tape orbit provenance is raw-concrete to 120M
  steps (33 generations) + macro-validated beyond + arithmetic ledger; (iv) startup floor: the laws are verified
  from a≥6 (real orbit joins at (6,2)); a≤5 startup is concrete-verified as part of the 120M run.
- o3 `[OPEN]`. The decision reduces to §5's explicit ledger conjecture. **No machine decided. No label upgraded.**

## Reproduce
- `o3_ground_truth.py` (halt gate + window saturation, 50M), `o3_structure.py` (sweep census, milestones),
  `o3_template_scan.py` (chunk-hash template, 120M), `o3_chunk_geometry.py`/`o3_gen_dissect.py`/`o3_dump_tape.py`
  (mechanics), `o3_body_proof.py` (certified body lemma), `o3_gen_proof.py` (generation-law grid + fatal-config
  hunt), `o3_boundary_pinning.py` (boundary-chunk pinning certification), `o3_ledger.py` (arithmetic orbit, 200k
  generations), `o3_bouncer_macro.py` (validated macro).
- Interpreter: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`. Basis: `O4_TEMPLATE_CLOSURE_2026-07-06.md`,
  `O3_TRANSDUCER.md` (corrected in §4), `CRYPTID_BOUNDARY_GRAPH_CENSUS_2026-07-05.md`.
