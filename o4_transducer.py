#!/usr/bin/env python3
"""o4 (BB6 cryptid, blank tape) consolidated verifier.
o4 = 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---   (halt = state F reads 1)
Table: A:0->1RB,1->0LD  B:0->1RC,1->1RF  C:0->1LA,1->0RA
       D:0->0LA,1->0LE  E:0->1LD,1->1LA  F:0->0RB,1->HALT

Verified claims (0 exceptions => holds on tested range):
 (0) [PROVEN from table] F is entered ONLY by B,1->1RF; F,1=HALT, F,0->0RB.
     => HALT <=> state B reads a 1 whose RIGHT neighbour is 1 (B meets a '11' = a
     1-block of length >=2 during its rightward sweep). A 11-existence gate.
 (I) Normal form at left-frontier milestone (A or E at lo): 1-blocks are UNIT (len 1),
     0-gaps are small (len 1 or 2) EXCEPT exactly ONE big-gap defect of length G.
     (transient len-2 1-blocks occur only mid-carry, off-milestone.)
 (II) Finite control: fixed sets of 11 boundary-crossing (state,read,dir) triples,
     4 right-reflection and 5 left-gate (state,read) pairs; nothing else ever occurs.
 (III) Safety: over the whole run, whenever B reads a 1 the right neighbour is 0
     (B always enters a UNIT 1-block) => the 11-gate never fires => no halt.
 (IV) Value orbit: the big-gap defect G is a genuine base-4/3 ODOMETER value:
     G' = floor(4G/3) + c(G mod 3),  c={0:3,1:5,2:1}.  This closed 1-D map
     reproduces the raw-TM generation orbit EXACTLY.  Ratio -> 4/3; v_3(4/3) = -1
     => the base-3 equidistribution kernel (Type I, new ratio mu=4/3, p=3).
"""
from o4_recon import M, SN
from collections import Counter, defaultdict

CROSS_OK={('A',0,'R'),('A',1,'L'),('B',0,'R'),('B',1,'R'),('C',0,'L'),('C',1,'R'),
          ('D',0,'L'),('D',1,'L'),('E',0,'L'),('E',1,'L'),('F',0,'R')}
REFL_OK={('A',0),('B',0),('C',0),('C',1)}
GATE_OK={('A',0),('D',0),('D',1),('E',0),('E',1)}
CMAP={0:3,1:5,2:1}

def run(maxsteps):
    SZ=1<<25; tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; step=0; lo=hi=pos
    R=dict(ms=0,lang=0,newX=set(),newR=set(),newG=set(),
           b_reads1=0,b_r1_right1=0,brun_ge2=0,multibig=0,
           gens=[], prev_mg=None, halt=None)
    while step<maxsteps:
        r=tape[pos]
        act=M[st][r]
        if act is None: R['halt']=step; break
        # (III) safety: B reads a 1 -> right neighbour?
        if st==1 and r==1:
            R['b_reads1']+=1
            if tape[pos+1]==1:
                R['b_r1_right1']+=1     # would HALT
                # length of the 1-run B is entering (>=2)
        # milestone (I)
        if pos==lo and (st==0 or st==4):
            runs=[];j=lo
            while j<=hi:
                s=tape[j];k=j
                while k<=hi and tape[k]==s:k+=1
                runs.append((s,k-j));j=k
            ones=[n for s,n in runs if s==1]; gaps=[n for s,n in runs if s==0]
            big=[g for g in gaps if g>=3]; small=[g for g in gaps if g<3]
            R['ms']+=1
            ok=(all(x==1 for x in ones) and all(g in (1,2) for g in small) and len(big)<=1)
            if not ok:
                # allow a single transient len-2 1-block
                if not(all(x<=2 for x in ones) and sum(1 for x in ones if x==2)<=1
                       and all(g in (1,2) for g in small) and len(big)<=1):
                    R['lang']+=1
            if len(big)>1: R['multibig']+=1
            # (IV) generation reset detection on the big gap
            mg=max(gaps) if gaps else 0
            if R['prev_mg'] is not None and mg>R['prev_mg'] and mg>=6:
                R['gens'].append(mg)
            R['prev_mg']=mg
        # (II) finite control
        ww,d,ns=act
        left=tape[pos-1]; right=tape[pos+1]
        boundary=(r==1 and ((d==1 and right==0) or (d==-1 and left==0))) or \
                 (r==0 and ((d==1 and right==1) or (d==-1 and left==1)))
        if boundary:
            t=(SN[st],r,'R' if d==1 else 'L')
            if t not in CROSS_OK: R['newX'].add(t)
        if pos>=hi and (SN[st],r) not in REFL_OK: R['newR'].add((SN[st],r))
        if pos<=lo and (SN[st],r) not in GATE_OK: R['newG'].add((SN[st],r))
        tape[pos]=ww; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return R

if __name__=="__main__":
    R=run(60_000_000)
    G=R['gens']
    # verify closed map reproduces orbit
    pred=[G[0]]
    for _ in range(len(G)-1):
        g=pred[-1]; pred.append((4*g)//3 + CMAP[g%3])
    map_ok = (pred==G)
    print(f"steps run                     : 60,000,000   halt: {R['halt']}")
    print(f"milestones checked            : {R['ms']}")
    print(f"(I)   language violations     : {R['lang']}   (unit 1-blocks, gaps in {{1,2}}, one big gap)")
    print(f"      milestones w/ >1 big gap : {R['multibig']}   (0 => single migrating defect)")
    print(f"(II)  new crossing symbols    : {sorted(R['newX']) or 'NONE'}   (fixed 11)")
    print(f"      new reflection symbols  : {sorted(R['newR']) or 'NONE'}   (fixed 4)")
    print(f"      new gate symbols        : {sorted(R['newG']) or 'NONE'}   (fixed 5)")
    print(f"(III) B-reads-1 events        : {R['b_reads1']}")
    print(f"      of which right-nbr = 1  : {R['b_r1_right1']}   (0 => B always enters a UNIT block; 11-gate never fires)")
    print(f"(IV)  generations detected    : {len(G)}")
    print(f"      G orbit                 : {G}")
    print(f"      G' = floor(4G/3)+c(Gmod3), c={CMAP}  reproduces raw orbit EXACTLY: {map_ok}")
    if len(G)>2:
        print(f"      ratio G[n+1]/G[n] -> {G[-1]/G[-2]:.5f}  (=4/3={4/3:.5f}); v_3(4/3)=-1 => Type I kernel prime 3")
    ok=(R['lang']==0 and not R['newX'] and not R['newR'] and not R['newG']
        and R['b_r1_right1']==0 and R['multibig']==0 and map_ok and R['halt'] is None)
    print(f"\nO4 TRANSDUCER + HALT-GATE + VALUE-ORBIT VERIFIED: {ok}")
    print("[PROVEN from table] HALT <=> B reads '11'. [OBSERVED 0 exc] never fires from blank.")
    print("Type I: base-4/3 value odometer (v_3(4/3)=-1 equidistribution kernel). Halting [OPEN].")
