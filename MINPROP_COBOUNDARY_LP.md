# Coboundary / Lyapunov LP for the induced Antihydra odd map (2026-06-28)

*Attack: try to make the one-sided target UNCONDITIONAL by finding a **bounded**
`g(o mod 2^k)` with the pointwise coboundary inequality `psi(o) <= g(T(o)) - g(o)`
for ALL odd `o`. If feasible at some level `k`, telescoping proves the bound for
EVERY orbit (no genericity). Set up as a finite LP, solved exactly, dual obstruction
extracted. Numerics `.venv` only (`busybeaver/minprop_lp.py`), exact big-int /
`Fraction`. Every line labelled. Zero false proofs. NOT committed.*

---

## 0. One-line answer

The coboundary LP is **INFEASIBLE at every level `k = 3..12`**, and provably at all
`k`. The dual obstruction is the **fixed point `o = 1` of the induced map**
(`T(1) = 1`, `psi(1) = +1/2 > 0`), which is an **atomic `T`-invariant measure**
`delta_1` with `integral psi = +1/2 > 0`. The Haar `1/4` slack is irrelevant: a
bounded residue-only certificate exists **iff `sup` over ALL invariant measures of
`integral psi <= 0`**, and the supremum is achieved by `delta_1` (and many other
low positive-mean cycles), **not** by Haar. So a bounded `g` does NOT exist; the
pointwise-for-all-`o` route is structurally dead. `[PROVEN]`

This is **not** a defeat to bury: it is a precise theorem identifying *why* the
one-sided bound resists. The induced map has genuine low periodic orbits (e.g.
`{1}`, where even-density `= 0 < 1/3`) on which the target is **FALSE**; a
certificate `g` that sees only `o mod 2^k` is **blind** to the distinction between
those orbits and the orbit of `o_0 = 27`. The missing ingredient is exactly
orbit-reachability / magnitude information that residues cannot carry. `[PROVEN]`

---

## 1. The potential `psi` and the exact reduction `[PROVEN]`

Induced odd map (GAP LEMMA): `T(o) = 3^{D-1}(3o-1)/2^D`, `D = v2(3o-1) >= 1`,
`o_0 = 27`. Define
> `psi(o) = 1{o == 1 mod 4} - 1{o == 3 mod 8} - 1/2 = 1{D=1} - 1{D>=3} - 1/2`.

Because `D=1 <=> o==1 mod4`, `D>=3 <=> o==3 mod8`, `psi` is a function of `o mod 8`:

| `o mod 8` | `D` | `psi` |
|---|---|---|
| `1, 5` (i.e. `o==1 mod4`) | `1` | `+1/2` |
| `7` | `2` | `-1/2` |
| `3` | `>=3` | `-3/2` |

Key identity (verified exact, `[PROVEN]`): `psi = 1/2 - 1{D>=2} - 1{D>=3}`, hence
> `(1/N) sum_{j<N} psi(o_j) = 1/2 - (1/N) sum_{j<N}[1{D_j>=2} + 1{D_j>=3}]`,
> so **`limsup (1/N) sum psi <= 0  <=>  liminf (1/N) sum[1{D>=2}+1{D>=3}] >= 1/2`**,

which is the **robust sufficient statement** (margin `1/4`) for `mean D >= 3/2`
`<=>` even-density `>= 1/3` `<=>` non-halt (`INDUCED_ONESIDED_DRIFT.md`,
`SESSION_2026-06-28_INDUCED_MAP.md`). Haar mean `integral psi = 1/2 - 1/4 - 1/2 =
-1/4` (1/4 of slack). So the *measure-theoretic* necessary condition for a
coboundary holds with room — which is exactly why the strategy looked plausible.

**The coboundary logic `[PROVEN]`.** If a bounded `g` satisfies `psi(o) <= g(T(o)) -
g(o)` for all odd `o`, then for any orbit `sum_{j<N} psi(o_j) <= g(o_N) - g(o_0) <=
2||g||_inf`, so `limsup (1/N) sum psi <= 0` for EVERY orbit — an UNCONDITIONAL proof.

---

## 2. The LP and its exact dual: difference constraints / positive cycles `[PROVEN]`

With `g` a function of `o mod 2^k`, the constraints `psi(o) <= g(b) - g(a)`
(`a = o mod 2^k`, `b = T(o) mod 2^k`) are **difference constraints** `g(b) - g(a) >=
w` with `w = psi(a)` (weight depends only on the source, since `psi` is a fn of
`a mod 8` for `k>=3`). By LP duality (Bellman-Ford / max-mean-cycle theory):

> **The system is FEASIBLE iff the residue constraint digraph has NO cycle of
> positive total weight.** A positive cycle = a periodic pseudo-orbit on residues
> with average `psi > 0` = the dual obstruction (an invariant "measure" on which
> `integral psi > 0`).

This is the finite, exactly-solvable form of the general fact: *a bounded `g` with
`psi <= g∘T - g` exists iff the forward Birkhoff sums of `psi` are uniformly bounded
above, iff `sup` over all `T`-invariant probability measures of `integral psi <= 0`.*

