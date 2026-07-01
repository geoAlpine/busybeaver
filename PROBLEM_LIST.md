# The problems that must be solved to decide BB(6) / Antihydra — definitive list (2026-07-01)

*A prioritized, honest inventory of the open problems standing between the current state and deciding the BB(6)
frontier. Each entry: statement, what it unlocks, dependencies, and an honest tractability call. SOUNDNESS: nothing
here is claimed solved; "hardness" tags reflect this program's proven barriers (No-Structure, Coverage No-Go,
decider-preemption, EVEN_COUNT_FLOOR). This supersedes/consolidates the ad-hoc open lists; it is a map of WHAT is
needed, not a claim any is close.*

---

## Tier 0 — the master goal

**P0. Determine BB(6) = Σ(6).** Requires: resolve (halting/non-halting of) every undecided 6-state holdout. BB(5)=
47,176,870 is proven (Coq, 2024); BB(6)'s lower bound is `Σ(6) > 2↑↑↑5` (mxdys, 2025). The obstruction is the
**cryptids** — holdouts whose halting is equivalent to open number-theoretic statements. `[OPEN, generational]`

---

## Tier 1 — the central kernel (unlocks the whole Mahler class)

**P1. (K) = the Mahler 3/2 / AEV kernel.** Prove: for `c_0=8`, `c_{n+1}=⌊3c_n/2⌋`, `liminf_n E_n/n ≥ 1/3`
(even-density; `E_n=#even`). Equivalently: `liminf` mean `D=v_2(3o-1) ≥ 3/2`; equivalently single-orbit
equidistribution of `c_n mod 2^k`; equivalently the floor-mirror of AEV Conj 1.6 at `p/q=3/2` ⟹ Mahler's 3/2
problem (1968).
- **Unlocks:** Antihydra non-halting, and (via the shared kernel) o10, o18, o15 — the whole BB(6) Mahler class at once.
- **Tractability:** `[OPEN, generational]`. Proven internally: no structural certificate (No-Structure), no
  rank-1 amenable framework (Coverage No-Go), no decider (decider-preemption), no sub-`(K)` rung on the even-count
  axis (EVEN_COUNT_FLOOR: the `Θ(log n)` floor is sharp). The residual is **single-realization genericity**.

**P1′. The precise missing tool.** Build: **effective single-orbit (quenched) equidistribution for a rank-1,
amenable, hyperbolic action on the `(2,3)`-solenoid** — equivalently, quenched 2-adic occupancy control for the
specified seed, crossing the **log-depth → linear-depth** reach gap (all unconditional tools reach `Θ(log N)`
depth; `(K)` needs `Θ(n)`). Must be non-spectral (`L_ann` odd-blind), non-structural (No-Structure), quenched (not
a.e./annealed), and a-priori (not assuming the D-law). `[OPEN — this is the new mathematics `(K)` requires]`

---

## Tier 2 — the per-cryptid problems

**P2. Antihydra.** = P1 (its non-halting is exactly `(K)`). The occupancy/RG theory (this program) is its
descriptive architecture; the quenched seat is P1. `[OPEN = P1]`

**P3. o10.** A nested two-level counter whose inner map is Mahler-`3/2` (`⌈3m/2⌉`). Non-halting reduces to the same
`(K)`-class kernel (single-orbit equidist of `⌊(3/2)^n⌋ mod 2`). `[OPEN = P1-class]`

**P4. o18.** Mahler-`8/3`: kernel = single-orbit equidist of `⌊(8/3)^n⌋ mod 3` (halt predicate = frontier-bit).
The `p=3` slice of the same family (occupancy/RG theory validated here empirically). `[OPEN, p=3 analogue of P1]`

**P5. o15.** Mahler-`8/3` class but **parity-irregular** (no clean 1-D map); shares the `p=3` equidistribution
kernel, with a messier (block-collision) halt predicate. `[OPEN, = P4-kernel + extra halt-predicate work]`

**P6. o17.** NOT in the Mahler family: a **carrying counter with unbounded digits** (off any fixed radix — sharper
than "base-3 odometer"; `O17_HALT_STRUCTURE.md`). Halt = left-frontier overflow; the embedded family `0A01^k` is
exact-linear off `3ℤ` and Collatz-irregular on `3ℤ` (no clean rule to `j=22`). **Problem:** determine whether the
carry is forever re-absorbed (non-halt) — a Collatz-type statement with no scalar/base reduction. `[OPEN, distinct
obstruction type; structurally the hardest to even place]`

