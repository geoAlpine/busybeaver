# (K) research — the count→frequency barrier is universal in the 2–3 digit world; fresh 2026 leads that may crack it

*Shifting focus to `(K)` itself. `(K)` = base-3/2 digit-`0` frequency `≥1/3` = a **positive-density lower bound on a
digit of a single specified orbit**. This note (i) quantifies the exact obstruction — the **count→frequency barrier**
(everyone can prove "→∞" ≈ `log`-count; nobody a positive frequency) — and shows it is **universal across the 2–3
digit world**, and (ii) flags the freshest 2026 literature that claims **positive-density / density-one** lower bounds
in *exactly* this world, as the highest-priority building-block leads. SOUNDNESS: `[OBSERVED]`/`[PROVEN-in-lit]`/`[lead]`;
`(K)` `[OPEN]`; no machine decided; no false proof.*

## 1. The barrier, quantified `[OBSERVED, exact big-int]`
| object | empirical truth (frequency) | best proven (count) |
|---|---|---|
| **Erdős-400 object** — `#` nonzero base-3 digits of `2^m` | `→ 0.665` (`≈2/3`, i.e. `~0.42m`, **linear**) | Stewart 1980: `≫ log m/log log m` (**log**) |
| **`(K)` object** — base-2 digit-`1` freq of `3^n` | `→ 0.49` (`≈½`, **linear**) | `#even ≥ 0.89 log n` analogue (**log**) |
At `m=5000`: Stewart count `~2.7` vs needed linear frequency `~1577` — a **`582×` (exponential) gap**. Both the
`2^m`-in-base-3 and the `3^n`-in-base-2 objects are **empirically fully normal** (linear-frequency), yet every
unconditional proof reaches only a **logarithmic count**. **This is `(K)`'s exact obstruction, and it is the same
barrier across the whole 2–3 digit world** — the difficulty is not special to Antihydra; it is the general failure to
convert "infinitely many nonzero digits" (`log`) into "a positive fraction of nonzero digits" (linear) for a single
specified lacunary orbit.

*(Aside `[OBSERVED]`: the clean seam identity `2^n c_n + S_n = 8·3^n` with `S_n = 8·3^n mod 2^n` holds for the
**non-recursive floor** `c_n=⌊8(3/2)^n⌋`; the **recursive** Antihydra orbit `⌊3c_{n−1}/2⌋` accumulates floor
corrections and decorrelates from it — so the moving-diagonal-digit-of-`3^n` framing is exact for the floor version and
heuristic for the recursive `(K)`. Both are the same normality class.)*

## 2. The freshest leads — 2026 papers claiming to break `log`→linear in the 2–3 world `[leads, to evaluate]`
The literature sweep (2026) surfaced results that, for the first time, claim **positive-density / density-one** digit
lower bounds in exactly this setting — candidate cracks in the count→frequency barrier:
- **arXiv:2606.23661** — *"a density-one lower bound for Erdős Problem 400"*, via **"mixed binary–ternary resource
  allocation,"** leading coefficient `3(k−1)/log 12`. Erdős 400 concerns the ternary digits of `2^n` — **the same 2–3
  digit tension as our seam**. If it yields a *linear* lower bound (not just `log`), it is the first breach of the
  barrier here.
- **arXiv:2606.24972** — *"Positive dyadic density for rational weighted binary expansions"*: reportedly proves a
  **positive density lower bound on digit-`1` positions** under a rationality hypothesis — *the exact shape `(K)`
  needs*.
- Supporting: **arXiv:2511.03861** (Ternary Digits of Powers of Two), **arXiv:2501.00850** (Drmota–Spiegelhofer, joint
  `(s_2, s_3)` distribution attains a.a. values), **arXiv:2506.12929** (normality under arithmetic operations).

**The critical question to evaluate for each `[the a.e.-vs-specific wall]`:** is the bound **single-orbit and for the
specified sequence**, or **density-one in `n` / almost-every** (which cannot certify our specific seed 8, the recurring
Fan–Fan–Ye wall)? "Density-one lower bound for Erdős 400" most likely means *for a density-one set of `n`* — a.e.-flavored
— so it may not directly give `(K)` for the one orbit; but it is the **closest existing result to a genuine
count→frequency breakthrough**, and its *method* (mixed binary–ternary resource allocation) is the most promising
external technique to import, because it operates on precisely our 2–3 digit structure.

## 3. `(K)`-research verdict + next steps
- **The obstruction is pinned to one universal phenomenon:** count (`log`) → frequency (linear) for a single lacunary
  orbit in the 2–3 digit world. `(K)`, Erdős 400, Mahler `Z`-numbers, and the Normality Conjecture all sit behind it.
- **Highest-value next step:** evaluate arXiv:2606.23661 and 2606.24972 — specifically whether their lower bounds are
  single-orbit/specified or a.e./density-one, and whether the "mixed binary–ternary resource allocation" method can be
  aimed at the base-3/2 orbit-word's digit-`0` frequency. This is the first genuinely new external technique in range
  since Stewart, and the most concrete `(K)` attack lead this program has surfaced.
- **Honest status:** no crack yet; but `(K)` research now has a **specific, current, on-target external method to
  probe**, not just the generational "P1′" placeholder.
**`(K)` `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce / basis
- `/tmp/k_research.py` (`/opt/homebrew/bin/python3.13`, exact big-int): `s_3`-nonzero of `2^m` freq `→0.665`; `s_2` of
  `3^n` freq `→0.49`; Stewart-vs-linear `582×` gap at `m=5000`. Basis: CITATIONS #10 (Stewart 1980), #11 (Normality
  Conjecture), `EVEN_COUNT_FLOOR`, `FRONTIER_LIT_2026-07-05`; leads arXiv:2606.23661, 2606.24972, 2511.03861,
  2501.00850, 2506.12929.
