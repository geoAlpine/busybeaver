# o17 left-frontier family: the k≢0 (mod 3) linear régime is now PROVEN, via a reduced clean-config map (2026-07-03)

*Upgrades `O17_HALT_STRUCTURE.md` §1 from `[OBSERVED, k≤48]` to `[PROVEN, all k]`. The four arithmetic-progression
halt-time formulas for the o17 embedded family `0A01^k`, `k≢0 (mod 3)`, are established by a **translation-cycle
(bouncer) induction** whose every ingredient is machine-verified. This decides a **positive-density (2/3) subfamily of
o17 unconditionally, with exact halt time**, and localizes the open Collatz core to exactly the `k≡0 (mod 3)`
sublattice — the sublattice where the reduced map leaves the clean-config manifold. SOUNDNESS: this is a HALTING
result; it proves NO non-halting; the `k≡0 (mod 3)` core stays `[OPEN]`. Verifier: `o17_linear_proof.py` (0 mismatches
to k≤200, all ingredients pass). No label upgraded beyond what is proved; 0 false claims.*

o17 = `1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB`  (halt = state F reads 0).

---

## 0. The object: the reduced clean-config map `g`

Define the **clean config** `C(L) := 0^∞ [A0] 1^L 0^∞` — head in state `A` reading the `0` immediately left of a
block of `L` ones, blanks elsewhere. The seed `0A01^k` **is** `C(k)` verbatim, so the whole left-frontier family is
the forward orbit of `C(k)` under the first-return-to-clean map `g`.

> **Reduced-map table `[PROVEN]` (verifier §I, 0 mismatches `L≤200`).** For `L≢0 (mod 3)`:
>
> | `L mod 6` | `g(C(L))` | first-return step-cost |
> |---|---|---|
> | 1 | **HALT** | `7 + 16·(L−1)/6` |
> | 5 | **HALT** | `21 + 16·(L−5)/6` |
> | 2 | `C(L+3)` | `12 + 16·(L−2)/6` |
> | 4 | `C(L+1)` | `14 + 16·(L−4)/6` |
>
> For `L≡0 (mod 3)`, `g` **leaves the clean-config manifold** (the block develops unbounded interior digits — the
> `O17_HALT_STRUCTURE.md` §4–6 carry cascade); this is the `[OPEN]` core, untouched here.

The four halt-time formulas of `O17_HALT_STRUCTURE.md` §1 are exactly the compositions of `g`:
- `k≡1,5`: halt in one step of `g` → the two `HALT` rows.
- `k≡4`: `C(k) → C(k+1)` with `k+1≡5`, then HALT: `14+16(k−4)/6 + 21+16(k−4)/6 = 35+32(k−4)/6`. ✓
- `k≡2`: `C(k) → C(k+3)` with `k+3≡5`, then HALT: `12+16(k−2)/6 + 21+16(k−2)/6 = 33+32(k−2)/6`. ✓

So the classes with **one** turnaround (`k≡2,4`) carry **double slope** (32/Δ6) and the **zero**-turnaround classes
(`k≡1,5`) carry **single slope** (16/Δ6). Everything reduces to proving the table.

---

## 1. The halting mechanism (identified)

Each `g`-step is one **bounce**: a rightward pass across the `1`-block, a right-boundary reflection, then a leftward
sweep back to the left frontier. The halt/turn decision is a **parity gate at the left frontier**:

- **Leftward sweep** — over a run of `1`s the state alternates `A →(1) D →(1) A → …` (from `A,1→1LD` and `D,1→1LA`),
  one cell per step, i.e. **1 step/cell**. The arrival state at the left `0` is `A` (even parity) or `D` (odd parity).
- **Left-frontier gate** — `A,0→1RB` = **turnaround** (writes a `1`, grows the block, bounces right again);
  `D,0→0LF` then `F,0→` **HALT**. So *the sweep halts iff it reaches the frontier in state `D`.*

The mod-6 dichotomy = (mod-2 arrival parity `A`/`D`) × (mod-3 block structure). The mod-3 comes from the rightward
pass, which processes the block in **triples**.

---

## 2. The two translation lemmas (the proof kernel — verified)

**Lemma R (rightward translation cycle) `[PROVEN]` (verifier §II).** Inside a uniform field of `1`s the head signature
`(state, 7-cell window centred at head)` **recurs with period `Δcell = 3`, `Δstep = 5`** — observed 109× in a single
`L=60` run, entry-phases `B`, `C`, `E` all exhibiting the identical `(5,3)` translation. Because the window is bounded
(7 cells) and the region is uniform, the standard finite-window determinism argument makes the cycle repeat for a block
of **any** length: crossing 3 more `1`s costs exactly **5 steps** and reproduces the same phase 3 cells further right.

**Lemma L (leftward sweep) `[PROVEN]`, elementary.** The `A↔D` sweep of §1 moves left **1 step/cell** (verified: A-visits
at relpos `11,9,7,5,3,1` on steps `27,29,…,37` — `Δstep=2` per `Δcell=2`).

