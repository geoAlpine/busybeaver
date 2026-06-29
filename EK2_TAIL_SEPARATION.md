# Can separation / anti-clustering / Borel–Cantelli give an UNCONDITIONAL summable occupancy-tail bound `Σ_k f_k < ∞` (⟺ E[K²]<∞ ⟹ μ({1})=0)?

*2026-06-30. Target (strictly WEAKER than (K)): the jump-depth second moment / occupancy-tail
summability `Σ_k f_k < ∞`, `f_k := freq{ c_n ≡ 1 mod 2^k }`. By `NONATOMIC_FIXEDPOINT.md` this is
exactly `E[K²]<∞` (mean 2-adic depth bounded) and implies `μ({1})=0` (no atom at the repelling
fixed point). It needs only a SUMMABLE tail, NOT the exact geometric law `f_k=2^{-k}` of (K) — so
it could be attackable where (K) is not. ANGLE: are deep landings into the thin cylinder
`{≡1 mod 2^k}` (Haar `2^{-k}`) rare/separated enough for a covering / Borel–Cantelli upper bound on
`f_k`? SOUNDNESS PARAMOUNT; every line labelled; do NOT claim (K). Numerics
`.venv` exact big-int, `ek2_tail_separation.py`. NOT committed.*

---

## 0. One-line verdict

**Verdict (c): separation / anti-clustering / Borel–Cantelli gives NO unconditional summable
occupancy-tail bound — it DIES at the EXACT min-gap-vs-density wall of `DIOPHANTINE_DENSITY.md`,
transposed to the 2-adic side.** A covering count needs a *guaranteed minimum index-gap* `g_k ≳ 2^k`
between successive visits to the thin cylinder `{c_n ≡ 1 mod 2^k}` (Haar `2^{-k}`) to force
`f_k ≲ 2^{-k}` (summable). But the **proven 2-adic structure makes the min index-gap `=1`**: by the
Countdown Lemma the visits to `{d_n ≥ k}` arrive in *contiguous runs* (the tail of each deep
excursion is `d=K,K−1,…,k,…,1`, consecutive `n`), so successive visits are **adjacent**, `g_k=1`,
and the covering bound is the trivial `f_k ≤ N/1`. Counting only the *excursion-starts* that reach
depth `≥k` removes the runs but their spacing is the **refill / return time**, whose distribution
(geometric mean `≈2^k`, min at the birthday/random scale `2^{−k}` matching i.i.d. — `SEPARATION_BAKER`)
is **exactly the occupancy/genericity = Mahler quantity**, OBSERVED not proven. Separation controls
the *min* 2-adic gap (birthday scale); summability needs the *count* (min-gap ÷ average-gap) — and
for this orbit min-gap ≪ average-gap, the same wall. Borel–Cantelli-I is the wrong tool: at fixed `k`,
`Σ_n P(c_n≡1 mod 2^k)=Σ_n 2^{-k}=∞`, so BC-I gives infinitely-many visits (correct), never a frequency
bound. **No unconditional summable `f_k` bound; `μ({1})=0` stays OPEN.** `[PROVEN that separation
cannot bound the occupancy tail]`. Numerics: `f_k≈2^{-k}`, mean depth `≈0.999`, `E[K²]≈5.97`,
**min index-gap `=1` at every `k`** while mean-gap `≈2^k` — separation is nowhere near binding.

---

## 1. The target — a PROVEN reduction (from `NONATOMIC_FIXEDPOINT.md`, restated)

Let `d_n := v₂(c_n − 1)` (2-adic depth toward the fixed point `1`) and
> `f_k := limsup_N (1/N)#{ n<N : c_n ≡ 1 (mod 2^k) } = limsup_N (1/N)#{ n<N : d_n ≥ k }`.

