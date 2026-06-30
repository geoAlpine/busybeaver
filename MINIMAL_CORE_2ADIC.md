# The minimal core after the sliding-lock collapse: specified-orbit genericity for ONE 2-adic Bernoulli orbit (2026-06-30)

*Reformulation of the new-mathematics target (roadmap re-examination, user request 2), sharpened by the 3-adic
sliding-block lock (`THREEADIC_SLIDING_LOCK.md`). That lock proved the `ℚ₃` place is a deterministic
sliding-block-code factor of the 2-adic depth process — so the solenoid's extra direction is inert, and the
irreducible object is purely 2-adic. This note states the minimal new-math object in its barest coordinates, drops
the adelic scaffolding shown to add nothing, and records honestly what is known and what is missing. SOUNDNESS: this
is `(K)` re-coordinatized, NOT made easier; the reduction steps are `[PROVEN]`; the target stays `[OPEN]`. NOT
committed by default.*

---

## 0. The collapse, in one line

Every place and every auxiliary structure the program built — the 3-adic coordinate, the carry `S_n`, the second
Mahler diagonal, the solenoid host — is `[PROVEN]` a **factor of the single 2-adic depth process** `(D_j)`,
`D_j = v₂(3o_j−1)` (3-adic via the sliding-block code `Ψ`; carry via `2ⁿc_n+S_n=8·3ⁿ`; diagonals via the seam
identity). So the genuine, irreducible object is the **2-adic induced map on one orbit**, and nothing else.

## 1. The minimal object `[PROVEN reduction]`

> **`(ℤ₂^×, T)` exact-Bernoulli, single orbit.** `T(o) = 3^{D−1}(3o−1)/2^{D}`, `D = v₂(3o−1)`, on the odd 2-adic
> units `ℤ₂^×`, started at the **specified** `o_0 = 27`. Under Haar on `ℤ₂^×`, `T` is **measure-preserving, exact,
> Bernoulli** with depth law `P(D=d) = 2^{−d}` i.i.d. (Bernstein–Lagarias 2-adic conjugacy; mean `D = 2`).

> **The kernel, minimal form.** `(K) ⟺` the single orbit `(o_j)_{j≥0}` of `o_0=27` satisfies `liminf_N (1/N)Σ_{j<N}
> D_j ≥ 3/2` (equivalently `liminf` even-density `≥ 1/3`). The genuine `(K)`-equivalent is this **one-sided liminf on
> the depth mean** — strictly weaker than full Haar-genericity of the orbit (which would control every cylinder).

There is no 3-adic, no `∞`-place, no solenoid in this statement. Those were `[PROVEN]`-inert (sliding lock + factor
identities); carrying them only added directions deterministically slaved to `(D_j)`.

## 2. Why dropping the solenoid is now justified (not a retreat) `[PROVEN]`

The solenoid placement (`BB6_FRAMEWORK_PACKAGE.md` §5) was valuable for *naming* the obstruction (AIU + ENT, proven
Rudolph–Johnson) and for the cross-field outreach. But for *attacking* the kernel it offered hope only through the
`ℚ₃` direction (Q-B), and the sliding-block lock closed that: `ℚ₃ = Ψ((D_j))`. The rank-1-in-rank-2 host does not
give extra leverage because the second place is a deterministic image of the first. Hence the minimal attack surface
is `(ℤ₂^×, T, o_0=27)` — a *one-place* problem. This is a genuine simplification of the **target description**, not
of the **difficulty** (the difficulty is conserved: it is still `(K)`).

## 3. The new-math object, restated minimally

> **Wanted:** a one-sided positive-density (liminf) bound on the depth sequence `D_j = v₂(3o_j−1)` of the **single
> specified** 2-adic orbit `o_0 = 27` of the exact-Bernoulli map `T` — i.e. **specified-orbit (quenched) genericity,
> or even just a one-sided depth-mean bound, for one orbit of a 2-adic Bernoulli automorphism.**

This is the **absolute minimal** empty-toolbox spot, the same wall as the `(d)` Coverage No-Go
(`RANK1_AMENABLE_EQUIDISTRIBUTION.md`) but in one place instead of on the solenoid. The Coverage Theorem applies
verbatim: every framework that proves genericity needs `{rank≥2 / non-amenable / unipotent / a.e.-in-support /
extremal / bounded-carry}`, and a single cyclic 2-adic Bernoulli orbit has none.

## 4. What is known about this minimal object (honest inventory)

- `[PROVEN-in-lit]` `T` is conjugate to the one-sided 2-adic shift; **Haar-a.e.** orbit is generic (Birkhoff +
  exactness). The exceptional (non-generic) set is `μ`-null but has **full Hausdorff dimension and full entropy**
  (Barreira–Schmeling), and contains the halting fixed point `o=1` (`D≡1`, mean `D=1<3/2`) — so genericity is
  **false for some specified orbits**, and the specified `o_0=27` cannot be decided by any a.e./all-orbits argument
  (the No-Structure theorem, `BB6_NO_STRUCTURE_THEOREM.md`, applies in these minimal coordinates too).
- `[PROVEN]` banked one-orbit facts: `#even(n) ≥ 0.89 log n`; valuation budget `Σ_{i<n} D_i = n + v₂(c_n) − v₂(c_0)`
  (first moment, exact); periodic-orbit exclusion; Countdown/Dual-Repulsion (`o=1` repels at `∞` and `2`); finite
  check `balance_n ≥ 0` to `n ≤ 2·10⁵`. All land at the first-moment / a.e. / topological tier.
- `[OPEN]` the second-moment / quenched-frequency content: `liminf` depth-mean `≥ 3/2` for *this* orbit. The
  heavy-tailed adversary (`E[K²]=∞`, first-moment-matched, white) — which *halts* — satisfies every proven one-orbit
  fact and is drift-indistinguishable (`EXCURSION_SYNTHESIS.md`). So no proven input separates `o_0=27` from a
  halting orbit; the second moment is the conclusion, not an input.

## 5. The precise missing theorem (minimal)

> **Specified-orbit quenched lower bound for a 2-adic Bernoulli automorphism:** force `liminf_N (1/N)Σ_{j<N} D_j ≥
> 3/2` for the *named* orbit `o_0=27` of `T`, using the orbit's specific 2-adic arithmetic, **without** assuming the
> depth law (which is `(K)`) and **without** an a.e./annealed reduction (which cannot see the named orbit). No method
> in the surveyed literature does this for a single cyclic Bernoulli orbit. This is the new mathematics the program
> needs, in its irreducible one-place form.

**Honest status.** This reformulation does not lower the difficulty; it removes the inert adelic scaffolding so the
target is stated in its minimal coordinates. It makes the empty-toolbox spot maximally legible — a *single 2-adic
Bernoulli orbit's quenched depth-mean* — which is the cleanest object to put to a homogeneous-dynamics / 2-adic
ergodic-theory specialist. **No machine decided. No label upgraded.** `(K)` remains `[OPEN]` = Mahler 3/2 / AEV.
