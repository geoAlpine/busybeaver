# Construction mode — building an aperiodic lap count: the exact average-vs-max obstruction (2026-07-05)

*Not mapping: a genuine attempt to CONSTRUCT the missing aperiodic analogue of the positive-dyadic-density
"complete-lap" count. Built a valid, periodicity-free deterministic inequality linking the even-count to the max
2-adic depth; verified it; and found — honestly — that it is **too loose to help**, for a reason that is itself the
crux: **aperiodic counting is forced to the MAX (worst-case) run length, while the periodic complete-lap counts the
AVERAGE (exact) — and the average-vs-max gap IS the `(K)` frequency information.** SOUNDNESS: the inequality is
`[PROVEN]` (verified), the negative conclusion `[PROVEN]`; `(K)` `[OPEN]`; no machine decided; no false proof.*

## The construction `[PROVEN, verified N=2·10⁵]`
An odd-run (maximal block of consecutive odd steps) of length `L` corresponds to a 2-adic cylinder `c≡1 mod 2^{L+1}`,
so **`L = max-depth-in-the-run` and `max odd-run = max_i v₂(c_i−1) − 1`** (`MINPROP_RUNS`; verified `20` vs `20`).
Each odd-run ends with `≥1` even step, so with `R` = number of runs:
> **(a)** `R ≤ E_n`  **(b)** `O_n = Σ(run lengths) ≤ R·(max odd-run)`  **⟹**
> **(d)** `E_n ≥ O_n/(max odd-run) = (n−E_n)/(max depth) ⟹ **`E_n ≥ n/(max_depth + 1)`**.**
All four links verified exactly at `N=2·10⁵` (`R=50034≤E=100037`; `O=99963≤R·20`; `E≥n/21`). **This is a genuine
periodicity-free "lap" inequality** — it counts even steps from the run structure with no period, exactly the
aperiodic analogue we sought. It unifies two of the program's open sub-problems: **the even-count floor and the
max-depth ceiling are linked by one exact deterministic inequality.**

## Why it is too loose — and why that is the crux `[PROVEN]`
Plug in the **true** small max-depth (`~20 ~ log n`): `E_n ≥ n/21 ≈ 9500`, but non-halting needs `E_n ≥ n/3 ≈ 66667`.
**`n/21 < n/3` — the inequality fails to give non-halting even when handed the true (tiny) max-depth.** The loss is
structural: `O_n ≤ R·(max run)` treats **every** run as maximal (worst-case), whereas almost all runs are short. The
sharp bound needs the **average** run length `O_n/R`, not the max — and:
> **average run length `= O_n/R = ` mean up-jump `+1 = ` the 2-adic cylinder occupancy `= (K)`.**
So the periodicity-free lap is valid but lossy by exactly the **average-vs-max gap**, and closing that gap is `(K)`.

## The genuine insight (construction-mode payoff)
This constructs *why* the aperiodic complete-lap is hard, rather than asserting it:
- **Periodic (rational, 2606.24972):** a period lets you count the **exact / average** number of `1`s per lap ⇒ a
  tight positive density.
- **Aperiodic (our orbit):** with no period, a deterministic lap can only bound runs by their **max** (worst case);
  `max/average` is exponentially loose here (`max ~ log n` visits vs `average ~ O(1)` — but the max is over a *linear*
  worst-case ceiling `0.585n`), so the count collapses to the trivial.
- **The average-vs-max gap is precisely the frequency/occupancy information `(K)` withholds.** A working aperiodic lap
  would need to prove the **average** run length is bounded — which is `(K)` itself.
This is the sharpest constructive statement of the aperiodic obstruction: *periodicity buys the average; aperiodicity
leaves only the max; the difference is `(K)`.*

## Verdict
**(c) — a real construction, honestly too weak, with the obstruction now built not asserted.** The periodicity-free
lap inequality `E_n ≥ n/(max_depth+1)` is valid and new-in-form (unifying even-count and max-depth), but too loose
because aperiodic counting is max-based; tightening to the average = `(K)`. Construction mode delivered exactly what it
should: a genuine attempt that produces a valid object and reveals, constructively, the precise seam where it breaks.
**`(K)` `[OPEN]`. No machine decided. No label upgraded.**

## Reproduce
- `/tmp/construct_lap.py` (`/opt/homebrew/bin/python3.13`, `N=2·10⁵`): chain `R≤E`, `O≤R·max_run`, `E≥n/(max_depth+1)`
  all verified; `max_odd_run=20=max_depth−1`. Basis: `MINPROP_RUNS`, `OCCUPANCY_PROFILE_THEORY §7`, `EXCURSION_SYNTHESIS`
  (potentials telescope to first moment), `K_LEADS_EVALUATED_2026-07-05` (2606.24972 periodic complete-lap).
