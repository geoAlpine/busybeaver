# o4 GAP-FRONTIER local-structure test (2026-07-06)
# Question: when the head is at the true left frontier (leftmost reached cell, into raw 0^G),
# is the local microstep computation drawn from a FIXED FINITE set independent of G?
# If yes -> the frontier is a bounded-width traveling wave -> window closure provable.
# We collect: (a) every distinct "frontier event" = the (state,read) sequence executed while
# the head is within `edge` cells of the running minpos, keyed by the local window it starts from;
# (b) how many distinct frontier local-windows (radius R) occur, vs G.
from collections import defaultdict

def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

def run(N,R=8):
    tape=defaultdict(int); pos=0; st='A'
    minpos=0; maxpos=0
    frontier_windows=defaultdict(lambda:[0,None,10**18,0])  # win -> count,first_step,minG,maxG
    # record the state in which the head first touches a brand-new leftmost cell (extends minpos)
    extend_events=defaultdict(int)  # state that writes the new leftmost cell
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return dict(halt=True,step=s)
        G=maxpos-minpos
        # frontier window: head within R of minpos
        if pos <= minpos + R:
            win=(st,)+tuple(tape.get(pos+o,0) for o in range(-R,R+1))
            rec=frontier_windows[win]; rec[0]+=1
            if rec[1] is None: rec[1]=s
            rec[2]=min(rec[2],G); rec[3]=max(rec[3],G)
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos<minpos:
            minpos=pos; extend_events[st]+=1
        if pos>maxpos: maxpos=pos
    return dict(halt=False, fw=dict(frontier_windows), extend=dict(extend_events),
                gmax=maxpos-minpos)

if __name__=='__main__':
    R=8
    r=run(30_000_000,R=R)
    print(f"final Gmax~{r['gmax']}   distinct frontier windows (state,radius {R}): {len(r['fw'])}")
    print(f"states that extend the frontier (write new leftmost cell): {r['extend']}")
    print("\nfrontier windows: count, first-step, G-range   (should be finite & G-independent)")
    for win,(ct,fs,gmn,gmx) in sorted(r['fw'].items(), key=lambda kv:-kv[1][0])[:40]:
        print(f"  {win}  x{ct:<9,} first@{fs:<10,} G in [{gmn},{gmx}]")
    # key test: are there windows first seen only at LARGE G (=> set still growing)?
    late=[(win,rec) for win,rec in r['fw'].items() if rec[1] and rec[1]>0.5* (r['gmax'] and 1)]
    firsts=sorted(rec[1] for rec in r['fw'].values())
    print(f"\nlatest first-appearance step among all frontier windows: {max(firsts):,}")
    print(f"(if << total steps, the frontier-window set has saturated)")
