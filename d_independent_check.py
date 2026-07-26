#!/usr/bin/env python3
"""INDEPENDENT re-derivation of D's milestone word (does NOT import d_spec.py).
Decisive question: is D's register  0^33 ++ (10)^k  [pure COMB, cheap]
                or a CHAIN of comb blocks with growing gaps [CASCADE, expensive]?
D^R = 1LB0LA_1RC0RE_0RD0RB_1LA0RF_1RB0LD_1RD---
"""
# table[state][sym] = (write, dir, next)  dir: -1 = L, +1 = R ; next None = halt
T = {
 'A': [(1,-1,'B'), (0,-1,'A')],
 'B': [(1, 1,'C'), (0, 1,'E')],
 'C': [(0, 1,'D'), (0, 1,'B')],
 'D': [(1,-1,'A'), (0, 1,'F')],
 'E': [(1, 1,'B'), (0,-1,'D')],
 'F': [(1, 1,'D'), None],
}
def run(N, marks):
    tape = {}
    pos = 0; st = 'A'; out = {}
    for t in range(N+1):
        if t in marks:
            lo = min(tape) if tape else 0
            hi = max(tape) if tape else 0
            out[t] = (st, pos, lo, hi, dict(tape))
        s = tape.get(pos, 0)
        tr = T[st][s]
        if tr is None:
            out['HALT'] = t; break
        w, d, nx = tr
        if w: tape[pos] = 1
        elif pos in tape: del tape[pos]
        pos += d; st = nx
    return out

def rle_from(tape, lo, hi):
    bits = [tape.get(i,0) for i in range(lo, hi+1)]
    runs = []
    for b in bits:
        if runs and runs[-1][0]==b: runs[-1][1]+=1
        else: runs.append([b,1])
    return runs

def fmt(runs, cap=40):
    parts=[]
    i=0
    while i < len(runs):
        # detect (1 0) comb: alternating 1^1 0^1
        j=i; n=0
        while j+1 < len(runs) and runs[j][0]==1 and runs[j][1]==1 and runs[j+1][0]==0 and runs[j+1][1]==1:
            n+=1; j+=2
        if n>=3:
            parts.append(f"(10)^{n}"); i=j
        else:
            b,l = runs[i]; parts.append(f"{b}^{l}" if l>1 else str(b)); i+=1
    return ' '.join(parts[:cap]) + (' ...' if len(parts)>cap else '')

MARKS = {160, 894, 14130, 66906, 291168, 1196412, 4846662}
res = run(5000000, MARKS)
print("t        state pos    span   register (head-relative RLE, right of leftmost cell)")
for t in sorted(MARKS):
    if t not in res: continue
    st,pos,lo,hi,tape = res[t]
    runs = rle_from(tape, lo, hi)
    print(f"{t:>8} {st}  pos={pos:>6} w={hi-lo+1:>6}  {fmt(runs)}")
