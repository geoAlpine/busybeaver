# The joint (∞,2,3) constraint on the o4 orbit — the 2-adic place is a bounded spectator; it does NOT exclude the cap-legal fatal adversary (2026-07-10)

*A genuinely new BUILD going BEYOND `U0_EXCLUSION_BUILD` (archimedean run-cap ALONE) and `INTRATERM_ADELIC_MINING`
(per-term first-moment ALONE). The reframe: the o4 orbit integer `m_i = G_i − x_{ρ_i}` is SIMULTANEOUSLY constrained
at all three places of the (2,3)-solenoid `ℝ×ℚ₂×ℚ₃`. `4 = 2²`, so `×4/3` is a 3-adic unit multiplier but a 2-adic
`2²` — the SAME `m_i` has a 3-adic depth `d_i = v₃(m_i)` (the fatal atom), a 2-adic valuation `v₂(m_i)`, and a real
magnitude `≈57·(4/3)^{n_i}`, all coupled by the product formula `∏_v|m_i|_v = 1`. Yesterday used only `|m_i|_∞`
(run-cap). Does the 2-adic side, JOINTLY, over-determine the cap-legal fatal adversary that survived U0? STRICT
soundness `[PROVEN]`/`[CONSTRUCTED]`/`[OBSERVED]`/`[OPEN]`. Exact big-int,
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python scratchpad/joint_adelic_build.py`. NOT committed.*

---

## 0. One-paragraph verdict

The `×4/3` automorphism acts on the three places as **∞ = expanding** (magnitude grows `4/3`/step, accumulating the
drained depth as the run-cap budget), **3 = the drained-depth place** (`d_i = v₃(m_i)`, the atom of the fatal
statistic), and — decisively — **2 = a BOUNDED SPECTATOR.** Although `4=2²` makes the *intermediate* product
`4^{d_i}w_i` 2-adically deep (`v₂ = 2d_i`), the fixed-point offset `x_{ρ}` **RESETS** the 2-adic valuation at every
reload: `v₂(m_{i+1}) = v₂(Δ_i + 4^{d_i}w_i) = v₂(Δ_i)`, which is **bounded**. Measured on the seed-43 orbit:
`v₂(m_i) ∈ {0,2,3}`, max **3**, mean 0.89, over 133 374 reloads; and `v₂(G_n) ∈ {0,1}` **deterministically**
(`v₂(G_{n+1}) = 1 ⟺ ρ_n = 1`, `[PROVEN]` from the parity of `4G+e`). Consequences, all verified: (i) the joint
product-formula cap `|m|≥2^{v₂}3^{d}` sharpens the archimedean run-cap by `v₂·log₃2 ≤ 3·0.631 = **1.893 bits**` —
**O(1), never n-scaling**; (ii) the product formula summed is `log|m_i| = d_i log3 + v₂ log2 + log(rest)`, a
first-moment identity whose 2-adic term `Σv₂log2 = O(M)` does **not** reach the second moment `Σd_i²`; (iii) by CRT
(`v₂` and `v₃` at coprime moduli) the 2-adic condition is a **free bounded congruence** on the reload unit — I
construct an o4 cap-legal heavy-tail adversary (`Σd²` super-linear) that is jointly `(∞,2,3)`-legal at **0/4000**
reloads. **The 2-adic feasibility does NOT exclude the cap-legal fatal adversary.** The three places give
`{first moment} ⊕ {archimedean support} ⊕ {bounded 2-adic congruence}`; the third is a time-shifted copy of the
branch itinerary (the `INTRATERM` lesson, now at o4's 2-adic place), null in the tail. No machine decided. No label
upgraded.

---

## 1. The joint (∞,2,3) structure of the SAME reload integer `[PROVEN + OBSERVED]`

o4 odometer `G' = (4G+e(ρ))/3`, `ρ=G mod 3`, `e={0:9,1:14,2:1}`; branch fixed points `x={0:−9,1:−14,2:−1}`;
maximal constant-`ρ` run of length `L` from entry `G`, with `m := G − x_ρ`, `d = v₃(m) = L` (`[PROVEN]`, uniform
fixed-point theorem — **0 mismatch / 133 374 runs**). The reload unit is `w = m/3^{d}`, an **integer** coprime to 3.

The product formula for the integer `m` is the factorization `|m| = 2^{v₂(m)}·3^{v₃(m)}·rest`, `rest⊥6`
(**0 mismatch / 133 374**). So the SAME `m_i` carries three coupled coordinates:

| place | read-out on `m_i` | behaviour under the orbit | rôle |
|---|---|---|---|
| **∞** | `log|m_i| ≈ log57 + n_i·log(4/3)` | **expands**, `n_i=Σ_{j<i}d_j` accumulates | run-cap budget (first moment) |
| **3** | `d_i = v₃(m_i)` | the **drained depth** (fatal atom) | fatal statistic `Σd_i`, `Σd_i²` |
| **2** | `v₂(m_i) ∈ {0,2,3}`, max 3, mean 0.89 | **bounded, resets each reload** | spectator |

**Why the 2-adic place resets `[PROVEN mechanism].`** The exit identity is `m_{i+1} = Δ_i + 4^{d_i} w_i` with
`Δ_i = x_{ρ_i}−x_{ρ_{i+1}} ∈ {0,±5,±8,±13}`. The multiplicative part `4^{d_i}w_i` has `v₂ = 2d_i` (the “×4 growth”
the brief flagged is real here) — but it is **added to the small offset** `Δ_i`, and `v₂(m_{i+1}) = v₂(Δ_i)` whenever
`v₂(Δ_i) < 2d_i` (always, for `d_i≥2`). The deep 2-adic part is **absorbed into the tail** and the observable
valuation collapses to `v₂(Δ_i) ≤ v₂(8) = 3`. **The 2-adic place accumulates NO budget** — the exact opposite of the
archimedean place, which accumulates all the drainage as magnitude.

Even cleaner on the orbit values themselves: `v₂(G_{n+1}) = 1` if `ρ_n=1` (then `4G+14 = 2(2G+7)`, `v₂=1` exactly)
and `= 0` otherwise (`e∈{9,1}` odd, `4G+e` odd) — **verified exactly to n=120 000**. `[PROVEN]` The 2-adic place of
the orbit is a **deterministic function of the branch itinerary**: it carries **zero information beyond `ρ`**.

## 2. The joint run-cap sharpens the archimedean cap by a BOUNDED amount `[PROVEN]`

The full product-formula bound is `|m|≥2^{v₂(m)}·3^{v₃(m)}`, giving

> **joint cap** `d_i ≤ log₃|m_i| − v₂(m_i)·log₃2`   vs   **archimedean-only** `d_i ≤ log₃|m_i|`.

The extra tooth is `v₂(m_i)·log₃2`. Since `v₂(m_i) ≤ 3` on the entire orbit, the **maximum sharpening over all
133 374 reloads is `3·log₃2 = 1.893 bits`** — an **O(1) constant, never n-scaling**. Asymptotically the joint cap is
the *same line* as the archimedean run-cap (slope `log₃(4/3)=0.262`). This is the precise sense in which the 2-adic
place adds **nothing that grows**: the only place whose budget scales with `n` is `∞`, exactly as in U0.

## 3. The product formula, summed, is first-moment — the 2-adic term does NOT reach `Σd_i²` `[PROVEN]`

Per term, `log|m_i| = d_i log3 + v₂(m_i) log2 + log(rest_i)` — a single scalar identity (codim-1). Summed over the
real orbit (199 999 reloads):

`Σd_i·log3 = 219 721` , `Σv₂·log2 = 81 964` , `Σlog(rest) = 3.83·10⁹` , total `= Σlog|m_i| = 3.83·10⁹` (**exact
match**). The 2-adic term `Σv₂log2 = O(M)` (because `v₂` is bounded) is a **first-moment correction** — it shifts the
renewal identity `log|m_i| ≈ log57 + n_i log(4/3)` by an O(1)-per-term amount and is **absent from the second moment**
`Σd_i² = 399 085`. Proposal 2 of the brief — *does {product formula at every i} + {reload recursion} constrain
`Σd_i²`?* — is answered **NO**: adding the 2-adic coordinate to the per-term product formula keeps it first-moment
(one bounded extra scalar/term); the second moment is a sum of **no** per-place read-out. This is `INTRATERM`'s
dimension count (codim-1 vs codim-∞) intact, now with the 2-adic place explicitly included and shown bounded.

## 4. The cap-legal fatal adversary is 2-adically FEASIBLE — CRT independence `[CONSTRUCTED, verified]`

The decisive adversarial test (proposal 3): take a cap-legal heavy-tail depth sequence `d_i` (o4 slope `0.262`, deep
excursions scheduled within the growing archimedean budget; `E[d]=2.06`, max `d=1102`, `Σd²/M` super-linear
`108.5→410.5`) and ask whether the **2-adic valuations it would REQUIRE are realizable by integers** — the analogue
of the archimedean feasibility that killed the naive u₀.

> **`[PROVEN, CRT]`** `v₂(m)=t` and `v₃(m)=d` are conditions at **coprime moduli** `2^{t+1}` and `3^{d+1}`. Hence for
> ANY `(t,d)` and any target magnitude, the integer `m = 2^{t}·3^{d}·(rest)`, `rest⊥6`, realizes all three places
> simultaneously — subject only to `rest≥1`, i.e. **only to the joint cap** of §2. The 2-adic condition is a bounded
> (`t≤3`) congruence choice on the reload unit, exactly the **INTRATERM Haar-preserving factor**, null in the tail.

