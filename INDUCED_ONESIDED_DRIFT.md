# One-sided induced-drift attack on wall (B): liminf mean-D ≥ 3/2 (2026-06-28)

*Attack on the ONE-SIDED target (`WALLB_EFFECTIVE.md`): non-halt ⟸ even-density ≥ 1/3 for all n,
which is WEAKER than equidistribution to 1/2. Reframed on the induced odd map via the GAP LEMMA
(`WALLB_VALUATION_SHARP.md`). Numerics `.venv` only (`scratchpad/induced_onesided.py`). Every line
labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

The one-sided target **liminf (mean D) ≥ 3/2** is a genuine *weakening* of full equidistribution — it
needs only a **one-sided LOWER bound on the total deep-cylinder occupation**, and is *sufficed* by the
single statement **`liminf freq(o ≡ 3 mod 4) ≥ 1/2`** along the induced odd orbit. But it does **not**
escape the wall: (i) the induced residue map is **NOT a bijection** mod `2^k` — it is *expanding*
(the base map `T` is exactly 2-to-1 mod `2^k`; the induced map is not even a *function* mod `2^k`, it needs
≈`k+15`-bit lookahead), so **no permutation/counting argument forces Haar**; (ii) **no drift / budget
identity yields the one-sided floor** (the budget is the renewal tautology = an *equality* `meanD = n/K`,
not a bound on the ratio; the conditional means `E[D'|D≥k]` are flat-to-mildly-*decreasing*, i.e. give no
helpful floor). So liminf mean-D ≥ 3/2 reduces to a **strictly smaller, one-sided, low-level instance** of
single-orbit cylinder-frequency control — same KIND as wall (B)/(A), but the minimal sufficient statement
is now pinned as small as it gets. **The gain is localization, not a breach.**

---

## 1. The exact arithmetic of shallow steps + the mean-D formula `[PROVEN]`

Induced odd map (GAP LEMMA): `o_{j+1} = 3^{D-1}(3o_j − 1)/2^D`, `D = D_j = v₂(3o_j − 1) ≥ 1`.

- **Shallow ⟺ residue.** `D = 1 ⟺ v₂(3o−1)=1 ⟺ 3o−1 ≡ 2 mod 4 ⟺ o ≡ 1 mod 4`.
  `D ≥ 2 ⟺ o ≡ 3 mod 4`. Generally `D ≥ k ⟺ 3o ≡ 1 mod 2^k ⟺ o ≡ 3^{−1} mod 2^k`
  (3 is a 2-adic unit, so this fixes `o` mod `2^k`; a thin cylinder of relative measure `2^{1−k}` among odds).

- **Mean-D formula `[PROVEN]`.** Since `D = Σ_{k≥1} 1{D≥k}`, averaging along the induced orbit,
  > **`mean D = Σ_{k≥1} freq(o ≡ 3^{−1} mod 2^k)`.**

  The `k=1` term is `1` (always, since `o` odd ⇒ `D≥1`); the `k=2` term is `freq(o ≡ 3 mod 4) = freq(D≥2)`.
  **Verified exactly** (`induced_onesided.py`, c₀=8, K≈10⁵): `Σ_k freq = 2.000720 = mean D` to all printed
  digits. Per-`k` `freq` matches Haar `2^{1−k}` to 2–3 dp (k=1..16).

- **The threshold.** `mean D ≥ 3/2 ⟺ freq(o≡3 mod 4) + Σ_{k≥3} freq(o≡3^{−1} mod 2^k) ≥ 1/2`,
  equivalently `Σ_{k≥2} freq(o≡3^{−1} mod 2^k) ≥ 1/2`, equivalently `E[D−1] ≥ 1/2`. (Measured LHS `=1.0007`.)

## 2. The even-density ⟺ mean-D equivalence (renewal counting) `[PROVEN]`

In a return block of length `D` there is exactly **1 odd + (D−1) even** step (GAP LEMMA). Over `K` returns
covering `n = Σ_{j<K} D_j` original steps: `#odd = K`, `#even = n − K`, so
> **even-density `= 1 − K/n = 1 − 1/(mean D)`.**

