# (K)-wall proof handles — the full-corpus dig (2026-07-22)

**Mission:** the owner asked for clues toward the new number theory the BB(6) core needs. This is a
three-track sweep of the whole corpus + git history (build-attempt post-mortems / banked constructive
structures / parked-vs-refuted thread audit), synthesized and **source-re-verified**: every
load-bearing claim below was re-read verbatim in its source document today, not taken from summaries.
Labels strict. **No machine is decided; no label is upgraded by this document.** Margins are
evidence, not proof.

---

## 0. The unifying shape (what the missing tool IS, seen from every angle)

Every door below is the same door viewed from a different side: **an effective quenched cancellation
bound for ONE specified orbit at ONE non-archimedean place, with large slack.** The annealed version
is proven everywhere it was tried; the specified-orbit version is (K). The corpus's sharpest
compression (`MINIMAL_CORE_2ADIC.md`): everything — 3-adic place, carry, solenoid, both Mahler
diagonals — is a PROVEN deterministic factor of the single 2-adic depth process; (K) ⟺
`liminf (1/N) Σ D_j ≥ 3/2` for the one orbit. The missing mathematics is not exotic in *statement* —
only in *kind*: no existing framework proves quenched facts about specified orbits of rank-1 amenable
non-sofic actions.

---

## 1. The doors (open, NOT refuted) — ranked

### D1. Theorem E — the δ→margin map. THE sharpest lever. `[PROVEN reduction]`
`THEORY.md` §B5′ (re-verified verbatim):

> If there exist `δ>0, C` with `|Σ_{i<N, c_i odd} ψ(c_i)| ≤ C·N^{1−δ}` for every nontrivial
> Dirichlet character ψ of conductor `≤ N^δ`, then Antihydra never halts.

**ANY power saving suffices, at LOW moduli only.** The hypothesis is the a.e.→specified gap of
Tao 2019 (Forum Math Pi) — open, and NOT proven impossible: the A5 no-go only shows it cannot come
from *finite-order* methods (a scope restriction). This is the correct external-facing formulation:
it is exactly the kind of inequality analytic number theorists prove.

### D2. The odd 2nd moment `M₂ᵒᵈᵈ` — the banked conditional theorem with a 100× margin
`ODD_ADDITIVE_ENERGY.md` (re-verified): Cauchy–Schwarz gives
`avg jump ≤ 1 + 2 Σ_k 2^{−(k+1)/2} M₂ᵒᵈᵈ(k)^{1/2}`, so a bound `M₂ᵒᵈᵈ(k) = O(2^k/J)` (odd-restricted
collision counting: each collision class mod 2^{k−1} splits evenly by the next bit) ⇒ non-halt.
Measured envelope **0.03–0.07 vs the sufficient 0.25** — the only banked conditional theorem whose
hypothesis is a *moment* (collision count), not equidistribution per se.
**Unpursued attach-point** (`RESEARCH_LOG.md` 06-24): the collision differences are S-unit-*like* —
p-adic Baker / linear forms in logs on `v₂(c'_i − c'_j)`. **Caveat carried:** the o7 Baker attempt
found its orbit values are NOT S-units ("no equation to apply"); the same may kill this. Untested
either way.

### D3. o4 first — the weakest open instance on the whole frontier (three stacked slacks)
The strategic clue, not just a target. o4's version of (K) is strictly milder than Antihydra's on
three independently PROVEN axes:
1. **Analytic slack:** decide o4 ⟺ `Re(S₁(n)) < 0.7·n` for seed-43 (`O4_EXPSUM`, re-verified:
   `freq{3|Wₙ} = 1/3 + (2/3)·Re(S₁)/N`, fatal ⟺ `≥ 0.7`). 70% of trivial; observed 0.00079 — 890×
   inside. The δ₋₁₄ counterexample blocks only the *all-orbits* version; **for seed-43 nothing is
   proven impossible.**
2. **Structural slack:** the subcritical certificate `p+1 ≤ q^{β+1}` (`5 ≤ 81`, Lean
   `o4_has_certificate`) — run-cap slope/budget slope = 0.087 vs Antihydra's **1.17 > 1**. The one
   PROVEN inequality on the frontier that flips a machine from the critical to the subcritical
   register; single-run fatality is dead, only a multi-run density-burst conspiracy survives.
