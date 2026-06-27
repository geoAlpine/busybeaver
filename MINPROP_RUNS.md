# Run-length structure of the SHALLOW set {D=1} = {o ≡ 1 mod 4} (2026-06-28)

*Angle: bound the occupancy of the shallow set `{D=1}={o≡1 mod4}` of the induced odd map
`T(o)=3^{D-1}(3o-1)/2^D`, `D=v2(3o-1)`, `o_0=27`, via the RUN structure of consecutive D=1 steps.
Target (robust form, `SESSION_2026-06-28_INDUCED_MAP.md`): `freq(D≥2)+freq(D≥3) ≥ 1/2`; tight form:
`freq(D=1) ≤ 1/2`. Numerics `.venv` only (`minprop_runs.py`), exact big-int orbit of o_0=27. Zero false
proofs. Every line labelled. NOT committed.*

---

## 0. One-line answer

A D=1 step is a **deterministic countdown**: it decrements `φ := v2(o−1)` by exactly 1. Hence a run of
`m` consecutive D=1 steps **⟺** the orbit sits in the thin cylinder `{o ≡ 1 mod 2^{m+1}}` (Haar measure
`2^{-(m+1)}`), and the maximal run length is `L = v2(o_start−1) − 1` exactly (numerics: **75139/75139
runs satisfy this with no exception**). The countdown is genuinely **self-limiting** (no infinite D=1
run is possible except at the 2-adic fixed point `o=1`, off-orbit). But it does **NOT** yield a one-sided
frequency bound for free: a telescoping/renewal identity gives the exact closed form
> **`[PROVEN]`  `freq(D=1) = 1 − 1/E_deep`,  where `E_deep = ` mean over deep (D≥2) steps of
> `v2(o_next−1)`;  equivalently  `freq(D=1) ≤ 1/2  ⟺  E_deep ≤ 2`.**

`E_deep` is the mean *entry valuation* refilled by deep steps = exactly the equidistribution/occupancy
quantity (Haar value 2). Numerics show `freq(D=1)` and `E_deep` **oscillate across `1/2` and `2` with NO
margin** (margin `−0.0004,+0.0017,−0.0015,−0.0003` at N=10k..600k). So the run/renewal argument
**reduces to conditional cylinder occupancy = single-orbit genericity = wall (A)** — confirming, not
breaching — but it produces a **sharper, sparser, closed-form target** (a conditional mean over only the
deep substeps, not all steps). The robust target `freq(D≥2)+freq(D≥3)≥1/2` keeps margin `≈0.247`
(observed `0.747`), being more fluctuation-tolerant, but is still an occupancy statement.

---

## 1. The exact residue automaton for D=1 steps `[PROVEN]`

Let `φ(o) := v2(o−1) ≥ 1` (well-defined for odd `o≠1`). Note `D=1 ⟺ o≡1 mod4 ⟺ φ(o) ≥ 2`, and
`D≥2 ⟺ o≡3 mod4 ⟺ φ(o)=1`.

> **Lemma (countdown).** If `φ(o)=a ≥ 2` (so `D=1`), then `T(o)=(3o−1)/2` and `φ(T(o)) = a − 1`.

**Proof.** Write `o = 1 + 2^a u`, `u` odd. Then `3o−1 = 2 + 3·2^a u = 2(1 + 3·2^{a−1} u)`, so
`D=v2(3o−1)=1` and `o' = (3o−1)/2 = 1 + 3·2^{a−1} u`. Since `3u` is odd, `v2(o'−1) = a−1`. ∎

So each D=1 step shifts the orbit from the cylinder `{o≡1 mod 2^a}` to `{o'≡1 mod 2^{a−1}}` (the "1"-bit
boundary climbs down by exactly one each step). Numerics §1 of the original residue note are consistent;
here verified directly along the orbit (next section).

---

## 2. Run ⟺ thin-cylinder relation `[PROVEN]` (exact, verified 75139/75139)

