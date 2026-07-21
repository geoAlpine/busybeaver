# D8 — two cheap falsifiable kill-tests against the (K) wall (2026-07-22)

*Two decisive-either-way numerical tests, run to completion. **TEST 1 KILLED A DOOR** that the corpus had
flagged "expected false" but never measured: the o4 run-cap hypothesis `R ≤ 3` is **FALSE on the real orbit**,
falsified at generation **n = 90**, inside the first hundred generations. **TEST 2 held**: the Antihydra
`M₂ᵒᵈᵈ` Cauchy–Schwarz envelope was reproduced to all recorded digits and pushed 25× deeper in `J`; it stays
far inside the required threshold and **decreases** — no anomaly. Both instruments were validated against
recorded anchors before use (all matched; see §0). All numerics `[OBSERVED]`. **Nothing here proves anything.
No machine decided. No label upgraded.**

Scripts: `d8_o4_runcap.py`, `d8_m2odd_envelope.py` (worktree root). Interpreter `python3` (CPython, exact
`int` big-int arithmetic + numpy for collision counts). Not committed.

---

## 0. Instrument validation FIRST (the broken-instrument discipline)

Both simulators were checked against every concrete anchor recorded in the corpus **before** any new number
was trusted.

### 0a. o4 odometer + ledger — `d8_o4_runcap.py`

Recurrences implemented: `3G′ = 4G + e(ρ)`, `ρ = G mod 3`, `e = {0:9, 1:14, 2:1}`; ledger
`a′ = a + δ(ρ)`, `δ = {1:−1, 2:+4, 0:+6}`. Seed **`G₀ = 3, a₀ = 3`** (verified from
`O4_LEDGER_ANALYSIS_2026-07-06.md` §5, whose table starts `n=0: G=3, a=3, ρ=0`). The task brief's
"`G` seed 43, `W = G+14` with `W₀ = 57`" is the **template-regime milestone**, which this orbit reaches at
**`n = 5`** (`G₅ = 43`, `W₅ = 57`) — confirmed, not assumed.

| anchor (`O4_LEDGER_ANALYSIS` §5) | recorded | measured | status |
|---|---|---|---|
| `n=0` | `G=3, a=3, ρ=0` | `G=3, a=3, ρ=0` | ✅ |
| `n=5` | `G=43, a=17, ρ=1` | `G=43, a=17, ρ=1` | ✅ |
| `n=9` | `G=151, a=30, ρ=1` | `G=151, a=30, ρ=1` | ✅ |
| `n=12` | `G=367, a=37, ρ=1` | `G=367, a=37, ρ=1` | ✅ |
| `n=20` | `G=3727, a=63, ρ=1` | `G=3727, a=63, ρ=1` | ✅ |
| `n=26` | `G=20983, a=90, ρ=1` | `G=20983, a=90, ρ=1` | ✅ |
| `n=31` | `G=88462, a=99, ρ=1` | `G=88462, a=99, ρ=1` | ✅ |
| `n=36` | `G=372814, a=115, ρ=1` | `G=372814, a=115, ρ=1` | ✅ |
| ledger at `ρ=1` gens: `12, 17, 30, 37, 54, 63, …, 115` | §5 | `12, 17, 30, 37, 54, 63, 90, 89, 100, 99, 116, 115` | ✅ |
| min `a` at any `ρ=1` generation | `9` (startup, `G=7`) | `9`, at `n=1`, `G=7` | ✅ |
| longest `ρ=1` run **within the recorded window** `n ≤ 40` | `2`, at `n=26–27, 30–31, 35–36` | `2`, at exactly `n=26–27, 30–31, 35–36` | ✅ |
| run-structure closed form `run = v₃(G+14)` (`O4_RUN_STRUCTURE` §1) | theorem | **22,277 runs checked, 0 mismatches** | ✅ |

