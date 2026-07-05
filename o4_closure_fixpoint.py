# o4 forward-closure FIXPOINT of the head-window transition (2026-07-06)
# Compute the least set W* containing the observed windows and closed under the
# adversarial microstep (incoming cell in {0,1}).  A SOUND local certificate exists
# iff W* is finite AND contains no unsafe (B reads 1, right-nbr 1) AND no halt window.
# Reports whether the free-incoming closure explodes into unsafe -> pins the wall.
from collections import defaultdict,deque

def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

def collect(N,R):
    tape=defaultdict(int); pos=0; st='A'; W=set()
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return None
        W.add((st,)+tuple(tape.get(pos+o,0) for o in range(-R,R+1)))
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
    return W

def succ(w,R,incoming):
    st=w[0]; cells={o:w[1+i] for i,o in enumerate(range(-R,R+1))}
    r=cells[0]; a=M[(st,r)]
    if a is None: return ('HALT',None,False)
    wr,d,ns=a
    unsafe=(st=='B' and r==1 and cells.get(1)==1)
    cells[0]=wr
    newc={}
    for o in range(-R,R+1):
        oldo=o+d
        newc[o]=cells[oldo] if oldo in cells else incoming
    return ('OK',(ns,)+tuple(newc[o] for o in range(-R,R+1)),unsafe)

def fixpoint(seed,R,cap=2_000_000):
    W=set(seed); q=deque(seed); unsafe_hit=[]; halt_hit=[]
    while q:
        w=q.popleft()
        for inc in (0,1):
            kind,wp,uns=succ(w,R,inc)
            if kind=='HALT':
                halt_hit.append(w); continue
            if uns and len(unsafe_hit)<8: unsafe_hit.append(w)
            if wp not in W:
                W.add(wp); q.append(wp)
                if len(W)>cap: return dict(size=len(W),blew=True,unsafe=unsafe_hit,halt=halt_hit)
    return dict(size=len(W),blew=False,unsafe=unsafe_hit,halt=halt_hit)

if __name__=='__main__':
    for R in (2,3,4,5):
        seed=collect(2_000_000,R)
        maxwin=6*2**(2*R+1)
        fp=fixpoint(seed,R)
        verdict = ("SOUND CERTIFICATE (PROOF)" if (not fp['blew'] and not fp['unsafe'] and not fp['halt'])
                   else "certificate FAILS")
        why=[]
        if fp['unsafe']: why.append(f"{len(fp['unsafe'])}+ unsafe reachable")
        if fp['halt']:   why.append("HALT reachable")
        if fp['blew']:   why.append("blew cap")
        print(f"R={R}: seed={len(seed)}  fixpoint|W*|={fp['size']}  (max possible {maxwin})  "
              f"-> {verdict}  {'; '.join(why)}")
        if fp['unsafe']:
            print("   e.g. unsafe-reachable window (B reads 1 w/ right-nbr 1):", fp['unsafe'][0])
