# The mirror ladder: every Type-I BB(6) cryptid is the p-adic depth process of an explicit ×p/q orbit

*Paper-style synthesis (theorem + census). The discovery notes are `O4_RUN_STRUCTURE_2026-07-07.md`,
`O15_FIXEDPOINT_2026-07-07.md`, `O11_REFILL_LAW_2026-07-08.md`, `O13_O14_FIXEDPOINT_2026-07-08.md`,
`O16_SPACENEEDLE_FIXEDPOINT_2026-07-08.md`, `ANTIHYDRA_LEDGER_UNIFICATION_2026-07-07.md`. One-command verification of
the whole (2,3)+(2,5)-even census: `mirror_census.py` (ALL RUN LAWS VERIFIED); the (3,4)/(3,8) v₃ forms are proven
in their own notes and in the Lean layer (`lean/RunStructure.lean`, `Suffix.lean`). No machine is decided.*

## 1. The uniform theorem

**Setup.** Each Type-I BB(6) cryptid, at its milestone abstraction, iterates a value map
$$T(v) \;=\; \Big\lfloor \tfrac{p}{q}\,v \Big\rfloor + c(v), \qquad \gcd(p,q)=1,$$
where the correction $c(v)$ is a bounded function of the branch (the residue $v \bmod q$ and, for $q=2$, the
parity). On each branch $T$ is affine: $b(v) = (p v + e)/q$ for an integer $e = e(\text{branch})$.

**Theorem (uniform fixed-point run law) `[PROVEN]`.** *Each branch map $b$ has the rational fixed point
$x = -\,e/(p-q)$; when $x \in \mathbb{Z}$, and because $p$ is a unit in the $q$-adic integers $\mathbb{Z}_q$
(as $\gcd(p,q)=1$),*
$$b(v) - x \;=\; \frac{p}{q}\,(v - x) \quad\Longrightarrow\quad v_q\big(b(v)-x\big) = v_q(v-x) - 1.$$
*Hence the maximal run of a branch starting from $v$ — the number of consecutive same-branch steps — equals
$v_q(v - x_{\text{branch}})$, and it is capped unconditionally by $\log_q\!\big(|v - x|\big)$.*

*Proof.* At the fixed point $q x = p x + e$, so $e = -(p-q)x$ and $b(v)-x = (pv+e)/q - x = (p(v-x))/q$. The map
$w \mapsto (p/q)w$ multiplies the $q$-adic value by $p$ (a unit, so $v_q$ unchanged) and divides by $q$ (drops
$v_q$ by 1); net $-1$ per step. The branch is taken exactly while $q \mid (v-x)$ (as $x \equiv$ the branch residue),
i.e. while $v_q(v-x) \ge 1$; the run length is the entry valuation. $3^{v_q(n)} \le |n|$ (resp. $q$) gives the cap. ∎

For the $q=2$ (×3/2, ×5/2) family with $T(\text{even }v)=3v/2+c_e$, $T(\text{odd }v)=(3v-1)/2+c_o$, the fixed points
close in the corrections: **$x_{\text{even}} = -2c_e$, $x_{\text{odd}} = 1 - 2c_o$**.

## 2. The census `[PROVEN run laws; verified by `mirror_census.py`]`

| machine | ×p/q | place | corrections | fixed points | run law |
|---|---|---|---|---|---|
| Antihydra | ×3/2 | $v_2$ | $(0,0)$ | $(0,\,1)$ | $v_2(c),\ v_2(c-1)$ |
| o2 (ceiling) | ×3/2 | $v_2$ | ceiling | $(0,\,1)$ | $v_2(y),\ v_2(y+1)$ |
| o16 | ×3/2 | $v_2$ | $(2,2)$ | $(-4,\,-3)$ | $v_2(s+4),\ v_2(s+3)$ |
| o11 | ×3/2 | $v_2$ | $(4,4)$ | $(-8,\,-7)$ | $v_2(m+8),\ v_2(m+7)$ |
| o14 (o11 twin) | ×3/2 | $v_2$ | $(6,6)$ | $(-12,\,-11)$ | $v_2(a+12),\ v_2(a+11)$ |
| o13 (o12-flavor) | ×3/2 | $v_2$ | $(7,4)$ | $(-14,\,-7)$ | $v_2(a+14),\ v_2(a+7)$ |
| o4 | ×4/3 | $v_3$ | $\{3,5,1\}$ | $(-9,-14,-1)$ | $v_3(G - x_\rho)$ |
| o15 / o18 | ×8/3 | $v_3$ | queued | $1$ | $v_3(V-1)$ |
| Space Needle | ×5/2 | $v_2$ | — | even $0$; **odd: none** | $v_2(m)$ (even branch) |

