# CITATIONS — pinned references for PAPER_MAIN.md and PAPER_HIERARCHY.md

Status of each citation flagged in the two notes' References sections. Confidence notes name the
verifying source. SOUNDNESS: anything not independently confirmed is flagged explicitly at the bottom.
(NOT committed — working note for the authors.)

---

## Item 1 — Ergodic optimization / sub-action theory (PAPER_MAIN Theorem 3 external input)

The Theorem-3 fact used is: *an all-orbits one-sided Birkhoff inequality `sum_{k<n} f(T^k x) <= C` for all x
holds iff `beta := max over T-invariant measures mu of integral f dmu <= 0`*, together with the existence of a
bounded (continuous) sub-action `phi` with `f <= phi∘T - phi + beta`. This is the variational principle +
the Mañé–Conze–Guivarc'h sub-action lemma of ergodic optimization.

- **R. Mañé**, *Generic properties and problems of minimizing measures of Lagrangian systems*,
  **Nonlinearity 9 (1996), no. 2, 273–310.** DOI 10.1088/0951-7715/9/2/002.
  (Minimizing/maximizing measures invariant; potential cohomologous to a constant on the support of ergodic
  components — the measure-side half.) — VERIFIED via IOPscience article page.
- **T. Bousch**, *Le poisson n'a pas d'arêtes*, **Ann. Inst. H. Poincaré Probab. Statist. 36 (2000), no. 4,
  489–508.** (Existence of a continuous/calibrated sub-action — the "revelation"; the sub-action existence
  half.) — VERIFIED via Numdam (AIHPB_2000__36_4_489_0) and ScienceDirect.
- **T. Bousch**, *La condition de Walters*, **Ann. Sci. Éc. Norm. Supér. (4) 34 (2001), no. 2, 287–311.**
  DOI 10.1016/S0012-9593(00)01062-4. (Sub-action existence under the Walters condition, generalizing the
  Hölder case.) — VERIFIED via Numdam (ASENS_2001_4_34_2_287_0) and EUDML.
- **O. Jenkinson**, *Ergodic optimization*, **Discrete Contin. Dyn. Syst. 15 (2006), no. 1, 197–224.**
  DOI 10.3934/dcds.2006.15.197. (Survey; the `beta = sup_mu ∫f dmu` variational principle + revelation
  theorem, cite for the equivalence as stated.) — VERIFIED via AIMS Sciences article page.
- **O. Jenkinson**, *Ergodic optimization in dynamical systems*, **Ergodic Theory Dynam. Systems 39 (2019),
  no. 10, 2593–2618.** DOI 10.1017/etds.2017.142 (arXiv:1712.02307). (Updated survey; same theorems with
  modern numbering.) — VERIFIED via Cambridge Core + arXiv.
- **Conze–Guivarc'h** (unpublished manuscript, c. 1990s) — the original Mañé–Conze–Guivarc'h sub-action lemma.
  **UNPINNABLE: never formally published.** Standard practice is to cite it as "Conze–Guivarc'h, unpublished
  (1993)" and lean on Bousch (2000/2001) + Jenkinson (2006/2019) for the published statements. Recommend
  keeping it only as an attribution alongside the published anchors.

Recommended precise cite for Theorem 3: the variational characterization = Jenkinson (2006) survey §2–3;
the bounded sub-action existence = Bousch (2000) for Hölder / Bousch (2001, "La condition de Walters") for the
Walters class; Mañé (1996) for the measure-rigidity half.

## Item 2 — 2-adic Collatz conjugacy / Bernoulli (PAPER_MAIN Theorem 2(b) external input)

- **J. C. Lagarias**, *The 3x+1 problem and its generalizations*, **Amer. Math. Monthly 92 (1985), no. 1,
  3–23.** DOI 10.1080/00029890.1985.11971528. (The 3x+1 map extends to a measure-preserving, ergodic map on
  Z_2 w.r.t. 2-adic measure.) — VERIFIED via Taylor & Francis + SciRP reference page.
- **D. J. Bernstein, J. C. Lagarias**, *The 3x+1 conjugacy map*, **Canad. J. Math. 48 (1996), no. 6,
  1154–1169.** DOI 10.4153/CJM-1996-060-x. (The conjugacy `Φ` on Z_2 conjugating the shift `S` to the 3x+1
  map `T`.) — VERIFIED via Cambridge Core (S0008414X0004606X) + cr.yp.to retypeset.
- **K. R. Matthews, A. M. Watts**, *A generalization of Hasse's generalization of the Syracuse algorithm*,
  **Acta Arith. 43 (1984), no. 2, 167–175.** (Ergodic/Markov properties of generalized 3x+1-type maps on Ẑ.)
  Companion: **K. R. Matthews, A. M. Watts**, *A Markov approach to the generalized Syracuse algorithm*,
  **Acta Arith. 45 (1985), no. 1, 29–42.** — VERIFIED via numbertheory.org + arXiv overview citations
  (volume/pages high confidence; recommend a final MathSciNet glance on the 1984 page range).

