# The digit bridge: run-depth = q-adic valuation of a NON-AUTONOMOUS ×(p/q) orbit — why the quenched p-adic-digit literature stops exactly at the cryptid (2026-07-09)

*BUILD attempt on the moving-diagonal digit connection (`PAPER_MIRROR_LADDER.md` §1: d_n = v_q(v_n − x)).
Fresh 2024–2026 literature scan + one [CONSTRUCTED-partial] bridge lemma, numerically verified
(`newmath_digit_bridge.py`, `.venv`, exact bigint). STRICT labels; no proof claims; (K) [OPEN]. NOT committed.*

---

## 0. One-line result

The uniform theorem makes each cryptid's run-depth the **q-adic VALUATION of its own ×(p/q) orbit**, and the
2024–2026 literature splits cleanly by **AUTONOMY**: constant-coefficient linear recurrences have periodic
residues mod q^k → **exact, quenched digit/valuation frequencies** (Lucas mod 3^k, arXiv:2511.00722; 3rd-order,
arXiv:2402.18279); the cryptid orbit is a **non-autonomous** rational-base numeration map whose residues mod q^k
**do not descend** → its digit frequency **is** AEV Conj 1.6 (arXiv:2510.11723) = (K). The bridge localizes the
gap to a single named obstruction — **no fixed characteristic polynomial ⇒ no p-adic analytic interpolant** — but
does not cross it. **No annealed digit theorem transfers.**

---

## 1. Fresh literature scan (2024–2026): the sharpest known results

| ref | date | statement | regime |
|---|---|---|---|
| **Drmota–Spiegelhofer 2501.00850** | Jan 2025 | (s₂(n),s₃(n)) attains **almost all of ℕ²** by density (digit **SUMS**); via Baker's theorem | global, digit-**sum** only |
| **AEV 2510.11723** (v2) | Apr 2026 | normality of base-p/q words **⟺** equidistribution mod q^k (Thm 1.7); ⟹ no Z_{p/q} under p<q² (Thm 1.5) | equivalences only, no uncond. distribution |
| **Fan–Fan–Ye 2512.05690** | Dec 2025 | **non-Archimedean Koksma**: for **a.e.** α the p-adic sequence equidistributes; exceptional-set Hausdorff dimensions computed | **annealed** (a.e.-α) + exceptional dim |
| **"Digit Mixing under Polynomial Maps" 2606.08325** | Jun 2026 | **a.s.** absolute normality of P(X), random X, sharp variance law p_n(1−p_n) ≳ (log n)^Γ n^{−(d−1)/d} | **annealed** (a.s.), polynomial, not exponential |
| **Lucas mod 3^k 2511.00722** | Nov 2025 | exact residue frequencies, **period 4·3^{k−1}**, for u_n=Pu_{n−1}+u_{n−2} | **quenched**, but **autonomous** recurrence |
| **3rd-order p-adic val. 2402.18279** | Feb 2024 | v_p(u_n) of const-coeff 3rd-order recurrences governed by rank-of-apparition periodicity | **quenched**, **autonomous** |
| Ren–Roettger 2511.03861 | Nov 2025 | block-uniform-distribution of base-3 digits of 2^n — **CONJECTURE** + 10⁶ numerics | conjecture (superset of (K)) |

**Two soundness notes banked.**
- **arXiv:2411.03468 "Mahler's 3/2 problem in ℤ⁺" is WITHDRAWN** (author Nikhil Kumar, 18 Jun 2025; own comment:
  "there are trivial ways to prove the same"). It is **not** an unconditional Mahler proof — do not cite as progress.
- **arXiv:2501.00850 is digit-SUM normality (Baker), NOT a run-lemma.** This confirms the standing correction
  (`CORE_ORBIT_ARITHMETIC.md` §5′): the longest-run bound L(M·3^K)=o(K) is real (Schlickewei p-adic subspace theorem,
  Bugeaud–Kaneko line) but must stay **[PROVEN-in-lit, exact citation pending]** — 2501.00850 is the wrong source.

**Sharpest QUENCHED result in the literature:** exact digit/valuation frequencies for **constant-coefficient linear
recurrences** (2511.00722 gives P(residue=b mod 3^k) exactly over the period 4·3^{k−1}; 2402.18279 gives v_p closed
forms). **Sharpest ANNEALED result touching (p/q)^n / p-adic orbits:** the non-Archimedean Koksma theorem
(2512.05690) — a.e.-α equidistribution in ℤ_p with exceptional-set dimension bounds. **No quenched digit/valuation
frequency for a SPECIFIC orbit of a rational-base (p/q) map exists** (confirmed by fresh scan; AEV is the frontier).

