# The self-referential carry S_n — obstacle, or lever? (2026-06-30)

*Deep-examination task. The genuinely-NEW object in Antihydra (vs pure Erdős/Mahler-of-3ⁿ) is the
**self-referential carry** `S_{n+1}=3S_n+2ⁿ b_n` with `b_n=c_n mod 2` = the orbit's own parity, equivalently
the closed loop "the orbit furnishes its own driving bit" `β_n=bit_k(c_n)`. QUESTION: is the self-reference
only an obstacle, or could it be a LEVER (self-correcting / bootstrap)? What carry-arithmetic could a proof of
(K) exploit? SOUNDNESS PARAMOUNT: every claim `[PROVEN]/[OBSERVED]/[CONJECTURE]/[OPEN]`; no proof claims; no
label upgraded. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/carry_lever.py`, exact
big-int orbit `c₀=8`, `N=10⁵`, <2 s. NOT committed.*

---

## 0. One-line verdict

**The self-reference is a lever on the WRONG subspace.** It is a genuine, proven self-correcting contraction on
the **marginal / even-character channel** (the renewal self-consistency map `Φ` pulls any biased fed-back bit
law back toward Bernoulli(½) — reproduced here, `q_in=0.2→q_out=0.41`, `0.8→0.59`, gap-driven). But the (K)
conclusion lives in the **odd-character / state-coupling channel** `V_odd`, and there the self-reference is
(i) measured to be **neutral white noise** — the per-step feedback `g_n=(β_n−½)χ_a(U(s_n,0))` has
autocorrelation at the `1/√N` floor (all lags `≤0.006`), partial sums grow `~√N` (martingale-difference), and
the one apparent block-level mean-reversion (`−0.14`) is **not significant** (shuffled control `−0.06±0.12`,
i.e. `<1σ`) — and (ii) the only mechanism that *could* sustain a bias (correlation of the fed-back bit with the
low state) is **provably invisible** to the contraction `Φ`, which sees only the marginal bit law
(`I(β_n;s_n)=0.00003` bits). So the lever self-corrects exactly the quantity that is never in danger (density)
and is absent on exactly the quantity that carries the obstruction (coupling). **Net: the self-reference is
neither a clean obstacle nor an active lever — it is OBSERVED-neutral on `V_odd`, and a proven lever on `V_even`
that is provably blind to `V_odd`.** A real lever would require a self-correction mechanism *on the coupling*,
and the only candidate is orbit-arithmetic (the 2-adic Lyapunov `V=v₂(c−1)`), not the gap. **No machine
decided. No label upgraded.**

---

## 1. The new object and why it is genuinely different from Erdős/Mahler-of-3ⁿ

Pure Mahler 3/2 studies the **exogenous** powers `(3/2)ⁿ` — an isometry on `ℤ₂` driven by nothing. Antihydra's
orbit is `c_{n+1}=⌊3c_n/2⌋`, which the renewal analysis (`antihydra_renewal_attack §1`) factors as
`(×3 isometry) ∘ (⌊·/2⌋ = mixing 2-adic shift)`. The shift supplies a **genuine spectral gap** the pure power
lacks — but it is fed by the orbit's own high bit. The exact bookkeeping (`2ⁿc_n+S_n=8·3ⁿ`,
`S_n=Σ_{j<n}3^{n−1−j}2^j b_j`, `b_j=c_j mod 2`) makes this precise `[PROVEN]`:

> `β_n=bit_k(c_n)=bit_{n+k}(8·3ⁿ − S_n)`. The driving bit of the shift IS the orbit's own carry-corrected
> high digit. The loop is closed: `S_n` is built from the very parities `b_j` that the dynamics produces.

This is the one structural feature absent from every classical tool (cocycle ergodicity, ×2,×3 rigidity,
self-consistent coupled maps): an **endogenous, single-specified-orbit, digit-level closed loop**
(`NEWMATH_ENDOGENOUS_UE §7`). The question of this note is whether that closure helps or only hurts.

---

## 2. Lever or obstacle — the two-channel answer

The character space splits `V_even ⊕ V_odd`; the annealed transfer operator is block-triangular with
`L_ann χ_odd ≡ 0` `[PROVEN, ENDOGENOUS_UE_BUILD C2]`. The two channels behave oppositely under the loop.

### 2.1 `V_even` (marginal density): the self-reference IS a lever `[PROVEN-numeric]`
The renewal self-consistency operator `Φ` (`antihydra_renewal §11–12`, `NEWMATH_ENDOGENOUS_UE §1.2`) maps an
incoming-bit law to the output state/bit law it produces, through the gap-0.99 low-bit chain. It **contracts to
Bernoulli(½)**:

> TEST4 (this note, k=6): `q_in → q_out` = `0.2→0.4136, 0.35→0.4502, 0.5→0.5000, 0.65→0.5498, 0.8→0.5859`.
> A biased fed-back bit is **pulled back** toward ½ — a strict contraction (slope `≈0.6<1`).

So at the level of marginal density the closed loop is genuinely **self-correcting**: feeding a biased bit back
into the gap-bearing chain destroys the bias. This is the kernel of truth in "the self-reference is a lever",
and it is why even-density is robust to bit-bias (`§6` weakened target: density `>1/3` for all `q∈[.01,.99]`).
**[PROVEN that the lever exists on `V_even`.]**

### 2.2 `V_odd` (state-coupling): the self-reference is OBSERVED-neutral, and the lever is blind to it
The (K) conclusion is `Inj_a(N)=(1/N)Σ(β_n−½)χ_a(U(s_n,0))→0` for odd `a` (`ENDOGENOUS_UE_BUILD §4`) — a
statement about the **coupling** of the fed-back bit to the transported phase, living entirely in `V_odd`,
which `L_ann` annihilates. Two measured facts pin the self-reference here:

- **The feedback is white / martingale-difference** `[OBSERVED]`. TEST1: the per-step series
  `g_n=(β_n−½)χ_a(U(s_n,0))` has autocorrelation at lags 1,2,3,4,5,8,16 all `≤0.006` (the `1/√N` floor) for
  `k=4,6,8`; partial sums `max|Σg|/√N = 0.28–0.77` (`~√N`, no plateau, no drift). The one suggestive signal —
  block-`|Inj|` lag-1 autocorr `−0.14` (TEST3, would indicate self-correction) — is **destroyed by control**:
  shuffling gives `−0.06±0.12`, so `−0.14` is `<1σ`, an artifact of the `|·|` statistic on 100 blocks. **No
  detectable self-correction OR self-sustenance on `V_odd`.** (This is the §13/§14 discipline: a tempting
  self-correction signal, rejected on control before any claim.)
- **The lever cannot see the coupling** `[OBSERVED]`. TEST5: `I(β_n ; top-bit of s_n)=0.00003` bits (k=8) — the
  fed-back bit and the low state are essentially independent on the real orbit. `Φ` is a function of the
  **marginal** bit law only, so it is structurally **blind** to the state-coupling that is the entire content of
  `V_odd`. The proven no-go (`ENDOGENOUS_UE_BUILD §5`, `NEWMATH_ENDOGENOUS_UE Lemma D`) is exactly this: an
  adversary with the same gap and automaton but a **state-correlated** input realizes `|Inj|≈1` (reproduced
  T4 of `endo_ue_consistency`, `0.165`), while the real orbit gives `0.001`. The gap/lever provably cannot
  distinguish them.

**Verdict.** The self-reference is a lever on `V_even` and OBSERVED-neutral on `V_odd`, and the `V_even` lever is
provably non-interacting with `V_odd`. It is therefore **not the active self-correcting bootstrap one hopes for**
— it does not damp a coupling-bias; it merely fails to create one (on the real orbit). Honest: obstacle-leaning,
because the only place a lever would matter (`V_odd`) is exactly where it is absent/blind.

---

## 3. Where the bootstrap fails to close — and whether a NEW closure is plausible

The §12 conditional theorem is the high-water mark: **IF** `bit_k(c_n) ⊥ c_n mod 2^k` **THEN** the gap-0.99
contraction forces even-density `½ > 1/3` and Antihydra never halts. The failure is precisely located:

1. **Circularity (the §12/§13 wall).** The hypothesis `bit_k ⊥ low-state` **is** `Inj_a→0` **is** (K). The
   §13 cascade and §14 CA-randomization both collapsed to this same hypothesis once made faithful (the
   left-permutive/affine model predicted `parity(c_n)=bit_k(c_{n−k})` at only 37–49%, falsified). The lever
   assumes the decoupling it would need to prove.
2. **Scale regress (`ENDOGENOUS_UE_BUILD §5`).** Bootstrapping scale `k → k+1`: the feedback at scale `k` is
   the top bit of the scale-`(k+1)` state, whose control needs the scale-`(k+1)` feedback — the gap never
   reaches the fresh end of the window. Infinite regress.

**Is a new closure plausible?** Honest triage of the three shapes requested:

- **(a) A different invariant (Lyapunov on the loop).** *Most plausible.* The corpus has a genuine
  orbit-arithmetic Lyapunov the gap does not: `V(c)=v₂(c−1)`, which **deterministically decreases by exactly 1**
  on every `d≥1` step (`[PROVEN]`, `REPELLER_ESCAPE §1`, 300174/300174), so the trap `c≡1 mod 2^k` is 2-adically
  repelling, simultaneously with archimedean growth (dual repulsion, multiplier 3). This is external to
  `(λ₂,U)`, so the no-go does not forbid it. A closure of the form "feedback correlation `Inj_a` ≤ a functional
  of the dispersion of `V`-excursions, `→0`" would be a NEW route. **Status:** the Lyapunov is `[PROVEN]`; the
  coupling of `Inj_a` to its excursions is **not built** — this is the `[OPEN]` Theorem-to-build
  (`NEWMATH_ENDOGENOUS_UE §5`). My numerics give it no free help: the feedback is white (§2.2), so any decrease
  must be in the *conditional* return-time law, not a per-step drift.
- **(b) Multi-scale / 2-step contraction.** *Unlikely as stated.* The scale-regress above is the obstruction;
  the renormalization operator `R=×(3/2)` on the moving diagonal (`NEWMATH_DIAGONAL_RENORM`) is the right
  multi-scale object, but it is `[PROVEN]` to have **no atomic/Pisot/sofic fixed point** (non-Pisot `|3/2|₂=2`)
  and only an **annealed** gap-½ contraction; the quenched single-orbit contraction (R-GEN) is `[CONJECTURE]` =
  (K). Multi-scale reshapes but does not close — it inherits the same `V_even`/`V_odd` split at every scale.
- **(c) Measure-valued fixed point.** *Reframes, does not close.* `Φ` (the self-consistency operator on
  `Prob(ℤ/2^k)`) has Haar as a fixed point, but **also** trap fixed points (`δ₁`, `NEWMATH_ENDOGENOUS_UE §1.2`),
  and the nearest literature (self-consistent coupled maps, arXiv:1909.04484) **produces non-uniqueness**
  generically. So a measure-fixed-point principle must add a *selection* of Haar among self-consistent measures
  by the one orbit — which is EUE itself. No free closure.

**Net:** the only NEW closure not already proven-circular is **(a) a Lyapunov sub-action on `V=v₂(c−1)`**, and
even there the missing piece is the coupling to `Inj_a`, which the numerics show carries no per-step drift.

---

## 4. The PROVEN carry-arithmetic constraints (assembled)

What is rigorously known about `S_n` (candidate raw material for a self-consistency that forces unbias):

| constraint | statement | label | source |
|---|---|---|---|
| **2-adic seam** | `S_n ≡ 8·3ⁿ (mod 2ⁿ)`, so the low-`n` block of the subtraction `8·3ⁿ−S_n` cancels with **borrow_n = 0** | `[PROVEN]` (0 fail) | `CARRY_COBOUNDARY §1a` |
| **finite-range borrow** | the borrow into bit `n+k` reads only the `k`-bit windows `[n,n+k)` of `8·3ⁿ` and `S_n` (bounded-range / finite-state) | `[PROVEN]` (0 fail) | `CARRY_COBOUNDARY §1a` |
| **3-adic structure** | `v₃(S_n)` = even-run length; the `×3` low-bit lemma `S_n≡3^{n−M}S_M (mod 2^M)` | `[PROVEN]` | `antihydra_attack §4f` |
| **growth / non-periodicity** | `c_n→∞`, `log₂c_n=0.585n+3` (parity-blind); itinerary not eventually periodic | `[PROVEN]` | `WALLB_NONATOMIC`, `renewal §8` |
| **exact-trap exclusion** | staying `c≡1 mod 2^k` forever ⇒ `c=1` (off-orbit); `δ₁` and all periodic traps excluded | `[PROVEN]` | `NEWMATH_ENDOGENOUS_UE Lemma A` |
| **2-adic Lyapunov drift** | `V=v₂(c−1)` decreases by exactly 1 each `d≥1` step; trap repelling, dual-repulsion multiplier 3 | `[PROVEN]` | `REPELLER_ESCAPE §1` |
| **renewal / geometric jumps** | depth countdown `D,D−1,…,0` then jump `D_j=v₂(3c′_j−1)`, `P(D≥k)=2^{−k}` | `[PROVEN]` countdown / `[OBSERVED]` geometry | `renewal §7` |
| **annealed carry = Rajchman** | annealed `σ_n=bit_{n+k}(S_n)` Weyl sum `=ν̂_{2/3}(ξ_n)`, 3/2 non-Pisot ⇒ `ν_{2/3}` Rajchman ⇒ equidistributes | `[PROVEN-identity + PROVEN-in-lit]` | `SECOND_DIAGONAL_RAJCHMAN`, `NEWMATH_ENDOGENOUS_UE Lemma E` |
| **carry contributes net ≈0** | iid random carry reproduces the full odd-character energy of `Inj_a` to seed scatter; carry self-energy cancelled by an algebraic cross-term | `[OBSERVED]` | `CARRY_EXOGENIZATION §2,§4` |
| **carry does NOT telescope** | `Σ(β_n−d_n)χ_a(s_n)` grows `~√N` (not bounded) ⇒ carry-piece is not a finite-state coboundary | `[PROVEN no-telescope]` | `CARRY_COBOUNDARY §2(iii)` |

**Can these be assembled into a self-consistency forcing unbias?** Honest reading: they constrain the carry
strongly in the **2-adic / archimedean / annealed** directions (exact seam, finite-range borrow, Lyapunov
drift, Rajchman decay), but every one of them is either (i) **blind to the state-coupling** (annealed
constraints, by definition) or (ii) a **deterministic countdown** that the carry rides without telescoping. The
constraints fence in *where* a bias could live (only in the state-coupling of the moving diagonal, surviving
the countdowns) but do not by themselves kill it. The assembly that would force unbias is exactly the
`[OPEN]` Lyapunov-coupling of §5.

---

## 5. The cleanest endogenous-UE fixed-point principle, the exact missing ingredient, and its shape

**The principle (the closure target), stated as cleanly as the corpus allows:**

> **Endogenous Anti-Resonance / R-genericity.** For the single closed-loop orbit `c₀=8`, the empirical measures
> `π_N=(1/N)Σδ_{s_n}` (`s_n=c_n mod 2^k`) converge to Haar for every `k` — equivalently the fed-back bit cannot
> phase-lock to its own low state, `Inj_a(N)=(1/N)Σ(β_n−½)χ_a(U(s_n,0))→0` for every odd `a`. `[CONJECTURE]`,
> proven `⟺ (K) ⟺` Antihydra non-halt (`NEWMATH_ENDOGENOUS_UE §4`).

**The exact missing ingredient (what the no-go forces, beyond gap+automaton).** The selector among
self-consistent measures must be a property **specific to the endogenous input** `β_n=bit_k(c_n)` — i.e.
orbit arithmetic — because `(λ₂,U)` provably cannot distinguish the real orbit from a coupling-adversary
(`§2.2`, no-go). Carry-stripped (`CARRY_EXOGENIZATION`: the carry is annealed-indistinguishable, net ≈0) and
reduced to the odd block (`Lemma C`: even is enslaved to odd), the single residue is **EAR-diagonal**:

> `(1/N) Σ_{n<N} (bit_{n+k}(8·3ⁿ) − ½)·χ_a(⌊3(c_n mod 2^k)/2⌋ mod 2^k) → 0`  (a odd)  `[OPEN]`.

This is the exogenous Mahler diagonal read against the **orbit-defined** phase — single-orbit Mahler 3/2 /
AEV Conj 1.6 at α=8.

**Its most plausible shape.** A **Kac-type return-time identity** coupling the feedback correlation `Inj_a`
to the **excursion statistics of the 2-adic Lyapunov `V=v₂(c−1)`** (the renewal countdowns + geometric jumps),
proving the excursions cannot conspire to a positive-density phase-lock — a **Lyapunov sub-action** for the
self-driven cocycle, *not* a contraction (the no-go forbids the gap from doing it). The seed is the exact
valuation budget `Σv₂(3c_i−1)=n+v₂(c_n)−v₂(c_0)` (`VALUATION_BUDGET`), a first-moment law that the
sub-action would have to upgrade to anti-concentration of the diagonal phase. My numerics constrain the shape:
the feedback is white per-step (§2.2), so the sub-action's decrease must live in the **conditional return-time
law across countdowns**, not in any per-step drift — i.e. the right object is the **first-return-to-even induced
map** `F(c′_j)=(3^{D}u+1)/2` (`renewal §8`) and the claim is that the moving-diagonal phase decorrelates across
its iid-geometric jumps. This is buildable in principle (proven base case Lemma A,B; proven annealed half Lemma
E; proven contraction wrapper Lemma C) and is the one route the no-go does not pre-empt — but it is `[OPEN]`
and `⟺` a 57-year open problem.

---

## 6. Numerics (`scratchpad/carry_lever.py`, exact big-int, N=10⁵, <2 s)

| test | what it checks | result | reading |
|---|---|---|---|
| **T1** feedback autocorr | is `g_n=(β_n−½)χ_a(U(s_n,0))` self-correcting (neg.), self-sustaining (pos.), or white? | lags 1–16 all `≤0.006`; `max|Σg|/√N=0.28–0.77` (k=4,6,8) | **white / martingale-difference** — neither lever nor obstacle per-step |
| **T2** renewal phase-reset | even-step vs odd-run feedback differ? | both ride the floor (`|Inj|=0.0011–0.0033`) | no strong differential |
| **T3** block mean-reversion | block-`|Inj|` lag-1 autocorr `<0` ⇒ self-correcting | real `−0.14`, but shuffled control `−0.06±0.12` (`<1σ`) | **artifact, rejected** (§13 discipline) |
| **T4** annealed `Φ` | does a biased fed-back bit get pulled back to ½? | `q_in 0.2→0.41, 0.5→0.50, 0.8→0.59` | **genuine lever on the MARGINAL channel** |
| **T5** coupling visibility | can `Φ` see the state-coupling? | `I(β_n;top-bit s_n)=0.00003` bits (k=8) | **blind** — lever cannot act on `V_odd` |

Each test could have falsified a claim; T3 nearly produced a false "self-correcting" reading and was killed by
control. The picture is consistent: lever on `V_even`, neutral+blind on `V_odd`.

---

## 7. Sources

- **Repo (proven/observed inputs):** `ENDOGENOUS_UE_BUILD.md` (seam identity, `L_annχ_odd≡0` C2, no-go §5, Open
  Lemma §4); `NEWMATH_ENDOGENOUS_UE.md` (EAR principle, Lemmas A–E, reduction §4, Theorem-to-build §5);
  `antihydra_renewal_attack.md` (§1 shift factorization, §2 gap-0.99, §6 weakened target, §7–8 renewal/induced
  map, §11–12 self-consistency `Φ` + conditional theorem, §13–14 falsified cascade/CA — the discipline
  precedent); `CARRY_EXOGENIZATION.md` (carry annealed-indistinguishable, net ≈0); `CARRY_COBOUNDARY.md`
  (borrow decomposition `β=d⊕σ⊕ρ`, finite-range borrow, no-telescope √N growth); `NEWMATH_DIAGONAL_RENORM.md`
  (R-GEN, non-Pisot no-atom, annealed gap-½); `REPELLER_ESCAPE.md`/`VALUATION_BUDGET.md` (2-adic Lyapunov,
  valuation budget); `WEAPONS_AUDIT_2026-06-29.md §5` (new-math spec); `COMPLETE_PROOF_CAPSTONE.md §2`
  (five-link reduction).
- **Literature (repo knowledge):** Mahler "An unsolved problem on the powers of 3/2" (1968, open);
  Andrieu–Eliahou–Vivion arXiv:2510.11723 (AEV Conj 1.6); Erdős(1939)/Salem(1944) Rajchman ⟺ non-Pisot;
  Varjú–Yu arXiv:2004.09358 (effective rate); self-consistent coupled maps arXiv:1909.04484 (non-uniqueness);
  Kaimanovich–Schmidt (cocycle ergodicity); Sinai/Kontorovich–Sinai (2-adic Collatz ergodicity).
- **Numerics:** `scratchpad/carry_lever.py` (T1 feedback white-noise autocorr + √N partial sums; T2 renewal
  even/odd split; T3 block mean-reversion + shuffle control; T4 annealed `Φ` contraction; T5 `I(β;state)≈0`),
  building on `seam_identity.py`, `carry_exo*.py`, `endo_ue_consistency.py`.

**No machine decided. No label upgraded.**
