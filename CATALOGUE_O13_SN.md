# Frontier catalogue — Space Needle, o13, o14, o16 (2026-06-28)

Per-machine deep characterisation of four assigned BB(6) cryptids. **Soundness paramount.** Every claim is
`[PROVEN]` (conjecture-free / elementary) / `[VERIFIED]` (machine-checked this session via the exact-bigint
`bb_sim`, not promoted to a proof) / `[OBSERVED]` (numeric pattern, no proof) / `[OPEN]`. **No machine is
decided; no non-halting is asserted unconditionally.** All numerics use `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`
(exact integer tape simulation) and were cross-checked against `bb_sim.run`.

## Exact specs (from `suite.py` CRYPTIDS — verbatim)
| name | spec |
|---|---|
| Space Needle | `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD` |
| cryptid o13 | `1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA` |
| cryptid o14 | `1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE` |
| cryptid o16 | `1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE` |

## Headline summary
| machine | envelope (`w/√t`) | structure | halt discriminator (verified) | kernel / content | decidable by our tools? |
|---|---|---|---|---|---|
| **Space Needle** | **exponential** (`w/√t`↓: 1.20→0.82→0.63→0.48→0.31) | two/three-counter `1^a 0 1^b 0 1^c` | **F reads 0** (F entered `C:0→1LF`) | **Mahler μ=5/2, p=2, T(x)=⌊5x/2⌋** `[VERIFIED]` | **NO — HOLDOUT** |
| **o13** | poly/sawtooth (`w/√t`≈1.0–1.26) | two-counter `1^a 0 1^b` + shrinking single-`1` tail | **E reads 0** (E entered `D:1→1LE`) | irregular geometric (Collatz) content | **NO — HOLDOUT** |
| **o14** | poly/sawtooth (`w/√t`≈1.0–1.5) | two-counter `1^a 0 1^b` over single-`1` field + `4,4,2` marker | **F reads 0** (F entered `C:0→1LF`) | irregular geometric (Collatz) content | **NO — HOLDOUT** |
| **o16** | poly/sawtooth (`w/√t`≈1.4–1.7) | single roaming `1^big` defect over `(10)*` sea, decaying leading `1^k` | **F reads 0** (F entered `E:0→1RF`) | irregular geometric (Collatz) content | **NO — HOLDOUT** |

This is consistent with, and refines, the existing `CRYPTID_REDUCTIONS.md` Stage-1 catalogue (Space Needle = T1
two-counter exponential; o13/o14 = T1 sawtooth; o16 = T2 single-defect sawtooth). **The one genuine refinement
is the Space Needle multiplier: 5/2, not 3/2** (§1).

---

## 0. Decidability / lottery check (rigorous; default HOLDOUT) — `[VERIFIED]`
All four were given the SOUND deciders with **generous** parameters. Every one is HOLDOUT; **none is decided**.

| machine | bb_sim non-halt | `far_dfa.prove` (m≤8, N≤8000) | `far_finder.prove` (k≤6, N≤5000) | `far_cegar.prove` (120/60 rounds) |
|---|---|---|---|---|
| Space Needle | no halt to 50M | HOLDOUT | HOLDOUT | HOLDOUT (not closed) |
| o13 | no halt to 50M | HOLDOUT | HOLDOUT | HOLDOUT (not closed) |
| o14 | no halt to 50M | HOLDOUT | HOLDOUT | HOLDOUT (not closed) |
| o16 | no halt to 50M | HOLDOUT | HOLDOUT | HOLDOUT (not closed) |

Halt-discriminator audit (50M steps, exact sim): the halting read **never fires** —
Space Needle F-visits = 1231 (all read 1), o13 E-visits = 7261 (all 1), o14 F-visits = 6382 (all 1),
o16 F-visits = 15 (all 1). **No DECISION claim is made for any machine. Default HOLDOUT stands.** The sound
`far_dfa.verify` gate did not confirm any invariant and the cryptid gate is not reached; per the discipline,
a DECIDED claim is withheld.

---

## 1. Space Needle — `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD`

