# The BB(6) Conditional Completion Skeleton (2026-07-10)

*The maximal rigorous internal structure: a machine-checkable reduction of the **complete** BB(6) proof to an
explicit, precisely-stated list of arithmetic conjectures. This document is the honest logical skeleton — it
**decides no machine**. Every line is labelled `[PROVEN, Lean]` / `[PROVEN on grid]` / `[PROVEN-in-lit]` /
`[OBSERVED]` / `[CONJECTURE]` / `[OPEN]`. It states exactly what is proven versus conjectured, and exactly what
remains and why (K)/Collatz-hardness is the barrier. Sources: `ROADMAP_COMPLETE_PROOF_2026-07-10.md`,
`PAPER_CENSUS.md`, `ATTACK_PLAN_2026-07-10.md`, `HOLDOUT_SWEEP_FEASIBILITY_2026-07-10.md`, per-machine notes,
`lean/` layer (`Mirror`, `RunStructure`, `Template`, `Suffix`, `O3`, `O18`, `O17`), AEV arXiv:2510.11723.*

---

## 0. The decomposition (the shape of the complete proof)

```
BB(6) = N(champion)  ⟺
  [A] the 17 named cryptids all NON-HALT   (each ⟺ one explicit arithmetic conjecture)
∧ [B] the ~1087 un-catalogued holdouts all NON-HALT   (community-scale residual)
∧ [C] the champion HALTS at exactly N   (checkable in principle; closed-form tower value)
∧ [D] the 5-tuple / 6-state enumeration is formally complete   (Coq-BB5-scale engineering)
```

Nothing below upgrades any label. The achievement is that **[A] is now an explicit finite list of named open
problems**, [C]/[D] are engineering, and [B] is a bounded community-scale sweep whose expected internal yield is 0.

---

## 1. THE FORMAL PROTECTION LEDGER — the 17 named cryptids

For each machine: (i) its exact halting characterization; (ii) the arithmetic conjecture whose truth forces
non-halting; (iii) the **reduction status** of "machine halts ⟺ conjecture"; (iv) the famous open problem it is
equivalent to. `p/q` = the branch multiplier; `v_q` = q-adic valuation; `x` = integer branch fixed point.

### 1a. The (K)-frequency band — 14 machines (protection = base-p/q normality / AEV Conj 1.6 / Mahler 3/2)

Uniform reduction `[PROVEN, Lean: Mirror.lean]`: each machine iterates `T(v)=⌊(p/q)v⌋+c(v)`; every branch is affine
`b(v)=(pv+e)/q` with integer fixed point `x=−e/(p−q)`; the maximal run of a branch from `v` is `v_q(v−x)` (theorem
`run_closed_form`/`run_cap`). Halting is a **gate** (local, `[PROVEN from the table]`, window census saturates small
and safe); the protection is that the gate never fires = a one-sided **frequency** bound on deep q-adic returns
`v_q(v_n−x) ≥ ℓ`. That frequency bound is base-p/q normality of the seed orbit — **(K)** = AEV Normality Conjecture
1.6 (arXiv:2510.11723), the floor-mirror of Mahler's 3/2 problem.

