# Positive lower even-density `liminf even-density ≥ ε > 0` — the v₂(cₙ) floor budget, and why it does not bind (2026-06-30)

*TARGET: prove `liminf_N even-density ≥ ε` for some EXPLICIT `ε>0`, unconditionally — strictly weaker than
(K) = even-density ≥ 1/3, but a genuine new partial (currently only `#even(n) ≥ 0.89 log n` is proven, which is
consistent with even-density → 0). Three fresh angles tried, the lead being a NEW conservation law: track the
2-adic valuation `v₂(cₙ)` itself as a hard-floored potential `≥ 0`. Orbit `c_{n+1}=⌊3cₙ/2⌋`, `c₀=8`.
SOUNDNESS: every line labelled; no (K) claim; willing to retract. Numerics `v2floor.py`, exact big-int, N≤10⁵, <5s.*

---

## 0. One-line verdict

**No angle proves `liminf even-density ≥ ε > 0`.** The `v₂(cₙ) ≥ 0` floor is a genuine new conservation law, but
it is the **wrong sign**: it caps even-RUNS *from above* (an even run cannot exceed the v₂ deposited by the
preceding deep odd step) and is fully satisfied by `v₂(cₙ) ≡ 0` (the all-odd / o-map regime, even-density 0). It
cannot *create* even steps, so it gives no lower bound on even-frequency. The exact reduction is clean and
[PROVEN]: **even-density `= 1 − 1/avgD`**, so `even-density ≥ ε ⟺ avgD ≥ 1/(1−ε)`, and `even-density → 0 ⟺
avgD → 1` (depths `Dⱼ` concentrate at the shallow value 1, i.e. odd values concentrate on `c ≡ 1 mod 4`). Every
proven budget is consistent with `avgD = 1`. **even-density → 0 stays consistent**; the gap is single-orbit
non-concentration on `c ≡ 1 mod 4` = the moving-middle-digit / (K)-adjacent wall.

---

## 1. The v₂(cₙ) telescoping budget, derived exactly [PROVEN, verified]

Two facts about how `v₂(cₙ)` moves under `c_{n+1}=⌊3cₙ/2⌋`:

- **Even step** (`cₙ` even, `c → 3c/2`): `v₂(c_{n+1}) = v₂(3c/2) = v₂(c) − 1` (since 3 is odd). **`Δv₂ = −1`.**
- **Odd step** (`cₙ` odd, so `v₂(cₙ)=0`; `c → (3c−1)/2`): `v₂(c_{n+1}) = v₂(3c−1) − 1 = Dₙ − 1`, where
  `Dₙ := v₂(3cₙ−1) ≥ 1`. **`Δv₂ = Dₙ − 1`.**

Telescoping `Σ_{n<N} Δv₂ = v₂(c_N) − v₂(c₀)` with `E` even steps (each `−1`) and the odd steps (each `Dₙ−1`):
```
−E + Σ_{odd n<N}(Dₙ − 1)  =  v₂(c_N) − v₂(c₀)
⟹  Σ_{odd n<N} Dₙ  =  E + #odd + v₂(c_N) − v₂(c₀)  =  N + v₂(c_N) − v₂(c₀).   [exact, = VALUATION_BUDGET]
```
This recovers the first-moment budget. The genuinely NEW object is the **un-summed potential** `v₂(cₙ)` with its
**hard floor `v₂(cₙ) ≥ 0`** and **ceiling `v₂(cₙ) ≤ log₂ cₙ ≈ 0.585 n`**. The floor reading is the structural
content:

**The countdown / refill structure `[PROVEN, verified 0 exceptions to N=10⁵]`.** Because each even step drops
`v₂` by exactly 1 and `v₂ ≥ 0`, an even run is exactly a countdown of `v₂`. The ONLY way `v₂` becomes positive is
a deep odd step (`D ≥ 2`), which deposits `v₂ = D−1`; the following even run then lasts **exactly `D−1` steps**
until `v₂` hits 0 and `c` is odd again. So:
> **even-runs are funded one-for-one by deep odd steps; an even-run of length `M` is preceded by an odd step of
> depth `D = M+1`.** (Numerically confirmed: `max even-run = max v₂` at every N — see §3.)

Hence the renewal cycle = (1 odd step of depth `D`) + (`D−1` even steps), of total length `D`, giving the clean

> **`even-density = (Σⱼ(Dⱼ−1)) / (Σⱼ Dⱼ) = 1 − #cycles/ΣDⱼ = 1 − 1/avgD`,   `avgD = (1/#odd)Σ_{odd}Dₙ`.**
> `[PROVEN asymptotically; numerics §3 confirm ed = 1−1/avgD to 4 digits]`

