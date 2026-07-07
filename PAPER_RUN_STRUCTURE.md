# Run structure of base-4/3 odometer itineraries: exact 3-adic closed forms, seed-specificity, and a mirror unification of Busy-Beaver cryptid kernels

*Paper-style writeup (theorem–proof only; discovery narrative and reproduction scripts live in the lab notes
`O4_RUN_STRUCTURE_2026-07-07.md`, `O4_LEDGER_ANALYSIS_2026-07-06.md`, `O15_FIXEDPOINT_2026-07-07.md`. Verification:
items `o4_ledger_bijection.py`, `o15_fp_vmap.py` in `verify_all.py`.)*

**Status of claims.** Every theorem below has a complete elementary proof given here in full, plus exhaustive machine
verification on stated ranges. Nothing in this document is conditional. The APPLICATION section states, with precise
labels, what these theorems do and do not settle about the Turing machine o4.

---

## 1. Setting

Fix the map
$$T(G) \;=\; \Big\lfloor \tfrac{4G}{3} \Big\rfloor + c(G \bmod 3), \qquad c(0)=3,\; c(1)=5,\; c(2)=1,$$
on positive integers. Writing $\rho = G \bmod 3$, an equivalent form is
$$3\,T(G) \;=\; 4G + e(\rho), \qquad e(0)=9,\; e(1)=14,\; e(2)=1. \tag{1}$$
(One checks $4G + e(\rho) \equiv 0 \pmod 3$ in each class, so $T(G)$ is a positive integer.)

The **itinerary** of a seed $G_0$ is the residue sequence $\rho_n = G_n \bmod 3$, $G_{n+1}=T(G_n)$.

This map is the generation counter ("odometer") of the 6-state Turing machine
o4 $=$ `1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---`, one of the BB(6) cryptids; see §5.

## 2. The itinerary bijection

**Theorem 1 (seed–itinerary bijection).** *For every $L \ge 1$, the map*
$$\{\,G \bmod 3^L\,\} \;\longrightarrow\; (\rho_0, \rho_1, \dots, \rho_{L-1}) \in \{0,1,2\}^L$$
*is a bijection.*

**Classical antecedent.** Theorem 1 is the base-4/3-odometer analogue of the classical *parity-vector bijection*
for the Collatz map (Terras 1976; Everett 1977): there, seeds mod $2^L$ biject with parity itineraries of length
$L$. The proof pattern (affine branch maps, unit multiplier) is the same; we state and prove it in this system's
coordinates because the ledger application (§5) consumes the exact constants.

*Proof.* Induction on $L$; the case $L=1$ is the definition. Write $G = 3H + \rho$. By (1),
$$T(G) \;=\; \frac{4(3H+\rho) + e(\rho)}{3} \;=\; 4H + s(\rho), \qquad s(\rho) := \frac{4\rho + e(\rho)}{3} \in \{3, 6, 3\}.$$
For fixed $\rho$, the map $H \mapsto 4H + s(\rho)$ is a bijection of $\mathbb{Z}/3^{L-1}$ (as $4$ is a unit mod $3$).
Hence $(G \bmod 3^L) \leftrightarrow (\rho,\, H \bmod 3^{L-1}) \leftrightarrow (\rho,\, \text{itinerary of } T(G)
\text{ of length } L-1)$, the last step by the induction hypothesis. $\blacksquare$

*Verified exhaustively for $L = 1,\dots,8$ (all $3^L$ seeds, all itineraries distinct).*

**Corollary 1.1 (no seed-uniform theorems).** Every finite residue pattern is realized by exactly one residue class
of seeds mod $3^L$ — in particular by infinitely many seeds. Consequently, any property of itineraries that fails for
some pattern (e.g. the ledger condition of §5) cannot be established by any argument uniform in the seed: a proof
must use the specific seed's 3-adic expansion. The set of seeds avoiding a given family of "fatal" patterns is the
complement of a union of cylinders, a closed 3-adic set.

## 3. Exact run structure

**Theorem 2 (run closed form).** *The three branch maps $G \mapsto (4G + e(\rho))/3$ have the integer fixed points*
$$x_\rho = -e(\rho): \qquad x_0 = -9,\quad x_1 = -14,\quad x_2 = -1,$$
*each satisfying $x_\rho \equiv \rho \pmod 3$. For every $G$ with $G \bmod 3 = \rho$, the maximal run of the residue
$\rho$ starting at $G$ (i.e. the largest $R$ with $\rho_0 = \dots = \rho_{R-1} = \rho$) equals*
$$R \;=\; v_3(G - x_\rho),$$
*the 3-adic valuation.*

*Proof.* At a fixed point, $3x = 4x + e$, i.e. $e = -x$. Hence on a $\rho$-branch step,
$$T(G) - x_\rho \;=\; \frac{4G + e(\rho)}{3} - x_\rho \;=\; \frac{4G - 4x_\rho}{3} \;=\; \frac{4}{3}\,(G - x_\rho).$$
Since $4$ is a 3-adic unit, $v_3$ decreases by exactly $1$ per step along the run. Moreover $x_\rho \equiv \rho
\pmod 3$ gives $G \equiv \rho \iff 3 \mid (G - x_\rho) \iff v_3(G - x_\rho) \ge 1$; so the run continues precisely
while the valuation is positive, and its length is the initial valuation. $\blacksquare$

*Verified exhaustively for $G = 3, \dots, 2\cdot 10^5$ (all three residues, zero mismatches) and along the o4 orbit.*

