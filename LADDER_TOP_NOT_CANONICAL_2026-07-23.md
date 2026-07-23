# The ladder's TOP rung is not `cascadeReg` — a measured correction to the T7 architecture (2026-07-23)

**Summary.** `ladderToCascade` is a true, green theorem, but on the real orbit it covers
`regenIn 5 → cascadeReg (g+8)`, **not** `→ cascadeReg (g+9)` as the T7 docstring and the
design doc state. The last rung's endpoints are **not** in `regenIn`/`cascadeReg` shape:
the comb `pow01 (2^{k−1}−2)` those definitions require has been exhausted by the climb.
The uncovered stretch is ≈ 75 % of the doubling phase by step count.

No theorem is retracted. No label is upgraded. This is a scope correction, found by
measurement.

---

## 1. How it was found

Every `cascadeReg` identification made earlier in this session used the **right side only**
(`0^3 · 1^{2^k−3} · 0^2 · descCascade(k−3)`), and every `regenIn` identification used only
the leading ones-run. The Lean definitions constrain the **left** as well:

```
regenIn k p z marker R
  left = ones(2^k−3) ++ [0,1,0,0,1] ++ pow01(2^{k−1}−2) ++ marker
cascadeReg k Lc p marker R
  left = pow01(Lc + 2^{k−1}−2) ++ marker
```

Re-running the g=2 doubling phase with the **full** shape checked (`x2r4_fullshape.py`):
255 right-side hits, of which the ladder's main-path configs are

| config | step | left comb | required | verdict |
|---|---|---|---|---|
| `regenIn 5` | 739 656 | ok | 14 | **canonical** |
| `regenIn 6…10` | 740 809 … 1 133 853 | ok | 30…510 | **canonical** |
| `cascadeReg 4…10` | 739 874 … 1 270 303 | ok | 6…510 | **canonical** |
| `regenIn 11` (top) | 2 315 814 | **0** | 1022 | **NOT canonical** |
| `cascadeReg 11` (top) | 2 851 880 | **1** | 1022 | **NOT canonical** |

It is the TOP, not the level, that fails. Inside g=4's phase the *same levels* mid-ladder
are fine, and g=4's own top fails:

| config | step | left comb | required | verdict |
|---|---|---|---|---|
| `cascadeReg 10` (mid, g=4) | 11 885 391 | 511 | 510 | canonical |
| `cascadeReg 11` (mid, g=4) | 13 466 968 | 1023 | 1022 | canonical |
| `cascadeReg 13` (top, g=4) | 44 986 730 | **1** | 4094 | **NOT canonical** |

**Corroboration from the earlier session.** `x2t7_boundary.py` (2026-07-22) already printed
`k=11: FAILED to parse regenIn 11 shape at step 2315814 (instrument problem?)` and recorded
EXACT nesting matches only for k = 5…10. That was not an instrument problem — it is the
same fact. The nesting premise holds for **five** rungs (5→10) at g=2, and the sixth
rung's output is a different object.

## 2. What it costs

g=2 doubling phase, M6(2) @733 076 → M1(3) @2 852 091 = 2 119 015 steps:

| stretch | steps | covered by |
|---|---|---|
| M6(2) → `descIn 9` | 1 683 | **topEntry — no theorem** (cost known: `384·2^g+53g+384`) |
| `descIn 9` → `regenIn 5` | 4 897 | `headLaw` ✅ |
| `regenIn 5` → `cascadeReg 10` | 530 647 | `ladderToCascade` ✅ (n = 5) |
| `cascadeReg 10` → tail IN | **1 581 651** | **NOTHING — the top rung** |
| tail IN → `M1(3)` | 137 | `tailLaw` ✅ |

Proven ∀-coverage: 535 681 / 2 119 015 = **25.3 %**. The gap is a *single rung*
(1 581 577) plus the 74-step seam, and 1 581 577 is exactly the `cascadeReg 10 →
cascadeReg 11` rung cost measured independently inside g=4's phase — so it is a normal
rung dynamically; only its endpoints are outside the `regenIn`/`cascadeReg` family.

## 3. What must change

- **`T7Ladder.ladderToCascade`'s docstring** claims its OUT is "the config the tail episode
  carries into `M1(g+1)`". On the orbit it is not; the tail's IN is one rung further.
  The theorem itself is untouched — only the docstring's on-orbit claim.
- **A new object is needed: `topRung`** — the last rung, from the (canonical)
  `cascadeReg (g+8)` to the tail's IN, `Θ(4^k)` steps, whose OUT has a collapsed comb.
  It is the largest single unproven span of the doubling phase.
