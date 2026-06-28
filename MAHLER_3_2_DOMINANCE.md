# The Mahler-3/2 Dominance of the BB(6) Collatz Core — quantified

*Making the headline "the BB(6) Collatz core is essentially the single Mahler 3/2 problem" RIGOROUS and
QUANTIFIED (2026-06-29). Soundness paramount; every claim carries `[PROVEN]`/`[VERIFIED]`/`[CONDITIONAL]`/`[OPEN]`
copied from the source documents and never upgraded. No machine is decided; no non-halting is asserted. Numerics
this session use `/Users/aokiyousuke/quantum-ecc/.venv/bin/python` (exact big-ints), cross-checked against the
`bb_sim.py` semantics; the inner-map relations and orbits below were re-confirmed exactly (o11 `⌊3m/2⌋+4` 12/12;
o16 `⌊3s/2⌋+2`; o12 `⌊3a/2⌋+3δ−1`; Antihydra `c₀=8` min balance `+2`, even-density `0.4994`, induced `o₀=27`
mean `D=1.9963`).*

Sources: `SESSION_2026-06-29_CATALOGUE_CLOSED.md`, `BB6_STRUCTURAL_LIMIT_THEOREM.md`, `AEV_DIGEST.md`,
`CATALOGUE_IRREGULAR.md`, `CATALOGUE_O7_O12.md`, `CATALOGUE_O13_SN.md`, `CATALOGUE_O2_O5.md`,
`COMPLETE_PROOF_CAPSTONE.md`.

---

## 0. The count, stated honestly

The "9 machines" headline is a **pre-o2 count**. The machines carrying a `[VERIFIED]` `μ=3/2` (`p=2`) engine are
**ten** named members:

> **Antihydra, o2, o7, o8, o10-inner, o11, o12, o13, o14, o16.**

`CATALOGUE_IRREGULAR.md` lists "9 members" because it omits **o2** (which `CATALOGUE_O2_O5.md` later placed in the
`3/2` family). `BB6_STRUCTURAL_LIMIT_THEOREM.md` §7.2 counts o2 in. So the precise statement is **10 machines with
`μ=3/2` content** (or 9 if o2 is excluded). Everything below is reported for all ten; the "1 solves N" arithmetic
is given both ways.

---

## 1. Per-machine kernel table for the `μ=3/2` cluster

Shared map: `T_{3/2}(x)=⌊3x/2⌋` (floor) — **except o10-inner, which is the literal AEV ceiling `⌈3m/2⌉`**.
The **seeds differ per machine** (each is the integer/config the blank-tape orbit settles into). "Level" = the
mod-`2^k` depth the exact reduction needs; only Antihydra has a derived level (`k=2`); for the in-family machines
only the multiplier is pinned, so the level is **not derived**.

