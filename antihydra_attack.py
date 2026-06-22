#!/usr/bin/env python
"""
Antihydra attack tool — the FAST abstract process (see antihydra_attack.md).

Instead of running the 6-state Turing machine (slow), iterate its derived arithmetic directly:
  Hydra value c:  c <- floor(3c/2),  starting c = 8     (8,12,18,27,40,60,90,135,...)
  balance:        +2 when c is even, -1 when c is odd
  HALT iff the balance ever reaches -1.
Equivalently, with E = #even values so far and n = #steps, balance = 3E - n, and
  HALT  <=>  3E = n-1  <=>  even-density E/n drops to ~1/3   (normally ~1/2).

This is millions of times faster than the TM and lets us study the question:
  does the balance ever hit -1?  (= does the even-density ever fall to 1/3?)
"""
from __future__ import annotations
import math


def run(N, c0=8):
    """iterate N Hydra steps; return a dict of diagnostics (and 'halt_at' if it halts)."""
    c = c0; E = 0; n = 0
    minbal = 10 ** 18; min_at = 0
    oddrun = 0; maxoddrun = 0
    for step in range(1, N + 1):
        n += 1
        if c % 2 == 0:
            E += 1; oddrun = 0
        else:
            oddrun += 1
            if oddrun > maxoddrun:
                maxoddrun = oddrun
        bal = 3 * E - n                       # = 2*E - (n-E), the balance counter
        if bal < minbal:
            minbal = bal; min_at = n
        if bal == -1:
            return {"halt_at": n, "E": E, "n": n}
        c = 3 * c // 2
    return {"halt_at": None, "n": n, "E": E, "even_density": E / n,
            "balance": 3 * E - n, "min_balance": minbal, "min_at": min_at,
            "max_odd_run": maxoddrun}


def v2(x):
    """2-adic valuation: number of trailing binary zeros of x (v2(0)=inf)."""
    if x == 0:
        return float("inf")
    k = 0
    while x % 2 == 0:
        x //= 2
        k += 1
    return k


def oddrun_check(N, c0=8):
    """§3c: verify the Lemma 'odd-run length == v2(c-1)' and the exact 2-adic halting criterion
    over N steps. Returns (runs_checked, all_match, min_halt_gap) where min_halt_gap is the minimum
    of (balance+1 - v2(c-1)); halting would require this to reach <= 0."""
    c = c0; E = 0; runlen = 0; start = 0
    checked = 0; ok = True; min_gap = 10 ** 18
    for n in range(1, N + 1):
        if c % 2 == 1:
            if runlen == 0:
                start = c
            runlen += 1
        else:
            E += 1
            if runlen > 0:
                if v2(start - 1) != runlen:
                    ok = False
                checked += 1
            runlen = 0
        bal = 3 * E - n
        gap = (bal + 1) - v2(c - 1)        # halt <=> gap <= 0 for some n
        if gap < min_gap:
            min_gap = gap
        c = 3 * c // 2
    return checked, ok, min_gap


def summit_probe(N=200000, c0=8):
    """§4a: verify the mod-4 parity rule and measure the halt gap on the real orbit.
    Returns (mod4_ok, max_v2, max_v2_at, min_gap, min_gap_at) where the halt criterion is
    HALT <=> some n has v2(c_n-1) >= balance_n+1, i.e. min_gap = min_n (balance_n+1 - v2(c_n-1)) <= 0."""
    c = c0; E = 0
    mod4_ok = True
    max_v2 = 0; max_v2_at = 0; min_gap = 10 ** 18; min_gap_at = 0
    for n in range(1, N + 1):
        if c % 2 == 0:
            E += 1
        bal = 3 * E - n
        val = v2(c - 1)
        if val > max_v2:
            max_v2 = val; max_v2_at = n
        gap = (bal + 1) - val
        if gap < min_gap:
            min_gap = gap; min_gap_at = n
        nxt = 3 * c // 2
        if ((nxt % 2 == 0) != (c % 4 in (0, 3))):      # mod-4 parity rule
            mod4_ok = False
        c = nxt
    return mod4_ok, max_v2, max_v2_at, min_gap, min_gap_at


def sigma_to_halt(n):
    """Fair-coin model: E ~ Binomial(n, 1/2), mean n/2, std sqrt(n)/2.
    HALT needs E <= (n-1)/3 => a downward deviation of (n/2 - n/3) = n/6,
    i.e. (n/6)/(sqrt(n)/2) = sqrt(n)/3 standard deviations. Returns that many sigmas.
    P(halt at step n) ~ exp(-sigma^2/2) = exp(-n/18); sum over n converges => (Borel-Cantelli)
    the orbit halts with probability 0 under the random model. The orbit is NOT random, so this
    is a heuristic, not a proof — exactly the gap that keeps Antihydra open (antihydra_attack.md §4)."""
    return math.sqrt(n) / 3.0


def main():
    print("Antihydra abstract process — does the balance ever hit -1?\n")
    for N in (1000, 10000, 100000, 300000):
        r = run(N)
        if r["halt_at"]:
            print(f"  N={N}: HALTS at {r['halt_at']}"); continue
        print(f"  n={N:<7} even-density={r['even_density']:.4f} (halt needs ~1/3={1/3:.4f})  "
              f"balance={r['balance']:<7} min-balance={r['min_balance']} @step {r['min_at']}  "
              f"max-odd-run={r['max_odd_run']} (log2 n={math.log2(N):.1f})")
    print("\n  => balance climbs ~0.5n (linear); odd-runs grow ~log2(n); min-balance stays >= 0.")
    print("     Non-halting <= 'even-density > 1/3 forever' (antihydra_attack.md §4) — open (Mahler family).")
    print("\n  Random-model 'why it (probably) never halts' (antihydra_attack.md §3b):")
    print(f"    {'n':>10} {'sigma_to_halt=sqrt(n)/3':>24} {'ln P(halt@n)~-n/18':>20}")
    for n in (10, 1000, 10 ** 5, 10 ** 9):
        print(f"    {n:>10} {sigma_to_halt(n):>24.2f} {-n / 18.0:>20.1f}")
    print("    => sigma-to-halt grows without bound; sum_n exp(-n/18) converges (Borel-Cantelli):")
    print("       halts w.p. 0 in the fair-coin model. Heuristic only — the orbit is deterministic.")
    print("\n  PROVEN 2-adic structure (antihydra_attack.md §3c):")
    checked, ok, min_gap = oddrun_check(200000)
    print(f"    Lemma 'odd-run length == v2(c-1)' holds for all {checked} maximal runs (n<=2e5): {ok}")
    print(f"    exact criterion: HALT <=> exists n with v2(c_n-1) >= balance_n+1.")
    print(f"    min over n<=2e5 of (balance+1 - v2(c-1)) = {min_gap}  (halt needs <= 0; stays > 0).")
    print("\n  SUMMIT — §4a sharpening of the open kernel:")
    m4, mv2, mv2at, mg, mgat = summit_probe(200000)
    print(f"    mod-4 parity rule (next even <=> c==0,3 mod4) holds for n<=2e5: {m4}")
    print(f"    max v2(c_n-1) ever = {mv2} (~log2 n, at n={mv2at}); halt threshold there balance+1 ~ {mv2at//2}.")
    print(f"    HALT <=> c_n == 1 (mod 2^(balance_n+1)); min gap (balance+1 - v2) = {mg} at n={mgat}.")
    print(f"    => gap ~ n/2 - log2(n) -> inf. OPEN kernel: prove v2(c_n-1) < balance_n+1 for ALL n.")


if __name__ == "__main__":
    raise SystemExit(main())
