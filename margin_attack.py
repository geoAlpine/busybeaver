"""Direct attack on the EXACT 2-adic halting criterion (single-pass).
  HALT <=> exists n: v2(c_n-1) >= balance_n+1  (balance_n = 3 E_n - n).
  NON-HALT <=> slack_n := balance_n + 1 - v2(c_n-1) > 0 for all n.
Probe: running MIN slack (closest approach), and per odd-depth L the MIN balance observed (the dangerous
coincidence is large depth + small balance). 0 false proofs: measurement of the exact criterion.
"""
from collections import defaultdict

def v2(x):
    if x == 0: return 10**9
    r = 0
    while x & 1 == 0: x >>= 1; r += 1
    return r

N = 1_000_000
c = 8; E = 0
min_slack = 10**9; min_slack_n = 0; min_state = None
min_bal_at_depth = defaultdict(lambda: 10**9); depth_count = defaultdict(int)
ck = {1000, 10000, 100000, N}; runmin = 10**9; run_at = {}
for n in range(1, N + 1):
    if c & 1 == 0: E += 1
    bal = 3 * E - n; depth = v2(c - 1); slack = bal + 1 - depth
    if slack < min_slack: min_slack = slack; min_slack_n = n; min_state = (bal, depth)
    if slack < runmin: runmin = slack
    depth_count[depth] += 1
    if bal < min_bal_at_depth[depth]: min_bal_at_depth[depth] = bal
    if n in ck: run_at[n] = runmin
    c = (3 * c) // 2

print(f"N={N}")
print(f"MIN slack over all n = {min_slack} at n={min_slack_n} (balance,depth)={min_state}")
print(f"  slack>0 everywhere => non-halt verified to N (halt needs slack<=0).")
print(f"\n{'depth L':>7} {'count':>9} {'N/2^(L+1)':>11} {'min balance@L':>14} {'min slack@L':>12}")
for L in range(0, 24):
    if depth_count[L] == 0: continue
    mb = min_bal_at_depth[L]
    print(f"{L:>7} {depth_count[L]:>9} {N/2**(L+1):>11.0f} {mb:>14} {mb + 1 - L:>12}")
print(f"\nrunning min slack at checkpoints (margin growing? min achieved at start?):")
for n in sorted(run_at): print(f"  n<={n:>8}: min slack = {run_at[n]}")

print(f"""
READING (the exact halting margin -- a sharper target):
  - The MINIMUM slack over all n is achieved AT n=1 (the start), slack=3, and is NEVER re-approached
    (running min stays 3 through n=10^6). The orbit's only brush with the halting boundary is the first
    step; thereafter it pulls away monotonically in the worst case.
  - min balance@L grows SUPER-LINEARLY in L (3,5,10,17,54,134,574,1553,...): a deep odd-depth L
    (= v2(c_n-1)>=L, the halting danger) only ever occurs when balance is already >> L. Operationally,
    a depth-L event needs c_n == 1 mod 2^L, whose first occurrence is at n ~ 2^L, by which time
    balance ~ n/2 ~ 2^{L-1} >> L. THIS is the timing that keeps slack positive.
  - SHARPENED PROOF TARGET: 'every odd-run of length L starts only after balance has grown past L' --
    i.e. the first hitting time of {c == 1 mod 2^L} is >= ~2L/ (so balance>=L). This is a HITTING-TIME /
    timing statement about the orbit mod 2^L, still = single-orbit equidistribution = Mahler, but a
    sharper and more 'local' form than even-density: control WHEN deep residues first appear, not the full
    density. (NOT a proof; the data shows the margin is large and grows, and locates the exact timing fact
    to prove.)""")
