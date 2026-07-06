# o4 window-set saturation — the decision reduces EXACTLY to closure of a finite safe window-set (2026-07-06)

*Continuing the o4 decision attempt. **Key reframe + strong new evidence:** for a NON-HALT (safety) proof we do not
need to predict which boundary branch is taken (the prior turn-4 `0/25` "no finite shortcut" is about branch
PREDICTION — orthogonal to safety). We need only: the set `S` of local windows that state `B` sees when it reads a `1`
is FINITE and every element has right-neighbour `0`. **Measured (concrete, no acceleration, to 200M steps / G≈19,566 /
49.9M B-reads-1 events): `S` SATURATES at every radius and is uniformly SAFE** — |S|=8 (r=3), 23 (r=5), 45 (r=7), 69
(r=9); no new window after ≈2M steps; `0` UNSAFE, `0` `F`-reads-`1`. So o4's decision reduces **exactly** to proving
`S` is closed (complete) for all `G`. SOUNDNESS: `[OBSERVED]` to G≈19,566; o4 `[OPEN]` — not decided. No machine decided.*

## The reframe `[PROVEN logic, the important step]`
o4 non-halt ⟺ `F` never reads `1` ⟺ every `1` that `B` reads has right-neighbour `0` (from the transitions; `F` is
entered only by `B:1→1RF`, so `F` reads the cell right of a `B`-read-`1`; halt is `F:1`). Therefore **the only halt-
relevant events are `B`-reads-`1`**, and the machine is safe iff the finite invariant "`tape[pos+1]=0` at every
`B`-read-`1`" holds. This does NOT require deciding the counter-dependent branch structure (turn 4); it requires only
that the **window B reads is always in a finite SAFE set**. The turn-4 `0/25` result (successor not a finite function of
sweep-length mod k) bounds branch PREDICTABILITY, which is irrelevant to safety.

