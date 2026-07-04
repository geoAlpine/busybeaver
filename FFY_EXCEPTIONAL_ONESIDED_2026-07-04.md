# Fan–Fan–Ye's exceptional set for the ONE-SIDED (K): still full dimension — unifying the metric wall with No-Structure C2 (2026-07-04)

*Follow-up to the building-block bridge (`BLOCK_BRIDGE_2026-07-04.md`): Fan–Fan–Ye (arXiv:2512.05690) prove
`⌊αxⁿ⌋` uniformly distributed for a.e. `x`, exceptional set `E_UD` of **full Hausdorff dimension**. But `(K)`
does **not** need full UD — only the **one-sided** `liminf` even-density `≥ 1/3`. **Does the exceptional set for
that weaker condition shrink below full dimension** (a potential crack)? Answer: **no — it is still full
dimension**, and the reason **unifies Fan–Fan–Ye's metric wall (multiplier space) with the program's No-Structure
theorem C2 (seed/orbit space)** as one specification phenomenon. SOUNDNESS: `[PROVEN-in-lit]`/`[OBSERVED]`; no
machine decided; `(K)` `[OPEN]`.*

## 0. Headline
- **The one-sided `(K)`-exceptional set has FULL Hausdorff dimension** `[PROVEN-in-lit + OBSERVED]`. Relaxing
  full-UD → one-sided `liminf ≥ 1/3` does **not** shrink the bad set below dimension 1, so it gives **no escape**
  from the a.e.→specified wall.
- **Subtle but decisive:** the set with **Cesàro limit exactly** `1/3` has dimension `h(1/3)=0.918 < 1` (a thin
  slice), which *might* look like a smaller target — **but `(K)`'s actual condition is a `liminf`/first-passage**
  (the running average dips below `1/3` i.o.), and **that set is full-dimensional** because the dips can be made
  **sparse** (density-0 in time): a full-entropy sequence sits at density `1/2` almost always and dips below `1/3`
  on a vanishing fraction of times.
- **Unification:** Fan–Fan–Ye's full-dim `E` (over the **multiplier** `x`) and the program's No-Structure **C2**
  full-dim violators (over the **seed/orbit** of the fixed `×3/2` map) are the **same** phenomenon — specification
  ⇒ full-dimensional exceptional set — in two parameter spaces. The `(K)` problem sits at `(x=3/2, α=8)`, a single
  point inside **both** full-dim exceptional sets.

## 1. The multifractal spectrum `[OBSERVED, exact]`
In the parity full-shift (annealed model; even-density is the Birkhoff average of `1{c_n even}`), the Hausdorff
dimension of the level set `{even-density = p}` is the binary entropy `f(p)=h(p)=-p\log_2 p-(1-p)\log_2(1-p)`:

| `p` | `1/6` | `0.2` | **`1/3`** | `0.4` | **`1/2`** | `2/3` |
|---|---|---|---|---|---|---|
| `f(p)=h(p)` | 0.650 | 0.722 | **0.918** | 0.971 | **1.000** | 0.918 |

Maximised at the typical value `p=1/2` (`f=1`, full). The **Cesàro-limit-exactly-`1/3`** set has `f(1/3)=0.918<1`.

## 2. But the ONE-SIDED (K) set is the liminf set — and that is FULL `[PROVEN-in-lit]`
`(K)` non-halting `⟺ B_n=3E_n-n ≥ 0 ∀n ⟺` running even-density `≥ 1/3` for all `n`; halting `⟺` the running
average **ever/i.o. dips below `1/3`**. So the `(K)`-**violating** (halting) set is a **`liminf`/first-passage**
set `{x : liminf_N (1/N)Σ 1{c_n even} < 1/3}`, **not** the Cesàro-exact slice.

