# o4 growing-regime CERTIFIER (2026-07-07)
# Decides the three standalone configs Z(k, g=3, a=0), k in {21,23,27} (the last [OPEN]
# entries of the small-a fatal-region map, O4_LEDGER_ANALYSIS_2026-07-06 SS4).
#
# STRUCTURE OF THE PROOF (certified trace-template method, red-team-corrected form of
# O4_TEMPLATE_CLOSURE_2026-07-06):
#   Family:  C(m) := 0^inf [head, state A, on 0] (10)^m 0 1 0^inf     (m >= 2)
#            (= bare zone (10)^(m-1) 1001, head one cell left of it; NO gap, NO filler.
#             Identity: C(m) is the body-lemma config B(m-1) after exactly one step E1=1LA,
#             so the C-generation is the PURE BODY iteration with nothing to its right.)
#   (0) SWEEP LEMMAS [PROVEN, 2-transition induction, checked from the transition table]:
#         B1F0 rightward read-only sweep, D1E0 leftward inverting sweep -- arbitrary length.
#   (1) ENTRY [concrete, exact]: Z(k,3,0) reaches, at a new-leftmost event, the EXACT global
#       config C(2) (all cells left of the head unvisited hence 0; all 1-cells matched),
#       with no halt and zero unsafe B-reads-1 on the way.
#   (2) SMALL-m CHAIN [concrete, exact]: C(m) -> C(m+2) shifted -1, exact global config,
#       for every m = 2..18 (below the template's compression threshold), unsafe=0,
#       span within [-2, 2m+4].
#   (3) TEMPLATE LEMMA [certified trace-template]: for all m >= 19, C(m) -> C(m+2) shifted -1
#       in exactly 4m+11 steps, span [-2, 2m+4], unsafe=0, no halt. Certified by:
#         (a) episode-skeleton IDENTITY across the grid (both parities),
#         (b) sweep lengths exactly AFFINE in m,
#         (c) EPISODE-LANDMARK PINNING: every episode step sits at an m-INDEPENDENT offset
#             from the left edge (cell 0) or the right terminator (cell 2m+1) -- so with
#             sweeps traversing only the uniform (10)^* region, the tape is symbolically
#             reconstructible and the first-divergence generalization closes (the red-team
#             repair of the sweep-termination gap),
#         (d) exact-landing endpoint spot-checks at LARGE m (up to 100001).
#   (4) INDUCTION: from C(2) the exact global orbit is C(2) -> C(4) -> C(6) -> ... forever;
#       every generation is halt-free; hence the machine never halts from Z(k,3,0).
#
# VERDICT if all checks pass: Z(21,3,0), Z(23,3,0), Z(27,3,0) are NON-HALTING
# [PROVEN -- candidate, pending main-loop re-verification]. These configs are STANDALONE
# (not claimed reachable from o4's initial tape); o4 itself stays [OPEN].
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

# ---------- (0) sweep lemmas, mechanically checked from the table ----------
def check_sweeps():
    # B1F0 rightward read-only: B on 1 -> (1,R,F); F on 0 -> (0,R,B).
    assert M[('B',1)]==(1,1,'F') and M[('F',0)]==(0,1,'B'), "B1F0 sweep broken"
    # => induction on n: from state B on the first 1 of (10)^n, after 2n steps the head is
    #    2n cells right, state B, tape unchanged. (Each pair: B1 rewrites 1, F0 rewrites 0.)
    # D1E0 leftward inverting: D on 1 -> (0,L,E); E on 0 -> (1,L,D).
    assert M[('D',1)]==(0,-1,'E') and M[('E',0)]==(1,-1,'D'), "D1E0 sweep broken"
    # => induction on n: from state D on the last 1 of (01)^n, after 2n steps the head is
    #    2n cells left, state D, the block inverted (10)^n -> (01)^n cellwise 1->0, 0->1.
    print("(0) sweep lemmas B1F0 (read-only right) / D1E0 (invert left): "
          "transition-table check PASS -> arbitrary length by 2-transition induction [PROVEN]")

