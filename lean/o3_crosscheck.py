#!/usr/bin/env python3
"""Numeric cross-check mirror for lean/O3.lean (second fully-formalized machine).

Mirrors every Lean statement of O3.lean with (a) a faithful zipper simulator
matching the Lean `mvR`/`mvL` semantics EXACTLY (trailing-blank canonical form)
and (b) an INDEPENDENT dict-tape simulator, then checks they agree with the
Lean anchors.  o3 = 1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC.

Run:  /usr/bin/python3 o3_crosscheck.py   (expect: ALL OK, exit 0)
"""
import sys
from collections import defaultdict

SPEC = "1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC"
def parse(spec):
    M = {}
    for kk, blk in enumerate(spec.split('_')):
        st = "ABCDEF"[kk]
        for r in (0, 1):
            c = blk[3*r:3*r+3]
            M[(st, r)] = None if c[0] == '-' else (int(c[0]), 1 if c[1] == 'R' else -1, c[2])
    return M
M = parse(SPEC)

# ---- (a) faithful zipper simulator (matches Lean O3.step / mvR / mvL) ----
def mvR(l, h, r):
    return ([h]+l, 0, []) if not r else ([h]+l, r[0], r[1:])
def mvL(l, h, r):
    return ([], 0, [h]+r) if not l else (l[1:], l[0], [h]+r)
def zip_run(st, l, h, r, N):
    pos = 0
    for _ in range(N):
        rd = 1 if h else 0
        a = M[(st, rd)]
        if a is None:
            return ('HALT', pos)
        w, d, ns = a
        h = w
        l, h, r = (mvR if d > 0 else mvL)(l, h, r)
        pos += d; st = ns
    return (st, pos, l, h, r)

# ---- (b) independent dict-tape simulator ----
def dict_run(cells, st, N):
    t = defaultdict(int);
    for c, v in cells.items(): t[c] = v
    pos = 0
    for _ in range(N):
        rd = t[pos]
        a = M[(st, rd)]
        if a is None:
            return ('HALT', pos)
        w, d, ns = a
        if w == 0: t.pop(pos, None)
        else: t[pos] = w
        pos += d; st = ns
    return (st, pos, dict((c, v) for c, v in t.items() if v))

def pow10(m): return [1, 0]*m
def pow01(m): return [0, 1]*m
def dep6(): return [1, 1, 1, 0, 1, 1]

ok = True
def check(name, cond):
    global ok
    print(("  OK   " if cond else "  FAIL ") + name)
    ok = ok and cond

print("== L1: machine + blank-tape anchors (sanity100, sanity300) ==")
# blank tape: cells empty, start A
r = zip_run('A', [], False, [], 100)
check("sanity100 zipper = (D, -8, [1], 1, (01)^5 0)",
      r == ('D', -8, [1], 0, [0,1,0,1,0,1,0,1,0,1,0]) if False else
      (r[0]=='D' and r[1]==-8 and r[2]==[1] and r[3]==1 and
       r[4]==[0,1,0,1,0,1,0,1,0,1,0]))
r = zip_run('A', [], False, [], 300)
check("sanity300 zipper = (B, -20, [1], 0, (10)^11 1 1 0)",
      r[0]=='B' and r[1]==-20 and r[2]==[1] and r[3]==0 and
      r[4]==pow10(11)+[1,1,0])
# independent dict-tape agreement
d100 = dict_run({}, 'A', 100); d300 = dict_run({}, 'A', 300)
check("dict-tape N=100 agrees (state,pos)", d100[0]=='D' and d100[1]==-8)
check("dict-tape N=300 agrees (state,pos)", d300[0]=='B' and d300[1]==-20)

print("== L2: crawlR (period-10, +6), crawlL (period-20, -6), zigzag (period-6, -2) ==")
# crawlR: n tiles, [A] head0, right = 0::(10)^(k+3n)::M  ->  +6n, dep6n on left, 0::(10)^k::M
for (n, k, Ltail, Mtail) in [(6,0,[0],[1,1]),(4,2,[1,0],[0]),(10,1,[],[1,1,0])]:
    l = list(Ltail); h = 0; r = [0]+pow10(k+3*n)+Mtail
    res = zip_run('A', l, h, r, 10*n)
    exp = ('A', 6*n, dep6()*n + Ltail, 0, [0]+pow10(k)+Mtail)
    check(f"crawlR n={n} k={k}", res == exp)
# crawlL: n tiles, [D] head1, left = dep6^n :: Lr, right R -> -6n, (01)^(3n)::R, R untouched
for (n, Lr, R) in [(5,[9],pow10(5)),(3,[1,0],pow10(4)+[0,0]),(8,[],pow10(2))]:
    l = dep6()*n + Lr; res = zip_run('D', l, 1, list(R), 20*n)
    exp = ('D', -6*n, Lr, 1, pow01(3*n)+R)
    check(f"crawlL n={n}", res == exp)
# zigzag: n tiles, [C] head1, left = (11)^n :: Lr, right 1::R' -> -2n, (10)^n prepended
for (n, Lr, Rp) in [(3,[8],[0,1,0,1,0,0]),(5,[1,1],[0]*4),(1,[],[1,0,1,0])]:
    l = [1,1]*n + Lr; res = zip_run('C', l, 1, [1]+Rp, 6*n)
    exp = ('C', -2*n, Lr, 1, pow10(n)+[1]+Rp)
    check(f"zigzag n={n}", res == exp)

print("== L3 (partial): body_phase1 + full body B(j)->B(j-3) landing ==")
def Bcells(j):
    c = {}; c[1]=0
    for i in range(j): c[2+2*i]=1
    c[2+2*j]=1; c[3+2*j]=1
    return c
def Bzip(j):  # zipper form of B(j)
    return [0], 0, [0]+pow10(j)+[1,1]
# phase1: j=3m, 10m steps -> A, +6m, dep6^m ++ [0] on left, right = [0,1,1]
for m in (4,5,6,8,17):
    j = 3*m; l,h,r = Bzip(j); res = zip_run('A', list(l), h, list(r), 10*m)
    exp = ('A', 6*m, dep6()*m + [0], 0, [0,1,1])
    check(f"body_phase1 m={m} (j={j})", res == exp)
# full body: 10j+4 steps -> state A, pos -2, halt-free; matches dict-tape independently
for j in (12,15,18,21,24,30,51):
    l,h,r = Bzip(j); res = zip_run('A', list(l), h, list(r), 10*j+4)
    dres = dict_run(Bcells(j), 'A', 10*j+4)
    check(f"full body j={j}: (A,-2), halt-free, zipper==dict",
          res[0]=='A' and res[1]==-2 and dres[0]=='A' and dres[1]==-2)
# halt gate: E reads 0 with right-neighbour 0 = HALT (F0). standalone M(a,0) a==2 mod3 halts.
def Mcells(a,k):  # milestone 0^inf [A] 0 0 (10)^a (110)^k
    c={}; base=2
    for i in range(a): c[base+2*i]=1
    p=base+2*a
    for i in range(k): c[p+3*i+0]=1; c[p+3*i+1]=1  # 110 block: 1 1 0
    return c
h8 = dict_run(Mcells(8,0),'A',10**6)
check("halt gate: standalone M(8,0) (a=8=2 mod3, k=0) HALTS", h8[0]=='HALT')
h11= dict_run(Mcells(11,0),'A',10**6)
check("standalone M(11,0) HALTS (a=11=2 mod3)", h11[0]=='HALT')

print()
print("ALL OK" if ok else "SOME FAILURES")
sys.exit(0 if ok else 1)
