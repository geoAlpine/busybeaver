# New-methods sweep (2026-06-30): four fresh probes, one convergence, one hairline crack

*Synthesis of four parallel new-method probes run on the minimal core (`MINIMAL_CORE_2ADIC.md`): single specified
2-adic Bernoulli orbit `o_0=27`, want `liminf` depth-mean `≥ 3/2` `= (K)`. Each probe was run under zero-false-proofs
discipline and forbidden from claiming `(K)`. SOUNDNESS: all four verdicts are NEGATIVE-or-clarifying; no label
upgraded; `(K)` stays `[OPEN]`. The value is (i) a quantitative localization of the wall that TWO independent probes
converged on, (ii) a logical-complexity classification, (iii) a computational confirmation, (iv) one named hairline
crack. NOT committed by default.*

---

## 0. Verdicts (all four)

| Probe | File | Verdict | Core finding |
|---|---|---|---|
| Tao/Syracuse technical drill | `TAO_SYRACUSE_DRILL.md` | **same wall, located** | needed input = finite-scale 2-adic equidist of the start to **linear** depth `~2n` (Tao Prop 1.9, hyp 1.11); quenched onto our orbit the char-fn bound (Prop 1.17) collapses to a single phase, modulus 1, zero decay |
| Proof-theoretic / independence | `LOGIC_INDEPENDENCE_PROBE.md` | **dead end as attack, clarifying** | `(K)` and non-halting are `Π⁰₁` (syntactic `Π⁰₃` collapses via `ΣD_i=n+v₂(c_n)−v₂(c_0)`); No-Structure ≠ PA-independence (category error); independence `~3–7%`, untouchable; "true-but-hard `Π₁`, Collatz species" |
| SOS / computational certificate | `SOS_CERTIFICATE_SEARCH.md` | **confirmed closed (computational)** | `β=sup_ν∫ψ dν=+1/2` exactly, `k=3..12` (δ₁ atom); magnitude-aware Lyapunov feasible only above a vacuous threshold, useful sign infeasible; nonlinear/piecewise die by the identical δ₁ mechanism; thresholding localizes the difficulty to `(K)` |
| Divergent new-angle generator | `NEW_ANGLES_DIVERGENT.md` | **space ≈ closed; 1 hairline crack** | 11 attack-kinds, 9 DEAD (heavy-tail white adversary kills 7); 2 least-dead (#1 Ostrowski/Diophantine, #2 adaptive Oseledets), their **combination** narrowly `WORTH-A-PROBE` |

## 1. The convergence — the wall is a LOG-vs-LINEAR depth-reach gap `[PROVEN-backed localization]`

Two independent probes landed on the **same** quantitative gap, which is the sharpest localization of the wall to date:

- **Tao drill**: his machinery (Prop 1.9) needs the start to be 2-adically equidistributed to depth `n_0 ≥ (2+c_0)n`
  — i.e. **linear** depth `Θ(n)`. That hypothesis (1.11) IS single-orbit 2-adic equidistribution = Mahler 3/2.
- **Divergent #1 (Diophantine)**: the finite irrationality measure of `log₂3` controls the orbit only at the **top
  `Θ(log N)` digits** (the banked top-digit / foothold partial, `k(N)/log₂N ≈ 0.85`) — **logarithmic** depth. The
  parity/depth bit that `(K)` reads lives at depth `Θ(j)` — **linear**.

> **The gap, named.** Every unconditional tool reaches **logarithmic** 2-adic depth; `(K)` (and Tao's quenched
> hypothesis) needs **linear** 2-adic depth. The missing factor is `Θ(n)/Θ(log n) = Θ(n/log n)` of depth-reach. This
> is the same wall as the moving-diagonal-of-`3ⁿ` frontier (`CORE_DIGITS3N_FRONTIER.md`), now quantified as a
> depth-reach ratio. `[PROVEN that available tools reach log-depth; that (K) needs linear-depth]`

This does not crack `(K)`, but it converts "the orbit is not equidistributed-enough" into a precise, citable
quantity (log-depth have / linear-depth need) — the cleanest single sentence to hand an effective-equidistribution
specialist.

## 2. The one hairline crack — PROBED, now CLOSED `[COLLAPSE, exact line pinned — HAIRLINE_CRACK_PROBE.md]`

> **UPDATE (probed 2026-06-30, `HAIRLINE_CRACK_PROBE.md`): the #1+#2 combination COLLAPSES on the log-vs-linear gap,
> exact line pinned.** `[PROVEN-backed]` (i) #2 genuinely needs **linear** depth: its surviving conjecture (CR) must
> certify the fresh bit `β_n = bit_k(c_n)` at the moving-middle position `≈ n+k = Θ(n)` deep is unbiased vs the low
> state `c_n mod 2^k` uniformly as `k→∞`; no log-depth functional equals that. (ii) #1 controls only the top
> `Θ(log N)` bits (foothold `k(N)/log₂N ≈ 0.84` re-confirmed), and a fresh mutual-information check finds it
> **statistically independent of the depth/parity bit** (`≈10⁻⁵` bits vs a 4-bit max) — so it cannot drive #2.
> (iii) Adaptivity does **not** break the infinite scale-regress: an orbit-built weight is conjugation-invariant for
> the coisometry cocycle (`‖Φ‖≡1`), and the depth-amplifying inducing map gains only `O(1)` depth per level while
> exhausting the orbit before reaching depth `Θ(n)`. (iv) Seam transfer fails on the exact line
> `bit_k(c_n) = bit_{n+k}(8·3ⁿ) ⊕ bit_{n+k}(S_n) ⊕ ρ_n`: the carry term `S_n` at precision `n+k` is built from
> `b_0…b_n` = the depth data itself (circular), and the carry-free term is the `Θ(n)`-deep moving-middle diagonal
> where van der Corput is proven closed. The only saving sub-lemma is `(CR)/(SL)` itself `= (K)`, **not weaker** — no
> intermediate object lives in the `Θ(n/log n)`-wide gap. The last untried thread is closed.

*Original assessment (now confirmed by the probe above):*

The divergent generator's only non-dead candidate is the **combination #1+#2**:
- **#2 (adaptive unbounded Oseledets / data-direction certificate)** is the one shape the coisometry no-go
  (`P-EUE`) explicitly leaves open (it rules out only *uniform/operator-norm* contraction); being unbounded it also
  escapes the δ₁/LP gate that killed every bounded and magnitude-aware template (§SOS). Its gap: the
  threshold-crossing sub-lemma reduces to `(K)`.
- **#1 (Ostrowski/Diophantine data)** is the only separator both adversaries lack (the heavy-tail adversary has no
  archimedean `(3/2)ⁿ` shadow; δ₁ sees no rotation).
