#!/usr/bin/env python
# RED TEAM attack 3 (prefix cone edge G>=37, "all a") + full-generation composition audit.
#  - From M(G,a): run 471 steps; hash the (st,r,w,d) word; check span [-11,30]; check landing:
#    zone (10)^19 1001 occupying [-11,30], REMAINING gap zeros [31,G-1], filler intact at G.
#  - Edge probe: G=31..36 (below cone) to see where/how it breaks.
#  - Composition: M(G,a) -> next milestone == (odo(G), a+delta(G)) for edge G=37..48 and spot G.
from collections import defaultdict
import hashlib
from o4_redteam_suffix import TT, build_M, run, summarize_miles, odo, delta

def prefix_run(G,a,steps=471):
    tape0,pos0,st0=build_M(G,a)
    tape=defaultdict(int)
    for kk,v in tape0.items(): tape[kk]=v
    pos=pos0; st=st0
    word=[]; lo=hi=0; unsafe=0
    for s in range(steps):
        r=tape[pos]; act=TT[(st,r)]
        if act is None: return dict(halt=True, steps=s)
        if st=='B' and r==1 and tape[pos+1]==1: unsafe+=1
        w,d,ns=act
        word.append((st,r,w,d))
        if w==0: tape.pop(pos,None)
        else: tape[pos]=1
        pos+=d; st=ns
        lo=min(lo,pos); hi=max(hi,pos)
    h=hashlib.sha256(str(word).encode()).hexdigest()[:12]
    # landing checks
    zone_ok = all(tape[-11+2*i]==1 and tape[-10+2*i]==0 for i in range(19)) \
              and tape[27]==1 and tape[28]==0 and tape[29]==0 and tape[30]==1
    gap_ok  = all(tape[i]==0 for i in range(31,G))
    fill_ok = all(tape[G+2*i]==1 and tape[G+2*i+1]==0 for i in range(a)) and tape[G+2*a]==1 \
              and tape[G+2*a+1]==0 and tape[G+2*a+2]==0 and tape[G+2*a+3]==1
    nothing_left = all(tape[i]==0 for i in range(lo-2,-11))
    return dict(halt=False, hash=h, span=(lo,hi), unsafe=unsafe, pos=pos, st=st,
                zone_ok=zone_ok, gap_ok=gap_ok, fill_ok=fill_ok, clean_left=nothing_left)

if __name__=='__main__':
    print("========= PREFIX: fixed 471-step word, G>=37, ALL a =========")
    base=None; allok=True
    for G in (37,38,39,40,41,42,100,101,102,103,200,501,1000):
        for a in (0,1,2,8,20):
            r=prefix_run(G,a)
            if base is None: base=r['hash']
            ok = (not r['halt']) and r['hash']==base and r['zone_ok'] and r['gap_ok'] and r['fill_ok'] \
                 and r['span']==(-11,30) and r['unsafe']==0 and r['clean_left']
            if not ok: allok=False
            tag='OK ' if ok else 'FAIL'
            print(f"  G={G:>4} a={a:>2}: {tag} hash={r.get('hash')} span={r.get('span')} "
                  f"zone={r.get('zone_ok')} gap={r.get('gap_ok')} fill={r.get('fill_ok')} "
                  f"end=({r.get('pos')},{r.get('st')}) unsafe={r.get('unsafe')}")
    print(f"  PREFIX uniformity over grid: {allok}  (hash={base})")

    print("\n========= PREFIX below the cone: G=31..36 =========")
    for G in (31,32,33,34,35,36):
        r=prefix_run(G,8)
        print(f"  G={G}: hash={'SAME' if r.get('hash')==base else 'DIFFERENT'} span={r.get('span')} "
              f"zone={r.get('zone_ok')} gap={r.get('gap_ok')} fill={r.get('fill_ok')} unsafe={r.get('unsafe')}")

    print("\n========= COMPOSITION: full generation M(G,a) -> M(odo(G), a+delta(G)) =========")
    allok=True
    for G in list(range(37,49))+[100,101,102,275,500]:
        a = 8 if G%3!=1 else 8   # a>=2 needed at G≡1
        t,p,s=build_M(G,a)
        Ge,ae=odo(G),a+delta(G)
        r=run(t,p,s,200_000_000,stop_at_gap=Ge)
        sm=summarize_miles(r['miles'])
        # milestones seen along the way: should include exactly (Ge,ae) as the excursion max
        land = sm[-1] if sm else None
        ok = land is not None and land[1]==Ge and land[2]==ae and r['unsafe']==0 and r['f1']==0
        if not ok: allok=False
        print(f"  M({G:>3},{a}) -> exp ({Ge},{ae})  got {land[1:] if land else None}  "
              f"{'OK' if ok else 'FAIL'}  unsafe={r['unsafe']} f1={r['f1']} steps={r['steps']}")
    print(f"  COMPOSITION all OK: {allok}")

    print("\n========= LEDGER edge: a=2 at G≡1 (validity floor), a=1,0 (below) =========")
    for (G,a) in [(37,2),(40,2),(100,2),(37,1),(37,0),(40,1),(40,0)]:
        t,p,s=build_M(G,a)
        Ge,ae=odo(G),a+delta(G)
        r=run(t,p,s,50_000_000,stop_at_gap=Ge)
        sm=summarize_miles(r['miles'])
        land=sm[-1] if sm else None
        print(f"  M({G},{a}): exp ({Ge},{ae}) got {land[1:] if land else None} halt={r['halt']} "
              f"unsafe={r['unsafe']} f1={r['f1']} timeout={r.get('timeout',False)}")
