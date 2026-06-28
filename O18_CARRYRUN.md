# o18 — the leading base-3 carry-run: exact recursion, growth, and whether the linear bound `run_n < 0.893 n` is unconditional (2026-06-28)

Attacks the `(R3)` sufficient input of `O18_QUENCHED_BC.md` §4: *if* the leading base-3 carry-run length
`run_n` of the orbit is `< 0.893 n` for all large `n`, then quenched Borel–Cantelli-I closes and o18 is
non-halting. The realized run is `O(log n)`. This note (i) defines `run_n` exactly, computes it to large `n`,
(ii) derives its **exact recursion** (a circle rotation / shrinking-target law), (iii) tests every unconditional
counting / 3-adic-valuation route against the **exact constant**, and (iv) gives the honest verdict.

**Soundness.** `[PROVEN]` = elementary arithmetic; `[VERIFIED]` = machine-checked this session, exact big-int
via `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`; `[OBSERVED]` = empirical single-orbit; `[MODEL]`/`[ANALOGY]`;
`[OPEN]`. **No machine decided, no label upgraded, no non-halt claimed.**
Scripts (scratchpad): `o18_carryrun.py`, `o18_rotation.py` (plus prior `o18_genericity.py`, `o18_arith.py`).

---

## 1. The carry-run, defined exactly, and its realized growth  [VERIFIED]

Orbit `N_{n+1} = ⌊8N_n/3⌋ + 2`, `N_0 = 10`. Write `N_n` in base 3 with `k_n = ⌊log_3 N_n⌋ + 1` trits.

> **Definition (leading carry-run).** `run_n = Llead_n` = the length of the maximal run of **equal leading
> (most-significant) trits** of `N_n`. (Companion proxies: `Ltop2_n` = leading run of the digit `2` — the
> genuine max-digit *overflow* run whose completion to the frontier is the o18-HALT alignment; `Ltrail_n` =
> trailing equal-trit run — the 3-adic / low end governed by the GAP LEMMA.)

This is the same `leadrun` quantity of `O18_QUENCHED_BC` §3, here computed to **12 000 epochs** (`N_{12000}` has
`k_n = 10 716` trits, exact big-int).

| `n` | `k_n = #trits` | `k_n / n` | running max `run_{≤n}` | `log_3 n` |
|---|---|---|---|---|
| 100 | 92 | 0.920 | 4 | 4.19 |
| 1 000 | 895 | 0.895 | 7 | 6.29 |
| 5 000 | 4 467 | 0.8934 | 8 | 7.75 |
| 12 000 | 10 716 | 0.8930 | **10** | 8.55 |

- **`k_n / n → log_3(8/3) = 0.892789…`** `[VERIFIED]` — this is the source of the threshold constant `0.893`.
- **`run_n` histogram** (12 001 epochs): `{1:8279, 2:2502, 3:814, 4:269, 5:95, 6:28, 7:10, 8:3, 10:1}`,
  **mean 1.462, max 10**. Tail `P(run_n ≥ k) ≈ 3^{-(k-1)}` exactly (`k=2:0.310` vs `0.333`; `k=4:0.034` vs
  `0.037`; `k=8:0.0003` vs `0.0005`). `[OBSERVED]`
- **`run_n = O(log n)`** `[OBSERVED]`: running max tracks `log_3 n` to `±2` (max 10 at `n=12000`,
  `log_3 12000 = 8.55`). The overflow proxy `Ltop2_n` and the trailing `Ltrail_n` are likewise geometric with
  max `8` — **all three carry-runs are `O(log n)`**.
