# The (K)-exceptional set's fine structure — (dim 1, measure 0) like badly-approximable, but no continued-fraction coordinate (2026-07-04)

*Two angles on the full-dimensional exceptional wall (`FFY_EXCEPTIONAL_ONESIDED_2026-07-04.md`): **(1)** does the
**measure-1 non-violator** side (a.e. non-halting) plus arithmetic give a handle on `3/2` that the point-blind
full-dimension side cannot? **(2)** a **refinement of the liminf multifractal** (native depth process). Result:
both `(c)` — no crack — but with a sharp characterization: the `(K)`-violating set is a **`(dim 1, measure 0)`
fractal, topologically like the badly-approximable numbers**, and the reason it gives no arithmetic handle is
**precisely the absence of a continued-fraction-type coordinate for `⌊3x/2⌋` (= non-Pisot)**. SOUNDNESS:
`[OBSERVED]`/`[PROVEN-in-lit]`/`[ARGUED]`; no machine decided; `(K)` `[OPEN]`.*

## 0. Headline
- **The `(K)`-violating (halting) set is `(dimension 1, measure 0)`** in parameter space — full Hausdorff
  dimension (No-Structure C2 / specification) yet measure zero (a.e. orbit non-halting). **A "large in dimension,
  small in measure" fractal — the exact topological type of the badly-approximable numbers.**