**Dimension of the liminf set = 1 (full).** By the multifractal analysis of `liminf`/`limsup` Birkhoff averages
under **specification** (Barreira–Schmeling; Fan–Jordan–Liao–Rams), `\dim\{liminf A_N ≤ a\}=1` for every `a` above
the essential infimum, because one can build a full-dimension set that spends a `(1-ε)` fraction of time at the
full-entropy value `1/2` and forces the average below `1/3` only on a sparse `ε→0` fraction of times. **Numeric
illustration `[OBSERVED]`:** an entropy budget `(1-ε)·h(½)+h(ε) → 1` as the dip-fraction `ε→0`, so full-dimensional
sequences with `liminf < 1/3` exist. This is exactly the program's **No-Structure theorem C2** `[PROVEN]`
(specification ⇒ multifractal; Birkhoff set of `1{D≥2}` is `[0,1]`; **full-Hausdorff-dim violators including `δ₁`**).

So **the one-sided relaxation does not shrink the exceptional set**: it is the liminf set, which is full-dim, not
the thin Cesàro slice `h(1/3)=0.918`.

## 3. Even the Cesàro (dim-0.918) version would not crack it `[ARGUED]`
Suppose `(K)` had needed the *Cesàro limit* `< 1/3` (exceptional dim `0.918 < 1`). That would **still** not localise
`x=3/2`: **membership of a specified point in a positive-dimension set is an arithmetic question, not a dimensional
one.** A dimension `0.918` fractal can contain or miss any named point; only an arithmetic UD-certificate at `3/2`
(= a single-orbit effective statement = `(K)`) decides. So sub-full dimension would sharpen the target's *size* but
not open the a.e.→specified door — and in fact the dimension is full anyway.

## 4. Unification — the metric wall and No-Structure C2 are one phenomenon `[the (b) gain]`
> **Two exceptional sets, one cause.** Fan–Fan–Ye's `E ⊂ \{x : |x|_p>1\}` (bad **multipliers**) is full-dim by the
> metric/de Mathan–Pollington mechanism. No-Structure C2's violator set `⊂` orbits/measures of the fixed `×3/2`
> map (bad **seeds**) is full-dim by specification. **Both are "specification ⇒ full-dimensional exceptional
> set,"** in the multiplier space and the seed space respectively. The `(K)` instance fixes `x=3/2` **and** `α=8`
> — a single point sitting inside **both** full-dim exceptional sets. Neither the metric route (remove a.e. over
> `x`) nor the multifractal route (select the seed) can localise its own point, for the identical reason:
> full-dimensional bad sets are not separated from named points by measure/dimension.

This connects the program's internal No-Structure theorem to the external Fan–Fan–Ye metric theory: they are the
**same wall in two coordinates**, and the one-sided `(K)` lives on it at full dimension in both.

## 5. Honest verdict
**(c) — no crack; the one-sided relaxation gives no escape.** The `(K)`-violating set is a `liminf`/first-passage
set of **full Hausdorff dimension** (`[PROVEN-in-lit]` specification / No-Structure C2), matching Fan–Fan–Ye's
full-dim `E`; the thin Cesàro slice (`h(1/3)=0.918`) is the wrong object, and even it would not localise `3/2`.
The durable gain is the **unification**: Fan–Fan–Ye's metric exceptional set (multiplier space) and No-Structure
C2 (seed space) are one specification phenomenon, and the one-sided `(K)` sits on it at full dimension in both
coordinates. **`(K)` `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad` (`/opt/homebrew/bin/python3.13`): `f(p)=h(p)` spectrum (`f(1/3)=0.918`, `f(1/2)=1`); dip-fraction
  entropy budget `(1-ε)h(½)+h(ε)→1`. Basis: `BB6_NO_STRUCTURE_THEOREM.md` (C2 full-dim violators, `[PROVEN]`),
  `EFFEQ_PARTIALS_LEDGER_2026-07-04.md` / `BLOCK_BRIDGE_2026-07-04.md` (Fan–Fan–Ye arXiv:2512.05690), Barreira–
  Schmeling (full-dim non-generic sets), Fan–Jordan–Liao–Rams (liminf/limsup Birkhoff multifractal).