Constructed and verified: **0/4000 joint-cap violations, 0/4000 2-adic realization failures.** Explicit witnesses
(reload `i`, target `d₃`, target `v₂`, realized `v₂(m)`, realized `v₃(m)`): `(8,8,0,0,8)`, `(32,21,0,0,21)`,
`(64,38,0,0,38)`, `(256,140,0,0,140)` — deep integers with the prescribed depth AND 2-adic valuation AND magnitude.
The adversary schedules its **deep excursions at branch `ρ=1`** (fixed point `−14`), where `v₂(m)=0` **exactly**
(empirically **44 513/44 513** ρ=1 reloads have `v₂=0`), so the 2-adic tax is **zero** and the joint cap equals the
archimedean cap. Even if a deep excursion were *forced* onto a `v₂=3` branch, the joint cap shaves its depth by only
`3·log₃2 = 1.893` bits (`≤2` in integer depth) — **cannot** halt the divergence of `Σd²`.

## 5. What was built / the precise residual

| item | result | label |
|---|---|---|
| Joint valuation structure of `m_i` | `d_i=v₃`, `v₂∈{0,2,3}` (max 3, mean .89), `\|m\|≈57(4/3)^{n_i}`; product formula exact 0/133 374 | `[PROVEN + OBSERVED]` |
| 2-adic place resets | `v₂(m_{i+1})=v₂(Δ_i)` bounded; `v₂(G_{n+1})=1⟺ρ_n=1` exact to 120k | `[PROVEN mechanism]` |
| Joint run-cap vs archimedean | sharpening `= v₂·log₃2 ≤ 1.893 bits`, **O(1), never n-scaling** | `[PROVEN]` |
| Product formula reaches `Σd²`? | **NO** — 2-adic term `Σv₂log2=O(M)` is first-moment; `Σd²` untouched | `[PROVEN]` |
| 2-adic feasibility of fatal adversary | **FEASIBLE** — CRT: bounded congruence on the unit; 0/4000 joint-cap violations, 0 realization failures; deep excursions at ρ=1 pay zero 2-adic tax | `[CONSTRUCTED, verified]` |
| **Does the joint (∞,2,3) exclude the cap-legal adversary?** | **NO** | `[OPEN = (K)]` |

**Precise residual — is it a "3-place tautology" or does it add over first-moment ⊕ archimedean-support?** The
answer is **sharp**: the three places give `{first moment (product formula)} ⊕ {archimedean support (run-cap)} ⊕
{bounded 2-adic congruence}`. The 2-adic place is **not vacuous** — it does tighten the run-cap, and it does bite the
cap-*saturating* adversary — but its content is **bounded (≤1.893 bits)** and **evadable** (schedule deep excursions
at `ρ=1`, `v₂=0`), because `v₂(m_i)` is a **deterministic, time-shifted copy of the branch itinerary** carrying no
information beyond `ρ`. So relative to U0's `{first moment ⊕ archimedean-support}`, the third place adds **only an
O(1) congruence, not a second n-scaling constraint** — it collapses, up to a bounded correction, to the SAME pair. It
is a **near-tautology at the 2-adic place**: the reload unit lives in `ℤ₃^×`, the SAME integer's 2-adic valuation is
a free bounded congruence orthogonal to the 3-adic depth (CRT), and neither reaches the second moment. The wall is
unchanged in species: an a-priori one-sided single-orbit large-deviation frequency bound `freq{3∣W_n} ≤ 4/5−ε`
(base-4/3 normality, AEV Conj 1.6) = (K).

Reproduce: `scratchpad/joint_adelic_build.py` (PART A joint valuations + product formula + joint cap; PART B 2-adic =
deterministic branch itinerary; PART C CRT-feasible cap-legal fatal adversary 0/4000; PART D product formula stays
first-moment). Basis: `U0_EXCLUSION_BUILD_2026-07-10` (archimedean run-cap this goes beyond),
`INTRATERM_ADELIC_MINING` (per-term first-moment / Haar-preserving factor), `RELOAD_EXCURSION_BUILD` +
`RELOAD_MAP_UNIFIED_2026-07-09` (exact reload map), `O4_NEWMATH_BUILD_2026-07-09` (fatal = `freq{3∣W_n}≥4/5`),
`NEWMATH_BUILD_SYNTHESIS_2026-07-09`. Kernel anchor AEV arXiv:2510.11723.

No machine decided. No label upgraded.