> **Proposition.** Starting at `o_start` (odd), the number of consecutive D=1 steps beginning at
> `o_start` is **exactly** `L = φ(o_start) − 1 = v2(o_start − 1) − 1`. Equivalently:
> *a run of `m` consecutive D=1 steps occurs at `o_start` ⟺ `o_start ≡ 1 mod 2^{m+1}`* (`φ ≥ m+1`),
> i.e. the orbit must lie in a cylinder of Haar measure `2^{-(m+1)}`.

**Proof.** By the Lemma, while `φ ≥ 2` (D=1 holds) the valuation decreases by 1 each step:
`φ(o_j) = φ(o_start) − j`. The D=1 condition `φ(o_j) ≥ 2` holds for `j = 0,1,…,φ(o_start)−2`, i.e. for
`φ(o_start)−1` steps; at `j = φ(o_start)−1` we reach `φ = 1` (`o≡3 mod4`), forcing `D≥2`. Hence the
maximal run length is `L = φ(o_start)−1`. A run of length `≥ m` therefore needs `φ(o_start) ≥ m+1`, i.e.
`o_start ≡ 1 mod 2^{m+1}`. ∎

**Constant `c`.** With `m`-run ⟺ `o ≡ 1 mod 2^{m+1}`, the cylinder has measure `2^{-(m+1)}` — so
`c = 1` in the prompt's "`measure 2^{-(m+c)}`". A run requires the orbit start in an **exponentially
thin** cylinder; the run length is the *deterministic* readout of the entry valuation.

**Self-limiting `[PROVEN]`.** Because `φ` strictly decreases on D=1 steps and is a non-negative integer,
**no infinite D=1 run exists** (it would force `φ=+∞`, i.e. the 2-adic fixed point `o=1`, not on the
orbit of `o_0=27`). Every run terminates in a deep (D≥2) step. So a long D=1 run **does** end by forcing
the very next step deep — but only **one** deep step is forced, which is not enough to bound the fraction
(see §3: deep runs are themselves geometric with the same mean).

**Numerics (orbit of o_0=27, N=300000).** Of all 75139 maximal D=1 runs, **every single one** satisfies
`L = v2(o_start−1) − 1` (0 exceptions). Longest run `L=19` arises exactly from `v2(o_start−1)=20`. The
run-length distribution is geometric: `frac(L=ℓ) ≈ 2^{-ℓ}` (`0.499, 0.250, 0.124, 0.065, 0.032, …`).

---

## 3. Does the run argument give a ONE-SIDED bound? — Renewal identity `[PROVEN]`, reduces to occupancy

**A naive renewal is WRONG.** One might pair each D=1 run with the deep step that ends it and conclude
`freq(D=1) ≤ 1/2 ⟺ E[run] ≤ 1`. This is **false**: deep steps also form runs (D≥2 can repeat), so
`#deep ≠ #shallow-runs`. Numerically the mean shallow run is `E[L] ≈ 2.0`, not `≤1` — yet
`freq(D=1) ≈ 1/2`, because the mean **deep** run is also `≈2.0` (geometric, p=1/2). The correct
statement is `freq(D=1) ≤ 1/2 ⟺ mean(shallow run) ≤ mean(deep run)`, both `≈2` with no margin.

**The exact telescoping identity `[PROVEN]`.** Track `φ_j = v2(o_j−1)`:
- D=1 step: `φ_{j+1} = φ_j − 1` (Lemma).
- deep step (`φ_j = 1`): `φ_{j+1} = v2(o_{j+1}−1) ≥ 1` (a "refill" of the valuation by fresh high bits).

Sum `Δφ` over `j=0..N−1`:  `φ_N − φ_0 = (−1)·N_1 + Σ_{deep}(φ_{j+1} − 1)`, where `N_1=#{D=1}`. Dividing
by `N` and using `φ_N/N → 0` (`φ = O(log N)`, bounded by max run +1):
> **`freq(D=1) = freq(deep)·(E_deep − 1)`,  `E_deep := ` mean over deep steps of `v2(o_next−1)`.**

Since `freq(deep) = 1 − freq(D=1)`, solving gives the **closed form**
> **`freq(D=1) = 1 − 1/E_deep`  ⟺  `freq(D=1) ≤ 1/2  ⟺  E_deep ≤ 2`.**

