# AEV_METHODS — mining arXiv:2510.11723 and its bibliography for an analytic handle

Target reduction (all else PROVEN): Antihydra non-halting ⇐ a ONE-SIDED single-orbit
equidistribution statement for the 3/2-Syracuse map:

    liminf even-density of the orbit of 27  >=  1/3.

In the AEV language this is the mod-2 (q=2) case of their equidistribution conjecture,
i.e. liminf frequency of an even letter in the minimal/maximal word of base 3/2 >= 1/3.
We only need >= 1/3, NOT full equidistribution (which would give 1/2).

Scope of this note: extract AEV's proof machinery (proven vs motivational), find any
partial / one-sided / density / conditional result in AEV or its references usable for a
SPECIFIC 3/2-orbit, decide whether any unconditional liminf even-density > 0 exists for a
specific orbit, and name the single most promising analytic technique.

================================================================================
1. AEV's PAPER AND ITS PROOF METHODS
================================================================================

Paper: M. Andrieu, S. Eliahou, L. Vivion, "A Normality Conjecture on Rational Base
Number Systems", arXiv:2510.11723 (v1 Oct 2025, v2 Apr 2026).

Central object: normality of the "minimal" / "maximal" words wmin_{p/q}, wmax_{p/q}
attached to the rational-base p/q numeration tree (Akiyama–Frougny–Sakarovitch theory).

CRUCIAL FRAMING FOR US — Theorem 1.7 + Conjecture 1.6:
  Conjecture 1.6: for every n>0, the orbit (T_{p/q}^l(n))_l is equidistributed in
  residue classes mod q^k, for all k, where T_{p/q}(x)=ceil(p x / q).
  Theorem 1.7 [PROVEN]: Conjecture 1.6 (equidistribution) <=> Conjecture 1.2 (normality
  of minimal/maximal words).
  => For p/q = 3/2, mod 2, this is EXACTLY our object. AEV CONJECTURE it (with a
     two-sided density 1/2). They do NOT prove it, nor any one-sided weakening.

What AEV actually PROVES — methods are ELEMENTARY / STRUCTURAL, not analytic:
  - Thm 1.5 [PROVEN]: if all minimal words (p<q^2) are normal then Z_{p/q}-numbers do
    not exist. Method: proof by contradiction + a polynomial inequality
    p^2 - q(q-1)p - q^2(q-1) > 0. (combinatorics, no analysis)
  - Thm 1.7 [PROVEN]: normality <=> equidistribution. Method: an explicit measure-
    preserving bijection f: Z/q^l Z -> {0,..,q-1}^l. (pure combinatorics on words)
  - Props 2.2/2.4/2.6/2.7 [PROVEN]: language is prefix-closed/right-extendable;
    valuation bijective & order-preserving; extension letters depend only on residue
    mod q^l; breadth-first edge sequence is p-periodic. Method: modular arithmetic +
    the "modified division algorithm" a_k <- (q n) mod p, n <- floor(q n / p).
  - Prop 3.10 [PROVEN]: normality => Akiyama's "at most two expansions" conjecture
    (disjoint alphabets {0..q-1} vs {p-q..p-1}). Method: symbolic/alphabet overlap.
  - Prop 3.13 [PROVEN]: equidistribution => Dubickas–Mossinghoff "4/3 problem"
    termination (all letters appear). Method: residue-class coverage.

What is ONLY MOTIVATIONAL (computer-assisted, no theorem):
  - Conj 1.2 / 1.6 (normality / equidistribution) supported ONLY by numerical
    experiments (Section 4): 139 words up to 10^6 letters, 40,000 words up to 10^5;
    richness thresholds; deviation statistic D_{w,l}(n) compared to random words.
  - The OBSERVED discrepancy trend ~ O(sqrt(loglog n)/sqrt(n)) (their eq. 4.2) matches
    Philipp's LIL for random / lacunary sequences, but this is EMPIRICAL for minimal
    words; it is NOT proven.

MACHINERY THAT IS ABSENT: AEV use NO exponential/Weyl sums, NO transfer operators,
NO Fourier dimension / Bourgain–Dyatlov, NO ergodic optimization, NO Diophantine
input on log3/log2. The paper offers ZERO analytic handle; it reduces our target to a
conjecture equivalent to ours and stops.

================================================================================
2. PARTIAL RESULTS IN AEV OR ITS BIBLIOGRAPHY
================================================================================

(a) one-sided density bound liminf freq >= c for {(3/2)^n} / Syracuse, specific OR
    generic orbit:  NONE PROVEN. [OPEN] Conjectured only (Conj 1.6).