- **The idea**: let #1 supply the orbit-specific, non-annealed data that #2 needs to make its adaptive weight without
  circularity.

> **Honest triage `[LIKELY DEAD]`.** The combination almost certainly collapses on the **same log-vs-linear gap (§1)**:
> #1's Diophantine data reaches only log-depth, but #2's adaptive certificate needs the depth bit at linear depth, so
> #1 cannot supply data where #2 needs it. The two independent collapses (Tao; Divergent #1) both being the log-vs-linear
> gap is strong evidence the combination inherits it. It is the *only* untried combination, so a single focused probe
> could confirm/refute it — but the prior is low (the program's proven walls stop just short of it, and the gap that
> stops them is the one the combination must cross).

## 3. Net

All four probes confirm the space is closed; none cracks `(K)` or yields a new partial toward it. Durable gains:
(i) the **log-vs-linear depth-reach localization** (§1, two independent probes converged) — the sharpest quantitative
statement of the wall; (ii) the **`Π⁰₁` classification** (`(K)` is true-but-hard Collatz-species, not
engineered-independence — independence `~3–7%` and untouchable); (iii) **computational confirmation** of the
`β=+1/2` / δ₁ wall across `k=3..12` and of the infeasibility of every (bounded, magnitude-aware, nonlinear,
piecewise) certificate; (iv) the named **hairline crack** (#1+#2), honestly triaged as likely dead on the
log-vs-linear gap, the only untried combination. **No machine decided. No label upgraded.** `(K)` remains `[OPEN]`
= Mahler 3/2 / AEV.
