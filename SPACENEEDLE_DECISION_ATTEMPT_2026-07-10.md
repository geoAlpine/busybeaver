# Space Needle — decision attempt via a finite invariant on the sporadic thin-set fatal set (2026-07-10)

*Attacks the Type-III cryptid **Space Needle** (μ = 5/2, the frontier's one non-(K) machine) with the
o7-style reachable-residue / congruence-automaton method: prove non-halt by showing the counter orbit's
residues avoid the fatal residue classes. **Outcome: the attack fails at its root — no finite congruence
invariant exists.** SN's fatal-set avoidance is a genuine 2-adic reachability wall. SOUNDNESS:
`[PROVEN]`/`[OBSERVED]`; zero false proofs; halting stays `[OPEN]`. Interpreter
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`. Scripts `snd_dynamics.py`, `snd_automaton.py`,
`snd_verdict.py`. Not committed.*

## 1. Exact dynamics + halt condition, re-derived and verified `[PROVEN from table]`

SN = `1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD`. Milestone normal form: `0^∞ 1^m 0^∞`, head on the `0`
right of the block, state `C`. One epoch is the 2-adic-digit map
> **`f(m) = m + 3·⌊m / 2^{v+1}⌋ + v`,  `v` = number of trailing 1-bits of `m`.**

**Halt gate** (`SPACE_NEEDLE_HALT.md`, re-read): the only halt is `F,0`; `F` is entered only via `C,0→1LF`
(write 1, move left), so **HALT ⟺ state `C` reads a `0` whose left neighbour is `0`**. An epoch seeded by
`1^m` halts iff `m` lands in the fatal set `S`. **Non-halt ⟺ the orbit `m₀=2, m_{n+1}=f(m_n)` never enters
`S`.**

**Verification (`snd_dynamics.py`, 0 mismatch):**
- Raw TM from a truly **blank tape**, 300 000 steps: does **not** halt; milestone sequence `[2,5,9,16,40,100]`
  is reproduced **exactly (6/6)** by iterating `f` from `m₀=2` (offset 0).
- `f` vs the raw TM, epoch-by-epoch, `m = 2..399`: **398/398 consistent** (halts counted consistently).

**Fatal set** (`SPACE_NEEDLE_HALT.md` census, S∩[1,599]): `S = {2^k−1 : k≥1} ∪ {6,102,311,351,371,…}` — the
all-ones cylinder (`m=2^k−1 ⟺ m+1` a power of 2) plus a sporadic 00-defect set. **`S ⊋ {2^k−1}`; the
sporadic rule is `[OPEN]`.**

## 2. Orbit vs. the finite sporadic part `[OBSERVED]`

Orbit values ≤ 600: `[2,5,9,16,40,100,250]`, then 625. So:
- `orbit ∩ {6,102,311,351,371} = ∅` — no small sporadic is ever hit.
- The orbit is **permanently > 371** (max known sporadic) from **gen 7** (`m=625`) and strictly increasing
  thereafter. **The small sporadic part is long-passed.**
- `orbit ∩ {2^k−1} = ∅` over 4000 generations.

So the *residual* fatal target is the **infinite all-ones family `{2^k−1}`** (plus any unknown sporadics
beyond 371). This is exactly the setup the attack needs.

## 3. The decision test — reachable residues vs. fatal residues `[the attack, and why it fails]`

`m = 2^k−1` forces, for every modulus `M`, `m ≡ (2^k−1) (mod M)`. Let `A_M = {(2^k−1) mod M : k≥1}`
(finite, period `ord_M(2)`). **If some `M` had the orbit residues `{m_n mod M}` avoiding `A_M` forever, the
orbit could never be all-ones → NON-HALT `[PROVEN]`.**

**Result (`snd_automaton.py`, 6000 gens, exact big-int, final width 5648 bits): NO such `M` exists.**
- Every tested modulus (all `M = 3..199`, plus `256,512,1024,4096,1155,3072,65535,65537`): the orbit **hits
  `A_M`**, typically within the first ~15 generations.
- **Equidistribution**: `M=7,31,63,127,255` → the orbit covers **all** `M` residues; `M=1023` covers
  1007/1023. The residue stream is **not eventually periodic** — it fills the whole class group and therefore
  meets every `A_M`. There is **no separation at any modulus.**

**Why no deeper look-ahead rescues it (`snd_verdict.py`, the fundamental obstruction).** The o7 method needs
`f` to be a **finite-state congruence** — `f(m) mod M` a function of finitely many low bits `m mod 2^j`. It
is **not**: the term `⌊m/2^{v+1}⌋` shifts *unboundedly-high* bits down into the low part. Concretely, for
every `M ∈ {7,31,255}` and every depth `j ∈ {4,8,12,16,20}`, we exhibit `u ≡ w (mod 2^j)` with
`f(u) ≢ f(w) (mod M)`. So **no mod-`M`, mod-`2^j·M`, or bounded-parity-look-ahead automaton over-approximates
the reachable set** — the reachable set is not a finite-automaton language. This is the Collatz / (K) wall in
its purest form.

## 4. Verdict — no candidate decision; SN's wall characterized `[honest report]`

**No separation, therefore no decision.** The margin (`snd_verdict.py`): halt (all-ones part) needs
`#zero-bits(m)=0`; along the orbit `#zero-bits(m) ≈ width/2` (e.g. gen 2000: width 1856, zero-bits 928),
i.e. bits **equidistribute**. The all-ones target recedes as `2^{−width}` — the summable, non-halt-*leaning*
picture — but this is a measure statement, **not an invariant**: the minimum zero-bit count is small only
because early generations are small; there is no structural lower bound above 0.

**Is SN's wall genuinely (K)-like, or is it different?** *Both, in a precise sense.* At the **residue level**
it is (K)-shaped: the orbit equidistributes mod every `M`, so — exactly like the Antihydra/o4 family — no
congruence invariant can decide it. But SN is **structurally harder** than the (K) sea machines, not easier.
The (K) machines are `⌊3x/2⌋`-driven with a *scalar draining ledger*; SN's odd branch has **no fixed point**
(the v-indexed carry), the counter is **cumulative** (grows ~×5/2, never resets), and `f` **mixes all bits**,
so SN has **no finite-state abstraction at all** — whereas o7's reachable-set method worked precisely because
o7's map *was* a bounded-look-ahead congruence automaton. SN, the sole non-(K)-seeded machine (5/2 ∉ 2^a/3^b),
sits on the o4/CUMULATIVE side of the memory axis: its non-halt lean is the **strongest** of the six, but the
actual content — does a genuine expanding 2-adic Collatz orbit ever enter the all-ones ∪ sporadic cylinder —
is a **real reachability that resists finite invariants**. Add the `[OPEN]` sporadic rule (a second,
independent unclassified fatal family), and a complete decision would need *two* things neither the
congruence method nor any weapon in the arsenal supplies.

**Verdict:** `[OPEN]`. The reachable-set / congruence-automaton attack is **definitively ruled out** for
Space Needle (no separating modulus; no finite-state abstraction of `f`). SN's wall is a genuine 2-adic
reachability wall, (K)-shaped at the residue level and strictly harder structurally.

## Soundness ledger
- Dynamics + halt gate `[PROVEN from table]`, re-verified 6/6 real-orbit milestones + 398/398 raw-TM epochs.
- Orbit-past-sporadics, all-ones/A_M hits, equidistribution, non-congruence counterexamples: `[OBSERVED /
  computed exact]`, big-int, 6000 gens / 5648-bit orbit.
- No margin, summability, or lean is ever a machine claim. **Machine `[OPEN]`.**

## Reproduce
`snd_dynamics.py [STEPS]` (raw-TM real orbit + f verification) · `snd_automaton.py [GENS]` (reachable-residue
vs A_M separation test + equidistribution) · `snd_verdict.py` (orbit location, non-congruence obstruction,
margin). Basis: `O16_SPACENEEDLE_FIXEDPOINT_2026-07-08.md`, `SPACE_NEEDLE_HALT.md`, `ATTACK_PLAN_2026-07-10.md`
§B2.

**No machine decided. No label upgraded.**
