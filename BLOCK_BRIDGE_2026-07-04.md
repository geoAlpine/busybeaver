# Bridging the two EFF-EQ building blocks — Stewart (count) ⨯ Fan–Fan–Ye (a.e.): a barrier analysis (2026-07-04)

*The known-partials ledger (`EFFEQ_PARTIALS_LEDGER_2026-07-04.md`) named two building blocks for the unified
EFF-EQ object: **Stewart 1980** (the right *shape* — single-orbit, effective, unconditional — but a *count* at
*log-size*) and **Fan–Fan–Ye 2025 / arXiv:2512.05690** (the right *object* — `⌊αxⁿ⌋` UD in the `p`-adic valuation
ring — but *a.e.* with a full-dim exceptional set). This note analyses the two barriers (Stewart count→frequency;
Fan–Fan–Ye a.e.→specified) and asks whether **feeding one into the other bridges them**. Verdict: **no — the bridge
reduces exactly to `(K)`**; the two blocks are the *count-side* and *object-side* of the **same** missing theorem.
SOUNDNESS: `[PROVEN-in-lit]`/`[OBSERVED]`/`[ARGUED]`; no machine decided; `(K)` stays `[OPEN]`.*

## 0. Headline
- **Barrier 1 (Stewart count→frequency) has TWO independent sub-walls**, both at/beyond the effective-Diophantine
  frontier: **(1a) log→linear** — even the *count* Stewart proves (`≫ log n/log log n`) is exponentially below the
  linear truth (the digit-weight of `3ⁿ`/`2ⁿ` is `~n/2`, `~2n/3`); **(1b) count→distribution** — Baker's method
  yields **one global inequality** (`2ⁿ` is far from any sparse `3`-adic sum), which controls the *total* number of
  nonzero digits but says **nothing about which digit values occur or their frequency**.
- **Barrier 2 (Fan–Fan–Ye a.e.→specified)** is the metric wall: the proof **integrates over `x`**, discarding the
  arithmetic of the specific `x=3/2`; its exceptional set is **full Hausdorff dimension**, so membership of a named
  point is *not* decidable by dimension. Removing "a.e." needs an **arithmetic UD-certificate at `3/2`**.
- **The bridge fails, and instructively:** the only single-orbit arithmetic input available (Stewart) certifies
  "the orbit's digits are **not too sparse**" (`weight ≥ log`), whereas excluding `3/2` from Fan–Fan–Ye's
  exceptional set needs "**equidistributed**" (a distribution, linear-depth). The gap between the two IS Barrier 1.
  So **connecting the blocks = upgrading Stewart = `(K)`.** The blocks are two faces of one gap; neither
  strengthens the other.

## 1. Barrier 1 — Stewart's count→frequency `[PROVEN-in-lit + OBSERVED numeric anchor]`
Stewart (1980, `J. Reine Angew. Math.` 319) proves, via **Baker's linear forms in logarithms**, that `2ⁿ` has
`≫ log n/(log log n + c)` nonzero base-3 digits (`c` effective); by symmetry the same bounds the base-2 Hamming
weight of `3ⁿ` — the seam object `d_n = bit_{n+k}(8·3ⁿ)` of the program.