3. **Measure-class slack:** annealed ruin is SUMMABLE (`Σ η^{3n} ≈ 3×10⁻¹⁰`, η=0.3349) vs
   Antihydra's divergent series — the required hypothesis drops from a divergent-BC/(K)-grade bound
   to a convergent-BC-I-grade one. (Careful — the source itself says Route 1 is "still closed
   (sharpened, not opened)": the gain is a weaker *required hypothesis*, still annealed-level; it is
   not a proof mechanism yet.)

Any new tool should be built and tested against o4's `freq ≤ 4/5−ε` FIRST; Antihydra's zero-margin
version only after.

### D4. The two "closest attach-points" — named by the program itself, never attempted
`SESSION_2026-07-04_INDEX.md` §3 / `EFFEQ_PARTIALS_LEDGER` §D: the missing theorem has two proven
corners — Stewart 1980 (single-orbit + effective, but count/log-depth) and Fan–Fan–Ye
(distributional + linear-depth, but a.e.). The BRIDGE between them is proven to reduce to (K)
(`BLOCK_BRIDGE`), but the two *individual upgrades* were parked untried:
(a) strengthen Stewart's method (Baker / p-adic Yu) toward a distributional or linear-depth bound;
(b) an arithmetic inclusion/exclusion placing 3/2 outside the FFY exceptional set.
Both are genuinely external mathematics — which is why they were parked, and why they belong in the
outreach conversation (D7).

### D5. AIU at the measure level — the conceded open crossing
`NEWMATH_ROADMAP` §3a: the pointwise sliding-block lock is PROVEN (the 3-adic word is a causal
factor of the depth process), but "pointwise lock ≠ measure-level invariance" — upgrading the lock
to `(×2)_*μ = μ` is the explicitly conceded open content, not proven impossible. With ENT it feeds
the PROVEN Rudolph–Johnson finisher. The named home theory: a low-entropy/neutral-direction
extension of Einsiedler–Lindenstrauss leafwise methods — the literature's empty spot (rank-2
rigidity exists, rank-1 non-rigidity exists, no bridge).

### D6. The magnitude invariant — the right SHAPE per the design spec
`O4_EQUIVALENTS_SEARCH` N3: `Φ_n = S_n + 5·v₃(W_n)` is bounded on the real orbit (max = 5) and
jumps ~5L on a depth-L return; boundedness ⟺ (K). It still *reduces* to (K) — but it is the best
existing example of an object satisfying the design spec's hardest requirement (magnitude-reading,
excursion-level). A new invariant of this shape with a provable a-priori bound is the internal
build target.

### D7. External: AEV/Eliahou collaboration `[GATED on explicit go-ahead]`
The non-transferability of AEV's own proven fragments is now precisely understood (re-verified):
Thm 1.7 is an equivalence (restates (K), zero leverage); Thm 1.5 assumes normality and its
"infinitely often" mechanism is strictly weaker than the banked `#even ≥ 0.89 log n`. So fragment
reuse is dead; **collaboration on the conjecture itself is the path** — and D1's Theorem E is the
right artifact to lead with (a proven "any δ>0 at low moduli suffices" reduction is a gift to an
analytic audience).

### D8. Cheap kill-tests (falsifiable this week, internal, no gates)
- **o4 run-cap R≤3:** if ρ=1 runs never exceed 3, o4 is DECIDED (`O4_CERTIFIED_FREQUENCY` §4:
  max-mean crosses 4/5 at R=4). Flagged "expected false" but unproven either way; longest observed
  run = 2. Extend the orbit simulation by orders of magnitude: one run of 4 kills the door
  cleanly; continued absence sharpens a remarkable observation into a target.
- **M₂ᵒᵈᵈ envelope depth:** push the measured envelope (currently 0.03–0.07 at the random rate) to
  larger J and larger k — a deviation would be the first internal anomaly in the corpus; continued
  compliance sharpens D2's constant.

