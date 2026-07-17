# The framing glue of REGEN(k) — `lead` / `trailing`, ∀k

**Task:** ROADMAP_2026-07-17 §1.3.2. Supply the `∀k` closed form for the framing glue, or
establish that none exists.

**Verdict: THERE IS A LAW.** `trailing` is **derived** (a word identity, no free parameters).
`lead` is **derived up to two measured constants** (a word identity fixing its recursion's
*shape*; the base value 154 and the per-level `−9` are `[OBSERVED]`).

**Nothing here is `[PROVEN]`.** Every statement below is `[OBSERVED]` at k=6..11 by transport.
No machine decided. No label upgraded.

---

## 1. The transport-verified table

`lead(k)` := steps from REGEN(k)'s window start to the **first** recursive sub-call.
`trailing(k)` := steps from the **end of the last** recursive sub-call to the window end.

| k | lead | trailing | exitSteps k | arity | calls |
|---|------|----------|-------------|-------|-------|
| 6 | 154 | 498 | 722 | 1 | `[4]` |
| 7 | 241 | 627 | 2530 | 3 | `[4,5,4]` |
| 8 | 424 | 884 | 9282 | 6 | `[4,5,6,4,5,4]` |
| 9 | 799 | 1397 | 35202 | 10 | `[4,5,6,7,4,5,6,4,5,4]` |
| 10 | 1558 | 2422 | 136450 | 15 | `[4,5,6,7,8,4,5,6,7,4,5,6,4,5,4]` |
| 11 | 3085 | 4471 | 536066 | 21 | `[4,5,6,7,8,9,4,5,6,7,8,4,5,6,7,4,5,6,4,5,4]` |

Probe: `x2fg_frame.py`. **Six transport-verified levels, up from two.**

Method compliance (each point was a stated non-negotiable):
- **By transport, never by length.** Sub-calls are TI classes: all occurrences of the exact
  `(st,h)` transport word. At k=7 the probe again rejects **4 of 8** length-candidates as false
  positives; at k=10 it measures arity **15**, not length's 16 — `exitArity 10 = 15` survives.
- **Word-identity == trace-identity, exactly.** Re-verified in `[0]`: every `(state,bit) →
  (write,move,next)` is total, so the word determines the whole `(state,head,Δpos)` trace.
- **Canonicity from the definition.** The k=4,5 reference windows are *asserted* equal to the
  ones Lean grounds (`carry_exit_j3 @ [6638,6708]`, `carry_exit_j4 @ [6923,7141]`); the probe
  aborts otherwise.
- **Tape extent from the tape.** All excursions are `min`/`max` of the actual head positions.
- Every level's decomposition sums to `exitSteps k` exactly.

**Cross-checks passed:**
- k=6 → 154/498 and k=7 → 241/627 reproduce the green `regen6_factored` / `regen7_factored`.
  (Asserted in-probe.)
- **k=8's `glueSegs`-table 424/884 is CONFIRMED by transport.** Given that §5z's
  `83/47/113/122/76` parse also produced the bogus `881`, this was not safe to inherit — it is
  now tested. (The `881` artifact does not touch the framing glue: it sits in the *inter*-element
  region, between sub-calls.)

---

## 2. `trailing` — DERIVED. Zero free parameters.

Claim **(T)**, tested as a word identity (`x2fg_geom.py` §2):

> The last `trailing(k)` steps of REGEN(k) are a **k-independent 359-step word**, followed by
> the single k-dependent closing block `TERM(k)`.

Both halves hold at **every** level k=6..11:
- (a) the 359-step tail word is byte-identical across all six levels — `True` at each;
- (b) the remainder is exactly a `TERM(k)` anchor window, at `[b−termSteps k, b]`, at each.

Therefore
```
trailing(k) = 359 + termSteps(k) = 359 + 2^(k+1) + k + 5 = 2^(k+1) + k + 364
```
The `2`, the `1`, and the `364` are **forced**, not fitted. The `2^(k+1)` is `termSteps(k)`'s
own — the closing block's sweep of `1^(2^k−3)`. The k-independent 359 = `113+24+122+24+76`
(the two 24s are `termSteps 3`), which is why the greedy parse got this one right.

An independent 3-parameter fit on k=6,7,8 returns `A,B,C = 2, 1, 364` — **identical** to the
derived coefficients. The fit is redundant here; the derivation stands alone.

---

## 3. `lead` — the NESTING LAW. Derived shape, two measured constants.

The interesting result. `x2fg_geom.py` §3(b) shows the common suffix of consecutive lead words
is `154, 241, 424, 799, 1558` — i.e. **exactly `lead(k)`**. Tested directly as claim **(L)**:

> `leadword(k+1) = P_(k+1) ++ leadword(k)` **exactly** — level k's *entire* lead is a literal
> suffix of level k+1's — with `|P_(k+1)| = 3·2^(k−1) − 9`.

| transition | `leadword(k+1)`.endswith(`leadword(k)`) | \|P\| | `3·2^(k−1)−9` |
|---|---|---|---|
| 6→7 | True | 87 | 87 |
| 7→8 | True | 183 | 183 |
| 8→9 | True | 375 | 375 |
| 9→10 | True | 759 | 759 |
| 10→11 | True | 1527 | 1527 |

**All five transitions hold as word identities.** So the lead is not an opaque number that
happens to fit a curve — it is a **strictly nested word**: each level prepends exactly one new
block and copies its predecessor's lead verbatim. That gives the recursion

```
lead(6) = 154 ;   lead(k+1) = lead(k) + 3·2^(k-1) − 9
```

whose closed-form solution is `lead(k) = 3·2^(k−1) − 9k + 112`.