`f_k ↓` in `k`, `μ({1}) = lim_k f_k`, so **`μ({1})=0 ⟺ f_k→0`**. The **Countdown Lemma `[PROVEN]`**:
an odd term with `d=k≥1` has successor with `d=k−1` (the odd part of `c−1` triples; `REPELLER_ESCAPE`
§1), so the orbit visits `{d≥k}` only in **contiguous countdown runs** `K,K−1,…,1` (then an even step,
`d=0`). Summing the countdown gives the **mean-depth identity `[PROVEN]`**
> `(1/N)Σ_{n<N} d_n = Σ_{k≥1} f_k = E[K(K+1)/2] / E[K+1]`  (renewal–reward; `K`=entry/jump depth),

hence `Σ_k f_k = ` mean depth, and **mean depth bounded ⟺ `Σ_k f_k < ∞` ⟺ `E[K²]<∞` ⟹ `f_k→0`
⟹ `μ({1})=0`.** This is the TARGET. It is strictly weaker than (K): (K) fixes `f_k = 2^{-k}`
*exactly for every residue*; the target needs only a **summable upper tail** on residue 1
(`f_k = o(1/k²)` weighted, e.g. `f_k ≤ Cρ^k` or `≤ C k^{-2-ε}` suffices).

## 2. Annealed vs quenched; what separation actually proves

- **Annealed (Haar).** The cylinder `{c≡1 mod 2^k}` has Haar measure `2^{-k}`; annealed `f_k=2^{-k}`,
  `Σ_k 2^{-k}=1<∞`. Annealed summability is **free and irrelevant** — it is what (K)-genericity would
  *give*, not an input.
- **Quenched (the one orbit).** `f_k` is the *actual* density of the specific orbit `c_0=3`,
  `c_{n+1}=⌊3c_n/2⌋`. Proving `f_k(quenched) ≤ g_k` summable is the whole game.
- **What separation proves `[PROVEN/OBSERVED]`.** Two visits to the same deep cylinder collide:
  `c_i≡c_j (mod 2^k) ⟺ v₂(c_i−c_j)≥k`. `SEPARATION_BAKER.md`: the orbit's self-separation
  `P(v₂(c_i−c_j)≥k)` matches the **random `2^{-k}`** (ratio `0.9–1.1`), max collision at the birthday
  scale `log₂(#pairs)` — **no better-than-random separation exists**, and `BAKER_LINFORMS.md` shows
  standard/`p`-adic Baker is **structurally inapplicable** (orbit terms `c_n=(3^n c_0−T_n)/2^n` have
  **unbounded height** `≈1.585n`, not bounded-height S-units). So the separation tool delivers a
  **min 2-adic gap at the birthday/random scale, and nothing one-sided.**

The transfer we would *need* — *quenched* `f_k ≤` *annealed* `2^{-k}` (or even `≤ C k^{-2}`) — is
precisely the statement that the orbit equidistributes mod `2^k` / that the refill law is Haar
(`REPELLER_ESCAPE` §2: `freq(D=1)=1−1/E_deep`, `E_deep=`mean refill `v₂(c_next−1)`). **That transfer
IS genericity = the refill-digit law = Mahler/(K)-adjacent.** No proven transfer exists.

## 3. The covering / separation argument and its EXACT failure

**Covering principle `[elementary]`.** If successive visits to `{c_n≡1 mod 2^k}` are separated by a
*guaranteed* minimum index-gap `g_k`, then `#{n<N : c_n≡1 mod 2^k} ≤ N/g_k + 1`, i.e. `f_k ≤ 1/g_k`.
**Summability `Σ_k f_k<∞` would follow from a guaranteed `g_k ≳ 2^k`** (giving `f_k ≲ 2^{-k}`), or
even just `g_k ≳ k^{1+ε}`. This is the spacing-only route — no equidistribution, no cancellation.

