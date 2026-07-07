#!/usr/bin/env python
"""ah_ledger_orbit.py — Antihydra real-orbit ledger census to n = 10^6.

Task 3: run-length histogram vs budget (deep-2-adic-return frequency at the 1.17-tight
threshold) — depth histogram of odd (drain) and even (refill) runs, deep-return counts vs
the annealed 2^-d law, worst single-run drain fraction s_i/B(entry), max depth vs the
unconditional ceiling 0.585n and the needed 0.5n.

Task 4: LEDGER-MEMORY — the balance is CUMULATIVE (never re-seeds): increments are only
{+2,-1} (verified pointwise), prefix minimum stops updating at n=1, and the suffix minimum
grows linearly (no renewal/reset structure, in contrast to o18's per-generation word wipe).

Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python   (~2 min, native bigints)
"""
import math
from collections import Counter

N = 1_000_000
c = 8
E = 0
B = 0
minB, argminB = 10**9, None            # over n >= 1
last_record_low_n = 0                  # last n where B set a new prefix minimum
worst_avg, arg_worst = 10.0, None
worst_avg100, arg_worst100 = 10.0, None
hist_even, hist_odd = Counter(), Counter()
max_odd, arg_max_odd, ceil_at_max = 0, None, None
worst_drain_frac, arg_wdf = 0.0, None
run_par, run_len, run_B = 0, 0, 0      # c0 = 8 even
Btraj_ck = {}                          # checkpoints
suffix_probe = []                      # (n, B) samples for suffix-min check
inc_ok = True

for n in range(N):
    par = c & 1
    if par != run_par:
        if run_par == 0:
            hist_even[run_len] += 1
        else:
            hist_odd[run_len] += 1
            if run_len > max_odd:
                max_odd, arg_max_odd = run_len, n - run_len
            if run_B > 0 and run_len / run_B > worst_drain_frac:
                worst_drain_frac, arg_wdf = run_len / run_B, n - run_len
        run_par, run_len, run_B = par, 0, B
    run_len += 1
    E += (par == 0)
    Bn = 3*E - (n + 1)
    if Bn - B != (2 if par == 0 else -1): inc_ok = False
    B = Bn
    if B < minB: minB, argminB, last_record_low_n = B, n + 1, n + 1
    a = (2*E - (n + 1)) / (n + 1)
    if a < worst_avg: worst_avg, arg_worst = a, n + 1
    if n + 1 >= 100 and a < worst_avg100: worst_avg100, arg_worst100 = a, n + 1
    if (n + 1) % 100_000 == 0:
        Btraj_ck[n + 1] = B
    if (n + 1) % 10_000 == 0:
        suffix_probe.append((n + 1, B))
    c = (3*c - par) >> 1

print(f"orbit to N={N}: E={E}, even-density={E/N:.6f}, B_N={B}  (bits of c: {c.bit_length()})")
print(f"increment law {{even:+2, odd:-1}} pointwise: {'OK' if inc_ok else 'VIOLATED'}")
print(f"min_(n>=1) B_n = {minB} at n={argminB}; last new prefix-record-low at n={last_record_low_n}")
print(f"worst running avg = {worst_avg:.6f} at N={arg_worst}  (global; -2/23 = {-2/23:.6f})")
print(f"worst running avg over N>=100 = {worst_avg100:.6f} at N={arg_worst100}  (-5/123 = {-5/123:.6f})")
print(f"B checkpoints (n: B, B/n): " +
      ", ".join(f"{k//1000}k: {v} ({v/k:.4f})" for k, v in sorted(Btraj_ck.items())[::2]))

# suffix minima: cumulative memory (no re-seed) — min of B over [n, N] should grow ~ n/2
print("\nLEDGER-MEMORY (Task 4): suffix minima of B (min over [n, 10^6]):")
suf = []
m = 10**18
for n, b in reversed(suffix_probe):
    m = min(m, b)
    suf.append((n, m))
suf.reverse()
for n, m in suf[::20]:
    print(f"   n = {n:>7}: min_(m>=n) B_m = {m}")
resets = sum(1 for i in range(1, len(suf)) if suf[i][1] < suf[i-1][1] * 0.5)
print(f"   B never re-seeds: increments only {{+2,-1}}, prefix min frozen since n={last_record_low_n}, "
      f"suffix min nondecreasing-in-practice (halvings: {resets}) -> CUMULATIVE, slope ~ B_N/N = {B/N:.4f}")

# run-length histograms vs annealed 2^-d law
n_odd = sum(hist_odd.values()); n_even = sum(hist_even.values())
print(f"\nRUN HISTOGRAM vs BUDGET (Task 3): {n_even} even runs (mean {sum(k*v for k,v in hist_even.items())/n_even:.4f}), "
      f"{n_odd} odd runs (mean {sum(k*v for k,v in hist_odd.items())/n_odd:.4f}); annealed means = 2, 2")
print("   d | odd runs (=deep returns v2(c-1)=d) | expected n_odd*2^-d | even runs | expected")
for d in range(1, max_odd + 1):
    print(f"  {d:>2} | {hist_odd.get(d,0):>10} | {n_odd*2**-d:>12.1f} | {hist_even.get(d,0):>9} | {n_even*2**-d:>10.1f}")
print(f"   max odd-run depth = {max_odd} at n={arg_max_odd}: unconditional ceiling 0.585n = {0.585*arg_max_odd:.0f}, "
      f"needed (0.5n) = {0.5*arg_max_odd:.0f}, truth ~ log2 n = {math.log2(arg_max_odd):.1f}")
print(f"   worst single-run drain fraction s_i/B(entry) = {worst_drain_frac:.4f} at n={arg_wdf}  (fatality = exceed 1)")
# aggregate-form margin (framework Link 2, Kac): the induced odd map's gap D = v2(3o-1)
# satisfies mean D = (total steps)/(odd steps) = 1/(1 - even-density); need >= 3/2 <=> density >= 1/3
meanD = N / (N - E)
print(f"   renewal form: mean D = N/O_N = {meanD:.5f}  (needed >= 3/2 <=> even-density >= 1/3; annealed/Haar = 2)")
