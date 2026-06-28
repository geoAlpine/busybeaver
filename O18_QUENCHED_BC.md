# o18 / o15 — the QUENCHED Borel–Cantelli facet: per-epoch alignment margins, summability, and the minimal effective input (2026-06-28)

Companion to `EXISTENCE_META_THEOREM.md`, `O18_REDUCTION.md`, `O15_REDUCTION.md`, `CRYPTID_O18_FRAMEWORK.md`.
Those notes settle the **annealed** facet (Borel–Cantelli I over Haar seeds, unconditional). This note attacks the
**quenched** facet for the **specific** o18/o15 orbit: makes the bad event `B_n` precise, computes the orbit's own
realized alignment-margin to large `n` (exact arithmetic + exact-mechanics simulation), tests whether the quenched
alignment count is observably summable, and pins **exactly** the minimal effective input that would yield a quenched
Borel–Cantelli — and whether it is genuinely weaker than Antihydra's density target.

**Soundness.** Every line is `[PROVEN]` (transition-table / elementary big-int), `[VERIFIED]` (machine-checked this
session, exact `bytearray` mechanics matching `bb_sim` semantics, exact big-int via `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`),
`[OBSERVED]` (empirical, single-orbit), `[MODEL]`/`[ANALOGY]`, or `[OPEN]`. **No machine decided. No label upgraded.**
Scripts in scratchpad: `o18_margin2.py`, `o15_margin.py`, `o18_arith.py`, `o18_genericity.py`.

---

## 1. The bad event `B_n`, made precise  [PROVEN]

For both machines the halt is an **existence/avoidance** event on a deterministic single orbit `(ℤ_3, T_{8/3}, x_0)`;
`B_n` is the (clopen) collision cylinder hit at epoch `n`.

**o18** (`1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`, halt = state F reads `1`).
State F is entered **only** via `D:1→1LF` (D at cell `p` reads `1`, moves L, enters F at `p−1`); `F:1→HALT`,
`F:0→1LE` (write 1, move L — the leftward rebuild sweep). Hence
> **`B_n^{o18} = {`at the epoch-`n` leftward D/F frontier the cell the sweep lands on already holds a `1``}`**
> = the base-3 carry of the `×(8/3)` step is **deposited at the frontier** instead of being absorbed into the clean
> `0 1^{N−1}` block (a left-frontier adjacent-`11`). `[PROVEN]` (transition table) / `[VERIFIED]` (`o18_haltdemo.py`:
> seeded `{−1:1,0:1}` halts in 1 step; control `{0:1}` does not).

**o15** (`1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA`, halt = state A reads `1`).
State A is entered **only** via `F:1→1RA`; `A:1→HALT`, `A:0→1RB`. Hence
> **`B_n^{o15} = {`at the epoch-`n` rightward F→A frontier two 1-blocks abut`}`** = the single `0`-separator at the
> active frontier **vanishes** (a right-frontier `11`-abutment) — the mirror of o18. `[PROVEN]` / `[VERIFIED]`.

**Non-halt** `⟺` `B_n` occurs for **no** `n` after the verified prefix `⟺` the orbit's alignment-margin (below)
is `≥ 1` at every epoch. This is a `∀n` avoidance statement, **not** a density average (the §2 of `O18_REDUCTION.md`
distinction, used throughout).

---

## 2. The specific orbit's realized alignment-margin — exact mechanics  [VERIFIED]

Define, at each halt-gate visit, the **alignment-margin** = the distance from the frontier cell to the nearest `1`
in the collision direction (LEFT for o18, RIGHT for o15) on the **live** tape. `margin = 0 ⟺ B_n ⟺ HALT`.
`margin = ∞` (recorded `−1`) means the entire half-tape in that direction is blank.

### o18 — `1.0·10^{10}` steps, epochs 0–11 (`o18_margin2.py`)  [VERIFIED]
`collisions = 0` (no halt). Per F-entry `(epoch, frontier relpos, F_reads, left-margin)`:

