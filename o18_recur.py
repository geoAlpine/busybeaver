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
N=1<<25
tape=bytearray(N); off=N//2
pos=off; st=0; lo=pos; hi=pos
configs=[]
step=0; maxsteps=200_000_000
while step<maxsteps:
    r=tape[pos]
    if st==5 and r==1:
        print("HALT",step); break
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo:
        lo=pos
        if st==5:
            seg=bytes(tape[pos:hi+1])
            s=seg.decode('latin1')
            s=''.join(chr(48+b) for b in seg)
            rle=re.findall(r'0+|1+',s)
            comp=[(c[0],len(c)) for c in rle]
            configs.append((step,comp))
            if len(configs)>=10: break
    if pos>hi: hi=pos
print("captured",len(configs),"epoch configs (full RLE):")
for step,comp in configs:
    width=sum(l for _,l in comp)
    # represent compactly: show non-trivial blocks (len>=2 or the structure)
    rep=' '.join(f"{c}{l}" for c,l in comp)
    # find interior-zero defects: a '0' block of len>=1 that is NOT the leading sep and breaks a 1-run
    print(f"step={step:11d} w={width:7d} blocks={len(comp)}")
    print(f"   {rep[:140]}")
