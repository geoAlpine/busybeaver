#!/usr/bin/env python3
"""
Independent re-derivation of o17 from the RAW TM (cell-for-cell), for the
template-class vs (K) verdict. Does NOT trust prior cryptid_map tags.

o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB   (halt = state F reads 0)

We test:
 (A) blank-tape orbit: halt predicate, odometer normal form, single-separator invariant,
     and the MARKER (top-digit) sequence of the ACTUAL blank orbit.
 (B) embedded left-frontier family C(k)=0^inf [A0] 1^k 0^inf : halt behaviour vs k mod 3.
 (C) whether the halt-deciding marker step (5->8) is a BOUNDED-LOCAL function
     (=> transport possible) or requires unbounded carry history (=> (K)).
"""
import re, sys

SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

def parse(spec):
    M=[]
    for st in spec.split('_'):
        row=[]
        for t in (st[0:3], st[3:6]):
            if t[0]=='-':
                row.append(None)
            else:
                row.append((int(t[0]), 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M

M = parse(SPEC)
STATES="ABCDEF"

def run_blank(maxsteps, sample_every=0, checkfn=None):
    """Run from all-blank tape, head state A. Return (halted, step, info)."""
    SZ = 1<<23
    tape = bytearray(SZ); off = SZ//2
    pos = off; st = 0; lo = hi = pos
    for step in range(maxsteps):
        r = tape[pos]
        if st==5 and r==0:            # F reads 0 -> HALT
            return True, step, (tape, lo, hi, off)
        cell = M[st][r]
        if cell is None:
            return True, step, (tape, lo, hi, off)  # any undefined = halt
        w,d,ns = cell
        tape[pos]=w; pos+=d; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        if sample_every and step%sample_every==0 and checkfn:
            checkfn(step, tape, lo, hi, pos, st)
    return False, maxsteps, (tape, lo, hi, off)

# ---------- (A) blank orbit: normal form + single separator + marker seq ----------
def blank_report(maxsteps):
    worst_sep=[0]; bad_blocks=[0]; checks=[0]
    marker_seq=[]  # (step, leading-block-length) sampled at milestones (head=A at left frontier)
    def chk(step, tape, lo, hi, pos, st):
        s=''.join(chr(48+tape[i]) for i in range(lo,hi+1)).strip('0')
        seps=re.findall(r'0+', s)
        msep=max((len(x) for x in seps),default=0)
        worst_sep[0]=max(worst_sep[0],msep)
        blocks=re.findall(r'1+', s)
        settled=blocks[:-1] if len(blocks)>1 else []
        bad=sum(1 for b in settled if len(b)%3!=2)
        bad_blocks[0]+=bad; checks[0]+=1
    halted,step,info=run_blank(maxsteps, sample_every=1_000_000, checkfn=chk)
    print(f"[A] blank orbit {maxsteps} steps: halted={halted} at {step}")
    print(f"    worst 0-separator ever seen (sampled) = {worst_sep[0]}  (1 => no 00 gap)")
    print(f"    settled-block mod3!=2 violations = {bad_blocks[0]} over {checks[0]} samples")
    return halted

# ---------- marker sequence of the blank orbit at every left-frontier A-milestone ----------
def blank_marker_sequence(maxsteps):
    """Milestone = state A reading the left-frontier 0 (pos == lo-ish, cell to right is 1).
       Record leading (marker) block length -> the top-digit automaton of the ACTUAL orbit."""
    SZ=1<<22; tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; lo=hi=pos
    seq=[]
    for step in range(maxsteps):
        r=tape[pos]
        if st==5 and r==0:
            seq.append((step,'HALT')); return seq, True
        # milestone detection: state A, reading 0, with a 1 to the right (left frontier of a block)
        if st==0 and r==0 and pos+1<=hi and tape[pos+1]==1:
            # is this the LEFT frontier? all cells left are blank
            if all(tape[i]==0 for i in range(lo,pos)):
                # measure leading block length
                L=0; i=pos+1
                while tape[i]==1: L+=1; i+=1
                seq.append((step,L))
        cell=M[st][r]
        if cell is None: seq.append((step,'HALT')); return seq, True
        w,d,ns=cell; tape[pos]=w; pos+=d; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return seq, False

# ---------- (B) embedded family C(k) ----------
def run_seed_block(k, maxsteps):
    """Seed 0^inf [A0] 1^k 0^inf : head state A on the 0 left of a k-block."""
    SZ=1<<22; tape=bytearray(SZ); off=SZ//2
    pos=off
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

if __name__=="__main__":
    mode = sys.argv[1] if len(sys.argv)>1 else "all"
    if mode in ("all","A"):
        blank_report(20_000_000)
    if mode in ("all","marker"):
        seq,halted = blank_marker_sequence(20_000_000)
        markers=[v for _,v in seq]
        print(f"\n[marker] blank orbit milestones: {len(seq)}, halted={halted}")
        print(f"    leading-block lengths (first 60): {markers[:60]}")
        from collections import Counter
        print(f"    distribution of marker lengths: {Counter(markers)}")
    if mode in ("all","B"):
        print("\n[B] embedded family C(k), maxsteps=5e6:")
        res={}
        for k in range(1,49):
            h,t=run_seed_block(k, 5_000_000)
            res[k]=(h,t)
        for r in range(3):
            ks=[k for k in range(1,49) if k%3==r]
            hs=[(k,res[k][1]) for k in ks if res[k][0]]
            nh=[k for k in ks if not res[k][0]]
            print(f"    k%3=={r}: halted {len(hs)}/{len(ks)}   nonhalt(<5e6): {nh}")
            print(f"        halt times: {hs}")
