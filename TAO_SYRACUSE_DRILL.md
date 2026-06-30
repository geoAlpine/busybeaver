# Drilling Tao 2019 at the technical level: does the Syracuse characteristic-function bound cast any shadow on our single orbit? (2026-06-30)

*Deep technical drill of T. Tao, "Almost all orbits of the Collatz map attain almost bounded values," arXiv:1909.03562
(Forum Math. Pi 10 (2022) e12). Earlier program notes recorded the CONCLUSION-level verdict
(`INDUCED_TAO_METHOD.md`, `AEV_METHODS.md` §3: "log-density over starts, gives nothing for the orbit of 27"). This
note goes a level deeper: it reads the actual quantitative input — Prop 1.17 (characteristic-function decay), its
upgrade Prop 1.14 (fine-scale mixing), and the bridge Prop 1.9 (valuation distribution) — and decides rigorously
whether the bound has ANY quenched shadow once we feed in our PROVEN structure (the 3-adic sliding lock
`Ψ((D_j))` and the 2-adic depth process). SOUNDNESS: every claim labelled. Verdict default = skepticism. No label
upgraded; `(K)` stays `[OPEN]`. NOT committed.*

---

## §0. Verdict `[PROVEN-in-scope, about the method's reach]`

**Same wall — but now located to the exact line.** Drilling Tao technically does NOT open a route and does NOT yield a
new partial. The quantitative Syracuse characteristic-function bound (Prop 1.17, superpolynomial decay `≪_A n^{-A}`)
is an expectation **over the i.i.d. depth ensemble `Geom(2)^n`**, equivalently over the log-uniform start `N`. For our
single deterministic orbit the depth sequence `(D_j)` is fixed, so that expectation degenerates to a single phase of
modulus exactly `1` — **zero decay, the bound is vacuous quenched.** The precise step where single-orbit information is
lost is **the hypothesis (1.11) of Proposition 1.9**: it requires the start `N` to be (a random variable that is)
approximately uniform `mod 2^{n_0}` with `n_0 ≥ (2+c_0)n`; this is supplied only by drawing `N` from the log-uniform
ensemble `Log(2ℕ+1 ∩ [y, y^α])`. Without it, Prop 1.9's conclusion (1.12) — that the depth vector `a^{(n)}(N)` is
`2^{-c_1 n}`-close in total variation to `Geom(2)^n` — fails to apply, and Props 1.17/1.14, whose probability space is
exactly `Geom(2)^n`, never engage. **The closest-to-quenched sub-lemma is Proposition 1.9**: it is the unique step
shaped as "finite-scale 2-adic equidistribution of the start ⟹ correct (mean-2) depth law," i.e. the exact conditional
form our program wants — but its hypothesis (1.11) *is* single-orbit 2-adic equidistribution = `(K)` / Mahler 3/2. So
the drill collapses, with full precision, to the annealed→quenched gap `= (K)`.

---

## §1. Tao's technical input, stated precisely with lemma numbers `[surveyed, verbatim from arXiv:1909.03562 v-published]`

The logical spine is `Thm 1.3 ⇐ Thm 1.6 ⇐ Prop 1.11 ⇐ {Prop 1.14, Prop 1.9}`, and `Prop 1.14 ⇔ Prop 1.17`.

- **Theorem 1.3 (main).** For any `f: ℕ+1→ℝ` with `f(N)→∞`, `Col_min(N) < f(N)` for almost all `N` **in the sense of
  logarithmic density**. (Thm 1.6 is the Syracuse-map reformulation, for a log-density-`1/2` set of odd `N`.)

- **The Syracuse random variable (eq. 1.21 / 1.26).** `Syrac(ℤ/3ⁿℤ) := F_n(Geom(2)^n) mod 3ⁿ`, explicitly
  `Syrac(ℤ/3ⁿℤ) ≡ 2^{−a_1} + 3·2^{−a_{[1,2]}} + ⋯ + 3^{n−1}·2^{−a_{[1,n]}} (mod 3ⁿ)` with `(a_1,…,a_n) ≡ Geom(2)^n`,
  `a_{[1,j]} = a_1+⋯+a_j`. **The `a_i` are i.i.d. Geometric(1/2), mean 2** — this is the entire source of randomness.

