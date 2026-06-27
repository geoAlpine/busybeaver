# Wall (B), EFFECTIVE finite-certification angle (2026-06-28)

Angle: a SPECIFIC computable point is special — unlike an a.e. statement it *might* admit an
**effective criterion**: a finite computation + an effective tail / self-improvement bound that
certifies the asymptotic. Does the Antihydra orbit admit one, or does every such bound secretly
require equidistribution (= the recurring wall (B) = line (5) of `PROOF_STATUS.md`)?

Verdict (all labelled, 0 false proofs):
1. The "1/6 effective tail" in the reduction is **a HYPOTHESIS of a proven implication, NOT a proven
   bound.** No unconditional effective bound on `|even-density − 1/2|` exists — not even a `liminf ≥ 1/3`
   frequency floor.
2. **No genuine self-improving discrepancy bound exists; any such bound IS the effective-equidistribution
   theorem (§3.6 object).** The standard bootstrap mechanisms that certify special points are **provably
   absent** here — same facts that kill the "regular certificate" route.
3. **FLP's `1/3` is a SUPPORT bound on the WRONG axis; it does NOT power any effective tail.** The
   `1/3 ↔ 1/3` coincidence is numerology (both from the `3` in `×3`) across support vs frequency. The
   gap is of **KIND**, not the size `1/3 → 1/2`.

---

## 1. What the proven "1/6 effective tail" actually certifies — [clarified, soundness]

`PROOF_STATUS.md` §0 / §3.8(1) states non-halt ⟸ "[finite check] `balance_n ≥ 0` for `n ≤ N₀` **plus**
[effective tail] `|E_n/n − 1/2| < 1/6` for all `n > N₀`."

Pulling this apart, exactly two things are **[PROVEN]**:
- **(i) the finite check** — `balance_n ≥ 0` for `n ≤ N₀`, a finite computation (bbchallenge, large `N₀`); and
- **(ii) the algebraic implication** — `balance_n = n(3·E_n/n − 1) ≥ n(1/2 − 3|E_n/n − 1/2|)`, so the
  bound `|E_n/n − 1/2| < 1/6` *implies* `balance_n > 0`. This is elementary algebra, unconditional.

What is **[OPEN]** is the bound `|E_n/n − 1/2| < 1/6` itself. It is the **hypothesis** of the implication
(ii), not a theorem. So:
> **The "1/6 effective tail" certifies nothing on its own. It is a clean restatement of the target
> (with a generous `1/6` slack), not a proven effective bound.** There is currently **no unconditional
> effective bound on `|even-density − 1/2|` at all** — not the conjectured `→ 0`, not the weaker one-sided
> `liminf ≥ 1/3` (`PROOF_STATUS` §3: "even that has no proof").

The **only** unconditional effective equidistribution proven for the orbit is `EFFECTIVE_TOPDIGIT.md`:
the **top `Θ(log N)` binary digits** of `c_n` equidistribute with discrepancy `≪ 1/N` at CF convergents
of `log₂3` (Weyl + finite irrationality measure). The parity / even-density bit is the **middle digit**
`bit_n(8·3ⁿ)` (position `n` of `≈1.585 n`), `Θ(n)` away from both the top and bottom footholds. **The
proven effective control never reaches the bit the tail bound needs.** So the "effective-tail structure
already in the reduction" is the *logical reduction to* an effective bound, not an effective bound.

## 2. Is there a SELF-IMPROVING / bootstrapping effective discrepancy bound? — [OPEN; reduces to (5)]

Target shape: "if `D_N ≤ f(N)` for `N ≤ N₀` (finite check), then `D_N ≤ g(N)` for all `N`, with `g → 0`."
This is how special points are sometimes certified (vs a.e.). Two findings, one structural, one numeric.

### 2a. The structural reason a bootstrap reduces to equidistribution — [PROVEN: mechanisms absent]
A finite check propagates to all `N` for a **specific** point only through some **self-similar /
finite-memory** structure that lets the head certify the tail. Every known such mechanism is **provably
absent** for this orbit (all already proven elsewhere in the kernel):
- **Finite-state / automatic structure** — absent: parity subword complexity `p(k) = 2^k` (full,
  verified to `k=14`) and **maximal linear complexity** (`EFFECTIVE_TOPDIGIT.md`, `digit_complexity.py`).
  A full-complexity sequence has no finite-automaton description to propagate a finite check.
