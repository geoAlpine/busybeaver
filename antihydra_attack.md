# Antihydra — attack notes (self-derived, 2026-06-22)

Working notes on attacking the BB(6) cryptid **Antihydra**
`1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` (halt = state F reads 0). Everything below was
re-derived from the raw transition table this session (the mechanism is also recorded in `antihydra.py`
and known to the bbchallenge community — these are *understanding* notes, not a new result, unless §5
yields one).

## 1. Mechanism (derived from simulation, verified)
The tape is always `0 1^a 0 0 1^b 0` — **two unary counters**:
- **b = the Hydra value, shifted: `c := b + 6` follows the clean map `c -> floor(3c/2)`** starting from
  `c = 8` (8,12,18,27,40,60,90,135,202,303,454,681,…). Verified: `c=b+6` matches the orbit exactly; the
  machine computes `floor(3c/2)` by an internal left/right sweep (the "countdown" seen between steps).
- **a = a balance counter.** Per Hydra step it changes **`+2` when `c` is even, `-1` when `c` is odd.**
- **Halt = the balance reaches `-1`** (state F reads 0). Equivalently: odds ever exceed twice the evens.

## 2. The clean reformulation (the key for the attack)
Let `E` = number of EVEN Hydra values in the first `n` steps. The balance is
```
   c_n = 2*E - (n - E) = 3E - n .
```
So **Antihydra HALTS  ⟺  c_n = -1 for some n  ⟺  3E = n-1  ⟺  the even-density E/n drops to ~1/3.**
Empirically the even-density is ≈ **0.499** (≈ 1/2). The whole question is whether it ever falls to 1/3.

## 3. What the simulation shows (the "probviously" made quantitative)
Abstract Hydra process (iterate `c->floor(3c/2)`, track the balance), 300k steps:
- **never halts**; balance `c=3E-n` climbs linearly (~`0.5 n`); its **minimum is `2`, reached at step 1**
  — it never dips again. Danger is only at the very start.
- longest run of consecutive ODD Hydra values: `8, 11, 20, 20` at `n = 1e3,1e4,1e5,3e5` — i.e.
  **odd-runs grow like `log2(n)`, NOT linearly.** To halt from balance `v` you need an odd-run of length
  `~v ≈ 0.5 n`; only `~log2 n` is ever available. The gap explodes.

## 3b. Why it (probably) never halts — the random-coin heuristic, made quantitative
Model the parities as a fair coin: `E ~ Binomial(n, 1/2)`, so `E` has mean `n/2` and std `sqrt(n)/2`.
Halting needs `E ≤ (n-1)/3` (§2), a **downward deviation of `n/2 - n/3 = n/6`**, i.e.
```
   sigma-to-halt(n) = (n/6) / (sqrt(n)/2) = sqrt(n)/3 .
```
This **grows without bound** — the orbit has to fall further and further below its mean to ever halt:

| `n`      | `sigma-to-halt = sqrt(n)/3` | `ln P(halt@n) ≈ -sigma²/2 = -n/18` |
|----------|------------------------------|------------------------------------|
| 1e3      | 10.5                         | −56                                |
| 1e5      | 105                          | −5 556                             |
| 1e9      | 10 541                       | −5.6e7                             |

So `P(halt at step n) ≲ exp(-n/18)`, and `Σ_n exp(-n/18)` **converges**. By Borel–Cantelli the orbit
**halts with probability 0** under the random model — and the entire non-negligible risk sits at tiny `n`
(while `sqrt(n)/3 = O(1)`, i.e. `n ≲ 9`), consistent with §3's "min-balance = 2, reached at step 1, never
again." **This is a heuristic, not a proof:** the orbit `floor(8·(3/2)^n)` is *deterministic*, not a coin.
Closing that gap — showing the real parities don't conspire to the rare `1/3` deviation — *is* the open §4
bound. The heuristic explains why everyone believes it never halts and why no one can prove it.

