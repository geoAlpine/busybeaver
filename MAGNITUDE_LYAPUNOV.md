# Magnitude-aware Lyapunov for the induced Antihydra odd map — WEAPONS AUDIT (2026-06-30)

*Target: the sole un-killed structural variant flagged in `MINPROP_COBOUNDARY_LP.md §5`:
an UNBOUNDED, magnitude-aware Lyapunov `g(o) = α·log2(o) + h(o mod 2^k)` (`h` bounded),
sought to satisfy the one-sided coboundary `ψ(o) ≤ g(T(o)) − g(o)`. Verify or BREAK the
sign-tension hypothesis (useful sign α<0 is infeasible; feasible sign α>0 is vacuous), and
decide the DECISIVE question: does the conditional/threshold version (restrict to `o>M0`)
escape the high-D obstruction or hit the same wall. Induced map `T(o)=3^{D−1}(3o−1)/2^D`,
`D=v2(3o−1)≥1`, seed `o0=27`. `ψ = ½ − 1{D≥2} − 1{D≥3}`. SOUNDNESS: zero false proofs;
every claim labelled. Numerics `.venv`, exact big-int. NOT committed.*

---

## 0. One-line verdict

**CLEAN NO-GO `[PROVEN]`.** The sign tension is CONFIRMED and, for the useful sign, the
obstruction is *even sharper* than via invariant measures: the per-step constraint already
fails. The useful sign `α<0` is INFEASIBLE — both globally and **conditionally for `o>M0`** —
because arbitrarily LARGE integers `o>M0` carry arbitrarily large `D=v2(3o−1)`, so the
modified observable `ψ̃ = ψ − α·log2(3/2)·D = ψ + |α|·log2(3/2)·D` is unbounded ABOVE on
`{o>M0}` and a bounded `h` cannot absorb it. The feasible sign `α>0` telescopes to
`Σψ ≤ α·log2(o_N)+O(1) → +∞` (orbit grows), so it is VACUOUS. The threshold `o>M0` does
**NOT** exclude the high-D obstruction, because high `D` lives at *arbitrarily large* `o`,
not near small `o`. The last structural door is closed; no machine decided; no label upgraded.

---

## 1. The exact size-drift identity `[PROVEN]`

`T(o) = 3^{D−1}(3o−1)/2^D`, so
> `T(o)/o = (3/2)^D · (3o−1)/(3o) = (3/2)^D · (1 − 1/(3o))`,
hence the **exact** identity (no asymptotics):
> `log2(T(o)/o) = D·log2(3/2) + ε(o)`,  `ε(o) := log2(1 − 1/(3o)) ∈ (−∞, 0)`.

- `ε(o) < 0` always (size drift is slightly BELOW `D·log2(3/2)`), and `ε(o) → 0⁻` as `o→∞`
  (`ε(o) ≈ −1/(3o·ln2)`). So for large integer `o` the drift is `D·log2(3/2)` up to a term
  that → 0 and is uniformly bounded on `{o ≥ o0}`.
- **Caveat (load-bearing):** `ε` is NOT small at the obstruction *measures*. At a constant-`D=d`
  2-adic fixed point `o_d = 3^{d−1}/(3^d−2^d) ≈ 1/3`, `T(o_d)=o_d` ⟹ `log2(T/o)=0`, so
  `ε(o_d) = −d·log2(3/2)` exactly cancels the drift. Magnitude `log2 o` is an **archimedean**
  quantity living on the integer orbit; the symbolic obstruction fixed points sit at small `|o|`.
  This is why the decisive analysis (§4) is done on large *integers*, not on `Z_2^*` measures.

`[PROVEN]` (closed form). Numerics §6 confirm `ε` exact and `→0`.

## 2. The reduction to a modified observable `[PROVEN]`