**Transitions.** A:`0→1RB,1→1LA`; B:`0→1LC,1→0RE`; C:`0→1LF,1→1LD`; D:`0→0RB,1→0LA`;
E:`0→1RC,1→1RE`; F:`0→---,1→0LD`.

**Halt discriminator `[PROVEN from spec, VERIFIED]`.** The only halt is **F reading 0**. F is reached solely via
`C:0→1LF` (write 1, move left into F). So Space Needle halts ⟺ a leftward `C→F` sweep, having written a 1, finds
a **0 immediately to its left** (an adjacent-`0` / left-frontier alignment). `[VERIFIED]` 1231 F-entries in 50M
steps, all read 1 (no halt).

**Genuine dynamics `[VERIFIED]`.** At the left extreme in state A the tape is `1^a 0 1^b (0 1^c)` — a
**two-counter, occasionally three-counter** configuration (the Antihydra/Hydra template). Within an epoch the
left counter decrements and the inner counter accumulates (`a→a−1, b→b+2` in the clean 2-block phase); when the
left counter bottoms out the epoch **resets** to `1 0 1^{b'}`. The reset orbit is the genuine growth event.

**The real growth event = exact ×5/2 `[VERIFIED]`.** Clean reset configs `1^1 0 1^b` over 150M steps give
`b = 12, 36, 96, 246, 621` (widths `15, 39, 99, 249, 624`). The **first differences are `24, 60, 150, 375` —
each exactly ×2.5** (60=24·5/2, 150=60·5/2, 375=150·5/2). Hence the kernel multiplier is **μ = 5/2 exactly**, i.e.
the clean induced map is `b ↦ ⌊5b/2⌋`-type on ℤ₂ (`T_μ(x)=⌊5x/2⌋`). Time per epoch grows ×≈11–15 while width grows
×5/2, so `time ~ width^{2.9}` (super-quadratic) ⇒ **exponential-envelope** (the lone exponential machine of the four;
`w/√t` decreases 1.20→0.31). The orbit is **irregular** off the clean phase (an intermittent 3-block `1 0 1^b 0 1^c`
phase, e.g. `[1,308,470]`, and floor/carry rounding since `24·(5/2)^k` is non-integral) — exactly the "irregular
geometric content" signature.

**Classification (b) — Collatz-kernel `T_μ`.**
- **kernel multiplier μ = 5/2, prime p = 2, `v₂(μ) = −1`** `[VERIFIED]`. This places Space Needle in the **same
  expanding-kernel CLASS as Antihydra** (`v_p(μ)=−1`, clean p-to-1 Haar-preserving `T_μ(x)=⌊μx⌋`; 5/2 is one of
  the multipliers explicitly `[VERIFIED]` clean in `BB6_STRUCTURAL_LIMIT_THEOREM.md` §4.1), but with a **different
  multiplier (5/2, not 3/2)**.
- **REFINEMENT (soundness):** `CRYPTID_REDUCTIONS.md` Stage-1 tagged Space Needle "Mahler-3/2-type." That was a
  loose family tag from coarse sampling; the **exact clean-reset differences give 5/2, not 3/2** (this session,
  `[VERIFIED]`). 5/2 is *not* of the `2^a/3^b` form, so Space Needle is **not** in the Erdős/`2^a/3` cluster nor
  the literal Antihydra 3/2 orbit — it is its own `μ=5/2`, `p=2` member of the clean expanding-kernel class.
- **facet:** existence-type (halt = a 2-adic carry/adjacency alignment of the `(5/2)^n` orbit at the C→F frontier),
  analogous to o18's frontier alignment but at multiplier 5/2. No clean scalar halt criterion derived beyond
  "F reads 0 ⟺ left-frontier 0-adjacency", which is `[PROVEN from spec]`.

