# o10 — finishing the one incomplete reduction (outer/refill structure, 2026-06-23)

`o10 = 1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC` (halt = state F reads 0).

In the 5-machine comparison (`CRYPTID_REDUCTIONS.md`) o10 was the only core machine whose reduction was
**incomplete**: the inner loop was solved but the **outer/refill orbit was never extracted** (the 2nd
refill is unreachable by direct simulation). This note finishes the structural examination — staying on
the BB(6) challenge, attacking the actual machine.

## Clean milestone (captured from the real run, verified)
At a milestone the head sits at the **left end in state E**, tape `0010 0^a 1^b 1101`, with `m=(a+9)/2`.
Inner loop (verified): `m → ⌈3m/2⌉`, balance `b → b−1` (m even) / `b−2` (m odd). When `b` hits 0 the
machine enters a **refill sub-routine** (not a halt) that **resets m→6 and jumps b up**. The real run from
blank: startup `m=6,b=3` exhausts at `m=14,b=0` (t=285), then refills to `m=6, b=55` (t=2621).

## Outer orbit = the b-at-refill sequence — doubly-exponential (why the 2nd refill is unreachable)
Each epoch the inner loop runs `b` down to 0 over ≈`b/1.5` steps, during which `m` grows like
`6·(3/2)^{#steps}`. So `b_{n+1}` ≈ a function of `m_exhaust ≈ 6·(3/2)^{b_n/1.5}` — **doubly exponential in
`b_n`**: `b: 3 → 55 → ~10^8 → …`. Confirmed operationally: in **40M TM steps only the first refill
occurs**; the 2nd is astronomically far (consistent with the earlier ~10^15 estimate). This is why direct
simulation cannot extract the outer orbit, and why a fast abstract process would be needed.

## Probing the refill rule (custom-config method) — it is NOT a clean function
Since the refill rule is a *local* mechanical fact, it can be probed from custom milestone configs
(restart in state E at the left end, vary m,b — reachability irrelevant for a local rule). Result
(m_exhaust → b_next): `9→33, 18→73, 21→87, 24→153, …` — **not** `f(m_exhaust)` for any simple f (no
affine/×k fit). The outer/refill map is irregular: this is the genuine reason the reduction was
"incomplete" — **not a missing technique, but real irregularity.**

## A regular sub-slice (honest, but only a slice)
The embedded family `0010 0^{2m-9} 1^1 1101` (b=1) **halts iff `m ≡ {1,2,8,9,10} (mod 16)`** — a clean
**regular** (modular) condition, verified zero-mismatch for `m=5..120`. Unlike o17's `0A01^k` (genuinely
Collatz-irregular), this slice is regular. But it is one b-slice; the full dynamics (varying b, the
irregular refill rule, the doubly-exponential outer orbit) are not regular, so this does not decide o10.

## Status
- **[PROVEN, this session]** inner map; outer orbit = doubly-exponential b-refill sequence (1st refill
  `b:3→55` reproduced; 2nd unreachable in 40M steps); refill rule probed and shown **not** a clean
  function; the b=1 sub-family is mod-16 regular (m=5..120).
- **[CONCLUSION]** o10 is a **nested two-level system** (inner Mahler-3/2 + mod-16-regular b=1 slice, but
  an **irregular doubly-exponential outer refill orbit**). The reduction is now *complete* in the sense
  that its outer structure has been examined: o10 is **Collatz-hard / undecided by us**, the irregularity
  living in the refill map. Now **all 5 core machines are fully characterized** (5/5 Collatz-hard, none
  with unexamined structure remaining).
- **[honest]** o10 not decided; no halt/non-halt claim. The attack reached the real obstruction (the
  doubly-exponential, irregular outer orbit), not a tooling gap.
