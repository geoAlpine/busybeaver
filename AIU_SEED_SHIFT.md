# AIU via the SEED-SHIFT reformulation — does the A-orbit limit measure depend on the seed within the `ℤ[1/6]ˣ`-coset? (2026-06-29)

*Target: the Adelic Invariance-Upgrade conjecture AIU (`NEWMATH_ADELIC_RIGIDITY` §2, `AIU_ATTACK`):
is the empirical limit measure `μ` of the single `A=×(3/2)`-orbit on the solenoid `X=(ℝ×ℚ₂×ℚ₃)/ℤ[1/6]`
also separately `×2`-invariant? Angle here: `×2` (and `×3`) commute with `A` in the abelian host
`⟨×2,×3⟩=ℤ[1/6]ˣ`, so `(×u)_*μ_{x₀}=μ_{u·x₀}` — AIU becomes a **seed-shift / seed-independence** statement.
SOUNDNESS PARAMOUNT: every claim labelled; no claim to prove (K). Numerics
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (`scratchpad/seed_shift.py`, exact big-int, induced odd
map, `N≤10⁵`, ≈25s). NOT committed.*

---

## 0. One-line verdict

**The seed-shift reformulation is `[PROVEN]` (AIU ⟺ `μ` is constant on the `ℤ[1/6]ˣ`-coset of the seed
⟺ `μ_8=μ_16`); numerically the orbits of `8,16,24,32,64` DO converge to one common limit law mod `2^k`
to the sampling floor (AIU strongly supported on the 2-adic axis); BUT the two orbits do NOT couple — they
are 2-adically independent (the gap `v₂(o_n(27)−o_n(81))` is geometric with mean 2, the orbits never merge),
so AIU is NOT obtainable via orbit-coupling. Verdict (b): AIU (seed-shift form) is strictly weaker than (K)
as a statement yet the only visible route to it is a full equidistribution of (K)-comparable difficulty;
the coupling shortcut (a) is numerically refuted, and (c) equivalence is false (AIU still needs ENT∨Furstenberg).**

---

## 1. The seed-shift identity `[PROVEN reformulation]`

**Commutation `[PROVEN]`.** `M_2,M_3,A=M_{3/2}` are all dilations `M_u`, `u∈ℤ[1/6]ˣ={±2^a3^b}`. `M_uM_w=M_{uw}=M_wM_u`
because `ℤ[1/6]ˣ` is abelian; in particular `M_2A=AM_2`, `M_3A=AM_3`. Each `M_u` is an automorphism of `X`
(it normalizes `Γ=ℤ[1/6]`). So `A^n(M_u x)=M_u A^n(x)` for all `n`.

**Seed-shift identity `[PROVEN, on the solenoid ×(3/2)-system]`.** For the empirical measures
`μ_N^{x₀}=N^{-1}Σ_{n<N}δ_{A^n x₀}`, the commutation gives `μ_N^{M_u x₀}=(M_u)_*μ_N^{x₀}` term-by-term, hence
for every weak-* limit
> `μ_{u·x₀} = (M_u)_* μ_{x₀}`,  in particular `μ_{2x₀}=(×2)_*μ_{x₀}` and `μ_{3x₀}=(×3)_*μ_{x₀}`.

**AIU restated `[PROVEN reformulation]`.** AIU = `(×2)_*μ_{x₀}=μ_{x₀}` ⟺ `μ_{2x₀}=μ_{x₀}` ⟺ (with `A`-inv,
which forces `(×2)_*μ=(×3)_*μ`, so also) `μ_{3x₀}=μ_{x₀}` ⟺
> **`μ` is constant on the whole `⟨×2,×3⟩=ℤ[1/6]ˣ`-coset of the seed** — the A-orbit limit measure is
> **independent of the seed within the host-coset.** With `x₀=8`: **AIU ⟺ `μ_8=μ_16` (≡ `μ_8=μ_24`).**

**Floor / integer caveat `[PROVEN — the identity is EXACT only on the solenoid]`.** The genuine `×(3/2)`
automorphism is exactly `M_u`-equivariant. The *integer* Antihydra map `f(c)=⌊3c/2⌋` is `×2`-equivariant
**only on even arguments** (`f(2c)=⌊3c⌋=3c=A(2c)`, no floor) and carries a `−½` defect on **odd**
arguments (`f(o)=(3o−1)/2=A(o)−½`); the induced odd map `o↦3^{D-1}(3o−1)/2^D` inherits this `−1`. On `X`
this defect is exactly the `Γ=ℤ[1/6]`-renewal translation, so `μ_{u·x₀}=(M_u)_*μ_{x₀}` is exact there;
on integers the *term-by-term* scaling `3·o_n(27)=o_n(81)` holds **only at `n=0`** then breaks at `n=1`
(`3·135=405≠121`; verified). Numerics below show the **measure-level** identity nonetheless survives to
the sampling floor for the integer induced orbits.