Hence **even-density ≥ 1/3 ⟺ mean D ≥ 3/2 ⟺ liminf (1/K) Σ_{j<K} D_j ≥ 3/2** — and this is **ONE-SIDED**
(the danger is only `mean D ↓ 1`, i.e. too many `D=1` shallow steps `o≡1 mod 4`). Verified:
even-density `0.500185` vs `1 − 1/meanD = 0.500180`; worst dip over `n=2·10⁵` is `0.4565 ≫ 1/3`,
worst `balance_n = +2`. `[OBSERVED]` (finite N ⇒ nothing about the limit).

**Minimal sufficient statement.** Because every `k≥3` term is `≥0`, a SUFFICIENT condition for the whole
target is the *single mod-4 cylinder* floor
> **`liminf_K freq_K(o ≡ 3 mod 4) ≥ 1/2`**  (one cylinder, one direction).

This is the **weakest possible** reduction of wall (B): a one-sided lower bound on a *single* cylinder
frequency at level `mod 4`, vs full two-sided equidistribution of *all* cylinders mod `2^k`.

## 3. Is the induced residue map a BIJECTION (forcing Haar)? — **NO, it is EXPANDING** `[PROVEN/OBSERVED]`

The hoped-for shortcut: if `o' mod 2^k` depended *bijectively* on `o mod 2^{k+c}`, a single orbit would
cycle through a permutation and Haar would be the unique stationary law, possibly giving the bound by
counting. **This fails — the structure is expanding, not bijective:**

- **`[PROVEN]` Base map `T(c)=⌊3c/2⌋` is exactly 2-to-1 mod `2^k`.** Solving `T(c)=y`: `c=(2y+r)/3`, and
  *both* `r=0,1` give a valid 2-adic `c` with parity `=r` (since `3^{−1}≡1 mod 2`). So `T` has **2
  preimages**, not 1 — it is the 2-to-1 full-shift map (conjugate to the one-sided 2-shift), **not a
  bijection**. Numerics: `T` preimage-size distribution mod `2^k` `= {2: …}` uniformly, `k=2..7`.
- **`[OBSERVED]` The induced map is not even a function mod `2^k`.** Along the orbit, `o' mod 2^k` is
  **not** well-defined from `o mod 2^k` for any `k=2..12` (collisions with distinct images). Minimal
  empirical lookahead `L` for `o' mod 2^k` to become a function of `o mod 2^{k+L}` is `L ≈ 12–16` — `≈` the
  **max depth `D`** in the window (each step loses `D` low bits). As `K→∞` the max `D` grows like `log K`,
  so **no finite uniform lookahead exists**: the induced map is genuinely expanding/shift-conjugate.

**Consequence.** Haar is the invariant / maximal-entropy measure but is **NOT forced on a single orbit** by
any finite-level permutation. Full topological complexity + expanding/non-sofic structure means
full-dimension non-generic orbits exist (Barreira–Schmeling; cf. `WALLB_INVARIANT_MEASURES.md`).
**So the bijection→Haar→counting route does not exist; genericity is still required.**

## 4. Is a one-sided floor obtainable by drift/budget (weaker than equidistribution)? — **NO** `[REDUCES]`

- **Budget = renewal tautology (an equality, not a one-sided bound).** `Σ_{odd} v₂(3c−1) = n + v₂(c_n) −
  v₂(c₀)` pins `mean D = n/K` *exactly* but says nothing about the *ratio* `K/n` we need bounded; it is
  `(#renewals)·(mean gap) = total time`, first-moment only (`WALLB_VALUATION_SHARP.md`). No one-sided floor.
- **No helpful conditional drift.** `E[D_{j+1} | D_j ≥ k]` is **flat-to-mildly-decreasing**: `2.00, 1.99,
  1.99, 1.98, 1.95, 1.92, 1.91` for `k=1..7`. A *floor* on mean-D would need these bounded **below** by
  something `>` the shallow pull; instead deep steps are followed by *slightly shallower* ones (the
  extremal self-correction, mild) — this pulls mean-D **down**, not up. No supermartingale gives the floor.
- **Therefore the one-sided floor `Σ_{k≥2} freq(o≡3^{−1} mod 2^k) ≥ 1/2` is a single-orbit cylinder-
  frequency LOWER bound with no arithmetic source.** It is strictly *weaker* than full equidistribution
  (one direction, and sufficed by a single mod-4 cylinder), but it is the **same KIND** of object — orbit
  cylinder occupation — for which the only known tool is wall-(A)/Mahler equidistribution. **Reduces to a
  weaker, one-sided, low-level instance of (B); does not breach it.**