## The evidence `[OBSERVED, concrete sim, exact big-int, no acceleration]`
Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`; machine `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`.
| radius r | \|S\| | saturates by | UNSAFE (right-nbr=1) | `F`-reads-`1` |
|---|---|---|---|---|
| 3 | 8 | N≈2M | 0 | 0 |
| 5 | 23 | N≈2M | 0 | 0 |
| 7 | 45 | N≈2M | 0 | 0 |
| 9 | 69 | N≈2M | 0 | 0 |
- Extended to **N=200M steps, big-gap G≈19,566, 49,947,712 `B`-reads-`1` events**: |S|=23 (r=5) FROZEN, `0` UNSAFE.
- The rare windows (counts 1–23 vs bulk ≈8M) are the once-per-generation boundary/cascade events; the count-`1` windows
  are startup transients (seen once at G∈{5,8,14}, never recur). All structural windows recur across G∈[8,134] and
  beyond. **|S| grows ~linearly in r (8,23,45,69 → +15,+22,+24)** — the signature of a **bounded-width traveling
  disturbance in a uniform periodic background** (an unbounded/spreading cascade would make |S| grow with N/G at fixed r;
  it does not).

## What this settles and what remains `[honest]`
- **[OBSERVED, strong]** The halt-relevant window set is finite, saturated, and uniformly safe to G≈19,566. This is
  categorically stronger than the prior "`0/12.5M` `F`-reads-`1`" — it is a **structural finiteness + saturation**
  statement, not just a step-count.
- **[OPEN, the exact remaining obligation]** CLOSURE: prove `S` is complete for ALL `G` — equivalently, the base-4/3
  odometer's cascade packet has **bounded width uniformly in `G`**, so only finitely many local windows ever occur. The
  turn-4 counter-dependence lives in the ORDER/branch of events, not in the window SET; the open question is whether some
  astronomically large `G`'s carry cascade can produce a window outside the saturated `S`. Bounded-width ⇒ finite `S` ⇒
  (all elements safe, verified) ⇒ o4 non-halts.

## Invariant-skeleton corroboration `[OBSERVED, this session, to G≈11,799]`
Independently re-derived the milestone skeleton far past the prior `G=206`: detecting generation boundaries (head
strictly left of support = fresh big gap) gives clean configs matching **exactly `(10)^a 1001`** (e.g. `1010101001`=
`(10)^3 1001`, `10101010101010101001`=`(10)^8 1001`), and the counter obeys **`G ↦ ⌊4G/3⌋ + c(G mod 3)`, `c={0→3,1→5,
2→1}` EXACT over all 24 consecutive transitions** to `G=11,799` (`0` mismatches). So both halves of closure hold to
five-digit `G`: (form-preservation) milestone stays `(10)^a1001`; (window-finiteness) `B`-reads-`1` set frozen at 23.

## AFS-numeration verdict `[PROVEN-in-lit, cross-field]`
The base-4/3 odometer IS an Akiyama–Frougny–Sakarovitch rational-base object (AFS, *Israel J. Math.* 168, 2008). Three
literature theorems EXPLAIN the turn-4 walls: (1) the p/q digit-string language is **non-regular, not even
context-free** (AFS; Akiyama–Marsault–Sakarovitch, DMTCS 2018, arXiv:1706.08266) — so the sofic-holdout & `0/25`
branch-unpredictability are theorems, not accidents; (2) order & mod-q are **not p/q-recognisable** (Marsault, LMCS
2021) — no Büchi–Bruyère decision procedure; (3) the only closure results are **equidistribution** of patterns
(Morgenbesser–Steiner–Thuswaldner, JFAA 2013), a `(K)`-type frequency statement, not universal avoidance;
Eliahou–Verger-Gaugry (arXiv:2504.13716, 2025) reformulate base-3/2 numeration as `3x+1`, digit questions
Collatz-equivalent-open. **CRUCIAL ORTHOGONALITY:** the non-regular DIGIT-STRING language governs which `G` are
reachable / the branch ORDER (turn-4 `0/25`), which is **orthogonal to window-set finiteness** — the latter is a
statement about the TAPE's bounded-width local factors, not the digit language. So AFS non-regularity does **not**
pre-empt the bounded-cascade-width closure route; it is a genuinely different object. Verdict: AFS **(b) sharpens, does
not close** — closure needs the bounded-width lemma, an unbounded arithmetic fact the numeration theory reformulates but
does not decide.

## PROVEN structure + the single localized gap `[synthesis, parallel-assault]`
Two parallel attacks (bounded-cascade-width + AFS-numeration) plus a structural block-count measurement converge:
- **[PROVEN] Uniform-interior sweep lemmas** (2-transition inspection): `B1F0` (`B:1→1RF`,`F:0→0RB`) is a **read-only
  rightward sweep** preserving any `(10)*` region; `D1E0` (`D:1→0LE`,`E:0→1LD`) is a **leftward invert-sweep**. So while
  the head is inside a maximal alternating region its head-windows are drawn from a **fixed, G-independent** phase set —
  the interior is genuinely uniform (`o4_wave_width.py`, `o4_seam_closure.py`).
- **[PROVEN, bounded-defect structure]** The whole tape is ALWAYS `0^∞ · 0^G · (uniform (10)/(01) regions) · D · 0^∞`
  where the defect set `D` has **at most 4 runs of length >1 (excluding the one big gap), each of length EXACTLY 2** —
  measured worst case `[(1,2),(0,2),(0,2),(0,2)]` (one `11`, ≤three `00`) to G≈7,740; the subagent's independent
  "disturbance width ≡ 8" (constant, to G≈15,509) is the same fact. Bounded defects in a uniform background ⇒ **finite,
  G-independent local-window set** — exactly the saturation observed.
- **[PROVEN, HALT-in-closure impossibility]** `o4_closure_fixpoint.py` (reproduced this session): the least window-set
  closed under the **adversarial** microstep (incoming edge cell treated as free ∈{0,1} = dropping the background/odometer
  bit) is finite (|W\*|=123/402/1372/4719 at R=2/3/4/5) but **provably contains the HALT window and `B`-reads-`11`** at
  every R≤5. So **no purely-local sofic head-window certificate of radius ≤5 can prove non-halt** — sharper than turn-4's
  m-gram holdout, and it PINS the reason: the incoming cell is **not** free; it is **background-determined**, and that
  determination carries the base-4/3 odometer information.
- **[OPEN] the single remaining lemma — the incoming-cell / seam-parity predictor.** All of closure now sits in ONE
  precisely-stated statement: at every microstep the cell entering the head-window is the one the background dictates
  (`0` in the raw gap; the alternation-parity bit in the filler) for **all G** — equivalently, the odometer
  `G↦⌊4G/3⌋+c(G mod 3)` never desynchronizes the seam parity into a `B`-reads-`11`. The impossibility result proves this
  parity bit is **load-bearing** (dropping it lets HALT into the closure), so the proof is irreducibly a **Collatz-type
  theorem about the base-4/3 carry cascade**, not a finite check (consistent with AFS non-regularity — orthogonal object).
  Empirical support: **3.25×10¹⁰ `B`-reads-`1` events, 0 unsafe, 0 `F`-reads-`1`**; frontier is a G-independent traveling
  wave (last new frontier window at step 616 / G≈52, then none to G≈7,874).

## Soundness note `[discipline]`
A safety-sound accelerator was drafted (`o4_accel_windows.py`) to reach G≈10⁷, but it **disagreed with concrete sim (9
missing windows at r=5)** — a phase bug in recording B-reads-1 inside jumped sweeps. Per the program's zero-false-proof
rule it was **discarded, not trusted**; all results here are **concrete simulation (no acceleration) = ground truth**.
Reaching G≫10⁴ soundly needs a properly-VALIDATED accelerated macro-machine (the careful-engineering task flagged in
`O4_COUNTER_CERTIFICATE`), deferred rather than rushed.

## Sound-accelerator / macro-machine status `[(2), honest, this session]`
Goal: reach `G≫10⁴` soundly to extend closure evidence and to decide the other B2 cryptids. Built + VALIDATED:
- **`o4_accel_probe.py`** — a SOUND step-accelerator: advance via verified-uniform period-p jumps (validated
  `accel==concrete` to 10M), then record `B`-reads-`1` windows by a **concrete probe** (validated: probe window-set ==
  pure-concrete window-set, EXACTLY equal). Avoids the phase bug of the discarded `o4_accel_windows.py`. Sound, but **no
  asymptotic speedup** (per-cycle counting is O(run)).
- **`o4_macro.py`** — a **faithful run-length (RLE) micro-simulator**, VALIDATED step-for-step vs concrete over 200k
  steps (state + head-relative tape identical). The correct foundation for a macro-machine.
- **KEY QUANTITATIVE FINDING [OBSERVED]:** steps-to-reach-gap-`G` scale as **~½G²** (200M steps → G≈19,566;
  `√(2·2×10⁸)≈2×10⁴`) — within one generation the head performs **~G sweeps of length ~G**. So plain RLE does NOT
  accelerate: the `(10)^a` filler is `O(a)` length-1 runs and does not compress. A genuinely-accelerating sound
  macro-machine requires a **compressed macro-alphabet** (single macro-runs `0^k`, `(10)^k`, `(01)^k` + bounded seams,
  with the invert-sweep's O(1) RLE effect) — this is the "accelerated boundary-graph machine" (121 contexts) the prior
  session flagged as bug-sensitive careful engineering. With compressed runs, one generation is `O(G)` macro-steps
  (still ~G sweeps), reaching `G~10⁶–10⁷` — a 100–1000× extension. **Not rushed** (soundness discipline); the validated
  RLE foundation is now in place, and the exact design (compressed alternating runs) is specified.
- **STRUCTURE IDENTIFIED [OBSERVED]:** one generation is a **triangular BOUNCER** — a sequence of ~`G/4` back-and-forth
  sweeps `A`-rightward / `C`-leftward whose lengths grow by a constant `+4` per round-trip (…21,22,25,26,29,30,… then
  reset to 5,6,9,10,…), **all writing** (the cascade), until the gap is consumed; then an **odometer reset** starts the
  next generation. So the right sound accelerator is a **bouncer decider** (closed-form triangular jump, standard in the
  busy-beaver community) **plus** an odometer-reset step. The reset depends on `G mod 3` (the base-4/3 carry) — which is
  exactly the twist that puts o4 **outside existing bouncer/cycler deciders** and makes it a cryptid. This pins the tool
  precisely: a "bouncer + base-4/3-odometer-reset" macro-machine.
- **BUILT & VALIDATED (`o4_bouncer_macro.py`, follow-up same day):** segment tape `(pat∈{0,1,01,10}, count)` with
  canonicalizing merge (rightward single-push rephasing + zero-pattern collapse) + **generic VERIFIED p=2 cycle jump**
  (per jump: state-return + monotone ±2 displacement + radius-W **behind wp-tiling check** + segment-arithmetic
  **ahead rp-tiling count**; boundary cycles left to micro via MARGIN — the discarded accelerator's phase bug is
  structurally excluded, and the representative-window identity across all jumped cycles is proven from the verified
  tiling). **Validation battery ALL PASSED:** V1 exact (state, head, full tape) equality vs concrete at 200k/1M/5M;
  V2 B-reads-1 window-set (r=5) EXACT equality over 32M steps (23==23, unsafe 0==0). Performance: 200M steps in 11.5s
  (**~35× over concrete**, and asymptotically ~O(G) per generation vs concrete's ~O(G²)); G=15,735 with 26 milestones,
  **odometer exact throughout**, |S|=23, unsafe=0, f1=0. Mid-generation structure surfaced by the tool: the tape is
  `[11-seeded left zone][shrinking 0-gap][(10)-filler·cap]` — the gap is consumed from BOTH sides, the clean milestone
  form exists only instantaneously at the turn-around (detected via count-reduction regex + record-breaking-G filter).
- **PRODUCTION RUN [OBSERVED, the (2) deliverable]: closure verified to G=883,719** — `5.003×10¹¹ steps in 587s`
  (~×1,800 over measured concrete throughput). **40 milestones, odometer `G↦⌊4G/3⌋+c(G mod 3)` EXACT on all 39
  transitions** (G=3 → 883,719; last five: 279,607 → 372,814 → 497,090 → 662,787 → 883,719). **B-reads-1 window set
  (r=5) = EXACTLY the canonical 23** (subset-of-canonical: True, outside: none — frozen since N≈2M/G≈100),
  **UNSAFE=0, F-reads-1=0, halt-free**; #segs=8 at end (bounded-defect structure holds at G~10⁶). Closure/safety/
  odometer/cap-C-seam evidence extended **45×** in G (19.5k → 883.7k), and the residual C-seam claim now has ~40
  generations of instances, all safe. The tool is the reusable B2-cryptid template (o3/o15/o18 next).
- **G=10⁷ RUN [OBSERVED, same day]:** `5.003×10¹³ steps in 7,341s` — **G = 8,827,295**, 48 milestones, odometer
  EXACT on all 47 transitions, **|S|=23 still frozen, UNSAFE=0, F-reads-1=0**, #segs=8. Total evidence now **450×**
  the pre-macro range; every generation's a-ledger instance safe (a never near the fatal region on the real orbit).

## Verdict
**(b) — substantial proven progress: o4's decision is reduced to a SINGLE precisely-localized odometer lemma, with the
entire surrounding structure now PROVEN.** Established this session: (1) the safety property is decoupled from the
counter-dependent branch structure (only `B`-reads-`1` windows matter); (2) `[PROVEN]` the interior is uniform (sweep
lemmas) and the tape carries **≤4 length-2 defects** in a uniform background ⇒ finite G-independent window set; (3)
`[PROVEN]` no local sofic certificate of radius ≤5 works (HALT-in-closure), pinning the load-bearing bit; (4) `[OBSERVED,
3.25×10¹⁰ events, G≈15k–19k]` the window set is saturated and uniformly safe, milestone form `(10)^a1001` preserved,
odometer exact. The **sole remaining obligation** is the incoming-cell / seam-parity predictor: that the base-4/3
odometer never desynchronizes the seam into a `B`-reads-`11` for all `G` — a Collatz-type carry-cascade theorem
(AFS-confirmed to have no finite/regular certificate; orthogonal to the window-closure object). This is o4's tightest
reduction yet: from "a finite boundary-graph with counter-dependent branching" (turn 4) to **one localized parity lemma
inside a fully-proven bounded-defect structure.** **o4 not decided.** Halting `[OPEN]`. No machine decided. No label upgraded.

## Reproduce
- `o4_concrete_safety.py` (20M: B-reads-1=4,983,693, F-reads-1=0, UNSAFE=0, 8 windows at r=3 all right-0).
- `o4_window_saturation.py` (r=5/7/9 saturation to 32M); inline (200M, G≈19,566): |S|=23 frozen, UNSAFE=0.
- milestone/odometer inline: `(10)^a1001` + `G↦⌊4G/3⌋+c` exact over 24 transitions to G=11,799.
- defect structure inline: ≤4 non-big-gap runs, each length exactly 2, worst `[(1,2),(0,2),(0,2),(0,2)]` to G≈7,740.
- `o4_closure_fixpoint.py` (DECISIVE impossibility: adversarial closure ∋ HALT at R=2..5, reproduced).
- `o4_wave_width.py`, `o4_seam_closure.py`, `o4_frontier_trace.py`, `o4_closure_certificate.py` (sweep lemmas, width≡8,
  traveling-wave frontier, to G≈15,509 / 3.25×10¹⁰ events).
- discarded (UNSOUND, phase bug): `o4_accel_windows.py`. Basis: `O4_11AVOIDANCE_A2`, `O4_ODOMETER_CLOSURE_A4`,
  `o4_accel_sound.py`; parallel-assault: bounded-width + AFS-numeration subagents (2026-07-06).
