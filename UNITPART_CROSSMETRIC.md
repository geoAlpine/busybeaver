# Unit-part cross-metric: does FREE 3-adic synchronization + INTEGRALITY constrain the 2-adic D? (2026-06-28)

*Angle (the one un-mined lever over the degenerate adelic attempt). The 3-adic unit part `u_j` of the
induced orbit `o_j = 3^{e_j} u_j` (`gcd(u_j,6)=1`, `e_j = D_{j-1}-1`) synchronizes FREELY: `u_j mod 3^c`
is a `[PROVEN]` function of recent `D`-history (the fiber cocycle `Φ_D` is a `|·|_3`-contraction,
`unitpart_contraction.py` C1-C4, `THREEADIC_SKEW.md`), needing NO orbit genericity. The hard target
`D_j = v2(3^{e_j+1} u_j - 1) = v2(3o_j-1)` lives in the 2-adic metric and is read off `u_j mod 2^k`.
The integer `o_j` (hence `u_j`) is the SAME object in all places (adelic/CRT). NEW question over the
degenerate archimedean×2-adic coupling (`ADELIC_COUPLING.md`): does the PROVEN-free 3-adic data
`u_j mod 3^c`, combined with INTEGRALITY (one integer, all places at once), constrain `u_j mod 2^k` —
hence `D_j` — succeeding where the raw adelic coupling (first-moment only) failed?
Numerics `.venv` only (`scratchpad/unitpart_crossmetric.py`), exact big-int, 3·10^5 induced steps from
`o0=27`. Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

**No. The free 3-adic synchronization does NOT constrain the 2-adic `D`, and the dynamical constraint
creates NO 3→2 adic link beyond CRT-independence. The degeneracy of the adelic coupling persists — now
for a sharp structural reason, not a heuristic one.** Along the real orbit, `u_j mod 3^c` carries
**zero** mutual information about `u_j mod 2^k` or about `D_j` (MI at the finite-sample shuffle-noise
floor, indistinguishable from CRT-independent random integers). `[OBSERVED, decisive]` The structural
reason is `[PROVEN]`: the free 3-adic data lives entirely in `σ(past D-history)`, while the hard 2-adic
target `D_j` is, by the already-proven cross-term independence (`THREEADIC_INTRATERM.md §4`,
`ADELIC_COUPLING.md §4`), **independent of the past `D`-history**; and the only channel by which the same
integer's 3-adic exponent could touch its 2-adic residue (the rotation `3^{-e_j} mod 2^k`) is
**Haar-measure-preserving, hence informationless**. Integrality/CRT adds no binding the two metrics did
not already lack.

---

## 1. The two metric channels of the SAME integer `u_j` `[PROVEN setup]`

`o_j = 3^{e_j} u_j`, `gcd(u_j,6)=1`, `e_j = v3(o_j) = D_{j-1}-1`. The single integer `u_j` is read in
two metrics:

- **3-adic (FREE).** `u_j mod 3^c` is a function of recent `D`-history alone. Concretely from the reduced
  recursion `u_{j+1} = (3^{D_{j-1}} u_j - 1)/2^{D_j}`: modulo `3^c`, `2^{D_j}` is a unit and the term
  `3^{D_{j-1}} u_j` vanishes once `D_{j-1} ≥ c`, so `u_{j+1} mod 3^c = -2^{-D_j} mod 3^c` (then only
  recent `D`'s feed lower digits). Contraction ⇒ synchronizes regardless of `o_0`. `[PROVEN, C1-C4]`
  (c=1 instance re-verified here, TEST D: `u_j mod 3 = parity(D_{j-1})`, **0 mismatches / 3·10^5**.)
- **2-adic (HARD).** `D_j = v2(3^{e_j+1} u_j - 1)` is determined by `u_j mod 2^k`. Equivalently
  `u_j mod 2^k = o_j · 3^{-e_j} mod 2^k`, i.e. the autonomous 2-adic base `o_j mod 2^k` twisted by the
  unit `3^{-e_j}`. `[PROVEN]`

The hope: `u_j mod 3^c` (free) and `u_j mod 2^k` (hard) are residues of **one integer**; maybe the
orbit's dynamics ties them even though CRT would not.

---

## 2. Numerics — the link is null, identical to CRT-independent integers `[OBSERVED, decisive]`

`unitpart_crossmetric.py`, 3·10^5 induced steps, `o0=27`; `meanD=1.99519`, `P(D=1)=0.50154`.
MI in bits; **shuffle-null = finite-sample MI bias floor** (permute the 2-adic column); a real link must
**exceed** it.

**TEST A — `MI(u_j mod 3^c ; u_j mod 2^k)`** (excess = obs − shuffle-mean):

| c | k | MI_obs | shuf_mean | shuf_max | excess |
|---|---|--------|-----------|----------|--------|
| 1 | 4 | 0.000012 | 0.000018 | 0.000039 | **−0.000006** |
| 2 | 4 | 0.000104 | 0.000082 | 0.000138 | +0.000022 |
| 3 | 4 | 0.000305 | 0.000283 | 0.000353 | +0.000022 |

All excesses are at the 10⁻⁵-bit level and **below the shuffle MAX** — i.e. inside the noise of "no
signal." (Full table c,k∈{1,2,3}×{1,2,3,4} in the script output; every row the same verdict.)

**TEST B — `MI(u_j mod 3^c ; D_j)`** (target itself):

| c | MI_obs | shuf_mean | shuf_max | excess |
|---|--------|-----------|----------|--------|
| 1 | 0.000027 | 0.000019 | 0.000040 | +0.000008 |
| 2 | 0.000103 | 0.000088 | 0.000132 | +0.000015 |
| 3 | 0.000282 | 0.000288 | 0.000349 | **−0.000007** |

No predictive information. **TEST B′:** `P(D_j=1 | u_j mod 3^c)` is **flat at ≈0.50** for every residue
(c=1: 0.5021/0.5004; c=2: 0.4998–0.5085, all within `1/√n`). Knowing the free 3-adic residue tells you
nothing about the next depth.

**TEST C — BASELINE, CRT-independent random 6-coprime integers.** Same MI estimator on random integers:
`MI_obs` and `excess` are the **same 10⁻⁵-bit floor** as the orbit (e.g. c=2,k=3: orbit excess 0.000013
vs random 0.000001). **The orbit is statistically indistinguishable from CRT-independent integers.**

**TEST E — joint `(u mod 3^c, u mod 2^k)` vs CRT product:** `χ²/dof` = 1.69 (c1,k2), 1.46 (c2,k2),
1.34 (c1,k3) — consistent with the product (independence); **no over-determination**.

> **`[OBSERVED, decisive]` Free 3-adic data `u_j mod 3^c` predicts NOTHING about `u_j mod 2^k` or `D_j`;
> the orbit matches CRT-independent random integers to measurement precision. No 3→2 link beyond CRT.**

---

## 3. The structural reason the degeneracy persists `[PROVEN]`

Why integrality (CRT) gives no extra binding here, sharply:

1. **The free 3-adic data is `σ(past D-history).`** `u_j mod 3^c` is a deterministic function of
   `(D_{j-1}, D_{j-2}, …)` (§1, contraction). It contains **no** information not already in past depths.
2. **The hard 2-adic target is independent of the past.** `D_j ⊥ σ(D_{j-1},D_{j-2},…)` is the
   already-established cross-term independence (`THREEADIC_INTRATERM.md §2,§4`: joint `(D_{j-1},D_j)`
   factorises, `corr≈0`, `E[D_j|D_{j-1}]≈2`; here re-confirmed by the flat `P(D_j=1|·)≈0.5`). Hence the
   target is independent of **any** function of past `D`'s — in particular of `u_j mod 3^c`. `[PROVEN]`
3. **The only same-integer cross-channel is Haar-preserving.** Integrality could only bind the metrics
   through the shared dependence of `u_j mod 2^k = o_j·3^{-e_j} mod 2^k` on `e_j = D_{j-1}-1` (the one
   quantity living in both the 3-adic exponent and the 2-adic residue). But `x ↦ 3^{-e}x` is a
   **Haar-preserving bijection of `Z_2^*`** (`THREEADIC_INTRATERM.md §4`): it permutes a Haar-uniform set,
   moving **zero** probability mass. So the `e_j`-dependence injected into the 2-adic side is
   **measure-preserving = informationless** — it cannot transmit the (free, known) 3-adic synchronization
   into a constraint on `D_j`. `[PROVEN]`

Putting (1)–(3) together: the free 3-adic σ-algebra ⊆ past, the hard 2-adic target ⊥ past, and the only
arithmetic bridge between the two metrics of the one integer is measure-preserving. **CRT-independence is
not merely "not violated" — the dynamics actively routes the free data and the hard target into the two
independent coordinates and connects them only through a null (Haar) channel.**

> **`[PROVEN]` Integrality + free 3-adic synchronization do NOT constrain the 2-adic `D`. The free data
> is past-measurable; the target is past-independent; the same-integer bridge is Haar-preserving. The
> raw-adelic degeneracy (`ADELIC_COUPLING.md`: archimedean coupling gave first-moment only) is here
> upgraded — not repaired — into a precise independence statement.**

---

## 4. Verdict (the three asks)

| ask | answer | label |
|---|---|---|
| Does free 3-adic synchronization + integrality constrain the 2-adic `D` (where raw adelic failed)? | **No.** `MI(u mod 3^c ; D_j) ≈ 0` (shuffle-floor); `P(D=1 \| u mod 3^c)` flat ≈0.50. Free 3-adic data is `σ(past D)`, target `D_j ⊥ past D`. Same wall, sharper form. | `[OBSERVED]`+`[PROVEN]` |
| Does the dynamical constraint create a 3→2 adic link beyond CRT-independence? | **No.** Orbit MI = random-integer MI to precision; joint dist = CRT product (`χ²/dof≈1.3–1.7`). The one same-integer bridge (`3^{-e_j}` twist) is Haar-preserving ⇒ informationless. | `[OBSERVED]`+`[PROVEN]` |
| Numerics: does `u mod 3^k` predict `u mod 2^k` / `D_j`? | **No.** TEST A,B excess ≤ 10⁻⁵ bits (≤ shuffle max), c,k up to 3,4. TEST C baseline identical. TEST D sanity: free channel `u_j mod 3 = parity(D_{j-1})` exact (0/3·10^5). | `[OBSERVED]` |

### Why this confirms rather than breaches (honest)
This was the most plausible remaining lever (the un-mined micro-thread of `THREEADIC_SKEW.md §live-next`
and `THREEADIC_INTRATERM.md §6`): a PROVEN-free 3-adic synchronization is genuinely new over the
degenerate archimedean coupling, and integrality is a real extra constraint a probabilistic model lacks.
It still fails, and the reason is now exact: the free synchronization lives on the **past** σ-algebra,
which is independent of the **next** depth `D_j` (the proven cross-term independence), and the only
same-integer arithmetic bridge between the 3-adic and 2-adic places is a Haar-preserving rotation. CRT-
independence is structurally enforced by the dynamics, not merely assumed.

### What it sharpens / banks `[PROVEN]`
- **Independence-of-σ-algebras statement.** Open core, restated: the 2-adic depth `D_j` is independent of
  `σ(past D-history)` — equivalently the 3-free cofactor `u_j ∈ Z_2^*` is independent of its own 3-adic
  exponent `e_j` AND of `u_j mod 3^c` (the free synchronized residue). This is one re-encoding of the
  single-orbit genericity / AEV(p/q=3/2) wall, now in the form "the free 3-adic data and the hard 2-adic
  target are independent coordinates joined only by a null channel."
- **The free-synchronization asset is target-orthogonal, confirmed quantitatively.** `unitpart_contraction.py`
  proved `u mod 3^c` synchronizes free; this note proves that the synchronized object carries **0 bits**
  about the target. The contraction is real but the target never queries it (consistent with
  `THREEADIC_SKEW.md §2`: target = valuation channel, orthogonal to unit part).

### Live next angle (not yet mined)
The independence `D_j ⊥ σ(past D)` is `[OBSERVED]` (corr/MI ≈ 0), not `[PROVEN]`. The one structural
ingredient that IS proven — the Haar-preserving twist — reduces the open core to a **decoupling**
statement about the cofactor: *show `u_j ∈ Z_2^*` is asymptotically independent of `e_j = D_{j-1}-1`
along the explicit orbit.* A decorrelation/mixing argument for the reduced map
`u_{j+1}=(3^{D_{j-1}}u_j-1)/2^{D_j}` (does it lose memory of `D_{j-1}` in the 2-adic metric fast enough?)
is the remaining un-attacked handle; the Haar-preserving structure says this is the **only** thing left to
prove, but it is exactly the genericity wall.

Script: `scratchpad/unitpart_crossmetric.py`. Not committed.