**Corollary 2.1 (unconditional run cap).** For positive $G$, $\,3^{v_3(G - x_\rho)} \le |G - x_\rho| \le G + 14$, so
every run satisfies $R \le \log_3(G + 14)$. Along an orbit with $G_n = \Theta((4/3)^n)$ this gives
$$R_n \;\le\; n \log_3 \tfrac{4}{3} + O(1) \;\approx\; 0.262\,n.$$

## 4. The mirror coordinate

**Theorem 3 (mirror form).** *Let $W = G + 14$ ($= G - x_1$). Then*
$$3\,W_{n+1} \;=\; 4\,W_n + f(\rho_n), \qquad f(1) = 0,\quad f(2) = -13,\quad f(0) = -5 .$$
*In particular $\rho=1$ steps multiply $W$ exactly by $4/3$, and the $\rho=1$ run structure of §3 is the statement
that the process $v_3(W_n)$ decreases by $1$ per step inside a run and re-randomizes at the additive reload steps.*

*Proof.* Substitute $G = W - 14$ into (1): $3(W' - 14) = 4(W - 14) + e$, so $3W' = 4W + (e - 14)$, and
$e - 14 \in \{0, -13, -5\}$ for $\rho = 1, 2, 0$ respectively. $\blacksquare$

**Remark (the mirror ladder).** Theorem 3 exhibits the deep structure of this system as *the 3-adic depth process of
an affine $\times\frac43$ orbit*. The identical structure appears across the BB(6) cryptid kernels:

| machine | orbit map | depth process | budget |
|---|---|---|---|
| Antihydra | $c \mapsto \lfloor 3c/2 \rfloor$ | $v_2(c_n - 1)$ under $\times\frac32$ | constant (critical) |
| o4 (this paper) | $T$ above | $v_3(W_n)$ under $\times\frac43$ | grows $+3$/generation |
| o15 | $V' = (8V+c)/3$ family | $v_3(V_n - 1)$ under $\times\frac83$ | cylinder form |
| o18 (depth) | push law $m' - 1 = \frac83(m-1)$ | $v_3(m - 1)$ | no fatal set known |

(The o15 and o18 closed forms are proved by the same fixed-point argument as Theorem 2; see
`O15_FIXEDPOINT_2026-07-07.md`, `O18_DEPTH_UNIFORM_2026-07-07.md`.) All four kernels are instances of ONE open
problem: *an effective quenched upper bound on the frequency of deep $p$-adic returns of an explicit affine
$\times\frac{p}{q}$ orbit*. Depth per return is controlled unconditionally by Corollary 2.1 and its analogues; only
the frequency axis is open. The budgets grade the family by margin, giving a natural staging (easiest first: o4).

## 5. Application to the machine o4 — precise status

The lab notes `O4_TEMPLATE_CLOSURE_2026-07-06.md` establish (by a grid-certified, red-team-audited trace-template
argument — *not* yet formalized in a proof assistant) that the machine o4's evolution is, for every generation, a
rigid template whose counters evolve by $T$ (the odometer, derived there) together with a second counter
$$a_{n+1} = a_n + \delta(\rho_n), \qquad \delta(1) = -1,\quad \delta(2) = +4,\quad \delta(0) = +6,$$
and that **o4 never halts provided $a_n \ge 2$ at every $\rho_n = 1$ generation** (the "ledger condition"). The
condition is not vacuous: an explicit configuration in the template family with $a = 0$ halts.

Within that context, the theorems above give:

- **(Seed-specificity — Corollary 1.1.)** Ledger-violating itineraries exist in every neighborhood of seed space;
  no seed-uniform proof of the ledger condition can exist. Any decision of o4 must use the specific orbit.
- **(Single-run fatality is impossible — Corollary 2.1.)** A ledger drain of $-1$ occurs only at $\rho = 1$ steps,
  and maximal $\rho=1$ runs are $\le 0.262\,n + O(1)$, while the verified ledger value at generation 40 is
  $a_{40} = 124$ and every non-drain step adds $\ge 4$. Hence no single run can breach the ledger beyond a bounded,
  concretely-verified horizon; any failure requires $\gtrsim a/(0.262\,n)$ *separate* deep 3-adic returns
  $G \equiv -14 \pmod{3^{R}}$, interleaved with recoveries.
- **(Quantified heuristic margin.)** For the i.i.d.-uniform itinerary model, the ruin probability from ledger value
  $a$ is $\eta^a$ with $\eta = 0.334895\ldots$ (the root in $(0,1)$ of $(\eta^{-1} + \eta^4 + \eta^6)/3 = 1$); the
  orbit's current frontier value $a = 124$ gives $\approx 10^{-59}$. This is a heuristic for the *quenched* statement,
  which remains open.

**What is NOT claimed.** The ledger condition itself — hence the non-halting of o4 — remains **open**; the theorems
here classify and constrain its failure modes but do not close it. No machine is decided.

## 6. References to the record
Reduction and template: `O4_TEMPLATE_CLOSURE_2026-07-06.md` (red-team log included). Ledger analysis and small-a
case map: `O4_LEDGER_ANALYSIS_2026-07-06.md`. Discovery note for §§2–4: `O4_RUN_STRUCTURE_2026-07-07.md`. Mirror
instances: `O15_FIXEDPOINT_2026-07-07.md`, `O18_DEPTH_UNIFORM_2026-07-07.md`. Antihydra kernel and its literature
anchor (Andrieu–Eliahou–Vivion normality conjecture, arXiv:2510.11723): `BB6_FRAMEWORK_PACKAGE.md`.
One-command verification: `verify_all.py`.