## Item 3 — Mahler 3/2 / Z-numbers, p>q^2 vs p<q^2 regime

- **K. Mahler**, *An unsolved problem on the powers of 3/2*, **J. Austral. Math. Soc. 8 (1968), no. 2,
  313–321.** DOI 10.1017/S1446788700005371. — VERIFIED via Cambridge Core + CARMA PDF (167.pdf).
- **L. Flatto, J. C. Lagarias, A. D. Pollington**, *On the range of fractional parts {ξ(p/q)ⁿ}*,
  **Acta Arith. 70 (1995), no. 2, 125–147.** (The `1/p` interval / spread bound; the `1/3` figure for 3/2 is
  the `p=3` case.) — VERIFIED via EUDML (doc/206742) + matwbn ICM PDF (aa7023.pdf).
- **A. Dubickas, M. J. Mossinghoff**, *Lower bounds for Z-numbers*, **Math. Comp. 78 (2009), no. 267,
  1837–1851.** DOI 10.1090/S0025-5718-09-02240-9. (This IS the "4/3 problem" paper: conjectures non-existence
  of `Z_{p/q}`-numbers for `1<q<p<q(q-1)`; lower bounds for 3/2, 4/3, 5/3.) — VERIFIED via dblp (Mossinghoff)
  + AMS issue search; page range cross-checked.
- **A. Dubickas**, *On integer sequences generated by linear maps*, **Glasgow Math. J. 51 (2009), no. 2,
  243–252.** DOI 10.1017/S0017089509004984. (Sequences `x_n = ⌊β x_{n-1}+γ⌋`; proves the lower bound on the
  complexity function — this is "Dubickas (2009), Theorem 3" cited by AEV, and the source of the subword
  slope used in PAPER_HIERARCHY §5 Lemma 6.) — VERIFIED via Cambridge Core + AEV (2510.11723) text quoting
  "Dubickas (2009, Theorem 3) ... liminf p_w(l)/l ≥ log q / log(p/q)".
  *Alternative if PAPER_MAIN's "Dubickas (2009)" was meant as the spread/interval result:* **A. Dubickas**,
  *Powers of a rational number modulo 1 cannot lie in a small interval*, **Acta Arith. 137 (2009), no. 3,
  233–239.** (Sharpens the FLP `1/p` bound.) — flagged: pick whichever matches the authors' intent.
- **S. Akiyama, Ch. Frougny, J. Sakarovitch**, *Powers of rationals modulo 1 and rational base number
  systems*, **Israel J. Math. 168 (2008), 53–91.** DOI 10.1007/s11856-008-1056-4. (Rational-base p/q number
  systems; the "triple expansions" structure — this is the canonical "Akiyama 2008".) — VERIFIED via Springer
  + telecom-paristech PDF.
- **W. Narkiewicz**, *A note on a paper of H. Gupta concerning powers of 2 and 3*, **Univ. Beograd. Publ.
  Elektrotehn. Fak. Ser. Mat. Fiz. No. 678–715 (1980), 173–174.** (Density bound `N(T) ≤ 1.62 T^{α₀}`,
  `α₀ = log₃2`, for powers of 2 omitting digit 2 in base 3.) — VERIFIED via arXiv:2202.13256 and the 3x+1
  annotated bibliography (math/0309224); the `1.62 x^{log_3 2}` figure matches the note exactly.
- **P. Erdős**, *Some unconventional problems in number theory*, **Math. Mag. 52 (1979), no. 2, 67–70.**
  (The ternary-digits-of-2ⁿ conjecture: only 2⁰,2²,2⁸ omit digit 2 in base 3.) — VERIFIED via arXiv:2202.13256
  + secondary literature. (Also appeared as Astérisque 61 (1979), 73–82 — same year/title; the Math. Mag.
  version is the usual cite.)

NOTE on Tijdeman / Kaneko / Pollington (named in the pinning brief): these do **not** appear as standalone
entries in either note's reference list (Pollington appears only as FLP co-author). No separate pin needed
unless the authors add them.

## Item 4 — arXiv:1901.03913 (PAPER_HIERARCHY §3.6, CF ⊊ CS rung)

- **D. Pálvölgyi (Dömötör Pálvölgyi)**, *The range of non-linear natural polynomials cannot be context-free*,
  **arXiv:1901.03913 (2019).** Establishes: the base-q representation of the range of a natural-valued
  polynomial is context-free **iff the polynomial is linear** (answers a question of Shallit; proof combines
  the Interchange Lemma with a generalized Pumping Lemma). — VERIFIED via arXiv PDF + ADS abstract.
  This exactly matches the use in PAPER_HIERARCHY ("range of a non-linear natural polynomial is not CF"). The
  "**authorship not independently confirmed**" caveat in PAPER_HIERARCHY can now be REMOVED — author is
  Dömötör Pálvölgyi (ELTE).

