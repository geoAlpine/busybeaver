def parse(spec):
    M=[]
    for st in spec.split('_'):
        ts=[st[i:i+3] for i in (0,3)]; row=[]
        for t in ts:
            if t[0]=='-' or t[2]=='Z': row.append(None)
            else: row.append((int(t[0]), t[1], 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M
spec="1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"
M=parse(spec)
# Which transition halts? state A (idx0) read 1 -> '---'
print("halt transition: state A reading 1")
import re
SZ=1<<24; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=pos; hi=pos
step=0; maxsteps=50_000_000
# observe structure: sample tape RLE at geometric times, and track extremes/state visits
samples_t={8000,32000,128000,512000,2000000,8000000}
configs=[]
# track when head reaches a NEW right frontier (extends right) in some state -> milestone candidate
milestones=[]
prevhi=hi
Areads=[]
while step<maxsteps:
    r=tape[pos]
    if st==0:  # state A about to read
        if r==1:
            print(">>> HALT (A reads 1) at step",step); break
        Areads.append((step,pos-off,r,pos>=hi))
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos>hi:
        hi=pos
        # milestone: new right frontier reached, record state + compact config
        milestones.append((step,ns,hi-lo+1))
    if pos<lo: lo=pos
    if step in samples_t:
        s=''.join(chr(48+tape[i]) for i in range(lo,hi+1))
        rle=re.findall(r'0+|1+',s)
        comp=' '.join(f"{c[0]}^{len(c)}" for c in rle)
        configs.append((step,hi-lo+1,comp[:150]))
print(f"steps={step}")
print("samples:")
for s,w,c in configs:
    print(f" t={s:8d} w={w:6d} {c}")
print(f"\nA-reads total={len(Areads)}, A-reads of 1 (halt)= {sum(1 for x in Areads if x[2]==1)}")
print(f"A-reads at right-frontier: {sum(1 for x in Areads if x[3])}/{len(Areads)}")
