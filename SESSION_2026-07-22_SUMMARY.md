# Session 2026-07-22 — clearing everything outside the BB(6) core

Brief: *"follow the roadmap and clear everything except BB(6) proper."* Gated items
(X1–X3 external outreach / D7 AEV letter) were **excluded** — they require explicit owner
go-ahead and nothing was sent. Below is what ran, what closed, and what each result is worth.

**Headline: two of my own claims from earlier the same day were refuted by measurement, and one
long-standing internal contradiction surfaced.** No machine is decided. No label is upgraded.

---

## 1. Roadmap sync to the `RegenLaw ∀k` closure ✅

`ROADMAP_2026-07-19.md` still described the crux as OPEN/off-orbit in five places, and `STATUS.md`
was two weeks stale. Synced with supersession banners (repo convention: never delete history).
Closure independently re-verified first: `regenLaw_closed : ∀ k, 4 ≤ k → RegenLaw k`,
`[propext, Quot.sound]`, `lake build X2` green, no live `sorry`, definition untouched since its
introducing commit `f688e47`.

Two corrections found while verifying, **both against my own first draft**:
- The interior fold **is load-bearing** in the closure — `regenLaw_of_trailLaw` calls
  `interiorFold_lower_expl (k−6)`. I had drafted that the closure bypassed it.
- `regenLaw_7` is **not** a base of the induction (bases are `regenLaw_4/5/6`); it is only the
  independent cross-check. This *vindicated* the 07-19 self-critique line I had first scored wrong.

## 2. BB(6) complete-proof roadmap ✅ (`BB6_COMPLETE_ROADMAP_2026-07-22.md`)

The 11-axiom discharge map, tiered **E** (internal engineering, actionable) / **C** (community
scale, gated) / **M** (the open-math wall, fenced by proven no-gos) / **X** (external, gated).
Measured fidelity finding: **only 1 of 18 conjuncts (`o4`) is machine-literal**; `O3.lean` covers
only the `a ≡ 0 (mod 3)` class and the Completion conjunct is the pinned `Normality43` form.

## 3. (K)-wall handle dig ✅ (`BB6_PROOF_HANDLES_2026-07-22.md`)

Three-track sweep (build post-mortems / banked constructive structures / parked-vs-refuted git
audit). Nine doors ranked, fourteen traps listed. Sharpest: **D1 Theorem E** — any `δ>0` low-moduli
power saving ⇒ Antihydra non-halt, a PROVEN reduction; **D2** the `M₂ᵒᵈᵈ` moment bound; **D3** the
o4-first strategy (three independently proven stacked slacks).

## 4. T7 recon — **the `⊕` IS wired; I was wrong** ✅ (`T7_RECON_2026-07-22.md`)

I had recorded that `h_doub = RegenLaw ∀k ⊕ (doubling assembly)` had an unwired `⊕`, inferring it
from the source-level fact that §5g/§5h reference no `regenIn`/`cascadeReg`/`RegenLaw`/`exitSteps`.
**The measurement was right; the inference was wrong.** The Lean development does not mention those
objects — the real orbit is full of them.

*Instrument check earned its keep:* the first run failed all three recorded anchors and caught a bug
in **my own** transition table (state `C` read-1 is `1LE`, move LEFT). After the fix all three match
exactly (`M1(1)`@188 099 / `1^503`, `M1(2)`@732 733 / `1^1021`, `M1(3)`@2 852 091 / `1^2039`), and
`M1(1)` agrees with the Lean-proven `h_init_reached`.

- 254 `regenIn`/`cascadeReg` configs inside the g=2 doubling phase.
- `regenIn k` → `cascadeReg k` in **exactly** `exitSteps k` — **8 on-orbit confirmations** of the
  closed form, 5 matching the recorded `exitSteps_grounds`.
- **`RegenLaw ∀k` already discharges 34.00 %** of the phase.
- The phase is an **ascending ladder of 7 disjoint transports, k=5…11**; the k=11 rung
  (536 066 steps, 25.30 %) ends **211 steps before `M1(3)`**.
- The uncovered 66 % obeys a clean **4× recursion** (ratios → 4; residuals `g_{j+1}−4g_j` =
  171, 363, 747, 1515, 3051, differences `192·2^j`).

**So T7 is not one monolithic Θ(2^{2K}) braid** but `gap(5), REGEN(5), …, gap(11), REGEN(11),
tail(211)` — the k-independent-seam structure that let §5bh/§5bj close. T7 is smaller and
better-shaped than recorded.

## 5. D8 kill-tests — one door CLOSED, one HELD ✅ (`D8_KILLTESTS_2026-07-22.md`)

Both instrument-validated first (o4: 8 recorded anchors + `run = v₃(G+14)` over 44 515 runs, 0
mismatches; Antihydra: `M₂ᵒᵈᵈ` reproduced to every recorded digit + independent FFT agreeing to
1e−13).

- **o4 run-cap `R≤3`: FALSIFIED.** First ρ=1 run of length 3 at n=51, of length 4 at **n=90**. The
  recorded "longest run = 2" was an **observation-window artifact** (extraction stopped at n≈40).
  The critical `R≤4` also dies. *A run of ≥4 does NOT mean o4 halts* — it kills one sufficient
  condition; the `R/(R+1)` theorem is untouched, only its applicability. o4 stays `[OPEN]`, and the
  non-halting picture is if anything stronger (freq{ρ=1} = 0.334, ledger ≈ +3/gen).