- **Leading-trit law is Benford base 3** `[OBSERVED]`: `P(lead=1)=0.631 ≈ log_3 2 = 0.6309`,
  `P(lead=2)=0.369 ≈ log_3(3/2)=0.3691` — i.e. the log-mantissa phase equidistributes (this *is* §2's rotation).

> **§1 verdict.** The carry-run is geometric/`O(log n)` in every reasonable definition, `≈ log_3 n`,
> astronomically below the linear threshold `0.893 n`. `[OBSERVED, single orbit]`

---

## 2. The exact carry-run recursion — a circle rotation with a geometrically-shrinking target  [VERIFIED / PROVEN]

Write `N_n = 3^{k_n − 1} · μ_n` with **mantissa** `μ_n ∈ [1,3)`, and phase `θ_n := log_3 μ_n = {log_3 N_n} ∈ [0,1)`.

> **Recursion `[PROVEN, up to O(1/N_n)]`.** `θ_{n+1} = {θ_n + α}` with **`α = log_3(8/3) = 0.892789…`** (irrational,
> since `α = 3 log_3 2 − 1`), plus a perturbation `δ_n = log_3((⌊8N_n/3⌋+2)/(8N_n/3)) = O(1/N_n)` that is summable,
> so `θ_n = {θ_0 + nα + β_n}` with `β_n → β := log_3 x`, `x = lim N_n/(8/3)^n`. **The leading edge of the orbit is
> an irrational circle rotation by `α = log_3(8/3)`.** `[VERIFIED]`: `θ_n` from exact top-trits matches the rotation
> (circular metric) to `O(1/N_n)`; the leading-trit Benford law of §1 is its equidistribution.

The carry-run is an **exact function of the phase**:

> **`[PROVEN]`** `run_n = ⌊ −log_3 dist(θ_n, C) ⌋ + O(1)`, where `dist(θ_n, C)` is the distance of `θ_n` to the
> nearest **corner** `C = {0, 1}` (digit-`1` leading runs sit at `μ_n ↓ 1`, i.e. `θ_n ↓ 0`; digit-`2` runs at
> `μ_n ↑ 3`, i.e. `θ_n ↑ 1`). A leading run of length `L` ⟺ `θ_n` within `≍ 3^{-L}` of a corner.

So **a long carry-run = the rotation orbit `{nα+β}` making a close approach to a corner.** `[VERIFIED]`:
the closest approaches over 3 000 epochs are `dist ≈ 3.6·10^{-4}` (at `n=897`, `⇒ run ≈ 7.2`), `4.1·10^{-4}`
(`n=2464`, run≈7.1) — i.e. the realized `max run ≈ 7–10` is exactly `−log_3(closest approach)`.

**Self-limiting? `[PROVEN: NO arithmetic cap].** The recursion is a *pure rotation*; an irrational rotation has
**no arithmetic mechanism preventing a close approach** to a corner at some epoch — close approaches are governed
by the continued fraction of `α` (three-distance theorem) and the offset `β`, an inhomogeneous-Diophantine object,
not by any valuation budget. The carry-run does **not** self-limit; its smallness is a genericity/Diophantine fact
about the *specific* `β`, not a structural identity.

---

## 3. The crux — the exact constant, and why no unconditional counting/valuation bound beats it

### 3a. The threshold, pinned exactly  [PROVEN]
The alignment (o18-HALT) needs the carry to propagate the run to the frontier, `run_n < R(n)` with
`R(n) = k_n − O(1)` and `k_n = ⌊log_3 N_n⌋ + 1 = α·n + O(1)`, `α = log_3(8/3) = 0.892789…`. So the required input is

> **`run_n < α n + O(1)`, `α = log_3(8/3) = 0.892789…`** — equivalently, in phase coordinates,
> **`dist(θ_n, C) ≥ 3^{-R(n)} ≍ 1/N_n = x^{-1}(3/8)^n`** for all `n > P`.

(Sanity: the per-epoch Haar probability `P(B_n)=1/N_n` of the note is exactly this corner-target measure `≍3^{-k_n}`.)

### 3b. The trivial unconditional bound lands EXACTLY on the threshold — zero slack  [PROVEN]
A run of equal digits cannot exceed the number of digits:

> **`run_n ≤ k_n = α n + O(1)`  unconditionally `[PROVEN]`.**

This is the **only** unconditional bound available from counting, and it **coincides with the threshold** `R(n) ≈ k_n`.
The residual gap between what is proved (`run_n ≤ k_n`) and what is needed (`run_n < R(n) = k_n − O(1)`, strict) is
**exactly the alignment event**: `run_n = k_n` means *all* trits of `N_n` are the same single run (the full-width
carry) = the frontier collision = HALT. So "`run_n < k_n` for all `n > P`" **is** the non-halting theorem verbatim —
this is route `(R1)`, **circular**, not a bound that beats the threshold.

> **Correction to the "factor ~0.9 slack" reading of `O18_QUENCHED_BC` `(R3)`.** The slack is **illusory as an
> unconditional statement.** The note's worry that "`run ≤ ln N_n ≈ 0.98 n` is too weak by a hair" used the *natural*
> log; the carry-run counts base-3 *digit positions*, so the correct trivial ceiling is `run ≤ log_3 N_n = 0.893 n`,
> which is not 0.98 n but **exactly the threshold** `0.893 n`. The "hair" is therefore not a 0.98-vs-0.893 gap; it is
> the `O(1)`-and-strictness gap between `≤ k_n` and `< k_n`, and **that gap is the halt event itself.** The genuine
> `O(log n)` smallness is real but `[OBSERVED]`, not unconditional.

### 3c. Does any sub-threshold counting bound exist? Does the 3-adic valuation budget cap the run?  [PROVEN: NO]
To gain real slack one needs `run_n ≤ (1−ε) k_n` (any `ε>0`) or `run_n = o(n)`. In phase coordinates this is
`dist(θ_n, C) ≥ N_n^{-(1−ε)}`. Two unconditional toolkits, both fail to reach it:

1. **Counting / equidistribution.** `dist(θ_n, C) ≥ N_n^{-(1−ε)}` is an **effective inhomogeneous-Diophantine /
   shrinking-target** statement for the rotation `{nα+β}` against a target of measure `N_n^{-(1−ε)}`. Since
   `Σ_n N_n^{-(1−ε)} = Σ_n x^{-(1-ε)}(3/8)^{(1−ε)n} < ∞` for every `ε<1`, Borel–Cantelli-I gives finiteness for
   **almost every** `β` — but for the **specific** `β = log_3 x` it is the effective single-orbit equidistribution
   that **no unconditional tool delivers** (AEV Conj 1.6 at `q=3`, Archimedean/Mahler facet; Narkiewicz 1980 gives
   only an upper *density* bound, the bad set is not even known finite). Open.

2. **3-adic valuation budget (the GAP-LEMMA / `v3` route, analog of Antihydra's `v3(o_{j+1})=D_j−1`).** The GAP
   LEMMA controls `D''_n = v_3(8N_n − r_n)` and caps the **trailing** equal-trit run `Ltrail_n` (geometric, mean
   `3/2`) — the **low / 3-adic place**. The carry-run that fires the halt is the **leading** run — the **top /
   Archimedean place**, the mantissa phase `θ_n` of §2. These are **different places of the adele**: the `v3`
   budget says nothing about leading digits, and there is **no product-formula link** that converts a trailing
   valuation bound into a leading-run bound. `[VERIFIED]`: `Ltrail` (3-adic, controlled) and `Llead` (Archimedean,
   open) are independent — both `O(log n)` empirically but only `Ltrail` is touched by the valuation identity.

> **§3 verdict `[PROVEN]`.** The only unconditional bound is `run_n ≤ k_n = 0.893 n + O(1)`, which **equals** the
> threshold (no slack; the residual gap = the halt event = circular). No crude counting or 3-adic-valuation
> argument beats it: the valuation budget lives at the **wrong (trailing/3-adic) place**, and any genuine
> sub-threshold bound `run_n ≤ (1−ε)·0.893 n` is the **effective Archimedean equidistribution** of the specific
> orbit = AEV `q=3` (Mahler facet), world-open.

---

## 4. The precise lemma needed, and the honest verdict

### The exact missing lemma
> **(L-carryrun) [OPEN].** For `α = log_3(8/3)` and `β = log_3 x` (`x = lim N_n/(8/3)^n`, the o18 leading
> constant), there is an effective `c>0` and `P` with
> **`dist({nα + β}, {0,1}) ≥ c·(3/8)^n` for all `n > P`** — equivalently the leading base-3 digits of
> `⌊x·(8/3)^n⌋` equidistribute effectively, so `run_n = o(n)` (indeed `O(log n)`). Any such effective bound
> (even with the crude constant `0.5 n`) closes `(R3)` ⇒ quenched BC-I ⇒ **o18 non-halting**.

This is the **Archimedean / Mahler facet of AEV Conj 1.6 at `q=3`**, the inhomogeneous shrinking-target form for
the rotation by `log_3(8/3)`. It is **strictly weaker in measure** than full equidistribution (any `ε<1` target is
Borel–Cantelli-summable; a.e. `β` satisfies it), but for the **specific** `β` it is exactly the open effective
single-orbit statement — no unconditional rate, lower bound, or finiteness exists in the literature.

### Honest verdict
**The weaker target `run_n < 0.893 n` REDUCES TO THE OPEN EQUIDISTRIBUTION — it does NOT close o18.** Precisely:

1. **It is a genuinely weaker *target*** (Borel–Cantelli-I vs Strong Law; summable corner-target; any `ε<1`
   works) — `O18_QUENCHED_BC` §4's ranking stands.
2. **But it is NOT unconditionally provable.** The single unconditional bound (digit count) is `run_n ≤ k_n`,
   which **coincides with the threshold** `0.893 n`; the gap to the strict bound needed is **the halt event
   itself** (circular = `(R1)`). The advertised "factor ~0.9 slack" exists only `[OBSERVED]` / for a.e. offset
   `β`, **not** as an unconditional pointwise bound for the specific orbit.
3. **No crude counting or valuation argument fits the gap.** The carry-run recursion is a *pure rotation* with
   **no arithmetic self-limit** (§2); the 3-adic GAP-LEMMA budget caps only the **trailing** place and cannot
   reach the **leading** (Archimedean) run (§3c).
4. **Exact point of reduction:** lemma **(L-carryrun)** above = effective inhomogeneous Diophantine for
   `{n log_3(8/3) + log_3 x}` = AEV `q=3` Archimedean facet. World-open.

> **One-line verdict.** `run_n < 0.893 n` is a **provably lower bar** but **not a present proof**: the only
> unconditional bound (`run_n ≤ 0.893 n + O(1)`) sits *exactly on* the threshold with the residual gap equal to
> the halt event (circular), and the realized `O(log n)` smallness is the **open effective Archimedean
> equidistribution** of the specific orbit (AEV `q=3`), unreachable by counting or by the 3-adic valuation
> budget. **Reduces to equidistribution; does not close o18.** No decision; soundness intact.

---

## Reproduce (`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
- `o18_carryrun.py` — 12 000 epochs exact: `k_n/n → 0.892789`; `run_n` histogram (max 10, mean 1.46, `P(run≥k)≈3^{-(k-1)}`); `Ltop2`, `Ltrail` proxies; Benford leading-trit law.
- `o18_rotation.py` — confirms `θ_n = {log_3 N_n}` is the rotation by `α=log_3(8/3)`; closest corner approaches `↔` realized max runs; `dist(θ_n,C) ≫ (3/8)^n` (the non-halt margin, in the open coordinate).
