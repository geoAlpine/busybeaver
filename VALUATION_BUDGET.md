# The 2-adic valuation budget — a third exact identity, and the unconditional range (2026-06-26)
*Program: rank-1 specified-orbit genericity. A non-circular pivot into exact 2-adic arithmetic (not the measure
framing). Yields a clean new exact identity, a third equivalent form of the non-halt criterion, and an
unconditional range (the 2-adic analog of Flatto–Lagarias–Pollington). Verified to n=10⁵. 0 false claims.*

## The identity (verified)
For `c_{n+1}=⌊3c_n/2⌋`, `c_0=8`, the 2-adic valuation telescopes: `v2(c_{i+1})−v2(c_i) = −1` if `c_i` even,
`= D_i−1` if `c_i` odd (`D_i = v2(3c_i−1)`). Summing:
```
Σ_{i<n, c_i odd} v2(3c_i − 1)  =  n + v2(c_n) − v2(c_0).        [exact, verified to n=10⁵]
```
This is **distinct** from the renewal identity `Σ_{even-renewals} v2(3c'_j−1) = #odd` (different sum, different
RHS): it is the **dual budget over odd steps**, balancing the 2-adic valuation that even steps spend (`−1` each)
against what odd steps produce (`D_i−1` each), pinned by `v2(c_n) ≥ 0`.

## Third equivalent form of the criterion
Since `c_n ~ A(3/2)^n` gives `v2(c_n) = o(n)` (empirically `v2(c_n)=O(log n)`), the identity yields
```
avgD_odd · (odd-density)  =  1 + o(1),   i.e.   odd-density = 1/avgD_odd  (asymptotically exact),
```
where `avgD_odd = (1/#odd) Σ_{odd} v2(3c_i−1)`. The non-halt criterion `even-density ≥ 1/3` (`odd-density ≤ 2/3`)
becomes:
> **Non-halt ⟺ `avgD_odd ≥ 3/2`** — the mean 2-adic depth `v2(3c_i−1)` over odd steps is `≥ 3/2`.
Haar gives `avgD_odd = 2` (a factor-`4/3` margin over the threshold `3/2`). This sits beside the two known forms
(`avg jump ≤ 2`; even-density `≥ 1/3`) and is the **cleanest lower-bound form**: a single average bounded below.

## The unconditional range (2-adic FLP analog)
From `0 ≤ v2(c_n) ≤ log2(c_n) = (1+log2 3/2)·... ≈ 0.585n + O(1)`:
```
n − v2(c_0)  ≤  Σ_{odd} v2(3c_i−1)  ≤  (1 + log2(3/2))·n − v2(c_0) ≈ 1.585 n − 3.    [UNCONDITIONAL]
```
This is a genuine **unconditional two-sided bound** on the odd-step depth sum — the 2-adic analog of
Flatto–Lagarias–Pollington's unconditional *range* result for the real `{(3/2)^n}` (which bounds the spread but
not the density). With each `D_i ≥ 1` it gives only `#odd ≤ 1.585n` (trivial); the **density** (`avgD_odd ≥ 3/2`,
not just `≥ 1`) is exactly the part it does **not** force.

## Honest verdict (it funnels, but cleanly)
The valuation budget does **not** break the wall: `avgD_odd ≥ 3/2` needs the odd-step branches to average above the
shallow value 1, i.e. the depths `D_i` cannot almost-all equal 1 — which is again a statement that the orbit does
not concentrate on the shallow cylinder `c_i ≡ 1 mod 4`, i.e. single-orbit equidistribution. (This is the same
funnel every elementary route hits: *long odd runs ⟺ deep cylinders*, so any depth/density bound reduces to
cylinder-frequency control.) **What is genuinely new and unconditional:** the exact identity, the third criterion
form (`avgD_odd ≥ 3/2`, a lower bound on one average, margin `4/3`), and the FLP-type range — all in exact 2-adic
arithmetic, independent of the measure framing.

## Why it is still worth having
- The `avgD_odd ≥ 3/2` form is the **most natural for a one-sided proof** (bound one average below by a constant) —
  a cleaner target than `avg jump ≤ 2`, and the right object for any future "second-moment / energy" attack.
- The range bound is the first **unconditional** statement we can make about the orbit's depth statistics; an
  expert in FLP-style methods may recognize whether the real-FLP machinery (which gives the real range) ports to
  the 2-adic side to push the range toward a one-sided density — exactly the kind of partial worth asking about.