- **`M₂ᵒᵈᵈ` envelope: HELD**, pushed 25× deeper (J = 8×10⁴ → 2×10⁶, k ≤ 34). Envelope
  0.047 → **0.0074** against the sufficient 0.25 — margin widened to **34×**. No anomaly.
  New: the envelope is **linear in the cutoff, not convergent in it** (every level contributes
  `1/(2√J)`), so the recorded 0.03–0.07 implicitly used `k_max = 20`; the natural cutoff `k*≈21`
  gives `≈ log₂(J)/(2√J) → 0`. A presentation gap in `ODD_ADDITIVE_ENERGY`, not an error.

## 6. D9 lacunary probe — **CLOSED, premise false** ✅ (`D9_LACUNARY_PROBE_2026-07-22.md`)

My own proposal from the previous document, correctly killed. Three independent refutations; the
decisive one needs no orbit data: **the implication runs backwards.** The budget-legal `E[K²]=∞`
adversary `P(D=d) ∝ d^{−2.478}` is up to **27× denser** than geometric — a divergent second moment
means deep returns are *more* frequent, so the surviving adversary is the *least* lacunary
budget-legal law. Empirically real `T_L` is indistinguishable from iid-geometric surrogates (55
tests); restricted cancellation shows zero effect (112 tests, mean z = 0.002) and destroys the
beyond-√ cancellation the full sums already exhibit. Added to the trap list. Two byproducts kept:
the budget identity in uniform form (verified 177/177 to n = 2.5×10⁶) and the full-sum beyond-√
cancellation, which belongs with the D1/D2/D3 margins.

## 7. E2 champion scoping ✅ (`E2_CHAMPION_SCOPING_2026-07-22.md`) — with a caveat

Recommendation: **GO**, 3–6 weeks, but with a restatement — `championSteps` and `BB6` are *both*
opaque axioms, so `champion_lower` as stated has no content; the real task is **defining `BB6`** as
a max over the finite subtype of halting 6-state machines, after which the exact value is never
needed. Hardest sub-obstacle is **not** the tower but the corpus's step-exact `Option`-valued
`steps` discipline (every lemma carries an explicit `Nat` cost); the fix is a count-free
`Reaches c c' := ∃ n, steps n c = some c'` layer — a re-architecture that must come first.

**⚠ Caveat I am flagging rather than propagating:** that report cites
`busycoq/verify/SOBCv5.v` lines 10210–11283 as an existing machine-checked halting proof.
**`busycoq` is not present on this filesystem** and I could not verify those line numbers. The
corpus does independently reference the busycoq project (`NOVELTY_AUDIT_2026-07-07.md` cites
`ccz181078/busycoq .../RWLAcc.v`), so the project is real — but treat the specific citation as
**UNVERIFIED** until checked.

## 8. Champion provenance — an internal contradiction, now flagged ⚠

Verified entirely in-repo, no external claim needed:

| site | value |
|---|---|
| `lean/Completion.lean` §3, `COMPLETION_SKELETON` §, `DATA_SUMMARY` | ≈ **10↑↑15**, "Kropitz-class" |
| `PROBLEM_LIST.md`, `NEW_MATH_PROGRAM.md` | **`Σ(6) > 2↑↑↑5`** (mxdys, 2025) |

`2↑↑↑5` is **pentational**; `10↑↑15` is tetrational — a whole hyperoperation level apart. They
cannot both be right, and the 10↑↑15 figure is the outlier (3 sites vs 2 independent records).
Flagged at all three sites as `[DISPUTED / UNVERIFIED in-repo — re-confirm externally before
quoting]`. **No theorem is affected** (`championSteps` is opaque, `champion_lower` is an axiom);
`lake build Completion` re-verified green after the docstring edit. Not silently "corrected" —
the repo's own discipline is to surface a contradiction, not to pick a side without evidence.

## 9. E1 (o17 Nerode re-verify) — still running at write time

Left to report separately.

---

## The calibration score for today

Consistent with the pattern the x2 closure exposed (*measured claims 5/5, structural narratives
0/2*), and it repeated twice more today:

| claim | kind | outcome |
|---|---|---|
| §5g/§5h reference no `regenIn`/`cascadeReg` | measured | ✅ held |
| ∴ the `⊕` is unwired | **narrative** | ❌ refuted within hours |
| o4's longest ρ=1 run is 2 | measured **in a window** | ❌ window artifact; run 4 at n=90 |
| lacunarity is forced by the budget | **narrative** | ❌ premise false, implication backwards |
| `M₂ᵒᵈᵈ` envelope sits far inside 1/4 | measured | ✅ held, margin widened 34× |
| the closure's axiom footprint | measured | ✅ held |

**Measure first, narrate after.** Every failure today was an inference drawn from a correct
measurement; every measurement survived. Applied forward: T7's "largest single object" label and
the `∀g` extrapolation of the ladder are narrative, and are the next things that should be
measured (g=3), not assumed.

## Recommended next

1. **Extract the gap law** for the doubling-phase ladder and derive it from the machine, the way
   `x2lead_rec.py` / `x2trail_rec.py` derived `leadRec_closed` / `trailSteps_closed`.
2. **Confirm the ladder at g=3** (M6(3)→M1(4)) — predicted: one REGEN per level k=5…13, gaps 4×.
3. Then state `h_doub` for one generation as `∏_k [gap(k) ∘ REGEN(k)]` with `REGEN(k)` supplied by
   `regenLaw_closed`. If the gap episodes admit a `∀k` transport, **T7 closes the way `RegenLaw ∀k`
   did**.
4. Owner decision still pending and untouched: **X1–X3 / D7** external hand-off.
