#!/usr/bin/env python3
"""dump exact raw tape at chosen milestones (head-relative) to fix standalone config forms."""
import sys
def parse(spec):
    M=[[None,None] for _ in range(6)]
    for k,blk in enumerate(spec.split('_')):
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[k][r]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,"ABCDEF".index(c[2]))
    return M
M=parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")

if __name__=='__main__':
    targets=set(int(x) for x in sys.argv[1:])
    SZ=1<<24
    tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; lo=hi=pos
    for step in range(max(targets)+1):
        if step in targets:
            s=''.join(str(tape[i]) for i in range(lo,hi+1))
            print(f"step {step}: state {'ABCDEF'[st]} head@{pos-off} lo={lo-off} hi={hi-off}")
            print(f"  tape[lo..hi] = {s}")
            print(f"  head offset from lo: {pos-lo}")
        r=tape[pos]; a=M[st][r]
        if a is None: break
        w,dd,ns=a
        tape[pos]=w; pos+=dd; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