## 5. Numerics summary (`induced_onesided.py`, exact big-int) `[OBSERVED]`

| quantity | result | reading |
|---|---|---|
| `mean D` (c₀=8, K≈10⁵) | `2.0007` | Haar value 2; identity `Σ_k freq = mean D` exact |
| even-density vs `1−1/meanD` | `0.500185` vs `0.500180` | renewal identity confirmed |
| worst even-density dip / worst `balance_n` | `0.4565` / `+2` | both safely inside ≥1/3 (finite N only) |
| `freq(o≡3 mod 4)` | `0.5005` | Haar 0.5; the minimal sufficient cylinder |
| min partial mean-D (K≥50) / sliding-W=2000 | `1.889` / `1.893` | never near 1.5 (no proof of limit) |
| induced map function mod `2^k`? | **False** all `k` | expanding; lookahead `L≈12–16 ≈ max D` |
| `T` preimage sizes mod `2^k` | `{2:…}` | exactly 2-to-1 (full shift, not bijection) |
| `E[D'|D≥k]`, k=1..7 | `2.00→1.91` | flat-to-down; **no helpful floor** |
| 7 seeds (incl. `2^200+8`, `3^{−1} mod 2^60`) | meanD `1.997–2.002` | seed-independent; extremal seed relaxes to Haar |

## 6. Verdict (0 false proofs)

| question | answer | label |
|---|---|---|
| Exact `mean D` formula | `mean D = Σ_{k≥1} freq(o ≡ 3^{−1} mod 2^k)` (k=1 term ≡1, k=2 = freq(o≡3 mod 4)) | `[PROVEN]` |
| even-density ⟺ mean-D | even-density `= 1 − 1/meanD`; so even-density ≥ 1/3 ⟺ liminf mean-D ≥ 3/2 (ONE-SIDED) | `[PROVEN]` |
| minimal sufficient statement | `liminf freq(o ≡ 3 mod 4) ≥ 1/2` (single cylinder, one-sided) suffices | `[PROVEN]` |
| Is the residue map a bijection forcing Haar? | **NO** — base map exactly 2-to-1 mod `2^k`; induced map not a function mod `2^k` (lookahead `≈ max D`). Expanding/shift-conjugate ⇒ Haar **not** forced on a single orbit | `[PROVEN/OBSERVED]` |
| One-sided liminf mean-D ≥ 3/2 by counting/drift? | **No shortcut.** Budget = renewal *equality*; conditional means flat-to-down (no floor). Reduces to a *weaker, one-sided, mod-4-level* instance of single-orbit cylinder frequency = wall (B)/(A) | `[REDUCES TO (A)]` |

**Net.** The one-sided reframing is real and is the **maximal localization** of the wall achieved so far:
the entire complete-proof analytic gap is now the single one-sided statement *"the induced odd orbit's
`mod 4` cylinder `{o≡3 mod 4}` is occupied with frequency `≥ 1/2` in liminf."* It is strictly weaker than
equidistribution, but the two mechanisms that could have delivered it for free — a bijective residue map
(→Haar by counting) and an arithmetic drift/budget floor — are **both provably/empirically absent**
(map is expanding 2-to-1, budget is the renewal tautology). So it bottoms out at single-orbit cylinder
frequency, same kind as Mahler. **Productive closure: the sufficient statement is now as small as a single
one-sided mod-4 cylinder floor.**

### Live next angle
The minimal target `liminf freq(o≡3 mod 4) ≥ 1/2` is a *one-sided* level-2 cylinder bound. The only
un-mined direction: whether the mild `E[D'|D≥k] < 2` anti-correlation (extremal self-correction) can be
turned into a *variance/large-deviation* statement that keeps the **empirical** mod-4 frequency from
dropping below 1/2 in liminf without proving its convergence — a one-sided LDP-style floor rather than a
CLT. Current data: the anti-correlation pulls the mean *down* slightly, so this is a long shot, but it is
the one statement about the induced orbit not yet shown literally identical to two-sided equidistribution.