**What Space Needle computes.** It runs a `⌊5x/2⌋`-type Mahler counter: a two-counter that repeatedly multiplies
its accumulator by 5/2 (exact integer differences ×5/2), building the tall thin "needle" space-time tower
(narrow exponential growth, `width ~ (5/2)^{epoch}`, time ~ width^2.9) the bbchallenge community named it for.
It **halts ⟺ the leftward C→F sweep ever lands a written 1 next to a 0 at the left frontier** = a 2-adic
adjacency/carry alignment event of the `(5/2)^n` orbit — an event that never occurs in 50M steps (1231 frontier
reads, all 1). This is the **5/2 analogue of Antihydra's 3/2 Mahler problem**: single-orbit equidistribution /
carry-avoidance of `⌊(5/2)^n x⌋` on ℤ₂. **`[OPEN]` — Mahler-class, in-class-not-in-proof-scope.**

**Decidable?** **NO.** HOLDOUT under all sound deciders (§0). Mahler-class hardness; no sound certificate found.

---

## 2. o13 — `1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA`

**Halt discriminator `[PROVEN from spec, VERIFIED]`.** The only halt is **E reading 0**. E is reached solely via
`D:1→1LE`. So o13 halts ⟺ a leftward `D→E` step lands the head on a 0. `[VERIFIED]` 7261 E-entries in 50M steps,
all read 1 (no halt).

**Genuine dynamics `[VERIFIED]`.** At the left extreme (milestone state C/D) the tape is `1^a 0 1^b 0 1 0 1 0 1`
— **two big counters** plus a short trailing run of single `1`s (3 of them) acting as markers. The two big blocks
**swap mass irregularly** across epochs: `[186,97]→[534,61]→[793,112]→[883,631]→[1627,496]→[411,2320]→[2748,286]`
(milestones at t≈8·10⁴…8·10⁶). The single-`1` tail count drifts down (15→11→8→7→6→5 blocks). Within an epoch the
clean local rule is `a→a−2, b→b+3`.

**Classification (d→b) — two-counter, irregular geometric content.** Poly/sawtooth envelope (`w/√t`≈1.0–1.26,
width ~√t), but the **content** (which counter holds the mass, and the mass values) is **Collatz-irregular** — no
clean scalar map fits the block-swap orbit `[VERIFIED]` (the `186,534,793,883,1627,411,2748` peak series is
non-monotone and non-geometric in the sampled milestones). This is the T1 two-counter template with irregular
`2^a/3^b`-rate content; it is *why* bouncer/FAR deciders correctly hold out (regular envelope, irregular content).
No exact arithmetic halt kernel cleanly extracted (the swap is not a single-variable orbit). Facet: existence
(halt = D→E lands on a 0).

**Decidable?** **NO.** HOLDOUT under all sound deciders. `[OPEN]`, "too irregular yet" for an exact reduction.

---

## 3. o14 — `1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE`

**Halt discriminator `[PROVEN from spec, VERIFIED]`.** The only halt is **F reading 0**. F is reached solely via
`C:0→1LF`. So o14 halts ⟺ a leftward `C→F` step lands the head on a 0. `[VERIFIED]` 6382 F-entries in 50M steps,
all read 1 (no halt).

**Genuine dynamics `[VERIFIED]`.** At the left extreme (milestone state E) the tape is
`1^a 0 1 0 1^b 0 (single-1 field) 0 1^4 0 1^4 0 1^2` — **two big counters** (`a`, the inner `b`) embedded in a
field of single `1`s, capped by a fixed `4,4,2` marker tail. The two big counters swap mass irregularly:
`[121,21]→[306,79]→[735,121]→[982,572]→[1225,1027]→[2406,544]→[2626,1018]→[3786,556]→[3324,1249]` (t≈4·10⁴…3·10⁷).
Block count slowly decreases (54→36). Leading counter trends upward.

**Classification (d→b) — two-counter, irregular geometric content.** Poly/sawtooth envelope (`w/√t`≈1.0–1.5).
The big-block swap is **Collatz-irregular** (no clean scalar map) `[VERIFIED]`. T1 two-counter template (with a
single-`1`/`(10)*`-like spacer field and a `4,4,2` marker) carrying irregular `2^a/3^b`-rate content. Facet:
existence (halt = C→F lands on a 0). No exact arithmetic halt kernel cleanly extracted.

