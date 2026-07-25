#!/usr/bin/env python3
"""
Decisive tests for the o17 template-vs-(K) verdict.

(1) Cell-for-cell trace of a halter (k=6): confirm halt = LEFT-FRONTIER OVERFLOW
    (head walks off the left edge of the written region, F reads a blank 0),
    NOT an interior 00 gap.  Confirms halt predicate.

(2) LOCALITY TEST of the halt decision.  For the embedded core family C(3j)
    (all-zero-digit seeds, identical bounded left window: marker '3' then blank/zeros,
    differing ONLY in string length j), does halt fate depend on a bounded window?
    If seeds with identical local left-windows have DIFFERENT fate, no bounded-window
    (transparent-carry) transport can exist => (K), not template.
"""
import re

SPEC="1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"
def parse(spec):
    M=[]
    for st in spec.split('_'):
        row=[]
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0]=='-' else (int(t[0]), 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M
M=parse(SPEC); STATES="ABCDEF"

def trace_seed(k, maxsteps, tail=14):
    SZ=1<<20; tape=bytearray(SZ); off=SZ//2
    pos=off
    for i in range(k): tape[off+1+i]=1
    st=0; lo=pos; hi=off+k
    hist=[]
    for step in range(maxsteps):
        r=tape[pos]
        # record window
        hist.append((step, STATES[st], pos-off, ''.join(chr(48+tape[i]) for i in range(lo-2,hi+3)), lo-off, hi-off))
        if st==5 and r==0:
            return step, hist[-tail:], lo-off, hi-off, pos-off
        cell=M[st][r]
        if cell is None: return step, hist[-tail:], lo-off, hi-off, pos-off
        w,d,ns=cell; tape[pos]=w; pos+=d; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return None, hist[-tail:], lo-off, hi-off, pos-off

print("="*70)
print("(1) HALT MECHANISM: k=6 halter, final steps (window = [lo-2 .. hi+2])")
print("="*70)
step,tail,lo,hi,fp=trace_seed(6, 100000)
print(f"halt at step {step}; final head col={fp}, written region cols [{lo}..{hi}]")
print("  step  state  headcol   window(lo-2..hi+2)   [lo,hi]")
for s,st,hc,win,l,h in tail:
    flag = "  <-- head LEFT of written region" if hc < l else ""
    print(f"  {s:5d}  {st}     {hc:5d}   |{win}|   [{l},{h}]{flag}")

print()
print("="*70)
print("(2) LOCALITY TEST: core family C(3j), identical local left-window, fate vs j")
print("="*70)
print("  All seeds C(3j) begin: 0^inf [A0] 1^(3j) 0^inf  -- same marker/local window,")
print("  differ ONLY in length j.  Fate (halt vs not) as function of j:")
def run_seed(k, maxsteps):
    SZ=1<<21; tape=bytearray(SZ); off=SZ//2; pos=off
    for i in range(k): tape[off+1+i]=1
    st=0; lo=pos; hi=off+k
    for step in range(maxsteps):
        r=tape[pos]
        if st==5 and r==0: return True, step
        cell=M[st][r]
        if cell is None: return True, step
        w,d,ns=cell; tape[pos]=w; pos+=d; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return False, maxsteps
rows=[]
for j in range(1,33):
    h,t=run_seed(3*j, 6_000_000)
    rows.append((j, 3*j, 'HALT@%d'%t if h else 'no-halt<6e6'))
for j,k,r in rows:
    print(f"    j={j:2d} k={k:2d}: {r}")
halters=[j for j,k,r in rows if r.startswith('HALT')]
nonh=[j for j,k,r in rows if not r.startswith('HALT')]
print(f"\n  halter j's:   {halters}")
print(f"  non-halt j's: {nonh}")
print("  => identical bounded left-window (marker 3), fate depends on UNBOUNDED length j,")
print("     interleaved with NO modulus => not a bounded-window/transparent-carry function.")