# ---------- (0b) conjugation to the PROVEN body lemma ----------
def check_conjugation():
    """C(m) = B(m-1) after exactly one step. B(k) = 0^inf [E, on first 1] (10)^k 1001 0^inf
    (o4_body_proof.py). Step E1 = 1LA rewrites the 1 and moves left => head at -1 on 0,
    state A, tape (10)^k 1001 = (10)^(k+1) 0 1 = C(k+1). Hence the C-generation lemma at m
    is EQUIVALENT to the certified body lemma at k = m-1 (steps 4m+11 = 15+4(m-1); sweeps
    (2m, 2m+2) = (2+2k, 4+2k)); for even m >= 20 it is INHERITED from the body lemma
    [PROVEN for all odd k >= 19]."""
    assert M[('E',1)]==(1,-1,'A'), "E1 transition changed?"
    for k in (19,20,50):
        B={};  # B(k) per o4_body_proof.build_B
        for i in range(k): B[2*i]=1
        B[2*k]=1; B[2*k+3]=1
        C=build_C(k+1)
        assert {c for c,v in B.items() if v}=={c for c,v in C.items() if v}, f"k={k}: tape mismatch"
    print("(0b) conjugation C(m) = B(m-1) + one step (E1=1LA): tape identity + transition PASS")
    print("     => the even-m C-lemma (m>=20) is the certified BODY LEMMA at k=m-1 [PROVEN]")

# ---------- config builders / exact-shape recognizer ----------
def build_C(m):
    t={}
    for i in range(m): t[2*i]=1
    t[2*m+1]=1
    return t

def build_Z(k,g,a):
    t={}
    for i in range(k): t[2*i]=1
    t[2*k]=1; t[2*k+3]=1
    base=2*k+4+g
    for i in range(a): t[base+2*i]=1
    t[base+2*a]=1; t[base+2*a+3]=1
    return t

def is_C(tape,pos):
    """tape dict holds EXACTLY the 1-cells (zeros are popped). Return m if the global config
    is exactly 0^inf [pos] (10)^m 0 1 0^inf, else None."""
    ones=sorted(c for c,v in tape.items() if v)
    if len(ones)<2: return None
    if ones[0]!=pos+1: return None
    body=ones[:-1]; last=ones[-1]; mm=len(body)
    for i,c in enumerate(body):
        if c!=pos+1+2*i: return None
    if last!=pos+2*mm+2: return None
    return mm

# ---------- (1) entry: Z(k,3,0) -> exact C(2) ----------
def entry(k,horizon=200_000):
    tape=defaultdict(int,build_Z(k,3,0)); pos=0; st='E'; lo=0; unsafe=0
    for s in range(1,horizon+1):
        r=tape[pos]; tr=M[(st,r)]
        if tr is None: return dict(halt=True,steps=s)
        if st=='B' and r==1 and tape.get(pos+1,0)==1: unsafe+=1
        w,d,ns=tr
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos<lo:
            lo=pos
            if st=='A' and tape.get(pos,0)==0:
                mm=is_C(tape,pos)
                if mm is not None:
                    return dict(halt=False,steps=s,pos=pos,m=mm,unsafe=unsafe)
    return dict(halt=False,steps=None)

# ---------- generation runner with full trace ----------
def gen_trace(m,want_trace=True):
    """run C(m) (head at -1, state A) to the first new-leftmost event whose global config is
    exactly a C-shape. Returns landing m', shift, steps, span, unsafe, and the trace of
    (state,read,write,move,pos-before-step)."""
    tape=defaultdict(int,build_C(m)); pos=-1; st='A'
    lo=-1; hi=2*m+1; unsafe=0; trace=[] if want_trace else None
    s=0
    while True:
        s+=1
        r=tape[pos]; tr=M[(st,r)]
        if tr is None: return dict(halt=True,steps=s)
        if st=='B' and r==1 and tape.get(pos+1,0)==1: unsafe+=1
        w,d,ns=tr
        if want_trace: trace.append((st,r,w,d,pos))
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos>hi: hi=pos
        if pos<lo:
            lo=pos
            if st=='A' and tape.get(pos,0)==0:
                mm=is_C(tape,pos)
                if mm is not None:
                    return dict(halt=False,m2=mm,shift=-1-pos,steps=s,lo=lo,hi=hi,
                                unsafe=unsafe,trace=trace)
        if s>10**8: return dict(halt=False,m2=None,steps=s)