**Failure, gap (A) — the Countdown Lemma forces `g_k = 1` `[PROVEN, decisive]`.** Visits to
`{d_n≥k}` are NOT isolated: each deep excursion of entry-depth `K≥k` produces a **contiguous block of
`K−k+1` consecutive indices** all with `d_n≥k` (the countdown `K,K−1,…,k`). So successive visits are
**adjacent** — the minimum index-gap is literally `1`. Covering gives `f_k ≤ N/1` = trivial. The very
2-adic structure that is *proven* (countdown) makes the per-step separation **maximally vacuous**.
*(Numerics §6: min index-gap `=1` at every tested `k=1..14`.)*

**Failure, gap (B) — counting excursion-starts only reduces to the return/refill law = genericity
`[PROVEN reduction]`.** Pass to the natural de-clustered object: the **starts** of excursions that
reach depth `≥k` (one per run). Two such starts `c_a,c_b` both have `c≡1 mod 2^k`, so
`v₂(c_a−c_b)≥k`. Their spacing is the **return time** to the cylinder, governed by the refill law:
after a run the orbit sits at `v₂(c−1)=1` (2-adically far) and must *re-approach* `1` to depth `≥k`,
which only a deep step can do, with fresh refill `r'` of size `≥k` at rate (observed Haar) `2^{-k}`.
Hence the start-spacing is **geometric with mean `≈2^k`** but **min at the birthday scale** — exactly
i.i.d.-like (`SEPARATION_BAKER`). A *guaranteed* `g_k≳2^k` would be a one-sided lower bound on the
return time = an upper bound on the refill-`≥k` rate = `E_deep`-tail control = **single-orbit
genericity = Mahler** (`REPELLER_ESCAPE` §2,5). Separation gives only the *min* (birthday) gap, never
the guaranteed gap. **Same min-gap-vs-density wall as `DIOPHANTINE_DENSITY.md` §3**, with the literal
correspondence:

| | `DIOPHANTINE_DENSITY` (archimedean) | here (2-adic occupancy tail) |
|---|---|---|
| object | `#{n<N : x_n∈[0,½)}`, `x_n={4(3/2)^n}` | `#{n<N : c_n≡1 mod 2^k}` |
| separation = | min archimedean gap `δ_N` | min index-gap between cylinder visits |
| what separation proves | `δ_N ∼ N^{-2}` (Poisson), Baker `≳2^{-cn}` | min-gap `=1` (countdown) / birthday between starts |
| what density needs | `δ_N ≳ 1/N` (near-equispaced lattice) | guaranteed `g_k ≳ 2^k` (no clustering of starts) |
| gap | min-gap ≪ average-gap (clusters freely) | runs (gap 1) + start-returns at random rate |
| status | **CLOSED**: separation can't control density | **CLOSED**: separation can't bound `f_k` |

## 4. The Borel–Cantelli angle (o18-style) — why BC-I is the WRONG tool here

`O18_REDUCTION.md` used **BC-I** (`Σ P<∞ ⟹ finitely many`, no independence) for an **existence /
finiteness** event (`Σ_k 1/N_k<∞`, one bad alignment per epoch). The occupancy tail is a **different
shape** and BC-I does not bite:

- **Fixed `k`, all `n`.** The events `A_n={c_n≡1 mod 2^k}` have annealed `P=2^{-k}`, so
  `Σ_n P(A_n)=Σ_n 2^{-k}=∞`. BC-I requires *summability over the index of the limsup*; here it gives
  only the (correct, useless) conclusion that `{d_n≥k}` happens **infinitely often**. `f_k` is the
  *Cesàro frequency* of these `i.o.` events — a strong-law / density object, **not** a finiteness
  object — exactly the density-vs-finiteness divide `O18_REDUCTION` §2 draws (and there density was
  *insufficient*; here finiteness is *unavailable*).
- **Moving depth `k_n→∞`.** BC-I *does* apply to `{d_n ≥ (1+ε)log₂ n}`: annealed
  `Σ_n n^{-(1+ε)}<∞ ⟹` finitely many ⟹ `M(N)=O(log N)` (matches the observed `M(N)≈log₂N`). But this
  bounds the **max depth**, and `M(N)=o(N)` provably does **NOT** control `f_k` (`NONATOMIC` §4: the
  atom mass is `inf_k f_k`, a fixed-`k` occupancy, invisible to the running max). And even this BC-I
  needs the *annealed* `P(d_n≥k)=2^{-k}` as a quenched bound — i.e. genericity again.