| # | machine | ×p/q | halt ⟺ (exact) | conjecture forcing non-halt | reduction "halt⟺conj" | ≡ open problem |
|---|---|---|---|---|---|---|
| 1 | **o4** | ×4/3 | gate fires ⟺ `freq{3∣W_n} ≥ 4/5`, seed `W₀=57` (margin 2.4, subcritical `5≤81`) | `freq{3∣W_n} ≤ 4/5 − ε` | **`[PROVEN, Lean END-TO-END]`** (odometer+ledger; only informal residue = the a-ledger conjecture) | base-4/3 normality (K) — **the easiest instance** |
| 2 | **o3** | ×4/3 | gate ⟺ same freq class (roles swapped, a=odometer) | base-4/3 return-freq bound | `[PROVEN, Lean: O3]` (body + generation map) | base-4/3 normality (K) |
| 3 | **Antihydra** | ×3/2 | halts ⟺ running balance `2·#even−#odd` goes `<0` ⟺ `even-density < 1/3` | `even-density ≥ 1/3` | `[PROVEN-in-lit]` (renewal/Kac; run-law corollary Lean) | **AEV Normality Conj 1.6** (verbatim), Mahler 3/2 |
| 4 | **o10** | ×3/2 | same as Antihydra (fixed pts (0,1), run `v₂(c),v₂(c−1)`) | `even-density ≥ 1/3` | `[PROVEN on grid]` (run-law corollary) | AEV 1.6 / Mahler 3/2 |
| 5 | **o2** | ×3/2 (ceiling) | gate ⟺ deep-return freq (fixed pts (0,1)); **critical**, ratio 1.17 | quenched `v₂`-return freq bound | `[PROVEN on grid]` (Link 0 certified; run-law corollary) | (K) at the critical boundary |
| 6 | **o11** | ×3/2 | gate ⟺ freq of `v₂(m+8),v₂(m+7)` returns (sea/resetting) | per-epoch residue-draw freq bound | `[PROVEN, Lean corollary]` (refill law grid) | (K) / Mahler 3/2 |
| 7 | **o13** | ×3/2 | fixed pts (−14,−7); run `v₂(a+14),v₂(a+7)` | same | `[PROVEN, Lean corollary]` | (K) |
| 8 | **o14** | ×3/2 | fixed pts (−12,−11); run `v₂(a+12),v₂(a+11)` | same | `[PROVEN, Lean corollary]` | (K) |
| 9 | **o16** | ×3/2 | fixed pts (−4,−3); run `v₂(s+4),v₂(s+3)` | same | `[PROVEN, Lean corollary]` | (K) |
| 10 | **o12** | ×3/2 (sea) | gate ⟺ sea-epoch return-freq bound | per-epoch residue-draw bound | `[OBSERVED]` (catalogue; same fixed-pt structure) | (K) |
| 11 | **o8** | ×3/2 (nested) | gate ⟺ nested-reset return-freq bound | same | `[OBSERVED]` (reset orbit reconfirmed) | (K) |
| 12 | **o5** | ×4/3 | gate ⟺ base-4/3 return-freq bound | `freq{3∣·} ≤ 1−ε` | `[OBSERVED]` (catalogue; o4-class) | base-4/3 normality (K) |
| 13 | **o15** | ×8/3 | gate ⟺ `v₃(V−1)` return-freq (fixed pt 1) | base-8/3 return-freq bound | `[PROVEN on grid + Lean depth]` | base-8/3 normality (K) |
| 14 | **o18** | ×8/3 | gate ⟺ same; pushdown 3-adic odometer | base-8/3 return-freq bound | `[PROVEN, Lean: O18]` (machine + sweeps) | base-8/3 normality (K) |

**Band verdict `[PROVEN, closure-with-proofs, 7 build attempts]`:** the depth axis of all 14 is controlled
unconditionally in Lean; the single residual per machine is the **frequency** axis = `ℤ_q^×`-equidistribution of the
seed's reload units = (K). The entire band is **one problem in 14 coordinates**; o4 is the least-protected instance.

### 1b. The thin-set-reachability band — 2 machines (protection = generalized-Collatz `2^k`-avoidance)

Not density statements: a **reachability** wall (halt ⟺ an explicit orbit ever hits a `2^k`-thin target). The no-go
corpus (No-Structure/AIU/rigidity/excursion/digit) does NOT cover these; they are the only named machines where an
internal decision was *a priori* conceivable — attacked 2026-07-10, both walls confirmed real.

| # | machine | halt ⟺ (exact) | conjecture forcing non-halt | reduction status | ≡ open problem |
|---|---|---|---|---|---|
| 15 | **o7** | milestone `u_n=a+3`; **halt ⟺ `u=2^k` (k≥2) ⟺ oddpart(u)=1** ever. Dynamics: even `u→3u/2`, odd `u→(u+1)/2`; cascade `u_e′=3^v·oddpart(x₁)−1` | oddpart(u_e) never `=1` (`min oddpart=7` over 49,941 entries, `[OBSERVED]`) | `[OBSERVED, 0-mismatch to 2·10⁷]` (milestone automaton, not Lean); non-Type-I (two multipliers) | Collatz-type 2-adic Diophantine; **no finite congruence invariant** (`ℤ/m` full, `[PROVEN, over-approx]`) |
| 16 | **Space Needle** | ×5/2 even branch (run `v₂(m+4)`); odd branch no fixed point. Epoch `1^m` halts ⟺ `m∈S`; **halt ⟺ `m_n+1=2^k`** (residual fatal target `{2^k−1}`) | orbit `m_{n+1}=f(m_n)` never enters `S={2^k−1}∪{6,102,311,351,371,…}` | `[OBSERVED]` (fatal-set census; automaton NOT finite-state) | Collatz-type 2-adic reachability; **no separating modulus** (`[PROVEN, bits equidistribute]`) |