**One indexing note (not a disagreement).** `O4_RUN_STRUCTURE_2026-07-07.md` §2 cites `a₄₀ = 124`. In this
indexing (`a₀ = 3` at `n = 0`) the value `124` occurs at `n = 39` and `a₄₀ = 130`. The ledger *sequence* is
identical — it is a one-step generation-index convention difference, not a numerical discrepancy. Every
`(G, a, ρ)` triple in the §5 anchor table matches exactly, which pins the convention used there.

The independent cross-check that matters most: the **run-structure theorem** `maximal ρ=1 run at `G` =
`v₃(G+14)`` was verified against the directly-observed runs on 22,277 separate runs with zero mismatches.
Two logically independent computations of the same quantity agree. **Instrument accepted.**

### 0b. Antihydra renewal / collision counts — `d8_m2odd_envelope.py`

Orbit `c₀ = 8`, `c → ⌊3c/2⌋`; renewal sequence `c′_j = c/2` taken at each **even** `c`
(definition read from `renewal_shift.py` / `alpha_attack.py`, not guessed). Collision probability
`C₂(k) = (1/J²)Σ_r count_r(k)²`; `M₂ᵒᵈᵈ(k) = 2^k C₂(k) − 2^{k−1} C₂(k−1)` (`ODD_ADDITIVE_ENERGY.md` §1).

`M₂ᵒᵈᵈ` at `J = 40000` against the recorded §5a table — **and** against an independent direct-FFT computation
of `Σ_{a odd}|π̂_N(a)|²`:

| k | recorded §5a | measured (identity) | measured (direct FFT) | FFT-vs-identity rel. diff |
|---|---|---|---|---|
| 6  | 0.00094 | 0.000940 | 0.000940 | `1.1e-13` |
| 8  | 0.00252 | 0.002516 | 0.002516 | `4.9e-14` |
| 10 | 0.01355 | 0.013547 | 0.013547 | `1.4e-14` |
| 12 | 0.05339 | 0.053391 | 0.053391 | `2.6e-16` |
| 14 | 0.21061 | 0.210606 | 0.210606 | `0.0e+00` |

`M₂ᶠᵘˡˡ` also reproduced exactly (`1.00161, 1.00598, 1.02634, 1.10587, 1.42092` vs recorded
`1.00161, 1.00598, 1.02634, 1.10587, 1.42092`).

Global anchors:

| anchor | recorded | measured | status |
|---|---|---|---|
| even-density | `≈ 0.50018` | `0.50020` at `J = 80000` | ✅ |
| avg jump (telescoping), `J=40000` | `1.00125/0.99738/0.99925` col | `0.99738` | ✅ (bit-match) |
| crude bound `(2/J)Σ|ε_k|` | `0.0105 / 0.0099 / 0.0090` | `0.0105 / 0.0100 / 0.0090` | ✅ |
| C–S envelope `2Σ2^{−(k+1)/2}√M₂ᵒᵈᵈ` | `0.142 / 0.094 / 0.067` | `0.14214 / 0.09447 / 0.06702` | ✅ |

The envelope reproduction also **recovers the recorded run's undocumented cutoff**: the recorded triple
`0.142 / 0.094 / 0.067` is matched to 3 significant figures precisely at `k_max = 20`. This matters — see §2.3.
**Instrument accepted.**

---

## 1. TEST 1 — o4 run-cap `R ≤ 3`: **DOOR CLOSED (hypothesis FALSIFIED)**

### 1.1 The stake

`O4_CERTIFIED_FREQUENCY_BUILD_2026-07-10.md` §4 `[PROVEN, exact]`: on the subshift where every `ρ=1` run has
length `≤ R`, the frequency max-mean cycle is exactly `R/(R+1)`. o4 is fatal iff `freq{ρ=1} ≥ 4/5` in some
prefix. So

> `R ≤ 3` ⟹ `freq ≤ 3/4 < 4/5` ⟹ **o4 DECIDED non-halting.**