| machine | seed / characteristic orbit `[VERIFIED]` | map | facet of halt event | exact kernel statement | reduction status |
|---|---|---|---|---|---|
| **Antihydra** | integer `c₀=8` (`c→⌊3c/2⌋`); induced odd `o₀=27`, `T(o)=3^{D−1}(3o−1)/2^D`, `D=v₂(3o−1)` | floor `3/2` | **density** (Cesàro average) | `liminf_N (1/N)#{n<N: D(o_n)≥2} ≥ 1/2`  ⟺ `mean D ≥ 3/2` ⟺ even-density of `c₀=8` `≥1/3` ⟺ `liminf freq(o≡3 mod4)≥1/2`. **Level `k=2`, one-sided, single-orbit, floor-mirror.** | **`[PROVEN]` exact** (in-scope); **only `β>0` barrier holder** |
| **o10-inner** | inner mass `m → ⌈3m/2⌉` (literal AEV ceiling); inner eat-length always even | **ceiling `3/2`** | composite/existence (epoch halts when `b`-countdown hits `b=0` on odd `m`) | inner loop never halts (eat-length even); halt is a **composite** countdown coincidence, not a clean one-sided event | **`[PROVEN]` reduction but `[CONDITIONAL]`**; **o10-FULL OUT** (probabilistically halts) |
| **o2** | reset orbit `a = 5,11,65,101,155,551,1253,1883` (nested powers of `3/2`) | floor `3/2` | existence (`00`-gap at D→F sweep, `q=2`) | `(3/2)^n` two-counter orbit avoids the clopen `00`-gap alignment set forever; **exact 2-adic predicate NOT derived** | `[VERIFIED]` multiplier; **in-family, not in-scope** |
| **o7** | reset orbit `a = 6,11,16,…,316,476,716,1076` | floor `3/2` | existence (F reads 0; head-local 2-adic carry/align) | orbit avoids the F-frontier carry alignment; **predicate NOT derived** | `[VERIFIED]`; in-family, not in-scope |
| **o8** | reset orbit `a = 2,4,7,…,70,106,160,241,…` (nested meta-epochs) | floor `3/2` (nested) | existence (F reads 0) | nested `(3/2)^n` orbit avoids F-alignment; **predicate NOT derived** | `[VERIFIED]`; in-family, not in-scope |
| **o11** | inner sea `m = 2,7,14,25,…,1226`, exact `m'=⌊3m/2⌋+4` (12/12); outer refill `3,9,26,303` | floor `3/2` (nested) | density-type growth; halt = C reads 0 (boundary collision) | nested `3/2`; **outer refill doubly-exponential, not eventually periodic**; predicate NOT derived | `[VERIFIED]`; in-family, not in-scope |
| **o12** | inner `a = 44,68,104,…,9584`, `a'=⌊3a/2⌋+3δ−1` (`δ∈{1,2}`, sea-coupled); outer refill `4,10,28,370` | floor `3/2` (nested) | density-type growth; halt = F reads 0 | nested `3/2` with `δ` carry-defect; predicate NOT derived | `[VERIFIED]`; in-family, not in-scope |
| **o13** | inner `a = 40,67,104,…,4411` (ratios →3/2); outer refill `3,6,10,64` | floor `3/2` (nested) | density-type growth; halt = E reads 0 | nested `3/2`, sea-coupled; predicate NOT derived | `[VERIFIED]`; in-family, not in-scope |
| **o14** | inner `a = 3,10,21,…,2764` (ratios →3/2) + accreting `4,4,2` marker tail | floor `3/2` (nested) | density-type growth; halt = F reads 0 | nested `3/2` + marker accretion; never pure-block; predicate NOT derived | `[VERIFIED]`; in-family, not in-scope |
| **o16** | inner sea `s = 73,111,168,…,4426`, `s'=⌊3s/2⌋+2`; leading `k→k−1` countdown; doubly-exp refill | floor `3/2` (nested, T2 costume) | density-type growth; halt = F reads 0 | "o11 with step −1"; nested `3/2`, doubly-exp refill; predicate NOT derived | `[VERIFIED]`; in-family, not in-scope |

**Key reading of the table.**
- All ten share the **map** `T_{3/2}` but have **distinct seeds** → these are **ten distinct single-orbit
  instances of one map**, not one statement.
- Only **two** have an exact halt reduction to a `3/2` event: **Antihydra** (`[PROVEN]` exact, density,
  floor-mirror, with `β>0` barrier) and **o10-inner** (`[PROVEN]` reduction but `[CONDITIONAL]`/composite, and the
  *literal* AEV ceiling). The other **eight** are **in-family by multiplier, not-in-scope by proof** — their
  halt event is pinned only to a head-local "reads 0" hitting event, with the exact `2^k` predicate **NOT
  derived**.
- The **facet** of the halt event is **density only for Antihydra**. o10-inner is composite; o2/o7/o8 and the
  nested o11–o16 halts are **existence/hitting** events (a frontier `0`-adjacency / boundary collision), even
  though their *growth* is `3/2`-density-driven (hence the catalogue's "density-type growth" tag, which is about
  growth, not the halt facet).

---

## 2. Does AEV Conj 1.6 (3/2) decide all ten at once?

**AEV Conj 1.6 (3/2)** `[OPEN]` (arXiv:2510.11723): for *every* starting integer `n` and *every* `k`, the orbit
of `T_{3/2}(x)=⌈3x/2⌉` is equidistributed mod `2^k`. It is an **all-orbits, all-level** statement → a **single
resolution covers every seed simultaneously**. That is the structural reason a single conjecture can address the
whole cluster. But "AEV(3/2) ⇒ all ten decided" is **NOT a clean valid `[CONDITIONAL]` implication as stated**,
for three independent soundness reasons:

1. **Ceiling vs floor (the floor-mirror gap).** AEV's map is the **ceiling** `⌈3x/2⌉`. Antihydra and the eight
   in-family machines run the **floor** `(3c−1)/2`/`⌊3c/2⌋`; the `±1` flips parity, so they are **not literally
   AEV-conjugate** (`COMPLETE_PROOF_CAPSTONE.md` §8; `AEV_DIGEST.md` §7). What decides them is the **floor-mirror
   analog** of AEV Conj 1.6 — "the same difficulty," a recognized open problem, but a **formally distinct
   conjecture** from the literal AEV statement. (**o10-inner is the lone exception: it runs the literal AEV
   ceiling `⌈3m/2⌉`**, so the literal AEV(3/2) applies to it directly.)

