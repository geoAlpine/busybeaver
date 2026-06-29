# Dichotomy Lemma audit — Berend vs Rudolph–Johnson on the (2,3)-solenoid (2026-06-29)

*WEAPONS_AUDIT style. Settles the truth of the "dichotomy lemma" of `NEWMATH_ADELIC_RIGIDITY.md` §3.2
(also quoted in `FURSTENBERG_CORNER_QUESTION.md` §0 and `NEWMATH_SYNTHESIS.md` §1). SOUNDNESS PARAMOUNT:
every claim labelled `[PROVEN]`/`[PROVEN-in-lit]`/`[OPEN]`/`[OVER-CLAIMED]`. No claim to prove (K). Not committed.*

---

## 0. ONE-LINE VERDICT

**OVER-CLAIMED — and corrected.** The lemma's measure conclusion ("the *only* gap between `A`-invariance and
Haar is `A`-invariant ⟹ `Φ`-invariant; a `Φ`-invariant ergodic limit is forced to be Haar or finite") is
**FALSE as proved**: its proof uses **Berend's topological set-rigidity to reach a measure conclusion**, which
it cannot. Berend gives only `supp(μ)` finite-or-`X`; the jump from *full support* to *Haar* is exactly the
entropy hypothesis (Rudolph–Johnson) or, without it, **Furstenberg's open conjecture**. So there are **TWO**
gaps to Haar, not one: **(i) AIU** (`A`-invariant ⟹ `Φ`-invariant) **and (ii) positive entropy**
`h_μ(M_2)>0`. What *does* survive `[PROVEN]` is a strictly weaker **topological** dichotomy for the **rank-2
host orbit** (not the rank-1 `A`-orbit). This confirms the soundness banner already prepended to
`FURSTENBERG_CORNER_QUESTION.md` and the correction in `LIMIT_MEASURE_ENTROPY.md`.

---

## 1. What BEREND actually gives — TOPOLOGICAL (set) rigidity, RANK ≥ 2 only

**Theorem (Berend 1983, tori; solenoid form via Einsiedler–Lindenstrauss notes / arXiv:2101.11120).**
`[PROVEN-in-lit]` Let `α : ℤ^d → Aut(Y)` act by automorphisms of a torus or (finite-dimensional) solenoid `Y`.
Then **every `α(ℤ^d)`-orbit is finite or dense** (equivalently: every closed `α`-invariant subset is finite or
`= Y`) **iff** the action satisfies all three:
1. **totally irreducible** — no finite-index subgroup of `ℤ^d` has a nontrivial proper closed invariant
   subgroup (no rational invariant subspace);
2. **not virtually cyclic** — the acting group is not a finite extension of `ℤ`; equivalently **rank ≥ 2**;
3. **contains a hyperbolic element** — some `α(n)` has no neutral (modulus-1 / norm-1) direction at any place.