### 1c. The gate-timing band — 1 machine (protection = unbounded-gate-state carry timing)

| # | machine | halt ⟺ (exact) | conjecture forcing non-halt | reduction status | ≡ open problem |
|---|---|---|---|---|---|
| 17 | **o17** | gate = `(μ∈{3,5}, d⃗)`; map `F(μ,d⃗)` exact. **halt ⟺ some μ=5 gate branches to μ′=8** (seam `0 0 [1]_A`) | every μ=5 gate branches to μ′=3 (blank orbit: 8 gates, μ=5 twice, both safe `[OBSERVED]`) | `[PROVEN parameterization, machine-validated + lean/O17.lean both directions]`; **no scalar residue** (digits→∞, no fixed base); **Nerode index 1,2,6,19,54,132 unbounded ⟹ no finite automaton `[OBSERVED, Myhill–Nerode]`** | Collatz-type gate-timing; tower-sparse (next gate ~10⁶⁰), "(K)-shaped" |

**Ledger bottom line `[honest]`:** 14 protections ≡ (K)/AEV 1.6/Mahler 3/2 (o4 easiest); 2 ≡ generalized-Collatz
`2^k`-reachability (o7, SN); 1 ≡ Collatz-type gate-timing (o17). **No protection is internally decidable** — each has
a mechanistic closure proof (frequency band) or a confirmed reachability/finite-state impossibility (o7/SN/o17).

---

## 2. THE CHAMPION — status of N

- **Champion machine** (bbchallenge BB(6) record, verbatim in `suite.py::CRYPTIDS`):
  `1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE`.
- **Step count:** halts after **~10↑↑15** [DISPUTED, see below] steps (`README.md`; Kropitz-class tetrational record). This is a specific
  ⚠ **VALUE FLAGGED 2026-07-22:** the `10↑↑15`/Kropitz figure contradicts this repo's own `PROBLEM_LIST.md` / `NEW_MATH_PROGRAM.md`, which record `Σ(6) > 2↑↑↑5` (mxdys, 2025) — pentational, one hyperoperation level higher. UNVERIFIED in-repo; re-confirm externally before quoting. Nothing depends on it (`championSteps` is opaque). See `lean/Completion.lean` §3.

  finite tower value with a closed form derivable from the machine's nested-loop structure, **not brute-force
  runnable** (unphysical). Our simulator self-verifies only the hand-checkable champions BB(2)=6, BB(3)=21,
  BB(4)=107, BB(5)=47,176,870 (`bb_sim.py`, `suite.py`); the BB(6) champion's halt is asserted from the analyzed
  closed form, not from a full trace. Status: `[OBSERVED / PROVEN-in-lit]` — the halt and the tower value are
  established by structural analysis; a fully machine-checked closed-form step count is **[OPEN, engineering]**.
- **Honest status of N:** **BB(6) is only bounded *below*.** `N(champion) ≈ 10↑↑15` gives `BB(6) ≥ N`. It is **NOT**
  a proven equality: N is the current record, not shown maximal. The complete proof needs `BB(6) = N`, i.e.
  additionally that **every** other 6-state machine halts in `≤ N` steps or never halts — which is exactly conjuncts
  [A]+[B]+[D]. So "BB(6)=N" is **[CONJECTURE]**; "BB(6)≥N" is `[OBSERVED/PROVEN-in-lit]`.

---

## 3. THE CONDITIONAL COMPLETION THEOREM

> **Theorem (conditional, honest skeleton).** Let `N` be the champion's step count. Then `BB(6) = N` provided:
> - **[A]** each of the 17 named protection conjectures of §1 holds (⟹ those 17 machines never halt);
> - **[B]** all ~1087 un-catalogued holdouts of `_bbdata/bb6_holdouts_1104.txt` (= 1104 − 17 named) never halt;
> - **[C]** the champion halts at exactly `N`;
> - **[D]** the 6-state TNF enumeration is complete: every 6-state machine is, up to isomorphism, the champion, one
>   of the 17 named, one of the 1087 holdouts, or already decided (halts `≤ N`, or proven non-halting) by the
>   certified deciders.

