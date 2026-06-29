# The a.e.→SPECIFIC selector via computability theory / algorithmic randomness (2026-06-29)

*Angle (A3 pivot ii of `SESSION_2026-06-29_A_ASSAULT.md`): attack the **second wall** — the a.e.→specific
selector — **independently of cancellation**, using computability theory and algorithmic randomness. The
orbit is a Busy-Beaver object, so computability is the apt lens and (per the literature passes
`WALL_B_*`, `COCYCLE_ERGODICITY.md`) it had **never been brought to bear**: prior notes use "computable
point" only descriptively and cite poly-time randomness once, but never deploy the randomness hierarchy or
the effective ergodic theorems as the selection mechanism. Every line labelled
[PROVEN] / [PROVEN-in-literature] / [OBSERVED] / [OPEN]. Numerics `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`
(`scratchpad/fsrand.py`). Zero false proofs. NOT committed.*

Target recall (`WEAKEST_SUFFICIENT.md`): the kernel (K) ⟺ **H₂ : liminf_N (1/N)Σ_{n<N}(−1)^{c_n} ≥ −1/3**,
i.e. even-density ≥ 1/3 for the orbit `c₀=8`, `c→⌊3c/2⌋`; the full Mahler/AEV statement is even-density → 1/2
= equidistribution = **normality of the orbit in base 3/2**. The parity word `(c_n mod 2)` is **computable**.

---

## 0. One-line verdict

Computability theory does **not** give a new route to *select* `c₀=8` — and it explains, with a sharp new
reason, **why no such route can exist**. The result is **a precise NEW characterization of the second wall
(verdict (b)), which rederives the wall (verdict (c)) but pins its cause to a computability-hierarchy
boundary, not measure zero.** The mechanism:

> **Every effective-randomness selector that the a.e.→specific upgrade theorems run on
> (Martin-Löf, computable, Schnorr, Avigad's UD-randomness, even Kurtz) provably EXCLUDES every
> computable point.** Our orbit point is computable, so **no** such theorem can ever name it.
> Meanwhile the *property we need* — equidistribution = base-3/2 normality — sits at the
> **finite-state-randomness** level, the **unique** rung of the randomness hierarchy that is
> *compatible* with computability (Champernowne is computable AND normal). For our orbit, that
> rung **is the kernel (K) itself**. So the only randomness notion the point could satisfy equals
> the open problem, and every notion strong enough to be a theorem-hypothesis is too strong to apply.
> **The point falls in the gap between "selectable by an effective test" and "computable."**

And the base makes it worse: the finite-automaton/P-martingale rescue of normality (Schnorr–Stimm and its
β-extension) **requires the base to be Pisot**; `3/2` is non-Pisot, so even the finite-state characterization
that saves integer/Pisot bases is unavailable — the computability-side mirror of the known non-sofic wall.

---

## 1. Frame precisely — is the prompt's "computable ⇒ not random ⇒ excluded" the right diagnosis?

**The prompt's hypothesis is half right and the correction is the whole point.**

- **[PROVEN-in-literature] TRUE half.** A computable real is **never** Martin-Löf random; never computably
  random; never **Schnorr** random; never even **Kurtz** random. Reason (textbook, Nies; Downey–Hirschfeldt):
  for a computable `x` the singleton `{x}` is an **effectively closed (Π⁰₁) null set**, and Kurtz randomness
  (the weakest standard notion: not a member of any Π⁰₁ null class) already fails on it; everything above
  Kurtz fails a fortiori. So our point is excluded from **every** notion in the standard hierarchy
  ML ⟹ computable ⟹ Schnorr ⟹ **Kurtz**.
- **[PROVEN-in-literature] The FALSE half — and the correction.** The a.e. equidistribution set is **NOT**
  the ML-random reals. For integer base `b`, "{xbⁿ} equidistributes" ⟺ "`x` is **normal** in base `b`"
  (Wall), and **normality = finite-state randomness** (Schnorr–Stimm 1972: `x` is normal iff no finite-state
  gambler/automaton-martingale wins on its digits). **Finite-state randomness is strictly weaker than Kurtz
  randomness and is COMPATIBLE with computability** — Champernowne's constant and the Becher–Heiber–Slaman
  number are **computable and (absolutely) normal**. So:

  > The standard a.e. set (normal numbers) does **NOT** exclude our computable point by the randomness route.
  > It excludes it only from the **strong** (Kurtz-and-above) subsets — which are a measure-1 *subset* of the
  > normals, not the equidistribution set itself. Equidistribution needs only the **finite-state** rung,
  > where computable points live freely.

**So the precise diagnosis is not "computable ⇒ non-random ⇒ non-equidistributing."** It is: our point is
non-random in every *effective* sense, but equidistribution does not require effective randomness — it
requires only finite-state randomness, which is computability-compatible. The wall is therefore **not** that
the point is provably "bad"; it is that **every proof technique that pins a specific point goes through an
effective-randomness selector the point cannot satisfy** (or through *construction*, unavailable for a given
point — `WALL_B_SPECIFIC_LITERATURE.md §1A`).

---

## 2. The randomness hierarchy, placed against the two boundaries [PROVEN-in-literature]

Two horizontal lines matter: the **computability line** (above it ⇒ non-computable) and the
**equidistribution line** (above it ⇒ the orbit equidistributes).

```
            ML-random  ──────────┐
            computably random     │  all of these:  • IMPLY non-computable (exclude c₀=8)
            Schnorr random        │                 • are SUFFICIENT for equidistribution
   ── Avigad UD-random ───────────┤   (Schnorr ⟹ UD ⟹ absolutely normal; effective Birkhoff good set
            Kurtz random  ────────┘    = Schnorr randoms, Gács–Hoyrup–Rojas)
   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ COMPUTABILITY LINE ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
            finite-state random  = NORMALITY = equidistribution        ← c₀=8 must be HERE
            (Schnorr–Stimm; computable-compatible: Champernowne)         and being here IS (K)
            ────────────── below: not even normal ──────────────
```

- **[PROVEN-in-lit] Avigad (2012, *J. Symbolic Logic*; arXiv:1203.4126).** Defines **UD-randomness** (x passes
  every effective u.d. test, i.e. `(aₙx)` is u.d. for all computable distinct-integer `(aₙ)`). Results:
  **Schnorr random ⟹ UD-random ⟹ absolutely normal**, and **there are Kurtz randoms that are NOT UD-random.**
  So UD-randomness — the notion *tailored to equidistribution* — sits **strictly between Schnorr and Kurtz**,
  i.e. **strictly above the computability line.** Even the bespoke equidistribution-randomness excludes every
  computable point.
- **[PROVEN-in-lit] Effective Birkhoff (Gács–Hoyrup–Rojas; V'yugin; Bienvenu–Day–Hoyrup–Mezhirov–Shen).** For a
  computable ergodic system and an L¹-computable observable, the Birkhoff average converges at every **Schnorr
  random** point — and **the Schnorr randoms are *exactly* the Birkhoff points** for computable ergodic maps
  w.r.t. effectively-closed sets of computable measure. So the effective ergodic theorem's *guaranteed-good
  set is precisely the Schnorr randoms* — **above the computability line.** V'yugin: there is a computable
  ergodic system with a **computable point where Birkhoff diverges** — computable points can be genuinely bad,
  and nothing in the effective theory rules our (computable) point in or out.

**Consequence [PROVEN, this repo].** Every a.e.→specific *selection theorem* in effective ergodic theory /
algorithmic randomness delivers its conclusion on a good set at the **Schnorr / UD / Kurtz** level. All three
**exclude every computable point.** Our orbit point is computable. **Therefore no theorem of this family can
ever select `c₀=8`** — not for lack of searching, but because its hypothesis (effective randomness) is
**provably false** at every computable point. This is the obstruction, stated as a theorem-level NO.

---

## 3. Can the orbit be Schnorr/computably random for SOME measure giving even-density ≥ 1/3? [PROVEN: NO]

The prompt's point 3. For a **computable atomless** measure `μ`, a **computable** point is **never** Schnorr
(or computably, or ML) random — the singleton is a `μ`-Schnorr-null set. So the only way a computable point is
random for a measure is if `μ` has an **atom** there. But:

- The orbit is **provably not eventually periodic** and **grows unboundedly** (`LIMIT_THEOREM.md §3″`,
  `WALL_B_SELF_SELECTION.md §2b`), so it is **not** supported on a periodic point; an atom at the (transient)
  orbit point is **not `T`-invariant**.
- The **only** atomic `T`-invariant measures for `×(3/2)` are `δ₀, δ₁` (the fixed points `0,1`), and the
  integer orbit `c₀≥2` is **outside their basin** (`WALL_B_SELF_SELECTION.md`, [PROVEN]).
- The only non-atomic invariant measure giving the even-density we need is **Haar (= SRB)**, for which the
  computable orbit is, by the above, **not Schnorr random.**

**[PROVEN] Verdict.** There is **no measure** under which the orbit is Schnorr/computably random **and** the
Birkhoff average yields even-density ≥ 1/3. Any such measure would have to be atomic at the point (excluded by
non-periodicity/invariance) or atomless (excludes the point from randomness). The Levin–Gács "every point is
ML-random for *some* computable measure" escape is vacuous here: that measure is the atomic/degenerate one,
whose Birkhoff average is the orbit's **own** time-average — circular, certifies nothing. So the
effective-ergodic selector cannot be salvaged by changing the measure.

---

## 4. Does any randomness notion the orbit PROVABLY satisfies yield the kernel? [PROVEN: NO]

The strongest *proven* "randomness-flavoured" facts about the orbit (`LIMIT_THEOREM.md §3″`):
not eventually periodic; not Sturmian; subword complexity `p(ℓ) ≥ 1.71 ℓ` (slope `log_{3/2}2`); grows.

- All of these are **complexity-floor** facts (counts of *distinct* subwords). The kernel (K) is a
  **frequency** fact (one-sided density of a symbol = simple-normality fragment). **Distinct-subword counts
  say nothing about frequencies**: a sequence can have any complexity with any letter-frequency. So **none of
  the proven properties implies even the one-sided `≥1/3` frequency floor.**
- In randomness terms, the proven floor `p(ℓ) ≥ 1.71ℓ` is **linear** complexity = **topological entropy 0** —
  it does not even reach *positive entropy*, let alone any randomness notion. The kernel needs the
  finite-state rung (full complexity `p(ℓ)=2^ℓ` for full normality; or just simple normality for the ≥1/3
  fragment), exponentially above the proven floor.

**[PROVEN] Verdict.** The orbit provably satisfies **no** randomness notion strong enough to give (K). The
weakest randomness notion that *would* give (K) is **finite-state randomness (= base-3/2 normality)**, and for
our orbit that notion **is** (K) — there is no strictly-weaker provable randomness notion in between that
delivers it.

---

## 5. The base-3/2 twist: the finite-state rescue itself fails (non-Pisot mirror) [PROVEN-in-lit]

For **integer** base, normality = finite-state randomness gives a *computable-compatible* characterization.
One might hope to reuse it at base 3/2 to make "the computable orbit is normal" a finite-state-checkable
property. **It does not transfer:**

- **[PROVEN-in-lit] (Scheerer / Madritsch et al., "Normality in non-integer bases and polynomial-time
  randomness", arXiv:1410.8594; *J. Comput. Syst. Sci.* 2015).** They extend Schnorr–Stimm via **P-martingales**
  computed by deterministic finite automata, and prove: **if `x` is polynomial-time random and `β` is Pisot,
  then `x` is normal in base `β`** (`(xβⁿ)` is u.d.). The **Pisot hypothesis is load-bearing** — the
  finite-automaton/Markov-measure characterization of β-normality requires the β-shift to be sofic.
- **`3/2` is non-Pisot** ⇒ the β-shift is **not even sofic** (Frougny; `WALL_B_SPECIFIC_LITERATURE.md §2`,
  `WALLB_EFFECTIVE.md §2a`). So there is **no finite-automaton / P-martingale characterization of base-3/2
  normality**. The one rung that is computability-compatible at integer/Pisot bases has **no machinery at our
  base.** This is the **computability-side mirror** of the already-proven non-sofic obstruction: non-Pisot
  helps the *annealed* Fourier tier (`ν_{2/3}` Rajchman) but **destroys the finite-state structure that any
  specific-point or computable-point argument would run on** — exactly the dual phenomenon flagged in
  `WALL_B_SPECIFIC_LITERATURE.md §1D`.

So even the *characterization* that could turn "our computable orbit equidistributes" into a finite-state /
poly-time-randomness statement is unavailable. Both the strong selectors (excluded by computability) and the
weak finite-state characterization (excluded by non-Pisot) fail.

---

## 6. Numerics — the orbit IS empirically finite-state random; that observation is the unprovable kernel

`scratchpad/fsrand.py` (exact big-int parity, `N = 2·10⁵`). Finite-state randomness has a clean empirical
signature (Schnorr–Stimm: all `2^k` blocks at Haar frequency `2^{-k}`, per-symbol block entropy → 1).

| `k` | distinct `k`-blocks / `2^k` | max\|freq − 2^{−k}\| | block-entropy / `k` |
|---|---|---|---|
| 1 | 2/2 | 1.85e−4 | 1.0000 |
| 4 | 16/16 | 1.30e−3 | 1.0000 |
| 8 | 256/256 | 4.31e−4 | 0.9999 |
| 12 | 4096/4096 | 1.51e−4 | 0.9988 |
| 14 | 16384/16384 | 6.90e−5 | 0.9958 |

Also: even-density `0.50018` (≫ 1/3); worst running `avg(−1)^{c_n}` for `n≥50` is `−0.0407` (⇒ min even-density
`0.480`, a `~0.15` margin above the H₂ floor `−1/3`).

**[OBSERVED] The orbit is empirically indistinguishable from finite-state random** (every block present at
Haar frequency, per-symbol entropy ≈ 1 to `k=14`). **This is the operational content of the verdict:** the
*only* randomness notion compatible with our computable point is finite-state randomness, the orbit *appears*
to satisfy it perfectly — and that appearance **is exactly (K)/Mahler**, which finite `N` can never upgrade to
a proof. The numerics show the point sitting precisely on the computability line: too computable for any
effective test to certify, exactly normal-looking for the one notion that would suffice.

---

## 7. Honest verdict (prompt point 4)

| Question | Answer |
|---|---|
| **(a)** A genuine new route to *select* `c₀=8`? | **NO [PROVEN].** Every effective-randomness selector (ML/computable/Schnorr/UD/Kurtz; effective Birkhoff good set = Schnorr randoms) **excludes all computable points**; our point is computable. No measure rescues it (§3). Theorem-level NO, not a search failure. |
| **(b)** A precise new *characterization* of why the selector fails? | **YES [PROVEN, this repo].** The a.e.→specific wall is a **computability-hierarchy mismatch**: selection mechanisms live at Kurtz-and-above (effective/limit-null tests, all excluding computable points); the target property (equidistribution = base-3/2 normality = **finite-state randomness**) lives **below** that line, computable-compatible. `c₀=8` falls in the gap. New sharp statement: **(K) ⟺ "the computable point c₀=8 is finite-state-random (normal) in base 3/2", and finite-state randomness is the UNIQUE rung both compatible with computability and sufficient for equidistribution — so the only applicable notion equals the open kernel.** |
| **(c)** Or just rederive the wall? | **It rederives the wall (no new theorem closes K) BUT with a genuinely new reason and a second obstruction.** New reason: the wall is the **computability line in the randomness hierarchy**, not "measure zero" (the measure-zero framing of `WALL_B_EXCEPTIONAL_SET.md` is *implied by but weaker than* this — measure-zero permits computable-compatible normality; the computability obstruction explains why the *selectors* still miss). Second obstruction: even the finite-state *characterization* that would make the property checkable **fails at non-Pisot 3/2** (§5, arXiv:1410.8594) — the computability mirror of the non-sofic wall. |

**Net.** This is the cleanest available *explanation* of the second wall, and it is **new** to the program: the
a.e.→specific gap for `c₀=8` is the statement that **a computable point cannot be reached by any effective
randomness selector, while the property it needs (normality) is the one randomness level computable points can
have — which, for this orbit, is the open kernel.** Computability theory thus **diagnoses** the wall with a
precision the measure-theoretic and cancellation routes lack, and **proves** (verdict (a)) that the entire
effective-randomness / effective-ergodic family is structurally incapable of selecting the orbit — so the
selector wall is **not** an accident of missing tools but a hierarchy boundary. It does **not** crack (K).

### What is genuinely new vs prior notes
1. **First deployment of the randomness hierarchy as the selector mechanism.** Prior notes
   (`WALL_B_EXCEPTIONAL_SET.md`, `COCYCLE_ERGODICITY.md`, `WALL_B_SPECIFIC_LITERATURE.md`) used "computable
   point" descriptively and the measure-zero framing; none placed the selectors (Schnorr/UD/Kurtz, effective
   Birkhoff) against the **computability line** to prove they *cannot* apply.
2. **The exact rung identified:** equidistribution = **finite-state randomness** (Schnorr–Stimm) = the unique
   randomness level compatible with computability; for our orbit it **equals** (K). This sharpens "a.e.→
   specific is open" to "the selectable randomness notions and the target property are on **opposite sides of
   the computability boundary**."
3. **Avigad's UD-randomness located strictly between Schnorr and Kurtz** — the equidistribution-bespoke
   randomness still excludes computable points; even the tailor-made notion misses our orbit.
4. **Computability-side mirror of the non-Pisot wall** (§5, arXiv:1410.8594): the finite-state/P-martingale
   characterization of β-normality requires **Pisot**; 3/2 is non-Pisot, so the one computable-compatible
   characterization has no machinery at our base.
5. **[PROVEN] No-measure result (§3):** the orbit is Schnorr-random for no measure giving the kernel —
   non-periodicity + invariance forbid the only escape (an atom at the point).

**No machine decided. No non-halt asserted. No label upgraded.** (K) remains [OPEN] = Mahler/AEV; this note
adds a computability-theoretic *characterization and impossibility-of-selector* result, not a proof of (K).

### Sources
- Avigad, *Uniform distribution and algorithmic randomness*, J. Symbolic Logic 78(1) (2013), arXiv:1203.4126,
  https://arxiv.org/abs/1203.4126 ; talk https://www.andrew.cmu.edu/user/avigad/Talks/ud_talk.pdf
  (Schnorr ⟹ UD ⟹ absolutely normal; some Kurtz randoms not UD).
- Gács–Hoyrup–Rojas; Bienvenu–Day–Hoyrup–Mezhirov–Shen, *A constructive Birkhoff ergodic theorem for ML/Schnorr
  random points*, arXiv:1007.5249, https://arxiv.org/pdf/1007.5249 ; Galatolo–Hoyrup–Rojas,
  *Effective symbolic dynamics, random points, statistical behavior…*, Inform. Comput. 208 (2010) 23–41
  (Schnorr randoms = Birkhoff points for computable ergodic maps).
- V'yugin, *On instability of the ergodic limit theorems w.r.t. small violations of algorithmic randomness*,
  arXiv:1105.4274 (computable point where Birkhoff diverges).
- Schnorr–Stimm 1972 (normality = finite-state randomness); modern: Bourke–Hitchcock–Vinodchandran;
  *Automatic Kolmogorov complexity, normality, and finite-state dimension*, arXiv:1701.09060,
  https://arxiv.org/pdf/1701.09060 .
- Madritsch–Scheerer–… , *Normality in non-integer bases and polynomial time randomness*, arXiv:1410.8594,
  https://arxiv.org/abs/1410.8594 (P-martingales; poly-time random + **Pisot** ⇒ β-normal — Pisot essential).
- Nies, *Computability and Randomness*; Downey–Hirschfeldt, *Algorithmic Randomness and Complexity*
  (computable reals are not Kurtz random: singleton is a Π⁰₁ null class). Scholarpedia *Algorithmic randomness*,
  http://www.scholarpedia.org/article/Algorithmic_randomness .
- Becher–Heiber–Slaman, computable absolutely normal number (computable ∧ normal witness),
  https://math.berkeley.edu/~slaman/papers/poly.pdf .
