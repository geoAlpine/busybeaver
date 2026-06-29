# The a-priori excursion estimate on V=v₂(c−1) — the last un-pre-empted route, now closed (2026-06-30)

*Deep attack on the one route the previous no-gos did not pre-empt (`CORE_ORBIT_ARITHMETIC.md` §5): a quenched
Kac/return-time / Lyapunov sub-action on the proven 2-adic potential `V=v₂(c−1)`, with the decrease in the conditional
return-time law (per-step feedback is white). Three sub-routes (excursion-level supermartingale; adelic magnitude–depth
budget; integrality/floor structure) all CLOSE. SOUNDNESS: every claim labelled; shuffle/adversary controls run; §13/§14
unfaithful-model trap caught and avoided. (K) [OPEN]. NOT committed by default.*

---

## 0. One-line verdict

**The last un-pre-empted route is closed as a SHARP NO-GO.** No a-priori excursion estimate on `V=v₂(c−1)` exists: every
candidate excursion-level drift is **linear in the entry-depth `K`** (so it reads only the first moment `E[K]`, a free
count `≤N`); forcing the drift to be `~K²` (which is what `E[K²]<∞` ⟺ `μ({1})=0` needs) requires exactly the degree-2
depth potential, which **telescopes to the `0=0` tautology**; and a **heavy-tailed adversary** (`E[K²]=∞`, white,
first-moment-matched) satisfies *every* proven fact yet is drift-indistinguishable from the real orbit for all candidate
potentials. So the second moment is the **conclusion, not a usable input** — the route reduces to single-orbit
equidistribution of `D_n=v₂(3c_n−1)` = (K).

---

## 1. The three sub-routes (all closed, each with a decisive reason)

- **Excursion-level supermartingale** (`EXCURSION_SUPERMARTINGALE.md`) — the core attempt. Kac sharpens the gap:
  even-density `= E[even-run]/E[R]`, so the renewal identity controls the **first** moment `E[K]` (free) and is
  structurally silent on the **second** `E[K²]` (the return-time energy). Every candidate `W` (e.g. `α log c + V`;
  `log·oddpart(c−1)`; bounded) has conditional excursion drift `g(K)=E[ΔW|K]` **at most linear in `K`** (measured
  `≈−1.3K, +K, ≈0`), so the mean drift reads `E[K]` only. A `g(K)~K²` potential is killed two independent ways:
  **(white-jump)** jumps are unpredictable (`K`-autocorr ≤0.012), so the compensating drift is `E[K²]`/excursion, finite
  iff `E[K²]<∞` (circular); **(telescoping)** the only `g(K)=K²` potential is `Q=d²`, which telescopes exactly to the
  EK2 `0=0` tautology. **Adversary control: NO survivor** — a heavy-tailed iid-`K` adversary gives the same drift sign as
  the real orbit for every `W` (`W₁`: real −1.62 vs adversary −3.59). §13/§14 trap caught: the `R²(K|c′ mod 2^m)→0.998`
  "predictability" is mere deterministic readout of the bits that *define* `K`; a level-`m` `W` misses the tail `K>m`, and
  the all-levels `W` is `Q=d²` (circular).
- **Adelic magnitude–depth budget** (`EXCURSION_ADELIC_BUDGET.md`) — a height-`K` excursion's countdown multiplies
  `|o−1|_∞` by `(3/2)^K`, but the per-step adelic increment is **depth-independent** (archimedean `(3/2)`/step, height
  `+log 3`/step), so summed it charges only `Σ K_i ≤ ΣD` (first moment) and **cannot reach `Σ K_i²`**.
  **Clustering-indifference (decisive):** one giant height-49948 excursion carries the *same* archimedean budget as ~50000
  short ones, yet `E[K²]=∞` — the budget cannot see the heavy tail. Product formula on `f_K=freq{o≡1 mod 2^K}` is
  codim-1 (a first-moment tautology) vs the codim-∞ tail.
- **Integrality / floor structure** (`EXCURSION_INTEGRALITY.md`) — the `−1` and the M4 budget give only `ΣK≤N` and the
  support cap `K≤0.585n`; the `p=2` accounting closes on itself (the second moment is **as bias-blind as the first**).
  **New decisive negative:** integrality imposes **no a-priori spacing** between deep excursions — successive deep entries
  cluster at the iid rate (min gap = 1, adjacent-pair count `≈N·p²`), so this fails *earlier* than the min-gap-vs-density
  wall (there is no nontrivial min-gap to deploy).

---

## 2. What this completes

With the excursion/return-time route closed, **the attack landscape is now proven-closed in every register**:
- structural (residue coboundary / all-orbits / measure-level) — No-Structure theorem;
- spectral (the gap is blind to the odd block) — endogenous-UE no-go;
- unbounded magnitude-aware / adelic sub-actions — sign-tension + product-formula no-go;
- **quenched excursion / Kac return-time / Lyapunov on `V`** — *this note* (drift linear in `K`; heavy-tailed adversary
  matches all proven facts).

All reduce to the single irreducible statement: **single-orbit equidistribution of `D_n=v₂(3c_n−1)`** = the quenched Weyl
sum = annealed→quenched transfer of `ν̂_{2/3}` = (K) = Mahler 3/2 / AEV Conj 1.6.

**The sharpest honest statement of the generational gap:** the proven facts about the orbit are *consistent with both* (K)
and its negation — a heavy-tailed `K` (atom at `o=1`, halting) satisfies every unconditional identity, count, support
bound, adelic budget, and excursion drift. Only the orbit's *specific* arithmetic — the actual value of `E[K²]` / the
actual occupancy `f_K` — decides, and computing it *is* solving Mahler/AEV. There is **no proper sub-problem and no
un-pre-empted route**: the second moment is the conclusion, never an input.

**No machine decided. No label upgraded.** (K) remains [OPEN] = Mahler 3/2 / AEV.