## 3c. Odd-runs are 2-adic, *exactly* — a conjecture-independent structural fact
§3 observed "longest odd-run grows like `log2 n`" empirically. That is now a **proven identity**, not a
heuristic. Let `T(c) = floor(3c/2)` and `v2(x)` = the 2-adic valuation (number of trailing binary zeros).

> **Lemma.** The odd run of Hydra values starting at `c` has length **exactly `v2(c-1)`**.

*Proof.* Let `L = v2(c-1)`, so `c = 1 + 2^L·m` with `m` **odd**. If `L ≥ 1` then `c` is odd and
`T(c) = (3c-1)/2 = 1 + 3·2^{L-1}·m`, hence `v2(T(c)-1) = (L-1) + v2(3m) = L-1` (because `3m` is odd). So one
`T`-step drops the valuation by **exactly 1**, and `c` stays odd exactly while `v2(c-1) ≥ 1`. Induction ⇒ the
run length is `v2(c-1)`. ∎  (Equivalently: for each `k` there is **exactly one** residue mod `2^k`, namely
`1`, that begins a run of length `≥ k` — verified by enumeration, density exactly `2^{-k}`; and all 50,034
maximal runs in the first `2·10^5` orbit steps satisfy it with zero violations.)

**Exact halting criterion.** Halting needs an odd run that drives the balance from `b` to `-1`, i.e. a run of
length `≥ b+1` while `balance = b`. By the Lemma:
```
   Antihydra HALTS  ⟺  ∃ n :  v2(c_n - 1)  ≥  balance_n + 1 ,   where balance_n = 3E_n - n.
```
So the whole question is **2-adic**: does the orbit `c_n = floor(8·(3/2)^n)` ever land within 2-adic distance
`2^{-(balance_n+1)}` of `1`? Empirically the gap `(balance_n+1) - v2(c_n-1)` has **minimum 3** over `n ≤ 2·10^5`
(again the danger is only at the very start). This **upgrades §3b**: the geometric tail `P(run ≥ k) = 2^{-k}`
is now *structural* (exactly one residue mod `2^k`), not a coin assumption — only the equidistribution of
`(3/2)^n` mod `2^k` (Mahler family) remains heuristic.

## 4. The (weaker) target the proof reduces to
Full equidistribution (even-density = 1/2 exactly) is **Mahler's 3/2 problem** (open). But halting only
needs the density to fall to **1/3**, so:
> **It suffices to prove the one-sided bound: even-density `E/n > 1/3` for all `n`.**
This is *weaker* than Mahler (one-sided, with a 1/2-vs-1/3 margin), but still a statement about the
2-adic distribution of `floor(8*(3/2)^n)` — the Mahler family. **Not solved; sharpened.**

### 4a. Summit attack (2026-06-23) — sharpened to a crisp conjecture-free open kernel
Three conjecture-free results pushing on §4 directly (all verified on the real orbit to `n=2·10^5`):
- **[PROVEN] mod-4 parity rule.** `c_{n+1}` is **even ⟺ `c_n ≡ 0 or 3 (mod 4)`** (odd ⟺ `c_n ≡ 1,2`).
  Equivalently `parity(c_{n+1}) = bit₀(c_n) ⊕ bit₁(c_n)`: the parity stream is the xor of the low two
  bits of the `×3/2` 2-adic odometer orbit — no finite-state reduction (the bits themselves carry).
- **[PROVEN] sharpened halt criterion.** Combining §3c (odd-run length `= v2(c−1)`, decreasing by 1 per
  step) with "halt needs an odd-run of length `≥ balance_n+1`":
  > **Antihydra HALTS ⟺ ∃n with `c_n ≡ 1 (mod 2^{balance_n+1})`** (the orbit lands on the residue `1`
  > to depth `balance_n+1`). Since `balance_n ~ n/2` and `c_n ~ 8(3/2)^n` has `~0.585n` bits, halting
  > demands the **low ~`n/2` bits of `c_n` be `0…01`** — half the bits forced to a single pattern.
