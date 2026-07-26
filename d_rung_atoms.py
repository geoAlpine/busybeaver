#!/usr/bin/env python3
"""D's rung tile, ATOM-LEVEL decomposition — the instrument that must agree with
`lean/DMachine.lean` §3-§4 before a single Lean lemma is written.

Two jobs:
  (1) print the exact state itinerary of one rung and cut it into atoms;
  (2) MEASURE the atom counts as functions of (u,m) so the Lean fold lemmas
      can be stated with the right multiplicities, and re-check the span.

Convention here is IN's *literal* m (as in d_tile_check.py / the tile_* theorems):
    span = 6(u+m)+15,   IN(u,m,c,g) -> IN(u+2,m-1,c+1,g-3) at pos+3,   m >= 1.
"""
T = {'A': [(1,-1,'B'), (0,-1,'A')], 'B': [(1, 1,'C'), (0, 1,'E')],
     'C': [(0, 1,'D'), (0, 1,'B')], 'D': [(1,-1,'A'), (0, 1,'F')],
     'E': [(1, 1,'B'), (0,-1,'D')], 'F': [(1, 1,'D'), None]}

def pow10(n): return [1,0]*n
def pow01(n): return [0,1]*n

def build(u,m,c,g,tail,rest,p=0):
    left = pow10(u) + [1,1] + pow01(m) + [0,0] + [1]*c + tail
    right = [1] + [0]*g + rest
    tape = {}
    for i,b in enumerate(left):
        if b: tape[p-1-i] = 1
    for i,b in enumerate(right):
        if b: tape[p+1+i] = 1
    return tape, p

def run(tape, pos, N):
    """return (itinerary of executed states, final st, final pos, tape)"""
    tape = dict(tape); st='A'; it=[]
    for _ in range(N):
        s = tape.get(pos,0)
        tr = T[st][s]
        if tr is None: return it, None, pos, tape
        it.append(st)
        w,d,nx = tr
        if w: tape[pos]=1
        elif pos in tape: del tape[pos]
        pos += d; st = nx
    return it, st, pos, tape

def chunk(it):
    """compress the itinerary into (block, count) runs of the known atoms"""
    ATOMS = ['ABED','EB','CB','CD','A','B','C','D','E','F']
    out=[]; i=0
    while i < len(it):
        s=''.join(it[i:i+4])
        for a in ATOMS:
            if s.startswith(a):
                if out and out[-1][0]==a: out[-1][1]+=1
                else: out.append([a,1])
                i += len(a); break
    return out

TAIL=[1,0,1,1,0]; REST=[1,1,0,1]

print("=== §1 the itinerary of one rung, cut into atoms ===")
for (u,m,c,g) in [(2,3,2,4),(0,1,1,3),(1,2,2,4),(3,1,2,5)]:
    tape,p = build(u,m,c,g,TAIL,REST)
    span = 6*(u+m)+15
    it,st,pos,_ = run(tape,p,span)
    print(f"u={u} m={m} c={c} g={g} span={span}: {''.join(it)}")
    print(f"    atoms: {'  '.join(f'{a}^{n}' if n>1 else a for a,n in chunk(it))}   -> {st} @ {pos-p:+d}")

print()
print("=== §2 atom multiplicities as functions of (u,m) ===")
print(" u  m | ABED-run1  A  ABED-run2  B  (EB)^i  (CB)^j  CD A | span  check")
for u in range(0,5):
  for m in range(1,5):
    tape,p = build(u,m,2,4,TAIL,REST)
    span = 6*(u+m)+15
    it,st,pos,_ = run(tape,p,span)
    ch = chunk(it)
    desc = ' '.join(f'{a}^{n}' for a,n in ch)
    ok = (st=='A' and pos==p+3)
    print(f"{u:2d} {m:2d} | {desc:52s} | {span:4d}  {'ok' if ok else 'BAD'}")

print()
print("=== §3 the return sweep: where does E->C switch, and what does it do? ===")
u,m,c,g = 2,3,2,4
tape,p = build(u,m,c,g,TAIL,REST)
span = 6*(u+m)+15
# step-by-step dump of the whole rung
tp = dict(tape); pos=p; st='A'
def show(tp,pos,lo,hi):
    return ''.join(('[' if i==pos else ' ')+str(tp.get(i,0))+(']' if i==pos else '') for i in range(lo,hi+1))
lo,hi = p-2*(u+m)-6, p+7
for t in range(span+1):
    s = tp.get(pos,0)
    print(f"t={t:3d} {st} pos={pos-p:+3d}  {show(tp,pos,lo,hi)}")
    if t==span: break
    w,d,nx = T[st][s]
    if w: tp[pos]=1
    elif pos in tp: del tp[pos]
    pos+=d; st=nx
