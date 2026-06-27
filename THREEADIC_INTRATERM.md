# Intra-term 2-adic × 3-adic self-consistency — the (e_j, D_j) pair and the 3→2 feedback channel (2026-06-28)

*Angle: the explicitly un-mined thread flagged in `ADELIC_COUPLING.md §live-next` and
`SESSION_2026-06-28_ADELIC_KERNEL.md`. Each induced term `o_j` carries a PAIR of valuations,
simultaneously determined: `e_j = v3(o_j) = D_{j-1}−1` (3-adic, from the previous step's coupling) and
`D_j = v2(3 o_j − 1)` (2-adic, controls the next 3-adic valuation). Probe whether the pair `(e_j, D_j)`
is JOINTLY constrained — a forbidden combination, a parity link, or a one-sided bound — beyond what each
place gives alone. Numerics `.venv` only (`scratchpad/intraterm.py`, `intraterm2.py`, exact big-int,
3·10^5 induced steps from `o0=27`). Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

There is a **genuine arithmetic feedback channel 3-adic → 2-adic**: writing `o_j = 3^{e_j} u_j` with
`u_j` coprime to 6, one has `D_j = v2(3^{e_j+1} u_j − 1)`, and the term `3^{e_j+1}` is a non-trivial
rotation of the 2-adic units (`3` has order `2^{k−2}` mod `2^k`). For **fixed** `u` the map `e ↦ D` is an
explicit, non-constant deterministic function `[PROVEN, §3]` — so the channel is real, not heuristic.
**But the channel is NULL on the orbit `[PROVEN structural + OBSERVED, §4]`:** the rotation `3^{e+1}` is a
**Haar-measure-preserving bijection** of `Z_2^*`, so the *only* way `e_j` can influence `D_j` is through a
statistical dependence of the cofactor `u_j` on `e_j` — and along the orbit `u_j ⊥ e_j` to measurement
precision. Consequences, all `[OBSERVED]` to 3 dp over 3·10^5 steps:

- joint `(D_{j−1}, D_j)` factorises: `P(a,b) ≈ 2^{−a}·2^{−b}`, `χ²=30.0` on `dof=25` (`p≈0.22`),
  `corr = −0.004`;
- `E[D_j | D_{j−1}=a] ≈ 2.00` and `P(D_j=1 | D_{j−1}=a) ≈ 0.500` for **every** `a` (hence every `e`);
- the marginal of `D_j` equals the marginal of `v2(u_j−1)` (the rotation **stripped**) — identical
  geometric shape, confirming the rotation moves no mass;
- second-order `E[D_j | D_{j−2}, D_{j−1}]` is also flat at `≈2.00`.

**No forbidden pair, no parity link, no one-sided constraint emerges. Cross-correlation 0 confirms
independence.** The pair `(e_j, D_j)` is jointly *unconstrained* exactly to the extent that `u_j` is
Haar-generic and independent of its own 3-adic exponent — which is, once again, the single-orbit
genericity / Mahler wall, now expressed as an **independence (not equidistribution) statement** about the
cofactor sequence. This is the cleanest disposal yet of the "two-valuations-at-one-term" hope: the
coupling that *exists* (the channel) is annihilated by an independence that *is* the open core.

---

## 1. The pair made precise `[PROVEN]`

For odd `o>1`, `N = 3o−1`, `D = v2(N)`, the induced map is `o' = 3^{D−1}·(N/2^D)`. Two facts pin the pair:

- **(prev → this term, 3-adic)** `3o−1 ≡ −1 (mod 3)` ⟹ `3 ∤ (3o−1)` ⟹ the odd part `m = N/2^D` is coprime
  to 3, so `v3(o') = (D−1) + v3(m) = D−1`. Hence along the orbit `e_j := v3(o_j) = D_{j−1} − 1`. `[PROVEN]`
  (re-confirmed here: holds for all `j≥1` over 3·10^5 steps, 0 exceptions).
- **(this term, 2-adic)** `D_j = v2(3 o_j − 1)`. Writing `o_j = 3^{e_j} u_j` with `gcd(u_j,6)=1`:
  > **`D_j = v2(3^{e_j+1} u_j − 1)`.** `[PROVEN — identity]`

So the **pair** is `(e_j, D_j) = (D_{j−1}−1, D_j)`: the `e`-sequence is the `D`-sequence shifted and
decremented by 1. The orbit's only freedom is the cofactor sequence `u_j ∈ Z_2^*` (odd, 3-free).

---

## 2. Joint law of `(D_{j−1}, D_j) = (e_j+1, D_j)` — independence `[OBSERVED]`

Joint empirical distribution `P(D_{j−1}=a, D_j=b)` (rows `a`, cols `b`, last col `=≥6`), 3·10^5 steps:

```
 a\b      1       2       3       4       5      ≥6
  1   0.2511  0.1248  0.0630  0.0310  0.0157  0.0160
  2   0.1251  0.0631  0.0311  0.0154  0.0076  0.0076
  3   0.0631  0.0313  0.0151  0.0077  0.0037  0.0039
  4   0.0307  0.0153  0.0079  0.0039  0.0020  0.0019
  5   0.0158  0.0076  0.0039  0.0018  0.0008  0.0008
 ≥6   0.0158  0.0077  0.0039  0.0019  0.0009  0.0009
```

Every cell `≈ 2^{−a}·2^{−b}` (product of geometric marginals). **No zero cell ⟹ no forbidden pair.**
`χ² = 30.03` on `dof = 25` (Wilson–Hilferty `p ≈ 0.22`); `pearson corr(D_{j−1}, D_j) = −0.0042`.
**Conclusion: `(D_{j−1}, D_j)` are independent to measurement precision; consistent with the §0 verdict.**

---

## 3. The 3→2 channel is REAL (fixed cofactor) `[PROVEN]`

`D_j = v2(3^{e_j+1} u_j − 1)` depends on `3^{e_j+1} mod 2^k`. Since `3` generates a cyclic group of order
`2^{k−2}` in `(Z/2^k)^*` (k≥3), `3^{e+1} mod 2^k` genuinely rotates with `e`. For a **fixed** unit `u`,
`e ↦ D` is therefore a concrete non-constant function:

```
 u= 1:  D(e=0..11) = [1, 3, 1, 4, 1, 3, 1, 5, 1, 3, 1, 4]   (2-adic ruler / LTE pattern)
 u= 5:  D(e=0..11) = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
 u= 7:  D(e=0..11) = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
 u=11:  D(e=0..11) = [5, 1, 3, 1, 4, 1, 3, 1, 6, 1, 3, 1]
```

(`u=1` is the textbook `v2(3^{e+1}−1)`: `=1` for `e+1` odd, `=2+v2(e+1)` for `e+1` even, via LTE.)
**The 3-adic exponent `e` DOES feed the 2-adic depth `D` deterministically once the cofactor is frozen.**
This is the candidate "feedback loop": 3-adic data → 2-adic `D_j` → next 3-adic `e_{j+1}=D_j−1` → …

---

## 4. …but the channel is NULL on the orbit `[PROVEN structural + OBSERVED]`

**Structural reason `[PROVEN]`.** The rotation `r_e : x ↦ 3^{e+1} x` is a **bijection of `Z_2^*`
preserving Haar measure** (multiplication by a unit). If `u_j` were Haar-random in `Z_2^*` and
**independent of `e_j`**, then `W_j := 3^{e_j+1} u_j` is Haar-random *regardless of `e_j`*, so
`D_j = v2(W_j − 1)` is geometric (`P(D=k)=2^{−k}`) **independent of `e_j`**. Thus **the only way `e_j` can
influence `D_j` is a dependence of `u_j` on `e_j`.** The feedback loop closes only if the cofactor
sequence remembers the 3-adic exponent.

**Empirical reason `[OBSERVED]` — it does not.** Along the orbit `u_j ⊥ e_j` to precision:

| test | result |
|---|---|
| `E[D_j \| D_{j−1}=a]` for `a=1..10` (i.e. all `e=0..9`) | all `∈ [1.95, 2.02] ≈ 2.00` |
| `P(D_j=1 \| D_{j−1}=a)` | all `≈ 0.500` (range 0.498–0.513, within noise) |
| `E[D]`, `P(D=1)` by `(e+1)` parity | `(2.0/0.500)` even vs `(2.0/0.502)` odd — flat |
| `E[D]`, `P(D=1)` by `e mod 4` | `2.00 / 0.50` across all four classes |
| `χ²(e parity vs u mod 4)` | `1.68`, `dof=1`, `p≈0.19` (independent) |
| marginal `D_j` vs marginal `v2(u_j−1)` (rotation **stripped**, `e→−1`) | identical geometric shape, both mean ≈ 2.00 |
| 2nd-order `E[D_j \| D_{j−2},D_{j−1}]` (9 classes) | all `≈ 2.00`, `P(D=1)≈0.50` |

The marginal-match line is decisive: stripping the rotation entirely (computing `v2(u_j−1)` instead of
`v2(3^{e_j+1}u_j−1)`) leaves the depth distribution **unchanged** — the rotation moves no probability mass,
because the cofactors already fill `Z_2^*` Haar-uniformly and the rotation merely permutes a uniform set.

> **Verdict `[PROVEN structural; OBSERVED null]`.** The 3-adic→2-adic feedback channel
> `e_j ↦ D_j` via `3^{e_j+1} mod 2^k` is a genuine deterministic channel (§3) but contributes **zero**
> constraint on the orbit because (i) the rotation is Haar-preserving, so it can only transmit `e`→`D`
> information through `u_j`'s dependence on `e_j`, and (ii) measurement shows `u_j ⊥ e_j`. No joint
> constraint, no forbidden combination, no parity link, **no one-sided bound**. Cross-corr 0 confirms
> independence.

---

## 5. Where this lands relative to the wall `[PROVEN-honest]`

The intra-term probe does **not** breach, but it sharpens the obstruction in a useful way:

- The hoped-for leverage was that `e_j` (3-adic) and `D_j` (2-adic) are *simultaneously determined within
  one term*, unlike the cross-term `corr 0`. They ARE linked by the exact channel `D_j=v2(3^{e_j+1}u_j−1)`
  (§1,§3) — but the link is **measure-preserving**, hence informationless, exactly when `u_j ⊥ e_j`.
- So the residual content is **not** "does the orbit equidistribute" (the usual phrasing) but the
  equivalent **independence statement**: *along the explicit orbit, the 3-free cofactor `u_j ∈ Z_2^*` is
  independent of its own 3-adic exponent `e_j = D_{j−1}−1`.* Independence of `u_j` from `e_j` ⟹ `D_j`
  geometric ⟹ mean `D = 2 > 3/2` ⟹ non-halting (with margin). This is a re-encoding of the same
  single-orbit genericity / AEV(2510.11723, p/q=3/2) wall — an **isomorphism of the obstruction, not a
  reduction** — now in the crisp form "cofactor ⊥ exponent."
- Consistent with `ADELIC_COUPLING.md` (cross-prime corr 0, coupling is isomorphism of difficulty),
  `REPELLER_ESCAPE.md` (Mahler core concentrated in the 2-adic refill digit law), and the meta-theorem
  (the open core is irreducibly orbit-specific). The honest gain: the two-valuation entanglement at a
  single term is now **fully characterised** — real channel, Haar-null, blocked only by an independence
  that is itself the open core.

---

## 6. Banked

- **`[PROVEN]` Intra-term identity.** `D_j = v2(3^{e_j+1} u_j − 1)` with `o_j = 3^{e_j}u_j`,
  `gcd(u_j,6)=1`, `e_j = D_{j−1}−1`. The 3-adic exponent enters the 2-adic depth via the unit rotation
  `3^{e_j+1} mod 2^k`.
- **`[PROVEN]` Channel-exists (fixed cofactor).** For fixed `u`, `e ↦ v2(3^{e+1}u−1)` is non-constant
  (e.g. `u=1`: `1,2+v2(e+1),…`). A real 3-adic→2-adic deterministic channel.
- **`[PROVEN structural] + [OBSERVED] ` Channel-null (on orbit).** The rotation is a Haar-preserving
  bijection of `Z_2^*`; it can only transmit `e`→`D` via dependence of `u_j` on `e_j`; measurement shows
  `u_j ⊥ e_j` (joint `(D_{j−1},D_j)` factorises `χ²=30/25 dof`, all conditional `E[D]≈2`, `P(D=1)≈0.5`,
  stripped marginal matches). No forbidden pair, no parity link, no one-sided constraint.
- **`[PROVEN-honest]` Re-encoding of the wall.** Residual core = "cofactor `u_j ⊥ exponent `e_j` along the
  explicit orbit" ⟺ same single-orbit genericity (AEV p/q=3/2). Isomorphism, not reduction.

Scripts: `scratchpad/intraterm.py`, `scratchpad/intraterm2.py`. Not committed.