Every Type-I cryptid analyzed is thus **the $q$-adic depth process of an explicit affine $\times(p/q)$ orbit**. The
$q=2$ machines and o2 share Antihydra's exact $(p,q)$; only the additive offset (the correction) distinguishes them.

## 3. The one exception, and what it means

**Space Needle is the sole break in the pattern.** Its even branch $m \mapsto 5m/2$ has fixed point $0$ and the
clean law $v_2(m)$ `[PROVEN]`; its **odd branch has no single fixed point** — it is a $v$-indexed carry step
$(2^{v+1}+3)q + 2^v + v - 1$, producing the parity-branching 2-adic recursion. Correspondingly Space Needle is the
one machine that is **not $(K)$-seeded** ($5/2 \notin p^a/q^b$) and the one with a **cumulative** (non-resetting)
ledger; on the criticality/summability axis it sits alone with o4 on the cumulative side (per-epoch fatal
probability $\sim 2^{-\text{width}}$, width cumulative $\Rightarrow$ summable $\Rightarrow$ annealed non-halt-leaning).

## 4. Criticality and ledger-memory — the two secondary axes

The run law is uniform; the machines differ on two derived axes (both `[PROVEN ingredients / MODEL for the lean]`):

- **Criticality** (only for cumulative-ledger machines): single-run fatality is excluded iff (run-cap slope)/(budget
  slope) $< 1$. **Antihydra and o2 sit at $\log_2\!\tfrac32 / \tfrac12 = 1.1699 > 1$** (critical — the $1.17\times$
  barrier); **o4 at $0.087$** (freely excluded); Space Needle's slope is $\log_2\tfrac52 = 1.322$ but with no
  draining scalar ledger the ratio is inapplicable (replaced by summability). The five sea machines
  (o11/o13/o14/o16 + o15/o18) drain their budget deterministically, residue-decoupled, so the ratio is inapplicable
  in-epoch — their fatality is a per-epoch residue draw at doubly-exponentially sparse refills.
- **Ledger-memory:** *cumulative* (Antihydra, o2, o4, o3, Space Needle — the balance never re-seeds; non-halt-leaning
  when sub-critical) vs *resetting* (o11/o13/o14/o16, o15/o18 — each refill re-seeds; a.s.-halt-leaning in the
  annealed model). The annealed halt/non-halt lean splits **exactly** along this axis, frontier-wide.

## 5. Consequence

The whole Type-I frontier is one problem in $|\text{family}|$ coordinates: **an effective quenched bound on the
frequency of deep $q$-adic returns ($v_q(v-x) \ge \ell$) of an explicit affine $\times(p/q)$ orbit.** The uniform
theorem controls the *depth* axis unconditionally (Theorem §1 + its cap); every machine's open protection is the
*frequency* axis. The margin ladder — Antihydra/o2 critical, o4 easiest, the sea machines' sparse resetting draws,
Space Needle's cumulative summable lean — orders the family and is the staging for the missing effective-equidistribution
tool. No cryptid is decided; the depth structure is now uniform and, for the $(3,\cdot)$ machines, Lean-checked.

## References to the record
Discovery notes as listed in the header; criticality framework `ANTIHYDRA_LEDGER_UNIFICATION_2026-07-07.md`;
species/memory axes `BB6_CRYPTID_SPECIES_2026-07-07.md` + `O18_ANNEALED_STANDOFF_2026-07-07.md`; Lean forms
`lean/RunStructure.lean`, `lean/Suffix.lean`; census verifier `mirror_census.py`. The kernel's external anchor
(Andrieu–Eliahou–Vivion, arXiv:2510.11723) is in `BB6_FRAMEWORK_PACKAGE.md`.