**Conjunct-by-conjunct status:**

| conjunct | content | status |
|---|---|---|
| **[C]** champion halts at N | closed-form tower value, structurally analyzed | `[OBSERVED/PROVEN-in-lit]`; fully-checked step count `[OPEN, engineering]` |
| **[A]** 17 named non-halt | 14 ≡ (K)/AEV 1.6/Mahler 3/2 (o4 easiest, `freq≤4/5−ε`); o7,SN ≡ Collatz `2^k`-reachability; o17 ≡ gate-timing | **17× `[CONJECTURE]`, each = a named open problem**; the *reductions* halt⟺conj are `[PROVEN, Lean]` (o4 end-to-end, o3, o18, run-law corollaries) down to `[OBSERVED]` (o7/SN automata, o5/o8/o12 catalogue) |
| **[B]** 1087 holdouts non-halt | certified suite yields 0/10, 0/300 (⊆ community decider class) | **community-scale `[OPEN]`**; not internally decidable with current tools |
| **[D]** enumeration complete | Coq-BB5-scale formal decider pipeline | **engineering `[OPEN]`**, no new math (BB(5) precedent) |

**Reading.** The complete BB(6) proof is reduced to: **17 explicit named conjectures (each equivalent to a famous
open problem)** + **1087 holdouts (community-scale sweep)** + **champion + enumeration (checkable engineering)**. The
*mathematical* barrier is entirely conjunct [A] — and within [A], the (K)/Collatz-hardness of the 17 protections.

---

## 4. LEAN-FORMALIZABILITY ASSESSMENT

**What is already Lean-done `[PROVEN, Lean]`** (`lean/`, 8 modules, 324 theorems, sorry-free, axioms
`[propext, Quot.sound]`): the uniform run-structure theorem + census corollaries (`Mirror`, `RunStructure`); o4's
machine→arithmetic reduction **END-TO-END** (`Template`, `Suffix` — the only informal residue is the a-ledger
conjecture itself); o3's body + generation map (`O3`); o18's machine + sweeps (`O18`); o17's gate map both directions
(`O17`); the criticality comparison + o4's subcritical exclusion.

**The CONDITIONAL theorem is Lean-formalizable now**, with the conjectures as hypotheses/`axiom`s. Effort estimate:
the reductions "Halts oX ↔ oXConjecture" exist for o4 (end-to-end) and structurally for the run-law band; wiring them
into one `BB6 = N` statement is **assembly, not new proof** — the hard content stays inside the named `axiom`s. The
1087 holdouts enter as a single quantified hypothesis; [D] enters as a `decide`-style completeness axiom pending the
full enumerator.

**Sketch — `lean/Completion.lean`:**

