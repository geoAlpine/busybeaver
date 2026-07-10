#!/usr/bin/env python3
"""Test the non-halt invariant:
HALT <=> rightward scanner enters a maximal 0-run of length exactly 3.
(A) record length of every maximal 0-run the E-scanner ENTERS (E reads a 0 that is the
    left boundary of a run) -> claim all even.
(B) periodically scan the WHOLE tape [lo,hi] for ANY maximal 0-run of length 3 (odd).
Also cross-check halt char by a mutant with a planted length-3 gap."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC="1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"

def run(maxsteps, SZ=1<<25, scan_every=200000):
    M=parse(SPEC); tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; step=0; lo=hi=pos
    entered_runlens={}   # run length entered by scanner (E at left boundary) -> count
    odd_entered=[]
    global_len3_events=[]   # (step, count of len-3 internal 0-runs)
    all_run_parity_bad=[]   # any odd internal run anywhere
    prev_pos=pos
    while step<maxsteps:
        r=tape[pos]
        # detect E entering a 0-run at its left boundary: state E, reads 0, and left neighbor is 1
        if st==4 and r==0 and pos>lo and tape[pos-1]==1:
            j=pos; z=0
            while j<=hi and tape[j]==0: z+=1; j+=1
            entered_runlens[z]=entered_runlens.get(z,0)+1
            if z%2==1:
                odd_entered.append((step,z,pos-off))
                if z==3:
                    pass # would halt path
        if st==1 and r==1:
            print(f"*** HALT at step {step} ***"); return entered_runlens,odd_entered,global_len3_events
        act=M[st][r]
        if act is None:
            print(f"HALT(other) step {step}"); return entered_runlens,odd_entered,global_len3_events
        ww,d,ns=act; tape[pos]=ww; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        elif pos>hi: hi=pos
        if step%scan_every==0:
            # scan whole tape for internal maximal 0-runs (bounded by 1 on both sides)
            i=lo; n3=0; odd=0
            while i<=hi:
                if tape[i]==0:
                    j=i
                    while j<=hi and tape[j]==0: j+=1
                    L=j-i
                    # internal iff bounded by 1s (i>lo-ish and j<=hi)
                    if i>lo and j<=hi and tape[i-1]==1 and tape[j]==1:
                        if L==3: n3+=1
                        if L%2==1: odd+=1
                    i=j
                else: i+=1
            if n3: global_len3_events.append((step,n3))
            if odd: all_run_parity_bad.append((step,odd))
    return entered_runlens,odd_entered,global_len3_events,all_run_parity_bad

if __name__=="__main__":
    cap=int(sys.argv[1]) if len(sys.argv)>1 else 30_000_000
    res=run(cap)
    entered,odd,g3=res[0],res[1],res[2]
    print("Entered-by-scanner maximal 0-run lengths (E at left boundary):")
    for k in sorted(entered): print(f"  len={k}: {entered[k]:,}  ({'ODD' if k%2 else 'even'})")
    print(f"ODD-length runs ENTERED by scanner: {len(odd)}  (any len-3 => HALT). examples: {odd[:5]}")
    print(f"Global tape scans finding a len-3 internal 0-run: {len(g3)} events. {g3[:5]}")
    if len(res)>3:
        print(f"Global scans finding ANY odd internal 0-run: {len(res[3])}. {res[3][:5]}")
