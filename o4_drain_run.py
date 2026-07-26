#!/usr/bin/env python3
"""o4 drain-run bound (2026-07-26): PROVE-and-VERIFY that the base-4/3 odometer's
drain-run length L(n) equals v_3(G_n + 14) exactly, hence L(n) <= log_3(G_n+14) ~ 0.262 n
(unconditional), and that the O(log n) bound would need v_3(G_n+14)=O(log n) = (K).

Gseq recurrence (from lean/Completion.lean + Template.cOdo):
  G_{n+1} = 4*G_n//3 + cOdo(G_n),  cOdo = {G%3==0:3, 1:5, 2:1},  G_0 = 43.
Drain step  <=> G % 3 == 1  (ledger -1 branch).  No machine decided. No label upgraded.
"""
def cOdo(G):
    r = G % 3
    return 3 if r == 0 else (5 if r == 1 else 1)

def v3(x):
    v = 0
    while x % 3 == 0:
        x //= 3; v += 1
    return v

N = 300000
G = 43
Gs = [G]
for _ in range(N):
    G = 4*G//3 + cOdo(G)
    Gs.append(G)

# drain-run length starting at each n = number of consecutive steps with G%3==1
# L(n) as maximal run: count k>=0 while Gs[n+k]%3==1
# Claim A: for the START of a maximal run (i.e. Gs[n-1]%3!=1 or n==0), L(n) = v3(Gs[n]+14)
# Actually claim: for EVERY n with Gs[n]%3==1, the remaining-run-from-n = v3(Gs[n]+14)? test both.
import math
mismatch_v3 = 0
checked = 0
max_run = 0
argmax_n = 0
runs = []  # (start n, length)
n = 0
while n <= N:
    if Gs[n] % 3 == 1:
        L = 0
        while n+L <= N and Gs[n+L] % 3 == 1:
            L += 1
        # L = length of maximal drain run starting at n
        # claim: L == v3(Gs[n]+14)
        pred = v3(Gs[n] + 14)
        checked += 1
        if pred != L:
            mismatch_v3 += 1
            if mismatch_v3 <= 5:
                print(f"  MISMATCH @n={n}: run L={L}, v3(G+14)={pred}, G={Gs[n]}")
        runs.append((n, L))
        if L > max_run:
            max_run = L; argmax_n = n
        n += L
    else:
        n += 1

print(f"checked {checked} maximal drain-runs up to N={N}")
print(f"L(n) == v3(G_n + 14) mismatches: {mismatch_v3}   -> {'CONFIRMED' if mismatch_v3==0 else 'FALSE'}")
print(f"max drain-run = {max_run} at n={argmax_n}")
print(f"  G_{{{argmax_n}}} has {len(str(Gs[argmax_n]))} digits; log_3(G+14) = {math.log(Gs[argmax_n]+14,3):.2f}")
print(f"  crude bound L <= log_3(G_n+14): {max_run} <= {math.log(Gs[argmax_n]+14,3):.2f}  {'OK' if max_run <= math.log(Gs[argmax_n]+14,3)+1 else 'VIOLATED'}")
# growth: log_3(G_n) vs 0.262 n
import statistics
slopes = [math.log(Gs[n]+14,3)/n for n in range(1000, N, 50000)]
print(f"  log_3(G_n+14)/n  (=> crude bound slope): ~{statistics.mean(slopes):.4f}  (theory log_3(4/3)={math.log(4/3,3):.4f})")
# max run as function of N: is it ~ log_3(N) [(K)-heuristic] or ~0.262 N [crude]?
print("  max-run vs prefix length (is it log-like or linear?):")
for cap in [1000, 10000, 100000, 300000]:
    mr = max(L for (s,L) in runs if s <= cap) if any(s<=cap for s,_ in runs) else 0
    print(f"    N={cap:>7}: max_run={mr:>3},  log_3(N)={math.log(cap,3):.1f},  0.262*N={0.262*cap:.0f}")