(b) effective / quantitative equidistribution with explicit error for a SPECIFIC orbit:
    NONE. [OPEN for specific] All quantitative results in the surrounding literature are
    METRIC, i.e. "for almost all x (Lebesgue)", which says nothing about the specific
    orbit of 27:
      - Koksma 1935: {xi x^n} u.d. for a.e. x>1.
      - Erdos–Koksma 1949 / Cassels 1950: discrepancy D_N({xi x^n}) = O(log N (loglog N)^{3/2+e}/sqrt N) for a.e. x. [PROVEN, metric]
      - Aistleitner 2014 (arXiv:1210.4215), "Quantitative uniform distribution results
        for geometric progressions": precise metric LIL
        limsup sqrt(N) D_N({xi x^n}) / sqrt(loglog N) = 1/sqrt2 for a.e. x [PROVEN, metric],
        plus a CLT for f(xi x^n). Explicitly: "no asymptotic LOWER bounds for D_N for
        TYPICAL x have ever been proved," and "deciding whether ({x^n}) is u.d. mod 1
        for a SPECIFIC value of x is notoriously difficult, and only few partial results
        are known." This is the authoritative statement of the wall.

(c) positive-density / full-density (in n) set of times for a SINGLE orbit:
    NONE. [OPEN]

(d) conditional result on a Diophantine hypothesis on log3/log2:
    NONE in AEV. (Bugeaud–Moshchevitin type constructions give related conditional /
    existence results for OTHER quantities, not density of a specific 3/2-orbit.)

Closest proven structural facts in the bibliography (still NOT density):
  - Dubickas [DUB09] subword-complexity bound: liminf_l p_w(l)/l >= log q / log(p/q).
    For 3/2 this is ~ log2/log(3/2) ~ 1.71 > 1. [PROVEN] But complexity >= richness,
    NOT letter frequency: it proves the word is not eventually periodic / is "rich",
    and says NOTHING about even-density.
  - Flatto–Lagarias–Pollington, "On the range of fractional parts {xi (p/q)^n}",
    Acta Arith. 70 (1995): the gap Omega(p/q) between limsup and liminf of {theta(p/q)^n}
    satisfies Omega(p/q) > 1/p, hence Omega(3/2) > 1/3, UNCONDITIONALLY, for every
    theta>0. [PROVEN] BUT this bounds the RANGE OF LIMIT POINTS (a closure / topological
    statement). It does NOT bound how OFTEN the orbit is even. It is the strongest
    unconditional one-sided fact about a specific 3/2-orbit and it is the wrong kind of
    one-sidedness (range, not density).

================================================================================
3. THE HUNT: any UNCONDITIONAL liminf even-density > 0 for a SPECIFIC 3/2-type orbit?
================================================================================

ANSWER: NO. Not for any specific orbit of a 3/2-type map in the p < q^2 regime
(3/2 has p=3 < q^2=4, the hardest regime).