# ---------- trace compression (same method as o4_body_proof.py) ----------
def compress(trace):
    """compress maximal uniform period-2 stretches (>=8 steps) into ('SWEEP',cycle,len,startpos)."""
    key=[(t[0],t[1],t[2],t[3]) for t in trace]
    out=[]; i=0; n=len(key)
    while i<n:
        j=i
        while j+2<n and key[j+2]==key[j]: j+=1
        L=j+2-i
        if L>=8 and key[i]!=key[i+1]:
            take=L-(L%2)
            out.append(('SWEEP',(key[i],key[i+1]),take,trace[i][4]))
            i+=take
        else:
            out.append(('E',key[i],trace[i][4])); i+=1
    return out

def skeleton(comp):
    skel=[]; lens=[]; ep_pos=[]
    for e in comp:
        if e[0]=='SWEEP':
            skel.append(('SWEEP',e[1])); lens.append(e[2]); ep_pos.append(None)
        else:
            skel.append(('E',e[1])); lens.append(None); ep_pos.append(e[2])
    return skel,lens,ep_pos

# ---------- main ----------
if __name__=='__main__':
    check_sweeps()
    check_conjugation()

    print("\n(1) ENTRY [concrete, exact global config]:")
    entries={}
    for k in (21,23,27):
        e=entry(k)
        assert not e['halt'] and e['steps'] is not None, f"Z({k},3,0): no entry"
        assert e['m']==2, f"Z({k},3,0): entry m != 2"
        entries[k]=e
        print(f"  Z({k},3,0) --{e['steps']} steps--> exact C(2) at cell {e['pos']} "
              f"(new leftmost; all cells left unvisited=0), unsafe={e['unsafe']}")
        assert e['unsafe']==0

    print("\n(2) SMALL-m CHAIN [concrete, exact]: C(m) -> C(m+2), m=2..18:")
    for m in range(2,19):
        r=gen_trace(m,want_trace=False)
        assert not r['halt'] and r['m2']==m+2 and r['shift']==1, f"m={m}: {r}"
        assert r['unsafe']==0 and r['lo']>=-2 and r['hi']<=2*m+4, f"m={m}: bounds {r}"
        print(f"  C({m:>2}) -> C({m+2:>2}) shift=-1  steps={r['steps']:>3} (=4m+11: {r['steps']==4*m+11})"
              f"  span=[{r['lo']},{r['hi']}] (<= [-2,{2*m+4}])  unsafe=0  EXACT")

    print("\n(3) TEMPLATE LEMMA for m>=19 [certified trace-template method]:")
    grid=[19,20,21,22,23,24,25,26,27,50,51,100,101,250,251]
    results={}
    for m in grid:
        r=gen_trace(m)
        assert not r['halt'] and r['m2']==m+2 and r['shift']==1
        assert r['unsafe']==0 and r['lo']>=-2 and r['hi']<=2*m+4
        assert r['steps']==4*m+11, f"m={m}: steps {r['steps']} != 4m+11"
        skel,lens,ep_pos=skeleton(compress(r['trace']))
        results[m]=(skel,lens,ep_pos,r)
        n_sw=sum(1 for x in skel if x[0]=='SWEEP')
        print(f"  m={m:>4}: steps={r['steps']:>5}  span=[{r['lo']},{r['hi']}]  "
              f"skeleton={len(skel)} items ({n_sw} sweeps)  unsafe=0  -> C({m+2}) EXACT")

    # (3a) skeleton identity
    base=results[grid[0]][0]
    same=all(results[m][0]==base for m in grid)
    print(f"\n  (3a) compressed-trace SKELETON identical across the whole grid "
          f"(both parities, m=19..251): {same}")
    assert same

    # (3b) sweep lengths exactly affine in m
    idx_sweeps=[i for i,x in enumerate(base) if x[0]=='SWEEP']
    affine=True; coeffs=[]
    m0,m1=grid[0],grid[1]
    for i in idx_sweeps:
        y0=results[m0][1][i]; y1=results[m1][1][i]
        b=(y1-y0)//(m1-m0); a=y0-b*m0
        for m in grid:
            if results[m][1][i]!=a+b*m: affine=False; print(f"    sweep@{i}: NOT affine at m={m}")
        coeffs.append((i,a,b))
    print(f"  (3b) ALL sweep lengths exactly affine in m: {affine}   (a+b*m): {[(a,b) for _,a,b in coeffs]}")
    assert affine

    # (3c) episode-landmark pinning: every episode step at an m-independent offset from
    #      the LEFT edge (cell 0) or the RIGHT terminator (cell 2m+1)
    idx_eps=[i for i,x in enumerate(base) if x[0]=='E']
    pin_ok=True; max_off=0; pins=[]
    for i in idx_eps:
        left_offsets={results[m][2][i] for m in grid}            # pos (offset from cell 0)
        right_offsets={results[m][2][i]-(2*m+1) for m in grid}   # offset from cell 2m+1
        if len(left_offsets)==1:
            off=left_offsets.pop(); pins.append(('L',off)); max_off=max(max_off,abs(off))
        elif len(right_offsets)==1:
            off=right_offsets.pop(); pins.append(('R',off)); max_off=max(max_off,abs(off))
        else:
            pin_ok=False; print(f"    episode@{i}: NOT pinned (L={sorted(left_offsets)[:4]}..., "
                                f"R={sorted(right_offsets)[:4]}...)")
    nL=sum(1 for p in pins if p[0]=='L'); nR=sum(1 for p in pins if p[0]=='R')
    print(f"  (3c) EPISODE-LANDMARK PINNING: all {len(idx_eps)} episode steps pinned: {pin_ok} "
          f"({nL} to the left edge, {nR} to the right terminator; max |offset| = {max_off})")
    assert pin_ok

    # (3d) endpoint-exact spot checks at LARGE m
    print("  (3d) large-m endpoint-exact spot checks:")
    for m in (1000,1001,5000,5001,20000,20001,100000,100001):
        r=gen_trace(m,want_trace=False)
        assert not r['halt'] and r['m2']==m+2 and r['shift']==1 and r['unsafe']==0
        assert r['steps']==4*m+11 and r['lo']>=-2 and r['hi']<=2*m+4
        print(f"    m={m:>6}: C({m}) -> C({m+2}) shift=-1 in 4m+11={r['steps']} steps, "
              f"span=[{r['lo']},{r['hi']}], unsafe=0  EXACT")

    print("""
(4) INDUCTION / VERDICT:
  From (1), each Z(k,3,0), k in {21,23,27}, reaches the EXACT global config C(2) with no halt.
  From (2)+(3), C(m) -> C(m+2) (shift -1) exactly and halt-free for EVERY m>=2:
  m=2..18 concrete; m>=19 by the certified template (identical skeleton, affine sweeps,
  landmark-pinned episodes, proven sweep lemmas => symbolic reconstructibility => the
  first-divergence argument closes, red-team-corrected form) -- and the even-m instances
  (the only ones the orbit uses, m>=20) are ALSO inherited from the already-proven body
  lemma via the 1-step conjugation (0b). Hence the orbit is C(2) -> C(4) -> C(6) -> ...
  forever: a TRANSLATED BOUNCER (leftmost -1/generation, 4m+11 steps/generation =>
  steps to generation n from entry = 4n^2+15n => leftmost ~ sqrt(steps)/2).
  => Z(21,3,0), Z(23,3,0), Z(27,3,0) are NON-HALTING
     [PROVEN -- candidate, pending main-loop re-verification].
  These are STANDALONE configs; reachability from o4's initial tape is NOT claimed.
  o4 itself stays [OPEN]. No machine decided. No label upgraded.""")
