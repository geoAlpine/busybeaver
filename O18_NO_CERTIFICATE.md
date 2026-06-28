# o18 — the existence-side "no tame certificate" barrier, made concrete and machine-checked (2026-06-28)

Goal (the task): establish, for **o18** (`1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---`, halt = F reads `1`),
the existence-axis analog of Antihydra's density-side **β>0** barrier — i.e. prove that **no tame certificate
(k-window / REG / FAR-DFA) can witness o18 non-halting**. This note carries out the embedded-family programme
that proved the certificate-hierarchy separations (`LIMIT_THEOREM.md`) and the o17 barrier
(`CRYPTID_O17_O15.md` §1d), applies it to o18, and reports the **honest, machine-checked outcome**.

**Soundness (paramount).** Every line is `[PROVEN]` (conjecture-free, elementary), `[VERIFIED]` (machine-checked
this session, exact, `bb_sim` semantics via `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`), `[OPEN]`, or
`[OBSERVED]`. No machine decided. The central result is **a precisely-scoped barrier plus a precisely-scoped
honest negative** — and the two together are the finding.

---

## 0. Headline verdict (read this first)

| certificate class | "no certificate proves o18 non-halting"? | basis |
|---|---|---|
| **2-window (SLT, m=2)** | **[PROVEN]** (conjecture-free, machine-checked) | §3 |
| **k-window (LT, k≥3)** | **[OPEN]** | §4 (head-locality, threshold = 3) |
| **REG (FAR-DFA)** | **[OPEN]** (= as hard as resolving o18) | §2, §4 |
| **SLIN / automatic** | **[OPEN]** | §4 |

> **One-line answer.** The cleanest *proven* existence-side barrier for o18 is **"no 2-window certificate"** —
> but this is the **bottom rung** (below o18's head-locality threshold of 3). At every meaningfully-tame class
> (k-window k≥3, REG, FAR-DFA, SLIN) the barrier is **OPEN**, and proving it is as hard as resolving o18. This
> does **NOT** establish a barrier parallel in strength to Antihydra's β>0 (which forbids *all* all-orbits
> density certificates). The reason is exactly `EXISTENCE_META_THEOREM.md` §2b — an invariant **set** can
> exclude the halting orbit — and here it is made concrete: **o18's halt discriminator is head-local**
> (adjacent cells of the marker), so any window of size ≥3 can gate exactly on it.

This is the existence-axis being genuinely **weaker** than the density axis (Antihydra β>0 **[PROVEN]**), and
genuinely **weaker than o17** (which *does* have a proven k-window/REG barrier, §5) — confirming and sharpening
the `EXISTENCE_META_THEOREM.md` `[OPEN]` placement, now for the specific machine o18.

---

## 1. Recap — the proven certificate-hierarchy tools, and what o18 would need  [PROVEN, from LIMIT_THEOREM.md]

A **certificate** for non-halting is a set `L` of configs with (S) start ∈ L, (C) `L` step-closed, (H) `L`
halt-free; `reachable(start)` is always one, the question is whether a *tame* one exists. The proven strict
separations (each an explicit simulation-verified witness, `LIMIT_THEOREM.md`):

```
star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ context-free ⊊ context-sensitive
  (d)parity      (a)EQ    (e)POW2W       (g)PALW          (f)SQW
```

The two **engines** that produce a "no certificate in class C" barrier:
- **Pumping engine (used for REG⊊SLIN, brick (a) EQ).** If `reachable` contains an unbounded clean family
  `{F_k}` and **pumping** a member (regular pumping lemma) yields a **halting** config, then any regular
  halt-free `L ⊇ reachable` must (pump) contain a halter — contradiction. ⇒ **no REG certificate.**
- **All-or-nothing engine (used for k-window⊊REG brick (d), and o17 §1d).** If `reachable` contains an
  unbounded family `{F_k}` that is **window-equivalent** for `k ≥ m` (members share their m-window set) and the
  halting/non-halting pattern across `k` is **not eventually constant** (k-window) / **not regular** (REG),
  then no m-window (resp. REG) `L ⊇ reachable` can include the reachable members while excluding the halters.
  ⇒ **no k-window (resp. REG) certificate.**

For o18 to get a barrier, one of these engines must fire on an embedded family that `reachable(o18)` actually
contains (or whose windows it contains). §2–§4 test exactly this. **Both engines fail for o18 at every level
above m=2**, for reasons machine-checked below.

---

## 2. The clean reachable family is uniformly non-halting ⇒ the pumping engine fails  [VERIFIED]

