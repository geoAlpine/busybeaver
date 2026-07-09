# o7 decision attempt via finite congruence / automaton invariant on the thin-set wall (2026-07-10)

*The first actual DECISION attempt on a BB(6) cryptid. Target: o7, the sole non-Type-I census machine, whose
protection is a thin-set `2^k`-reachability wall (not a density/(K) wall). Method: forward-reachable-set
(congruence-automaton) invariants on its milestone dynamics. Interpreter
`/Users/aokiyousuke/quantum-ecc/.venv/bin/python`, exact big-int. Scripts: `o7d_verify.py`, `o7d_verify_F.py`,
`o7d_reach.py`, `o7d_reach_odd.py`. SOUNDNESS: labels `[PROVEN]`/`[OBSERVED]`; over-approximations only. Nothing
committed.*

## 0. Verdict

**NO SEPARATION AT ANY MODULUS TRIED — the thin-set reachability wall is REAL for o7.** Two independent SOUND
over-approximations of the forward-reachable set both fail to avoid the halting-consistent residues:

- **2-adic milestone automaton** `(u mod 2^J·m, b mod M)`, `J ≤ 14`, `m ∈ {1,3,5,7}`: the u-projection reaches a
  power-of-2 residue at every modulus.
- **odd-adic cascade automaton** `u mod m`, all odd `m ≤ 729`: the reachable set is the **FULL** ring `ℤ/m` for
  every `m` coprime to 3, and for `3∣m` it is proper (size `m/3`) but **still contains every power of 2**.

o7 stays `[OPEN]`. The obstruction is intrinsic (the odd-part / 2-adic-valuation coupling is the Collatz
obstruction itself). Reported honestly per the mandate. **No machine decided. No label upgraded.**

## 1. Exact dynamics, re-derived and re-verified from the raw TM

`o7 = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC`. Milestone state = `(a,b)` (machine config `D`, tape `0 1^a 0 1^b`).
Write `u := a+3`. **HALT ⟺ `a=1` ⟺ `u = 2^k` (k≥2) ⟺ oddpart(u)=1.** Milestone automaton (`o7d_verify.py`,
`step_map` re-checked against the raw TM, **0 mismatches over 30·10⁶ raw steps**):

```
a=1  (u=4)      -> HALT
a=3  (u=6)      -> a'=b+5,          b'=1+(b mod 2)          (special)
a even (u odd)  -> a'=3a/2+1+b,     b'=1        EVEN branch  [COUPLES b into a]
a odd  (u even) -> a'=(a-3)/2,      b'=b+(a+5)/2  ODD branch [autonomous halving: u'=u/2]
```

The even branch is **not** autonomous in `u` — it injects the ledger `b`. So no invariant on `u` alone is
forward-closed at the milestone level unless `b` is tracked too.

**The b-free cascade-compressed map `F` [PROVEN given the automaton; 0 violations].** A cascade = maximal run of
ODD branches; it is entered with `b=1` (the preceding EVEN branch resets `b→1`). Collapsing one cascade + its
reseed + the following even-chain gives a map on cascade-entry values `u_e` (always even) that needs **no `b`**:

```
w = oddpart(u_e),  d = v2(u_e)            (HALT iff w==1, i.e. u_e a power of 2)
b_exit = 1 + (u_e - w) + d
u_1    = (3w-1)/2 + b_exit                 (reseed; u_1 odd)
x_1    = u_1 + 1,   v = v2(x_1)
u_e'   = 3^v · oddpart(x_1) - 1            (next cascade entry)
```

Verified: `F` reproduces the next cascade entry with **0 mismatches over 49,940 entry-to-entry transitions**
(`o7d_verify_F.py`, orbit to 200k milestones, final `u_e` ≈ 40,459 bits), and on the 7 transitions extracted
directly from the raw TM. `b=1` at **all** 49,941 entries (the `a=3` path, which alone could give `b∈{1,2}`, is
never taken). `min oddpart(u_e) = 7` over the whole orbit `[OBSERVED]` — the orbit never approaches a power of 2.

## 2. The congruence-automaton invariants (both SOUND)

**Halt-consistent residues.** A halt requires `u = 2^k` at a milestone, so `H_M = {2^k mod M : k≥2}`. Separation
= the reachable u-set avoids `H_M`.

**(A) 2-adic milestone automaton** (`o7d_reach.py`). State `(u mod M, b mod M)`, `M=2^J·m`. Branch selection is
by `u mod 2` (exact). Every `/2` is handled by the 2-adic 2-way lift `x/2 → {x/2, x/2+M/2}` — SOUND (the true
value is always included; the low `J` bits of `u` are tracked exactly, so this is the depth-`J` parity
look-ahead the plan calls for). BFS to closure from the real seed `(u,b)=(5,2)`.

**(B) odd-adic cascade automaton** (`o7d_reach_odd.py`). State `u_e mod m`, `m` odd (2 and 3 invertible). The
2-adic valuations `d=v2(u_e)`, `v=v2(x_1)` are independent of `u_e mod m`, so they are SOUNDLY over-approximated
by enumerating every residue class of `d` (period `lcm(ord_m 2, m)`) and `v` (period covering `ord_m 2` and the
eventual period of `3^v mod m`). The true `(d,v)` are always among them, so `R_m` is a sound superset of the real
cascade-entry residues.

## 3. Results — no separation anywhere

| model | moduli | outcome |
|---|---|---|
| (A) 2-adic `(u,b)` | `2^J·m`, `J=1..14`, `m∈{1,3,5,7}` | u-projection reaches a power-of-2 residue (u≡4/8/16/32) at **every** M; `|Hu|=1`; never separated |
| (B) odd-adic `u_e` | all odd `m ≤ 729` | `R_m = ℤ/m` (**FULL**) for every `m` coprime to 3; for `3∣m`, `R_m` proper (`|R_m|=m/3`) but **contains every `2^k`** (`|Hu|>0`); never separated |

**Why it is full (the honest structural reason).** Mod `m`, `w = oddpart(u_e) = u_e·2^{-d}` and the successor
carries `3^v·2^{-v}`; with `d,v` free the odd part sweeps the whole cyclic orbit `u_e·⟨2^{-1}⟩` and the `3^v`
factor sweeps `⟨3⟩`, so the image fills `ℤ/m`. This is precisely the Collatz-type coupling between the 2-adic
valuation and the residue — the operation "oddpart" is not congruence-continuous, and it sits inside **both** the
halt condition and the dynamics. No finite `mod M` model can see it.

Direct-simulation coverage of the small-`k` halts `H_M` requires (the automaton test covers all `k`, but for the
record): the real orbit's `min oddpart(u_e)=7` over 49,941 entries (to ~40k bits) means **no** cascade entry is a
power of 2 — no small-`k` halt occurred `[OBSERVED]`.

## 4. Soundness ledger
- `step_map` vs raw TM: 0 mismatch / 30·10⁶ steps. `F` vs orbit: 0 mismatch / 49,940 transitions + 7 raw.
- Both reachable-set models are over-approximations (2-way 2-adic lifts in A; full `d,v` enumeration in B);
  "no separation" is therefore a genuine impossibility result *for these invariant families*, not a modeling gap
  in the permissive direction. A `[PROVEN]` non-halt would have required a separation; none exists.
- Nothing strengthens any non-halting claim; nothing committed.

**The thin-set reachability wall is real for o7. No machine decided. No label upgraded.**
