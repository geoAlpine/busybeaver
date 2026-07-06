# o18 template port — the template closes at every reachable level, but the "ledger" is a 3-adic RECURSION TOWER with Collatz-irregular depth; a prior-note orbit claim is CORRECTED (3890 → 27660, not 10375) (2026-07-07)

*Porting the o4/o3 certified trace-template pipeline (`O4_TEMPLATE_CLOSURE_2026-07-06.md`,
`O3_TEMPLATE_PORT_2026-07-06.md`) to **o18** (`1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`, blank tape; halt =
F reads 1; spec confirmed identically in `suite.py`, `O18_NO_CERTIFICATE.md`, `CRYPTID_O18_FRAMEWORK.md`, all
`o18_*.py`). **Verdict: (c)+(b) — a FOURTH species.** Every piece of the o3/o4 decomposition that can be reached
is there (rigid template, certified sweeps, one complete integer counter, exact affine generation laws), but the
counter map is **not a finite-residue δ-map**: on `N ≡ 2 (mod 3)` the generation recurses through a
**self-similar 3-adic branch tower** whose depth is **Collatz-irregular** (not bounded by `v₃`), and the real
orbit enters the unclosed part of the tower at generation 11. Also: **no fatal configuration exists anywhere we
looked** — the o3/o4-style fatal set is EMPTY on every tested family. o18 stays `[OPEN]`. No machine decided.*

## 0. Ground truth `[PROVEN from table / verified concrete]` (`o18_ground_truth.py`)
- **Halt gate:** halt = `F,1`; F is entered ONLY by `D,1 → 1LF` (writes 1, moves L). So
  **HALT ⟺ D reads a 1 whose left neighbour is 1** `[PROVEN from table]` (confirms `O18_NO_CERTIFICATE.md` §3).
  Local safety condition: every D-read-of-1 has left neighbour 0.
- **Window census (concrete, 2·10⁷ steps, blank):** the gate fires **once per epoch** (7 events), all safe, and
  the radius-3/4/5 window census **saturates at ONE window** — `000[1]_D111` — at step 35. Sharpest saturation
  in the whole family (o3: 3/5/6 windows; o17: 11). Near-misses (`D` reads 0 with left 1): 3,092 interior.

## 1. Milestones + the counter `[PROVEN on observed prefix]` (`o18_milestones.py`)
Clean reset `C_N = 0^∞ [F] 0 1^{N-1} 0^∞`; the blank orbit joins at `C_10` (step 36). Every observed reset is
EXACTLY clean (interior zeros = 0, cell-for-cell = `build C_N`) ⇒ **N is a complete state at clean resets**.
Law `N' = ⌊8N/3⌋ + 2` exact for `N ≡ 0,1 (mod 3)` — but see §3 for `N ≡ 2`.

## 2. Level-0 template `[PROVEN on grid + live-tape cycle certificates]`
(`o18_template_scan.py`, `o18_body_dissect.py`, `o18_cycle_cert2.py`)
- Per-generation event stream (minimal-period compression, p≤24 — the o3 lesson — then level-2 shape
  compression) is EXACTLY **prefix(`F0 E0 C0`) · body^r · suffix**, ONE shape hash per class:
  `86b5cb350a` (N≡0,1 mod 3, 17 L2-tokens), `244ee6606a` (N≡2, 23 tokens, runs to the first dirty F-entry).
  Grid: all N=10..62, 99..104, 200-202, 300-302, 500-502, 1000-1003. **r exactly affine:**
  `(N−3)/3 / (N−4)/3 / (N−5)/3` per class; body = fixed 16-token word; sweep lengths affine (+4 per round trip).
- **Sweep cycle certificates (o3_bouncer_macro standard, live tape):** `[A0 B1]` (rightward, D=+2),
  `[A1 E1 B0 C0]` (leftward inverting, D=−2), `[C1 D0]` (leftward solidifying — the gate sweep, D=−2):
  interior cycles 100% self-similar under shift across the grid (≈20,100 + 19,802 + 399 cycles at N=300-302,
  zero divergences; 3-cycle episode margins at sweep ends). All non-halting runs: **unsafe = 0**.