2. **In-scope vs in-family (missing reduction link).** Only Antihydra and o10-inner have a derived exact halt
   criterion. For o2/o7/o8/o11/o12/o13/o14/o16 the exact `2^k` halt predicate is **`[OPEN]` (not derived)**, so
   even a proof of AEV(3/2) does not *yet* formally decide them — the reduction "halt ⟺ [specific 3/2
   equidistribution/avoidance event]" is missing. They are **decided-modulo-completing-their-reductions**.

3. **Density vs existence facet (qualitative vs effective).** Antihydra's kernel is a **one-sided density**
   bound; **qualitative** equidistribution (which AEV Conj 1.6 is) is *more than enough* — AEV(3/2) gives the
   exact limiting density `1/2 ≥ 1/3`, so it **over-implies** the kernel (Antihydra needs only the weaker
   one-sided single-level `k=2` fragment). But the **existence/hitting**-facet members (o2/o7/o8 and the nested
   halts) need the orbit to **avoid a thin (measure-zero / summable) target**, which requires **EFFECTIVE
   equidistribution with a rate beating a summable target** — a statement **stronger** than AEV Conj 1.6's
   qualitative all-`k` equidistribution (`BB6_STRUCTURAL_LIMIT_THEOREM.md` §7.1, §8; `EXISTENCE_META_THEOREM.md`).
   So qualitative AEV(3/2) is **not sufficient** for the existence-facet members even with reductions completed.

**Honest `[CONDITIONAL]` ledger for "AEV(3/2) decides the cluster":**

| machine(s) | what a resolution of AEV(3/2) gives | residual gap |
|---|---|---|
| **Antihydra** | **decided `[CONDITIONAL]`** (qualitative AEV over-implies the one-sided `k=2` density kernel; plus finite check `balance_n≥0`, `[VERIFIED]` to `n≤2·10⁵`) | floor-mirror form must be the thing resolved |
| **o10-inner** | **decided `[CONDITIONAL]`** (literal ceiling; AEV(3/2) applies directly) | composite/o10-FULL OUT; only the inner sub-orbit |
| **o2,o7,o8,o11,o12,o13,o14,o16** | **kernel input supplied, NOT decided** | (a) exact halt reduction `[OPEN]`; (b) existence members need **effective-rate** AEV, stronger than Conj 1.6 |

So the rigorous count is **"2 decided outright `[CONDITIONAL]`, 8 reduced (modulo completing reductions + an
effective-rate strengthening for the existence members)"** — not a clean "1 ⇒ 10." The *morally* correct
headline ("one named problem under the cluster") is sound; the *literal* "one conjecture decides all ten" is
**over-claimed** and is flagged here.

---

## 3. One statement, or ten distinct instances? — the precise answer

> **They are ten DISTINCT single-orbit instances of ONE map, all SUBSUMED under one all-orbits conjecture.**

- **Distinct instances:** same map `T_{3/2}` (floor; o10-inner ceiling), but **different seeds** (Antihydra
  `o₀=27`; o2 `5,11,65,…`; o7 `6,11,16,…`; o8 `2,4,7,…`; o11 sea `2,7,14,…`; o12 `44,68,…`; o13 `40,67,…`; o14
  `3,10,21,…`; o16 sea `73,111,…`). They are **not literally the same statement**.