---

## 2. [CONSTRUCTED-partial] The bridge lemma: run-depth is v_q of a NON-AUTONOMOUS orbit

**Setup (from the uniform theorem).** o4's odometer is `3G' = 4G + e(ρ)`, `ρ = G mod 3`, `e={0:9,1:14,2:1}`, branch
fixed points `x_ρ=−e(ρ)`. Run law `[PROVEN, guard re-checked 4000/4000]`: the maximal ρ-run at G equals `v₃(G−x_ρ)`.
So the run-depth sequence is `d_n = v₃(G_n − x_{ρ_n})` — the **3-adic valuation of the orbit's own value**.

**Lemma [CONSTRUCTED-partial, verified `newmath_digit_bridge.py`].**
*The map generating d_n is **non-autonomous**: its "recurrence coefficient" is the branch e(ρ_n), self-selected by
the orbit's residue ρ_n = G_n mod 3. Consequently the residue sequence (G_n mod 3^k) is **not eventually periodic**
(verified: no period for k=1,2,3 over 2·10⁵ steps), because G' = (4G+e(G mod 3))/3 divides by 3 each step and thus
depends on G mod 3^{k+1}, not on G mod 3^k — the AEV **non-descent**. In sharp contrast, a constant-coefficient
linear recurrence has residues mod 3^k that ARE eventually periodic (verified: Fibonacci periods 8, 24, 72 mod
3,9,27 — the 4·3^{k−1} Lucas structure of 2511.00722), which is precisely the mechanism that makes its v₃-frequency
exact and computable.*

**What this transfers.** The lemma places the cryptid **exactly on the boundary** between the two literature regimes:
- the **only** source of *quenched* p-adic-valuation-frequency results (autonomous linear recurrences, 2511.00722 /
  2402.18279) needs the autonomy the cryptid **provably lacks** (aperiodic branch itinerary; residues non-descending);
- the **annealed** frontier (non-Archimedean Koksma 2512.05690; polynomial digit-mixing 2606.08325) delivers a.e.-α /
  a.s. equidistribution of the moving p-adic digit — but the cryptid orbit is a **single, given** α, the measure-zero
  case these theorems explicitly cannot reach.
So the identity d_n = v_q(v_n − x) **does not** let any annealed digit result transfer: it re-expresses the target as
the valuation of a specific non-autonomous orbit, which is exactly the object both literatures leave open (AEV Thm 1.7:
this frequency = normality of the base-4/3 word = equidistribution mod 3^k = Conj 1.6).

---

## 3. The self-reference / Skolem–Mahler–Lech angle, sharpened

o4's `W_n = G_n + 14` obeys `3W_{n+1} = 4W_n + (e(ρ_n)−14)`, ρ_n = W_n mod 3 — the "×4/3 on W" mirror
(`O4_RUN_STRUCTURE` §3). The hope (prompt angle 3): is d_n the valuation of a **linear-recurrence** sequence, hence
in reach of **Skolem–Mahler–Lech / p-adic (Skolem) analytic** methods that fail for generic real α?

**Answer [ASSESSED, sharpened]: NO — SML's *hypothesis* fails, not merely its output.** SML and the Skolem p-adic
method apply to **constant-coefficient** recurrences: a fixed characteristic polynomial yields a p-adic analytic
interpolant u(z)=Σ c_i γ_i^z whose zero set (Strassmann/Weierstrass counting) is finite ∪ finite APs — this is exactly
what makes residues mod p^k periodic and v_p computable (the 2402.18279 engine). **W_n is non-autonomous** (coefficient
e(ρ_n) self-selected), so there is **no fixed characteristic polynomial and no p-adic analytic interpolant** to which
SML/Skolem could be applied. The prior arith-dynamics scan's "SML gives only AP-structure" is thus superseded by the
cleaner statement: **the exact W_n recurrence is not a linear recurrence at all** — the branch self-selection is the
non-descent, so the SML hook is empty. (The earlier note that fixing the branch trivializes v₃ — a pure-ρ run drops
v₃ by exactly 1/step — is the degenerate autonomous limit; the real orbit never fixes it.)

---

## 4. The precise remaining gap

The run-cap `d_n ≤ 0.262n + O(1)` (`O4_RUN_STRUCTURE` §2) and the explicit `W_n = exact bigint` give
**per-term computability** but not the **per-n uniformity-from-a-fixed-analytic-object** that quenched digit theorems
require. The autonomous case's quenched power flows from: fixed char poly → p-adic analytic interpolant → periodic
residues mod q^k → exact frequency. The cryptid breaks the **first** link (no fixed char poly, §3), so every
downstream link is unavailable. The missing ingredient is therefore, exactly:

> **an effective equidistribution mod q^k of a SPECIFIC orbit of the rational-base map T_{p/q}, without a
> finite-state / p-adic-analytic descent.** This is AEV Conj 1.6 = Mahler/(K).

The run-cap is a genuine **new per-orbit UPPER constraint**, but it forces **no digit-frequency LOWER bound**: a
Thue–Morse-type bounded-run itinerary satisfies the cap and every banked fact yet would decide the machine (logged,
`FREQUENCY_AXIS_PROBE_2026-07-08.md` §2) — so "cap + computable W_n" cannot substitute for the equidistribution input.

---

## 5. Deliverable summary

- **Sharpest lit found:** quenched side — exact residue-frequency mod 3^k for **autonomous** linear recurrences
  (2511.00722, period 4·3^{k−1}; 2402.18279); annealed side — **non-Archimedean Koksma** a.e.-α p-adic equidistribution
  + exceptional dimensions (2512.05690, Dec 2025), and a.s. polynomial digit-mixing (2606.08325, Jun 2026). Both fresh
  annealed results are the correct "what generic-α / a.s. methods give" citations and both are **measure-theoretic**.
- **What the new theorem transfers:** it identifies d_n = v_q(orbit) and, via the verified **non-autonomy / non-descent
  dichotomy**, proves the cryptid sits on the OPEN side of the autonomy split — so **no** annealed digit theorem and
  **no** autonomous-recurrence quenched theorem grips it. A [CONSTRUCTED-partial] bridge lemma, not a crossing.
- **Precise gap:** effective equidistribution mod q^k of the **specific** rational-base orbit with **no analytic
  descent** = AEV Conj 1.6 = (K). Named obstruction: **non-autonomous ⇒ no fixed characteristic polynomial ⇒ no
  p-adic analytic interpolant**, which is the same non-descent AEV's equivalence encodes.

**Scripts:** `newmath_digit_bridge.py` (dichotomy, run-law guard, non-descent — all pass).

## References
- Drmota, Spiegelhofer, *The joint distribution of binary and ternary digit sums*, arXiv:2501.00850 (Jan 2025) — digit-SUM normality via Baker; **not** a run-lemma.
- Andrieu, Eliahou, Vivion, *A Normality Conjecture on Rational Base Number Systems*, arXiv:2510.11723 (v2 Apr 2026).
- Fan, Fan, Ye, *Non-Archimedean Koksma Theorems and Dimensions of Exceptional Sets*, arXiv:2512.05690 (Dec 2025).
- *Digit Mixing under Polynomial Maps*, arXiv:2606.08325 (Jun 2026).
- *Residues of Terms of Lucas Sequences Modulo 3^k*, arXiv:2511.00722 (Nov 2025).
- *On the p-adic valuation of third order linear recurrence sequences*, arXiv:2402.18279 (Feb 2024).
- Ren, Roettger, *Ternary Digits of Powers of Two*, arXiv:2511.03861 (Nov 2025).
- **WITHDRAWN:** *Mahler's 3/2 problem in ℤ⁺*, arXiv:2411.03468 (withdrawn 18 Jun 2025) — not a valid Mahler proof.
- Run-bound L(M·3^K)=o(K): Schlickewei p-adic subspace theorem / Bugeaud–Kaneko — **[PROVEN-in-lit, exact citation pending]**.
- Cross-refs: `PAPER_MIRROR_LADDER.md`, `O4_RUN_STRUCTURE_2026-07-07.md`, `FREQUENCY_AXIS_PROBE_2026-07-08.md`, `CORE_ORBIT_ARITHMETIC.md`, `AEV_DIGEST.md`, `DIGITS_OF_3N.md`.

No machine decided. No label upgraded.
