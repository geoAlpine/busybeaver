#!/usr/bin/env python3
"""INDEPENDENT check of D's rung tile (shares no code with d_spec.py).
Claim: steps(6(u+m)+15) IN(u,m,c,g) = IN(u+2, m-1, c+1, g-3) at pos+3.
Also measures the exact locality window."""
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

def sim(tape, pos, N):
    tape = dict(tape); st='A'; lo=hi=pos
    for t in range(N):
        s = tape.get(pos,0)
        tr = T[st][s]
        if tr is None: return None, None, None, (lo,hi)
        w,d,nx = tr
        if w: tape[pos]=1
        elif pos in tape: del tape[pos]
        pos += d; st = nx
        lo=min(lo,pos); hi=max(hi,pos)
    return st, pos, tape, (lo,hi)

def eq_region(tape, exp_tape, lo, hi):
    for i in range(lo,hi+1):
        if tape.get(i,0) != exp_tape.get(i,0): return False, i
    return True, None

print("u  m  c  g  span  -> result (expect A, pos+3, IN(u+2,m-1,c+1,g-3))   window")
ok=0; bad=0
TAIL=[1,0,1,1,0]; REST=[1,1,0,1]
for u in range(0,4):
  for m in range(1,4):
    for c in range(1,4):
      for g in range(3,7):
        tape,p = build(u,m,c,g,TAIL,REST)
        span = 6*(u+m)+15
        st,pos,out,(lo,hi) = sim(tape,p,span)
        etape,ep = build(u+2,m-1,c+1,g-3,TAIL,REST,p=p+3)
        if st is None: print(f"{u} {m} {c} {g}  HALT!"); bad+=1; continue
        # compare over the union span
        allpos = set(out)|set(etape)
        same = all(out.get(i,0)==etape.get(i,0) for i in allpos)
        good = (st=='A' and pos==p+3 and same)
        if good: ok+=1
        else:
            bad+=1
            if bad<=4:
                diff=[i for i in sorted(allpos) if out.get(i,0)!=etape.get(i,0)]
                print(f"  MISMATCH u={u} m={m} c={c} g={g}: st={st} pos={pos} (exp {p+3}) diffcells={diff[:8]}")
        if (u,m,c,g)==(1,2,2,4):
            print(f"  sample u=1,m=2,c=2,g=4 span={span}: st={st} pos={pos} window=[{lo},{hi}] "
                  f"(pred [{p-2*(u+m)-4}, {p+4}])")
print(f"TILE LAW: {ok} ok, {bad} mismatches")
# control that MUST fail: wrong span
tape,p = build(1,2,2,4,TAIL,REST)
st,pos,out,_ = sim(tape,p,6*(1+2)+15+1)
etape,_ = build(3,1,3,1,TAIL,REST,p=p+3)
print("CONTROL (span+1 must NOT match):", "FAILS as required" if not(st=='A' and pos==p+3 and all(out.get(i,0)==etape.get(i,0) for i in set(out)|set(etape))) else "*** MATCHED - BAD ***")
