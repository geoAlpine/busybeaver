# o10 as a HALTER — the lottery-upside question, answered rigorously (2026-06-28)

**Machine.** `o10 = 1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC` (halt = state F reads 0).
This note asks the *opposite-direction* question to Antihydra: o10's **heuristic** direction is **HALT**
(each epoch ~1/3 to halt, infinitely many epochs ⇒ Borel–Cantelli-II "divergence side" ⇒ halts a.s.).
Can o10 be **DECIDED** as a halter, or does it hit the same a.e.-vs-specific wall (now on the divergence
side)?

Soundness labels: `[PROVEN]` (machine-verified, exact integers, cross-checked vs raw TM) /
`[HEURISTIC]` (ensemble/model statistic, NOT a proof) / `[OPEN]`.
All numerics: `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (exact big-int), cross-checked vs `bb_sim`.

## BOTTOM LINE (read this first)

> **STATUS of "o10 halts": `[OPEN]`.** The *heuristic* direction is HALT (`[HEURISTIC]`, ensemble
> per-epoch halt-rate 33.667% over B=1..3000), but **o10 is NOT decidable as a halter by any argument we
> have, and Borel–Cantelli II CANNOT be applied to it.** It hits the *same* a.e.-vs-specific (annealed→
> quenched) wall as Antihydra — in the opposite direction. **No decision is claimed. No false proof.**

---

## 1. The exact per-epoch halt condition and the refill map  [PROVEN, raw-TM-faithful]

From `O10_REDUCTION.md` (re-verified here, exact integers, vs raw TM):

- **Inner map** (one macro-step): `m → ⌈3m/2⌉`, `b → b − (1 + [m odd])`. The inner eat consumes the left
  1-block of length `L = 2m − 8`, **always even**, so by (HALT-MECHANIC) (a C/F eat-sweep halts iff it eats
  an ODD run) **no inner step ever halts**. Halting can occur ONLY at the b-countdown underflow.
- **(H-CRITERION) [PROVEN].** Within an epoch (countdown from `(m=6, b=B)`), o10 **halts iff the countdown
  reaches EXACTLY `b = 0` at a step where `m` is ODD.** Otherwise it **refills** (lands on `b=0` at even `m`,
  or overshoots `b=0` via a `−2` step from `b=1` at odd `m`) and restarts a new epoch at `m=6`.
- **Refill map** `R(terminal) → B_next` (piecewise-affine, TM-derived):
  terminal `(m,1)` with `m` odd → `B_next = 3(m−2)`; terminal `(m,0)` with `m` even → `B_next = 3m − 7`.
- **(FULL) [PROVEN].** o10 **halts ⟺ ∃ epoch `e` whose countdown from `(6, B_e)` lands exactly on `b=0` at
  odd `m`.** The `B_e` form the refill orbit, `B_1 = 5`.

**Cross-check vs raw TM (this session, `scratchpad/o10_halter_check.py`, exact integers).** Abstract
`epoch(B)` halt-verdict vs raw TM run from clean config `1 0^{2m−8} 1^b 0 1`, refill detected as the
counter rebuilt to `m=6` with `b>B`:

```
B=1: HALT(217)  B=2: refill→21  B=3: refill→35  B=4: HALT(2274)  B=5: refill→57
B=6:→89  B=7:→137  B=8:→209  B=9:→317  B=10:→479  B=11: HALT(460457)  B=12:→723
B=13: HALT(1050877)  B=14:→1089  B=15:→1637  B=16: predicted-halt (>3M cap, timeout, not a mismatch)
  --> halt-mismatches = 0/15 ; refill-formula matches = 11/11 ; 0 bad
