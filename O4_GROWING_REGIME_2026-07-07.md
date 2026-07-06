# o4 growing-regime closure — the three √-growth configs are the PURE BODY attractor (translated bouncer); all three NON-HALTING [PROVEN — candidate] (2026-07-07)

*Closes the last completeness item of the small-a fatal-region map (`O4_LEDGER_ANALYSIS_2026-07-06` §4 / WANDER
RESOLUTION): the three standalone configs `Z(k, g=3, a=0)`, k ∈ {21, 23, 27}, that entered a milestone-free
√steps-growth regime (not translated cyclers at horizon 8M / W=10⁴). Their attractor is identified and certified:
they collapse to the **bare-zone family C(m) — the body lemma with nothing to its right** — and iterate
`C(m) → C(m+2)` forever: a **translated bouncer**. All three are NON-HALTING
`[PROVEN — candidate, pending main-loop re-verification]`. o4 itself stays `[OPEN]`. No machine decided.*

Machine: o4 = `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---` (halt = F reads 1).
Scripts: `o4_growing_probe.py` (RLE dumps), `o4_growing_genlaw.py` (generation map + entry), `o4_growing_certify.py`
(the full certificate; all assertions pass).

## 1. The attractor `[OBSERVED → identified exactly]`
RLE dumps at new-leftmost events (`o4_growing_probe.py`): after a transient, all three configs' tapes collapse to a
**single block** —
**`C(m) := 0^∞ [head, state A, on 0] (10)^m 0 1 0^∞`** (= bare zone `(10)^(m−1) 1001`, head one cell left, state A;
**no gap, no filler**). This is why the milestone detector never fired: the milestone form `M(G,a)` requires
zone+gap+filler; here the gap/filler are consumed in the transient and the machine is left iterating the zone alone.
(The macro run's "5 segments" was an artifact of the off-template representation-maintenance issue already flagged in
the WANDER RESOLUTION; concrete dumps show 1 block.)

**The structural identity:** `C(m)` is exactly the body-lemma config `B(m−1)` (`o4_body_proof.py`) after ONE step
(`E1 = 1LA`) — tape sets identical, mechanically asserted (`check_conjugation`). The growing regime is the **pure
body iteration with an empty right context**.

## 2. The generation law `[measured exactly, grid m=2..1001 + spot checks to 100001]`
**`C(m) → C(m+2)`, shifted −1, in exactly `4m+11` steps** (= body's `15+4(m−1)`), head span `[−2, 2m+4]`, unsafe = 0,
no halt — uniform in m, BOTH parities, no residue classes, no ledger. Leftmost −1/generation; steps to generation n
from entry `= 4n² + 15n` ⇒ leftmost ~ √steps/2 — quantitatively matching the old macro observation
(1.1×10¹² steps ⇒ n ≈ 524k vs the reported G ≈ 530k ✓), and explaining the failed cycler search: the window content
grows every generation, so no exact recurrence exists (bouncer, not cycler).

## 3. The certificate (`o4_growing_certify.py`, all PASS)
1. **Sweep lemmas `[PROVEN]`:** `B1F0` read-only rightward, `D1E0` invert leftward — transition-table check +
   2-transition induction (same lemmas as the template closure).
2. **Entry `[concrete, exact]`:** `Z(21,3,0) →(1791 steps)`, `Z(23,3,0) →(24109)`, `Z(27,3,0) →(2539)` the EXACT
   global config `C(2)` at a new-leftmost cell (−27/−157/−31; cells left unvisited hence 0; 1-cells matched exactly);
   no halt, unsafe=0 en route. **All three land on the same family at the same parameter m=2** — one family, three
   transients.
3. **Small-m chain `[concrete, exact]`:** `C(m) → C(m+2)` exact global config for every m = 2..18.
4. **Template lemma for m ≥ 19 `[certified trace-template method, red-team-corrected form]`:**
   skeleton IDENTICAL across m = 19..251 both parities (11 items: 9 episodes + 2 sweeps); sweep lengths exactly
   affine `(2m, 2m+2)` (= body's `(2+2k, 4+2k)` at k=m−1); **episode-landmark pinning:** all 9 episode steps at
   m-independent offsets (≤3) from the left edge (3) or right terminator (6) — with sweeps traversing only the
   uniform `(10)^*` region the tape is symbolically reconstructible and the first-divergence argument closes;
   endpoint-exact spot checks at m = 1000..100001. **Moreover the even-m instances — the only ones the orbit uses —
   are INHERITED from the already-proven body lemma** (odd k ≥ 19) via the 1-step conjugation, so the new
   certification burden beyond banked results is only the concrete pieces (2)–(3).
5. **Induction:** from `C(2)` the exact global orbit is `C(2) → C(4) → C(6) → …` forever, halt-free at every step.

**⇒ `Z(21,3,0)`, `Z(23,3,0)`, `Z(27,3,0)` are NON-HALTING [PROVEN — candidate, pending main-loop re-verification].**

## 4. Consequence for the small-a map
The a=0 WANDER row of `O4_LEDGER_ANALYSIS` §4 is now fully resolved: k=29,101 translated cyclers `[PROVEN]`
(`o4_wander_certify.py`), k=21,23,27 translated bouncers `[PROVEN — candidate]` (this note). The small-a exit mix is
exactly **{recover-to-template / halt (k=41) / translated cycler / translated bouncer}** — every observed outcome now
carries a certificate or a proof. The ledger conjecture (the a≥2-at-ρ=1 condition) remains the sole `[OPEN]` core of o4.

## 5. Soundness ledger `[discipline]`
- Entry + small-m chain are RAW CONCRETE simulation with exact global-config equality (tape dict stores exactly the
  1-cells; zeros popped; new-leftmost ⇒ everything left unvisited ⇒ 0). No acceleration anywhere in the proof path.
- The m≥19 generalization step is the **certified trace-template method** — the same standard (and the same red-team
  corrections: landmark pinning) as the closed body/prefix/suffix lemmas, hence the "candidate, pending main-loop
  re-verification" qualifier; the even-m subchain is additionally covered by the banked body lemma.
- These are STANDALONE configs: reachability from o4's initial tape is NOT claimed (that is exactly the open ledger
  question). No claim about o4 itself is upgraded.
- Honest residual: the trace-template generalization is grid-certified, not machine-checked symbolic induction —
  identical status to every other template-closure lemma in the o4 track.

o4 `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce
- `/Users/aokiyousuke/quantum-ecc/.venv/bin/python o4_growing_certify.py` (full certificate, ~seconds).
- `o4_growing_probe.py` (attractor discovery dumps), `o4_growing_genlaw.py` (generation map m=4..1001 + entries).
- Basis: `o4_body_proof.py` (body lemma), `O4_TEMPLATE_CLOSURE_2026-07-06.md` (method + red-team),
  `O4_LEDGER_ANALYSIS_2026-07-06.md` §4 (the open row), `o4_wander_certify.py` (sibling cyclers).