Equivalently `even-density ≥ ε ⟺ avgD ≥ 1/(1−ε)` (e.g. `ε=0.01 ⟺ avgD ≥ 1.0101`; `ε=1/3 ⟺ avgD ≥ 3/2`, the (K)
threshold). `even-density → 0 ⟺ avgD → 1 ⟺` almost all `Dⱼ = 1 ⟺` almost all odd `cₙ ≡ 1 mod 4`.

---

## 2. Why the floor does NOT force `ε>0` — the exact wrong-sign asymmetry [the obstruction]

This is the decisive point and answers angle 1 directly.

**The floor `v₂ ≥ 0` is non-binding in the bad regime.** Set every `Dₙ = 1` (every odd `cₙ ≡ 1 mod 4`). Then
every odd step has `Δv₂ = D−1 = 0`, there are **no** even steps, and `v₂(cₙ) ≡ 0` for all `n` — the floor
`v₂ ≥ 0` is satisfied with equality forever. This is the all-odd o-map regime (`c → (3c−1)/2`), `even-density
= 0`, `avgD = 1`. The budget reads `Σ_{odd}Dₙ = #odd = N = N + v₂(c_N) − v₂(c₀)` (with `v₂≡0`), i.e. it is
**satisfied identically**. So the floor carries **no lower bound on #even or on even-frequency**: it cannot
manufacture an even step, because an even step requires `v₂ > 0`, which requires a *prior* deep odd step — exactly
what the bad regime declines to provide.

**The asymmetry, stated sharply.** `v₂ ≥ 0` + (even steps cost `−1`) is an **upper** bound on even-run length
(`M ≤ v₂ at run start = D−1 ≤ 0.585n`), the **opposite direction** from the wanted lower bound on even-frequency.
A floored potential constrains how fast you may *spend*, never that you must *earn*. To force `avgD ≥ 1+δ` you
must prevent the depths from concentrating at `D=1`, i.e. prevent the orbit from concentrating on the shallow
cylinder `c ≡ 1 mod 4` — pure single-orbit non-concentration, which the floor does not see.

**Angle 2 (integrality/growth obstruction): kills "finitely many even", not "vanishing density".** A *strict*
all-odd tail (even-density eventually exactly 0) would need `v₂(cₙ−1) = dₙ ≥ n − N₀ → ∞`, but `dₙ ≤ log₂ cₙ ≈
0.585n`, contradiction for large `n` — this is exactly the proven `#even(n) ≥ 0.89 log n` (infinitely many even
steps; EVEN_DENSITY_PARTIAL). But `even-density → 0` does NOT require a strict tail: O(log n) even steps in
geometrically-growing odd runs realise `Σ run → n` at the boundary (EVEN_DENSITY_PARTIAL: n=10⁹ ⇒ 43 runs,
`Σ=0.99999n`). The growth/integrality obstruction is **marginally** consistent with `avgD → 1`. No obstruction.

**Angle 3 (renewal large-deviation lower bound): no deterministic input.** Even steps are renewal points and
`even-density = 1 − 1/avgD` is the renewal mean, but a *lower* bound on the renewal rate needs a lower bound on
the deep-refill frequency `P(D≥2) = freq(c ≡ 3 mod 4)`, which is precisely the occupancy the proven identities do
not pin (the renewal closed form `freq(D=1) = 1 − 1/E_deep` has no one-sided margin — MINPROP_RUNS, EK2). No
deterministic renewal inequality beats `avgD ≥ 1` (= `ed ≥ 0`, vacuous).

---

## 3. Numerics `[OBSERVED, exact big-int, v2floor.py, N≤10⁵, 4.2s]`

| N | even-density | `1 − 1/avgD` | avgD | `N₃/O` (`c≡3 mod4`) | budget `ΣD = N+v₂(c_N)−v₂(c₀)`? | min v₂ | max v₂ | max even-run | max odd-run |
|---|---|---|---|---|---|---|---|---|---|
| 10³ | 0.4990 | 0.4975 | 1.9900 | 0.4810 | exact | 0 | 10 | 10 | 8 |
| 10⁴ | 0.4954 | 0.4952 | 1.9812 | 0.4879 | exact | 0 | 15 | 15 | 11 |
| 5·10⁴ | 0.4997 | 0.4997 | 1.9988 | 0.5006 | exact | 0 | 15 | 15 | 14 |
| 10⁵ | 0.5016 | 0.5016 | 2.0064 | 0.5021 | exact | 0 | 15 | 15 | 20 |

