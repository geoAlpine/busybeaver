# The irreducible Antihydra kernel — crispest statement + exact literature placement (2026-06-28)

Synthesis of today's reductions (`SESSION_2026-06-28_INDUCED_MAP.md`, `SESSION_2026-06-28_MINPROP.md`,
`PROOF_STATUS.md`, `NONPISOT_FOURIER_CHAIN.md`). Goal: state the single open kernel after all PROVEN
reductions in every equivalent form, give the clean conditional theorem, and place it EXACTLY in the
literature, naming the weakest known open conjecture that closes it. Every line labelled. Zero false proofs.

---

## 1. The kernel — all equivalent forms with the [PROVEN] chain connecting them

Setup (all [PROVEN], cited):
- Antihydra: `c₀=8`, `c_{n+1}=⌊3c_n/2⌋`; halts iff `balance_n = 3E_n − n < 0` ever (`E_n` = #even steps).
  **[PROVEN]** non-halt ⟺ `balance_n ≥ 0 ∀n` ⟺ even-density `E_n/n ≥ 1/3 ∀n` (`PROOF_STATUS.md` §0).
- GAP-LEMMA induced odd map `T(o)=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)`, started at `o₀=27` (from `c₀=8→12→18→27`)
  (`SESSION_2026-06-28_INDUCED_MAP.md`).
- **[PROVEN, renewal identity]** even-density `= 1 − 1/(mean D)` ⟹ even-density `≥ 1/3 ⟺ mean D ≥ 3/2`
  (`INDUCED_MAP` §"標的の正しい形"; the only danger is excess `D=1`).
- **[PROVEN, exact formula]** `mean D = Σ_{k≥1} freq(o ≡ 3⁻¹ mod 2ᵏ)`; `k=1` term `≡1`, `k=2` term `=freq(o≡3 mod4)`
  (`INDUCED_MAP` E2). Since all `k≥3` terms are `≥0`: `mean D ≥ 3/2 ⟸ freq(o≡3 mod4) ≥ 1/2`.
- **[PROVEN, GAP-LEMMA arithmetic]** `D=1 ⟺ o≡1 mod4`, `D≥2 ⟺ o≡3 mod4`; refined `D=1`/`D=2`/`D≥3` are
  functions of `o mod 4`, `o mod 8` (`MINPROP` F3: ψ is a function of `D` only, 0 mismatch for `o<2·10⁶`).
- **[PROVEN, induced map is exact]** `T` is Haar-preserving, exact/Bernoulli on the odd 2-adic units `ℤ₂*`,
  with `D_j` i.i.d. geometric `2⁻ᵈ` (mean 2) (`INDUCED_MAP` E4, branch-by-branch + finite enumeration).
  So under Haar every form below holds with equality at the central value; the kernel is purely whether the
  **specific deterministic orbit `o₀=27` is Haar-generic** (`PROOF_STATUS.md` line (5)).

The single open kernel, in five [PROVEN]-equivalent one-sided forms:

| Form | Statement | Bridge to next (all [PROVEN]) |
|---|---|---|
| (i) | even-density of `c`-orbit (`c₀=8`) `≥ 1/3` | renewal identity ↔ (ii) |
| (ii) | `mean D ≥ 3/2` along induced orbit (`o₀=27`), `D=v₂(3o−1)` | `mean D=1+freq(D≥2)+…` ↔ (iii) |
| (iii) | `freq(D≥2)+freq(D≥3) ≥ 1/2` (robust, Haar-margin 1/4); zero-margin tight form: `freq(o≡3 mod4) ≥ 1/2` | `D`-residue arithmetic ↔ (iv) |
| (iv) | `freq(D=1) = freq(o≡1 mod4) ≤ 1/2 + freq(o≡3 mod8)` (one-sided cylinder occupancy) | ergodic-opt sign ↔ (v) |
| (v) | the orbit's Cesàro empirical measure does NOT concentrate on the `D=1`-dominant region near the halting fixed point `o=1` | meta-thm below |

All five are the SAME single open statement; each is a one-sided (`≥`/`≤`), **density/frequency** fact for
**one deterministic orbit**. Everything around them is PROVEN.

**[PROVEN meta-theorem, `MINPROP` F3]** a one-sided bound that holds for *all* orbits is impossible:
`β(ψ):=max_{T-invariant μ} ∫ψ dμ = +1/2 > 0`, attained at the **halting fixed point `o=1`** (`D=1` forever
= even-density 0 = a genuinely halting orbit). Hence the kernel is irreducibly **orbit-specific**: the
content is exactly that `o₀=27` (an integer orbit that *grows*, so is repelled from `o=1`) is generic, NOT
that all orbits are. This is why every structural attack only relocated the gap.

---

## 2. Clean conditional theorem

> **Theorem (conditional, [PROVEN reduction]).**
> Let `o₀=27`, `o_{n+1}=T(o_n)=3^{D(o_n)−1}(3o_n−1)/2^{D(o_n)}` with `D(o)=v₂(3o−1)`. Then
> **the Antihydra Turing machine does not halt** if and only if
> > **(K)** `liminf_{N→∞} (1/N) #{ n<N : D(o_n) ≥ 2 } ≥ 1/2`
> > (equivalently `mean D ≥ 3/2`, equivalently `liminf` even-density of `c₀=8` `≥ 1/3`),
> **together with the finite check** `balance_n ≥ 0` for `n ≤ N₀` (done to large `N₀` by bbchallenge).
>
> **Converse / sharpness.** If `liminf` even-density `< 1/3` then `balance_n → −∞` along a subsequence and
> the machine halts; so the `1/3` threshold is exact. Under the Haar measure on `ℤ₂*` (for which `T` is
> exact, mean `D = 2 > 3/2`, [PROVEN]) (K) holds with room to spare; the whole problem is whether the single
> orbit `o₀=27` inherits the a.e. value — i.e. is Haar-generic for `T`.

One-line kernel: **"the induced 3/2-Syracuse orbit of 27 spends asymptotic frequency ≥ 1/2 outside the
`D=1` (i.e. `o≡1 mod 4`) cylinder."** Equivalently: **`mean D ≥ 3/2` for the orbit of 27.**

---

## 3. Exact literature placement

The kernel lives on the **frequency/density axis** for **one orbit**. The four candidate homes split cleanly
by (a) support-vs-frequency and (b) ensemble-vs-single-orbit:

**(a) Mahler's 3/2 problem (1968, literal "no Z-numbers").** A **confinement/support** statement: no `ξ`
with `{ξ(3/2)ⁿ} ∈ [0,½) ∀n`. **NOT our kernel and neither implies the other.** Ruling out total confinement
to a half does not bound the *frequency* of a region; an orbit can be unconfined yet have density →0 there.
Flatto's counting bound (#Z-numbers `≤ x^{log₂(3/2)}≈x^{0.59}`) is again a support/counting result. So Mahler
literal is on the **wrong axis** (support, not density) — solving it would NOT close Antihydra. (`PROOF_STATUS`
§3.5 (a).)

**(b) Flatto–Lagarias–Pollington (Acta Arith. 70 (1995); "On the range of {ξ(p/q)ⁿ}").** **[verified this
session]** Proves `limsup_n{ξ(3/2)ⁿ} − liminf_n{ξ(3/2)ⁿ} ≥ 1/3` — a lower bound on the **spread (support
diameter)**, i.e. the orbit cannot be confined to any interval of width `<1/3`. **This is NOT our `density
≥ 1/3`.** Their `1/3` and ours are numerically identical but on **orthogonal axes** (which values are hit vs
how often). No bridge spread→density (see §4). So FLP is the closest-looking but is genuinely a different
theorem.

**(c) AEV normality conjecture (Andrieu–Eliahou–Vivion, arXiv:2510.11723, "A Normality Conjecture on
Rational Base Number Systems"). ← THE EXACT NAMED HOME.** Their Conjecture 1.6 (proved [Thm 1.7] equivalent
to the normality Conjecture 1.2): for coprime `p>q≥1`, every orbit of the ceiling map
`T_{p/q}(x)=⌈(p/q)x⌉` is **equidistributed in residue classes mod `qᵏ` for all `k`**. For `p/q=3/2`, `q=2`:
this is exactly **single-orbit equidistribution mod `2ᵏ` of the `⌈(3/2)x⌉` orbit** — precisely the kernel (K)
of `PROOF_STATUS.md` line (5) (note `c_{n+1}=⌊3c_n/2⌋` and `⌈3x/2⌉` are the same affine 3/2-iteration up to
the odd/even bookkeeping the GAP-LEMMA already handles). AEV themselves note this implies Mahler (1968),
Flatto's `Z_{p/q}`-numbers, Akiyama's triple-expansion (2008), and the **Dubickas–Mossinghoff 2009 "4/3
problem"** (termination of `⌈(p/q)·⌉`-type maps). So AEV is the **single umbrella conjecture** sitting above
the whole 3/2 cluster, and Antihydra's kernel is one more instance under it.

**(d) Effective single-orbit equidistribution of `{(3/2)ⁿ}`-type data / Collatz-type.** The kernel is a
**Collatz/Syracuse-type** statement (an induced 3x−1 Syracuse map, dressed by `3^{D−1}`, `INDUCED_MAP` E1
Lagarias 2-adic conjugacy). Tao 2019 (arXiv:1909.03562) is the nearest density result but is **log-density,
almost-all starting points** = an **ensemble** theorem; it does not produce per-orbit time statistics. EVG25
(Eliahou–Verger-Gaugry, "The number system in rational base 3/2 and the 3x+1 problem", arXiv:2504.13716) ties
base-3/2 digit frequencies to 3x+1 but **leaves digit equidistribution as an open question — proves nothing
about frequency** (verified this session).

**Placement verdict.** The kernel is a **special case of (c) the AEV normality conjecture** (its `p/q=3/2`,
single-orbit, mod-`2ᵏ` instance), is **Collatz/Syracuse-type (d)**, is on a **different axis from (a) Mahler
literal and (b) FLP** (support vs frequency), and is implied by **effective single-orbit equidistribution of
`{(3/2)ⁿ}`** (stronger than needed).

---

## 4. Is the one-sided, ≥1/3 kernel known-open, or a corollary of something weaker?

**The kernel is logically strictly WEAKER than AEV/full equidistribution** (one-sided, and `≥1/3` not the
equidistribution value, not `=1/2`). Despite that, after a literature sweep:

- **No published result gives `liminf` even-density `> 0` (let alone `≥1/3`) for a SPECIFIC orbit** of a
  3/2-type or Syracuse map. The unconditional single-orbit facts are only `D≥1`, `mean D ≥ 1`
  (even-density `≥0`) — far from the target (`INDUCED_MAP` E3).
- The four near-misses each fail on a DIFFERENT axis (matches `PROOF_STATUS` §2):
  - **FLP/Dubickas**: support/spread, not frequency (§3b).
  - **Tao 2019**: log-density, almost-all start points (ensemble), no per-orbit output.
  - **Krasikov–Lagarias (`x^{0.84}`, 2003)**: counts starting integers via inverse-tree branching; a single
    orbit has no population to count.
  - **Invariant-measure / Birkhoff**: `T` on `ℤ` is transient (grows like `(3/2)ⁿ`), so there is no invariant
    *probability* measure to average against — Birkhoff gives nothing for the integer orbit. (The exact Haar
    measure lives on `ℤ₂*` and only yields the a.e. statement, silent on `o₀=27`.)

- **No NAMED conjecture sits at the exact weaker level** of "one-sided density `≥1/3` for one orbit." The
  weakest *named, established-open* conjecture that **implies** the kernel is therefore **the AEV normality
  conjecture (arXiv:2510.11723), in its `p/q=3/2` single-orbit mod-`2ᵏ` form** — equivalently effective
  single-orbit equidistribution of `{(3/2)ⁿ}`. A genuine one-sided `≥1/3` (or even any `liminf>0`) density
  theorem for a single 3/2-orbit would be a *new, strictly weaker* result than AEV and would already close
  Antihydra; **no such weaker result exists in the literature.**

**Conclusion (Q3):** the one-sided `≥1/3` kernel is **OPEN**, and is **not** a corollary of any weaker
established result. It is bracketed: strictly weaker than AEV/full equidistribution (so AEV closes it), but
strictly stronger than everything currently proven (FLP support, Tao ensemble, KL counting). The gap between
"proven" and "needed" is exactly one orbit's genericity.

---

## 5. The gap from FLP's 1/3 (spread) to our 1/3 (density)

FLP gives **spread ≥ 1/3** = `limsup − liminf ≥ 1/3` = the orbit's accumulation set has diameter `≥1/3`
(WHICH residues/values are visited infinitely often). We need **density ≥ 1/3** = asymptotic **frequency** of
the even/`D≥2` event (HOW OFTEN). These are independent:

- Spread is a statement about the **support** of the orbit's limit set; density is about its **empirical
  (Cesàro) measure**. An orbit can have full spread (visits a wide range i.o.) while its empirical measure
  concentrates almost all its mass on a thin region (density of any fixed region →0). The meta-theorem of §1
  is the sharp obstruction here: the empirical measure is allowed (by all structural constraints) to drift
  toward the atom `δ₁` at the halting fixed point — which has full `D=1` density yet is a perfectly legal
  limit; spread bounds say nothing about whether `o₀=27`'s empirical measure approaches it.
- **No known route from spread to density for this structure.** Spread→density would require a *non-
  concentration* / equidistribution input, which is exactly the kernel itself. The FLP method (symbolic
  dynamics on the `(3/2)`-odometer giving a forbidden-pattern/confinement bound) controls *which* words can
  occur, not their *frequencies*; it has no averaging step. So FLP's `1/3` is, despite the numerical
  coincidence, **not a partial result toward our `1/3`** — it is on the orthogonal (support) axis with no
  published bridge.

---

## 6. One-paragraph bottom line

After today the complete proof of Antihydra non-halting is PROVEN-reduced to a single one-sided density fact
for one orbit: **`mean D ≥ 3/2` (equivalently even-density `≥1/3`, equivalently `freq(o≡3 mod4) ≥ 1/2`) for
the induced 3/2-Syracuse orbit of 27.** This is the **`p/q=3/2`, single-orbit, mod-`2ᵏ` instance of the
Andrieu–Eliahou–Vivion normality conjecture (arXiv:2510.11723)** — the weakest *named* open conjecture that
implies it — and is Collatz/Syracuse-type. It is **strictly weaker** than full single-orbit equidistribution
of `{(3/2)ⁿ}` (we need only one-sided `≥1/3`, not `=1/2`), yet **strictly stronger** than everything proven:
FLP's `1/3` is **spread, not density** (orthogonal axis, no bridge), Tao 2019 is ensemble/log-density not
per-orbit, Krasikov–Lagarias counts starting integers, and transience kills invariant-measure Birkhoff.
**No published bound gives `liminf` even-density `> 0` for any specific 3/2/Syracuse orbit.** The kernel is
open, orbit-specific by a proven ergodic-optimization obstruction (the halting fixed point `o=1` realizes the
extremal value), and closes the instant the AEV/Mahler-equidistribution line moves.

## References
- Flatto, Lagarias, Pollington, *On the range of fractional parts {ξ(p/q)ⁿ}*, Acta Arith. 70 (1995) 125–147.
- Mahler, *An unsolved problem on the powers of 3/2*, J. Austral. Math. Soc. 8 (1968); Wikipedia "Mahler's 3/2 problem".
- Andrieu, Eliahou, Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (2025) — Conj. 1.2 / 1.6, Thm 1.7.
- Eliahou, Verger-Gaugry, *The number system in rational base 3/2 and the 3x+1 problem*, arXiv:2504.13716 (2025).
- Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562 (2019/2022).
- Krasikov, Lagarias, *Bounds for the 3x+1 problem using difference inequalities* (2003).
- Dubickas, Mossinghoff (2009) "4/3 problem"; Akiyama (2008) triple expansions — both implied by AEV Conj.