- **Angle 1 — the measure-1 side gives no handle.** Both dimension *and* measure are **point-blind**: a full-dim
  set and a full-measure set can each contain or miss any *named* point. The only thing that separates `3/2` is an
  **arithmetic coordinate**. Badly-approximable numbers *have* one (bounded continued-fraction partial quotients,
  from the Gauss map) — but `⌊3x/2⌋` is **non-Pisot ⇒ not sofic ⇒ has no continued-fraction-type symbolic
  coordinate** (`[PROVEN-in-lit]`, the program's Selector/Frougny wall). So the analogy shows the halting set has
  the *right topology* for an arithmetic characterization, and pins **exactly what is missing**: the coordinate
  system. That missing coordinate *is* `(K)`.
- **Angle 2 — the multifractal, refined.** Native depth process (`D` iid geometric, `E[D]=2`): the Cesàro slice
  `{mean-D = 3/2} = {even-density = 1/3}` has dimension **`0.9183`** (identical in the depth and parity codings — a
  consistency check); the actual liminf/first-passage `(K)`-set is **full-dim `1`**; the boundary large-deviation
  rate is the **golden ratio** `θ*=\log φ`.

## 1. Angle 2 — the refined multifractal spectrum `[OBSERVED, exact]`
Depth coordinates (native): `D_i` iid, `P(D=d)=2^{-d}`, `E[D]=2`; `even-density = 1 − 1/\mathrm{mean}D`; `(K)`
boundary `mean-D = 3/2`. Thermodynamic (Gibbs-tilted) dimension of the Cesàro level set `{mean-D=m}`:

| `mean-D` | 2.00 (typical) | 1.82 | 1.67 | **1.50 (K-boundary)** | 1.33 | 1.25 |
|---|---|---|---|---|---|---|
| `dim{mean-D=m}` | **1.000** | 0.993 | 0.971 | **0.918** | 0.811 | 0.722 |

- **Consistency check:** `dim{mean-D=3/2}=0.9183` **equals** `dim{even-density=1/3}=h(1/3)=0.9183` from the parity
  coding (`FFY_EXCEPTIONAL_ONESIDED §1`) — the same event, two codings, same dimension. ✔
- **Cesàro slice vs liminf set:** the *Cesàro-limit-exactly-3/2* slice is dimension `0.918 < 1` (thin); the *actual*
  `(K)`-violating condition is a **liminf/first-passage** (`B_n=3E_n-n<0` ever / running mean-D dips below 3/2
  i.o.), and `\dim\{liminf\ \mathrm{mean}D ≤ 3/2\}=1` (full) by sparse dips (Barreira–Schmeling; No-Structure C2).
- **Boundary rate = golden ratio:** the balance increment `X=2D-3` (drift `+1`) has Cramér/Lundberg exponent
  `E[e^{-θ^*X}]=1 ⇒ x^3-2x+1=0, x=1/φ`, `θ^*=\log φ=0.4812` — the halting large-deviation rate `~φ^{-s}`
  (`OCCUPANCY_THEORY_PAPER.md` T5). So the fine structure is fully pinned: **Cesàro dim `0.918`, liminf dim `1`,
  measure `0`, boundary rate `\log φ`.**

## 2. Angle 1 — the measure-1 side is point-blind; the badly-approximable analogy `[ARGUED]`
The a.e.-non-halting statement makes the non-violators **measure 1**. Could "measure 1 + arithmetic" localise `3/2`
where "full dimension" could not?

**No — measure is point-blind too.** A full-measure set (like a full-dimension set) can contain or miss any
specified point; the specific orbit `8·(3/2)^n` is a single point, `measure 0` in any continuous parameter measure.
**Neither measure nor dimension separates a named point** — both are invariant under the "generic" moves that do
not see arithmetic. The only separator is an **arithmetic coordinate on the orbit**.

**The badly-approximable analogy — and its precise failure.** The halting set is `(dim 1, measure 0)`, exactly the
type of `\mathrm{BA}=\{x: \liminf n\|nx\|>0\}`. Crucially, **`BA` is decidable pointwise** — `x∈BA ⟺` its
continued-fraction partial quotients are bounded — because the Gauss map supplies a **symbolic coordinate** in
which the `liminf` condition becomes a bounded-digit condition. So a `(dim 1, measure 0)` set *can* have a clean
arithmetic membership test **when the dynamics provide the right coordinate.**

For `⌊3x/2⌋` **there is no such coordinate:** `3/2` is **non-Pisot ⇒ its `β`-shift is not even sofic** (Frougny;
`SELECTOR_COMPUTABILITY.md`), so no finite-state / continued-fraction-type recoding of the orbit exists in which
"halting" becomes a bounded/decidable digit condition. **This is the sharp reason the exceptional-set structure
gives no handle:** the halting set has the *right topology* for an arithmetic membership test, but the map lacks
the *coordinate system* (CF/sofic) that would deliver one — and constructing that coordinate is exactly the
empty-toolbox single-orbit equidistribution problem `= (K)`.

## 3. Synthesis
Both angles rederive the wall, and together they **characterize it precisely**: the `(K)`-violating set is a
`(dim 1, measure 0)` fractal (boundary rate `\log φ`, Cesàro slice `0.918`), topologically a badly-approximable-type
set; **membership of the specified point `3/2` is invisible to both its measure and its dimension**, and would be
decided by an arithmetic coordinate the way `BA` is decided by continued fractions — **except `⌊3x/2⌋` is non-Pisot
and has no such coordinate.** So "use the measure-1 side" and "refine the multifractal" both terminate at the same
place: the missing arithmetic coordinate is `(K)`. This is the cleanest statement yet of *why* the full-dimensional
exceptional wall is impervious — not merely "full dimension," but "full dimension **and** no continued-fraction-type
coordinate," the latter forced by non-Pisot.

## 4. Honest verdict
**(c) — no crack; a sharp characterization.** The `(K)`-exceptional set is `(dim 1, measure 0)` like
badly-approximable; measure and dimension are both point-blind; the arithmetic coordinate that would decide
membership (as continued fractions decide `BA`) does not exist for `⌊3x/2⌋` (non-Pisot / non-sofic), and building it
is `(K)`. The refined multifractal (Cesàro `0.918`, liminf full, rate `\log φ`) is a durable characterization.
**`(K)` `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad` (`/opt/homebrew/bin/python3.13`): depth Gibbs-tilt dimension spectrum (`dim{mean-D=3/2}=0.918`,
  matches parity `h(1/3)`), golden-ratio Cramér `θ*=\log φ=0.4812`. Basis: `FFY_EXCEPTIONAL_ONESIDED_2026-07-04.md`,
  `BB6_NO_STRUCTURE_THEOREM.md` (C2), `OCCUPANCY_THEORY_PAPER.md` (T5 golden ratio), `SELECTOR_COMPUTABILITY.md`
  (non-Pisot ⇒ non-sofic). Barreira–Schmeling (full-dim non-generic); badly-approximable = Jarník (dim 1, measure 0).
