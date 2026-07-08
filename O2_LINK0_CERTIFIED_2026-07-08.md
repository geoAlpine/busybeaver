# o2 Link 0 certified: the milestone automaton is a theorem of the certified trace-template method (2026-07-08)

*Closes the single foundational gap of the second Antihydra flagged in `X32_FAMILY_REDUCTIONS_2026-07-07.md` §1.4
and `X32_CLEANUP_2026-07-08.md` §1.0: o2's Link 0 (machine ⟺ milestone automaton) was `[OBSERVED, 0-mismatch:
17 raw transitions + 320 seeded configs]` — "honestly still not a certified induction" — where Antihydra's is
`[PROVEN]` and o4's lemmas are `[PROVEN, certified trace-template]`. This note upgrades o2's Link 0 to the o4
standard, by the method of `PAPER_TEMPLATE_METHOD.md` §2 in its red-team-corrected form (episode-landmark
pinning mandatory). SOUNDNESS: every claim labeled; all checks exact concrete simulation + exact integer/
Fraction identities, assertion-checked in `o2_link0_certify.py` (interpreter
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, runs in ~6 s). **No machine decided.***

## 0. Headline

| item | result |
|---|---|
| **Link 0** | `[OBSERVED, 0-mismatch]` → **`[PROVEN, certified trace-template method]`** — for **all** (a,b), a ≥ 1, b ≥ 0, all four branches, no intermediate milestone, halt-gate silent except the predicted HALT firing |
| **decomposition** | one milestone transition = `prefix(10) · unit(k)^J · exit`, with a **single canonical 16-item unit** (14 landmark-pinned episodes + 2 sweeps `B1E1`/`C0A1` of lengths 6k+2, 6k+4) reused by **both phases of the b=0 branches**; 7 exit templates |
| **cut invariant** | every F-event is a structural cut; the global config at cut c is **exactly** `0^∞ 1^{6c−1} 0 [F:1] (01)^m ⟨rest⟩ 0^∞` (p = 6c−1, head 4c, block edge −2c); phase-2 filler length **(3a+7)/2 — its parity IS the mod-4 halt/escape criterion** |
| **certificate size** | 474 full transitions (a ≤ 1001, b ≤ 1000, corner [1,40]×[0,10] complete); 8,977 unit instances k ≤ 753 + standalone units at k = 1000/5000/20000; 7 exit families, skeleton-identical, sweep lengths exactly affine, all items pinned (max offset 9) |
| **cross-check** | derived closed-form step counts reproduce the banked 10⁸-step blank run **exactly**: 44 + 17 certified transitions = D(7187,11) at raw step **62,095,432** (`X32_CLEANUP` §1.0) |
| **chain effect** | every o2 theorem loses the "given the automaton" caveat at the certified-trace-template standard; **the one `[OPEN]` link is now exactly the (K)-shaped ledger/hatch condition** — o2 reaches parity with o4: finitely many certified lemmas + one explicit arithmetic conjecture |

## 1. Statement

`o2 = 1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA` (halt F,0; unique edge into F: `D,0→0RF`, so every F-event
is a D-read-0, and HALT ⟺ that 0 has right neighbour 0). **Milestone** `D(a,b)`: state A, head on a 0, all
cells strictly left blank, tape rightward `0·11·(01)^a·0·11·(01)^b·0^∞` (a ≥ 1, b ≥ 0).

> **Link 0 `[PROVEN, certified trace-template method]`.** From any milestone D(a,b) the raw machine evolves,
> halt-free and with no intermediate milestone configuration, exactly to:
> - a even: `D((3a+4)/2, b+2)` at head offset −(a+4);
> - a odd, b ≥ 1: `D((3a+7)/2, b−1)` at −(a+5);
> - a ≡ 3 (mod 4), b = 0: `D((9a+29)/4, 1)` at −(5a+25)/2 (escape);
> - a ≡ 1 (mod 4), b = 0: **HALT** (F reads 0) at 2a+8, final tape `1^{(9a+37)/2}` from −(5a+23)/2.
>
> This is the milestone automaton of `CRYPTID_SLOWWIDTH_2026-07-04.md` §1 in composed form, now for the whole
> cone, with landing offsets and step counts exact.

## 2. The decomposition (found from microstep logs)

**Sweep lemmas `[PROVEN, 2-transition induction from the table]`.** o2 has one 2-cycle in each direction, and
both are *inverting* (o4's rightward sweep was read-only; o2's are not):
- `B1E1` (B:1→1LE, E:1→0LB): leftward, converts `1^{2n} → (01)^n` in 2n steps;
- `C0A1` (C:0→1RA, A:1→1RC): rightward, converts `(01)^n → 1^{2n}` in 2n steps (entered on the A-phase it is
  `A1C0`, converting `(10)^n`, which appears once in the even-branch exit).
Both periods are 2 (o4's p=2 as well; o2 needs no longer cycles). Conditional: valid while the region ahead is
correctly tiled — the cut invariant below supplies exactly that.

**Cut invariant.** F is entered only by `D,0→0RF`; F reading 1 continues, F reading 0 is the halt. So the
F-events cut every transition into `prefix · segments`. Verified at **every cut of every certified run**, the
global configuration at the c-th cut is exactly:

| phase | shape (head on the [F:1] cell) | parameters |
|---|---|---|
| 1, c = 1..⌈a/2⌉ | `W: 0^∞ 1^{6c−1} 0 [F:1] (01)^m 0 11 (01)^q 0^∞` | m = a−2c+1, **q = b untouched**, head 4c, block edge −2c |
| 1-exit, a even | `T: 0^∞ 1^{3a+5} 0 [F:1] 1 (01)^b 0^∞` | head 2a+4 |
| 1-exit, a odd | `W with m = 0` | head 2a+2 |
| 2 (b=0 only), c₂ ≥ 1 | `V: 0^∞ 1^{6c₂−1} 0 [F:1] (01)^{m₂} 0^∞` | m₂ = (3a+7)/2 − 2(c₂−1), head −(a+1)+4(c₂−1) |

The phase-2 filler starts at length **(3a+7)/2**, and its **parity is the mod-4 criterion**: a ≡ 3 (mod 4) ⟹
even ⟹ phase 2 drains to V(m₂=0) and escapes; a ≡ 1 (mod 4) ⟹ odd ⟹ drains to m₂ = 1 and the next F-entry
reads a blank 0: HALT. (The machine-level meaning of Link 2's escape hatch.)

**Prefix `[certified]`:** a fixed 10-step word (`A0 B1 E1 B0 C0 A1 C0 A1 C1 D0`), span [−2,3], identical raw
(op, position) sequence in all 474 runs; content is milestone-determined for every a ≥ 1, b ≥ 0; lands cut 1.

**Canonical unit `[certified trace-template]`:** from any W/V cut with m ≥ 1, the next segment is a fixed
**16-item skeleton** — 14 episodes + `B1E1` (length 6k+2, start h0+1) + `C0A1` (length 6k+4, start L−2), where
k = cut index, h0 = head, L = h0−6k = block left edge — taking exactly **12k+20 steps**, touching exactly
[L−2, h0+3], landing on the next cut (block +6 ones, m −= 2, everything right of h0+3 untouched). Episode
pinning: `F1@R+0 A0@R+1 B1@R+2 E1@R+1 B1@R+0 E0@R−1 A1@R−2 C1@R−1 D1@R+0 E0@R+1 A0@R+0 B0@L−1 C1@R+2 D0@R+3`
(R = h0; max offset 3 — the o4 pinning bound met exactly). The read window [h0, h0+3] is `1,0,1,0` for
**every** m ≥ 1 (at m = 1 the terminator/blank 0 aligns with the pattern 0), so one template serves the whole
loop, both phases, all branches, down to the last iteration.

**Exit templates `[certified trace-template]`** (skeletons identical across their whole grids; sweep lengths
exactly affine — Fraction fits verified at every point; every episode and sweep-start pinned to an anchor from
{exit head F, right end R = 2a+2b+5, landing point P, block edge L}):

| class | validity | items | sweeps (exact) | lands |
|---|---|---|---|---|
| SUF_EVEN_G | a even, b ≥ 3 | 17 | `A1C0` 2b+2, `B1E1` 2b+6, `B1E1` 3a+6 | D((3a+4)/2, b+2) @ −(a+4) |
| SUF_EVEN_B0/B1/B2 | a even, b = 0/1/2 | 23/20/22 | (b-sweeps below compression: per-b variants, §2.5 form) + `B1E1` 3a+6 | same law |
| SUF_ODD | a odd, b ≥ 1 | 21 | `B1E1` 3a+5, `C0A1` 3a+7, `B1E1` 3a+9 — **b-gradient exactly 0** | D((3a+7)/2, b−1) @ −(a+5) |
| MID | a odd, b = 0 (both residues) | 31 | same three lengths as SUF_ODD | phase-2 entry V @ −(a+1) |
| SUF_ESC | a ≡ 3 (4), b = 0 | 19 | `B1E1` (9a+33)/2 | D((9a+29)/4, 1) @ −(5a+25)/2 |
| TERMINAL | a ≡ 1 (4), b = 0 | = canonical unit | — | F-entry reads 0: HALT @ 2a+8, exact final block |

SUF_ODD's zero b-gradient is the certified form of "the b-filler is untouched until landing": its only contact
is one read of its leading 0; the b-decrement is boundary reinterpretation at the landing, not traversal. The
b-filler-crossing sweeps live in the even branch (2b+2, 2b+6).

## 3. The certificate (what was checked, exactly)

- **Grids (full trace, every check per run):** EVEN a ∈ {2,4,…,40,100,250,1000} × b ∈ {0,1,2,3,4,7,10,…};
  ODD a ∈ {1,3,…,41,101,251,1001} × b ∈ {1,2,3,7,10}; ESC a ∈ {3,7,…,43,103,251,999}; HALT a ∈
  {1,5,…,41,101,401,1001}; b-spots (6,50),(6,251),(6,1000),(7,50),(7,1000); complete corner [1,40]×[0,10].
  **474 transitions**, each verified: landing = automaton + exact offset; every cut parses to the exact
  predicted shape (q = b at every phase-1 cut); prefix word identity; every unit segment = canonical template
  with exact span; halt-gate fires 0 times (non-halt branches) / exactly once (HALT); exact final halted tape.
- **Units:** 8,977 in-run instances, k ≤ 753, zero deviations; plus **standalone** V-shape instances at
  k = 1000, 5000, 20000 × m ∈ {1,2,3,11}: unit word == canon, span [−6k−2, +3], 12k+20 steps, exact landing
  (m ≥ 2) and the isolated terminal halt (m = 1).
- **Families:** 7 exit classes, 22–212 instances each, skeleton-identical, all items pinned (max offset 9),
  sweep lengths exactly affine in (a,b).
- **Cross-check against the bank:** the derived closed forms (unit 12k+20; exits: EVEN_G 28+3a+4b, B0 28+3a,
  B1 32+3a, B2 36+3a; ODD 39+9a; MID 49+9a; ESC 69/2+9a/2) match all 474 run totals exactly, and the abstract
  blank chain 44 + Σ(17 transitions from D(2,1)) lands D(7187,11) at raw step **62,095,432 — equal to the
  banked 10⁸-step raw log** (`X32_CLEANUP` §1.0). Blank → D(2,1) at step 44 re-verified concrete.

## 4. Composition argument (red-team-corrected form) and label

Prefix: fixed word on a fixed window whose content every milestone (a ≥ 1) supplies. Units and exits: every
episode step is landmark-pinned at a parameter-independent offset (≤ 9) from a structural landmark; every
parameter-dependent stretch is one of the proven sweeps over a region whose exact content the cut invariant
fixes; hence the tape is **symbolically reconstructible** at every step, and the first-divergence argument
closes: skeleton identity + exactly-affine sweep lengths on the grids certify each lemma on its whole cone
(`PAPER_TEMPLATE_METHOD.md` §2.4). Induction on cuts composes them: **Link 0 for all (a,b), a ≥ 1, b ≥ 0**,
including "no intermediate milestone" (at every step of every template the head has the growing 1-block or a
non-milestone local shape on its left — verified configurationally in all 474 runs, symbolically off-grid).
Small parameters need no per-a variants (suffix skeletons are uniform down to a = 1); the even branch needs
the three per-b variants b = 0,1,2 (§2.5 small-parameter restatement), and the corner is covered concretely.

> **LABEL: o2 Link 0 `[OBSERVED, 0-mismatch]` → `[PROVEN, certified trace-template method]`.**
> *Epistemic status (unchanged from o4's standard):* grid-certified composition argument with mandatory
> episode-landmark pinning; **not** a machine-checked (Lean/Coq) symbolic induction. Exactly the label under
> which o4's prefix/body/suffix lemmas are banked.

## 5. The chain, re-derived

With Link 0 certified, every "given the automaton" caveat in o2's chain resolves to the same standard:
- **Link 1** (conjugacy: universal manifold 3 | a+4, `y = (a+4)/3 ↦ ⌈3y/2⌉` exactly, escape = two ceiling
  steps) — `[PROVEN, certified trace-template + exact algebra]`.
- **Link 2** (halt ⟺ b = 0 at y ≡ 3 (mod 4); escape reseeds b = 1) — same, and now with its machine-level
  mechanism: the parity of the phase-2 filler (3a+7)/2.
- **Link 3** (ledger `b_n = 1 + 3E_n − n`; ceiling gap lemma `T̂(o) = 3^{G−1}(3o+1)/2^G`; run form
  halt ⟺ ∃i: s_i ≥ B_i + 2) — same.
- **`[OPEN]`, the one remaining link:** the ledger/hatch condition — the (y,b) process from (2,1) never
  reaches b = 0 ∧ y ≡ 3 (mod 4); implied by ceiling-(K) seed 2 (+ the finite check, verified n ≤ 10⁶).

o2 now sits at o4's evidential standard precisely: **finitely many certified trace-template lemmas + one
explicit Collatz-like arithmetic conjecture.** Differences that remain: o4's ledger is a finite-residue δ-map
(its open core is the odometer run structure); o2's is the Antihydra-type cumulative balance with the mod-4
hatch — a strictly-weaker-than-(K) target, but a (K)-species wall. The AIU/no-structure meta-theorems still
have not been formally ported to the ceiling side (`X32_CLEANUP` §1.5) — o2's (K)-hardness stays inherited
morally, `[OPEN]` formally.

## Reproduce

`/Users/aokiyousuke/quantum-ecc/.venv/bin/python o2_link0_certify.py` (~6 s; all checks are assertions:
gate + sweep lemmas from the table; blank base; canonical-unit extraction D(40,3); 474 grid+corner transitions
with per-cut exact shape parsing; standalone units to k = 20000; 7 exit families pinned + affine; closed-form
step counts + the 62,095,432 blank-chain identity; prints the composition summary).

**o2's halting stays `[OPEN]`; this note certifies the reduction's foundation, not any non-halting claim.
Link 0's evidence label is upgraded as stated; no halting verdict changed anywhere.
No machine decided. No label upgraded.**
