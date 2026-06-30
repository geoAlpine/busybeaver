# The 3-adic sliding-block lock: the ℚ₃ place is an automatic factor of the 2-adic depth process (2026-06-30)

*Banked structural fact (roadmap re-examination, user request 1). SHARPENS the known `THREEADIC_ROTATION.md`
result ("`o_j mod 3^k` is measure-isomorphic to / driven by the depth sequence `D`, no free equidistribution") to
an EXACT causal form: the `k`-th 3-adic digit of the orbit is determined by exactly the `k` most recent depths.
CONSEQUENCE: answers `EMPTY_TOOLBOX_QUESTION.md` Q-B in the negative — the solenoid's "extra contracting 3-adic
direction" is a sliding-block-code factor of the 2-adic depth process, carrying NO leverage independent of the
2-adic problem. SOUNDNESS: the lock is `[PROVEN]` (algebraic, below) and verified by exact big-int data to `3^6`.
This CONFIRMS a wall, does not breach it; no label upgraded; `(K)` stays `[OPEN]`. NOT committed by default.*

---

## 0. The lock `[PROVEN]`

Induced odd map `o_{j+1} = 3^{D_j−1}(3o_j−1)/2^{D_j}`, `D_j = v₂(3o_j−1)`, `o_0 = 27`. Since `3o_j−1 ≡ −1 (mod 3)`
is a 3-adic **unit** and `2` is a 3-adic unit, `v₃(o_{j+1}) = D_j − 1` and the 3-adic **unit part** is, exactly in
`ℤ₃^×`,

> **`[PROVEN]`** `unit(o_{j+1}) := o_{j+1}/3^{D_j−1} = (3o_j − 1)·2^{−D_j}` (in `ℤ₃^×`).

> **Sliding-block lock `[PROVEN]`.** `unit(o_{j+1}) mod 3^k` is a deterministic function of exactly the depth
> window `(D_j, D_{j−1}, …, D_{j−k+1})` — and of no earlier history. Equivalently the orbit's 3-adic word
> `(unit(o_j))_j` is the image of the depth sequence `(D_j)_j` under a **causal sliding block code** `Ψ` whose
> `k`-th output digit reads the `k` most recent input depths.

**Proof (induction on `k`).** `unit(o_{j+1}) mod 3^k = (3o_j−1)·2^{−D_j} mod 3^k`. The factor `2^{−D_j} mod 3^k`
depends only on `D_j mod ord_{3^k}(2)` (so only on `D_j`). The factor `(3o_j−1) mod 3^k` needs `o_j mod 3^{k−1}`.
Now `o_j = 3^{D_{j−1}−1}·unit(o_j)`: if `D_{j−1}−1 ≥ k−1` then `o_j ≡ 0 (mod 3^{k−1})`, so `3o_j−1 ≡ −1`, fixed by
`D_{j−1}` alone; otherwise `o_j mod 3^{k−1}` needs `unit(o_j) mod 3^{k−D_{j−1}}`, which by the inductive hypothesis
reads the window `(D_{j−1}, …)` of length `k−D_{j−1}`. Each step backward consumes `≥1` of the budget `k` (one per
3-adic digit when the intermediate depth is `1`, more when it is larger), so the total history read is a window of
length `≤ k`, attained `= k` in the all-`D=1` worst case. ∎

**Data (exact big-int, `o_0=27`, `N=2·10⁵` induced steps, `scratchpad/chainlock.py`):** for each `k=1..6`, the
window `(D_j,…,D_{j−k+1})` determines `unit(o_{j+1}) mod 3^k` for **100% of samples** (17/17, 155/155, 829/829,
3215/3215, 9540/9540, 22877/22877 predictor cells, each a single value). Control: a length-`k` window does **not**
determine the `(k+1)`-th digit (`mod 3^{k+1}` splits in most cells) — so the window length is **exactly** `k`,
confirming the triangular/causal structure of `Ψ`. The leading digit recovers the known parity law
`unit(o_{j+1}) ≡ (−1)^{D_j−1} (mod 3)` (`= (−1)^{v₃(o_{j+1})}`), e.g. `(D_j,D_{j−1})→unit mod 9`: `(1,1)→1`,
`(1,≥2)→4`.

---

## 1. Consequence — the ℚ₃ place carries no independent σ-algebra `[PROVEN]`

The depth sequence `(D_j)` is a function of the 2-adic coordinate alone (`D_j = v₂(3o_j−1)`, read off `o_j mod 2^∞`).
The lock says the entire 3-adic word is `Ψ((D_j))` — a continuous, shift-commuting **factor** of the depth process.
Hence:

- **The ℚ₃ marginal of the orbit's limit measure is a factor of the 2-adic depth process**, not an independent
  direction. Its equidistribution (3-adic-word genericity) is *equivalent* to depth-sequence genericity, with no
  slack: `Ψ` is deterministic and finitary, so it transports genericity in both directions (a sliding block code
  neither creates nor destroys a generic point).
- **This is the strongest form of the anti-lever** (`AIU_THIRD_MECHANISM_PROBE.md`): AIU = `ℚ₃`-rotation invariance
  of the leaf conditionals is not merely "coupled to" the depth statistics — it is a deterministic image of them,
  so the neutral `ℚ₃` direction supplies literally zero degrees of freedom beyond the 2-adic depth process.

## 2. Answer to `EMPTY_TOOLBOX_QUESTION.md` Q-B (negative) `[PROVEN-backed]`

Q-B asked whether "the solenoid's **extra contracting 3-adic (stable) direction** is a genuine lever the bare real
`{(3/2)ⁿ}` lacks." **Answer: no.** The 3-adic place is the sliding-block-code factor `Ψ((D_j))` of the 2-adic depth
process; it adds no information and no leverage. The solenoid placement (rank-1-in-rank-2 host, §5 of the package)
remains a correct and useful *framing* — it names AIU + ENT and connects to proven Rudolph–Johnson — but the hope
that the `ℚ₃` direction is an independent handle is now closed: any control of the 3-adic side is, by `Ψ`, a control
of the 2-adic depth side, i.e. `(K)` itself. The genuine degrees of freedom live entirely in the 2-adic coordinate
(see `MINIMAL_CORE_2ADIC.md`).

## 3. Honest scope

This is a refinement of a wall, not a breach. It (i) upgrades `THREEADIC_ROTATION.md`'s "measure-isomorphic to `D`"
to an exact causal sliding-block code, (ii) gives the anti-lever its strongest form, and (iii) closes the Q-B
"3-adic lever" hope. It does **not** prove or disprove `(K)`, and it does not provide a new attack — on the
contrary, it shows the 3-adic/solenoid apparatus cannot, by itself, since it is downstream of the 2-adic depth
process by a deterministic code. **No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