**Numerics (verified to 6 digits, multiple N).** The identity is exact:

| N | freq(D=1) | E_deep | 1 − 1/E_deep | margin (½ − freq) |
|---|---|---|---|---|
| 10000  | 0.500400 | 2.001601 | 0.500400 | −0.000400 |
| 40000  | 0.498250 | 1.993024 | 0.498250 | +0.001750 |
| 100000 | 0.499480 | 1.997962 | 0.499490 | +0.000520 |
| 300000 | 0.501537 | 2.006166 | 0.501537 | −0.001537 |
| 600000 | 0.500290 | 2.001167 | 0.500292 | −0.000290 |

**Conclusion (the central point).** `E_deep` is the **mean entry valuation refilled by deep steps** —
precisely a conditional cylinder-occupancy statistic. The countdown (§2) is self-limiting and ends every
run, but the *frequency* of D=1 equals `1 − 1/E_deep`, governed entirely by how high the deep steps
refill `φ` — which is the equidistribution/genericity quantity (Haar gives `E_deep = Σ_{a≥1} a 2^{-a}=2`
exactly). There is **NO one-sided margin**: `freq(D=1)` and `E_deep` oscillate across `1/2` and `2`
(signs `−,+,+,−,−`). **So the run/renewal argument does NOT give a one-sided bound; it reduces to the
conditional occupancy `E_deep ≤ 2` = single-orbit genericity = wall (A).** `[PROVEN reduction; OBSERVED
no margin]`