Evidence / why this is a hard wall, not a gap in our search:
  - {(3/2)^n} mod 1 is NOT EVEN KNOWN TO BE DENSE in [0,1], let alone equidistributed
    or to have positive lower even-density. Aistleitner records the brutal status: we do
    not even know limsup_n {(3/2)^n} - liminf_n {(3/2)^n} >= 1/2 (FLP only gives > 1/3).
  - Positive results DO exist but only in the EASY regime p > q^2 (Tijdeman; Flatto
    "Z-numbers and beta-transformations"; Kaneko; Dubickas "Fractional parts of powers
    of large rational numbers"): there one can control Z_{p/q}-numbers, get
    equidistribution, etc. These methods structurally FAIL at 3/2 (p<q^2). This is the
    same boundary as Mahler's 3/2 problem and the 3x+1 / Collatz wall.
  - Tao 2019 ("Almost all Collatz orbits attain almost bounded values"): logarithmic-
    density statement over STARTING points (a measure on initial conditions), NOT a
    single fixed orbit; gives nothing for the orbit of 27 specifically.

Net: the analytic genericity input we need has NO unconditional precedent for ANY
specific orbit. The literature confirms this is precisely the Mahler-3/2 / Collatz
frontier. (This is consistent with — and sharpens — our two meta-theorems that no
structure-only proof exists: the missing input is genuinely analytic AND genuinely
open at the specific-orbit level.)

================================================================================
4. SINGLE MOST PROMISING ANALYTIC TECHNIQUE TO PURSUE NEXT
================================================================================

Technique: EXPONENTIAL-SUM / FOURIER-DECAY cancellation tied to the non-Pisot property
of 3/2, aiming ONLY at the weak one-sided target (>= 1/3, not 1/2).

Why this and not the others:
  - Aistleitner pinpoints the exact structural obstruction: geometric progressions
    {xi r^n} LACK the Fourier orthogonality that lacunary sequences enjoy, so the only
    available tool is direct van der Corput / Weyl-sum cancellation on
    S_N(t) = sum_{n<=N} e(t * xi * (3/2)^n) for the SPECIFIC xi attached to the orbit.
    Even a one-sided cancellation bound for the lowest frequency t (k=1, mod 2) yields a
    one-sided density statement — and we only need density >= 1/3, a very weak target far
    below full equidistribution. A one-sided (liminf) bound is strictly weaker than the
    two-sided u.d. that is open, which is the only reason this is not hopeless.
  - This dovetails with our OWN proven input (commit 984f70f): 3/2 is non-Pisot =>
    the Bernoulli convolution nu_{2/3} is RAJCHMAN (its Fourier transform -> 0). The
    spectral measure of the 3/2-orbit / digit process is of the same self-similar /
    non-Pisot type, so its Fourier coefficients decay. Rajchman = qualitative decay is
    enough to KILL the "stuck in a half" failure mode but is NOT enough for a density
    rate.

EXACTLY what it needs (the single missing ingredient):
  An EFFECTIVE Fourier-decay RATE (polynomial or even logarithmic, e.g.
  |hat nu(t)| <= C |t|^{-a} or <= C/(log|t|)^a) for nu_{2/3} (or the orbit's spectral
  measure), as opposed to the bare Rajchman decay-without-rate we currently have. A
  quantitative rate converts, via a Davenport–Erdos / correlation (or a Koksma–Hlawka /
  Erdos–Turan) inequality, into a one-sided lower bound on the even-density. Pure
  Rajchman does NOT.

Where to get the rate (refs to mine next):
  - Bremont, "On the rate of convergence in the Erdos–Volkmann / Bernoulli-convolution
    Fourier-decay for non-Pisot bases"; Varju–Yu and P. Varju on Fourier decay of self-
    similar measures; Streck (2023-24) on power Fourier decay of Bernoulli convolutions
    for algebraic non-Pisot parameters; Bourgain–Dyatlov / fractal-uncertainty type
    sum-product input for Fourier dimension > 0 of self-similar measures.
  - The target lemma: "for 3/2 (algebraic, non-Pisot), nu_{2/3} has power Fourier decay
    with explicit exponent a>0." If a>0 is established for our specific measure, the
    Erdos–Turan inequality gives liminf even-density >= 1/2 - O(decay) which already
    clears 1/3 with room to spare.

Honest status label:
  - [PROVEN] (ours): 3/2 non-Pisot => nu_{2/3} Rajchman (decay, no rate).
  - [OPEN, but the right target]: power Fourier-decay RATE for nu_{2/3}; this is the
    one analytic input that closes the reduction, it is strictly weaker than the open
    u.d. of {(3/2)^n}, and there is an active literature (Streck, Varju, Bremont) that
    has produced power-decay rates for related non-Pisot self-similar measures.
  - Fallback weaker target also worth pricing: even a "positive lower even-density >= c"
    for any c>0 from qualitative Rajchman + a soft ergodic-averaging argument would be a
    genuine partial result; but our reduction specifically needs c >= 1/3, so a rate is
    the clean route.

================================================================================
KEY REFERENCES (precise)
================================================================================
- Andrieu–Eliahou–Vivion, arXiv:2510.11723 (Thm 1.7 = normality<=>equidist; Conj 1.6
  = our object; all proofs combinatorial/modular; evidence computer-assisted only).
- Flatto–Lagarias–Pollington, "On the range of fractional parts {xi(p/q)^n}",
  Acta Arith. 70 (1995) 125-147. Omega(3/2) > 1/3 [PROVEN, range not density].
- Aistleitner, "Quantitative uniform distribution results for geometric progressions",
  arXiv:1210.4215 (metric LIL/CLT; states specific-x u.d. is open; no metric lower bds).
- Dubickas [DUB09] complexity bound liminf p_w(l)/l >= log q/log(p/q) [richness, not freq].
- Mahler 1968; Akiyama 2008; Akiyama–Frougny–Sakarovitch (core rational-base theory);
  Dubickas–Mossinghoff (4/3 problem); Flatto, Tijdeman, Kaneko (p>q^2 EASY regime).
- For the rate: Streck, Varju(-Yu), Bremont on power Fourier decay of non-Pisot
  Bernoulli convolutions; Bourgain–Dyatlov fractal-uncertainty for Fourier dimension.

BOTTOM LINE: AEV gives us a clean equivalent restatement (normality<=>equidistribution)
but NO analytic tool and NO partial density bound. No unconditional liminf even-density>0
exists for any specific 3/2-orbit anywhere in the literature — this is the Mahler/Collatz
wall. The one live route is an EFFECTIVE power Fourier-decay rate for nu_{2/3} (we already
have the qualitative Rajchman half PROVEN), fed through an Erdos–Turan inequality, aimed
at the weak >= 1/3 target.