**Does the solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` with host `Φ=⟨×2,×3⟩≅ℤ²` satisfy (1)–(3)?** **YES `[PROVEN]`:**
- (1) `X` is the 1-dimensional `ℤ[1/6]`-solenoid; its dual `ℤ[1/6]` has rank 1, so there is no proper rational
  invariant subspace — totally irreducible. `[PROVEN]`
- (2) `Φ=⟨×2,×3⟩≅ℤ²` (2, 3 multiplicatively independent) is **rank 2**, not virtually cyclic. `[PROVEN]`
- (3) **`A=M_3M_2^{-1}=×(3/2)∈Φ` is hyperbolic** (dilations `(3/2,2,1/3)`, no neutral place). `[PROVEN]`
  (Note `M_2` alone has dilations `(2,½,1)` — *neutral* at `ℚ₃`; `M_3` is neutral at `ℚ₂`; so the hyperbolic
  witness must be a genuine rank-2 combination such as `A`.)

So Berend **applies to the rank-2 host `Φ`** and yields, `[PROVEN]`:
> **(B-set)** Every closed `Φ`-invariant subset of `X` is finite or `=X`. Hence the **`Φ`-orbit** of any
> `ℤ[1/6]`-point with infinite orbit is **dense** in `X`.

**CRUCIAL — Berend says NOTHING about a single `A`-orbit.** `A=×(3/2)` generates `⟨A⟩≅ℤ`, which **is virtually
cyclic** — it **fails condition (2)**. Berend is a statement about the **rank-`d≥2`** orbit
`{Φ(n)·x : n∈ℤ²}`, not about the **rank-1 sub-orbit** `{Aⁿ·x : n∈ℤ}`. A single hyperbolic toral/solenoid
automorphism has an **uncountable** family of closed invariant sets and invariant measures — **no** topological
rigidity (Einsiedler–Lindenstrauss, rank-one case, JMD 2008). `[PROVEN-in-lit]`

---

## 2. What RUDOLPH–JOHNSON gives — MEASURE rigidity, REQUIRES positive entropy

**Theorem (Rudolph 1990; Johnson 1992).** `[PROVEN-in-lit]` Let `p,q` be multiplicatively independent
(`Rudolph`: coprime integers; `Johnson`: any non-lacunary multiplicative semigroup). If `μ` is a Borel
probability measure on `ℝ/ℤ`, invariant under **both** `×p` and `×q`, **ergodic** under the generated
semigroup, and `h_μ(×p) > 0` **for some element** (positive entropy), then `μ` is **Lebesgue**. Equivalently:
a non-Lebesgue jointly-invariant ergodic measure has `h_μ=0` under every element (and the maps are a.e.
invertible).

**Solenoid form.** `[PROVEN-in-lit]` Einsiedler–Lindenstrauss, *Rigidity properties for commuting automorphisms
on tori and solenoids* (arXiv:2101.11120): a `Φ=⟨×2,×3⟩`-invariant, ergodic measure on a solenoid of this type
with **positive entropy under some element** is **Haar**. The positive-entropy hypothesis is **essential and is
not removable** by any known method on a density-zero semigroup like `⟨2,3⟩` (the one entropy-free theorem,
Einsiedler–Fish arXiv:0804.3586, needs a **positive-density** semigroup and does **not** apply).

**Furstenberg's conjecture** `[OPEN]` (Furstenberg 1967): a non-atomic ergodic `×2,×3`-invariant measure is
Lebesgue — i.e. Rudolph–Johnson **without** the entropy hypothesis. This is a famous **open** problem; the
non-atomic zero-entropy case is exactly what is unresolved (existence of a non-Haar such measure is itself
open). Therefore **"`Φ`-invariant ergodic ⟹ Haar or finite, without entropy" IS Furstenberg's open
conjecture.**

---

## 3. THE VERDICT

### (a) Is "`Φ`-invariant ergodic measure ⟹ Haar or finite" true WITHOUT entropy? — **NO. `[OPEN]`**
That is precisely **Furstenberg's conjecture** (solenoid form). It is **open**. So the lemma, read as a measure
statement, asserts an open conjecture as `[PROVEN]`. **`[OVER-CLAIMED]`.**

**Where the §3.2 proof breaks (the exact bug).** The proof says: "Berend ⟹ every proper closed `Φ`-invariant
set is finite ⟹ (with periodic exclusion) `μ` is Haar." But Berend classifies **closed invariant SETS**, not
**invariant MEASURES**. The most it gives for a measure is: `supp(μ)` is a closed `Φ`-invariant set, hence
**`supp(μ)` is finite or `=X`**. For non-atomic `μ` this yields **`supp(μ)=X` (full support) — NOT `μ=Haar`.**
A fully-supported, non-atomic, zero-entropy, non-Haar `Φ`-invariant measure is **not excluded by Berend**;
excluding it is exactly the open content. The proof **conflates support-rigidity (topological) with
measure-rigidity**. Invalid.

### (b) Is the correct statement "AIU + positive entropy ⟹ Haar (Rudolph–Johnson)", i.e. TWO gaps? — **YES.**
From the `[PROVEN]` `A`-invariance (`μ` non-atomicity is **[OPEN]**, not proven — see `ENT_NONATOMIC.md`; the orbit
provably avoids periodic points per-visit, but `μ` charging them zero mass = vanishing occupancy is (K)-hard), reaching
Haar requires **both**:
- **Gap (i) — AIU:** `A`-invariant ⟹ `Φ=⟨×2,×3⟩`-invariant. `[OPEN, CONJECTURE]`
- **Gap (ii) — positive entropy:** `h_μ(M_2) > 0`, to invoke the **proven** Rudolph–Johnson. `[OPEN]`,
  and `(K)`-necessary (under `(K)`, `μ=`Haar has `h_{Haar}(M_2)=log2>0`; `h_μ=0 ⟹ μ≠`Haar `⟹ (K)` false —
  see `LIMIT_MEASURE_ENTROPY.md`). The alternative to (ii) is resolving the zero-entropy **Furstenberg** case,
  itself `[OPEN]`.

The original lemma's "the **only** gap is AIU" **folds gap (ii) silently into Berend** — that is the
over-claim. Corrected: **(K) ⟸ AIU ∧ ( h_μ(M_2)>0 ∨ Furstenberg )**; with `h_μ(M_2)>0` the **proven** RJ
finishes; without it one is in the open zero-entropy Furstenberg regime.

### (c) Does Berend give a PROVEN topological dichotomy weaker than (K) needs? — **YES, but only for the host.**
`[PROVEN-in-lit, applies]` **(B-set)** above: every closed `Φ`-invariant subset of `X` is finite or `=X`.
This is genuine and weaker than the measure statement (K) needs (full support ≠ equidistribution ≠ Haar).

---

## 4. CORRECTED LEMMA (what survives, exactly)

> **Lemma (corrected — topological host-rigidity, `[PROVEN-in-lit]`).** On `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]` the rank-2
> host `Φ=⟨×2,×3⟩` is totally irreducible, not virtually cyclic, and contains the hyperbolic element `A=×(3/2)`;
> hence (Berend) **every closed `Φ`-invariant subset is finite or `=X`**. Consequently the **support** of any
> non-atomic `Φ`-invariant measure is **all of `X`** (full support).
>
> **What this does NOT give (`[OPEN]`).** It does **not** give `μ=`Haar. Promoting full-support to Haar needs
> **positive entropy** `h_μ(M_2)>0` (then Rudolph–Johnson, `[PROVEN-in-lit]`, finishes) **or**, entropy-free,
> Furstenberg's conjecture (`[OPEN]`). And all of this is **conditional on AIU** (`A`-invariant ⟹ `Φ`-invariant,
> `[OPEN]`), since the orbit measure is a priori only `A`-invariant.
>
> **Net:** `A`-invariance ⟶[AIU] `Φ`-invariance ⟶[h>0, RJ] Haar. **Two** independent open inputs, not one.

The single sentence to delete from `NEWMATH_ADELIC_RIGIDITY.md` §3.2 / `NEWMATH_SYNTHESIS.md` §1 /
`FURSTENBERG_CORNER_QUESTION.md` §0 is **"the only gap is AIU"** / **"`Φ`-invariant ergodic limit is forced to
be Haar or finite."** Replace with the corrected lemma above (this matches `LIMIT_MEASURE_ENTROPY.md`'s table,
which already lists AIU **and** `h_μ(M_2)>0` as the two open inputs).

---

## 5. PROVEN vs OPEN ledger

| Item | Label |
|---|---|
| `Φ=⟨×2,×3⟩` is totally irreducible, rank-2, contains hyperbolic `A` on `X` | **[PROVEN]** |
| Berend ⟹ every closed `Φ`-invariant set is finite or `=X` (host topological rigidity) | **[PROVEN-in-lit, applies]** |
| `Φ`-orbit `{2^a3^b·8}` is infinite ⟹ **dense in `X`** (rank-2 host orbit) | **[PROVEN]** (see §6) |
| `supp(μ)=X` for any non-atomic `Φ`-invariant `μ` | **[PROVEN-in-lit]** |
| Rudolph–Johnson / E–L solenoid: `Φ`-inv ergodic **+ `h_μ(M_2)>0`** ⟹ Haar | **[PROVEN-in-lit]** |
| "`Φ`-inv ergodic ⟹ Haar **without** entropy" (the lemma's measure claim) | **[OPEN]** = Furstenberg |
| §3.2 proof (Berend topological ⟹ measure=Haar) | **[OVER-CLAIMED / INVALID]** |
| Berend applies to the single `A=×(3/2)` (rank-1) | **NO** — `⟨A⟩` virtually cyclic, fails cond. (2) |
| `A`-orbit `{Aⁿ·8}` finite-or-dense | **[OPEN]** — Berend gives nothing for rank 1 |
| Gap to Haar from `A`-invariance | **TWO**: AIU `[OPEN]` ∧ `h_μ(M_2)>0` `[OPEN]` |

---

## 6. Bonus — the one genuine `[PROVEN]` topological partial (and its limit)

`[PROVEN]` **The rank-2 host orbit of `8` is dense in `X`.** `Φ·8 = {2^a 3^b·8 : a,b∈ℤ} ⊂ ℤ[1/6]` is an
**infinite** set (distinct adelic points), hence a closed `Φ`-invariant set that is not finite; by **(B-set)**
its closure is `X`. This is a real, citable consequence of Berend on the solenoid.

**But it is NOT the partial (K) would want, on two counts:**
1. It is density of the **rank-2** orbit `{2^a3^b·8}`, **not** the **rank-1** `A`-orbit `{(3/2)ⁿ·8}` that
   Antihydra actually iterates. Berend gives **no** density for the `A`-orbit (rank-1, virtually cyclic).
   So there is **no `[PROVEN]` topological-density statement for the orbit of 8 under `×(3/2)`** — the
   honest bonus answer is *negative* for the rank-1 orbit.
2. Even for the host orbit, **topological density ≠ equidistribution ≠ Haar**: a dense orbit can fail to
   equidistribute, and a full-support invariant measure can be non-Haar (zero-entropy). Density is far short
   of (K).

So the only genuinely new `[PROVEN]` topological yield is host-orbit density — interesting, weaker than (K),
and **not** a density result for the iterated `×(3/2)`-orbit.

---

## Sources

- D. Berend, *Multi-invariant sets on tori*, Trans. AMS **280** (1983) 509–532
  (https://www.ams.org/tran/1983-280-02/S0002-9947-1983-0716835-6/) — topological set rigidity; conditions
  totally irreducible + not virtually cyclic + hyperbolic element. `[PROVEN-in-lit]`
- D. J. Rudolph, *×2 and ×3 invariant measures and entropy*, ETDS **10** (1990) 395–406
  (https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/2-and-3-invariant-measures-and-entropy/64243AD8323B37089540F911F8CC77EB)
  — positive-entropy measure rigidity. `[PROVEN-in-lit]`
- A. S. A. Johnson, *Measures on the circle invariant under multiplication by a nonlacunary subsemigroup*,
  Israel J. Math. **77** (1992) 211–240. `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *Rigidity properties for commuting automorphisms on tori and solenoids*,
  arXiv:2101.11120 (https://arxiv.org/pdf/2101.11120) — solenoid form of RJ measure rigidity (positive
  entropy). `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, ETH notes *Rigidity properties of `ℤ^d`-actions on tori and solenoids*
  (https://people.math.ethz.ch/~einsiedl/RA_toralm.pdf) — Berend solenoid statement (no proper infinite closed
  invariant set ⟺ totally irreducible, not virtually cyclic, hyperbolic element). `[PROVEN-in-lit]`
- M. Einsiedler, E. Lindenstrauss, *On measures invariant under diagonalizable actions: the rank-one case*,
  JMD (2008) — rank-1 (single map) **non-rigidity**: uncountably many invariant measures/sets. `[PROVEN-in-lit]`
- M. Einsiedler, A. Fish, arXiv:0804.3586 — entropy-free rigidity needs positive-density semigroup (fails for
  `⟨2,3⟩`, density 0). `[PROVEN-in-lit]`
- H. Furstenberg, *Disjointness in ergodic theory…* (1967); survey M. Tal, arXiv:2110.05989 — the `×2,×3`
  conjecture (measure rigidity without entropy). `[OPEN]`
- Repo: `NEWMATH_ADELIC_RIGIDITY.md` §3.2 (the lemma), `NEWMATH_SYNTHESIS.md` §1/§3,
  `FURSTENBERG_CORNER_QUESTION.md` §0 (soundness banner), `LIMIT_MEASURE_ENTROPY.md` (two-input correction),
  `REPELLER_ESCAPE.md` (non-atomicity).

No machine decided. No label upgraded.
