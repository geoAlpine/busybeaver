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
import re
SZ=1<<27
tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=pos; hi=pos
step=0; maxsteps=900_000_000
epochs=[]
interiorF=[]
while step<maxsteps:
    r=tape[pos]
    if st==5:
        if r==1:
            print(">>> HALT F-read-1 at step",step); break
        if pos>lo:
            interiorF.append((len(epochs),step,pos-off,r))
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo:
        lo=pos
        if st==5:
            seg=tape[pos:hi+1]
            zeros_interior = seg[1:].count(0)
            width=hi-pos+1
            epochs.append((step,width,zeros_interior))
    if pos>hi: hi=pos
print(f"reached step={step}, epochs={len(epochs)}")
for i,(s,w,z) in enumerate(epochs):
    mark = " <-- DEFECT" if z>0 else ""
    print(f"  epoch {i:2d}: width={w:9d} interior_zeros={z}{mark}")
print(f"\ninterior F-reads: {len(interiorF)}")
for e,s,p,r in interiorF: print(f"  epoch {e}: step={s} pos={p} read={r}")
# base-3 of widths at defect epochs vs clean
def b3(n):
    d=[]
    while n: d.append(n%3); n//=3
    return ''.join(str(x) for x in reversed(d)) or '0'
print("\nwidth base-3 (N_k) and predecessor:")
for i,(s,w,z) in enumerate(epochs):
    print(f"  e{i:2d} N={w:9d} b3={b3(w):20s} z={z}")