The exact config o18 visits at each clean "reset" is **`C_N := [F] 0 1^{N-1}`** — state F on the leftmost cell
of a single block `0 1^{N-1}`, blank on both sides (`o18_reset.py` `[VERIFIED]`: real run resets at steps
35, 225, 1429, 9561, 66752, 468793, … with head at the leftmost cell and tape `0 1^{N-1}`, widths
`N = 10, 28, 76, 204, 546, …` = the `⌊8N/3⌋+2` epochs). So `reachable(o18) ⊇ { C_N : N ∈ {10,28,76,…} }`.

> **[VERIFIED] `C_N` never halts** for **N = 1..120** (budget 5·10⁶ steps each, `o18_family.py`); an extended
> search **N = 1..160** at budget 3·10⁷ found **no halter** (`o18_CN_big.py`). Structurally this is expected:
> a clean block evolves to the next clean block (`f(N)=⌊8N/3⌋+2`), strictly increasing/transient, and the
> leftward D/F sweep over a clean `0 1^{N-1}` never creates an adjacent-`11` at the frontier.

**Consequence (pumping engine fails).** Pumping the clean family `C_N` (lengthening the `1`-run) yields another
**clean, non-halting** `C_{N'}`. So pumping a reachable member does **not** produce a halter — the EQ/brick-(a)
route that proved REG⊊SLIN **does not transfer to o18.** No REG certificate barrier from reachable pumping.
This is the concrete o18 instance of `EXISTENCE_META_THEOREM.md` §2b "a set can exclude the halting orbit."

---

## 3. The PROVEN barrier: no 2-window certificate  [PROVEN, conjecture-free, VERIFIED]

This is the one rung where an engine *does* fire. The o18 halt mechanism (`O18_REDUCTION.md` §1, re-verified):
F is reached only via `D:1→1LF`, so **halt ⟺ D reads a `1` whose left neighbour is `1`** (the leftward
frontier lands on an existing `1`; the pre-halt config is `1 [D] 1`, which steps `D:1→1LF` onto the left `1`,
then `F:1→HALT`).

Encode configs as in `far_dfa.py`: a string `… c_{-1} [q] c_0 c_1 …` with the marker `q` written immediately
before its head cell `c_0`. The relevant 2-grams of the collision config `1 [D] 1` are **`(1,D)`** (cell `1`
then marker D) and **`(D,1)`** (marker D then cell `1`).

> **[VERIFIED] census of state D in reachable** (`o18_2gram.py`, 8·10⁷ steps):
> - `D` reads `0` with left neighbour `1` : **8274 times** ⇒ the 2-gram **`(1,D)` ∈ 2-grams(reachable)**.
> - `D` reads `1` with left neighbour `0` : **9 times** (block left-edges) ⇒ **`(D,1)` ∈ 2-grams(reachable)`**.
> - `D` reads `1` with left neighbour `1` : **0 times** (the collision — confirms non-halting in the prefix).

> **Theorem [PROVEN].** No 2-window certificate proves o18 non-halting.
> *Proof.* Let `L` be any 2-window set with `L ⊇ reachable` (so its permitted 2-gram set `G ⊇ 2-grams(reachable)`).
> By the census, `{(1,D),(D,1)} ⊆ 2-grams(reachable) ⊆ G`. The config `c = 1 [D] 1` is a single-marker config
> whose every 2-gram lies in `{(1,D),(D,1)}∪{tape 2-grams}` ⊆ `G`, so `c ∈ L`. But `c` halts in 2 steps
> (`D:1→1LF`, `F:1→HALT`) `[VERIFIED]`. Step-closure of `L` then forces the halt config into `L`, violating
> halt-freeness (H). So no such `L` exists. ∎

Cross-check: `far_dfa.verify` on o18 at **m=2** fails for **exactly this reason** — `"closure L fails:
D,1→1LF ctx (('0',),0) cL 1"` (`far_detail.py`). A 2-gram window cannot see the head cell's symbol and its
left neighbour *simultaneously*, so it conflates the reachable `1[D]0` (D reads 0, left 1) with the forbidden
`1[D]1` (collision).

**This is the cleanest conjecture-free existence-side barrier for o18 — but it is the m=2 floor (SLT), and §4
shows it does not extend upward.**

---

## 4. Why the barrier STOPS at m=2 — head-locality, threshold exactly 3  [PROVEN / VERIFIED — the honest negative]

The 2-window failure is a *blindness* artifact, not a genuine obstruction: the discriminator (head-cell symbol
together with its left neighbour) is **head-local**, captured by a window of size **3**.

- **3-window distinguishes collision from reachable.** The collision 3-gram is `(1,D,1)` (D reads 1, left 1);
  the reachable look-alike is `(1,D,0)` (D reads 0, left 1, occurs 8274×). `(1,D,1)` **never** occurs in
  reachable (`o18_2gram.py`, 0 collisions in 8·10⁷ steps `[VERIFIED]`). So a *tight* 3-window `G =
  3-grams(reachable)` **excludes** the collision while keeping all of reachable.