- **Sofic / Markov coding** — absent: `3/2` is **non-Pisot**, so the base-`3/2` (β-)shift is **not even
  sofic** (Frougny: finite-state digit automaton ⟺ Pisot; `WALL_B_SPECIFIC_LITERATURE.md`). No finite
  Markov partition whose finite head-statistics close the tail.
- **Finite cyclic-group reduction** — absent: this is the exact mechanism that makes Bailey–Crandall
  Stoneham normality *unconditional* (`b^{cᵐ}α` collapses into `(ℤ/cⁿℤ)*`). For `b = 3/2`, `bᵏ mod cⁿ`
  is meaningless / there is no finite-group reduction (`T_n` not an `S`-unit; `PROOF_STATUS` §2,
  `WALL_B_SPECIFIC_LITERATURE.md` B3).

> **[PROVEN, this repo] The three mechanisms by which a finite check bootstraps to all-`N` for a specific
> point — automatic, sofic, finite-group — are each provably unavailable for this orbit.** Therefore a
> self-improving bound, if one existed, could NOT come from any of them; it would have to be an
> *unconditional effective single-orbit equidistribution theorem* — i.e. the §3.6 object itself. The
> bootstrap does not shortcut the wall; **it is the wall.** This is the **same** obstruction as
> bbchallenge's "no regular certificate", seen from the effective-bootstrap side: full complexity / non-
> sofic kills both the *decider* certificate and the *analytic* self-improvement.

This does **not** prove "no self-improvement of any conceivable kind can exist" (that would be a meta-
impossibility we do not claim). It proves the **standard** bootstrap mechanisms are ruled out, so any
self-improvement must inject genuinely new effective equidistribution — exactly line (5).

### 2b. Numeric confirmation — [OBSERVED] no contraction; head gives no leverage on tail
`wallb_effective.py` (exact integer arithmetic for `θ_n = {4(3/2)ⁿ} = (8·3ⁿ mod 2^{n+1})/2^{n+1}`, to
`N = 131072`):
- **Star-discrepancy** `D*_N` of `θ_n`: log-log slope `≈ −0.35`; `|F_N − 1/2|` (upper-half frequency):
  slope `≈ −0.18`, with the `·√N`-normalized value **wandering 0.06 → 1.0** (noisy CLT-band, not a clean
  rate). Both **match a random iid control** in magnitude at every `N` (no anomaly, no super-generic decay).
- **Self-improvement ratio** `R(N) = D*_N / D*_{N/2}`: pure equidistribution (`D ~ N^{-1/2}`) predicts
  `R → 2^{-1/2} = 0.7071` **constant**; a genuine bootstrap predicts `R < 0.707` and **decreasing**.
  Measured `R(N)` wanders `0.47, 0.65, 0.51, 1.31, 0.72, 1.09, 0.97` — **no downward/contraction trend
  (it exceeds 1 repeatedly).** No self-improvement.
- **Head-certifies-tail**: the disjoint tail window `[N/2, N)` star-discrepancy, normalized by `√(window)`,
  is **stationary-to-growing** (mean `0.94`, no shrink as the head lengthens); `corr(head_norm, tail_norm)
  ≈ +0.33` over 7 points (small-sample noise, no real signal). **The verified history carries no
  leverage on the tail's discrepancy constant** — the tail is certified only by equidistribution itself.

> **Conclusion (2):** the orbit's discrepancy just **tracks the generic equidistribution rate**; there is
> **no measured contraction and no head→tail leverage.** Combined with 2a, a self-improving effective
> bound **does not exist short of, and is equivalent to, line (5)** (Haar-genericity of the orbit =
> single-orbit equidistribution mod `2ᵏ`). The "specific point might be special" hope is **falsified for
> the standard bootstrap routes** and reduces to the open wall otherwise.

## 3. FLP's `1/3`: NOT the effective ceiling; the `1/3 → 1/2` framing is wrong-axis — [PROVEN/clarified]
The prompt's premise — "FLP's `1/3` powers the proven effective tail, and the `1/3 → 1/2` gap is wall (B)"
— is **incorrect**, and the correction is itself the sharp statement:
- **Flatto–Lagarias–Pollington (1995)** gives, unconditionally, `limsup_n {ξ(3/2)ⁿ} − liminf_n {ξ(3/2)ⁿ}
  ≥ 1/3` — a **SUPPORT / spread** bound (where the orbit goes), **not a frequency / density** bound (how
  often it is even). `flp_margin.py`: the orbit's measured spread is `≈ 1.0` (near full circle), FLP
  satisfied with enormous margin, while the *frequency* (the actual constraint) is the open quantity.