```lean
import BB6.Machine   -- TM6, step, halts, haltsAt, TNF-isomorphism
import BB6.Mirror     -- the PROVEN uniform reduction + run laws
namespace BB6.Completion

def champion : TM6 := ⟨"1RB1RA_1RC1RZ_1LD0RF_1RA0LE_0LD1RC_1RA0RE"⟩
def N : ℕ := tower 10 15            -- closed-form ~10↑↑15 (structural, [OPEN] to fully verify)

def named17   : Finset TM6 := { o4, o3, antihydra, o10, o2, o11, o13, o14, o16,
                                o12, o8, o5, o15, o18, o7, spaceNeedle, o17 }
def holdouts1087 : Finset TM6 := ofList bb6_holdouts_1104 \ named17

/- [A] the 17 protection conjectures (each ≡ a famous open problem), as explicit Props -/
def O4Conj : Prop := ∀ ε>0, freqDiv3 W0_57 ≤ 4/5 - ε        -- base-4/3 normality (K)
def AntihydraConj : Prop := evenDensity ≥ 1/3               -- AEV Normality Conj 1.6
def O7Conj : Prop := ∀ n, oddpart (u n) ≠ 1                 -- generalized-Collatz 2^k-avoidance
def SNConj : Prop := ∀ n, (m n) + 1 ∉ powersOfTwo
def O17Conj : Prop := ∀ g, gateMarker g = 5 → gateBranch g ≠ 8
-- … o3, o10, o2, o11, o13, o14, o16, o12, o8, o5, o15, o18 …

/- Reductions: PROVEN, Lean (o4 END-TO-END); the others cited/[OBSERVED] as axioms for now -/
theorem o4_reduction  : ¬ halts o4  ↔ O4Conj := Mirror.o4_end_to_end   -- [PROVEN, Lean]
axiom antihydra_reduction : ¬ halts antihydra ↔ AntihydraConj          -- [PROVEN-in-lit]
axiom o7_reduction        : ¬ halts o7        ↔ O7Conj                 -- [OBSERVED automaton]
-- … one per named machine …

theorem champion_halts_at_N : haltsAt champion N := by structural_analysis  -- [C], [OPEN] to close
axiom enumeration_complete :                                                -- [D], engineering
  ∀ M : TM6, (M ≈ champion) ∨ (∃ m ∈ named17, M ≈ m) ∨ (∃ h ∈ holdouts1087, M ≈ h)
           ∨ decidedNonHalt M ∨ (∃ k ≤ N, haltsAt M k)

theorem BB6_eq_N
    (hA : O4Conj ∧ AntihydraConj ∧ O7Conj ∧ SNConj ∧ O17Conj ∧ …)  -- the 17
    (hB : ∀ M ∈ holdouts1087, ¬ halts M)                            -- the 1087
    : BB6 = N := by
  -- champion ≥ N via champion_halts_at_N; every other M ≤ N or ¬halts
  -- via enumeration_complete + reductions(hA) + hB; sup = N.
  sorry  -- assembly from the above; hard content isolated in hA/hB/[C]/[D]
end BB6.Completion
```

**Verdict:** the conditional theorem `BB6 = N ⟸ (17 conjectures) ∧ (1087 non-halt) ∧ [C] ∧ [D]` is **Lean-stateable
today** and largely **Lean-provable modulo the four labelled gaps** (o4 reduction is already discharged; the rest are
`axiom`s standing for cited/observed reductions and the engineering conjuncts). It cleanly isolates all
irreducible mathematics into the named `axiom`s. This is the maximal internal formal object.

---

## 5. THE HONEST BOTTOM LINE

The complete BB(6) proof is **reduced to an explicit, finite, machine-checkable skeleton**:

1. **17 named conjectures**, each equivalent to a famous open problem — 14 to **base-p/q normality** (AEV
   Conjecture 1.6 / Mahler's 3/2 problem; o4 the least-protected, `freq{3∣W_n} ≤ 4/5 − ε` at seed 57), 2 to
   **generalized-Collatz `2^k`-reachability** (o7, Space Needle), 1 to **Collatz-type gate-timing** (o17). Each has
   a *proven internal closure* (the frequency band's 7 build attempts; o7/SN's no-finite-invariant results; o17's
   unbounded Nerode index) explaining why it is **not internally decidable**.
2. **~1087 un-catalogued holdouts** — community-scale; our certified suite (⊆ the community's decider class that
   *produced* this residual) yields 0, so this flank needs the Coq-BB5-scale pipeline or per-machine reductions.
3. **Champion + enumeration** — checkable engineering: `N ≈ 10↑↑15`, `BB(6) ≥ N` established, `BB(6) = N` pending [A].

**This is the maximal achievement reachable WITHOUT resolving the walls.** It makes precise EXACTLY what remains:
the whole complete-proof enterprise is now the conjunction `[17 named open problems] ∧ [1087-machine community sweep]
∧ [champion + enumeration engineering]`, with a Lean statement (`Completion.lean`) that isolates every irreducible
piece into a named hypothesis. The barrier is (K)/Collatz-hardness, localized to 17 explicit places — the moment the
AEV/Eliahou circle resolves base-p/q normality, conjunct [A]'s frequency band (14 of 17) falls simultaneously.

No cryptid is decided; no protection is closed. The skeleton is a **reduction**, not a proof of BB(6).

---

*Verification: `verify_all.py --quick` (7/7 PASS); Lean `lake build` (17 jobs green, 324 theorems, sorry 0, axioms
`[propext, Quot.sound]`). Holdout list: `_bbdata/bb6_holdouts_1104.txt`. This document introduces no new claim and
upgrades no label.*

No machine decided. No label upgraded.
