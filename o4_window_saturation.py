# o4 B-reads-1 WINDOW-SET saturation test (2026-07-06)
# Does the set S of B-reads-1 local windows saturate (finite) as G grows,
# and does every element stay SAFE (right-neighbour 0)?
# Record, per window, first-seen step, count, and the min/max tape-max (~G proxy) at which it occurs.
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

def run(N, W):
    tape=defaultdict(int); pos=0; st='A'
    unsafe=0
    wins=defaultdict(lambda:[0,None,10**18,0])  # count, first_step, minG, maxG
    maxpos=0
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return dict(halt=True, step=s)
        if st=='B' and r==1:
            win=tuple(tape.get(pos+o,0) for o in range(-W,W+1))
            rec=wins[win]; rec[0]+=1
            if rec[1] is None: rec[1]=s
            rec[2]=min(rec[2],maxpos); rec[3]=max(rec[3],maxpos)
            if tape.get(pos+1,0)==1: unsafe+=1
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos>maxpos: maxpos=pos
    return dict(halt=False, wins=dict(wins), unsafe=unsafe, gmax=maxpos)

if __name__=='__main__':
    W=5
    print(f"window radius W={W}")
    prev=set()
    for N in (2_000_000, 8_000_000, 32_000_000):
        r=run(N,W)
        cur=set(r['wins'].keys())
        new=cur-prev
        # verify safety: index of offset +1 is W+1
        bad=[w for w in cur if w[W+1]==1]
        print(f"N={N:>10}: gmax~{r['gmax']:>6}  |S|={len(cur):>3}  new={len(new):>3}  UNSAFE={r['unsafe']}  bad-windows={len(bad)}")
        prev=cur
    print("\nFinal window census (window @ radius 5) : count, first-step, G-range-seen")
    for win,(ct,fs,gmn,gmx) in sorted(r['wins'].items(), key=lambda kv:-kv[1][0]):
        safe = "SAFE" if win[W+1]==0 else "UNSAFE!!"
        print(f"  {win}  x{ct:<9,} first@{fs:<9} G∈[{gmn},{gmx}]  {safe}")