## Item 5 — AEV and Eliahou–Verger-Gaugry

- **M. Andrieu, S. Eliahou, L. Vivion**, *A Normality Conjecture on Rational Base Number Systems*,
  **arXiv:2510.11723** (v1 6 Oct 2025; revised 2026). math.NT/math.CO. — VERIFIED via arXiv abstract + HTML.
  Numbering (quoted from the HTML, VERIFIED):
  - **Conjecture 1.2**: for all coprime p/q (p>q≥1) and all integer expansions u, the maximal word
    `wmax_{p/q}(u)` is normal over `{p−q,…,p−1}` and (for u≠ε) the minimal word `wmin_{p/q}(u)` is normal over
    `{0,…,q−1}`. (Normality conjecture — the named [OPEN] kernel.)
  - **Conjecture 1.4**: for coprime p>q>1 with p<q², no `Z_{p/q}`-number exists (no x>0 with all
    `{x(p/q)ⁿ} ∈ [0,1/q)`). (Generalized Mahler.)
  - **Conjecture 1.6**: for coprime p>q≥1, every orbit `(T^l_{p/q}(n))_l`, `T_{p/q}(x)=⌈px/q⌉`, is
    equidistributed in residue classes mod `q^k` for all k. (Collatz-flavoured equidistribution.)
  - **Theorem 1.5**: Conjecture 1.2 ⟹ Conjecture 1.4.
  - **Theorem 1.7**: Conjectures 1.2 and 1.6 are equivalent.
  (Conjecture 1.2's validity ⟹ Akiyama 2008's conjecture and a positive answer to Dubickas–Mossinghoff 2009.)
- **S. Eliahou, J.-L. Verger-Gaugry**, *The number system in rational base 3/2 and the 3x+1 problem*,
  **arXiv:2504.13716** (18 Apr 2025), to appear in **C. R. Math. Acad. Sci. Paris**. — VERIFIED via arXiv +
  comptes-rendus PDF (crmath.662).

---

## Lines to update in the source notes

PAPER_MAIN.md "Partially pinned" block (lines ~708–724) → promote to "Pinned" with:
- Ergodic optimization: Mañé, Nonlinearity 9 (1996) 273–310; Bousch, Ann. IHP PS 36 (2000) 489–508 and
  Bousch, Ann. Sci. ÉNS (4) 34 (2001) 287–311; Jenkinson, DCDS 15 (2006) 197–224 and ETDS 39 (2019)
  2593–2618. Keep Conze–Guivarc'h as "unpublished, c.1993" (unpinnable, see below).
- 2-adic Collatz: Lagarias, Amer. Math. Monthly 92 (1985) 3–23; Bernstein–Lagarias, Canad. J. Math. 48
  (1996) 1154–1169; Matthews–Watts, Acta Arith. 43 (1984) 167–175.
- Narkiewicz: Univ. Beograd. Publ. Elektrotehn. Fak. Ser. Mat. Fiz. No. 678–715 (1980) 173–174.
- Erdős: Math. Mag. 52 (1979), no. 2, 67–70.
- Dubickas (2009): Glasgow Math. J. 51 (2009) 243–252 [or Acta Arith. 137 (2009) 233–239 — pick by intent];
  Dubickas–Mossinghoff: Math. Comp. 78 (2009) 1837–1851; Akiyama (2008) = Akiyama–Frougny–Sakarovitch,
  Israel J. Math. 168 (2008) 53–91.
- arXiv:1901.03913 → add author "Dömötör Pálvölgyi", full title as above.

PAPER_HIERARCHY.md References (lines ~606, ~609–611):
- Line 606 (Dubickas subword) → "A. Dubickas, *On integer sequences generated by linear maps*, Glasgow Math.
  J. 51 (2009), no. 2, 243–252 (Thm 3: complexity lower bound, slope log q/log(p/q))."
- Lines 609–611 (arXiv:1901.03913) → add "Dömötör Pálvölgyi" and DROP the "authorship not independently
  confirmed" caveat.
- Line 615 (Mahler) is correct; line 616 (Tao/FLP/AEV) consistent with the pins above.

---

## Remaining UNPINNABLE / flagged

1. **Conze–Guivarc'h (unpublished, ~1990s)** — genuinely never published; cite as "unpublished" alongside
   Bousch/Jenkinson/Mañé. Cannot give venue/pages.