- **Quenched BC has no independence/mixing.** Within a countdown run the events are perfectly
  *dependent* (deterministic decrement), so no second-Borel–Cantelli / lower bound, and the upper BC
  needs the annealed transfer that is itself (K)-adjacent.

**Net:** BC controls the **max** depth (log-scale, side fact), not the **occupancy** tail; it cannot
deliver `Σ_k f_k<∞`.

## 5. Is there ANY unconditional summable bound? (first-vs-second-moment budget)

No. The proven **valuation budget** `Σ_{odd i<n} v₂(3c_i−1) = n + v₂(c_n) − v₂(c_0)` controls the
**first** moment: `Σ_i K_i ≈ n`, i.e. `E[K]≈2` (mean gap, a first-moment tautology). The target
`Σ_k f_k = (1/N)Σ_i K_i(K_i+1)/2 = E[K²]/2 + …` is a **second** moment `Σ_i K_i²`, on which the budget
says **nothing**. The crude proven envelope `K_i ≤ 0.585 n` permits (without contradiction) a single
run of length `≈0.585N`, giving `E[K²]=∞` and an atom `μ({1})≥0.585` — so the proven structure does
not even bound `Σ_k f_k`, let alone make it summable. The only crude unconditional `f_k` bound is the
trivial `f_k ≤ f_1 ≤ 1` (not summable). **Verdict (a) "summable tail PROVEN" is FALSE; the honest
verdict is (c).**

## 6. Numerics (`.venv` exact big-int, `ek2_tail_separation.py`, `c_0=3`, `N=10⁵`)

**Occupancy `f_k` — geometric, mean depth bounded (consistent with `E[K²]<∞`, NOT proof):**

| k | f_k | 2^{-k} | f_k/2^{-k} | f_k/f_{k-1} |
|---|---|---|---|---|
| 1 | 0.50002 | 0.5 | 1.000 | – |
| 4 | 0.06264 | 0.0625 | 1.002 | 0.504 |
| 8 | 0.00402 | 0.00391 | 1.029 | 0.504 |
| 12 | 0.00019 | 0.000244 | 0.778 | 0.463 |
| 16 | 0.00001 | 0.000015 | 0.655 | 0.500 |

mean depth `Σd_n/N = 0.99883`; `Σ_{k} f_k = 0.99883`; `E[K]=1.993`, `E[K²]=5.969`, `maxK=16`;
`P(K≥k)` geometric, `k·P(K≥k)` summable — all OBSERVED consistent with `E[K²]<∞`.

**Spacing — the decisive picture: min index-gap `=1` everywhere, mean-gap `≈2^k`:**

| k | #visits to {d≥k} | min index-gap | mean index-gap | `1/f_k` |
|---|---|---|---|---|
| 4 | 6264 | **1** | 16.0 | 16.0 |
| 8 | 402 | **1** | 248.7 | 248.8 |
| 10 | 86 | **1** | 1165 | 1163 |
| 12 | 19 | **1** | 5425 | 5263 |

Covering test: a *guaranteed* gap of `2^k` is needed for `f_k≲2^{-k}`; the **actual** min-gap is `1`
(countdown runs), so the covering bound `N/min-gap = N = 10⁵` is **trivial at every `k`** (≫ the actual
`#visits`). Separation is nowhere near binding — identical to `DIOPHANTINE_DENSITY` §3's "orbit
clusters freely within its separation budget."

**2-adic self-separation `P(v₂(c_i−c_j)≥k)` (200k sampled pairs):** matches random `2^{-k}`, ratio
`0.9–1.1` through `k≈13` (birthday tail thereafter) — reconfirms `SEPARATION_BAKER`: **no
better-than-random separation to exploit.**