**P7. The slow-width cryptids** (Space Needle, o2,o3,o4,o7,o11,o12,o13,o14,o16, Lucy's Moonlight). **Kernels
UN-EXTRACTED** (`CRYPTID_CENSUS.md`): the crude milestone extractor finds only near-linear growth; the real
growth/halt event is elsewhere or slower. **Problem (per machine):** reverse-engineer the tape mechanics → the exact
arithmetic kernel (as was done for Antihydra/o18). *Prerequisite:* their TMs (not in this repo; on bbchallenge).
`[OPEN, un-started; blocked internally on TM availability]`

---

## Tier 3 — supporting / intermediate problems (honest status)

**P8. Improve `#even(n)` past `Θ(log n)`.** `[PROVEN (K)-hard]` — EVEN_COUNT_FLOOR shows the `0.89 log n` floor is
sharp; any `ω(log n)` bound needs quenched cylinder-frequency = `(K)`. **Not a genuine sub-problem** (no sub-`(K)`
rung exists on this axis). Listed to mark it closed as an independent target.

**P9. Prove drift > 0 for the Antihydra balance walk.** `[= (K)]` — `drift = 2-3/meanD > 0 ⟺ meanD > 3/2`, i.e.
`(K)` itself. The elementary run-ceiling (`0.585·index`) exceeds the a.e. drift (`0.5·index`) by `1.17×`, so
elementary bounds are consistent with both halt and non-halt. Not independent.

**P10. Quenched Cramér / Lundberg bound.** `[= (K) via No-Structure]` — the golden-ratio annealed exponent
`θ*=logφ` is exact, but its deterministic (supermartingale/coboundary) realization is the `(C1)` sub-action proven
infeasible (`δ_1` maximizer). Not independent.

**P11. o17's `k≡0 mod 3` halting map.** Determine which `j=k/3` halt (Collatz-irregular; no rule found to `j=22`).
Sub-problem of P6; also a self-contained Collatz-type curiosity. `[OPEN]`

---

## Tier 4 — the external / meta problems (not internal math)

**P12. Named-conjecture status.** AEV Conjecture 1.6 (arXiv:2510.11723) is the weakest established-open named
conjecture implying `(K)`; Mahler's 3/2 problem is the classical ancestor. Progress on either moves P1.
`[OPEN in the literature; no unconditional partial density exists]`

**P13. Independence question.** Is Antihydra non-halting independent of PA/strong theories? `[PROVEN Π⁰₁; independence
~3-7% & untouchable]` — Antihydra encodes no metamathematics and is the wrong shape for Goodstein/Paris-Harrington
routes (LOGIC_INDEPENDENCE_PROBE). Effectively a dead end, listed for completeness.

---

## The dependency picture (what unlocks what)

```
P1′ (build the quenched-occupancy tool)
   └─> P1 = (K) = Mahler 3/2 / AEV
          ├─> P2 Antihydra   ─┐
          ├─> P3 o10 (inner)  ├─> the BB(6) Mahler class decided
          ├─> P4 o18          │
          └─> P5 o15 (+halt)  ─┘
P6 o17  (separate: unbounded-digit carry; own Collatz-type problem)
P7 slow-width ×10 (each: extract kernel first — blocked on TMs)
   └────────────────────────────────> all cryptids resolved => P0 BB(6) determined
```

## Honest priority

1. **P1′ / P1** is THE problem — one tool decides the whole Mahler class (P2–P5). It is generational; no internal
   route remains (proven), so genuine progress needs the new mathematics of P1′ (multi-year) or external movement on
   P12.
2. **P6 (o17)** and **P7 (slow-width)** are separate, each hard; P7 is additionally blocked internally (no TMs).
3. **P8–P10** are proven `(K)`-equivalent/hard — not independent handles.

**Net.** Deciding BB(6) requires solving P1 (the Mahler kernel, unlocking 4 cryptids) **and** P6 (o17) **and** P7
(the ten slow-width kernels), each generational or blocked. The single highest-leverage target is **P1′** — the
quenched single-orbit equidistribution tool — which does not yet exist in any field. **No machine decided. No label
upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