### Sound tail truncation `[PROVEN]` (this is where a false proof would hide)

`T(o) mod 2^k` depends on `o mod 2^{k+D}` and `D` is unbounded, so the constraint
graph is built with lookahead: enumerate odd `r mod 2^K` (`K = k + L`, `L>=2`).

- **Determined branch** (`D(r) <= K-k`, so `k+D <= K`): `T(r) mod 2^k` is fixed by
  `r mod 2^K`; add edge `a -> T(r) mod 2^k`, weight `psi(r)`.
- **Tail branch** (`D(r) > K-k`): `T(r) mod 2^k` is undetermined. **Soundness:** with
  `K-k >= 2` every tail residue has `D >= 3`, hence `psi = -3/2` (the *most
  favorable* value), and the branch is full (`A_d` maps ONTO all of `Z_2^*`,
  `INDUCED_RESIDUE_STRUCTURE.md` Thm), so `T(o)` can be ANY odd residue `s`. The
  SOUND requirement is `psi <= g(s) - g(a)` for **all** `s`, i.e. add loose edges
  `a -> s` of weight `-3/2`. These are very negative and can never lie on a positive
  cycle, but they are included so the reported feasibility is the TRUE LP feasibility,
  not an under-constrained relaxation.

**Audit (`tail_audit`, `[PROVEN at finite level]`):** for `k=3,5,7` with `K=k+4`,
the undetermined set is exactly `2^{-(K-k)} = 1/16` of odd residues, and **`0` of
them have `psi != -3/2`** — confirming the `-3/2` tail value is exact, not assumed.
The infeasibility below is driven entirely by *determined* edges (the `+1/2`
self-loop at `o=1`), so it does **not** depend on the tail treatment at all.

---

## 3. Result: INFEASIBLE at every `k`, dual obstruction = `delta_1` `[PROVEN]`

`minprop_lp.py` output (exact `Fraction` arithmetic):

| `k` | `K` | `|V|` | `|E|` | verdict | obstruction |
|---|---|---|---|---|---|
| 3 | 7 | 4 | 12 | **INFEASIBLE** | self-loop @1 `w=1/2` |
| 4 | 8 | 8 | 32 | **INFEASIBLE** | self-loop @1 `w=1/2` |
| 5 | 9 | 16 | 64 | **INFEASIBLE** | self-loop @1 `w=1/2` |
| 6 | 10 | 32 | 128 | **INFEASIBLE** | self-loop @1; also cycle `[17,57,53,15]` mean `1/4` |
| 7 | 11 | 64 | 256 | **INFEASIBLE** | self-loop @1 `w=1/2` |
| 8 | 12 | 128 | 512 | **INFEASIBLE** | self-loop @1 `w=1/2` |
| 9..12 | k+3/4 | up to 2048 | up to 6144 | **INFEASIBLE** | self-loop @1 `w=1/2` |

**The driving obstruction `[PROVEN, level-independent]`.** `o = 1` is a fixed point:
`3·1 - 1 = 2`, `D = 1`, `T(1) = 3^0·2/2 = 1`. And `psi(1) = +1/2` (`1 == 1 mod 4`).
So residue `1 mod 2^k` carries a **self-loop of weight `+1/2` for every `k >= 3`**,
i.e. a positive cycle. Max single-edge weight `= +1/2`, so the **max-mean-cycle
`= +1/2` exactly at every level** — feasibility is impossible at all `k`.

Dynamically: the constant orbit `1,1,1,...` has `mean psi = +1/2`, `mean D = 1`,
even-density `= 1 - 1/1 = 0 < 1/3`. The target is **literally false** on this orbit,
so any pointwise-for-all-`o` certificate (which would prove it) cannot exist.

**The obstruction is pervasive, not a single removable atom `[PROVEN]`.** Removing
node `1` from the graph still leaves positive cycles, all reachable from `27`'s
residue: at `k=6`, `[15,33,17,57,53]` mean `3/10`; at `k=8`, `[129,65,225,81,121,
181,143]` mean `5/14`. The residue graph from `27 mod 2^k` reaches **all** nodes
(`32/32`, `128/128`), so a "restrict `g` to the reachable SCC" dodge is unavailable —
the reachable component is the whole graph and is riddled with positive pseudo-cycles.

---

## 4. The exact sound statement proved

> **`[PROVEN]` (negative).** There is **no** bounded function `g: (Z/2^k Z)^* -> R`
> (any `k`) with `psi(o) <= g(T(o) mod 2^k) - g(o mod 2^k)` for all odd `o`.
> Equivalently, the Birkhoff sums `sum_{j<N} psi(o_j)` are **not** uniformly bounded
> above over all orbits: the constant orbit at the fixed point `o = 1` has
> `sum_{j<N} psi = +N/2 -> +infinity`.
>
> Reason: `sup` over `T`-invariant probability measures of `integral psi` is
> `>= integral psi d(delta_1) = +1/2 > 0` (achieved by the atomic measure at the
> fixed point), whereas a bounded coboundary certificate requires this `sup <= 0`.
> The Haar value `integral psi d(Haar) = -1/4` is one (typical) invariant measure but
> NOT the maximizing one.