`ψ(o) ≤ g(To)−g(o) = α(log2 To − log2 o) + (h(To)−h(o)) = α D log2(3/2) + α ε(o) + h(To)−h(o)`.
Set `c := log2(3/2) = 0.5849625…` and the **modified observable**
> `ψ̃(o) := ψ(o) − α·c·D`.
The inequality becomes `ψ̃(o) − α ε(o) ≤ h(To) − h(o)`. Since `α ε(o)` is bounded on `{o≥o0}`
(→0), bounded `h` feasibility is governed by `ψ̃` exactly as in the bounded-LP theory:
> **bounded `h` exists ⟺ Birkhoff sums of `ψ̃` are uniformly bounded above ⟺
> `sup_ν ∫ψ̃ dν ≤ 0` over `T`-invariant measures ν** (Mañé/Conze–Guivarc'h sub-action), and
> `∫ψ̃ dν = ∫ψ dν − α·c·E_ν[D]`.

## 3. Sign tension — CONFIRMED `[PROVEN]`

**Useful sign `α<0` ⟹ INFEASIBLE.** `∫ψ̃ dν = ∫ψ dν + |α|·c·E_ν[D]`. The constant-`D=d`
2-adic fixed points `o_d` are genuine atomic `T`-invariant measures with `E_ν[D]=d`,
`∫ψ dν = ψ(d) ∈ {+½,−½,−3/2}` (bounded). Hence
> `∫ψ̃ d(δ_{o_d}) = ψ(d) + |α|·c·d → +∞` as `d→∞`,  so `sup_ν ∫ψ̃ = +∞`.
More generally any full-branch Bernoulli stationary `D`-law with `E[D]→∞` does this. INFEASIBLE.
And telescoping with `α<0` would have given `Σψ ≤ α·log2(o_N)+O(1) → −∞` (USEFUL) — i.e. the
useful sign is exactly the infeasible sign. `[PROVEN]`

**Feasible sign `α>0` ⟹ VACUOUS.** `∫ψ̃ dν = ∫ψ dν − α c E_ν[D]`. As a function of the current
symbol, `ψ̃ = ψ(d)−α c d` is maximized at `d=1`: `sup_ν ∫ψ̃ = ½ − α c`, which is `≤0` iff
`α ≥ 1/(2c) = 0.8548…`. So feasibility holds for `α ≥ 0.8548`. But telescoping then gives
`Σ_{j<N} ψ(o_j) ≤ α(log2 o_N − log2 o_0) + 2‖h‖_∞`. The orbit grows (`§5`), so `log2 o_N → +∞`
and with `α>0` the bound `→ +∞`; dividing by `N`, `log2 o_N/N → c·(mean D) > 0`, so the bound
on `limsup(1/N)Σψ` is a POSITIVE constant — VACUOUS. `[PROVEN]`

> **Sign-tension theorem `[PROVEN]`.** Useful sign (`α<0`) ⟺ infeasible; feasible sign
> (`α≥0.855`) ⟺ vacuous. There is no `α` that is simultaneously feasible and useful.

## 4. The DECISIVE question: does the threshold `o>M0` escape? — NO `[PROVEN]`

The conditional proposal: demand `ψ(o) ≤ g(To)−g(o)` only for `o>M0`, plus a finite check that
`o0`'s orbit eventually stays above `M0`. Granting the orbit hypothesis (§5, PROVEN), the
conditional certificate with `α<0` would telescope on the high tail to `Σψ → −∞` — i.e. it WOULD
prove (K). So the only question is whether the conditional certificate is FEASIBLE. It is not:

> **The high-D wall is NOT confined to small `o`.** For any `d` and any threshold `M0`, the
> residue class `o ≡ 3^{−1} (mod 2^d)` contains arbitrarily large integers `o>M0` with
> `v2(3o−1) ≥ d`. For such `o`, the *single-step* constraint reads
> `ψ̃(o) = ψ(o) + |α|·c·D ≤ h(To) − h(o) ≤ 2‖h‖_∞`,
> which FAILS as soon as `D > (2‖h‖_∞ + 3/2)/(|α|·c)`. `[PROVEN]`

So the conditional (`o>M0`, `α<0`) certificate is infeasible at the **per-step** level — we do
not even need invariant measures. The threshold `o>M0` removes only the small-`o` fixed points;
it leaves untouched the genuine obstruction, which is the unbounded valuation `D=v2(3o−1)`
available at arbitrarily large `o`. The feasible sign `α>0` remains feasible conditionally but
remains VACUOUS (same telescoping `→+∞`). **The conditional version hits the SAME wall.** `[PROVEN]`

Reconciliation with §1's caveat: the *symbolic-measure* obstruction (constant-`D` fixed points)
sits at small `|o|`, but the *archimedean-integer* obstruction (large `D` at large `o`) is the
one that matters for a magnitude-aware Lyapunov, and it is dense in size. The threshold escapes
neither — it cannot, because both reduce to the same fact: `D` is unbounded on every tail.

## 5. The orbit grows unboundedly `[PROVEN, elementary]`

For integer `o>1` and any `D≥1`: `T(o)/o = (3/2)^D(1−1/(3o)) ≥ (3/2)(1−1/(3o)) = (3o−1)/(2o) > 1`
iff `o>1`. So `T` is strictly increasing on integers `>1`; the orbit of `o0=27` is strictly
increasing, hence `o_j→∞` and `log2 o_j→∞`. (Note: unbounded *growth* is elementary and does
NOT settle (K), which is about the Cesàro density of `D≥2,3`, a frequency statement.) `[PROVEN]`

## 6. Numerics (`magnitude_lyapunov.py`, `.venv`, exact big-int)

**(1) Drift identity exact** — residual `log2(T/o) − (D·c + ε(o))` is `< 2.3e−16` (float
round-off) at every test `o`; `ε(o) = log2(1−1/(3o)) < 0` and decays as `o` grows:
`ε(3)=−0.17, ε(27)=−1.8e−2, ε(10^6+1)=−4.8e−7, ε(10^9+7)=−4.8e−10`. `[PROVEN/exact]`

**(2) High-D at large `o`** — smallest integer `> M0=10^9` in class `3^{−1} mod 2^d` has
`D=v2(3o−1) ≥ d`: e.g. `o=1000000171 (D=13)`, `o=1001040555 (D=24)`, `o=733007751851 (D=41)`.
Large `D` is available at arbitrarily large `o` ⟹ the threshold `o>M0` does NOT exclude it.

**(3) sup over constant-`D=d` measures of `∫ψ̃` vs `α`** —
`α=−0.5: +56.996 @d=200 (→+∞, INFEASIBLE)`; `α=−0.1: +10.199 (→+∞)`;
`α=+0.5: sup=+0.21 (>0, infeasible-but-useless-sign)`; `α=+0.855: sup=−0.0000`;
`α=+0.9: sup=−0.027 (feasible)`. Feasibility threshold `α ≥ 0.5/c = 0.85476`. Matches theory.

**(4) Orbit of `o0=27`** — `avg ψ → −0.2506` (Haar `−¼`), `avg D → 2.0007`,
`log2(o_N)` grows linearly (`117037` at `N=10^5`) confirming §5 unbounded growth. The orbit's
own `(1/N)Σ ψ̃`: for `α=−0.5` it is `+0.335 > 0` (so even along this single orbit `Σψ̃→+∞`,
witnessing that no bounded `h` exists — a per-orbit confirmation of §3/§4, since a valid `h`
forces `Σψ̃ = O(1)`); for `α=+0.855` it is `−1.25` (bounded-below but the telescope on the
positive `α·log2 o_N` side is what makes it vacuous, §3).

## 7. Honest verdict

Outcome **(a): clean NO-GO `[PROVEN]`**. The magnitude-aware Lyapunov closes the last
structural door flagged in `MINPROP_COBOUNDARY_LP §5`:
- useful sign `α<0` infeasible (high-D measures `sup_ν∫ψ̃=+∞`; conditionally, per-step failure);
- feasible sign `α≥0.855` vacuous (`Σψ ≤ α·log2 o_N → +∞`);
- conditional/threshold `o>M0` escapes neither, because large `D` occurs at arbitrarily large `o`.

The residual that ANY proof of (K) must supply is unchanged: orbit-specific control that
`o0`'s itinerary has Cesàro density `freq(D≥2)+freq(D≥3) ≥ ½` = single-orbit equidistribution
= Mahler 3/2 / AEV = (K) itself. The Lyapunov adds the archimedean drift coupling but cannot
beat the unboundedness of `D`.

## Sources
- `MINPROP_COBOUNDARY_LP.md` (§5 flagged this variant as the only [OPEN] structural one).
- `MINPROP_ERGODIC_OPT.md` (sub-action criterion `β(ψ)=+½`; maximizer = fixed point `o=1`).
- `INDUCED_RESIDUE_STRUCTURE.md` (T Haar-preserving, exact, Bernoulli; full-branch; `D` i.i.d. geometric).
- `BB6_NO_STRUCTURE_THEOREM.md` (§§1–3, the three structure-only certificate classes).
- This file's numerics: `busybeaver/magnitude_lyapunov.py` (NOT committed).

No machine decided. No label upgraded.