**No sub-stochastic domination `[PROVEN structural].** A pointwise one-sided bound would need
`v2(o_next−1) ≤` (something) deterministically after a deep step. But `o_next = 3^{D−1}(3o−1)/2^D` pulls
in fresh high bits and `v2(o_next−1)` is unbounded above (any cylinder reachable) — so neither the real
orbit dominates nor is dominated by a sub-stochastic chain. The refill law is the full Haar law or
nothing.

**Gain (honest).** The renewal does buy something real: it rewrites the all-steps target
`freq(D=1)≤1/2` as a conditional mean over **only the deep substeps** (`E_deep ≤ 2`), a sparser set, and
in **closed form** `freq(D=1)=1−1/E_deep`. This is the cleanest localization yet of the tight target,
matching `WALLB_VALUATION_SHARP §5`'s `E[D'|…]≤2` flat-conditional, now with an *exact identity* rather
than a heuristic.

---

## 4. The annealed Markov chain on `o mod 2^k` `[PROVEN value; a.e. only]`

Build the chain treating pulled-in high bits as Haar (the annealed chain). By the `[PROVEN]` Haar-
preservation + exactness of `T` on `Z_2^*` (`INDUCED_RESIDUE_STRUCTURE.md §2`), the stationary
distribution on odd residues `mod 2^k` is **uniform** (`2^{1−k}` each). Hence:
> **Annealed occupancy of `{o≡1 mod4}` = 1/2 exactly; annealed `freq(D=1) = 1/2`, `E_deep = 2`.**

**Is this a provable one-sided bound for the real orbit?** **No.** The annealed chain *assumes* Haar
high bits — exactly the genericity hypothesis. It is the Birkhoff/ergodic-average value, valid for
Haar-**a.e.** `o`, silent about the specified `o_0=27`. There is no sub-stochastic domination giving a
one-sided inequality (the real high bits are deterministic, neither ≤ nor ≥ Haar). So the annealed
prediction (1/2) is `a.e.`, not a `[PROVEN]` bound for `o_0`. `[PROVEN it is the a.e. value; OPEN for the
specific orbit]`.

---

## 5. Numerics summary (orbit of o_0=27, exact big-int, `minprop_runs.py`)

`[OBSERVED]` (N up to 600000):
- `freq(D=1) ≈ 0.5003`, oscillates across `1/2` (margin `±0.0017`) — **no robust one-sided margin** for
  the tight target.
- `mean D ≈ 2.00`; D-law geometric: `P(D=d) ≈ 2^{-d}` to 3 dp.
- **Run-length distribution geometric**: `frac(L=ℓ) ≈ 2^{-ℓ}`; **max run = 19** (N=3e5).
- **Run⟺cylinder exact**: `L = v2(o_start−1)−1` for **all** 75139 runs (0 fail). Longest runs trace to
  exactly `φ = L+1` (deterministic countdown confirmed for L = 19,15,14,13,12,11).
- **Renewal/closed form exact**: `freq(D=1) = 1 − 1/E_deep` to 6 digits at every checkpoint;
  `E_deep ≈ 2.00` oscillating across 2.
- `freq(o ≡ 1 mod 2^k) ≈ 2^{-(k-1)}` (Haar) for k=2..16 (deep cylinders rare, finite-N noise in tail).
- `o mod 4` occupancy `{1:0.498, 3:0.502}`, `o mod 8` `{1:.247,3:.253,5:.251,7:.249}` — equidistributed
  (OBSERVED, exactly what genericity predicts; not forced by structure).
- **Robust target** `freq(D≥2)+freq(D≥3) ≈ 0.747 ≥ 1/2` with margin `≈0.247` — robustly satisfied
  (still an occupancy statement, but fluctuation-tolerant).

---

## 6. Verdict (the prompt's asks)

| ask | answer | label |
|---|---|---|
| Exact "run of m D=1 ⟺ thin cylinder" relation | **Run of m ⟺ `o ≡ 1 mod 2^{m+1}` (measure `2^{-(m+1)}`, c=1); maximal `L = v2(o_start−1)−1`**, via the countdown Lemma `φ→φ−1`. Verified 75139/75139. | `[PROVEN]` |
| Does run-length/renewal give a one-sided `freq(D=1)` bound, or reduce to occupancy? | **Reduces to occupancy.** Exact identity `freq(D=1)=1−1/E_deep`, so `≤1/2 ⟺ E_deep≤2` where `E_deep` = mean deep-step refill valuation = the genericity quantity. No margin (oscillates), no sub-stochastic domination. Self-limiting countdown ends each run but does not bound the fraction. | `[PROVEN reduction; OBSERVED no margin]` |
| Annealed-chain occupancy + is it a provable bound? | **Annealed occupancy = 1/2 exactly** (uniform stationary law from Haar-preservation). **Not a provable bound** for `o_0` — it is the a.e./Birkhoff value; assuming Haar high bits = genericity; no domination. | `[PROVEN value; a.e. only]` |
| Numerics | run-length geometric, max 19, run⟺cylinder exact, closed form exact, `freq(o≡1 mod2^k)≈2^{-(k-1)}`, `freq(D=1)≈0.500` with no one-sided margin; robust target `0.747` margin `0.247`. | `[OBSERVED]` |

### Banked
- `[PROVEN]` **Countdown Lemma** `v2(o−1)=a≥2 ⟹ v2(T(o)−1)=a−1`, hence the **run⟺thin-cylinder** identity
  `L = v2(o_start−1)−1`.
- `[PROVEN]` **Renewal closed form** `freq(D=1) = 1 − 1/E_deep`, `E_deep =` mean deep-step refill
  valuation; the tight target `freq(D=1)≤1/2` is *exactly* `E_deep ≤ 2`, a conditional mean over the
  sparse deep-substep set — the sharpest localization of the tight target, an exact identity (no
  heuristic), matching `WALLB_VALUATION_SHARP §5`'s flat `E[D'|…]≤2`.

### Honest: this confirms, does not breach
The countdown is self-limiting and exact, but the D=1 *frequency* is `1−1/E_deep`, set by the refill law
of deep steps, which is Haar (a.e.) and unbounded pointwise — so it reduces to single-orbit genericity =
wall (A), with no one-sided margin for the tight form. The robust form `freq(D≥2)+freq(D≥3)≥1/2` keeps a
`0.247` margin and is the right primary target, but remains an occupancy/genericity statement.

Script: `minprop_runs.py` (scratchpad). Not committed.