Observations confirming the structure (NOT the proof): (i) the budget identity `ΣD = N + v₂(c_N) − v₂(c₀)` is
**exact** at every N (boundary term `v₂(c_N)` shows: 0 when the orbit ends on an odd step, 3 at N=10⁵). (ii)
`even-density = 1 − 1/avgD` to 4 digits — the renewal formula is exact. (iii) **`min v₂ = 0` at every N** — the
floor is *reached constantly*, confirming it is non-binding (the orbit empties its v₂ reservoir every cycle and
the floor never forces a refill). (iv) **`max even-run = max v₂` exactly** — even runs are precisely the v₂
countdowns, funded by deep odd steps. (v) `even-density ≈ 0.50`, `avgD ≈ 2`, `N₃/O ≈ 0.50` — Haar values, margin
`4/3` over the (K) threshold `avgD=3/2`. All consistent with `ε=1/3` being TRUE — but the same
equidistribution-flavoured data finite N can never upgrade, and every proven identity also permits `avgD → 1`.

---

## 4. Honest verdict

| angle | claim attempted | status |
|---|---|---|
| 1. v₂(cₙ) floor budget | `v₂ ≥ 0` forces #even / even-frequency lower bound | **NOT achieved** — floor is wrong-sign (caps even-runs above), satisfied by `v₂≡0` (all-odd) |
| 2. integrality/growth obstruction | seed-8 orbit forbids even-density → 0 | **NOT achieved** — only forbids *finitely many* even (= `#even ≥ 0.89 log n`); vanishing density marginally OK |
| 3. renewal large-deviation | deterministic lower bound on renewal rate | **NOT achieved** — needs lower bound on `freq(c≡3 mod 4)`; no one-sided margin |
| **reduction (clean, new framing)** | **`even-density = 1 − 1/avgD`; `ε>0 ⟺ avgD ≥ 1+δ` (depths not concentrated at `D=1`)** | **[PROVEN] reduction; the bound itself OPEN** |

**The exact gap.** The proven budget `Σ_{odd}Dₙ = N + o(n)` is satisfied identically by `Dₙ ≡ 1` (because then
`ΣD = #odd = N`), which is `even-density = 0`. The identity bounds `avgD` *only* by `avgD ≥ 1` (i.e. `ed ≥ 0`,
vacuous). The hard floor `v₂ ≥ 0` adds nothing in this direction (it bounds even-runs from above). To get `avgD ≥
1+δ` for ANY explicit `δ>0` one must prove the depths do not concentrate at `D=1`, i.e. the odd subsequence does
not concentrate on `c ≡ 1 mod 4` — a positive-density statement about a single deterministic orbit's residues =
the moving-middle-digit / Mahler-3/2 single-orbit non-concentration wall. No proven 2-adic identity, and no
sign-floored potential, bridges "satisfied-by-`D≡1`" to "`avgD` bounded above 1".

So even the **weakest** target `ε=0.01` is NOT a free partial: it is `avgD ≥ 1.0101` = a one-sided fractional
positive-density bound on `{c ≡ 3 mod 4}`, of exactly the same single-orbit-equidistribution character as (K)
itself, only with a smaller (but still positive) margin requirement. Positive even-density is `(K)`-hard in kind,
not just in degree.

---

## Sources

- `VALUATION_BUDGET.md` — the PROVEN first-moment budget `Σ_{odd}v₂(3cᵢ−1)=n+v₂(cₙ)−v₂(c₀)`; recovered here from
  the un-summed v₂ potential; the unconditional range `Dᵢ ≤ 0.585n`.
- `EVEN_DENSITY_PARTIAL.md` — the proven `#even(n) ≥ 0.89 log n`; the marginal geometric-run scenario realising
  `even-density → 0` at the growth boundary (kills angle 2); the shrinking-target / Borel–Cantelli wall.
- `EK2_SECOND_BUDGET.md` — third criterion form `Non-halt ⟺ avgD_odd ≥ 3/2`; first-moment-is-a-count tautology;
  potentials telescope `ΣK^p` to themselves (the floor's wrong-sign analog at p=1).
- `NONATOMIC_FIXEDPOINT.md` — countdown structure `dₙ→dₙ−1` [PROVEN]; first-vs-second-moment gap; `f_k → 0` open.
- `M4_P2_RESULT.md` — `avgD × density` is an identity bounding neither factor; integrality = rigidity, bias-blind.
- `v2floor.py` (scratchpad) — exact big-int verification: budget identity exact; `ed = 1−1/avgD`; `min v₂ = 0`,
  `max even-run = max v₂` (floor non-binding / even-runs are v₂ countdowns), N≤10⁵.

No machine decided. No label upgraded.