**Sub-wall 1a — log vs linear `[OBSERVED, block_bridge anchor]`.** The digit-weight is empirically **linear**:
`w₃(2ⁿ)/#digits → 0.67 ≈ 2/3` and `w₂(3ⁿ)/#digits → 0.50 ≈ 1/2` (normal-like). Stewart *proves* only `~log
n/log log n`. Loose factor `w₃/Stewart`: **16× (n=50) → 177× (10³) → 2811× (2·10⁴)**, growing like `n/log n`. So the
*count itself* is log-vs-linear — the same gap as `#even ≥ 0.89 log n`. **Why:** Baker's lower bounds on `|linear
form in logs|` are inherently **logarithmic in the height** (`~n`); a linear-in-`n` digit count would need effective
bounds exponentially sharper than Baker — `abc`/`Hall`-conjecture strength — which no unconditional method supplies.

**Sub-wall 1b — count vs distribution `[ARGUED]`.** Even granting a hypothetical *linear* count, Baker's method
produces a **single Diophantine inequality** (`2ⁿ` is far from `Σ_{i∈S} 3^{a_i}` for small `|S|`) — a statement
about the *total* sparsity. Digit **frequency** (`each of 0,1,2` appears with density `1/3`; or the moving digit
`d_n` is even with density `1/2`) is a statement about the **joint distribution of all digit positions**, which a
proximity/magnitude inequality cannot access: Baker controls *how close* `2ⁿ` is to a sparse set, not *where* its
nonzero digits sit. These are orthogonal axes; no strengthening of the *magnitude* bound yields a *positional*
distribution.

## 2. Barrier 2 — Fan–Fan–Ye's a.e.→specified `[PROVEN-in-lit + ARGUED]`
Fan–Fan–Ye (arXiv:2512.05690) prove `(⌊αxⁿ⌋)` is uniformly distributed in the valuation ring for **almost every**
`x` (`|x|_p>1`), with the exceptional set `E` of **full Hausdorff dimension** and rich fractal structure. To use it
at `x=3/2` we must show `3/2 ∉ E`. Two structural obstructions:
- **The method integrates out the arithmetic.** The proof is a metric/second-moment argument over the parameter
  measure `dx`; it establishes `|E|=0` but is **constant on the arithmetic of any single `x`** — it has no handle
  that distinguishes `3/2` from a generic point (the same a.e.→specified wall as Aistleitner, de Mathan–Pollington,
  Tao 2019, the program's own annealed→quenched seam).
- **Full dimension ⇒ membership is arithmetic, not metric.** Because `dim E = 1`, "is `3/2 ∈ E`?" cannot be settled
  by any dimension/measure estimate (a full-dim set can contain or miss any named point); it requires an **arithmetic
  UD-certificate for `3/2`'s orbit** — precisely a single-specified-orbit effective equidistribution statement.

## 3. The bridge attempt — feed Stewart into Fan–Fan–Ye `[ARGUED → reduces to (K)]`
The natural hope: Stewart supplies **single-orbit arithmetic** (which the metric method lacks); plug it in as the
certificate that removes "a.e." at `3/2`. **It fails for a precise reason.** Excluding `3/2` from `E` requires
certifying its orbit is **equidistributed** (or at least the one-sided `(K)` density). Stewart certifies only that
the orbit is **not too sparse** (digit-weight `≥ log`). The implication needed —
> *not-too-sparse (Stewart) ⟹ equidistributed (∉ E)* —
is **exactly Barrier 1** (count→frequency, and log→linear). So the bridge does not add anything: it **reduces to
upgrading Stewart**, which is `(K)`. (The `p`-adic variant — using **Yu's `p`-adic linear forms in logs** to get a
`p`-adic Stewart bound native to Fan–Fan–Ye's valuation-ring setting — was considered and **closes the same way**:
Yu bounds a `p`-adic *valuation* of a linear form, still a **count/magnitude**, still **log-strength**; it feeds the
same not-too-sparse input, not a distribution.)

## 4. What the two blocks actually are — opposite corners of one gap `[the (b) sharpening]`
> **The unified EFF-EQ target = `[single-orbit, effective, unconditional, distributional, linear-depth]`.**
> **Stewart** occupies `[single-orbit, effective, unconditional, COUNT, log-depth]` — correct on the *hard* axes
> (deterministic orbit, effective, unconditional), deficient on **distributional** and **linear-depth**.
> **Fan–Fan–Ye** occupies `[DISTRIBUTIONAL (UD), linear-depth (valuation ring), a.e.]` — correct on the *object*
> axes (distribution, the right `p`-adic floor-orbit), deficient on **single-specified-orbit**.
> **They are complementary but non-overlapping:** each has exactly what the other lacks, and the region they would
> have to meet — single-orbit ∧ distributional ∧ linear-depth ∧ effective — is empty (= the target). Bridging them
> is not a matter of combination; it requires the **one missing upgrade** that neither partial contains.

This is the precise, outreach-ready statement of the gap: **a bridging theorem is one that makes Stewart
distributional-and-linear OR removes Fan–Fan–Ye's a.e. at a specified point — and these are the same theorem.**

## 5. Honest verdict
**(c) — the bridge reduces to `(K)`, with a `(b)` structural sharpening.** Neither building block strengthens the
other: Stewart's not-too-sparse count is far too weak to certify Fan–Fan–Ye's UD (Barrier 1), and Fan–Fan–Ye's
a.e. cannot be localized to `3/2` without exactly such a certificate (Barrier 2). The `p`-adic Baker variant closes
identically. The durable gain is the crisp placement — **Stewart and Fan–Fan–Ye are the count-side and object-side
of the single missing theorem** — which sharpens the empty-toolbox verdict into a two-corner target picture for
outreach (Stewart's shape + Fan–Fan–Ye's object, bridged only by the `(K)`-grade upgrade). **`(K)` `[OPEN]`. No
machine decided. No label upgraded.**

## Reproduce
- Numeric anchor (`scratchpad`, `/opt/homebrew/bin/python3.13`): base-3 weight of `2ⁿ` and base-2 Hamming weight of
  `3ⁿ` → `≈ 2/3, 1/2` of the digit count (linear); Stewart bound `~log n/log log n`; loose factor `16×→2811×`
  (`n=50…2·10⁴`). Basis: `EFFEQ_PARTIALS_LEDGER_2026-07-04.md` (§B Stewart, Fan–Fan–Ye), `CITATIONS.md` #8, #10;
  Stewart *J. Reine Angew. Math.* 319 (1980); Fan–Fan–Ye arXiv:2512.05690; Yu `p`-adic logs (K. Yu, *Acta Arith.*).