### D9. `[PROPOSED — untested, this document's only new idea]` Lacunary structure of the fatal cone
The surviving adversary class is cap-legal E[K²]=∞ (`U0_EXCLUSION`): deep excursions can only be
scheduled where the linearly-growing budget first permits — depth-K events are confined to indices
≳ K/log(p/q), and with the first-moment budget `ΣK ≤ N + O(1)` a divergent second moment forces the
deep-return TIME SET to be very sparse (near-lacunary). Question nothing in the corpus appears to
have asked: restrict the D1/D2 character sums to the *deep-return time set* — for lacunary/Sidon-type
index sets, harmonic analysis has genuinely *unconditional* cancellation tools (Salem–Zygmund class).
Sniff-test against the no-go fence: orbit-specific (reads the budget) ✓, excursion-level ✓,
magnitude-reading (budget = archimedean size) ✓, a-priori (run-cap is proven) ✓, non-spectral ✓.
Honest risks: (i) the adelic-budget no-go proved budget-counting is clustering-INDIFFERENT — this
proposal must read the *time-set geometry*, not the budget sum, to differ; (ii) the excursion
supermartingale no-go showed drift-indistinguishability — but that was for potentials of the depth
process, not for restricted character sums over the return-time set. May well reduce to (K) like
everything else; it is cheap to probe numerically first (measure the return-time set's lacunarity
constant and the restricted sums' cancellation rate on the real orbit).

---

## 2. The traps — closed doors that look open (do NOT re-open)

Verified-refuted or proven-reducing; each has a named reason in its document:
Category B thin-set decisions (o7/SN/o17 — attacked 07-10, honest negatives, Diophantine-hard);
intra-term adelic coupling (tautology); Siegel (p,q)-adic WTT (annealed at the seam); non-Pisot
diffraction (orthogonal coordinate); the entire 2026-07-04 arc (all six notes end in closure `(c)`,
none in session-exhaustion); spectral/op-norm cross-scale routes (coisometry, λ_op ≡ 0); ANY
certificate on the frequency axis (B(3,k) max-mean ≡ 1); reload-map carry-coupling at the tail
(unit-refresh decouples); cross-machine transfer (per-seed even for the identical engine);
single-map rigidity (needs 2 m.i. maps; the exceptional set is a fat dim-0.582 fractal); effective
p-adic equidistribution (governs backward/height→0 orbits; ours is forward/height→∞); automatic /
nilsequence structure (kernels FREE, U²/U³-uniform — maximally structureless); Heuberger–Krenn
regular-sequence asymptotics (gated on automaticity, which is refuted); internal sub-(K) rungs
(none exist between `#even ≥ 0.89 log n` and the kernel).

---

## 3. The calibration lesson (from the x2 closure, this week)

The x2 crux closed on 2026-07-21 after its own file had *twice* mis-predicted what the crux WAS —
while every *measured* claim held. Score across that ledger: *"what the object is" narratives 0/2;
measured claims 5/5.* Applied here, cautiously: the (K) no-gos are measured/proven and STAND — but
the 7-constraint *design spec* of the missing tool is partly narrative, and the x2 precedent is
that the closing move came from a banked lemma nobody had recognized as the induction step, found
by measurement. The (K)-analogues of "banked lemmas that might already be the step" are exactly
D2's moment inequality, D6's bounded invariant, and the sliding-block lock. **Measure first,
narrate after** — hence D8's kill-tests before any theory-building.

## 4. Recommended sequence

1. **D8 kill-tests** (internal, days): extend o4 runs; deepen the M₂ᵒᵈᵈ envelope. Cheap, decisive
   either way.
2. **D9 probe** (internal, days): measure the deep-return time-set geometry + restricted-sum
   cancellation on the real orbits (Antihydra seed 8/27; o4 seed 43). If it reduces, document the
   reduction and add it to the trap list; if not, it is the first new mechanism since 07-10.
3. **D3 discipline**: any tool candidate gets tested against o4's slack-2.4 target first.
4. **D7 decision** (owner): the AEV letter with Theorem E (D1) + the D4 attach-points as the
   technical payload. This remains the corpus's own top-ranked path, and the only one that can
   summon the missing theory. Gated on your explicit go-ahead — nothing sent without it.

**Bottom line:** the corpus contains no unexamined shortcut — but it does contain three proven
conditional theorems with 100–1000× measured margins (D1, D2, D3-analytic), one strategic ordering
(D3: o4's three stacked slacks), two never-attempted external attach-points (D4), one conceded open
crossing (D5), and one untested new probe direction (D9). That is what "clues" honestly look like on
this frontier.
