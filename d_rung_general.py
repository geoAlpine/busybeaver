#!/usr/bin/env python3
"""D's rung tile at FULL generality — the exact hypotheses the Lean proof will assume.

Two things this instrument decides:
  (A) the SPAN.  `lean/DMachine.lean`'s `RungTile` says `6*(u+m)+15` on `IN u (m+1) ...`,
      i.e. 6(u+m)+15 with the *shifted* m.  The tile_* instances say 6(u+m_literal)+15.
      Those differ by 6.  Which is right?
  (B) how far the hypotheses relax: is `c >= 1` needed (RungTile assumes `c+1`)?
      is `g = 3` enough?  are TAIL/REST really arbitrary (incl. hostile prefixes)?
"""
import itertools, random

T = {'A': [(1,-1,'B'), (0,-1,'A')], 'B': [(1, 1,'C'), (0, 1,'E')],
     'C': [(0, 1,'D'), (0, 1,'B')], 'D': [(1,-1,'A'), (0, 1,'F')],
     'E': [(1, 1,'B'), (0,-1,'D')], 'F': [(1, 1,'D'), None]}

def pow10(n): return [1,0]*n
def pow01(n): return [0,1]*n

def build(u,m,c,g,tail,rest,p=0):
    left  = pow10(u) + [1,1] + pow01(m) + [0,0] + [1]*c + tail
    right = [1] + [0]*g + rest
    tape = {}
    for i,b in enumerate(left):
        if b: tape[p-1-i] = 1
    for i,b in enumerate(right):
        if b: tape[p+1+i] = 1
    return tape, p

def sim(tape,pos,N):
    tape=dict(tape); st='A'; lo=hi=pos
    for _ in range(N):
        s=tape.get(pos,0); tr=T[st][s]
        if tr is None: return None,None,None,(lo,hi)
        w,d,nx=tr
        if w: tape[pos]=1
        elif pos in tape: del tape[pos]
        pos+=d; st=nx; lo=min(lo,pos); hi=max(hi,pos)
    return st,pos,tape,(lo,hi)

def check(u,m,c,g,tail,rest,span):
    tape,p = build(u,m,c,g,tail,rest)
    st,pos,out,(lo,hi) = sim(tape,p,span)
    if st is None: return False,'HALT',None
    etape,_ = build(u+2,m-1,c+1,g-3,tail,rest,p=p+3)
    allp = set(out)|set(etape)
    same = all(out.get(i,0)==etape.get(i,0) for i in allp)
    return (st=='A' and pos==p+3 and same), f"st={st} pos={pos-p:+d}", (lo-p,hi-p)

print("=== (A) which span? ===")
for (u,m) in [(0,1),(1,2),(2,3),(3,1)]:
    a = check(u,m,2,4,[1,0,1],[1,1], 6*(u+m)+15)[0]        # literal-m span (tile_* instances)
    b = check(u,m,2,4,[1,0,1],[1,1], 6*(u+(m-1))+15)[0]    # RungTile's stated span
    print(f"  u={u} m_literal={m}:  6(u+m)+15={6*(u+m)+15} -> {'OK' if a else 'FAIL'}   "
          f"RungTile's 6(u+m-1)+15={6*(u+m-1)+15} -> {'OK' if b else 'FAIL'}")

print()
print("=== (B) hypothesis relaxation sweep (span = 6(u+m_literal)+15) ===")
ok=bad=0; fails=[]
rng = random.Random(20260726)
TAILS = [[], [1], [0], [1,1], [0,0], [1,0,1,1,0], [0,1,0,1], [1]*7, [0]*7]
RESTS = [[], [1], [0], [1,1], [0,0], [1,1,0,1], [0,0,0,0], [1,0]*4]
for u in range(0,5):
  for m in range(1,5):
    for c in range(0,4):            # <-- c = 0 included: does the tile need c >= 1?
      for g in range(3,7):          # <-- g = 3 included: is 3 the true floor?
        for tail in TAILS:
          for rest in RESTS:
            good,msg,win = check(u,m,c,g,tail,rest,6*(u+m)+15)
            if good: ok+=1
            else:
                bad+=1
                if len(fails)<6: fails.append((u,m,c,g,tail,rest,msg))
print(f"  {ok} ok, {bad} fail")
for f in fails: print("   FAIL", f)

print()
print("=== (B2) g = 2 must FAIL (g>=3 is a real hypothesis, not slack) ===")
for g in (0,1,2,3):
    good,msg,_ = check(1,2,2,g,[1,0,1],[1,1],6*(1+2)+15)
    print(f"  g={g}: {'matches' if good else 'no match ('+str(msg)+')'}")

print()
print("=== (C) locality window (TAIL/REST provably untouched) ===")
for (u,m,c,g) in [(0,1,0,3),(2,3,2,4),(4,4,3,6)]:
    _,_,win = check(u,m,c,g,[1,0,1,1,0],[1,1,0,1],6*(u+m)+15)
    print(f"  u={u} m={m} c={c} g={g}: window {win}  (pred left {-2*(u+m)-4}, right +4)")

print()
print("=== (D) atom-phase step accounting vs 6(u+m)+15 ===")
print("   4u (crawl^u) + 4 (crawl over [1,1]) + 1 (A1 marker) + 4m (crawl^m) + 1 (A0 turnaround)")
print("   + 2 (S2) + 2m (S1^m) + 2(u+2) (S2^{u+2}) + 3 (turn)")
for u in range(0,4):
  for m in range(1,4):
    tot = 4*u + 4 + 1 + 4*m + 1 + 2 + 2*m + 2*(u+2) + 3
    print(f"   u={u} m_lit={m}: phases={tot}  span={6*(u+m)+15}  {'OK' if tot==6*(u+m)+15 else 'MISMATCH'}")
