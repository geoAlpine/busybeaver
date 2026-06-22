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


if __name__ == "__main__":
    raise SystemExit(main())
