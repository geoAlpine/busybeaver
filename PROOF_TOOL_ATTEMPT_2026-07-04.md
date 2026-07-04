# Aiming for a proof — a genuine attempt to build the tool, and the sharpest minimal target (2026-07-04)

*Not another audit: an actual attempt to **construct the missing a-priori estimate** that would prove Antihydra
non-halting. Two objects were pushed hard — the **max-depth ceiling** (which the balance walk needs) and the
**second-moment `E[K²]`** (which the atom needs). Both reduce to a single-orbit arithmetic statement with **no
a-priori source**. The genuine gain is a **sharpening**: the minimal needed statement is a `1.17×` improvement on a
*proven* ceiling — astronomically weaker than the truth — yet even that is `(K)`. SOUNDNESS: `[PROVEN]`/`[OBSERVED]`;
no proof obtained; `(K)` `[OPEN]`.*

## 1. The minimal needed statement — a `1.17×` ceiling improvement `[OBSERVED + PROVEN]`
Antihydra non-halt `⟺ B_n = 3E_n − n ≥ 0 ∀n`. A downward excursion of size `s` needs an odd-run (deep 2-adic visit)
of length `s = v₂(c_n−1)`. So non-halt `⟺` **`max_{n} v₂(c_n−1) < ½·(accumulated balance) ≈ 0.5 n`**. The three
numbers, at `N=2·10⁵`:

| quantity | value | note |
|---|---|---|
| **true** `max_n v₂(c_n−1)` | **`20`** `[OBSERVED]` | grows `~ log₂ N` — the deepest run is tiny |
| **needed** for non-halt | `< 0.5 N = 100000` | a **massive** relaxation of the truth |
| **proven a-priori ceiling** | `≤ 0.585 N = 117000` `[PROVEN]` | magnitude: depth `k ⟹ c ≥ 2^k`, `c~(3/2)^n` |

**The whole problem is the `0.585 → 0.5` step (factor `1.17×`).** The proven ceiling is `1.17×` too weak; closing it
= proving `c_n ≢ 1 (mod 2^{0.5n})` for all large `n` = a **single-orbit residue-avoidance** = `(K)`. There is **no
a-priori source** for it (the magnitude ceiling is tight for a single potential deep visit — `c_n` *could* be
`2^k+1`; ruling it out is arithmetic on the specific orbit).

## 2. The attempt on `E[K²]` (the atom sub-question) `[OBSERVED]`
The occupancy `N_k = freq(c ≡ 1 mod 2^k) ≈ 2^{-k}` empirically. The **valuation budget** `[PROVEN]` controls the
**first moment** `Σ_k N_k ≈ 1` (bounded). But `E[K²]` needs the **weighted** sum `Σ_k k·N_k` (`≈ 1.99` empirically),
which the budget does **not** bound: `Σ N_k < ∞` allows `N_k ~ k^{-1-ε} ⟹ Σ k N_k = ∞`. **Weak-tail sufficiency:**
`E[K²]<∞` needs only `N_k = O(k^{-2-ε})` — *polynomially* weak, exponentially weaker than the true geometric `2^{-k}`
— **yet even that is single-orbit cylinder occupancy `= (K)`.** No a-priori mechanism gives *any* `k`-decay of `N_k`.

## 3. Why every fresh construction closes `[PROVEN, the precise reasons]`
- **Two-place / adelic energy.** The product formula `Σ_p v_p(m)\log p = \log m` gives, for `m=c−1`, exactly
  `v₂(c−1)\log2 ≤ \log(c−1)` — the **first-moment magnitude ceiling** (`0.585n`). It is a **per-term inequality**;
  it carries **no distributional / second-moment / max-below-ceiling content**. So the adelic route gives the `0.585n`
  ceiling and nothing sharper — the same closure as the program's adelic sub-action.
- **Budget / telescope.** Degree-1 potentials → a count `≤ N` (free, first moment); degree-≥2 → the tautology `0=0`
  (`EK2` self-closure). No second moment.
- **Excursion supermartingale.** Any compensator equals `E[K²]` (circular); a heavy-tailed white adversary is
  drift-indistinguishable (`EXCURSION_SYNTHESIS`).
Each closes at the identical seam: **a-priori facts are first-moment / per-term / magnitude; the needed statement is
distributional / max-below-ceiling / single-orbit residue = `(K)`.**

## 4. Honest verdict
**(c) — no proof; a genuine attempt, sharpened to the minimal target.** Aiming for a proof, I tried to *build* the
a-priori estimate (max-depth ceiling and `E[K²]`), via the freshest constructions (two-place adelic energy,
weak-tail sufficiency, occupancy budget). **All close** at the first-moment/per-term/magnitude vs.
distributional/single-orbit seam — the proven `(K)` wall. The genuine gain is the **sharpest minimal target**: the
proof needs only `max_n v₂(c_n−1) < 0.5n` — a `1.17×` improvement on the *proven* `0.585n` ceiling, itself an
astronomical relaxation of the `~log n` truth — and that `1.17×` **is** `(K)`. The gap is *simultaneously tiny and
generational*: there is no "almost there"; the missing `1.17×` is exactly the single-orbit arithmetic no a-priori
mechanism supplies. **A proof genuinely requires the `P1′` tool (external/generational), confirmed by construction,
not just by the No-Structure meta-theorem.** **Halting `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `scratchpad` (`/opt/homebrew/bin/python3.13`): `max v₂(c_n−1)=20` at `N=2·10⁵` (`~log₂N`), ceiling `0.585N`, needed
  `<0.5N`; occupancy `N_k≈2^{-k}`, budget `ΣN_k≈1`, `Σk·N_k≈1.99`; product-formula per-term ceiling. Basis:
  `OCCUPANCY_PROFILE_THEORY.md §7` (balance/run-ceiling), `EK2_*`/`EXCURSION_SYNTHESIS.md` (second-moment no-go),
  `MAGNITUDE_LYAPUNOV.md`/`ADELIC_SUBACTION.md` (adelic closure), `NEW_MATH_PROGRAM.md` (P1′), `PROOF_ATTEMPT_AUDIT_2026-07-04.md`.
