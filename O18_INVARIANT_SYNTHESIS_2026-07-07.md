# o18 push-margin invariant synthesis — the search DECIDES ITSELF NEGATIVELY: fatal cells are EXACTLY reachable from the exit cone under adversarial residues (97-pass witness, every edge concretely confirmed), so NO residue-oblivious invariant of ANY class exists; the o18 decision is irreducibly arithmetic (2026-07-07)

*Executes the invariant-synthesis program on the `O18_MULTIDEFECT_2026-07-07.md` §6.1 blocker (the
push-margin law). Verdict: **invariant-class exclusion, universal** — not one class at a time but all
of them at once: the fatal region is genuinely reachable from the exit cone in the exact word dynamics
once the residue itinerary is adversarial. The conjectured margin mechanism ("a fresh 2 carries
2(v−2)/3 escort") is real but NOT protective: escort is drainable at will (1 unit per r=2 POP), so
protection can only come from the actual 3-adic itinerary of m. This is genuine structural evidence
FOR the community's "probviously halting" expectation, and it aligns the repo's picture with the
community's known fatal residue sequences (length ~110) for the same table. No machine decided.*

## 0. What was attempted (the task) and what happened
Sought: an inductive potential/invariant Φ over the multi-defect word grammar (`o18_md_rules.py`
transducer T) with exit-cone ⊆ Inv, Inv closed under T for all residues, fatal ∩ Inv = ∅ — searched
as (a) linear over margin features, (b) piecewise/lexicographic, (c) regular-language. The search
program TERMINATED at stage 0': the closure precondition (adversarial safety of the exact system)
is FALSE — there is an explicit finite path from the exit cone to a halting cell. All three synthesis
classes are excluded by the one witness; no LP/DFA search can succeed, and none is needed to see why.

## 1. Failure forensics on the abstract BFS `[PROVEN]` (`o18_inv_forensics.py`)
The adversarial-residue BFS of `o18_md_closure.py` (66 fatal/unknown abstract cells) was replayed
exactly. All **10 abstract HALT paths are GLUE-JUMP artifacts**: each passes through ≥1 of 328
`concretize∘abstract ≠ id` points where the abstraction snaps a true value DOWN to a class
representative — unit-trains of true length 10 → 7, blocks 17→14, 18→15, 20→14, 21→15, 23→14 —
always downward, always by a multiple of 3 (i.e. exactly stolen push-margin), and the TRUE
continuation from every jump point under the same residues LANDs or stays alive (0 real halts among
all 328 jump continuations). **The feature the abstraction discards is the exact magnitude of (a)
unit-trains ≥ 10 and (b) block values ≥ 16** — precisely the escort ledger. So the ORIGINAL closure
failure was spurious… but refining the abstraction would not have helped (§3): deeper exact paths
are genuinely fatal.

## 2. Ground-truth feature discovery: the exact adversarial attractor `[PROVEN on bounded universe]`
(`o18_inv_attractor.py`, `o18_inv_conemap.py`) On an 800,712-word bounded universe (len ≤ 5, b ≤ 9,
s ≤ 3), the least fixpoint "adversary can force HALT in-universe" contains **65,669 words**; every
one contains a block of value exactly 2 (0 exceptions), and the 55 without a *tail* 2 all have
first non-unit block `(3,2)` (0 exceptions, checked), which converts to a tail-2 in one r=1 pass. The **exit cone and the whole
D-family are 0/36 BAD**. The BAD boundary is NOT a pattern language boundary: candidate patterns P0
("two unit-separated 2s") … P3 (generalized precursor) each miss 10k–58k BAD words — the danger
predicate is inherently non-local (separator parity, escort counts, merge potentials 2j+6+v with
adversary-drainable j all enter). This is the graded refutation of pattern-invariant hopes; the
witness (§3) is the absolute one.

## 3. THE WITNESS: fatal cells are exactly reachable from the exit cone `[PROVEN]`
(`o18_inv_reach.py`, `o18_inv_witness_verify.py`) Exact forward closure of the exit cone
(`[2t+2,6]`, `[4,1,1,1]`) under T with free residue choice, exact words, generous caps
(len ≤ 14, b ≤ 60, s ≤ 6):
- reachable exact words: 3,000,000 (budget-capped; the graph is NARROW: ~100–200 new words per
  depth level — the adversarial reachable set is highly constrained, which is why beam/depth-16
  searches missed the fatality);
- **491 reachable HALT cells** (and 517 reachable Unknown cells — the unpinned deep-R1 fractal is
  adversarially reachable too, so it can no longer be dismissed as decoration);
- **minimal fatal schedule: 97 passes** (depth-BFS; consistent with the depth-16 exhaustive
  all-LAND result — the conspiracy simply lives deeper), ending in the genuine fatal family
  `1^{≤1} (1,2)(1,2) 1^*`.
- waiting-2s (tail blocks of exact value 2 — the necessary fatal ingredient) form adversarially in
  a handful of passes (428,383 of the 3M reached words carry one) via the motif: PUSH v≡2 down to a front-2, recycle the front-2 by
  `R1 v≥3: 1^j(1,2) 1^p (1,5) Z → (1,2j+6) 1^{p+2} (1,2) Z` (pushtail births the tail-2), and the
  merge rules `r=1, s≥2: → [2j+6(+v)]` manufacture the ≡2 (mod 3) escort block in front of it.

Verification layers (all in `o18_inv_witness_verify.py` output) — **STATUS: ALL COMPLETE**:
- L2 (PASS): every edge re-verified by independent T application.
- **L3 (PASS, complete): every edge of the 97-pass path confirmed by FRESH CONCRETE SIMULATION at
  5 magnitudes of m (right residue class, m up to ~1000): word rewrite AND constant c exact at all
  485 edge probes; the final halting cell HALTs concretely at 5 values of m ≡ 1. The witness does
  NOT rest on the grid extrapolation.** Two probes at edge 95 (the last POP, m=101/1001) carried a
  run-wide `unsafe=1` with EXACT word/constant agreement: per-pass isolation (maxF=2) shows the
  edge clean (unsafe=0); the flag came from the probe's free-running continuation itself halting at
  m′=274/2674 ≡ 1 — the documented multi-pass attribution effect (O18_MULTIDEFECT §7), and doubly
  confirmatory: those two runs executed the final POP **and the fatal halt back-to-back in one
  concrete run**. At the three magnitudes with m′ ≡ 0,2: no halt, no flag — exactly as the fatal
  law predicts. (Verifier now isolates this case; see `o18_inv_witness_verify.py` L3 note.)
- L4 (PASS): an explicit m₀ = 17947798775329759924367280608390008110328418350 (47 digits,
  constructed 3-adically, class mod 3⁹⁷) realizes the whole 97-pass itinerary in exact bigint
  arithmetic (integrality + residues all PASS); at the fatal cell m ≡ 1 (mod 3) as the fatal law
  requires (m_fatal is an 88-digit integer).

**Impossibility meta-theorem `[PROVEN]`.** Let I be ANY set of words with (i) exit-cone ⊆ I,
(ii) for every w ∈ I and every residue r realized by some m (all are), the pass successor is in I
and is not HALT. By induction along the witness path, I must contain its final word, whose r=1
pass HALTs (confirmed concretely at 5 magnitudes) — contradiction. Since (i)+(ii) is exactly what
"inductive invariant over the word grammar" means, **no linear, piecewise, lexicographic, regular,
or ANY other residue-oblivious invariant exists.** The three requested synthesis classes are
excluded with one witness each = the same witness; the "exact witness rule that breaks them" is the
schedule of §3 (POP drains the escort for free; the R1 v≥3 recycle births tail-2s; the s≥2 merges
birth ≡2 escorts). The conjectured push-margin law is true as a bookkeeping identity but has no
protective force: margins drain 1/POP with no compensating obligation on the itinerary.

**The requested LP, run for the record** (`o18_inv_lp.py`): linear potential over 9 margin features
(lead units, total units, block count, #exact-2s, #tail-2s, #≡2-mod-3 blocks, escort-to-first-≡2,
total value, separator excess), monotone sublevel form, constrained on the witness path +
exit/fatal separation: **INFEASIBLE (HiGHS), with an 8-transition irreducible core** = the tail-2
birth (pass 55), the ≡2-escort births (79, 82, 87), the front-8/5 pushes onto the waiting 2
(48, 89, 90), and the endgame POP (95). Piecewise/lexicographic and regular classes need no
separate search: the impossibility meta-theorem covers every sublevel/set-shaped invariant at once.

## 4. Quantification — what the failure shares, and the null model
(`o18_inv_anatomy.py`, `o18_inv_montecarlo.py`, `o18_inv_nullmodel_dp.py`)
- The minimal fatal schedule's anatomy (`o18_inv_anatomy.py`; rule census PUSH 33, POP 51,
  R1 6, MERGE-1 7) is a five-phase conspiracy: (I) passes 0–12: push 8→5→2 and recycle the
  front-2 off the `(1,6)` tail; (II) 13–42: unit-farming loops — `PUSH v=3` manufactures `(2,·)`
  separator blocks, `MERGE-1 s=2` births value-tuned `2j+6+v` blocks (9, 9, 9, 11); (III) pass 43:
  the double-≡2 precursor `(1,8)(1,8)` (exactly `R1(j≡0 mod 3, 1^p)` → `(1,2j+2)(1,2p+6)`);
  (IV) pass 55–56: the tail-2 birth `(1,2) 1² (1,5) →[r=1]→ (1,6) 1⁴ (1,2)` (R1-v≥3 recycle,
  pushtail(5) = the waiting 2); (V) 88–96: manufacture `(1,11)` (≡2) in front of the waiting 2,
  push 11→8→5→2, drain 5 POPs to `1¹(1,2)(1,2)`, r=1 HALTs. The 97-digit residue string
  (`11222111222211122211112222211112222…1222221`, anatomy output) contains **no 0 at all**: the
  conspiracy lives entirely in r ∈ {1,2}; every r≡0 pass (delegation/absorb) derails it — which
  is why random itineraries LAND in a median of 2 passes. **Every ingredient the §6.1 margin law hoped to forbid is manufacturable:
  escorts drain for free (51 POPs), ≡2 escort blocks are born on demand (MERGE-1), and the
  waiting-2 is born from a 5-block behind a front-2 (R1 recycle).**