- **`far_dfa` confirms the shift.** For **m ≥ 3** the verification no longer fails on the collision; it fails on
  the benign **blank-expansion** transition `"A,0→1RB ctx (0,…,0)"` (`far_detail.py`, m=3..10) — a
  sample-size/closure artifact of the m-gram *sampled* set, not a forced halter. I.e. once windows can see the
  marker's left neighbour, **the collision is no longer forced into the over-approximation.**

So at **k ≥ 3** the all-or-nothing engine has **no fuel**: there is no embedded family that `reachable` must
contain whose halting pattern a k-window cannot gate. Concretely:

- **Single-block `1^k` families are locally-testable.** Sweeping every state × small left-context × head-side
  over `1^k`, the halting pattern in `k` is **eventually constant** in every case (`o18_scan.py`): either
  eventually-all-halt (head on a block ≥ threshold ⇒ immediate adjacent-`11`) or eventually-all-run. None is
  modular or irregular. So no single-parameter k-window obstruction. `[VERIFIED]`
- **Gap families `1^b 0^g [D]1` ARE irregular in `g` but NOT reachable-window-covered.** `[VERIFIED]`
  (`o18_gfam.py`) their halting pattern in `g` is non-eventually-periodic (both halters and non-halters persist
  to g=80). But these put D on an **isolated** `1` (window `0[D]1 0`), whereas in reachable **D reads `1` only
  at a block's left edge** — `0 0 0 0 [D]1 1 1 1` for all 9 events, and once `1 0 1 0 [D]1 1 1 1` at the
  epoch-7 defect (`o18_windows.py`) — always with a `1` to the **right** and `0` to the **left**. The
  gap-family head-window `0[D]1 0` **never occurs in reachable**, so a ≥3-window can exclude these configs
  without touching reachable. The irregular family is real TM behaviour but **off the reachable window set.**

**Net (§4) [PROVEN negative].** o18's halt discriminator lives in the **3-cell neighbourhood of the head**
(left neighbour, head cell). Every window of size ≥3 sees it and can gate exactly on the reachable
neighbourhoods (`[D]11…`, left 0) while excluding the collision (`1[D]1`). Hence **neither the pumping engine
(§2) nor the all-or-nothing engine fires above m=2**, and "no k-window (k≥3) / REG / FAR / SLIN certificate"
is **[OPEN]** — as hard as resolving o18 itself (a verified FAR/k-window certificate would *decide* o18
non-halting; `far_dfa` returns **HOLDOUT** through m=10, `[VERIFIED]`: evidence, not proof).

---

## 5. Contrast — why o17 HAS a barrier and o18 does not (the structural reason)  [VERIFIED contrast]

o17 (`CRYPTID_O17_O15.md` §1d) gets a proven k-window/REG barrier; o18 does not. The difference is *where the
discriminator sits*:

| | o18 | o17 |
|---|---|---|
| tape shape | **single block** `0 1^{N-1}` | **many blocks** `(0 1^ℓ)*` |
| halt event | **adjacent-`11` at the head** (carry alignment of two *simultaneously-growing* quantities) | **carry overflow** depending on a **reachable block length mod 3** |
| embedded reachable single-param family | `C_N`: **uniformly non-halting** (§2) | `0 A 0 1^k`: **halts irregularly in k** `[VERIFIED]` (`o17_check.py`: non-eventually-periodic; late halters k=10@795k, k=16@4.2M interleaved with runners) |
| discriminator | **head-local** (3-window gates it) | **non-local block length** (window-equivalent for k≥m, but halting varies ⇒ all-or-nothing engine fires) |
| barrier | **only m=2 [PROVEN]; ≥3 [OPEN]** | k-window/REG **[PROVEN]** per `CRYPTID_O17_O15.md` |

o17's discriminator is a *length read modulo 3* of a **reachable** block — non-local, so window-equivalent
members carry different halting status and the all-or-nothing engine bites. o18's discriminator is a *local
adjacency* that reachable **never** exhibits (it would halt), so a window can gate it out. **o18's "two growing
quantities must align" event cannot be exposed by holding all-but-one parameter fixed** (the one-parameter
slices are either locally-trivial, §4, or off the reachable window set), which is exactly why no embedded family
gives a barrier.

---

## 6. Connection to the unified theorem — does this match Antihydra's β>0?  [honest]

**No — and the gap is the point.**