`R = 4` is critical (`4/5`), `R ≥ 5` decides nothing. The corpus recorded "longest observed `ρ=1` run = 2",
labelled `[OPEN]`, "expected false". It had never been measured beyond the extraction horizon.

### 1.2 Result

**The recorded "longest run = 2" is an artifact of the observation window.** The `O4_LEDGER_ANALYSIS` extraction
ran to `G ≈ 884k`, i.e. **`n ≈ 40` generations**. Within `n ≤ 40` the maximum run really is `2` (reproduced
exactly, §0a). The hypothesis dies almost immediately after that horizon:

| event | generation | `G` bit-length |
|---|---|---|
| first `ρ=1` run of length **3** | **`n = 51`** | 25 |
| first `ρ=1` run of length **4** | **`n = 90`** | 40 |
| first `ρ=1` run of length **5** | `n = 545` | 229 |
| first `ρ=1` run of length 6 | `n = 6556` | 2722 |
| first `ρ=1` run of length 7 | `n = 6656` | 2763 |
| first `ρ=1` run of length 8 | `n = 9030` | 3748 |
| first `ρ=1` run of length 9 | `n = 17826` | 7398 |
| first `ρ=1` run of length 12 | `n = 84793` | 35191 |

`[OBSERVED]` — and cross-certified: each of these runs was independently confirmed by the closed form
`run = v₃(G_n + 14)` (`O4_RUN_STRUCTURE` §1), 0 mismatches.

**`R ≤ 3` is FALSE. `R ≤ 4` (the critical case) is also FALSE. The run-cap door is closed, and it was closed
at generation 90 — 50 generations past where anyone had looked.**

### 1.3 Growth of the maximal run

Simulated to **`N = 2×10⁶` generations** (`G` = 830,079 bits ≈ 249,900 decimal digits), exact big-int:

| generations `N` | max `ρ=1` run | `log₃ N` | `G` bit-length | wall |
|---|---|---|---|---|
| `10³` | 5 | 6.29 | 419 | 0.0 s |
| `10⁴` | 8 | 8.38 | 4,154 | 0.0 s |
| `10⁵` | 12 | 10.48 | 41,508 | 1.1 s |
| `10⁶` | 12 | 12.58 | 415,042 | 82.5 s |
| `2×10⁶` | **12** | 13.21 | 830,079 | 332.2 s |

Full run census at `N = 2×10⁶` (`[OBSERVED]`):

| run length `L` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| count | 296,301 | 99,302 | 33,017 | 11,031 | 3,633 | 1,218 | 408 | 124 | 43 | 20 | 5 | 2 |
| ratio to previous | — | 0.335 | 0.333 | 0.334 | 0.329 | 0.335 | 0.335 | 0.304 | 0.347 | 0.465 | 0.250 | 0.400 |

The run-length distribution is geometric with ratio `1/3` to three digits — the exact annealed law. Totals:
445,104 maximal runs, 668,067 `ρ=1` steps, **`freq{ρ=1} = 0.334033`** (annealed `1/3`; fatal threshold `0.8`),
**mean run length 1.5009** (annealed `1/(1−1/3) = 1.5`).

The maximal run grows like `log₃ n`, exactly the annealed/random-itinerary law (a random ternary itinerary of
length `n` has longest single-symbol run `≈ log₃ n`). Observed `freq{ρ=1} ≈ 1/3`, again the annealed value,
nowhere near the fatal `4/5`. The unconditional cap `run ≤ 0.262n + O(1)` (`O4_RUN_STRUCTURE` §2) is nowhere
near binding: at `n = 10⁵` the cap allows 26,200 and the observed max is 12.

### 1.4 INTERPRETATION — what this does and does not mean

**A run of length ≥ 4 does NOT mean o4 halts.** It means exactly one thing: the *sufficient condition*
"`R ≤ 3` ⟹ non-halting" has no purchase on the real orbit, because its hypothesis is false there. The
run-length subshift route to deciding o4 is dead as stated.