- The R4 assembly must be re-drawn as
  `topEntry ∘ headLaw ∘ ladderToCascade(→ g+8) ∘ topRung ∘ tailLaw`.

## 4. Honest limits

- Measured at g=2 (full phase) and at three configs inside g=4. The "canonical up to g+8,
  top not canonical" rule has two generations behind it; a scan of g=4's `cascadeReg k≥9`
  is running to pin the exact last canonical level there.
- Nothing here says `ladderToCascade` is wrong — it is green and true; the finding is about
  **where the orbit is**, not about the theorem.
- No machine decided. No label upgraded. `x2` remains `[OPEN]`.

---

# ADDENDUM (same day) — the gap reduces to ONE generalization of an already-proven theorem

## 5. `topRung` decomposed exactly

The g=2 top rung, `cascadeReg 10 @1 270 303 → cascadeReg-11-shape @2 851 880`, splits at the
intermediate config @2 315 814 into two pieces whose costs are **exactly** the library's own
closed forms:

| piece | measured | library | status |
|---|---|---|---|
| `cascadeReg 10 → (regenIn 11 with an empty comb)` | 1 045 511 | `topGrindSteps 10` = 1 045 511 | **`cascadeReg_topgrind` is ∀ marker — it ALREADY applies at the top** |
| `(regenIn 11, empty comb) → cascadeReg-11-shape` | 536 066 | `exitSteps 11` = 536 066 | needs `RegenLaw` with a free comb |
| total | 1 581 577 | | |

The intermediate config is `regenIn 11` **with the comb `pow01 1022` absent** — which is
exactly the shape `cascadeReg_topgrind`'s ∀-marker OUT produces when the marker's next
ladder layer `0 0 1 (01)^{2^k−2}` has degenerated to `0 0 1` (measured: at the ladder top the
marker's layer carries `pow01 0`).

## 6. The comb is CARRIED, never READ `[MEASURED]`

During the 536 066-step REGEN segment the head descends **exactly 2 049 cells** into the left
— the length of `ones(2^11−3) ++ [0,1,0,0,1]` — and **never enters the comb region**.

And the comb count is conserved +1: `regenIn`'s comb `pow01 a` becomes `cascadeReg`'s
`pow01 (a+1)`. Canonical: `a = 2^{k−1}−2 → 2^{k−1}−1 = 1 + (2^{k−1}−2)` ✓. At the top:
`a = 0 → 1` — and the measured top OUT comb is **1**. Exactly.

## 7. `RegenLawGen` — stated, and TRUE at five levels

```lean
def regenInGen (k) (p) (z) (T R) : Cfg :=
  ⟨.E, p, ⟨ones (2^k − 3) ++ (false::true::false::false::true:: T), false,
      false :: (descCascade (k−4) ++ (zeros z ++ R))⟩⟩
def cascadeRegGen (k) (p) (T R) : Cfg :=
  ⟨.E, p, ⟨pow01 1 ++ T, false, <cascadeReg k's right>⟩⟩

RegenLawGen k :  steps (exitSteps k) (regenInGen k p (2^{k−1}+9) T R)
                   = some (cascadeRegGen k (p − 2^k) T R)      -- ∀ T
```

`regenIn`'s fixed comb `pow01 (2^{k−1}−2) ++ marker` is replaced by a single free tail `T`.

**Verified `true` by `#eval`** at k = 4, 5, 6, 7, 8 with `T := []` (the degenerate case the
ladder top presents) and with arbitrary non-empty `T`; and the CONTROL that the existing
`RegenLaw` is exactly the instance `T := pow01 (2^{k−1}−2) ++ marker` also evaluates `true`.
So `RegenLawGen` is a strict generalization that specializes to the proven law.

## 8. The target, precisely

```
topRung k  =  cascadeReg_topgrind k   [PROVEN, ∀ marker]
            ∘ RegenLawGen (k+1)       [TRUE at 5 levels, UNPROVEN ∀k]
```

So the ~75 % of the doubling phase that has no theorem reduces to **one generalization of
`regenLaw_closed` in a single parameter** — the comb count — which the measurement says the
machine never reads. That is an `X2.lean`-scale refactor (the proof chain
`regenLaw_all_of_trailLaw_all ∘ trailLaw_all` must be re-run with the comb free), not a new
mathematical obstacle.

**Not proven. `#eval` at five levels is evidence, not a theorem.** No label is upgraded.