- Uniform-random residues (the community's null model, measured on the word grammar): 200,000
  random excursions from the exit cone — **0 halts**; excursion length quartiles 1/2/4, max 33.
  The fatality needs a ~97-pass conspiracy; random walks land almost immediately.
- Exact DP bounds on the per-excursion halt probability (value iteration on the 3M-state exact
  graph; escapes censored both ways): p_halt ∈ [2.0·10⁻³⁸, 2.3·10⁻³] across cone starts
  (for `[8,6]` specifically [4.3·10⁻³⁴, 6.0·10⁻⁶]; lower bounds count in-universe fatal paths
  only, upper bounds assume every universe escape is fatal). Null-model time-to-halt:
  ~10^2.6–10^37.7 generations — halting a.s., but at timescales consistent with the community's
  iterated-exponential halt estimates; 122,015 clean generations so far are unremarkable under
  any p < 10⁻⁶.
- The true orbit (122,015 clean generations to m ≈ 10^85194) never even forms a waiting-2: its
  itinerary is doing ALL the protective work.

## 5. What this means for o18/o15 `[honest statement]`
1. **The finite-search door is closed.** The one place in the cryptid family where a decision looked
   reachable by finite ranking-function synthesis is now PROVEN to have no such decision: any proof
   of o18-orbit safety must be a one-sided ARITHMETIC condition along the orbit's own 3-adic
   itinerary (o4-ledger-shaped), i.e. exactly the (K)-type object the impossibility meta-theorems
   already frame. o18 fully joins the boundary-graph unification picture: finite word grammar,
   counter(m)-dependent branching, fatal set reachable in the graph-adversarial closure.
2. **Evidence FOR "probviously halting":** the community's expectation needed the fatal region to be
   dynamically accessible; it is (491 cells, schedule of length 97 from the cone). Our witness is
   the o18-coordinates confirmation of the community's known fatal residue sequences (length ~110,
   o15 wiki; the lengths are consistent — different anchor, same table). What keeps the orbit alive
   is not structure but the specific residue stream — and the null model says nothing protects it
   in the long run. Via the o15=o18 identity (one table, two seeds), the same witness speaks for the
   o15 orbit's separate seed: both seeds face the same irreducibly arithmetic decision, each on its
   own itinerary; neither can be saved by word structure.