**Geometry** (`x2fg_geom.py` §3(d), excursions derived from the move trace):
`lead/2^k = 2.406, 1.883, 1.656, 1.561, 1.521, 1.506` → **1.5** monotonically, and the head
excursion is `(0, 2^k−4)` at every level (33, 64, 127, 254, 509, 1020). The `3·2^(k−1)` is
**one-and-a-half sweeps of the `1^(2^k−3)` block** — the exit sweeps right across the block and
back half way. That is the derivation of the leading term.

**Honestly not derived:** the base constant `lead(6) = 154` and the per-level `−9`. Both are
`[OBSERVED]` — measured, stable across six levels, but not forced by any argument I have. I
looked for a link between the `−9` and `descentSteps(k) = 2^(2k) − 9k + 110`'s `−9k`; the
numerical coincidence is real but I could not verify a mechanism, so **I am not claiming one**.

---

## 4. Discipline: points, parameters, out-of-sample

Stated explicitly because this program has been burned by exactly this (§5o).

| | data points | free parameters | out-of-sample |
|---|---|---|---|
| `trailing` | 6 (k=6..11) | **0** (derived) | n/a — no extrapolation |
| `lead` closed form | 6 (k=6..11) | 3 (`A·2^k + Bk + C`) | k=9,10,11 |
| `lead` nesting law (L) | 5 transitions | **0** (word identity) | n/a |

The 3-parameter fit was determined on **k=6,7,8 only** and predicts:

| k | lead pred | lead meas | trail pred | trail meas | |
|---|---|---|---|---|---|
| 9 | 799 | 799 | 1397 | 1397 | EXACT |
| 10 | 1558 | 1558 | 2422 | 2422 | EXACT |
| 11 | **3085** | 3085 | **4471** | 4471 | EXACT — predicted before measuring |

**Protocol note, stated exactly as it happened.** These are not equal evidence. k=9,10 were
already measured when I chose the ansatz — the *parameters* never saw them, but the *ansatz*
did, so discount them. k=11 was genuinely unseen: 3085/4471 were written into `x2fg_law.py`
before the k=11 output was read. The k=11 run had been launched in the background beforehand;
its output was not read until after. That is not a git-sealed prediction, and I am not dressing
it up as one.

**But the fit is not the load-bearing evidence.** §2 and §3 are word identities holding at every
level, requiring no extrapolation at all. A 3-parameter fit on 3 points has zero explanatory
content by itself; what makes this credible is that (T) and (L) are *structural*.

---

## 5. The law, in the form Lean will take it

For the sibling proving `FramingGlueLaw → ∀k, RegenLaw k`:

```lean
def leadSteps : Nat → Nat
  | 6     => 154
  | (k+1) => leadSteps k + 3 * 2^(k-1) - 9      -- intended for k ≥ 6
  | _     => 0

def trailSteps (k : Nat) : Nat := 359 + termSteps k

theorem leadSteps_closed (k : Nat) (h : 6 ≤ k) :
    leadSteps k = 3 * 2^(k-1) - 9*k + 112

theorem trailSteps_closed (k : Nat) :
    trailSteps k = 2^(k+1) + k + 364

theorem framingGlue (k : Nat) (h : 6 ≤ k) :
    exitSteps k = leadSteps k + interSteps k + trailSteps k
```

**Two consumption notes, both load-bearing:**

1. **`trailSteps` is the one to lean on.** It is `359 + termSteps k` *by construction* — the
   359-step word is literally k-independent, so its transport lemma should be a single
   `∀ L R`-parametric primitive instantiated at every k, with `TERM(k)` composed after. No
   induction needed.

2. **`leadSteps`'s recursion is the honest shape** — prefer it to the closed form. The nesting
   law (L) says level k+1's lead *contains level k's lead verbatim as a suffix*, so the natural
   Lean proof is: prove the `P_(k+1)` block transport `∀k` once, then `leadSteps` follows by
   induction with `steps_pos_shift`, reusing level k's proof term exactly as `regen7_factored`
   reuses `regen6_factored`'s. Beware `Nat` truncated subtraction in `3 * 2^(k-1) - 9`: for
   k ≥ 6 the term is ≥ 87 so it never truncates, but the `k-1` and the `-9` both want
   `6 ≤ k` in scope.

---

## 6. Verdict

**There is a `∀k` framing-glue law.**

- `trailing(k) = 2^(k+1) + k + 364` — **derived**, zero free parameters, a word identity at
  k=6..11.
- `lead(k) = 3·2^(k−1) − 9k + 112` — **derived in shape** (the nesting law (L), a word identity
  at all five transitions k=6..11) with two `[OBSERVED]` constants: base 154, per-level `−9`.
  Its leading `3·2^(k−1)` is derived from tape geometry (1.5 sweeps of `1^(2^k−3)`).

The framing glue is **not** the obstruction. It is the mildest piece of `h_doub`'s
decomposition — it does not re-enter the recursion, it does not grow in arity, and the trailing
half needs no induction whatever. §1.3.2 can be moved off the critical path; **`RegenLaw ∀k`
(§1.3.3) remains the object**, and nothing here touches it.

Caveat I will not soften: six levels is six levels. (L) and (T) are exact where tested and have
the right *kind* of evidence (structural identity, not curve-fitting), but "holds at k=6..11"
is not "holds ∀k". This document upgrades no label.

---

**Probes:** `x2fg_frame.py` (transport table), `x2fg_law.py` (fit, parameter count,
out-of-sample, Lean form), `x2fg_geom.py` (the (T) and (L) word identities, the geometry).

Reproduce:
```
python x2fg_frame.py 2400000 11
python x2fg_geom.py  2400000 11
python x2fg_law.py
```

**No machine decided. No label upgraded.**
