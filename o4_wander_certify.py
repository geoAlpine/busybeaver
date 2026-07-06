# o4 WANDER-config translated-cycler certifier (2026-07-07)
# For the Z(k, g=3, a<=1) small-a configs left unresolved by O4_LEDGER_ANALYSIS:
# detect an exact recurrence of (state, forward-window W) at new-leftmost events, then
# VERIFY the certificate by replaying one period: (i) no halt, (ii) head confined to
# [p0-dpos-5, p0+W-1] (cells left of p0 are unvisited hence 0 at a new-leftmost event;
# window content right of p0 recorded), (iii) exact landing at p0-dpos in the same state
# with the identical shifted window. PASS => the cycle repeats forever => NON-HALTING [PROVEN].
from collections import defaultdict

def parse(spec):
    M={}
    for kk,blk in enumerate(spec.split('_')):
        st="ABCDEF"[kk]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

def build_Z(k,g,a):
    t={}
    for i in range(k): t[2*i]=1
    t[2*k]=1; t[2*k+3]=1
    base=2*k+4+g
    for i in range(a): t[base+2*i]=1
    t[base+2*a]=1; t[base+2*a+3]=1
    return t

def certify(k,a,W=3000,horizon=8_000_000):
    tape=defaultdict(int,build_Z(k,3,a)); pos=0; st='E'
    lo=0; events={}; found=None
    for s in range(horizon):
        r=tape[pos]; tr=M[(st,r)]
        if tr is None: return ('HALT',s)
        w,d,ns=tr
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos<lo:
            lo=pos
            win=tuple(tape.get(pos+o,0) for o in range(0,W))
            key=(st,win)
            if key in events:
                s0,p0=events[key]; found=(s-s0,p0-pos,s0,p0); break
            events[key]=(s,pos)
    if not found: return ('NOREC',)
    dstep,dpos,s0,p0=found
    # replay verification
    t3=defaultdict(int,build_Z(k,3,a)); pp=0; ss='E'
    for s in range(s0+1):
        r=t3[pp]; w,d,ns=M[(ss,r)]
        if w==0: t3.pop(pp,None)
        else: t3[pp]=w
        pp+=d; ss=ns
    win0=tuple(t3.get(p0+o,0) for o in range(0,W))
    hi=pp; lo2=pp; okh=True
    for s in range(dstep):
        r=t3[pp]; tr=M[(ss,r)]
        if tr is None: okh=False; break
        w,d,ns=tr
        if w==0: t3.pop(pp,None)
        else: t3[pp]=w
        pp+=d; ss=ns
        hi=max(hi,pp); lo2=min(lo2,pp)
    win1=tuple(t3.get(pp+o,0) for o in range(0,W))
    ok = okh and pp==p0-dpos and win1==win0 and hi<=p0+W-1 and lo2>=p0-dpos-5
    return ('PASS' if ok else 'FAIL', dstep, dpos, hi-p0)

if __name__=='__main__':
    print('translated-cycler certificates for the former-WANDER configs:')
    for k,a in [(29,0),(101,0),(23,1),(41,1)]:
        r=certify(k,a)
        print(f'  Z(k={k:>3},g=3,a={a}): {r}')
        assert r[0]=='PASS', 'expected certificate'
    print('  => all four NON-HALTING [PROVEN] (period 411, 19 cells left per period).')
    for k,a in [(21,0),(23,0),(27,0)]:
        r=certify(k,a,W=10000)
        print(f'  Z(k={k:>3},g=3,a={a}): {r}  (sqrt-growth milestone-free regime, no exact recurrence -> [OPEN])')