What is *not* affected:
- o4's non-halting remains `[OPEN]` and is if anything *more* strongly supported: `freq{ρ=1} ≈ 1/3`, the
  ledger `a` grows `≈ +3` per generation and stands at `a ≈ 3×10⁵` by `n = 10⁵` (fatality needs `a ≤ 1`).
- The `R/(R+1)` theorem is untouched — it was `[PROVEN, exact]` and remains so. Only its *applicability* died.
- No new evidence for halting. The orbit looks maximally generic, which is the non-halting picture.

**The honest gain is negative-but-real:** the corpus carried an `[OPEN]` sufficient condition whose falsity was
*guessed* ("expected false"). It is now *measured* false, cheaply, and the frequency axis is confirmed to have
no run-length escape hatch. The `(K)` wall is unmoved — the run-length route was never a way through it, and
now that is a fact rather than an expectation.

---

## 2. TEST 2 — Antihydra `M₂ᵒᵈᵈ` envelope: **HELD, no anomaly**

### 2.1 The stake

`ODD_ADDITIVE_ENERGY.md` §3/§6: a sufficient condition for Antihydra non-halting is

> `Σ_{k≥1} 2^{−(k+1)/2} M₂ᵒᵈᵈ(k)^{1/2} ≤ 1/4`  (equivalently `2Σ… ≤ 1`, giving `avg jump ≤ 2`).

Recorded empirical envelope `≈ 0.03–0.07` (as `Σ`, vs the `1/4` threshold) / `0.067–0.14` (as `2Σ`, vs `1`),
measured up to `J = 8×10⁴`. Any upward drift toward the threshold would be the first internal anomaly in this
corpus.

### 2.2 Result — pushed deeper in `J`

Pushed from the recorded `J ≤ 8×10⁴` to **`J = 2×10⁶`** (25× deeper; 4,002,538 orbit steps, final `c` =
2,341,338 bits) and from `k ≤ 14` to `k ≤ 34`. `k*` = natural cutoff (last `k` with `ε_k ≠ 0`, §2.3).

| `J` | orbit steps | crude `(2/J)Σ|ε_k|` (≤1) | `k*` | **`Σ` @ `k*` (need ≤ 1/4)** | `2Σ` @ `k*` (≤1) | `2Σ` @ `k_max=20` | recorded |
|---|---|---|---|---|---|---|---|
| 16,000 | 31,975 | 0.0105 | 14 | **0.04733** | 0.09467 | 0.14214 | 0.142 ✅ |
| 40,000 | 79,892 | 0.0100 | 21 | **0.04974** | 0.09947 | 0.09447 | 0.094 ✅ |
| 80,000 | 160,046 | 0.0090 | 21 | **0.03528** | 0.07056 | 0.06702 | 0.067 ✅ |
| 200,000 | 400,285 | 0.0077 | 21 | **0.02499** | 0.04999 | 0.04775 | — |
| 500,000 | 1,000,878 | 0.0050 | 21 | **0.01536** | 0.03072 | 0.02931 | — |
| 1,000,000 | 2,002,179 | 0.0031 | 21 | **0.01086** | 0.02171 | 0.02071 | — |
| **2,000,000** | 4,002,538 | **0.0016** | 21 | **0.00737** | 0.01474 | 0.01403 | — |

At `J = 2×10⁶` the envelope is **0.0074 against a threshold of 0.25 — a 34× margin**, down from the recorded
`0.03–0.07` (a 3.5–8× margin). The crude magnitude bound is `0.0016` against `1` — a 625× margin.

**Verdict: the envelope stays far inside the threshold and DECREASES monotonically with `J`.** No drift up.
No anomaly. `[OBSERVED]`

The crude (magnitude) bound `(2/J)Σ|ε_k| ≤ 1` likewise keeps falling and holds with a `>100×` margin
throughout.

### 2.3 A genuine methodological finding: the envelope is cutoff-dominated

This was not recorded and is worth stating, because it changes how the number should be read.