- **Proposition 1.17 (decay of characteristic function) — THE key quantitative input.** For `n ≥ 1` and `ξ ∈ ℤ/3ⁿℤ`
  **not divisible by 3**:
  > `E e^{−2πi ξ·Syrac(ℤ/3ⁿℤ)/3ⁿ} ≪_A n^{−A}` for every fixed `A > 0`, uniformly in `n` and `ξ`.  (1.25)

  This is **superpolynomial** decay of the Fourier coefficients. Proven (Section 7, "most difficult step") by pairing
  adjacent terms, conditioning on the Pascal sums `b_j = a_{2j−1}+a_{2j}` to expose an independent structure, writing
  the characteristic function as an average of products of cosines over a **two-dimensional renewal process** `v_{[1,k]}`
  in `ℤ²`, and a geometric "white/black triangle" separation argument ensuring the renewal walk meets enough
  small-cosine ("white") points.

- **Proposition 1.14 (fine-scale mixing), equivalent to 1.17 (Remark 1.18).** For `1 ≤ m ≤ n`,
  `Osc_{m,n}(P(Syrac(ℤ/3ⁿℤ)=Y))_{Y} ≪_A m^{−A}` — i.e. `d_TV(Syrac, Syrac + Unif(3^m ℤ/3ⁿℤ)) ≪_A m^{−A}`: the variable
  is approximately uniform in high-frequency (fine 3-adic) cosets. This is the "stabilisation toward uniform `mod 3ⁿ`"
  the program previously recorded; (1.17) and (1.14) are literally equivalent (Remark 1.18 derives each from the other).

- **Proposition 1.9 (distribution of the n-Syracuse valuation) — THE bridge from 2-adic equidistribution to the depth
  law.** Let `N` be a random variable on `2ℕ+1`. **Hypothesis (1.11):** there is `c_0>0` and `n_0 ≥ (2+c_0)n` with
  `d_TV(N mod 2^{n_0}, Unif((2ℤ+1)/2^{n_0}ℤ)) ≪ 2^{−n_0}` (the start is approx. uniform at 2-adic depth `n_0`, which is
  `>2×` the number of steps). **Conclusion (1.12):** `d_TV(a^{(n)}(N), Geom(2)^n) ≪ 2^{−c_1 n}` — the first `n` depth
  exponents are jointly within exponentially small TV of i.i.d. Geometric(1/2). This is what *licenses* replacing the
  real depths by `Geom(2)^n` so that Props 1.17/1.14 can be used.

- **Proposition 1.11 (stabilisation of first passage).** Using 1.14 + 1.9, the first-passage distributions of starts
  `N_{x^α}` and `N_{x^{α²}}` are `≪ log^{−c} x`-close in TV once synchronised past `x` (1.20); iterating transports
  almost all log-mass down to `O(1)`. The crucial averaging object is `N_y ≡ Log(2ℕ+1 ∩ [y, y^α])` — **the log-uniform
  measure on starting integers.**

- **Why logarithmic density is essential (Tao §1.2–1.3, eq. 1.17).** The multiplicative noise `exp(O(n^{1/2}))` in
  `Syr_n(N) = exp(O(√n))(3/4)ⁿ N` is exactly the fluctuation that natural density cannot absorb but the scale-invariant
  `1/N`-weighting can; hence the drop from Korec's natural density to log density. **All randomness is over the start
  `N`**; there is no time-average along a single orbit anywhere.

