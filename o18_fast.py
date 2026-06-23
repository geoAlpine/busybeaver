# fast array-based o18 sim to find cleanliness breakdown / halt far out
def parse(spec):
    M=[]
    for st in spec.split('_'):
        ts=[st[i:i+3] for i in (0,3)]; row=[]
        for t in ts:
            if t[0]=='-' or t[2]=='Z': row.append(None)
            else: row.append((int(t[0]), t[1], 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M
spec="1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"
M=parse(spec)
N=1<<24
tape=bytearray(N)
off=N//2
pos=off; st=0; lo=pos; hi=pos
resets=[]
import sys
maxsteps=200_000_000
step=0
while step<maxsteps:
    r=tape[pos]
    if st==5 and r==1:
        print("HALT at step",step,"pos",pos-off); break
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo:
        lo=pos
        # check clean form: 0 then all 1 up to hi (state about to be F=5)
        if st==5:
            # scan from pos..hi
            seg=tape[pos:hi+1]
            width=hi-pos+1
            # clean iff seg[0]==0 and rest all 1
            clean = (seg[0]==0) and (1 not in seg[1:].translate(bytes.maketrans(b'\x01',b'\x00')))
            # simpler: count zeros in seg[1:]
            zeros = seg[1:].count(0)
            resets.append((step,width,zeros))
    if pos>hi: hi=pos
print("epochs reached:",len(resets))
for s,w,z in resets:
    print(f"  step={s:11d} width={w:8d} interior_zeros_after_frontier={z}")