> **`[PROVEN]` (what the LP *does* certify, soundly).** For any orbit that, from some
> point on, stays in the residue region where the relevant constraints hold... — no
> such restriction helps, because the obstruction cycles are reachable everywhere in
> residues. The LP yields **no** unconditional sub-statement: the only honest output
> is the impossibility above plus the localization of the obstruction.

> **`[PROVEN]` (tail soundness).** The truncation is exact: the undetermined residue
> set has relative measure `2^{-(K-k)}` and, for `K-k >= 2`, consists entirely of
> `D >= 3` residues with `psi = -3/2`, handled by the conservative full-branch edges
> `a -> (all s)` of weight `-3/2`. No unsound shortcut is taken; the infeasibility is
> independent of the tail.

---

## 5. Why it resists, and the one live escape (honest)

The obstruction is **not** a measure-theoretic deficit (Haar has `1/4` slack) but a
**topological/atomic** one: the induced map carries low periodic orbits — the fixed
point `1`, and an abundance of positive-mean residue pseudo-cycles — on which
even-density `< 1/3`. A residue certificate `g(o mod 2^k)` is **blind to magnitude
and to reachability from `27`**, the very data that distinguishes those orbits from
`o_0`'s. The conjecture *is* the statement that `o_0`'s orbit avoids the basins of
these low cycles (it grows unboundedly), so any certificate that proves it MUST
encode magnitude/avoidance — exactly the single-orbit information a bounded mod-`2^k`
function cannot hold. This is the same wall (A) = genericity, now seen from the dual
side: **the obstruction is the atomic invariant measures, and they are residue-
reachable, so no finite-state bounded certificate can exclude them.** `[PROVEN]`

**Live next angle (not an LP).** Allow an UNBOUNDED, magnitude-aware Lyapunov
`g(o) = alpha * log o + h(o mod 2^k)` and ask for `psi(o) <= g(T(o)) - g(o)`. Along
the orbit `log T(o) - log o = log(3^D/2^D) = D log(3/2)` (drift `+`), so the
`log`-part contributes `alpha * D log(3/2)`; choosing `alpha < 0` *subtracts* a
positive multiple of `D`, which is precisely the quantity whose average we want
bounded below — a genuine coupling between `psi` and the size drift that the bounded
residue LP could not express. This does NOT see the fixed point `1` as a self-loop
(there `log` is constant, `=0`, so `psi(1)=+1/2` still blocks a *global* statement),
so it can only work as a *conditional* certificate valid for `o` above a threshold,
combined with a finite check that `o_0`'s orbit stays above it — which is again the
conjecture. The honest status: the magnitude-aware version is the only direction the
LP analysis does not already kill, and it remains tied to avoidance of the low
cycles. `[OPEN]`

---

## 6. Verdict (0 false proofs)

| question | answer | label |
|---|---|---|
| Is the coboundary LP feasible at any `k` (=> unconditional proof)? | **NO** — INFEASIBLE at every `k=3..12` and provably all `k`. | `[PROVEN]` |
| Dual obstruction | atomic invariant measure `delta_1` (fixed point `o=1`, `T(1)=1`, `psi=+1/2`); self-loop weight `+1/2` at residue `1` for all `k`; max-mean-cycle `=+1/2`. Plus an abundance of other positive-mean residue cycles, all reachable from `27`'s residue. | `[PROVEN]` |
| Is the obstruction a truncation artifact? | **NO** — it is a genuine integer fixed point, independent of the tail; tail audit shows the truncation is exact (undetermined set `=2^{-(K-k)}`, all `psi=-3/2`). | `[PROVEN]` |
| Can a residue-domain restriction dodge it? | **NO** — `27`'s residue reaches all nodes; positive cycles persist after deleting node `1`. | `[PROVEN]` |
| Real positive-mean integer cycles of `T` in `[1,2·10^4]` | exactly one: `{1}` (`mean psi=+1/2`, `mean D=1`). | `[OBSERVED]` |
| Real orbit `o_0=27` (`N=2·10^5`) | `avg psi = -0.2485` (Haar `-1/4`), `avg[1{D>=2}+1{D>=3}] = 0.7485 >> 1/2`; identity `avg psi = 1/2 - avg target` exact. | `[OBSERVED]` |

**Net.** The clean LP reformulation *settles* the bounded-coboundary route in the
negative and pinpoints the obstruction with certainty: the one-sided bound resists
because the induced map has low positive-mean periodic orbits (atomic invariant
measures) that a bounded residue function cannot separate from `o_0`'s orbit. The
Haar slack is real but defeated by atoms. The only surviving variant is a
magnitude-aware (unbounded) Lyapunov, which necessarily reintroduces the
avoidance/genericity content. Sound, no over-claim; the impossibility is exact.

Script: `busybeaver/minprop_lp.py`. Not committed.