- **[verified, conjecture-free DATA] the gap diverges.** Over `n ≤ 2·10^5`: `max_n v2(c_n−1) = 20`
  (at `n=67941`, `≈ log₂ n`), while the halt threshold `balance_n+1 ≈ n/2` (≈ 34000 there). The gap
  `(balance_n+1) − v2(c_n−1)` has **minimum 3, at `n=1`**, and grows like `n/2 − log₂ n → ∞`. No size
  obstruction kills it either (dimensionally `c_n ≡ 1 mod 2^{n/2}` is consistent: the odd cofactor would
  be `~8·(3/2^{3/2})^n = 8·(1.06)^n`, no contradiction) — so the gap is real but not closed by counting.
- **Open kernel, now crisp:** prove **`v2(c_n − 1) < balance_n + 1` for all `n`** — equivalently
  **odd-run lengths grow sub-linearly** (`= o(n)`; empirically `~log₂ n`). This is the entire remaining
  content of "Antihydra never halts", isolated to one 2-adic statement about the iterated orbit
  (`c_{n+1}=⌊3c_n/2⌋`, growth `~A(3/2)^n`, `A≈7.864`). Bounding `v2(c_n − 1)` unconditionally is the
  Mahler-family core — **the summit**. *(NB: `c_n ≠ ⌊8(3/2)^n⌋` for `n≥6` — see §4c correction.)*

