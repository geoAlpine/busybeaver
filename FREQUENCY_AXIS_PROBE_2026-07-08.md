# Frequency-axis probe — the run-depth SEQUENCE after the uniform fixed-point theorem (2026-07-08)

*EVALUATE-BEFORE-EXECUTING reconnaissance. The uniform fixed-point theorem (`PAPER_MIRROR_LADDER.md` §1,
`O4_RUN_STRUCTURE_2026-07-07.md` §1) unconditionally caps the DEPTH axis (run ≤ log_q); every cryptid's open
protection is now the FREQUENCY of deep q-adic returns (§5). This probes whether any FRESH angle on that
frequency, exploiting the new uniform structure, is non-circular and not already closed. STRICT: honest recon,
not forcing a result. Numerics exact-bigint, interpreter `.venv` python, run-length==v_q(entry−x) VERIFIED as a
soundness guard (o4: 0/2711 mismatch; AH: 0/2005). NOT committed.*

---

## 0. What was instrumented `[OBSERVED, exact]`

The run-depth sequence (d_1,d_2,…) is, by the theorem, the run-length encoding of the orbit's constant-residue
(o4) / constant-parity (Antihydra) itinerary: d_i = v_q(entry_i − x_branch). Measured to 3·10^5 generations
(o4: 200 122 runs; AH: 150 117 runs):

