#!/usr/bin/env python
"""
FAST diagnostic: in reachable(o17, blank), every time state A reads a 0, record
(left run of 0s before head, right run of 1s after head). This decides whether the
embedded family head-window 'A 0 1^k' (A reads 0, k ones to its right, blanks to left)
is reachable-window-covered, i.e. whether the all-or-nothing barrier can fire at window
size m (it needs A-reads-0 with right-1-run >= m-2 AND left-0-run >= m-2 simultaneously).
"""
from collections import Counter
SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"
def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M
Mt = parse(SPEC)
A = 0  # state A index

STEPS = 50_000_000
SZ = 1 << 24; tape = bytearray(SZ); off = SZ // 2
pos = off; st = 0; lo = hi = pos
right1 = Counter(); left0 = Counter(); joint = Counter()
maxright_with_left = {}  # left0-run -> max right1-run seen (for A reads 0)
for step in range(STEPS):
    r = tape[pos]
    if st == A and r == 0:
        # left run of 0s (before head, i.e. positions pos-1, pos-2, ... within [lo,hi])
        i = pos - 1; l0 = 0
        while i >= lo and tape[i] == 0:
            l0 += 1; i -= 1
        # if we reached below lo, it's blank-infinity to the left
        left_inf = (i < lo)
        # right run of 1s (after head)
        i = pos + 1; r1 = 0
        while i <= hi and tape[i] == 1:
            r1 += 1; i += 1
        lkey = 'INF' if left_inf else l0
        right1[min(r1, 20)] += 1
        left0[lkey] += 1
        joint[(lkey if lkey == 'INF' else min(l0, 12), min(r1, 20))] += 1
        key = lkey
        if r1 > maxright_with_left.get(key, -1):
            maxright_with_left[key] = r1
    cell = Mt[st][r]
    if cell is None:
        print("HALT?!", step); break
    w, d, ns = cell
    tape[pos] = w; pos += d; st = ns
    if pos < lo: lo = pos
    if pos > hi: hi = pos

print(f"steps={STEPS}, final width={hi-lo+1}")
print("A-reads-0 events total:", sum(right1.values()))
print("\nright-1-run after head (capped 20):")
for k in sorted(right1): print(f"  r1={k}: {right1[k]}")
print("\nleft-0-run before head (INF=A at true left frontier; capped):")
for k in sorted(left0, key=lambda x: (x=='INF', x)): print(f"  l0={k}: {left0[k]}")
print("\nmax right-1-run observed, by left-0-run class:")
for k in sorted(maxright_with_left, key=lambda x:(x=='INF',x)):
    print(f"  left={k}: max right-1-run={maxright_with_left[k]}")
print("\njoint (left0 capped12/INF, right1 capped20) top 25:")
for kv in joint.most_common(25): print("  ", kv)
# the barrier at window m needs: A reads 0 with left-0-run>=m-2 AND right-1-run>=m-2 in ONE event
print("\nFor each m, exists A-reads-0 event with left-0-run>=m-2 and right-1-run>=m-2 ?")
for m in range(2, 16):
    need = m - 2
    ok = any((lk == 'INF' or lk >= need) and rk >= need and cnt > 0
             for (lk, rk), cnt in joint.items())
    print(f"  m={m:2d} (need left>= {need}, right>= {need}): {'YES' if ok else 'NO'}")