### 4a′. Transfer-operator NO-GO (2026-06-23) — [PROVEN, conjecture-free] the dynamics alone bound nothing
A structural attack on the kernel, with a **proven negative**: no finite transfer operator / parity
automaton built from the map `T(c)=⌊3c/2⌋` can bound the even-density, because **the parity itinerary of
`T` is the full 2-shift**.
- **Engine lemma [PROVEN, verified 30000 cases].** For all integers `c` and `0 ≤ t ≤ j`:
  `T^t(c+2^j) − T^t(c) = 3^t · 2^{j−t}` (floors never interfere — both trajectories share parities until
  the gap's 2-adic valuation hits 0; this is the §3c "v2 drops by 1" mechanism). At `t=j` the gap is `3^j`
  (odd), so **flipping bit `j` of `c` flips the `j`-th parity bit `bit₀(T^j c)`**.
- **Consequence [PROVEN, verified: all 2^10 length-10 prefixes realized].** The coding
  `c ↦ (bit₀(T^n c))_{n≥0}` is **surjective onto `{0,1}^ℕ`** (measure-preserving onto Bernoulli(½)). So
  `T` realizes *every* parity sequence — including all-odd (the fixed point `T(1)=1`). Over the carry-free
  automaton on `ℤ/2^k` (free incoming top bit), the min-mean even-density is **0** and max is **1** (Karp,
  k=2..11): the recurrence permits **any** density in `[0,1]`.
- **Upshot.** Any proof of `even-density > 1/3` **must use the arithmetic of the specific point**
  `c_n = ⌊8·3^n/2^n⌋`, not the dynamics of `T`. This closes the "build a finite transfer operator
  yourself" route, complementing §4b (which closes the "stand on a published theorem" route). The summit's
  content is irreducibly the point-specific 2-adic behaviour of `8(3/2)^n`. (Reproduce: see the engine
  lemma + surjectivity check; both machine-verified this session.)

### 4b. Literature attack (2026-06-23, deep-research, 15 sources / 22 verified claims) — the summit is genuinely open, gap pinpointed
We searched the number-theory literature for an **unconditional** theorem that would bound the
even-density of `c_n = ⌊8(3/2)^n⌋`. Verdict (high confidence): **nothing known reaches even-density
`> 1/3`, or even any positive density lower bound.** The precise landscape:
- **Closest unconditional result — Flatto–Lagarias–Pollington (1995), Acta Arith. 70.** For coprime
  `p>q≥2`, the **range (spread = limsup − liminf) of `{ξ(p/q)^n}` is `≥ 1/(p−1)`** — for `3/2` this gives
  **spread `≥ 1/3`** (unconditional, via a finite-automata / de Bruijn-graph argument; `Ω(α)` is their
  inf-over-thresholds quantity). **But this is a RANGE bound, not a DENSITY bound.** It says the
  fractional parts cannot all huddle in a short interval; it says **nothing** about how *often* they land
  in a given half — which is exactly what Antihydra's parity/even-density needs. So **FLP does not apply.**
- **The gap, named:** Antihydra needs a *frequency/density* analogue of FLP's *range* `Ω(3/2)` — i.e. a
  lower bound on the **density** of `n` with `{8(3/2)^n}` in the even-half. **No such density analogue is
  known** (the literature's open question "frequency analogue of `Ω`?"). This is the missing piece.
- **Everything stronger is conditional.** Mahler's `Z`-number emptiness (no `ξ` with `{ξ(3/2)^n}<1/2 ∀n`)
  and the Strauch / Kahane–Pollington structural results are **conditional** (e.g. on the existence side),
  not unconditional density bounds. One 2024 arXiv attempt in this area (`2411.03468`) was **withdrawn by
  its author (v2, June 2025)** — do not rely on it.
- **Community status (bbchallenge wiki, `bbchallenge.org/antihydra`, sligocki "BB(6,2) is Hard" 2024-07,
  OEIS A385902).** Our reduction matches theirs exactly (orbit `a→⌊3a/2⌋` from 8; halt iff the odd/even
  balance hits the threshold). The **only basis for believing Antihydra never halts is the probabilistic
  heuristic** (our §3b) — there is **no known proof, partial or conditional, of its non-halting.** It is
  the canonical "hard" BB(6) machine.

**Upshot for the summit.** The literature attack is itself a result: it **closes off the "stand on a known
theorem" route** (no unconditional density bound exists) and **pins the missing piece precisely** — a
density/frequency analogue of the FLP range bound `Ω(3/2)`. Proving Antihydra non-halting is, today,
**not reducible to any published unconditional result**; it requires new mathematics of exactly that
"density-of-(3/2)^n-in-a-half" type (or our §4a kernel `v2(c_n−1)<balance_n+1 ∀n`, the same statement
2-adically). Honest end-state of the summit assault: the kernel is crisp, verified, and provably beyond
current literature.

### 4c. RETRACTED + corrected (2026-06-23) — the orbit is the ITERATED floor, not `⌊8(3/2)ⁿ⌋`; the new tool is the Φ-potential
> ⚠ **SOUNDNESS CORRECTION (a fan-out agent caught it; I verified).** The first version of §4c claimed
> `c_n = ⌊8·3ⁿ/2ⁿ⌋ = ⌊3ⁿ/2^{n−3}⌋` and reduced halting to a `3ⁿ mod 2ᵏ` dyadic-window hit. **This is WRONG.**
> The real Antihydra orbit is the **iterated floor** `c_{n+1} = ⌊3c_n/2⌋` from `c_0=8` (= the bbchallenge
> definition: `8,12,18,27,40,60,90,135,202,…`), which **diverges from `⌊8(3/2)ⁿ⌋`** (`…,60,91,136,…`)
> **at n=6** (`90 ≠ 91`): the iterated floor loses one low bit per step and the loss never carries back.
> The `3ⁿ mod 2ᵏ` reformulation holds for `⌊3ⁿ/2^{n−3}⌋` (0/31) but **FAILS on the real orbit (12/31)**, so
> it is retracted. **What still stands:** §3b, §3c (odd-run `= v2(c−1)`, re-verified 50 034 runs on the real
> orbit), §4, §4a, §4a′, §4b — all were *computed on the iterated orbit* (the code, `c=3*c//2`); only the
> *closed-form identification* in the prose was wrong. (Replace stray "`⌊8(3/2)ⁿ⌋`" by "the iterated orbit".)
> **The Mahler framing survives:** the real orbit grows like `A·(3/2)ⁿ` with `A = 8 − κ = 7.864177262…`
> (`κ = 0.135822738…`), so it is still a `(3/2)ⁿ`-family object with the same open one-sided-density core.

**[PROVEN, verified] corrected exact identity.** `2ⁿ·c_n = 8·3ⁿ − S_n` (verified `n=0..199`), where the
self-referential `S_n` collects the lost low bits: `S_{n+1} = 3·S_n + 2ⁿ·[c_n odd]`, `S_0=0`. So
`c_n = (8 − κ_n)(3/2)ⁿ`, `κ_n = S_n/3ⁿ → κ`. This is the term the wrong §4c dropped.

**[PROVEN, verified] the Φ-potential (the genuine new tool).** Let `Φ_n = balance_n − v2(c_n − 1)`. Then by
§3c, **Antihydra HALTS ⟺ ∃ n: Φ_n ≤ −1.** Exact step rule (0 violations over `2·10⁵` steps):
- **inside an odd-run (`c_n` odd): `Φ_{n+1} = Φ_n` — Φ is FROZEN** (the run drops `v2` by 1 and the balance
  by 1 in lockstep; §3c's "v2 drops by 1" exactly cancels the −1 balance hit);
- **at an even step: `Φ_{n+1} = Φ_n + (2 − L′)`**, where `L′` = length of the odd-run about to start
  (`P(L′)=2^{−(L′+1)}`, `E[L′]=1`, so mean drift `+1` per even step).
So **"Antihydra never halts" ⟺ the one-sided walk Φ — frozen on odd-runs, mean-drift `+1` on even steps —
never reaches `−1`.** Measured `min Φ = 2` over `n ≤ 2·10⁵` (the min is at the very start). This localizes the
open kernel to a single **drift-positivity** statement (a martingale, not a dynamics black box) — the honest
replacement for the retracted §4c. It does **not** close the problem (the drift is in expectation, not
adversarially bounded — the same Mahler wall, now in martingale dress), but it is a clean, conjecture-free,
verified new handle. (The parallel `3ⁿ mod 2ᵏ` and exponential-sum probes were about the *wrong* sequence
`⌊3ⁿ/2^{n−3}⌋` and are NOT recorded as Antihydra results.)

## 5. Status / open
- **[understood, recorded]** mechanism §1, reformulation §2, empirics §3, random-coin heuristic §3b
  (sigma-to-halt `= sqrt(n)/3 → ∞`, halt-prob `~ exp(-n/18)`, Borel–Cantelli ⇒ halts w.p. 0 in the model).
- **[PROVEN, conjecture-independent]** §3c Lemma: odd-run length `= v2(c-1)` exactly, giving the **exact 2-adic
  halting criterion** `HALT ⟺ ∃n: v2(c_n-1) ≥ balance_n+1`. Makes §3b's `2^{-k}` tail structural, not assumed.
- **[reduction]** non-halting ⟸ even-density `> 1/3` forever (§4) — a sharper, weaker target than Mahler.
- **[PROVEN, conjecture-free, §4a]** mod-4 parity rule; sharpened halt criterion `HALT ⟺ ∃n: c_n ≡ 1
  (mod 2^{balance_n+1})`; verified gap `(balance_n+1)−v2(c_n−1)` ≥ 3 with min at `n=1`, diverging `~n/2`.
- **[open — THE SUMMIT]** prove `v2(c_n−1) < balance_n+1 ∀n`, i.e. odd-run lengths are `o(n)` (`~log₂n`).
  A single 2-adic statement about `(3/2)^n` (Mahler family). The honest progress: §2 reformulation, §3c
  exact criterion, §4 reduction, and §4a's sharpening of the open kernel to a crisp data-backed target.
  **Literature attack done (§4b):** no known unconditional theorem reaches even-density `>1/3` or any
  positive density bound. Closest is FLP's *range* `≥1/3` (not a density), so it does not apply; the
  missing piece is a *density/frequency analogue* of FLP's `Ω(3/2)`, which is itself open. The summit is
  provably beyond current literature — it needs genuinely new number theory (or a proof of the §4a kernel).

Run `antihydra_attack.py` to reproduce §3 / §3b / §3c and to keep attacking §4.