- **Tao's own annealed dictionary (Remark 1.10) — directly our object.** Tao notes that the alternative justification of
  the depth heuristic is the **Haar measure on the odd 2-adics `2ℤ₂+1`**: under Haar, `ν_2(3·Syr^j(Haar)+1)` for `j∈ℕ`
  are **i.i.d. Geom(2)**. This is *exactly* `MINIMAL_CORE_2ADIC.md`'s `(ℤ₂^×, T)` Bernoulli depth process — Tao's
  ensemble IS our annealed model, and he is explicit that he uses the start-ensemble, not a single orbit.

---

## §2. Single-orbit vs. ensemble: the exact loss point `[PROVEN-in-scope]`

**Does Prop 1.17 control the empirical 3-adic distribution of ONE specified orbit? No — only the ensemble average.**
Two equivalent ways to see the loss point, both exact:

**(a) The Fourier object degenerates under quenching.** Prop 1.17 is `E[e^{−2πi ξ S/3ⁿ}]` where the expectation is over
`S = F_n(Geom(2)^n)` — i.e. over the i.i.d. depth vector `(a_1,…,a_n)`. Our orbit's 3-adic word is, by the **PROVEN
sliding-block lock** (`THREEADIC_SLIDING_LOCK.md`), `Ψ((D_j))` with `(D_j)` the **deterministic** depth sequence of
`o_0=27` (and `Ψ` is precisely the factor-code form of Tao's offset map `F_n`). Feeding the single orbit in replaces
the random `(a_i)` by the fixed `(D_i)`, so the expectation collapses to ONE term:
`e^{−2πi ξ·Ψ((D_i))/3ⁿ}`, of modulus **exactly 1**. There is no averaging set left, hence **no decay** — the bound
`≪_A n^{−A}` becomes the trivially true but useless `|·| = 1 ≪ n^{−A}`? No: it is simply not implied, because the only
thing Prop 1.17 ever asserted was cancellation *in the mean over the ensemble*. **Quenched, the characteristic-function
bound says nothing.** (This is the Fourier-side restatement of the annealed/quenched distinction already banked in
`NONPISOT_FOURIER_CHAIN.md`: Prop 1.17 is an annealed coefficient bound, not a quenched Weyl-sum bound.)

**(b) The hypothesis of Prop 1.9 is where the start-ensemble is injected — the precise line.** Even before the Fourier
step, the depths are only `Geom(2)^n`-distributed *because of* Prop 1.9's hypothesis (1.11): `N mod 2^{n_0}` approx.
uniform, `n_0 ≥ (2+c_0)n`. This is achieved only by **drawing `N` from the log-uniform ensemble** `Log([y,y^α])`
(Prop 1.11). For our single deterministic orbit, at induced step `j` the relevant "start" is `o_j`, a **single point**,
whose residue `o_j mod 2^{n_0}` is a delta mass, the opposite of uniform; (1.11) fails outright, so (1.12) does not
fire, so `a^{(n)}` is NOT certified `Geom(2)^n`, so Props 1.14/1.17 have no probability space to act on.

**Is there any quenched re-feed?** Default skepticism confirmed. The only way to feed `o_0=27` so the chain survives is
to *supply* hypothesis (1.11) for the orbit's own iterates — i.e. to prove that `o_j mod 2^{n_0}` is approximately
equidistributed in odd classes at depth `n_0 ≳ 2j` **along the single orbit**. That statement is exactly single-orbit
2-adic equidistribution of `c_n mod 2^k` = line (5) = Mahler 3/2 = `(K)`. So the only "re-feed" is to assume the
conclusion. **No quenched survival.** `[OPEN, = (K)]`.

> **Loss point, named:** **Proposition 1.9, hypothesis (1.11).** It is the single inlet through which the
> start-ensemble (log-uniform `N`, or equivalently 2-adic Haar) is converted into the i.i.d. `Geom(2)` depth law that
> the rest of the paper (1.17→1.14→1.11) consumes. Remove the ensemble and (1.11) is the first thing that fails.

---

## §3. One-sided positive-density survival test `[PROVEN-in-scope: it collapses]`

Question: Prop 1.17 is *quantitative* (superpolynomial decay). Combined with our PROVEN facts — finite check
`balance_n ≥ 0` to `2·10⁵`; first-moment valuation budget `Σ_{i<n} D_i = n + v_2(c_n) − v_2(c_0)`; the sliding lock —
does any one-sided liminf-even-density `≥ 1/3` (equivalently `liminf` depth-mean `≥ 3/2`) consequence survive quenched?

**No. It provably collapses to the annealed→quenched gap.** Reasons, each labelled:

1. **The quantity Tao controls is orthogonal to the depth-mean.** Props 1.17/1.14 control the **3-adic spatial
   distribution** of `Syrac` *given* the depths are `Geom(2)^n`. The target `liminf (1/N)Σ D_j ≥ 3/2` is a statement
   about the **2-adic depth frequencies themselves**. Under Tao's ensemble the depth mean is `2 ≥ 3/2` automatically
   (i.i.d. Geom(2)) — it is an *input assumption* (via Prop 1.9's conclusion 1.12), **not** an output of the
   characteristic-function decay. So even the full strength of Prop 1.17 yields no lower bound on `(D_j)` frequencies it
   was not already handed. `[PROVEN-in-scope]`

2. **The decay rate cannot be ported to a single-orbit Weyl sum.** A quenched even-density bound would need cancellation
   in `S_N(t) = Σ_{j<N} e(t·(orbit phase)_j)` for the *fixed* orbit — a time/Weyl sum. Prop 1.17 bounds an *ensemble*
   coefficient `E_{Geom}[e(...)]`, a different object; converting "ensemble coefficient decay" to "single-orbit
   time-sum decay" is exactly the annealed→quenched bridge that is `(K)`. Our banked input is even sharper here:
   `ν_{2/3}`'s proven Fourier decay is only **logarithmic** (Streck / Varjú–Yu, sharp), and the Datta–Jana threshold for
   any Fourier→equidistribution bridge needs rate `> 1/2` — astronomically out of reach (`AEV_METHODS.md` correction
   banner). Prop 1.17's `n^{−A}` is decay in the *step-count of the ensemble construction*, **not** decay of the orbit's
   spectral measure, so it does not even enter the Datta–Jana ledger. `[PROVEN-in-scope]`

3. **Our PROVEN one-orbit facts are all first-moment / a.e. / topological tier and cannot lift to the second moment.**
   `Σ D_i = n + O(1)` is the *first moment* (gives `mean(D) → 2` only if the orbit doesn't escape, i.e. is itself the
   non-halt conclusion); the finite check is a bounded-time certificate; the sliding lock is a determinism statement.
   None bounds the *frequency* of low-depth times. The heavy-tailed first-moment-matched white adversary
   (`EXCURSION_SYNTHESIS.md`, `E[K²]=∞`) **halts** yet satisfies every one of these — so no proven input separates
   `o_0=27` from a halting orbit, and Prop 1.17 adds nothing on this axis. `[PROVEN-in-scope]`

**Survival test result:** the one-sided `≥1/3` consequence does **not** survive; it collapses to `(K)`. The quantitative
strength of Prop 1.17 is real but is spent entirely on the 3-adic spatial mixing *of the annealed model*, which the
sliding lock shows is a deterministic factor of the 2-adic depth process — so it carries **zero** independent leverage
over the depth-mean (consistent with `THREEADIC_SLIDING_LOCK.md` §1: the `ℚ₃` place supplies no degrees of freedom).

---

## §4. Honest net + the sub-lemma to flag for outreach `[surveyed / OPEN]`

**Net: same wall, now precisely located — not an opening, not a new partial.** The technical drill *adds value* by
pinning the failure to a single hypothesis line rather than to the vague "averages over starts": the entire
ensemble-dependence of Tao's argument funnels through **Prop 1.9 hypothesis (1.11)**, and everything downstream
(1.17, 1.14, 1.11) is conditional on the depths already being `Geom(2)^n`. The Fourier bound itself, however strong, is
annealed by construction and degenerates to modulus 1 when quenched.

**The single closest-to-quenched sub-lemma — flag for outreach: Proposition 1.9.** It is the only step in Tao's paper
with the conditional shape the program needs:
> *finite-scale 2-adic equidistribution of the start (`N mod 2^{n_0}` uniform, `n_0 ≳ 2n`)  ⟹  correct i.i.d. mean-2
> depth law `a^{(n)} ≈ Geom(2)^n` (TV `≪ 2^{−c_1 n}`).*

Two features make it the right thing to put to a 2-adic ergodic-theory / homogeneous-dynamics specialist:
- **Its hypothesis is FINITE-scale, not full Haar genericity.** It needs equidistribution only at *one* 2-adic depth
  `n_0 ≥ (2+c_0)n` (polynomially deeper than the step count), not control of every cylinder for all time. That is a
  strictly weaker, more concrete target than full single-orbit normality — and it is exactly the "effective single-orbit
  equidistribution" object (`§3.6` in the program's framing). If anyone can establish (1.11) **quenched** for the
  forward iterates `o_j` of `o_0=27` (i.e. `o_j mod 2^{n_0}` approximately uniform along the orbit, with `n_0 ≳ 2j`),
  Tao's machinery delivers the depth law — hence `liminf` mean-`D` `= 2 ≥ 3/2` — for our orbit, closing `(K)`.
- **It cleanly isolates what is and isn't conditional.** Prop 1.9 says the *only* arithmetic input the whole Collatz
  bound needs about the start is its 2-adic equidistribution at depth `~2n`; the hard 3-adic Fourier work (1.17) is
  start-agnostic. This tells outreach precisely where a single-orbit advance must land: **not** on the 3-adic side
  (inert, by the sliding lock) but on **finite-scale 2-adic equidistribution of one orbit** — `MINIMAL_CORE_2ADIC.md`'s
  irreducible object, here independently confirmed from Tao's own dependency graph.

**Caveat / why it is still `(K)` and not a loophole.** Hypothesis (1.11) for the single orbit's iterates is itself a
single-orbit 2-adic equidistribution statement, i.e. Mahler 3/2 / `(K)`. Prop 1.9 does not weaken `(K)`; it *re-expresses
the minimal needed input* and certifies that the input suffices. That re-expression is the genuine, honest yield of the
drill: the depth-law target is conditional on a **finite-depth** (`n_0 ≳ 2n`) 2-adic equidistribution of the named
orbit — the sharpest, most concrete form of the wall, and the cleanest single lemma to hand to a specialist.

**No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV Conjecture 1.6.

### Sources
- T. Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum Math. Pi 10 (2022) e12,
  arXiv:1909.03562 — https://arxiv.org/abs/1909.03562 (Thm 1.3/1.6; Prop 1.9 + hyp. (1.11)/concl. (1.12); Prop 1.11
  + (1.19)/(1.20); Prop 1.14 + (1.23); Prop 1.17 + (1.25); Remark 1.10 [2-adic Haar = i.i.d. Geom(2)]; Remark 1.18
  [1.14 ⇔ 1.17]; §7 renewal-process / white-black-triangle proof). Numbering verified verbatim from the arXiv PDF text.
- Blog: https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/
- Program cross-refs: `THREEADIC_SLIDING_LOCK.md` (3-adic = `Ψ((D_j))`, factor of 2-adic depths),
  `MINIMAL_CORE_2ADIC.md` (irreducible `(ℤ₂^×,T,o_0=27)` quenched depth-mean object), `INDUCED_TAO_METHOD.md`
  (conclusion-level prior pass), `AEV_METHODS.md` (annealed/quenched Fourier ledger, Datta–Jana threshold),
  `EXCURSION_SYNTHESIS.md` (heavy-tailed halting adversary, first-moment-indistinguishable).