```

`B=5 → B_next=57` reproduces the **real machine's** epoch-1→epoch-2 refill exactly. The model is TM-faithful.

> **⚠ SOUNDNESS NOTE (a self-inflicted near-miss, caught and corrected, in the spirit of
> `SOUNDNESS_INCIDENT.md`).** My first cross-check harness declared "REFILL" on the FIRST inner clean config
> (it only tested `(a2,b2) != (a,b0)`), instead of requiring the counter to be rebuilt to `m=6`. That buggy
> refill-detector produced **8 spurious halt-"mismatches" and 19 refill-"mismatches"** — which would have
> looked like the reduction was wrong. Re-running with the CORRECT refill condition (`m2==6 and b2>b0`, as in
> the authoritative `o10_crosscheck.py`) gives **0/15 mismatches**. Lesson re-learned: a measurement harness
> can be unfaithful just like a decider; the apparent "mismatch" was the harness, not the machine. The
> reduction stands.

## 2. The SINGLE deterministic refill orbit — and how far it is feasible  [PROVEN feasibility ceiling]

o10 is **one** orbit, not an ensemble. Its actual refill sequence (exact integers,
`scratchpad/o10_halter_check.py`):

| epoch | `B_e` | digits of `B_e` | halt? | inner steps | terminal `m` | feasible? |
|---|---|---|---|---|---|---|
| 1 | 5 | 1 | **NO** (refill) | 3 | 21 (odd) | yes (raw-TM) |
| 2 | 57 | 2 | **NO** (refill) | 40 | 70091069 (odd, 8 digits) | yes (abstract; epoch-1→2 raw-TM-confirmed) |
| 3 | 210273201 | 9 | **?** | ~1.4×10⁸ | ~10^(24.7 million) | **INFEASIBLE** |

The b-countdown loses ≈1.5 per inner step, so epoch `e` has ≈`2 B_e/3` inner steps and its terminal `m`
reaches ≈`6·(3/2)^{2B_e/3}`. Hence:

- **Epochs 1–2 are decided: both REFILL (non-halt).** This is consistent with the real BB(6) holdout running
  ≥40M raw steps without halting — those 40M steps are *inside epochs 1–2*.
- **Epoch 3 (`B_3 ≈ 2.1×10⁸`) is already unreachable**: ~1.4×10⁸ inner steps, with `m` blowing up to a
  number of ≈**24.7 million decimal digits**. Even the *abstract* (post-§3c-reduction) epoch is infeasible;
  the raw TM is `(3/2)`-exponentially worse. The refill orbit `B_3, B_4, …` is **unreachable by any
  simulation** (doubly-exponential growth: `5 → 57 → 2.1×10⁸ → …`).

So **direct simulation decides exactly two epochs, both non-halting.** Lottery upside by brute force: none.

## 3. Borel–Cantelli II CANNOT apply to o10  [PROVEN negative]

The heuristic argument is: per-epoch halt-probability ≈ 1/3 (`[HEURISTIC]`, ensemble 33.667% over
B=1..3000), so `Σ_e P(epoch e halts) = ∞`, and "by Borel–Cantelli II, infinitely many epochs halt a.s. ⇒
o10 halts." **This is not a valid proof, for two compounding reasons.**

**(a) The divergence sum.** In the *ensemble* (B drawn at random) each epoch halts with prob ≈1/3, so the
annealed `Σ P = ∞`. ✔ — *but only as an ensemble statement.* For the **deterministic** orbit, "P(epoch e
halts)" is not a probability at all: each term is already `0` or `1`, fixed by the parity of `m` at the
underflow of the `⌈3m/2⌉`-orbit started at `(6, B_e)`. The "sum" for the orbit is just *the count of epochs
that actually halt*, and the whole question is whether ANY term is `1`. There is no `Σ P = ∞` for a single
trajectory.

**(b) Independence — the fatal gap.** Borel–Cantelli **II** (the divergence ⇒ `P(limsup)=1` direction) is a
theorem about a sequence of events **in a probability space**, and it **requires independence** (or a
quantitative quasi-independence: Kochen–Stone / a second-moment/`Σ_{i,j}` correlation bound). o10's
per-epoch halt events are **deterministic functions of one fixed orbit** — there is *no probability space,
no randomness, and nothing to be independent of.* B-C II literally does not type-check here.

> **(B-C verdict) [PROVEN negative].** Borel–Cantelli II **cannot be applied to o10.** B-C II governs
> *random* events; a single deterministic orbit's epoch-halt events are each already `∈{0,1}`. The "halts
> a.s." conclusion is a statement about a **random ensemble of B-values**, not about the specific seed
> `B_1=5`. (Note: Borel–Cantelli **I** — the convergence ⇒ a.e.-finite direction — needs *no* independence,
> which is why the *non-halting existence* cryptids o18/o15 get a clean annealed a.e. result in
> `EXISTENCE_META_THEOREM.md`. The *divergence* side that o10 would need is the one that *does* require
> independence — and that is precisely what a deterministic orbit cannot supply.)

## 4. The decisive soundness check — o10 is a divergence-side genericity wall  [OPEN]

"Halts with probability 1 over random epochs" is an **ENSEMBLE/annealed** statement. o10 is **ONE
deterministic orbit.** Deciding "o10 halts" requires exhibiting that the **specific** doubly-exponential
sequence `B_e` realizes the event "the `⌈3m/2⌉`-countdown from `(6, B_e)` lands on `b=0` at odd `m`" for some
`e` — a **single-orbit equidistribution/genericity statement**, now on the **divergence side**.

This is the exact mirror of Antihydra:

| | Antihydra (convergence side) | o10 (divergence side) |
|---|---|---|
| generic behaviour ⇒ | **non-halt** (even-density →1/2 > 1/3) | **HALT** (per-epoch ≈1/3, ∞ epochs) |
| to DECIDE you must control | the **specific** orbit's liminf density | the **specific** refill orbit's parity-at-underflow |
| obstruction | annealed→quenched: the seed could be the atypical (halting) orbit | annealed→quenched: the seed could be the atypical (**never**-halting) orbit |
| B-C usable? | — | **II needed, but needs independence a single orbit lacks** |
| status | `[OPEN]` (a.e.-vs-specific wall) | `[OPEN]` (same wall, opposite direction) |

The annealed "1/3 per epoch ⇒ halts" reasoning silently models the `B_e` as *fresh pseudo-random draws*
(so the parities-at-underflow look like independent fair-ish coins). That pseudo-randomness is a **model
assumption** — exactly the "extrapolate forever from a model/finite sample" failure mode that
`SOUNDNESS_INCIDENT.md` warns against. The specific `B_e` is a *single deterministic trajectory*; nothing
proven forces it to be pseudo-random, and it could lie in the measure-zero set of seeds that refill forever.

**Is there a structural miracle (a provably-halting reachable epoch)?**
- Epochs 1 and 2 are exactly simulated and **both refill** — no halt there.
- Epoch 3 onward is **infeasible** (24.7-million-digit `m`), so no reachable halting epoch can be exhibited.
- No closed-form/structural argument forces any specific `B_e` to give the odd-`m`-at-`b=0` parity.

So **no miracle: o10 is not decidable as a halter by any means available here.**

## 5. The open kernel for o10 (divergence-side analog)  [OPEN]

> **(o10 open kernel).** Decide whether the deterministic, doubly-exponentially-sparse refill orbit
> `B_1=5, B_{e+1}=R(terminal of epoch e)` ever produces an epoch whose `⌈3m/2⌉`-countdown from `(6,B_e)`
> **lands exactly on `b=0` at odd `m`.** Equivalently: an **equidistribution-of-`m`-parity result at the
> dynamically-determined underflow index of each epoch, evaluated along the specific doubly-exponential
> `B_e` sequence, across infinitely many restarting epochs.**

This is **strictly harder** than Antihydra's single-orbit `3/2` density fragment (a single liminf on one
orbit): o10 needs a *uniformity* statement across an infinite family of restarting orbits whose start
points are doubly-exponentially sparse and themselves generated by the dynamics. It is **outside** the
unified non-halting density limit theorem (whose `β>0` barrier proves *non-halting* from a density floor;
o10's heuristic direction is the opposite) **and** outside the clean existence/Borel–Cantelli-I annealed
result of `EXISTENCE_META_THEOREM.md` (which is the *convergence* side, summable target, no independence —
o10 would need the *divergence* side, which needs the independence a single orbit cannot give).

## 6. Explicit soundness statement

- **"o10 halts": `[OPEN]`.** Heuristic direction HALT (`[HEURISTIC]`: ensemble per-epoch ≈1/3 ⇒ informal
  "halts a.s."). **This is NOT a proof and is labelled as such.**
- **Borel–Cantelli II CANNOT be applied to o10** (`[PROVEN negative]`): it requires randomness/independence;
  o10 is a single deterministic orbit whose epoch-halt events are each already `∈{0,1}`. "Halts a.s." is an
  ensemble statement about random B, silent about the deterministic seed `B_1=5`.
- **Decided by exact simulation: epochs 1–2 only, both non-halt.** Epoch 3 (`B_3≈2.1×10⁸`, terminal `m`
  ≈24.7-million digits) and beyond are **infeasible** — the refill orbit is unreachable.
- **Open kernel:** the divergence-side single-orbit genericity statement of §5 — that the specific
  doubly-exponential refill orbit hits an odd-`m` underflow. Same a.e.-vs-specific wall as Antihydra, opposite
  direction.
- **NO DECISION IS CLAIMED. NO `[PROVEN halts]`. NO false proof.** Reduction/feasibility/B-C-negative are
  machine-verified (exact integers, 0 raw-TM mismatch over B=1..15); the halting *direction* remains open.

## Reproduce
- `scratchpad/o10_halter_check.py` — abstract `epoch(B)`, refill map `R`, raw-TM `tm_from_clean`,
  the real refill orbit (epochs 1–3 + feasibility ceiling), ensemble halt fraction.
- `scratchpad/o10_crosscheck.py` (authoritative, `m2==6 and b2>b0` refill) — 0 mismatch B=1..16.
- `O10_REDUCTION.md` — the §3c reduction (H-CRITERION, refill map, FULL criterion).
- `EXISTENCE_META_THEOREM.md` §3a — B-C I (no independence, convergence side) vs B-C II (needs independence,
  divergence side); the annealed→quenched wall.
- `SOUNDNESS_INCIDENT.md` — the "never extrapolate forever from a model/sample" lesson (applied in §1 and §4).