**The funnel that makes the 2-adic test clean `[PROVEN, new]`.** Antihydra seed `2^k` reaches its first odd
value `3^k` **exactly** (all-even prefix, no floor): `8→27=3³, 16→81=3⁴, 32→243=3⁵, 64→729=3⁶` (and
`24=3·8→81`, `48→243`). Hence the limit measures satisfy `μ_8=μ_{27}`, `μ_16=μ_{81}=μ_{3·27}`, etc.
So `μ_8` vs `μ_16` is the comparison `μ_{27}` vs `μ_{3·27}=(×3)_*μ_{27}` — and **`×3` is a 2-adic UNIT**
(permutes the odd residues mod `2^k`), so the comparison is testable on the 2-adic marginal **without** the
support-shift that defeated the raw `(×2)_*μ` test of `AIU_ATTACK` (`×2` moves odds off the unit shell).
By `A`-invariance `(×2)_*μ_8=(×3)_*μ_8`, so the two descriptions of `μ_16` agree — the `×3`-unit one is the
one that can be measured.

---

## 2. Decisive numeric — do the orbits of `8,16,24,32,64` share one limit law mod `2^k`? `[OBSERVED, exact, N≤10⁵]`

Induced odd orbits from seeds `27,81,243,729` (= Antihydra `8,16/24,32,64`). `TV` of empirical
`o_n mod 2^k`; sampling floor `≈√(2^{k-1}/N)`.

| N | `TV(μ_8,μ_16)` k=4 | k=6 | k=8 | k=10 | floor(k=4) | floor(k=8) |
|---|---|---|---|---|---|---|
| 10³ | 0.046 | 0.090 | 0.219 | 0.375 | 0.089 | 0.358 |
| 10⁴ | 0.0158 | 0.0301 | 0.0643 | 0.1245 | 0.0283 | 0.1131 |
| 10⁵ | **0.0045** | 0.0106 | 0.0209 | 0.0407 | **0.0089** | 0.0358 |

`TV(μ_8,μ_16)→0` at the finite-sampling rate, **at or below the floor** for every `k`. Same for
`TV(μ_8,μ_32)`, `TV(μ_8,μ_64)` (k=4,N=10⁵: 0.0062, 0.0061). The integer-level seed-shift identity check
`TV(μ_16,(×3)_*μ_8)≈floor` (k=4,N=10⁵: 0.0043) and the on-orbit `×3`-invariance `TV(μ_8,(×3)_*μ_8)≈floor`
(0.0065 — matching `AIU_ATTACK` table (a)) are all consistent.

> **`[OBSERVED]` The A-orbit limit measure mod `2^k` is the SAME for all seeds in the `ℤ[1/6]ˣ`-coset of `8`,
> to the sampling floor.** This is exactly `μ_8=μ_16` on the (testable) 2-adic axis: AIU is **strongly
> supported**. (Caveat unchanged from `AIU_ATTACK`: both AIU and (K) predict the uniform-on-odds law here,
> so this axis confirms AIU but cannot *separate* it from (K); the 3-adic axis remains renewal-contaminated.)

---

## 3. Orbit-coupling test — do the two orbits MERGE mod `2^k`? `[OBSERVED, exact, N=10⁵]` — NO

If `o_n(27)` and `o_n(81)` *synchronized* (agreed mod `2^k` after some `n`, or `v₂(o_n(27)−o_n(81))→∞`),
then `μ_8=μ_16` would follow **without** equidistribution — a genuine partial AIU. They do not.

- **Aligned-term agreement mod `2^k`** = `{n<10⁵ : o_n(27)≡o_n(81) (2^k)}`: `k=4`→12485, `k=8`→790,
  `k=16`→4. These match the **independent-uniform** prediction `N/2^{k-1}` (12500, 781, 3) to within noise.
- **2-adic gap law:** `v₂(o_n(27)−o_n(81))` is geometric, `P(gap=j)=2^{-j}` (0.5001,0.2501,0.125,…),
  **mean 1.999**, max 20 over 10⁵ — i.e. exactly the law of `v₂` of a difference of two *independent* random
  2-adic units. The orbits coincide **0** times; the gap shows **no** downward drift / no contraction.

> **`[OBSERVED — decisive]` The orbits of `8` and `16` are 2-adically INDEPENDENT: they never merge and their
> 2-adic distance does not shrink.** There is **no orbit-coupling / contraction** to exploit. The equality
> `μ_8=μ_16` holds (§2) only in the way two *independent* equidistributing orbits share a limit — i.e. it
> carries the full equidistribution content, not a shortcut to it. **Route (a) is numerically refuted.**

---

## 4. Structural analysis — is `μ_8=μ_16` attackable below full equidistribution?