| stat | o4 (×4/3, v₃) | Antihydra (×3/2, v₂) |
|---|---|---|
| mean depth | 1.4991 (≈ q/(q−1)=3/2) | 1.9984 (≈ 2) |
| P(depth=ℓ) vs geom q^{−(ℓ−1)} | matches to 3 dp through ℓ=9 | matches to 3 dp through ℓ=12 |
| autocorr lag 1,2,3,5,10 | −.003,.002,.002,.003,−.003 | .006,−.001,.001,.008,.004 |
| H(dₙ) vs H(dₙ\|last 3) | 1.3703 → 1.3676 (drop 0.2%) | 1.9372 → 1.9318 (drop 0.3%) |
| max run-depth | 12 (ρ=1); tracks log₃(#runs)=11.1 | 20; tracks log₂(#runs)=17.2 |

Max run-depth grows in lock-step with log_q(#runs) (o4: 6/9/9/12 at #runs=659/6.7k/20k/200k vs log₃=5.9/8.0/9.0/11.1)
— the extreme-value law of an i.i.d. geometric(1/q), on the nose.

---

## 1. Angle 1 — is the run-depth SEQUENCE structured (self-similar / substitutive / digit-linked)?

**Verdict: (K)-EQUIVALENT.** `[ASSESSED]` Two independent measurements make the sequence statistically
**indistinguishable from i.i.d. geometric**: (i) autocorrelation ≤ 0.008 at every tested lag — the "white-jump"
property banked for Antihydra (`EXCURSION_SYNTHESIS.md` §1, K-autocorr ≤ 0.012) now confirmed for o4 and extended
one register: (ii) the conditional entropy H(dₙ | last 3 depths) equals the marginal H(dₙ) to within 0.2–0.3% — so
the sequence is **not finite-order Markov and carries no substitutive/automatic structure detectable from a bounded
past**. A genuinely substitutive or q-automatic run-depth sequence would be a **sofic coding of the ×p/q orbit**,
which is exactly what the banked non-Pisot obstruction forbids (`NEW_MATH_PROGRAM.md` §8.7: the q-adic residue does
not descend; ⌊pc/q⌋ mod q^K has branching *exactly q* at every residue — a one-symbol-lookahead shift, no finite
window closes). The "digit-at-a-computable-position" hope resolves the same way: d_n = v_q(entry_n − x) *is* a
readout of the low-order base-q digits of the orbit's OWN value at position n (the moving-diagonal digit), and the
conditional-entropy test shows it is not recoverable from any bounded window of the itinerary — computing it is
running the orbit. **No unconditional statement beyond the first-moment tautology** (Σ run-lengths = n; the
per-residue refill-sum ≡ drain-count identity, `O4_GROWING_BUDGET_ASSESSMENT_2026-07-07.md` §1) survives. Not
re-running a logged NO-GO — this is the first direct sequence-level (autocorr + conditional-entropy) instrumentation;
it lands on the same wall.

## 2. Angle 2 — the coboundary run-bound threshold vs (K)

`O4_COBOUNDARY_LP_2026-07-08.md` §4: an eventual run bound v₃(Wₙ) ≤ 3 DECIDES o4 (sub-action margin −1/4);
R=4 critical; R≥5 carries the +1 obstruction (δ₋₁₄). Precise placement:

- **The real orbit exceeds the threshold**: max run-depth reaches 12 (ρ=1) by generation 84 788 (archimedean cap
  0.262·84788 ≈ 22 214 — the depth is ~1800× below its proven ceiling). So "run-depth ≤ 3 eventually" is
  empirically FALSE, i.e. the LP certificate **does not apply to the real orbit** — confirming the note's own
  reading that the threshold is a *localization, not a route*. `[OBSERVED]`
- **"run-depth unbounded" is NOT proven — it is (K)-equivalent.** `[ASSESSED]` Unboundedness ⟺ the itinerary
  contains arbitrarily long constant-residue blocks 1^L (equivalently v₃(Wₙ)≥L i.o. — arbitrarily deep 3-adic
  returns to the integer fixed point −14). Nothing proven forces this: a **Thue–Morse-type itinerary has runs
  bounded by 2**, satisfies every banked fact (run cap, telescope, all residue-finite data, the de Bruijn shift
  structure), and would DECIDE o4 through the very LP (bounded runs ⟹ feasible sub-action ⟹ ledger safe). Excluding
  it is precisely a deep-return-*frequency* statement = (K). The log₃(#runs) growth we measure is the
  **equidistribution prediction**, not a theorem — it is the (K)-heuristic itself. The only unconditional
  direction is the UPPER cap (proven); there is **no unconditional lower bound forcing even run-depth ≥ 4 i.o.**
  Where the threshold sits relative to (K): the deciding hypothesis ("run ≤ 3 eventually") sits *below* (K) as a
  strictly stronger-than-needed structural statement, and its negation-with-frequency (the actual open content)
  sits *on* (K).

## 3. Angle 3 — cross-machine leverage from the easier margins

**Verdict: no unconditional foothold transfers; each orbit's frequency is independently (K)-hard.**
`[ASSESSED]` The frequency axis is the same *object* across the ladder, but the objects live on **different,
arithmetically unrelated orbits** (o4 on the ×4/3 3-adic solenoid, Antihydra on the ×3/2 2-adic solenoid; no map
between them — the mirror is a (p,q)-swap, not a morphism, `O4_RUN_STRUCTURE` §3). o4's easier margin (fatal needs
prefix ρ=1-density ≥ 4/5 with slack vs Antihydra's zero-margin ≥ 1/3) is a **weaker required bound of the same
species**, blocked by the identical annealed→quenched wall (`O4_GROWING_BUDGET_ASSESSMENT` §2, §6). The +3 drift
already bought its one flip (single-run fatality excluded, banked `[PROVEN]`); it buys nothing on frequency because
the no-gos are **threshold-uniform** — δ₋₁₄ realizes drain-density 1 and the itinerary bijection realizes every
intermediate density at every threshold < 1 (`O4_LEDGER_ANALYSIS` §2). The sea machines' sparse resetting draws and
Space Needle's summable lean are convergent-class (BC-I) but the needed unconditional surrogate P[deep return]≲q^{−ℓ}
is the same open per-orbit return-frequency bound. The measured statistical identity of o4's and Antihydra's
run-depth laws (both exactly geometric, both white, both zero conditional structure) is the *evidence* that they are
one problem in |family| coordinates — and that there is no easier coordinate to transfer from.

## 4. Route-viability verdict

| angle | verdict | why |
|---|---|---|
| 1 run-depth SEQUENCE structure | **(K)-equivalent** | white (autocorr ≤ .008) + zero conditional structure (H-drop ≤ 0.3%); any substitutive/automatic law = sofic coding = forbidden by non-Pisot |
| 2 coboundary run-bound threshold | **closed as localization** (LP §4) + unboundedness **(K)-equivalent** | orbit exceeds R=3 (max 12); no unconditional lower bound; Thue–Morse-type bounded-run itinerary not excluded |
| 3 cross-machine leverage | **(K)-equivalent, independently per orbit** | threshold-uniform no-gos; unrelated solenoids; margins weaken the ask, not the wall |

## 5. The sharpest new statement of why the frequency axis is (K) in every coordinate

> The uniform theorem makes the run-depth sequence an **exact function of the moving-diagonal q-adic digit of the
> ×(p/q) orbit**, and that sequence is measured to be **white and conditionally structureless** — statistically an
> i.i.d. geometric(1/q). The frequency axis therefore has *no* exploitable self-similarity, finite-memory, or
> cross-machine reduction below the first-moment tautology: possessing any such structure is equivalent to a sofic
> coding of a non-Pisot ×(p/q) expansion, which is exactly the ingredient the banked obstruction (`NEW_MATH_PROGRAM`
> §8.7) proves absent. Every deciding hypothesis (bounded runs; density < threshold; a return-frequency law) reads
> the specific seed's arithmetic and is (K)/normality-on-base-p/q in that coordinate. The margin ladder orders the
> *strength* of the ask; it does not open a coordinate where the ask is easier than (K).

No machine decided. No label upgraded.
