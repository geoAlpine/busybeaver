#!/usr/bin/env python3
"""
Mahler-sea survey — o11 residue check (2026-07-07).
Which (k mod 4) does the real blank orbit visit at clean [1^k 0 (10)^m] milestones?
(The fatal map shows k=2 mod 4 rows fully fatal in the standalone family; if the real
orbit only ever visits other residues, the protection is a residue-avoidance statement
on the doubly-exponential refill orbit.) [OBSERVED]
"""
import sys
from collections import Counter
from msea_struct2 import run_milestones

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 40_000_000
    snaps = run_milestones("1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", 1, 'R', N)
    clean = [(s, b[0], len(b) - 1) for s, b in snaps
             if len(b) >= 2 and b[0] > 1 and all(x == 1 for x in b[1:])]
    print(f"clean milestones: {len(clean)}")
    print("  (step, k, m, k mod 4):")
    for s, k, m in clean:
        print(f"    {s:>10,}  k={k:<5} m={m:<6} k%4={k % 4}")
    print(f"  k%4 census: {dict(Counter(k % 4 for _, k, _ in clean))}")
    print(f"  (k%4, m%2) census: {dict(Counter((k % 4, m % 2) for _, k, m in clean))}")
    print("No machine decided. No label upgraded.")