- The two `1/3`s — FLP's spread floor and the non-halt threshold `even-density ≥ 1/3` — are the **same
  number on different axes**, both arising from the `3` in `×3`. It is **numerology, not a powering
  relation**: FLP's support bound implies **nothing** about the frequency (an orbit can span the whole
  circle yet visit the even half a vanishing fraction of the time). `flp_lead.py` confirms the annealed
  decay rate `→ log 2` **iff** `θ_j` equidistributes — so even the annealed product is Mahler-class, not
  FLP-provable.

> **So FLP's `1/3` is the ceiling of the *support* method, not the *effective-density* ceiling.** There is
> **no proven effective density floor at all** (not `1/2`, not `1/3`). The real picture:
> - **proven effective:** top `Θ(log N)` digits (Weyl/`log₂3` CF) **+** support spread `≥ 1/3` (FLP) —
>   two different correct axes, both insufficient;
> - **needed:** effective **frequency** control of the middle digit = **wall (B)** = named-point
>   equidistribution of `{4(3/2)ⁿ}`, which (`WALL_B_WHICH_PART.md`) is incarnate in the explicit half
>   `a_n = bit_n(8·3ⁿ)`, with no self-reference.
>
> The gap is therefore **of kind (support/Θ(log N)-digit → frequency/middle-digit), not the size
> `1/3 → 1/2`.** Wall (B) is precisely the absence of an effective frequency bound for the middle digit;
> FLP's `1/3` sits on the support axis and never crosses to it.

## 4. Numerics (`wallb_effective.py`, exact arithmetic, `N ≤ 131072`)
| quantity | result | generic expectation | reading |
|---|---|---|---|
| `D*_N` of `{4(3/2)ⁿ}` log-log slope | `−0.35` | `−0.5` (CLT) | equidistributing, noisy, **= random control** |
| `\|F_N−1/2\|` slope | `−0.18` | `−0.5` | CLT-band, `·√N` wanders 0.06–1.0 |
| `R(N)=D*_N/D*_{N/2}` | wanders 0.47–1.31, **no down-trend** | const `0.707` if equidist; `<0.707 ↓` if bootstrap | **no self-improvement** |
| tail-window norm. disc. | stationary-to-growing (mean 0.94) | shrinking if head certifies tail | **head gives no leverage** |
| corr(head, tail) | `+0.33` (7 pts) | `0` | small-sample noise, no signal |
| orbit `D*` vs random `D*` | same magnitude every `N` | — | **no super-generic / no anomaly** |

## 5. Bankable conclusions (0 false proofs)
1. **[clarified]** The "1/6 effective tail" is a **hypothesis of a proven implication**, not a proven
   bound. Proven = finite check + the algebra `balance_n ≥ n(1/2 − 3|dev|)`. No unconditional effective
   bound on `|even-density − 1/2|` exists (not even `liminf ≥ 1/3`). Only `Θ(log N)` top digits are
   effectively controlled, and the parity is the `Θ(n)`-distant middle digit.
2. **[PROVEN: mechanisms absent + OBSERVED]** No self-improving effective discrepancy bound exists short
   of equidistribution. The three special-point bootstrap mechanisms (automatic, sofic, finite-group) are
   each **provably unavailable** (full complexity `p(k)=2ᵏ`, non-Pisot ⇒ non-sofic, not `S`-unit);
   numerics show no contraction (`R(N)` no down-trend) and no head→tail leverage. A bootstrap would **be**
   the §3.6 effective-equidistribution theorem — it does not shortcut line (5). This is the **same wall**
   as bbchallenge's "no regular certificate", from the effective-bootstrap side.
3. **[PROVEN/clarified]** FLP's `1/3` is a **support** bound (wrong axis), not the effective-density
   ceiling; the `1/3 ↔ 1/3` is numerology. The true gap is **support/log-digit → frequency/middle-digit**
   (= wall (B)), not the size `1/3 → 1/2`. No proven effective density floor exists.

**Net for the program:** the "specific points can be effectively certified" hope is **closed for all
standard routes** and otherwise **identical to line (5)** — but the closure is *productive*: it unifies
the analytic wall with bbchallenge's certificate wall (both = full complexity / non-sofic), and pins the
honest status of the "1/6 effective tail" (a target, not a theorem). Remaining live target unchanged:
line (5) = effective single-orbit equidistribution of the middle digit (§3.6 object).