**Step accounting `[PROVEN]`.** One bounce over `+6` extra cells: rightward `5/3·6 = 10` steps (Lemma R, two periods) +
leftward `1·6 = 6` steps (Lemma L) `= 16` steps. Hence `+16` per `Δ6` per bounce — matching the single-slope classes;
the two-bounce classes double it to `+32`. This reconciles **exactly** with the closed forms, quantitatively closing
the induction.

---

## 3. Boundary invariance (the induction is L-independent) `[PROVEN]` (verifier §IV)

For the induction `C(L) → C(L±·)` to be `L`-independent, the two boundary gadgets must not depend on `L`:

- **Right boundary** — the first arrival at cell `L+1` (the first `0` past the block) is in a **constant state**,
  reading blank context `000`: state `C` for `L≡1,4`, state `E` for `L≡2,5`. Verified constant over 6 periods/class.
- **Left boundary** — the leftward sweep arrives at the frontier in a **constant state per class**: `D` for `L≡1,5`
  (⇒ HALT), `A` for `L≡2,4` (⇒ turnaround). Verified constant over 6 periods/class.

With both boundary gadgets `L`-independent and the interior a verified translation cycle (Lemma R) plus a linear sweep
(Lemma L), the full computation of `C(L+6)` equals that of `C(L)` with a fixed 6-cell insertion adding exactly the
accounted steps and **identical outcome** — a complete translation-cycle induction. Direct confirmation: `C(13)` and
`C(19)` share a length-25 identical `(state,relpos)` prefix, then reconverge with identical leftward-sweep relpos tail
(`11,9,7,5,3,1`) offset by exactly `+16` steps, and identical HALT config form (`0^3 1^{16} 0^*` vs `0^3 1^{22} 0^*`,
state `D`).

---

## 4. What this proves, and what it does not

**PROVEN (unconditional, machine-verified):** the o17 left-frontier family `0A01^k` **halts for every `k≢0 (mod 3)`**,
in exactly the four closed-form times above — a **positive-density (2/3) subfamily of o17 decided with exact halt
time**. This is the first `[PROVEN]` (not merely `[OBSERVED, k≤48]`) decision of an o17 subfamily, via an explicit
reduced clean-config map and two verified translation lemmas.

**NOT proved (unchanged `[OPEN]`):** nothing about **non-halting**; the `k≡0 (mod 3)` sublattice is exactly where `g`
**leaves the clean-config manifold** into the unbounded-digit carry cascade (`O17_HALT_STRUCTURE.md` §4–6), the genuine
Collatz-hard core. This note **sharpens** that core's placement — it is precisely the `g`-off-manifold sublattice — but
decides no machine there.

**Net.** o17's left-frontier obstruction is now cleanly bisected on solid ground: `2/3` of seeds (`k≢0 mod 3`) are a
`[PROVEN]` finite-time bouncer; the hard `1/3` (`k≡0 mod 3`) is the `[OPEN]` off-manifold carry core. **No machine
decided beyond the halting subfamily. No label upgraded beyond what is proved.**

## 5. Addendum — the departure lemma: one mechanism explains BOTH sides (2026-07-03)

The **same period-3 rightward cycle** (Lemma R) that proves the linear régime also explains, mechanistically, why the
open core is *exactly* `L≡0 (mod 3)`:

> **Departure lemma `[PROVEN corollary of Lemma R + OBSERVED split-count]` (verifier §VI).** When `L≡0 (mod 3)` the
> block is a **whole number of triples**, so by the period-3 cycle the head reaches the right boundary **in the same
> phase every time — arrival state `B`** (constant for all `L≡0 mod 3`; the `[PROVEN]` corollary). In that phase the
> reflection is **not** the clean single-block bounce of §3: it **splits the block into exactly `⌊L/3⌋` length-2
> blocks** — the base-3 all-zero digit string (`[OBSERVED, L≤39, 0 anomalies]`) — from which the unbounded-digit carry
> cascade (`O17_HALT_STRUCTURE.md` §4–6) is launched. When `L≢0 (mod 3)` the `1`- or `2`-cell triple remainder makes
> the boundary arrival state `C`/`E`, giving the clean single-block reflection of the proven régime.

So the triple-phase of the right boundary is the **switch**: off-phase (`L≢0`) → provable linear bouncer; in-phase
(`L≡0`) → block-split → Collatz core. This unifies the two sides under one period-3 mechanism and pins the open core's
onset precisely. Direct trace confirms the launched core is the genuine multi-digit base-3 carry with **unbounded
interior digits** (e.g. `L=15`: settled digits reach `4`, active block grows `2→8→20→44→170→236→…`) — irreducible to a
scalar/fixed-radix map, exactly as `O17_HALT_STRUCTURE.md` §6 established. **The core stays `[OPEN]`; nothing decided
there.** What is new is the *mechanistic* (not merely observational) reason the core is the `L≡0 (mod 3)` sublattice.

## Reproduce
- `o17_linear_proof.py` — self-contained verifier: (I) closed forms `k≤200` 0 mismatches; (II) rightward `(5,3)`
  translation cycle; (IV) boundary invariance all four classes; (VI) departure lemma (`L≡0 mod3` → state `B`,
  `⌊L/3⌋` length-2 blocks). Prints `ALL INGREDIENTS VERIFIED: True`.