- Note: `[C1 D0]` terminates in the suffix `C1 D1` — the D-read-of-1 that fires the gate. The gate is the
  termination event of the solidifying sweep; its safety is the termination CONTEXT of that sweep.

## 3. THE CORRECTION — `⌊8N/3⌋+2` is FALSE as the clean-reset map for `N ≡ 2 (mod 3)` (`o18_orbit_verify.py`)
`CRYPTID_O18_FRAMEWORK.md` §1 claimed `[VERIFIED] 10→28→76→204→546→1458→3890→10375→27668`. **Machine-checked
here: the real orbit goes `3890 → 27660`** (concrete, 163,684,437 steps, unsafe=0): the epoch passes through a
dirty F-entry at width 10,373 (one interior 0) which the old reset detector miscounted as the clean reset
"10375", and `27668 = f(10375)` was propagated from it. The `×8/3` rate is still right per SUB-epoch; the
clean-reset (complete-state) map is different on this class. Downstream framework identities (GAP lemma, Haar
analysis of `⌊8N/3⌋`) are unaffected as statements about the pure Mahler map, but their attachment to the
o18 orbit at `N≡2` steps needs re-derivation through the composite laws below.

## 4. The `N ≡ 2 (mod 3)` composite generation — the 3-adic recursion tower
(`o18_gen_proof.py`, `o18_mod9_law.py`, guarded re-census `o18_tower.py` — earlier two had wraparound risk at
large widths, all surviving claims re-verified with tape-edge guards)
- Sub-epoch 1 ends at a **dirty F-entry pair**: interior meet form `1^2 0 (1 0)^m 1^5`, then frontier form
  **`D₁ = [F] 1^{f(N)−10} 0 1^6`** (single 0-defect, 6 from the right end; verified m = f(N)−10 at
  N = 41, 200, 1001, 3890). Gate windows there:
  `10101[0]_F 11111` and `00000[0]_F 11111` — **F reads 0, safe, every observed time**.
- **Closed laws `[PROVEN on grids, exact concrete, 0 exceptions, unsafe=0]`:**
  | class | law | #F-entries | grid |
  |---|---|---|---|
  | `N≡2 (mod 9)` | `L=(64N−20)/9` | 3 | 28 members ≤1001, + real orbit 3890→27660 |
  | `N≡5 (mod 9)` | `L=(64N−104)/9` | 3 | 28 members, + **predict-confirm N=2003→14232** (43.3M steps) |
  | `N≡8 (mod 27)` | `L=(512N−1288)/27` | 4 | 10 members, + **predict-confirm N=305→5736** |
  | `N≡80 (mod 81)` | `L=(4096N−11618)/81` | 5 | N=80,161,242 |
  (predict-and-confirm = the o3 gold standard: landing computed from the law FIRST, then confirmed by fresh
  simulation.)
- **The deep branches are OPEN and genuinely irregular:** the natural hypothesis "recursion depth =
  `v₃(N+10)`" (suggested by the branch points 2→8→17≡−10 mod 27) is **REFUTED**: `N≡26,53 (mod 81)` members —
  including **N=26 itself** — run **>2.5·10⁸ steps without a clean reset** (≥7 recursion levels, while
  `v₃(26+10)=2`); `N≡17 (mod 27)` splits again mod 81/243 with only single-member fits so far. Depth is
  **Collatz-irregular** `[OBSERVED]`.
- **Self-similar dirty-form ladder** `[OBSERVED]`: level-k frontier forms
  `1^m 0 1^6 → 1^m 0 (10)^2 1^3 → 1^m 0 (10)^3 1 / 1^m 0 1 0 1^3 → … → 1^m 0 1^*` — the defect train encodes
  the pending tower levels; the head-side geometry is level-uniform in every observed form.