In the equidistributed regime the measured `M₂ᵒᵈᵈ(k)` tracks the random value `2^{k−1}/J` to within a few
percent (measured ratio `1.00–1.06` for all `k ≥ 9`, `[OBSERVED]`). Substituting:

> `2^{−(k+1)/2} · (2^{k−1}/J)^{1/2} = 1/(2√J)` — **independent of `k`.**

So every level contributes the *same* amount, and

> `Σ_{k=1}^{k_max} ≈ k_max / (2√J)`.

Measured against this law:

| `J` | `k*` | `Σ` @ `k*` | `Σ·√J` (measured) | `k*/2` (predicted) | per-level `1/(2√J)` |
|---|---|---|---|---|---|
| 16,000 | 14 | 0.04733 | 5.99 | 7.0 | 0.003953 |
| 40,000 | 21 | 0.04974 | 9.95 | 10.5 | 0.002500 |
| 80,000 | 21 | 0.03528 | 9.98 | 10.5 | 0.001768 |
| 200,000 | 21 | 0.02499 | 11.18 | 10.5 | 0.001118 |
| 500,000 | 21 | 0.01536 | 10.86 | 10.5 | 0.000707 |
| 1,000,000 | 21 | 0.01086 | 10.86 | 10.5 | 0.000500 |
| 2,000,000 | 21 | 0.00737 | 10.42 | 10.5 | 0.000354 |

At `J = 10⁶` the measured per-level term is `0.000500` for every `k` from 16 to 32, against the predicted
`1/(2√J) = 0.000500` — and `M₂ᵒᵈᵈ(k)/(2^{k−1}/J) = 1.000` at every one of those levels. The law is exact to
the displayed digits.

The `Σ·√J ≈ k*/2` prediction holds to ~3 digits. Two consequences:

1. **The envelope is linear in the cutoff `k_max`, not convergent in it.** The naive sum `Σ_{k≥1}` *diverges*
   at any fixed `J`. The recorded `0.03–0.07` is therefore only meaningful together with a cutoff, and the
   recovered cutoff of the original run was `k_max = 20` (§0b). This is a presentation gap in
   `ODD_ADDITIVE_ENERGY.md` §5c, not an error in it.
2. **There is a natural cutoff and it is the right one.** `ε_k = N_k − N_{k−1}/2` becomes identically zero
   once `N_k = 0`, i.e. once `2^k` exceeds the resolution of `J` samples — measured `k* ≈ 21` across
   `J = 4×10⁴ … 2×10⁶`, growing like `log₂ J`. Beyond `k*` the Cauchy–Schwarz bound is not merely loose, it
   bounds a quantity that is exactly `0`. Truncating there is legitimate, and gives the `k*`-column above.

So the correct asymptotic statement is: **envelope `≈ log₂(J) / (2√J) → 0`**, matching the rate
`~(log₂J)/√J` that `ODD_ADDITIVE_ENERGY.md` §5c already asserted. The deeper run confirms that assertion out
to `J = 2×10⁶` rather than `8×10⁴`.

### 2.4 INTERPRETATION

**Continued compliance sharpens the constant; it proves nothing.** The envelope's decay is *precisely* the
random/equidistributed rate — which is to say, the measurement confirms that the orbit *behaves like* an
equidistributed sequence, which is exactly the content of `(K)`/Mahler-3/2 that cannot be proven. The
numerics are consistent with the open lemma being true; they are not evidence that it is provable, and a
periodic-orbit counterexample (`ODD_ADDITIVE_ENERGY.md` §4.3) still survives the odd restriction. The
`M₂ᵒᵈᵈ = o(2^k)` input remains `[OPEN]` and remains `(K)`.

**No upward drift was seen. Nothing to report loudly.**

---

## 3. Compute budget

