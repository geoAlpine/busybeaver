# The carry calculus on the integer-×2 machine — the low-part decoded, the "counter-dependent" wall dissolved (2026-07-11)

*The carry-calculus attack on `M = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE`: derive the
low-part (odometer register) update law instead of instrumenting carries as opaque
observations. Interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact big-int /
exact bytearray / exact symbolic-RLE. Scripts `x2cc_fast.py` (exact accelerated simulator,
step-exact validated), `x2cc_ledger.py`, `x2cc_decode.py`, `x2cc_symb.py` (certified symbolic
RLE executor), `x2cc_faith.py` (mechanized induction prover), `x2cc_gencheck.py`,
`x2cc_lowtrace.py`. SOUNDNESS: `[PROVEN]` = machine-checked symbolic derivation /
exhaustively certified closed form; `[OBSERVED]` = exact measurement, range stated. ZERO
false proofs. Not committed.*

## 0. Verdict

**NO certified decision — but the load-bearing claim of the whole prior investigation is
REFUTED: the E-met gap lengths are NOT counter-dependent.** The low part is not a free
binary counter; it is a rigid unary+parity ledger with an explicit affine update law, and
the per-generation E-met gap multiset is **eventually periodic with period 2**: exactly
`{18, 10}` (odd generations) / `{18, 10, 6}` (even generations), in FIXED parameter-free
contexts, for every mature generation — `[PROVEN for the whole low phase, all g, by
mechanized induction; OBSERVED exact g=3..11 for the full ledger]`. Route A's
"counter-dependent multisets" (`{4},{6,14},{},{6,14,22},{10,18},{6,10,18}`) are exactly
reproduced and explained: an immature transient (generations ≤ `big=253`) plus the parity
alternation. What remains open is NOT a counter-dependent invariant but the symbolic
composition of the doubling phase (§5). `[NOT decided; open core reshaped and shrunk]`

## 1. The register decoded `[OBSERVED exact, 0 mismatch, g=3..12, to 8·10¹¹ steps]`

Milestones = E@0 strictly left of every 1 (the x2p definition). Six milestones per
generation. Writing `U = 1 0^6`, K = g+8, the generation-start milestone is EXACTLY

```
M1(g) = [E] 0^22  U^(g-1)  T_g  1^(B_g)  0^2 1^(2^(K-1)-3) 0^2 … 0^2 1^5 0^2 1 0
  T_g  = 1 0^10            (g even)     |  1 0^4 (10)^6        (g odd)
  B_g  = 2^K - 3           (g even)     |  2^K - 9              (g odd)
```

and the other five milestone forms (M2..M6) are the templates in `x2cc_decode.py` —
**60 milestone configurations checked against the templates over g=3..12 (steps to
8·10¹¹), 0 mismatches** (`x2cc_ledger.py 8e11` + `x2cc_decode.py`).

**The update law: `g → g+1`.** One U-unit is appended every 2 generations; the tail
alternates with parity; the big block doubles `B → 2B+3` (with the odd-generation −4/−6
bookkeeping shown above). The register is a **unary ledger with a parity bit — an explicit,
fully-understood object**, NOT a (K)-type orbit and NOT a binary counter (the task's
"ruler sequence" hypothesis is refuted along with route A's counter-dependence: the carry
gaps are CONSTANTS, not functions of a counter value).

## 2. The derived carry-gap ledger — exact match `[OBSERVED exact g=3..11]`

Derived from the decoded law: per generation the E-met gaps of length ≥ 3 are
`{18, 10} ∪ {6 iff g even}`, all in fixed contexts (`1^5 0^18 U…`, `…1 0 1^5 0^10 U…`,
`1 0 1^6 0 1^5 0^6 1…`), all emitted in the LOW phase (M2→M4); the doubling phase emits
only lengths 1 and 2, the L=2s in five fixed right-tail contexts (`…0^2 1^13 0^2 1 0`,
`1^16 0^2 1^5…`; `x2cc` context census). Match against observation: **exact, every mature
generation g=3..11** (`x2cc_decode.py`: "GAP DERIVATION: EXACT MATCH"), and route A's
historical multisets are reproduced verbatim including the transient.

## 3. The faithfulness induction — what is PROVEN

Infrastructure: `x2cc_symb.py`, a symbolic RLE executor over parameterized configurations
(affine run counts, pattern runs, canonical folding), whose only primitives are (i) the raw
TM table and (ii) three closed-form cycle lemmas (R-cycle comb-repack, L-cycle unpack
even/odd, D-loop crossing), each certified against brute micro-stepping for all lengths ≤ 40
(`check_rules`) — the standard 2-transition-induction sweep lemmas of the campaign, now
machine-checked. Canonical folding is certified exact by randomized round-trips
(`check_fold`). The prover `x2cc_faith.py` does exhaustive case-splitting on every
undecidable comparison and **loop acceleration with accumulator generalization**: a detected
recurrence config(p) →* config(p−1) is re-proven symbolically (fresh accumulator parameter
J, body INV(p+1,J) →* INV(p,J+1)) before being used — a genuine mechanized induction.