3. **Against immediate halt:** the measured null-model halt rate per excursion is astronomically
   small (lower bounds 10⁻³⁸–10⁻³⁴ from in-universe paths; §4); halting, if it comes, comes at
   iterated-exponential timescales — consistent with the community's halt estimates for this
   table and far beyond simulation.
4. The 517 reachable Unknown cells (deep R1 fractal `h_{p≥4}`, j=0 nestings) must be pinned before
   any FUTURE conditional-safety claim: they are now known to be adversarially reachable.

## 5b. Class-exclusion summary + reconciliation with the annealed track
| invariant class | verdict | breaking witness |
|---|---|---|
| linear potential (9 margin features, sublevel) | EXCLUDED (LP infeasible, HiGHS) | 8-transition core: tail-2 birth (pass 55), ≡2-escort births (79/82/87), pushes onto waiting-2 (48/89/90), endgame POP (95) |
| piecewise / lexicographic ranking | EXCLUDED | same 97-pass witness (meta-theorem; any sublevel-set shape is a word-set) |
| regular-language (DFA over word alphabet) | EXCLUDED | same witness (a T-closed regular set containing the cone must contain the path) |
| ANY residue-oblivious word-set | EXCLUDED `[PROVEN]` | the 97-pass witness, every edge concrete |
| itinerary-coupled predicate on (m mod 3^k, w) | **OPEN — the only surviving shape** | not excluded; to dodge this witness alone needs k ~ 97, and the 491 halting cells + variants push k up without bound in the residue-oblivious limit |