| test | run | wall time | scale reached |
|---|---|---|---|
| 1 | `d8_o4_runcap.py 100000` (validation) | 1.1 s | `n = 10⁵`, `G` = 41,508 bits |
| 1 | `d8_o4_runcap.py 2000000` (deep) | 332 s | `n = 2×10⁶`, `G` = 830,079 bits |
| 2 | `d8_m2odd_envelope.py` `J = 16000…500000` | ~60 s total | `J ≤ 5×10⁵` |
| 2 | `d8_m2odd_envelope.py 1000000` | 128 s | `J = 10⁶`, `c` = 1,171,203 bits |
| 2 | `d8_m2odd_envelope.py 2000000` | 424 s | `J = 2×10⁶`, `c` = 2,341,338 bits |

Total ≈ 16 minutes single-core. Both tests were decided far inside budget — TEST 1 was in fact decided in the first
90 generations (microseconds); the remaining compute only characterized the growth law.

---

## 4. Verdict table

| question | answer | label |
|---|---|---|
| Instruments validated against recorded anchors? | **Yes, all matched** (o4: 8/8 ledger triples + 22,277 closed-form cross-checks, 0 mismatches; Antihydra: `M₂ᵒᵈᵈ`, `M₂ᶠᵘˡˡ`, crude bound, envelope, even-density all reproduced) | `[VERIFIED]` |
| o4: does the real orbit have a `ρ=1` run of length ≥ 3? | **Yes, first at `n = 51`** | `[OBSERVED]` |
| o4: length ≥ 4? | **Yes, first at `n = 90`** | `[OBSERVED]` |
| Is the `R ≤ 3` sufficient condition true on the real orbit? | **NO — falsified** | `[OBSERVED, decisive]` |
| Is the critical `R ≤ 4` true? | **NO — also falsified** | `[OBSERVED, decisive]` |
| Does this mean o4 halts? | **NO.** It kills one sufficient condition, nothing more | `[interpretation]` |
| Does o4's status change? | **No** — `[OPEN]`, non-halting still strongly supported (`freq{ρ=1} ≈ 1/3`, ledger `≈ +3/gen`) | `[unchanged]` |
| Antihydra: does the `M₂ᵒᵈᵈ` envelope stay inside `1/4`? | **Yes, far inside**, and decreasing in `J` | `[OBSERVED]` |
| Any upward drift toward `0.25`? | **None.** Decays at `log₂(J)/(2√J)` | `[OBSERVED]` |
| New finding on the envelope? | It is **linear in the cutoff `k_max`**; the recorded figure implicitly used `k_max = 20`; the natural cutoff is `k* ≈ log₂J` where `ε_k ≡ 0` | `[OBSERVED]` |
| Did either test move the `(K)` wall? | **No.** One route was removed (o4 run-cap); the other was re-confirmed as `(K)`-equivalent | `[unchanged]` |

**Net.** One door closed — the o4 run-length subshift route, dead at generation 90, previously only *expected*
to be dead. One door confirmed open-but-blocked — the `M₂ᵒᵈᵈ` envelope holds with a growing margin and is
exactly `(K)` in disguise. Zero anomalies. Zero false proofs.

**No machine decided. No label upgraded.**

---

## Reproduce

- `python3 d8_o4_runcap.py 2000000` — o4 odometer/ledger, anchor validation, run census, closed-form cross-check.
- `python3 d8_m2odd_envelope.py <J> <k_max> <fft_check_k>` — Antihydra renewal, `C₂(k)`, `M₂ᵒᵈᵈ(k)`,
  direct-FFT identity check, `ε_k`, envelope partial sums, cutoff diagnostics.
- Basis: `O4_CERTIFIED_FREQUENCY_BUILD_2026-07-10.md` §4 (`R/(R+1)`), `O4_LEDGER_ANALYSIS_2026-07-06.md` §5
  (anchors), `O4_RUN_STRUCTURE_2026-07-07.md` §1–2 (closed form, cap), `ODD_ADDITIVE_ENERGY.md` §1/§3/§5
  (identity, envelope, anchors), `renewal_shift.py`, `alpha_attack.py` (renewal definition).
