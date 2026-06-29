# E[K²]<∞ — partial-moment / tail-decay / longest-run audit of the jump-depth K (2026-06-30)

*WEAPONS_AUDIT-style. K = run-length of consecutive odd orbit values = 2-adic entry depth `v₂(c−1)`;
by `NONATOMIC_FIXEDPOINT.md`, `μ({1})=0 ⟸ mean depth bounded ⟺ E[K²]<∞`. Two sibling notes already
close the second-moment question: `EK2_SECOND_BUDGET.md` (verdict (b): no exact 2nd-moment identity)
and `EK2_TAIL_SEPARATION.md` (verdict (c): separation/BC can't bound the occupancy tail). THIS note
adds the **partial/fractional-moment** angle `E[K^{1+ε}]<∞` and a **sharp correction** to the
tempting "longest-run ⟹ max K = o(N)" route. SOUNDNESS PARAMOUNT; every line labelled; (K) NOT
claimed; willing to retract. Orbit `c_{n+1}=⌊3c_n/2⌋`, `c_0=8`. Numerics `.venv`, exact big-int,
N=10⁵, `ek2.py`/`ek2b.py`. NOT committed.*

---

## 0. One-line verdict

**Verdict (b), sharpened to "first-moment SUM is the only free fact".** No proven fractional moment
`E[K^{1+ε}]<∞` exists for ANY `ε>0`, and no proven tail-decay RATE on `P(K≥k)` beyond bare
summability. The longest-run literature (`L(8·3ⁿ)=o(n)`, Spiegelhofer–Wallner) **does NOT even apply
to the orbit**: the iterated-floor orbit `cₙ` is NOT the top bits of `8·3ⁿ` (verified: they diverge
from `n=6`, 54/60 mismatched in `n<60`), so its run-length `K=v₂(cₙ−1)` is governed by `cₙ mod 2ᵏ`
(the Mahler vertex), not by the bit-runs of the standalone power — hence even **max Kᵢ = o(N) is
OPEN/OBSERVED, not proven-in-lit**; only the crude support bound `Kᵢ ≤ 0.585n` is proven. The single
unconditionally proven moment fact is the **first-moment SUM** `Σ Kᵢ = #{dₙ≥1} ≤ N` (a trivial count,
exact via the valuation budget); even the first-moment *mean* `E[K]=O(1)` is not a free limit theorem
— it implies `even-density ≥ 1/(E[K]+1) > 0`, which is itself OPEN (`EVEN_DENSITY_PARTIAL.md`: only
`#even ≥ c·log n` proven). The exact gap: a **pointwise tail-decay rate** `P(K≥k)=O(k^{-(1+ε)})`
(equiv. `fₖ=O(k^{-(1+ε)})`), supplied by neither the exact first-moment budget nor any support bound —
it is the single-orbit equidistribution of `cₙ mod 2ᵏ` = (K)-adjacent.

---

## 1. What K is, exactly, and the moment ladder [PROVEN]

**Countdown Lemma [PROVEN, verified 0 exceptions, `MINPROP_RUNS.md`/`NONATOMIC_FIXEDPOINT.md`].**
For odd `c` with `d:=v₂(c−1)=a≥1`, the successor `c'=⌊3c/2⌋=(3c−1)/2` has `c'−1=3(c−1)/2`, so
`v₂(c'−1)=a−1`. Hence the orbit visits depth `≥1` only in **contiguous countdown runs**: a run of
**entry depth K** realises depths `K,K−1,…,1`, then an even step (`d=0`). Therefore

> **K = run-length of consecutive odd values = v₂(c_start−1)**  [PROVEN; verified run-length =
> v₂(c_start−1) for all 25025 runs in N=10⁵, 0 violations].

**The moment ladder (sum form, sidesteps the renewal-mean subtlety of §4).** With `dₙ=v₂(cₙ−1)`:

| moment | sum identity | status |
|---|---|---|
| `p=1` (count) | `Σᵢ Kᵢ = #{n<N: dₙ≥1} ≤ N` (`+O(log N)`) | **[PROVEN]** — trivial count = valuation budget |
| `1<p<2` (fractional) | `Σᵢ Kᵢ^p` = `O(N)`? | **[OPEN]** (this note) — no proven ε |
| `p=2` (energy) | `Σᵢ Kᵢ² = 2Σₙdₙ − #{dₙ≥1}` `= O(N)` ⟺ mean depth bounded ⟺ `E[K²]<∞` | **[OPEN]** = `μ({1})=0` precursor |

`Σₙ dₙ = ½(ΣKᵢ² + ΣKᵢ)` exactly (geometric run-sum, `EK2_SECOND_BUDGET §2`), so mean depth
`Σₙdₙ/N = O(1) ⟺ ΣKᵢ² = O(N) ⟺ E[K²]<∞`.

---

## 2. Is E[K²]<∞ equivalent to a known statement? The longest-run route FAILS for the orbit

**(i) E[K²]<∞ is NOT the longest-run statement, and is NOT a known literature object.** It is the
occupancy-tail summability `Σₖ fₖ < ∞` (`fₖ=freq{cₙ≡1 mod 2ᵏ}`), a **frequency/tail** statement,
sitting strictly:
> `(K)` [fixes `fₖ=2⁻ᵏ` ∀ residues]  ⟹  **E[K²]<∞** [`Σfₖ<∞`]  ⟹  `μ({1})=0` [`fₖ→0`, i.e. `inf fₖ=0`].
It is a genuinely intermediate rung with no named-literature equivalent except as a fragment of
single-orbit equidistribution.

**(ii) [PROVEN-in-lit, but the wrong axis] `L(M·3ᴷ) ≤ ηK+o(K)` (Spiegelhofer–Wallner 2025,
arXiv:2501.00850 Lemma 4.1, Schlickewei subspace theorem)** bounds the longest run of identical *bits
of the standalone integer* `M·3ᴷ`; with `M=8`, `L(8·3ⁿ)=o(n)`. `DIGITS_OF_3N.md` already noted this
is a horizontal run, not the diagonal density.

**(iii) [NEW, decisive — the route fails earlier than expected] The longest-run bound does not even
APPLY to the orbit's K.** A tempting argument runs: "`cₙ = ⌊8·3ⁿ/2ⁿ⌋` = top bits of `8·3ⁿ`, so the
low-bit zero-run of `cₙ` (= `K−1`) is a bit-run of `8·3ⁿ`, hence `Kₙ ≤ 1+L(8·3ⁿ)=o(n)`, hence
`max Kᵢ = o(N)` [PROVEN-in-lit]." **This is FALSE because the orbit is iterated-floor, not the
standalone power:** `⌊3⌊3c/2⌋/2⌋ ≠ ⌊9c/4⌋`. Verified (`ek2b.py`):

| n | `cₙ` (iterated) | `⌊8·(3/2)ⁿ⌋` = top bits of `8·3ⁿ` | equal? |
|---|---|---|---|
| 5 | 60 | 60 | yes |
| 6 | **90** | **91** | **NO** |
| 10 | 454 | 461 | no |
| 19 | 17434 | 17734 | no |

They diverge from `n=6` and stay divergent (54/60 mismatched in `n<60`). Since `v₂` is 2-adically
discontinuous, `v₂(cₙ−1)` (orbit run-length) has **no relation** to `v₂(⌊8·3ⁿ/2ⁿ⌋−1)` or to the
bit-runs of `8·3ⁿ`. So the subspace-theorem bound governs a *different integer sequence*; the orbit's
`K=v₂(cₙ−1)` is governed by `cₙ mod 2ᵏ` — single-orbit equidistribution of the iterated map = the
Mahler/parity-complexity vertex (`LIMIT_THEOREM §3″`, `DIGITS_OF_3N`).

**Consequence:** even `max Kᵢ = o(N)` is **OPEN / OBSERVED** (`M(N)≈log₂N` numerically), **not
proven-in-lit**. The only PROVEN max bound for the orbit is the crude support bound
`Kₙ = v₂(cₙ−1) ≤ ⌊log₂cₙ⌋ ≈ 0.585n` (`VALUATION_BUDGET.md`). *(This corrects the premise of the
ask; `NONATOMIC §4` is consistent — it cites `M(N)≈log₂N` as OBSERVED, never as proven.)*

---

## 3. Any proven partial moment E[K^{1+ε}]<∞ or tail-decay rate? — NO, with proof

**(a) No fractional moment for any ε>0 [PROVEN negative, from the only available inputs].** The best
proven envelope is `Kᵢ ≤ 0.585n` (support) and `ΣKᵢ ≤ N` (count). For any `ε>0`,
> `Σᵢ Kᵢ^{1+ε} ≤ (max Kᵢ)^ε · Σᵢ Kᵢ ≤ (0.585N)^ε · N = 0.585^ε · N^{1+ε}`,
so the proven bound only gives `Σ Kᵢ^{1+ε} = O(N^{1+ε})`, a factor `N^ε` above the `O(N)` needed for
`E[K^{1+ε}]<∞`. **Even the (unproven) `max K=o(N)` would not help:** with `max K = g(N)=o(N)`,
`ΣK^{1+ε} ≤ g(N)^ε·ΣK ≤ g(N)^ε·N`, which is `O(N)` only if `g` is *bounded* — false. A single run of
length `g(N)=N/log N` (allowed by `o(N)`) already gives `ΣK^{1+ε} ≥ (N/log N)^{1+ε} ≫ N`. **So no
support/max bound, however good short of `O(1)`, yields any fractional moment.** The gap above the
first moment is **total**: a moment bound `>1` requires a *frequency/tail* input, which a support
bound structurally cannot provide. *(This is why interpolation/Hölder between `E[K]` and `E[K²]` buys
nothing — Hölder needs two genuine `Lᵖ` norms; here only `L¹`-sum `≤N` and `L^∞≤0.585n` are proven,
and `L^∞` is just the support.)*

**(b) Tail decay: only bare summability, no rate [PROVEN extent + PROVEN obstruction].** `E[K]<∞`
(the renewal first moment, *where it holds* — see §4) gives `Σₖ P(K≥k) = E[K] < ∞`, hence
`P(K≥k)` is summable and `→0`. But summability is **not a pointwise rate**: e.g.
`P(K≥k)=1/(k log²k)` is summable yet `Σₖ kᵉ P(K≥k)=∞` for every `ε>0` — so summability alone forces
**no** fractional moment. The needed `E[K^{1+ε}]<∞ ⟺ Σₖ k^ε P(K≥k) < ∞` (weaker than
`E[K²]=Σₖ k·P(K≥k)`), interpolating strictly between first and second moment — is exactly the missing
decay RATE.

---

## 4. Does E[K]<∞'s exactness force any E[K²]/tail decay? — NO; and even E[K]<∞ is not free in the limit

**The first-moment budget is EXACT but is a COUNT, carrying no tail rate [PROVEN].** The valuation
budget `Σ_{odd i<n} v₂(3cᵢ−1) = n + v₂(cₙ) − v₂(c₀)` (and its depth form `ΣKᵢ = #{dₙ≥1}`) is an exact
identity. Its refill term is `#{dₙ≥1} ≤ N` — bounded by `N` for a reason **external to the orbit's
statistics** (you cannot have more than `N` positive-depth steps). Exactness pins the *value* of the
first-moment sum; it says **nothing** about how `ΣKᵢ` distributes across small vs large runs.
`EK2_SECOND_BUDGET §3` proves the sharp reason: any current-depth potential `Q(dₙ)` telescopes
`ΣKᵢ^p` into (countdown decrements) + (refill injections) which are the SAME `p`-th moment — the
identity **closes on itself** (`0=0`), free at `p=1` (refill = count `≤N`) and `(K)`-hard at `p=2`
(refill = `Σdₙ` itself, no `O(N)` cap). So **budget exactness does not force `P(K≥k) ≤ C/k²`** or any
decay; a single `K≈0.585N` run is consistent with every proven identity and gives `E[K²]=∞`,
`μ({1})≥0.585`.

**Sharper: even `E[K]<∞` (the MEAN, in the limit) is not unconditionally proven [PROVEN reduction].**
The *free* fact is only the first-moment **SUM** `ΣKᵢ ≤ N`. The first-moment **mean**
`E[K]=ΣKᵢ/R` (`R=#runs`) being `O(1)` requires `R=Ω(N)` refills, and
> `E[K]<∞ ⟹ #even ≥ R−1 ≥ ΣKᵢ/E[K] − 1 ≥ (N−#even)/E[K] − 1 ⟹ even-density ≥ 1/(E[K]+1) > 0.`
Since positive **even-density is OPEN** (`EVEN_DENSITY_PARTIAL.md`: only `#even ≥ c·log n ≈ 0.89·log₂n`
is proven, and `even-density→0` is *marginally consistent* with all proven growth constraints),
the limit-finiteness of `E[K]` is **at least as hard as even-density > 0**, hence also OPEN. The prompt's
"`E[K]` PROVEN ≈2" holds only in the exact-accounting / finite-N-tautology sense (`ΣKᵢ≤N` + observed
`R/N≈0.25`), **not** as a proven limit theorem. *(So the true PROVEN/OPEN line sits one notch lower
than usually stated: the first-moment SUM is free; the first-moment MEAN already buys the open
even-density positivity; the second moment is the `(K)`-adjacent wall.)*

---

## 5. The exact gap

> **A pointwise tail-decay rate `P(K≥k) = O(k^{-(1+ε)})` (equivalently `fₖ = O(k^{-(1+ε)})`), for any
> `ε>0`.** This is what separates the available facts (exact first-moment SUM `≤N`; crude support
> `K≤0.585n`; bare summability of `P(K≥k)` *where* `E[K]<∞`) from any moment above the first.
> Neither the EXACT first-moment budget (a count, self-closing telescope) nor any support/max bound
> (even the conjectural `max K=o(N)`) supplies a rate — a rate is a **frequency** statement, i.e. the
> single-orbit equidistribution of `cₙ mod 2ᵏ` (would give the geometric `fₖ≈2⁻ᵏ`, `P(K≥k)≈2⁻ᵏ`,
> all moments finite). That is the open Mahler `(3/2)ⁿ` kernel, (K)-adjacent.

---

## 6. Verdict (a)/(b)/(c)

| option | status |
|---|---|
| **(a)** proven partial moment `E[K^{1+ε}]<∞` or tail-decay rate ⟹ a `μ({1})=0` partial | **NOT achieved** — §3 proves no support/count input yields any `ε>0`; §4 proves exactness gives no rate |
| **(b)** only first-moment proven, `E[K²]` (and all `E[K^{1+ε}]`) open, with precise reason | **THIS** — precise reason = a tail-decay rate, unreachable from count/support inputs (§3,§4,§5); sharpened: even `E[K]<∞`-in-limit reduces to the open even-density>0 (§4) |
| **(c)** reduces to (K) | the missing rate **is** single-orbit equidistribution of `cₙ mod 2ᵏ` = Mahler/(K)-adjacent (§5) — (b) bottoms out here, consistent with `EK2_TAIL_SEPARATION`, `EK2_SECOND_BUDGET` |

---

## 7. Numerics [OBSERVED, exact big-int, N=10⁵, `ek2.py`/`ek2b.py`]

- 25025 runs; **E[K]=1.9916, E[K^1.5]=3.2657, E[K²]=5.9181** — all stable across prefixes
  (¼N..N: E[K²]=6.08, 5.95, 5.92, 5.92); max K = 20 ≈ log₂N=16.6 (≪ 0.585N=58500). even-density=0.5016;
  R/N=0.2502.
- **Sum forms per N (target = O(1)):** `ΣK/N=0.498` (≤1 trivially, PROVEN); `ΣK^{1.5}/N=0.817`;
  `ΣK²/N=1.481` (= 2·mean-depth−…; OBSERVED bounded, unbounded by proof). Crude cap
  `max K^ε·ΣK/N`: ε=0.5 → 2.23, ε=1.0 → 9.97 (the proven envelope is loose by the `N^ε` factor of §3).
- **Tail `P(K≥k)` geometric ≈2⁻ᵏ** (`P(K≥k)/2⁻ᵏ`≈1.0–1.05 to k≈8); weighted `k²·P(K≥k)` peaks 2.26 at
  k=3 then decays (→ `E[K²]` numerically convergent); `k^{1.5}·P(K≥k)` peaks 1.41 — all consistent with
  `E[K²]<∞` and every fractional moment finite, **evidence not proof** (the equidistribution-flavoured
  data finite N cannot upgrade).
- **Longest-run route correction:** iterated orbit `cₙ ≠ ⌊8(3/2)ⁿ⌋` from n=6 (54/60 divergent);
  `L(8·3ⁿ)`-bound does not bound `v₂(cₙ−1)`.

---

## 8. Sources

- `NONATOMIC_FIXEDPOINT.md` — reduction `μ({1})=0 ⟺ fₖ→0 ⟸ Σfₖ<∞ ⟺ E[K²]<∞`; mean-depth identity;
  first-vs-second-moment gap; `M(N)≈log₂N` OBSERVED (not proven).
- `EK2_SECOND_BUDGET.md` — verdict (b): no exact 2nd-moment identity; state-depth potentials telescope
  `ΣK^p` to itself; `p=1` free count, `p=2` `(K)`-hard.
- `EK2_TAIL_SEPARATION.md` — verdict (c): separation/anti-clustering/BC cannot bound `Σfₖ`; countdown
  forces min index-gap=1; reduces to refill-law genericity.
- `VALUATION_BUDGET.md` — PROVEN exact first-moment budget `Σ_{odd}v₂(3cᵢ−1)=n+v₂(cₙ)−v₂(c₀)`; crude
  range `Kᵢ ≤ 0.585n`; `avgD_odd≥3/2` form.
- `EVEN_DENSITY_PARTIAL.md` — `#even ≥ c·log n` PROVEN; positive even-density OPEN (marginal with
  `even-density→0`). [Used in §4: `E[K]<∞ ⟹ even-density>0`.]
- `MINPROP_RUNS.md` — Countdown Lemma `φ→φ−1` [PROVEN]; run⟺thin-cylinder; renewal closed form
  `freq(D=1)=1−1/E_deep`, no one-sided margin.
- `DIGITS_OF_3N.md` — longest-run `L(M·3ᴷ)≤ηK+o(K)` (Spiegelhofer–Wallner 2025, arXiv:2501.00850
  Lemma 4.1, Schlickewei subspace theorem); horizontal-run, not occupancy.
- `LIMIT_THEOREM.md §3″` — parity subword complexity; `p(ℓ)=2ℓ` ⟺ single-orbit equidist. = Mahler.
- Numerics: `scratchpad/ek2.py`, `ek2b.py` (exact big-int; moments, tail, fractional sums,
  orbit-vs-power divergence; N=10⁵).

---

No machine decided. No label upgraded.
