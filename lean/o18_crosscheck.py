#!/usr/bin/env python3
# Cross-check for lean/O18.lean: mirrors the L1 anchors + the L2 sweeps + the
# L3 clean_gate against an independent zipper simulator of
#   o18 = 1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---   (halt = F reads 1)
# Run: /usr/bin/python3 o18_crosscheck.py   (exit 0 = all OK)
import sys
SPEC = "1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else
                       (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M
M = parse(SPEC)

class Z:
    __slots__ = ('left', 'head', 'right')
    def __init__(s, l, h, r): s.left = list(l); s.head = h; s.right = list(r)
    def mvR(s): s.left.insert(0, s.head); s.head = s.right.pop(0) if s.right else 0
    def mvL(s): s.right.insert(0, s.head); s.head = s.left.pop(0) if s.left else 0

def step(st, pos, z):
    tr = M[st][z.head]
    if tr is None: return None
    w, d, ns = tr; z.head = w; (z.mvR() if d > 0 else z.mvL()); return (ns, pos + d, z)

def run(st, pos, z, n):
    for _ in range(n):
        r = step(st, pos, z)
        if r is None: return None
        st, pos, z = r
    return (st, pos, z)

A, B, C, D, E, F = 0, 1, 2, 3, 4, 5
def pow10(k): return [1, 0] * k
def pow01(k): return [0, 1] * k
def ones(k):  return [1] * k

ok = True
def chk(name, got, exp):
    global ok
    good = got == exp
    ok = ok and good
    print(f"[{'OK ' if good else 'BAD'}] {name}")
    if not good: print("   got", got, "\n   exp", exp)

# --- L1 anchors (Lean sanity100 / sanity300) ---
st, pos, z = run(A, 0, Z([], 0, []), 100)
chk("sanity100", (st, pos, z.left, z.head, z.right),
    (A, -16, [], 0,
     [1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1]))
st, pos, z = run(A, 0, Z([], 0, []), 300)
chk("sanity300", (st, pos, z.left, z.head, z.right),
    (B, -26, [1,0,1,0,1,1], 1,
     [0,1,0,1,0,1,0,1,0,1] + [1]*21))

# --- L2 sweepAB : A on 0, right=(10)^k M -> A +2k, left (01)^k, right M ---
for k in range(0, 20):
    L = [1, 1, 0]; Mt = [1, 0, 1]
    st, pos, z = run(A, 0, Z(L, 0, pow10(k) + Mt), 2 * k)
    chk(f"sweepAB k={k}", (st, pos, z.left, z.head, z.right),
        (A, 2 * k, pow01(k) + L, 0, Mt))

# --- L2 sweepDC : D on 0, left=(10)^k L -> D -2k, right 1^{2k} ---
for k in range(0, 20):
    L = [1, 0, 1]; R = [1, 1, 0]
    st, pos, z = run(D, 0, Z(pow10(k) + L, 0, R), 2 * k)
    chk(f"sweepDC k={k}", (st, pos, z.left, z.head, z.right),
        (D, -2 * k, L, 0, ones(2 * k) + R))

# --- L3 clean_gate : D on 0, left=(10)^k 1 1, right R -> F on 0, 1^{2k+3} R ---
for k in range(0, 15):
    for R in ([], [1, 0, 1]):
        st, pos, z = run(D, 0, Z(pow10(k) + [1, 1], 0, list(R)), 2 * k + 3)
        chk(f"clean_gate k={k} R={R}", (st, pos, z.left, z.head, z.right),
            (F, -(2 * k + 3), [], 0, ones(2 * k + 3) + R))

print("ALL OK" if ok else "FAILURES")
sys.exit(0 if ok else 1)
