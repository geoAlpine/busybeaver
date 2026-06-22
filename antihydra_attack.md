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

## 4. The (weaker) target the proof reduces to
Full equidistribution (even-density = 1/2 exactly) is **Mahler's 3/2 problem** (open). But halting only
needs the density to fall to **1/3**, so:
> **It suffices to prove the one-sided bound: even-density `E/n > 1/3` for all `n`.**
This is *weaker* than Mahler (one-sided, with a 1/2-vs-1/3 margin), but still a statement about the
2-adic distribution of `floor(8*(3/2)^n)` — the Mahler family. **Not solved; sharpened.**

## 5. Status / open
- **[understood, recorded]** mechanism §1, reformulation §2, empirics §3, random-coin heuristic §3b
  (sigma-to-halt `= sqrt(n)/3 → ∞`, halt-prob `~ exp(-n/18)`, Borel–Cantelli ⇒ halts w.p. 0 in the model).
- **[reduction]** non-halting ⟸ even-density `> 1/3` forever (§4) — a sharper, weaker target than Mahler.
- **[open]** proving the §4 bound. It is a 2-adic / Weyl-equidistribution statement about `(3/2)^n`;
  hard, in the Mahler family. The honest "getting closer" of this session is the §2 reformulation and
  the §4 reduction, with the §3 quantitative confirmation.

Run `antihydra_attack.py` to reproduce §3 and to keep attacking §4.