## 7. Verdict + the exact gap

> **(c) — closed with a precise reason.** Separation/anti-clustering/Borel–Cantelli does **not** yield
> an unconditional summable occupancy-tail bound `Σ_k f_k<∞`, so it does **not** prove `E[K²]<∞` or
> `μ({1})=0`. The covering route needs a *guaranteed minimum index-gap* `g_k≳2^k` between visits to the
> thin cylinder `{c_n≡1 mod 2^k}`; the **proven Countdown Lemma forces `g_k=1`** (visits arrive in
> contiguous runs), and de-clustering to excursion-*starts* only relocates the question to the
> return/refill law, whose required one-sided gap bound **is** the refill-digit genericity = Mahler/(K).
> The proven self-separation is exactly random-scale (`SEPARATION_BAKER`) and standard Baker is
> inapplicable (unbounded height, `BAKER_LINFORMS`), so separation delivers only the *min* 2-adic gap
> (birthday), never the *guaranteed* gap a count needs. BC-I addresses *finiteness* (it bounds the max
> depth `M(N)=O(log N)`, a side fact that does **not** bound fixed-`k` `f_k`), not the *Cesàro
> frequency*; at fixed `k`, `Σ_n P=∞`, so BC-I correctly yields only "infinitely often."

**The exact gap (one sentence).** *Separation = the minimum 2-adic / index gap between cylinder
visits (proven random/birthday scale; countdown forces it to `1` per-step); summability of `f_k` =
the visit COUNT = how the min-gap relates to the average return-gap `≈2^k`; for this orbit
min-gap ≪ average-gap, and closing the ratio is precisely the refill-law occupancy = single-orbit
genericity = the open Mahler `(3/2)^n` kernel — the identical min-gap-vs-density wall as
`DIOPHANTINE_DENSITY.md`, transposed from the archimedean orbit `{4(3/2)^n}` to the 2-adic depth
`v₂(c_n−1)`.* It is a **first-moment-proven / second-moment-open** gap: the valuation budget gives
`Σ_i K_i≈n` (mean gap), never `Σ_i K_i²` (the occupancy tail).

### Sources
- `NONATOMIC_FIXEDPOINT.md` — the PROVEN reduction `μ({1})=0 ⟺ f_k→0 ⟸ Σ_k f_k<∞ ⟺ E[K²]<∞`; mean-depth identity; first-vs-second-moment gap; `f_k≈2^{-k}` numerics.
- `REPELLER_ESCAPE.md` — Countdown / dual-repulsion lemma `[PROVEN]`; refill law `freq(D=1)=1−1/E_deep`; reduction of the density to the refill-digit law = genericity = Mahler.
- `SEPARATION_BAKER.md` — orbit self-separation `v₂(c_i−c_j)` is exactly random `2^{-k}` (birthday scale); no exploitable separation.
- `BAKER_LINFORMS.md` — standard/`p`-adic Baker structurally inapplicable: orbit terms have unbounded height `≈1.585n` (nested-floor `T_n`), not bounded-height S-units.
- `DIOPHANTINE_DENSITY.md` — the archimedean min-gap-vs-density wall (separation `δ_N∼N^{-2}` ≪ needed `1/N`); this note is its 2-adic transposition.
- `O18_REDUCTION.md` — Borel–Cantelli-I used for an *existence/finiteness* event; the density-vs-finiteness divide showing BC-I is the wrong tool for a fixed-`k` Cesàro frequency.
- `DIGITS_OF_3N.md` — longest-run `L(M·3^K)=o(K)` (subspace theorem) bounds horizontal runs, not occupancy; nearest unconditional handle, provably short.
- Numerics: `scratchpad/ek2_tail_separation.py` (exact big-int; `f_k`, spacing, covering test, self-separation; `c_0=3`, `N=10⁵`).

No machine decided. No label upgraded.