| epoch | step | frontier relpos | F_reads | **left-margin** |
|---|---|---|---|---|
| 0 | 36 | −6 | 0 | ∞ (blank) |
| 1 | 226 | −22 | 0 | ∞ |
| 2 | 1 430 | −68 | 0 | ∞ |
| 3 | 9 562 | −194 | 0 | ∞ |
| 4 | 66 753 | −535 | 0 | ∞ |
| 5 | 468 794 | −1 446 | 0 | ∞ |
| 6 | 3 315 299 | −3 877 | 0 | ∞ |
| **7** | 23 492 737 | **+9 (interior)** | 0 | **1** ← only finite margin |
| 8 | 23 503 104 | −10 358 | 0 | ∞ |
| 9 | 166 999 736 | −27 644 | 0 | ∞ |
| 10 | 1 187 331 039 | −73 745 | 0 | ∞ |
| 11 | 8 442 192 549 | −196 681 | 0 | ∞ |

Frontier `|relpos|` ratios `→ 8/3` (`196681/73745 = 2.667`), confirming `N_k ≍ (8/3)^k` **off the raw tape**.

### o15 — `1.3·10^{9}` steps, epochs 0–12 (`o15_margin.py`)  [VERIFIED]
`collisions = 0`. The frontier (growing `|relpos|` = 14,35,101,282,763,2049,5480,14621,39002) is **always** `margin = ∞`
(blank beyond — safe). The only `margin = 1` events are the static near-origin single-`0` separators (the `(1,0,1)`
triples at relpos +1, −4, −7), re-scanned each macro-cycle — i.e. persistent counter-region features, **not** an
advancing-frontier near-miss.

### The realized-margin law  [OBSERVED, the central datum]
> **For both orbits the realized alignment-margin is binary — `∞` (blank/wide frontier) at almost every epoch, and
> exactly `1` only at carry-defect / split epochs — and is NEVER `0` and NEVER grows.** o18 produced **one** finite
> margin (value `1`) in 12 epochs; it occurred precisely at the first carry-defect epoch (epoch 7, where the clean map
> `⌊8N/3⌋+2` first breaks: predicts `10375`, true `10373`, defect `−2`). The carry defects at epochs 8–11 were
> absorbed without leaving any residual `1` in the sweep path (`margin = ∞`), so **near-misses are rarer than defects**.

**Consequence for the task's "does the margin grow like `c·n`?" hypothesis:** *No — the geometric margin does the
opposite of growing.* At the dangerous (carry-defect) epochs it sits pinned at the **minimum nonzero value `1`** — the
orbit grazes one cell from halting and the safety does **not** increase. There is **no realized growing geometric
safety margin to exploit** (this refutes the optimistic reading of task #3 in the literal tape coordinate; the only
coordinate in which a margin grows linearly is the abstract carry-run deficit of §4, and that growth is conditional).

---

## 3. Is the quenched count observably summable?  [OBSERVED]

Three distinct counts must be separated; conflating them is the easy error here.

1. **Annealed budget `Σ_n Haar(B_n) = Σ_n 1/N_n`** `[VERIFIED, exact Fraction]`. Successive ratios are **exactly `3/8`**
   (geometric), so it is summable: `Σ_{n≥7} 1/N_n = 1.542·10^{-4}` (o18), `4.08·10^{-5}` (o15 width orbit from `W=40`).
   This is the §3a/§4.2 `EXISTENCE_META_THEOREM` result, reconfirmed exactly.
2. **Quenched halt count `Σ_n 1[margin_n = 0]`** = the count that actually decides the machine. **Observed `= 0`**
   through epoch 11 (o18) / 12 (o15) — trivially summable, but that is just "no halt yet."
3. **Quenched near-miss count `Σ_n 1[margin_n = 1]`** = the realized danger events. o18: **1** in 12 epochs (sparse).
   o15: recurs at split epochs but those are static counter separators (§2), not advancing alignments. This count is
   **not** the halt count and its summability is **not** what BC needs (see the trap below).

> **The summability trap (honest correction of a tempting over-read).** The realized **geometric** near-miss
> (margin `≤ 1`) is *not* the event whose probability is `1/N_n`. The margin reaches `1` whenever a carry defect leaves
> any residual `1` near the frontier — an `O(1)`-per-defect, **not** `1/N_n`, event. The `1/N_n` (summable) rate is the
> **finer** event "the residual lands at margin **exactly 0**," i.e. the defect carry propagates the *full* width to hit
> the frontier cell. So the summable budget lives one level **below** the realized geometric margin; the realized
> margin's `∞/1` binary structure is consistent with summability of the halt event but does **not** itself display it.