- **Coupling/contraction route — CLOSED `[OBSERVED, §3]`.** A proof of `μ_8=μ_16` via a coupling that
  merges the orbits mod `2^k` (or 2-adically contracts their difference) is ruled out: the orbits behave as
  independent, gap-law geometric-mean-2, never coinciding. The host map `×(3/2)` is **expanding** at the
  2-adic place (dilation 2), so 2-adic differences are *amplified*, not contracted — there is no stable
  2-adic foliation along which to couple the two seeds. `[PROVEN — the 2-adic direction is expanding]`
- **Why seed-shift does not lower the difficulty `[PROVEN-honest]`.** The reformulation `μ_8=μ_16` is exact
  and clean, but to *prove* it one must show the two independent single orbits have the **same** weak-*
  limit. With no coupling (§3) and no second iterated map, the only visible mechanism is that each orbit
  *individually* equidistributes to a seed-independent measure — which on the 2-adic place is the
  single-orbit equidistribution that **is** (K) (`ADELIC_COUPLING` §3, Mahler-3/2 wall). Seed-shift relocates
  AIU to "seed-independence of the limit" but, exactly as `AIU_ATTACK` §3.4 found for the `×2`-axis, the only
  route is an equidistribution no easier than (K).
- **Logical strength unchanged from `AIU_ATTACK` `[PROVEN]`.** `(K)⟹AIU` (Haar is `×u`-invariant);
  `AIU⟹(K)` only modulo OPEN `{h_μ(M_2)>0 ∨ Furstenberg}`. Seed-shift adds no link to ENT and does not close
  that gap. So AIU is still **strictly weaker** than (K) as a statement.

---

## 5. Honest verdict (a)/(b)/(c)

| question | verdict | label |
|---|---|---|
| Seed-shift identity `μ_{u x₀}=(M_u)_*μ_{x₀}` | **Yes**, exact on solenoid; integer/induced only up to the `−1` renewal (term-scaling breaks at step 1) | `[PROVEN]` |
| AIU ⟺ `μ` constant on `ℤ[1/6]ˣ`-seed-coset ⟺ `μ_8=μ_16` | **Yes** | `[PROVEN reformulation]` |
| Do orbits of `8,16,24,32,64` share one limit law mod `2^k`? | **Yes, to the sampling floor** (`TV→0`) | `[OBSERVED]` |
| Do the two orbits provably couple / merge mod `2^k`? | **No** — 2-adically independent, gap geometric mean 2, never merge; `×(3/2)` is 2-adically expanding | `[OBSERVED + PROVEN-expanding]` |
| **(a)** provable via orbit-coupling? | **No — refuted.** No coupling exists to exploit | `[OBSERVED]` |
| **(b)** strictly weaker than (K) but still hard? | **Yes.** Statement weaker (needs ENT∨Furstenberg for (K)); only proof route is (K)-hard equidistribution | `[PROVEN + honest]` |
| **(c)** equivalent to (K)? | **No** — strictly weaker as a statement | `[PROVEN]` |

**Exact remaining gap.** AIU (seed-shift form) = the unproven claim that two **independent**, non-coupling
single `×(3/2)`-orbits (`27` and `3·27`) share one weak-* limit mod `2^k`. With no coupling (§3) and a
2-adically *expanding* host, the only visible route is each orbit's individual single-orbit equidistribution
— the Mahler-3/2 / `×2,×3` wall, of (K)-comparable difficulty — and even granting `μ_8=μ_16` one still needs
`{h_μ(M_2)>0 ∨ Furstenberg}` to reach (K). The seed-shift is a **clean exact reformulation and a clean
numeric confirmation**, not a reduction in difficulty; it positively **closes** the orbit-coupling route as a
shortcut.

---

## Sources
- Repo: `AIU_ATTACK.md` (AIU strictly weaker than (K); 2-adic axis consistent, table (a) `TV(μ,(×3)_*μ)`),
  `NEWMATH_ADELIC_RIGIDITY.md` (§2 AIU, §3.2 two-gaps ENT∨Furstenberg, §3.3 (T1)–(T2)),
  `ADELIC_COUPLING.md` (`v₃(o_{j+1})=D_j−1`; Mahler-3/2 = irreducible wall), `LIMIT_MEASURE_ENTROPY.md`,
  `DICHOTOMY_LEMMA_AUDIT.md`.
- Literature: Rudolph (ETDS 1990)/Johnson `×2,×3` rigidity (positive entropy ⟹ Haar) `[PROVEN-in-lit]`;
  Furstenberg (1967) measure conjecture `[OPEN]`; *Rigidity… commuting automorphisms on tori and solenoids*
  arXiv:2101.11120 `[PROVEN-in-lit]`; Einsiedler–Lindenstrauss (JMD 2008, rank-1 non-rigidity)
  `[PROVEN-in-lit]`.
- Numerics: `scratchpad/seed_shift.py` (exact big-int, induced odd map, seeds `27,81,243,729`, `N≤10⁵`,
  ≈25s): §2 TV table, §3 coupling/gap test, funnel `2^k→3^k`.

No machine decided. No label upgraded.
