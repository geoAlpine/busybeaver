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

## 4. The (weaker) target the proof reduces to
Full equidistribution (even-density = 1/2 exactly) is **Mahler's 3/2 problem** (open). But halting only
needs the density to fall to **1/3**, so:
> **It suffices to prove the one-sided bound: even-density `E/n > 1/3` for all `n`.**
This is *weaker* than Mahler (one-sided, with a 1/2-vs-1/3 margin), but still a statement about the
2-adic distribution of `floor(8*(3/2)^n)` — the Mahler family. **Not solved; sharpened.**

## 5. Status / open
- **[understood, recorded]** mechanism §1, reformulation §2, empirics §3.
- **[reduction]** non-halting ⟸ even-density `> 1/3` forever (§4) — a sharper, weaker target than Mahler.
- **[open]** proving the §4 bound. It is a 2-adic / Weyl-equidistribution statement about `(3/2)^n`;
  hard, in the Mahler family. The honest "getting closer" of this session is the §2 reformulation and
  the §4 reduction, with the §3 quantitative confirmation.

Run `antihydra_attack.py` to reproduce §3 and to keep attacking §4.
