#!/usr/bin/env python
"""
Diagnose WHY the A01^k embedded-family barrier stops at m=9:
  - which length-m windows of 'A 0 1^k' are MISSING from grams(reachable)?
  - is it a sampling artifact (longer run includes them) or genuine (off reachable window set)?
Also census: does reachable ever have state A reading 0 at the far-left frontier with many
blanks to the left and a long 1-run to the right (the 'A 0 1^k' head window)?
"""
import sys
sys.path.insert(0, "/Users/aokiyousuke/quantum-ecc/busybeaver")
from far_dfa import reachable_configs, canon
from far import STATES

O17 = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

def grams_of(cfg, m):
    pad = ["0"] * (m - 1)
    seq = pad + list(cfg) + pad
    return [tuple(seq[i:i+m]) for i in range(len(seq) - m + 1)]

def G_from(configs, m):
    G = set()
    for cfg in configs:
        for g in grams_of(cfg, m):
            G.add(g)
    return G

for N in (200_000, 1_000_000, 3_000_000):
    configs, halted = reachable_configs(O17, N)
    assert not halted
    print("="*72)
    print(f"reachable run N={N} ({len(configs)} configs)")
    print("="*72)
    for m in (8, 9, 10, 11, 12):
        G = G_from(configs, m)
        # missing windows of halter A 0 1^k with k>=m+2 (so 1^m window present)
        k = m + 5
        c = canon(["A", "0"] + ["1"] * k)
        miss = [g for g in grams_of(c, m) if g not in G]
        # dedup preserve order
        seen=set(); missu=[g for g in miss if not (g in seen or seen.add(g))]
        print(f"  m={m:2d}: |G|={len(G):6d}  A01^{k} missing grams ({len(missu)} distinct): {missu}")

# Census: in reachable, when state A reads a 0, what is its (left-run-of-0, right-run-of-1)?
print("\n" + "="*72)
print("CENSUS: state A reading 0 in reachable — left-blank-run and right-1-run lengths")
print("="*72)
configs, _ = reachable_configs(3_000_000, 0) if False else reachable_configs(O17, 1_000_000)
from collections import Counter
leftblank = Counter(); right1 = Counter(); both=Counter()
for cfg in configs:
    s = list(cfg)
    # find marker
    try:
        j = next(i for i,ch in enumerate(s) if ch in STATES)
    except StopIteration:
        continue
    if s[j] != 'A':
        continue
    head = j+1
    if head >= len(s) or s[head] != '0':
        continue
    # left run of 0 immediately before marker
    lb = 0; i = j-1
    while i >= 0 and s[i] == '0':
        lb += 1; i -= 1
    lb_eff = lb if i >= 0 else 10**9  # 10^9 = blank-infinity to the left
    # right run of 1 after head cell
    r1 = 0; i = head+1
    while i < len(s) and s[i] == '1':
        r1 += 1; i += 1
    leftblank[lb_eff] += 1; right1[min(r1,15)] += 1
    both[(min(lb_eff,5) if lb_eff<10**9 else 'INF', min(r1,15))] += 1
print("  left-blank-run before A (INF=A at true left frontier):", dict(leftblank.most_common(10)))
print("  right-1-run after head cell (capped 15):", dict(sorted(right1.items())))
print("  (leftblank capped5/INF, right1 capped15) joint top:", both.most_common(12))
sys.stdout.flush()