**Decidable?** **NO.** HOLDOUT under all sound deciders. `[OPEN]`, "too irregular yet."

---

## 4. o16 — `1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE`

**Halt discriminator `[PROVEN from spec, VERIFIED]`.** The only halt is **F reading 0**. F is reached solely via
`E:0→1RF`. So o16 halts ⟺ a rightward `E→F` step lands the head on a 0. `[VERIFIED]` only **15** F-entries in 50M
steps (rare event), all read 1 (no halt).

**Genuine dynamics `[VERIFIED]`.** At the right extreme (milestone state A/B/C) the tape is
`1^k 0^2 (10)* 1^big` — a **decaying leading block** `1^k` (k: 21→…→8, drifting to a small constant), a `(10)*`
background sea, and a **single roaming `1^big` defect** whose peak grows irregularly:
`76→708→1068→142→3586→3096→636→4080→4998→5226` (t≈7·10⁴…3·10⁷). The number of `(10)` cells fluctuates wildly
(22→227→1264→116→936→2741→1593 blocks) as the defect roams. This is the **T2 single-defect template** (o4/o16
family), distinct from the two-counter machines above.

**Classification (d→b) — single drifting defect, irregular geometric content.** Poly/sawtooth envelope
(`w/√t`≈1.4–1.7). The defect **magnitude grows geometrically but its fine structure is Collatz-irregular**
(non-monotone peak series) `[VERIFIED]`. No clean scalar map for the defect orbit. Facet: existence (halt = the
roaming defect ever forces E→F onto a 0 at the right frontier; it stays away — only 15 frontier touches in 50M).
No exact arithmetic halt kernel cleanly extracted.

**Decidable?** **NO.** HOLDOUT under all sound deciders. `[OPEN]`, "too irregular yet."

---

## 5. Net findings
1. **All four are HOLDOUT under every sound decider** (far_dfa / far_finder / far_cegar, generous params) and
   non-halting to 50M steps with the halt read never firing. **No machine is decidable by our sound tools.**
   No DECISION claimed; default HOLDOUT enforced. (Lottery: empty.)
2. **Halt discriminators pinned exactly** (`[PROVEN from spec]`): Space Needle / o14 = `C:0→1LF` then F reads 0;
   o16 = `E:0→1RF` then F reads 0; o13 = `D:1→1LE` then E reads 0. All are **left/right-frontier 0-adjacency
   (existence) events** — none is a density criterion.
3. **Space Needle's multiplier is μ = 5/2 (p=2, v₂=−1), not 3/2** — the one substantive refinement to the
   existing catalogue. `T_μ(x)=⌊5x/2⌋`, in the clean expanding-kernel class (alongside Antihydra's 3/2) but a
   distinct multiplier; 5/2 ∉ `{2^a/3^b}` so it is neither the literal Antihydra orbit nor the Erdős/`8·3⁻¹`
   cluster. What it computes: a `⌊5x/2⌋` Mahler counter (the tall "needle" tower), halting iff a 2-adic
   frontier-carry alignment of `(5/2)^n` ever occurs — the 5/2 analogue of Antihydra's Mahler problem. `[OPEN]`.
4. **Structure templates confirmed:** Space Needle / o13 / o14 = two-counter `1^a 0 1^b` (T1); o16 = single
   roaming defect over `(10)*` (T2). Space Needle alone has an **exponential** width envelope; o13/o14/o16 are
   **poly/sawtooth** (`w/√t` roughly constant) with irregular geometric content underneath. Envelope difference
   is cosmetic; deep content is uniformly irregular `2^a/3^b`-rate (Mahler/Collatz), per the settled catalogue.

*Soundness: zero false proofs; no machine decided; no non-halting asserted unconditionally. Multiplier 5/2 is
`[VERIFIED]` (exact integer difference ratios over 4 clean epochs), not promoted to `[PROVEN]`. All sim via the
.venv exact-bigint interpreter, cross-checked against `bb_sim`.*
