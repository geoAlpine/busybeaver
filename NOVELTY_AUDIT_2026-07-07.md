# Novelty audit — template/ledger campaign results vs. bbchallenge community & literature (2026-07-07)

*Scope: the results in `CAMPAIGN_2026-07-06_TEMPLATE_LEDGER.md`, `PAPER_RUN_STRUCTURE.md`,
`PAPER_SPECIES_SURVEY.md`. Method: WebSearch/WebFetch over wiki.bbchallenge.org, bbchallenge.org,
discuss.bbchallenge.org (as indexed), sligocki.com, arXiv, GitHub. Verdict labels:
**KNOWN** (cite) / **PARTIAL-PRIOR** (cite) / **NOVEL-as-far-as-searched**. Caveat throughout:
absence of evidence ≠ proof of novelty — most day-to-day cryptid work happens on the bbchallenge
Discord, which is NOT web-indexed; only what has been copied to the wiki/blogs/forum is searchable.*

---

## 1. Machine-ID mapping (highest-priority item)

None of o3/o4/o15/o17/o18 has a community *name*; bbchallenge refers to them by their standard-format
transition string, and **four of the five have dedicated BusyBeaverWiki pages** (page title = spec string).
All five appear on or via the BB(6) page's cryptid/holdout material
(https://wiki.bbchallenge.org/wiki/BB(6)).

| ours | spec | community identity | documented state (source) |
|---|---|---|---|
| Antihydra | `1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA` | **Antihydra** (named cryptid) | Full page + status page; found by mxdys 2024-06-28, high-level rules by Racheline; "probviously non-halting"; the standard formulation already includes the **condition counter** (halts iff counter hits −1, i.e. odd steps outnumber 2×even). https://wiki.bbchallenge.org/wiki/Antihydra ; https://bbchallenge.org/antihydra ; https://www.sligocki.com/2024/07/06/bb-6-2-is-hard.html |
| o4 | `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---` | no name; own wiki page; listed under "similar to Antihydra" on BB(6) page | Found by **@dyuan01**, Discord, **2024-09-04**. Wiki page documents the exact two-counter recurrence `(3b+0,c+1)→(4b+5,c)`, `(3b+1,c)→(4b+2,c+4)`, `(3b+2,c+1)→(4b+6,c+7)` and the halt rule `(3(3(3(3b+2)+1)+1)+0,0)→halt`; "probviously non-halting". Also notes the start-state-C normalization `1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB`. https://wiki.bbchallenge.org/wiki/1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB--- |
| o3 | `1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC` | no name; own wiki page; "similar to Antihydra" | Found by **@mxdys**, Discord, **2024-08-20**. Wiki documents `(3x+0,y)→(4x+4,y+1)`, `(3x+1,y+1)→(4x+5,y+2)`, `(3x+2,y)→(4x+8,max(0,y−1))`, halt at `(3x+1,0)`; simulated 10⁶ iterations (x~10^124940, y=331762). https://wiki.bbchallenge.org/wiki/1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC |
| o15 | `1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA` | no name; own wiki page; "probviously halting cryptid" | Found by **Racheline 2024-11-23**; ×8/3-per-step rule with mod-3 branching and left-side information storage; **halting residue sequences known**: shortest found length 110, counted as a class of 2¹³·3¹⁵ ≈ 1.18·10¹¹ sequences; halt probability ≈ 3⁻⁸⁷ per epoch, expected halt around 10^10^38.1 steps. https://wiki.bbchallenge.org/wiki/1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA |
| o17 | `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB` | no name; own wiki page | Analyzed by **Racheline 2025-02-09** (+ later "Opus 4.7 / DrDisentangle" section): gate `F,0→---` reachable only via `D,0→0LF` (D-left-sweep landing on 00); 335+ macro-rule families all of the form `dt=(8k+C_family)/3`, `Δk=+3`; block sizes ≡2 (mod 3); "shift-overflow counter with chaotic counting dynamics"; **iterated-exponential halt estimate ≈1.24^1.24^530 ≈ 10^(3·10⁴⁸)**; Lean traces at https://github.com/rwst/bbchallenge/blob/main/1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB/machine.lean . Wiki: https://wiki.bbchallenge.org/wiki/1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB |
| o18 | `1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---` | no own page — **redirects to the o15 page**. **o18 IS o15's table**: locally VERIFIED (this audit, `scratchpad/tnf_check.py`) that o18 = mirror of o15's transition table re-rooted at start state D (TNF); the wiki states this ("When the starting state is D, the TNF is 1RB0RE_…"). The repo currently treats them as two distinct species members — this must be acknowledged before release. | Analyzed by **@-d** (Discord 2025-08-13 / 2025-08-25, mirrored on the wiki): config `A(n,r)`, `n→~8n/3` with branch chosen by `n mod 3`, `r` a stored word; **an explicit length-108 fatal residue sequence** `EEBBEBEEBEEEBB…BE` exists; ≈10⁵⁷⁹¹⁶²¹⁵²⁹⁶(sic, as quoted on wiki) halting paths of length 108, halt chance ≈10⁻³⁹ per window; simulated past 2.7·10⁶ A-epochs; **community status: "probviously HALTING"**. **Lean-verified fatal class:** "@-d has a formal proof that A(3¹⁰⁸·k + 19757005…946348086) will halt" — https://github.com/int-y1/proofs/blob/1929f57df4dd7afcc11c3f458e20526fd1f991e0/BusyLean/Individual/1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---.lean#L321-L322 . Wiki (redirect target): https://wiki.bbchallenge.org/wiki/1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA |

Context: ~1,101 BB(6) holdouts remain as of June 2026, all simulated to 10¹³ steps
(https://wiki.bbchallenge.org/wiki/BB(6)). Named BB(6) cryptids on the wiki Cryptids page: Antihydra,
Lucy's Moonlight, Space Needle (https://wiki.bbchallenge.org/wiki/Cryptids).

## 2. Result-by-result verdicts

| our result | community/prior work found | verdict | action |
|---|---|---|---|
| (a) o4 template reduction + a-ledger (non-halt ⟸ prefix-sum ledger boundedness over base-4/3 residue itinerary) | The **two-counter recurrence and the c=0 halt gate are already on the o4 wiki page** (dyuan01, 2024-09) — i.e. the *statement* "o4 halts iff the second counter hits the fatal pattern at c=0" is community knowledge; ditto o3 (mxdys, 2024-08: halt at `(3x+1,0)`), and the ledger/condition-counter formulation is the standard one for Antihydra itself (https://wiki.bbchallenge.org/wiki/Antihydra). What is NOT found: a *certified* trace-template proof (macro prefix/body/suffix lemmas red-teamed into a proven reduction), the seed-specificity corollary, the ruin quantification. | **PARTIAL-PRIOR** (reduction statement KNOWN; certification apparatus not found in searched sources) | Cite dyuan01/mxdys wiki pages prominently; reposition o4/o3 contribution as *certification + structure theory* of a known reduction, not discovery of the reduction |
| (b) o18 pushdown-3-adic-odometer collapse | o18 is documented on the o15 wiki page (@-d, 2025-08): `A(n,r)` with mod-3-driven branching and a stored word `r` — informally the same "counter + word memory" decomposition. The specific "pushdown 3-adic odometer, one finite table" formulation: not found in searched sources. **BUT: our "no fatal set" claim is CONTRADICTED — @-d has a Lean-verified fatal congruence class mod 3¹⁰⁸ (URL above), and community status is "probviously halting".** | **PARTIAL-PRIOR** on structure; **our no-fatal-set finding is REFUTED by prior work** | **Correct `O18_TEMPLATE_PORT_2026-07-07.md` and the species survey before any release** (the searched families simply missed the fatal class); cite @-d + int-y1/proofs; re-check whether the pushdown-odometer table already predicts the length-108 sequence |
| (c) o15 queue/big-block reduction + `[2,2]` fatal cylinder | Racheline's wiki analysis (2024-11) already has: ×8/3 rule, mod-3 branching, left-side storage, **explicit fatal residue sequences (length ~110, counted to 2¹³·3¹⁵ variants), halt probability 3⁻⁸⁷**. Our leading-`[2,2]`-digit-pair *coordinateization* of the fatal set (digit-string cylinder + predict-and-confirm) not found verbatim, but the existence, size and probability of the fatal set are prior. | **PARTIAL-PRIOR** (fatal set KNOWN; cylinder/digit-string formulation not found) | Cite Racheline; verify our `[2,2]` cylinder against her length-110 sequences (consistency check); claim only the coordinate change |
| (d) o17 gate map + iterated-exponential gate sparsity | Racheline (2025-02) has the gate (`F,0` via D-sweep on 00), the `dt=(8k+C)/3, Δk=+3` macro laws, block ≡2 (mod 3) invariant, and an **iterated-exponential halt estimate 1.24^1.24^530**; Lean traces exist (rwst/bbchallenge). Our exact gate map F, t≈3.97n², and the log n′≈a·n sparsity law: not found in searched sources (wiki has no quantitative sparsity statement). | **PARTIAL-PRIOR** (gate + tower estimate KNOWN; exact gate map/sparsity law not found) | Cite Racheline + rwst Lean; position the gate law as sharpening her estimate |
| (e) run-length closed forms via branch fixed points, run = v_p(G−x_ρ); seed-itinerary bijection mod 3^L | For these specific machines: not found in searched sources. But the mathematical content is the classical Collatz parity-vector theory: **Terras 1976 / Everett 1977** prove the parity vector ↔ n mod 2^k bijection, and run/valuation arguments are standard in the 3x+1 literature (survey: Lagarias, arXiv:math/0309224; https://en.wikipedia.org/wiki/Collatz_conjecture). Active 2026 parity-vector work exists in the Collatz world (e.g. arXiv:2605.13886; arXiv:2601.04289). | **PARTIAL-PRIOR** (classical analogue; machine-specific closed forms not found) | Cite Terras/Everett/Lagarias in `PAPER_RUN_STRUCTURE.md` as the 2-adic ancestor; claim the 4/3–8/3 transposition + machine applications only |
| (f) "cryptid kernels = one-sided rational-base return-frequency problems, with a margin ladder" unification | The Antihydra↔Mahler-3/2/Z-number connection is on the wiki Antihydra page (citing Dubickas 2009, Odlyzko–Wilf) and in Brubaker's essay (https://benbrubaker.com/why-busy-beaver-hunters-fear-the-antihydra/); "cryptids reduce to hard Collatz-like math" is canonical (https://wiki.bbchallenge.org/wiki/Cryptids). NOT found: the one-sided (liminf) weakening as the minimal input, the cross-machine ×4/3–×8/3 return-frequency family, the margin ladder, or any explicit bridge to AEV (arXiv:2510.11723) — see §4. | **PARTIAL-PRIOR** (Antihydra↔Mahler known informally; the one-sided family unification + AEV bridge not found) | Cite wiki Antihydra page + Dubickas 2009 + Mahler 1968; present unification as extension |

## 3. Method audit — deciders

- Full documented decider inventory (https://wiki.bbchallenge.org/wiki/Deciders): Cycler, Translated
  Cycler, Backward Reasoning, CPS/Closed Position Set (savask's, per
  https://wiki.bbchallenge.org/wiki/Closed_Position_Set), CTL, FAR, Bouncer, Halting Segment, RepWL,
  RWLAcc, n-Gram CPS, Inductive Proof System. Peer-reviewed decider papers: "Turing machine deciders,
  part I" (arXiv:2504.20563) and the BB(5) paper (arXiv:2509.12337; Coq artifact
  https://github.com/ccz181078/Coq-BB5).
- **A "template with parameterized odometer reset" decider: not found in searched sources.** Closest
  prior ingredients: the **Inductive Proof System**
  (https://wiki.bbchallenge.org/wiki/Inductive_Proof_System — auto-detected parameterized rules proved
  by base case + inductive case, nested repeaters, binary counters) and sligocki's hand-worked
  **counter-induction templates** (https://www.sligocki.com/2022/06/14/counter-induction.html), plus
  mxdys's Rocq **RWLAcc** with "L0/L1 inductive rules" and "Collatz Level 2 inductive rules" for
  tetrational machines (https://github.com/ccz181078/busycoq/blob/BB6/verify/RWLAcc.v). The specific
  prefix/body/suffix episode-template architecture certified on a parameter grid is not documented.
  Verdict: **NOVEL-as-far-as-searched as a decider architecture; PARTIAL-PRIOR in ingredients** (cite
  Inductive Proof System + counter-induction as ancestors).
- Macro machines / block simulation: **KNOWN** since 2005 (Ligockis' Quick_Sim; Mateon1's hashlife
  fasttm) — https://wiki.bbchallenge.org/wiki/Accelerated_simulator. Our `o4_bouncer_macro.py`-style
  validated macro build is standard technique; no novelty claim should be made there.
- "Cryptids are beyond all current deciders / reduce to hard math": **KNOWN and canonical**
  (https://wiki.bbchallenge.org/wiki/Cryptids ; https://www.sligocki.com/2024/07/06/bb-6-2-is-hard.html).
- Random-walk / ruin heuristics for cryptids: **KNOWN** in substance — sligocki computes the biased-walk
  ruin probability (1/φ)^(n+1) for Hydra (https://www.sligocki.com/2024/05/10/bb-2-5-is-hard.html) and
  the analogous walk argument for Antihydra (https://www.sligocki.com/2024/07/06/bb-6-2-is-hard.html);
  wiki Antihydra page frames it as a ±(+2/−1) random walk. The words "ledger"/"prefix-sum" are not used,
  but our ruin η≈0.335 / 10⁻⁵⁹-style margins are the same genre of heuristic. Cite sligocki.

## 4. The AEV connection

- AEV = arXiv:2510.11723, "A Normality Conjecture on Rational Base Number Systems," Mélodie Andrieu,
  Shalom Eliahou, Léo Vivion (v1 2025-10-06, v2 2026-04-07; https://arxiv.org/abs/2510.11723). The paper
  itself **never mentions busy beavers, Antihydra, or Turing machines** (full-text check of the PDF).
- The bbchallenge wiki's Antihydra page **already makes the Mahler-3/2 / normality-flavored connection
  informally**: it notes the parity question resembles Mahler's 3/2 problem and that a positive answer
  "could also mean that the parity vector of D(n) is normal," citing Dubickas 2009 and Odlyzko–Wilf —
  but it does **not** cite AEV or any 2025 normality-conjecture paper
  (https://wiki.bbchallenge.org/wiki/Antihydra). Ben Brubaker's essay also popularizes the
  Mahler/Z-number connection (https://benbrubaker.com/why-busy-beaver-hunters-fear-the-antihydra/).
- Citations of AEV as of 2026-07-07 (Semantic Scholar): exactly one — arXiv:2604.28171 (Chunikhin,
  rational semantic numeration systems), **not busy-beaver-related**. No forum/blog/TMBR item connecting
  BB(6) cryptids to AEV was found (TMBR Aug/Dec 2025, TYBR 2025 checked; forum search negative).
- Verdict on our cryptid↔AEV bridge (`AEV_KERNEL_MAP.md`, the one-sided/margin-ladder unification):
  **NOVEL-as-far-as-searched as an explicit bridge**; **PARTIAL-PRIOR for the underlying idea**, since
  the Antihydra↔Mahler-3/2/normality resemblance is already on the wiki (uncited, informal, two-sided,
  Antihydra-only). Our specific contributions not found anywhere: (i) the exact dictionary to AEV's
  conjectures, (ii) the ONE-SIDED liminf weakening as the minimal input, (iii) extending the
  correspondence to o4 (×4/3), o15/o18 (×8/3) as one return-frequency family with a margin ladder.
  Action: cite the wiki Antihydra page's normality remark and Dubickas 2009 as precedent; state the
  bridge as a sharpening/extension, not a first observation.

## 5. Collision risks & correctness flags (act before release)

1. **[CORRECTNESS, highest priority] o18 "no fatal set" is REFUTED by prior work.**
   `O18_TEMPLATE_PORT_2026-07-07.md` §5 ("there is NO fatal set where we can see") and the species
   survey's "no known fatal region at all" are contradicted: @-d has a **Lean-verified halting
   congruence class mod 3¹⁰⁸** for exactly this machine
   (https://github.com/int-y1/proofs/blob/1929f57df4dd7afcc11c3f458e20526fd1f991e0/BusyLean/Individual/1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---.lean#L321-L322),
   and the community status is "probviously **halting**" with a known length-108 fatal rule sequence.
   The repo's negative result was an honest bounded search over the B(m,e) families — it simply did not
   reach the fatal class. Every downstream claim ("first place the program has seen where nothing fatal
   exists to avoid", the o18 species characterization, parts of the margin ladder) must be revised.
2. **[STRUCTURE] o15 and o18 are one machine.** Verified locally in this audit (mirror + re-root at
   state D; wiki states it). The repo's classification counts them as two species members with
   different structures ("string-ledger" vs "recursion tower"); different start states do give
   different orbits, so the analyses need not be wrong, but the species survey's counting and the
   mirror-ladder membership list must be corrected, and the two analyses should be reconciled against
   each other (they describe the same table).
3. **[ACTIVE WORK] o15/o18 is actively worked (Discord, Aug 2025)** — @-d's simulation program, path
   counting, and formal proofs are recent and ongoing; anyone extending that line could produce the
   "candidate decision" the repo is one step from. Racheline is similarly active on o17 (Feb 2025 +
   Lean traces at https://github.com/rwst/bbchallenge). Antihydra has continuous attention (apgoucher's
   2³⁸-iteration simulation, mechanical/3D-printed implementations, TMBR digests).
4. **[PROVENANCE RESOLVED 2026-07-07] The o17 wiki page's macro-rule section ("Opus 4.7 /
   DrDisentangle") is NOT this project** (confirmed by the project owner) — it is genuine independent
   third-party prior art, itself AI-assisted. It substantially overlaps our o17 macro-rule census
   (dt=(8k+C)/3, Δk=+3, 335+ families) and MUST be cited; our incremental o17 contributions are the
   exact gate-to-gate map F(μ,d⃗), the wall-and-erosion derivation of the tower law, and the
   no-finite-reduction results for m≥3. Collision-risk note: another researcher is actively working
   these machines with AI assistance — priority for the NOVEL items favors early community engagement.
5. **[LOW] Collatz-side 2026 activity on parity vectors/rotations** (arXiv:2605.13886,
   arXiv:2601.04289) is adjacent to the run-structure theorems but not BB-specific; monitor, no action.
6. **[LOW] AEV bridge window.** AEV (arXiv:2510.11723) has exactly one citation to date and no BB
   connection anywhere found; the explicit bridge appears open. The wiki Antihydra page's informal
   normality remark means the community is one small step away — publishing the bridge promptly
   preserves priority.

## 6. Search-coverage caveats
- **Discord is the community's primary working medium and is not web-indexed**; the BB(6) page
  references a per-machine annotated spreadsheet of Discord links that could not be opened. Deeper
  unpublished analyses of any of these machines may exist there. All NOVEL verdicts are
  "as-far-as-searched" only.
- Forum search found no dedicated threads for o3/o4/o15/o17/o18 (only Antihydra #242 and generic
  holdout threads, e.g. https://discuss.bbchallenge.org/t/shawns-bb-6-holdouts/136).
- Wiki full-text search was partially blocked (anti-scrape layer); negative results for "3-adic",
  "fatal sequence", "prefix-sum ledger" rest on multiple query phrasings, not exhaustive index access.
- TMBR digests checked: Aug 2025, Dec 2025, TYBR 2025. Pascal Michel's survey (mirror
  https://bbchallenge.org/~pascal.michel/ha.html, updated July 2026) mentions Antihydra only, none of
  the other five specs.

---
*Audit run 2026-07-07. Absence of evidence ≠ novelty.*