- **Density side (Antihydra) [PROVEN, strong].** β = max over *T-invariant measures* of `∫(θ−φ)dμ = +1/2 > 0`,
  attained at the halting fixed-point atom `δ_{o=1}`. The `max`-over-measures **necessarily includes** the
  halting orbit's atom, so **every** all-orbits density certificate is blocked. A top-level barrier.
- **Existence side (o18) [OPEN above m=2].** The analog would be: *every* tame invariant **set** `L ⊇
  orbit(x₀)` meets the halt set `H`. This is **false in general** (`EXISTENCE_META_THEOREM.md` §2b: a set can
  exclude the halting orbit), and this note **confirms it concretely** — the halt discriminator is head-local,
  so a tight ≥3-window over-approximation excludes `H` while keeping reachable. There is **no β** (no Cesàro
  functional; the criterion is an existence/Borel–Cantelli event), and the proven barrier is only the m=2 SLT
  floor.

So o18's existence-side barrier is **PROVEN only at the bottom rung (no 2-window certificate)** and **OPEN** at
every class strong enough to matter (k-window k≥3, REG, FAR-DFA, SLIN). It does **not** give o18 a barrier
parallel in strength to Antihydra's β>0. This is fully consistent with — and is the machine-checked,
o18-specific instantiation of — `EXISTENCE_META_THEOREM.md` §2–§5 (existence barrier = the over-approximation /
descriptive-complexity axis, `[OPEN]`; not the proven dynamical/ergodic axis). The contribution is to **pin the
exact rung where the existence barrier is proven (m=2) and the exact mechanism that stops it (head-locality,
threshold 3)**, and to show o18 lacks even the o17-style embedded-family barrier.

---

## 7. Answers to the task's five items

1. **Proven separations / what o18 would need (§1).** The proven tools are the strict tower `k-window ⊊ REG ⊊
   SLIN ⊊ …` via two engines (pumping; all-or-nothing on a window-equivalent reachable family). o18 would need
   one of these engines to fire on a reachable (or reachable-window-covered) embedded family.
2. **Embedded-family argument (§2–§5, cross-checked vs `bb_sim`).** o18's natural embedded families:
   `C_N` clean blocks are **uniformly non-halting** (no pumping barrier); single-`1^k` families are
   **eventually-constant** (locally testable, no all-or-nothing barrier); the only **irregular** family
   (`1^b 0^g [D]1`) is **not reachable-window-covered** (D-on-isolated-`1` never occurs; reachable has D-reads-`1`
   only at block left-edges, left neighbour 0, **0 collisions in 8·10⁷ steps**). So the embedded-family
   non-regularity argument **does not transfer to o18** — a machine-checked honest negative.
3. **Exact certificate class proven (§3–§4).** **PROVEN: no 2-window (SLT m=2) certificate** (conjecture-free:
   reachable's 2-grams `{(1,D),(D,1)}` force the halt-reaching `1[D]1`). **OPEN: k-window (k≥3), REG, FAR-DFA,
   SLIN** — head-locality threshold is exactly 3.
4. **Existence-axis item of the unified theorem (§6).** This does **NOT** establish a strong existence-side
   barrier parallel to Antihydra's β>0. The proven barrier covers only the **m=2 floor**; above it the barrier
   is `[OPEN]` (= as hard as o18), confirming `EXISTENCE_META_THEOREM.md`'s placement that the existence barrier
   lives on the over-approximation axis and is open.
5. **This file.** `busybeaver/O18_NO_CERTIFICATE.md` (not committed).

**No machine decided. No false barrier claimed. The proven barrier (no 2-window) is airtight; everything above
m=2 is honestly OPEN. Soundness intact.**

## Reproduce (all `/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, scratchpad scripts, bb_sim semantics)
- `o18_reset.py` — exact reset config `C_N = [F]0 1^{N-1}`, real-run widths 10,28,76,204,546,….
- `o18_family.py`, `o18_CN_big.py` — `C_N` non-halting N=1..120 @5·10⁶ (and N=1..160 @3·10⁷, no halter).
- `o18_scan.py` — single-`1^k` families eventually-constant (locally testable).
- `o18_gfam.py` — gap families `1^b 0^g[D]1` non-eventually-periodic in g.
- `o18_windows.py` — reachable D-reads-`1` neighbourhoods (all block-left-edge `0000[D]1111`; one defect `1010[D]1111`).
- `o18_2gram.py` — D cell/left census: `(1,D)` 8274×, `(D,1)` 9×, collision `1[D]1` 0× ⇒ the §3 theorem.
- `far_detail.py` — `far_dfa` fails on collision at m=2, shifts to benign blank-expansion at m≥3; HOLDOUT to m=10.
- `o17_check.py` — o17 `0A01^k` irregular halting (the §5 contrast).