- **One umbrella:** AEV Conj 1.6 (3/2) quantifies over **every** starting integer, so its single resolution
  addresses **all seeds at once** (subject to §2's floor-mirror / in-scope / effective-rate caveats).
- **Per-orbit results decide them one at a time:** a per-orbit Mahler-type theorem (e.g. settling only the
  `o₀=27` orbit) decides only that one machine; weaker per-orbit progress is a one-at-a-time path.

So "essentially the single Mahler 3/2 problem" is **rigorous in this exact sense**: all ten are instances of a
**single named all-orbits conjecture (AEV Conj 1.6, base 3/2)** differing only in seed; it is **not** rigorous to
call them one statement, and a single *literal* implication to "all decided" fails on the three §2 gaps.

---

## 4. The full frontier dependency map: named conjecture → machines decided

The four expanding-kernel multipliers are four **distinct base-instances of the same AEV Conj 1.6** (general
`p/q`). Each specific base is independently `[OPEN]`. Writing `μ=p/q`, AEV Thm 1.5 ties Conj 1.6 to Mahler only in
the **hard regime `p<q²`** (`3/2`,`4/3`,`8/3` hard; `5/2` easy).

| named conjecture (base) | regime | machines it would decide | count | soundness of the implication |
|---|---|---|---|---|
| **AEV Conj 1.6 `3/2`** (floor-mirror; ceiling for o10-inner) | hard `3<4` | **Antihydra, o10-inner** (decided `[CONDITIONAL]`); **o2,o7,o8,o11,o12,o13,o14,o16** (kernel-input only) | **10** (or 9 w/o o2) | 2 `[CONDITIONAL]`; 8 need exact reductions + effective-rate for existence facet |
| **AEV Conj 1.6 `8/3`** (`q=3` Erdős existence) | hard `8<9` | **o18, o15** | **2** | in-scope exact `[PROVEN]` reductions; `[CONDITIONAL]` on the q=3 **existence/Erdős** fragment (needs effective rate beating a summable target) |
| **AEV Conj 1.6 `4/3`** (`q=3` Erdős existence) | hard `4<9` | **o4, o5** | **2** | `[VERIFIED]` multiplier; in-family not in-scope; `[CONDITIONAL]` |
| **AEV Conj 1.6 `5/2`** (`q=2`, easy `p>q²`) | **easy `5>4`** | **Space Needle** | **1** | `[VERIFIED]` multiplier; existence facet, **all-orbits avoidance provably impossible** (Kaneko/Pollington: confined `Z_{5/2}` orbits EXIST; AEV Conj 1.4 requires `p<q²`) → decidable **only** by a specific-orbit result, **not** by an all-orbits conjecture |
| **(none — kernel-less odometers)** | — | **o3, o17** | **2** | no Mahler/AEV kernel; hardness = Collatz-irregular carry/halt predicate; o17 has the highest certificate floor `m*=8` `[PROVEN]`; separate problem entirely |

**Totals:** `10 + 2 + 2 + 1 + 2 = 17` frontier machines (the bbchallenge count of "19 cryptids" additionally
counts o10-FULL and split entries; the 17 named here are the analyzed frontier members).

**The "1 solves N" structure, quantified.**
- **AEV(3/2) is the dominant single conjecture: 10 of 17 (≈59%)** of the frontier hinge on it (9 of 17 if o2 is
  excluded). This is the precise content of "the BB(6) Collatz core is essentially the single Mahler 3/2 problem."
- The remaining 7 split: **AEV(8/3) → 2, AEV(4/3) → 2, AEV(5/2) → 1, kernel-less odometers → 2.**
- **Strongest unification:** since all four bases are instances of one general conjecture, **AEV Conj 1.6 proven
  in full generality would decide 15 of 17** (everything except the two odometers o3, o17) — `[CONDITIONAL]`,
  with the per-facet caveats (floor-mirror for the q=2 floor machines; effective-rate for every existence-facet
  member; completed exact reductions for the in-family machines). But each base is independently open, so
  practically the frontier is **four open base-instances + two odometers**, with **3/2 carrying the majority.**

---

## 5. Soundness summary (labels enforced, none upgraded)

- The **reductions** (raw TM → `2^a/3^b` arithmetic event) are `[PROVEN]` for the in-scope set {Antihydra, o18,
  o15, o10-inner} and `[VERIFIED]` (multiplier + halt-event, exact predicate **not** derived) for the in-family
  set {o2, o7, o8, o4, o5, o11, o12, o13, o14, o16, Space Needle}. **Not upgraded.**
- The **implications "conjecture ⇒ machines decided" are `[CONDITIONAL]`** and additionally gated by: the
  **floor-mirror** vs literal-AEV distinction (q=2 floor machines), the **in-scope vs in-family** reduction gap
  (8 of the 3/2 machines, all of 4/3, Space Needle), and **density (qualitative-sufficient) vs existence
  (effective-rate-required)** facet. Antihydra needs only the **weaker** one-sided single-level `k=2` fragment;
  the existence-facet members need the **stronger** effective-rate version.
- **The only `[PROVEN]` no-structure-only barrier in the entire family is Antihydra's density `β=+1/2>0`**
  (Bousch ergodic optimization, halting fixed point `o=1`). It does **not** transfer to the existence-facet
  members (no `β`; their barrier is the `[OPEN]` over-approximation top).
- **No machine is decided; no non-halting is asserted.** All orbits/relations re-confirmed this session with the
  `.venv` exact-bigint interpreter against `bb_sim` semantics.