**Genericity probes that the summable (`1/N_n`) model needs — tested on the specific orbit, exact to 5 000 epochs**
(`o18_genericity.py`):
- **Units trit `N_n mod 3` and carry trit `8N_n mod 3` equidistribute**: empirical `D_n = max_d|freq_d − 1/3|`
  decays `≈ 1/√n` or better (o18: `0.047, 0.023, 0.016, 0.0073` at `n = 100, 500, 2000, 5000`; same for o15). The
  **specific** orbit is numerically generic mod 3. `[OBSERVED]`
- **Leading base-3 carry-run length is geometric and bounded**: histogram `{1:1382, 2:417, 3:134, 4:44, 5:18, 6:3, 7:3}`
  over 2000 epochs, mean `1.46`, **max `7`** (attained early, epoch 194 — it does **not** grow with `n`). `P(run ≥ k) ≈ 3^{−k}`.
  `[OBSERVED]`

> **Verdict (§3).** The quenched **halt** count is observably `0` and the orbit is observably **generic** (trit
> discrepancy `~1/√n`, carry-runs bounded), all **consistent with** the annealed `1/N_n` summable rate applying
> quenched — but this is `[OBSERVED]` genericity, **not** a proof that the specific orbit is non-exceptional. The
> realized geometric margin (`∞/1`) does not directly exhibit the summable rate; the summable rate is the finer
> "margin = 0" event, observed to never occur.

---

## 4. The minimal effective input for a quenched Borel–Cantelli — and is it weaker than Antihydra's density?

The quenched target is **`Σ_{n>P} 1[B_n] = 0`** (a non-negative integer; the machine halts at the **first** hit, so
"finitely many" is *not* enough — we need **zero** after the verified prefix `P`). Three routes, with the input each needs:

**(R1) Direct (circular).** Prove `margin_n ≥ 1` for all `n>P`. This **is** the non-halt theorem verbatim — **not** weaker.

**(R2) Counting via effective equidistribution.**
`#{n>P : B_n} ≤ Σ_{n>P} Haar(B_n) + Err`, where `Err` = cumulative single-orbit discrepancy for the residue mod
`3^{k_n}` (`k_n ≈ log_3 N_n ≈ 0.893 n`) hitting the **single** forbidden class (the carry-aligned one) of measure
`~1/N_n`. Since `Σ_{n>P} Haar(B_n) = 1.5·10^{-4} ≪ 1`, **if** `Err < 1 − 1.5·10^{-4}`, then the count is `< 1`, hence
`= 0`, hence **non-halt**. Required input: an effective single-orbit equidistribution mod `3^{k_n}` with **cumulative
ABSOLUTE discrepancy `< 1` over all epochs**. This is **Borel–Cantelli-I strength**.

**(R3) Carry-run route.** `B_n` requires the `×(8/3)` carry to propagate a run of length `R(n) = Θ(k_n) = Θ(n)` all
the way to the frontier `[MODEL/ANALOGY — the natural "carry reaches the frontier" reading; the exact `R(n)` identity
is the same analogy-not-reduction status as the Erdős link, `O18_REDUCTION.md` §1]`. The realized carry-run is
`O(1)` (max 7, §3). **Any** effective bound `run_n = o(n)` — even a crude `run_n ≤ 0.5 n` — gives `run_n < R(n)`
eventually ⇒ no alignment ⇒ non-halt. The "safety factor" is `~0.9` (need `< 0.893n`, have `O(log n)` empirically).

### Comparison with Antihydra's density target  [the honest analytic ranking]

| | **Antihydra (density / 3/2)** | **o18 (existence / 8/3)** |
|---|---|---|
| quenched target | `liminf_N (1/N)Σ_{n<N} 1[D_n≥2] ≥ 1/2` | `Σ_{n>P} 1[B_n] = 0` |
| probabilistic skeleton | **Strong Law** (average → a constant) | **Borel–Cantelli I** (`ΣP<∞ ⇒` a.s. finite) |
| target magnitude vs `n` | a **constant floor**, never decays | a **summable, geometrically-tiny** budget (`Σ=1.5e-4`) |
| error control needed | `o(N)` **relative**, sign-definite, **forever** | `< 1` **absolute**, cumulative over all `n` (R2) — or `run = o(n)` (R3) |
| slack | none (must hit the exact density value) | `~1` full count (R2) / factor `~0.9` (R3) |