## 5. Ledger verdict — there is NO fatal set where we can see (`o18_ledger.py`, `o18_orbit_ledger.py`)
- **Fatal-config hunt:** the standalone defective family `B(m,e) = [F] 1^m 0 1^e` (the reachable dirty form is
  e=6), m=6..30,40,50 × e=0..10: **ZERO halting configurations** (contrast o3's `M(a,0)/M(a,1)` halters and
  o4's `Z(41,3,0)`). The `m≡2 (mod 3)` rows ignore the defect entirely. Every gate exposure in every run of
  this session (including the 163.7M- and 250M-step runs) was safe: **cumulative unsafe = 0 everywhere**.
- **Arithmetic orbit:** iterating the verified laws from N=10: generations 0..10 =
  `10,28,76,204,546,1458,3890,27660,73762,196700,1398744` — then **N₁₁ = 3,729,986 ≡ 17 (mod 81): the real
  orbit enters the UNCLOSED deep tower at generation 11.** The tower is not a parameter-space corner; it is
  on the orbit. (Branch usage so far: ≡0/≡1: 9, ≡2 mod 9: 1, ≡5 mod 9: 1, deep: 1.)

## 6. Species classification — a FOURTH kind
| o4-decomposition piece | o3/o4 | o17 | **o18** |
|---|---|---|---|
| local halt gate (proven, window-saturating) | YES | YES | **YES — 1 window** |
| rigid template prefix·body^r·suffix | YES | NO | **YES at every closed level** |
| complete O(1) counter state at milestones | YES (2 counters) | NO | **YES (1 counter)** |
| finite-residue δ-map / ledger | YES | NO | **NO — 3-adic branch tower, Collatz-irregular depth** |
| standalone fatal configs | YES (both) | family halters | **NONE FOUND** |
| drift/margin quantity | YES | none | **none needed so far — every level lands safely** |
o18 = **"self-similar 3-adic recursion-tower bouncer"**: o3/o4's rigidity at every level, o17's unbounded
recursion BETWEEN levels, and — unlike all three — **no known fatal region at all**. Its non-halt statement has
the form: *every level of the tower lands cleanly and safely* — a **level-induction** target, not a
count-vs-frequency ledger. If the level-k dirty-passage template can be certified uniformly in k (the dirty
forms are visibly self-similar), o18 would become the **most decision-adjacent cryptid in the family** — the
first place the program has seen where nothing fatal exists to avoid. That induction (and closing the ≡26/53
mod 81 branches, where single sub-epochs exceed 2.5·10⁸ steps) is the exact `[OPEN]` blocker.

## 7. Soundness ledger `[discipline]`
- Gate reduction: exhaustive table scan. All laws/templates: exact concrete simulation on standalone configs;
  no acceleration anywhere in this session.
- **Wraparound audit (this session):** `o18_gen_proof.py`/`o18_mod9_law.py` had pads too small for multi-epoch
  `≡2` growth (silent bytearray wraparound possible for N≳20 on those rows); **superseded by the guarded
  `o18_tower.py`** (raises on tape-edge approach); every claim above cites guarded or single-epoch runs only.
- Level-0 template: [PROVEN on grid] + live-tape cycle certificates; episode-landmark pinning at o4's standard
  NOT yet run (episodes here are ≤16 tokens with 3-cycle sweep margins — pinning is the natural next step).
- Deep-branch laws (mod 243+): single-member fits, `[OBSERVED]` only. Depth-irregularity: `[OBSERVED]`
  (budget-capped at 2.5·10⁸ steps/run).
- The absence of fatal configs is a NEGATIVE search result over the stated families/ranges, not a theorem.
- o18 `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce (interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
`o18_ground_truth.py` (gate + 20M census) · `o18_milestones.py` (resets, law, complete-state) ·
`o18_template_scan.py` (template + shape classes) · `o18_body_dissect.py` (body word, affine sweeps) ·
`o18_cycle_cert2.py` (live-tape cycle certificates; `o18_cycle_cert.py` = synthetic-tiling variant, one tiling
halts — the gate is live) · `o18_gen_proof.py`/`o18_mod9_law.py` (superseded, kept for the audit trail) ·
`o18_tower.py` (guarded tower census; output in scratchpad `o18_tower_out.txt`) · `o18_orbit_verify.py`
(3890→27660, the correction) · `o18_ledger.py` (B(m,e) fatal hunt) · `o18_orbit_ledger.py` (arithmetic orbit +
predict-confirm). Basis: `O4_TEMPLATE_CLOSURE_2026-07-06.md`, `O3_TEMPLATE_PORT_2026-07-06.md`,
`O18_NO_CERTIFICATE.md`, `CRYPTID_O18_FRAMEWORK.md` (corrected in §3), `O17_HALT_FLAVOR_2026-07-06.md`.