2. **"Dubickas (2009)" disambiguation** — two distinct real Dubickas 2009 papers fit different uses
   (Glasgow Math. J. 51 = subword/complexity, used by PAPER_HIERARCHY §5; Acta Arith. 137 = spread/interval,
   a possible reading of PAPER_MAIN). Authors must choose which one each "Dubickas (2009)" denotes. Both
   citations themselves are VERIFIED; only the mapping to the in-text use is ambiguous.
3. **Matthews–Watts 1984 exact page range (167–175)** — high confidence from numbertheory.org and the 3x+1
   bibliography, but not seen on the publisher's own page; recommend a 30-second MathSciNet confirmation.
4. **Akiyama, "Mahler's Z-number and 3/2 number systems" (2008)** — a separately-existing solo Akiyama 2008
   item surfaced (ResearchGate), but its venue could NOT be confirmed (no journal/volume found; possibly a
   RIMS Kôkyûroku / preprint). The notes' "Akiyama (2008, triple expansions)" is best served by the
   Akiyama–Frougny–Sakarovitch Israel J. Math. paper (pinned); do NOT cite the solo Z-number item until
   its venue is confirmed.

---

## Verified additions (2026-06-30, surfaced by an external second-opinion consult)

5. **Lee–Palvannan 2024 [VERIFIED, real; relevance: measure-level, NOT specified-orbit].** Jungwon Lee,
   Bharathwaj Palvannan, *An ergodic approach towards an equidistribution result of Ferrero–Washington*,
   J. Théor. Nombres Bordeaux **36** (2024), no. 3, 805–833 (Numdam, DOI 10.5802/jtnb.1296). VERIFIED via the
   Numdam page. Content: re-proves the Ferrero–Washington equidistribution (vanishing of the cyclotomic
   μ-invariant for Kubota–Leopoldt p-adic L-functions) by realizing an **ergodic skew-product on `ℤ_p × [0,1]`
   as a factor of the 2-sided Bernoulli shift**. ASSESSMENT (soundness): structurally the **nearest recent
   ergodic-skew-product / factor-of-Bernoulli technique** to our setup (our `T` is exact Bernoulli; the 3-adic
   place is a factor — `THREEADIC_SLIDING_LOCK.md`), BUT the result is **measure-theoretic / generic, not a
   single specified orbit**, and concerns Iwasawa theory, not `3x/2` or `(3/2)ⁿ`. It therefore lands on the
   **a.e./measure side of our wall — confirms, does not breach**. Value: a legitimate new citation as the
   closest ergodic-factor technique, and a plausible outreach circle for the *quenched* (specified-orbit)
   version. Flagged by an external second-opinion (ChatGPT) repo read; the other refs it raised
   (arXiv:2411.03468, Strauch on `ξ(3/2)ⁿ mod 1`, AEV arXiv:2510.11723) were already in-corpus.

6. **Filip 2025 [VERIFIED, real; relevance: nearest recent frontier, DISQUALIFIED].** Simion Filip,
   *Measure Rigidity beyond Homogeneous Dynamics*, **arXiv:2512.13865** (Dec 2025). The most "beyond-homogeneous"
   recent measure-rigidity item; still requires **higher-rank / non-amenable smooth-manifold structure and
   orbit-closure (not single-orbit) behavior** — so our rank-1 amenable hyperbolic single specified orbit is
   disqualified. Value: confirms the `(d)` Coverage No-Go (`RANK1_AMENABLE_EQUIDISTRIBUTION.md`) **through the
   current (2025) frontier** — even the newest rigidity beyond homogeneous spaces does not reach our regime.
   (Surfaced by `RECENT_LIT_SCAN_2026.md`.)

7. **Coq-BB5 2025 [VERIFIED, real; relevance: context, the frontier gate].** The bbchallenge collaboration,
   *Determination of the fifth Busy Beaver value*, **arXiv:2509.12337** (Sep 2025, rev. Mar 2026), Coq-verified
   `S(5)=BB(5)=47,176,870`. Context, not a weapon: it cements **BB(6) as the live frontier, gated precisely on
   Antihydra** (a Cryptid whose non-halting = our `(K)`). Community status (2026): Antihydra still open, simulated
   to `2^38` steps, with only Lean **recurrence-equivalence** formalizations (a reduction certificate, NOT a
   halting proof) — independently confirming our reduction is the accepted one and that the reduction itself is
   community folklore (so a paper's novelty must be the barrier results, not the reduction).

> **SOUNDNESS NOTE (2026-06-30).** Several 2025–2026 "Collatz/3x+1 proof" preprints encountered during the recent
> scan (e.g. arXiv:2603.25753) bear strong crank/LLM markers and were **REJECTED, not banked**. No unconditional
> partial density bound, one-sided result, or specified-orbit result for Mahler 3/2 / AEV exists in the literature.