**Surviving candidates: NONE in any searched class; exact surviving domain:** predicates that
constrain the orbit's own 3-adic itinerary (o4-ledger-shaped). Nothing weaker can work.

**Reconciliation with `O18_ANNEALED_STANDOFF_2026-07-07.md` (parallel track):** the annealed
margin-aware model predicted exactly this outcome — margins do not accumulate across generations
(clean generations re-seed at `((1,6))`-type words), two-2 words are itinerary-reachable
(their replay-verified witnesses at depth 51–56, always units-gapped), and fatal (gap-0) entrances
have positive annealed measure. Our synthesis run independently CONFIRMS the annealed analysis
from the exact side: no all-itinerary invariant exists in any sound class, the fatal entrances are
realizable (gap-0 requires the deeper 97-pass schedule vs their units-gapped depth 51–56 — the two
depth scales are consistent: closing the last units-gap is exactly the expensive endgame phase V),
and no candidate invariant survived that could contradict the annealed track. The two tracks now
agree on one picture: **the o18/o15 standoff is measure (annealed halting) vs the actual
itinerary's conspiracy-avoidance, with no structural safety net.**

## 6. Soundness ledger `[discipline]`
- The witness does not rest on abstraction: every pass is a concretely simulated machine pass
  (5 magnitudes/edge); the halting cell is concretely fatal (5 magnitudes, m ≡ 1).
- NOT claimed: that the o18 (or o15) ORBIT halts, or reaches the witness path — the orbit's actual
  itinerary at its exit epochs is unknown at magnitude; simulation to 200k tower-steps shows it
  dodging every dangerous motif. NOT claimed: that no invariant of any kind exists — an
  itinerary-COUPLED invariant (predicate on (m mod 3^k, w)) remains possible and is now the ONLY
  possible proof shape for non-halt.
- The single-m₀ full-chain statement (L4) additionally rests on the grid law
  [(m mod 3, w)-determinism, PROVEN on grid] at magnitude ~3⁹⁷; the impossibility meta-theorem does
  NOT need it.
- Abstract-BFS forensics: the old closure's HALT cells were spurious (all GLUE-JUMP), yet its
  non-closure verdict was RIGHT — restated with the real witness. ~40th self-caught correction
  class: "the right conclusion for the wrong reason" is still a bug.
- L3's two `unsafe=1` flags were investigated to root cause before acceptance (multi-pass
  attribution, per-pass isolation clean, m′-residue pattern exactly matching the fatal law) — the
  flags strengthen rather than weaken the witness; verifier updated to isolate the case.
- o18/o15 stay `[OPEN]`. **No machine decided. No label upgraded.**

## Reproduce (interpreter `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`)
`o18_inv_forensics.py` (abstract-HALT replay/classification) · `o18_inv_attractor.py` +
`o18_inv_conemap.py` (exact adversarial BAD attractor + exit-cone status + pattern mining) ·
`o18_inv_reach.py` (exact adversarial reachable set; 491 halts) · `o18_inv_witness_verify.py`
(minimal witness + L2/L3/L4 verification) · `o18_inv_anatomy.py` (schedule anatomy) ·
`o18_inv_montecarlo.py`, `o18_inv_nullmodel_dp.py` (null model) · `o18_inv_lp.py` (the LP record).
Basis: `O18_MULTIDEFECT_2026-07-07.md`, `O15_O18_IDENTITY_2026-07-07.md`.

**No machine decided. No label upgraded.**