**(a) The LOW PHASE M1(g) →* M6(g) is PROVEN for all g** (both parities; n = g−1 ≥ 1
symbolic; B symbolic with the correct mod-4 residue and B ≥ ~4000; smaller g and B are
covered by the exact concrete ledger, §1). The prover closes even-g in 3 branches and odd-g
in 3 branches, each ending at the M6 template exactly, with TOTAL event ledger
`{18, 10} + {2}×(g+1) + {6 iff g even}` — never 3. **This kills the "counter-dependent
even-gap invariant": every ≥3 gap E ever meets is one of three constants, proven for all
generations.** The executor HALTS on any gap-3 (halt gate built in), so these derivations
are non-halt proofs for the covered segments.

**(b) The doubling phase M6(g) →* M1(g+1): machine-checked EXACTLY for g = 2..6**
(`x2cc_gencheck.py`: five full generations derived in the certified executor, final config
= M1(g+1) template EXACT, ledger exact — g=6 is 1.3·10⁸ raw TM steps walked as 1.2·10⁶
certified ops), and its **interior engine is PROVEN symbolically**: the chew-cycle body
`(01)^k [D] 0^3 1^(2r+5) → (01)^(k+1) [D] 0^3 1^(2r+3)` for ALL k,r (6 steps, 0 events)
and the cascade-separator crossing `[D] 0^3 1^3 0^2 1^(2s+5) → (01)^(+2) 0^2 1 [D] 0^3
1^(2s+3)` for ALL k,s (15 steps, 0 events), each verified stub-generically. The block →
comb-with-frozen-0^2-markers phase of the doubling — the bulk of every generation — is
therefore lemma-level proven never to meet a gap ≥ 3.

**(c) NOT yet proven symbolically:** the doubling phase's remaining episodes — the entry
(register (1^5 0^2)^j → marked comb), the right-end tail/fresh-territory episodes (where
the +2 value growth and the L=2 events live), the repack phase (marked comb → next cascade),
and the register-rebuild endgame (where U^g and the parity tail are written — the register
increment itself). These are episodes of exactly the kind the prover closes, but their full
chain (an induction over the cascade block list) was not completed in this session. They are
covered only by (b)'s per-generation exact derivations and the raw evidence.

## 4. Cross-checks

- `x2cc_fast.py --validate 100000000`: the accelerated simulator is **step-exact vs the raw
  TM to 10⁸** (position, state, tape agree at every checkpoint and at 10⁸). Prior raw runs
  to 3·10⁸ (x2_scan). Halt-free with the validated simulator to **8·10¹¹ steps** (g=12).
- Milestone templates: 0 mismatches g=3..12. Gap multisets: exact match g=3..11 derived vs
  observed; route A multisets reproduced.
- Full-generation executor derivations g=2..6: final configs and ledgers exact.

## 5. Honest status and the reshaped open core

**No machine decided.** Non-halt = (low phase safe, ∀g) ∧ (doubling phase safe, ∀g). The
first conjunct is **PROVEN** (§3a — the part that carried the "counter-dependent" wall).
The second is proven at the engine level (§3b) and exactly machine-checked for g=2..6, but
its symbolic composition over the cascade (entry, tail, repack, rebuild episodes) is the
remaining open work — **a finite list of bounded/loop episodes of the same provable kind,
not a counter-dependent invariant**. The honest failure mode named in the task ("the update
law couples back to deep state") did NOT materialize: the register is rigid and explicit;
what stopped this session short of "CANDIDATE DECISION" is engineering volume (the T7
episode chain), not a conceptual wall. That is a real, sharp change to the frontier map:
the x2 open core is now "compose the remaining doubling-phase episodes in the certified
prover," with every ingredient already demonstrated.

## 6. Soundness ledger

- Register decode + update law: `[OBSERVED exact, 0 mismatch, g=3..12, 8·10¹¹ steps]`.
- Derived gap ledger = observed: `[OBSERVED exact g=3..11]`; low-phase ledger additionally
  `[PROVEN ∀g]` by (§3a).
- Cycle closed forms (R/L/D): `[PROVEN`, 2-transition induction; machine-certified ≤ 40`]`.
- Low phase M1→M6, both parities, all g (n≥1, B≥4·10³ right residue): `[PROVEN,
  mechanized: exhaustive splits + certified loop induction; events {18,10,2×(g+1),6-parity}]`.
- Doubling interior (chew body ∀k,r; separator crossing ∀k,s): `[PROVEN, stub-generic]`.
- Doubling full transports g=2..6: `[MACHINE-CHECKED exact per generation]`.
- Doubling symbolic composition (entry, tail, repack, rebuild, ∀g): **OPEN** — not used as
  a machine claim.
- Raw cross-check: `[PROVEN step-exact to 10⁸; halt-free to 8·10¹¹ validated-accelerated]`.

**No machine decided. No label upgraded.**