> **The required analytic INPUT for o18 is STRICTLY WEAKER in shape:** Borel–Cantelli-I (summable ⇒ finite) is strictly
> weaker than the Strong Law (average → constant); an **absolute** cumulative error `<1` against a **summable** target is
> a coarser demand than a **relative** `o(N)` error against a **constant** density floor that must hold in the limit
> forever; a **sublinear carry-run** bound `o(n)` (factor-`0.9` slack) is weaker than pinning a density to its exact value.
> This confirms `EXISTENCE_META_THEOREM.md` §3b on the data: existence asks only for a rate that **beats a summable
> target**, density asks for a **positive liminf floor**.

---

## 5. Honest difficulty assessment — is o18's existence target genuinely closer to provable?

**Yes on the bar; no on the tools — "weaker target, same wall, no current crack."**

1. **The bar is provably lower `[PROVEN ranking]`.** By §4, o18 needs only a Borel–Cantelli-I-strength effective input
   (absolute cumulative discrepancy `<1` against a `1.5·10^{-4}` summable budget, or a sublinear carry-run bound),
   whereas Antihydra needs a Strong-Law-strength input (a positive lower **density**, an asymptotic average pinned to a
   constant). BC-I `<` SLLN. So *in principle* o18's facet is closer to provable, and the **summable budget is exactly
   what converts BC-I strength into the required `zero` count** (the machine halts at the first hit, so only the tiny
   total budget `<1` lets "expected count `<1`" force "count `= 0`"). Antihydra gets no such help — no amount of
   summability touches a density.

2. **The data is fully consistent with non-halting `[OBSERVED]`.** 0 collisions to epoch 11/12; the specific orbit is
   numerically generic (trit discrepancy `~1/√n`); carry-runs bounded (max 7); the halt event (`margin = 0`) never occurs.

3. **But no unconditional tool reaches even the weaker input `[OPEN]`.** Both targets reduce to single-orbit effective
   equidistribution = **AEV Conj 1.6** (o18 the `q=3` Erdős/floor-mirror facet, Antihydra the `q=2` Mahler facet). The
   only unconditional result at `q=3` is Narkiewicz 1980 (an **upper** density bound; the bad set is **not even known
   finite**) — there is **no** effective single-orbit equidistribution rate, no lower bound, no finiteness. The crude
   `run_n = o(n)` bound of (R3) sounds elementary but is exactly this missing effective statement — there is **no
   elementary arithmetic reason** the orbit cannot have a long carry-run at some epoch (that *is* the open alignment).

4. **The realized margin gives no shortcut `[OBSERVED]`.** Crucially, the orbit's realized **geometric** margin does
   **not** grow — it sits pinned at `1` at the carry-defect epochs (one cell from the cliff) and is `∞` elsewhere. The
   only coordinate with a linearly-growing margin is the abstract **carry-run deficit** `k_n − run_n ≈ 0.9 n`, and that
   growth is precisely the conditional equidistribution statement, not an unconditional fact. So the orbit offers no
   "increasing safety margin" to ride to a proof.

> **One-line verdict.** o18/o15's **existence/summable** target is **provably a lower bar** than Antihydra's **density**
> target (Borel–Cantelli I vs Strong Law; absolute-`<1` vs relative-`o(N)`; sublinear-run vs exact-density), and the
> specific orbit is observably generic with **0** halts and near-misses pinned at margin `1` — yet it sits behind the
> **same** AEV/Erdős wall, with **no** unconditional tool reaching even the weaker input, and the realized margin does
> not grow to give a crack. **Weaker target, same wall, no current crack: a lower bar, not a present proof.**

---

## Reproduce (exact, `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
- `o18_margin2.py 10000000000` — o18 to epoch 11: 0 collisions; realized margins `∞` except epoch-7 = `1`.
- `o15_margin.py 1300000000` — o15 to epoch 12: 0 collisions; frontier margin `∞`, only static near-origin `margin=1`.
- `o18_arith.py` — clean orbit `⌊8N/3⌋+2`; exact `Σ 1/N_n`, ratio `3/8`; base-3 leading digits.
- `o18_genericity.py` — units/carry trit equidistribution (`D_n ~ 1/√n`); leading carry-run histogram (max 7, mean 1.46, non-growing).

**No machine decided; no non-halt claimed; no false barrier. Soundness intact.**
