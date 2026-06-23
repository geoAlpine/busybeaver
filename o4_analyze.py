import re
def parse(spec):
    M=[]
    for st in spec.split('_'):
        ts=[st[i:i+3] for i in (0,3)]
        row=[]
        for t in ts:
            if t[0]=='-' or t[2]=='Z': row.append(None)
            else: row.append((int(t[0]), t[1], ord(t[2])-ord('A')))
        M.append(row)
    return M
spec="1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---"
M=parse(spec)
def snapshot(maxsteps, sample_at):
    tape={}; pos=0; st=0; out=[]; targets=sorted(sample_at); ti=0
    for step in range(maxsteps+1):
        if ti<len(targets) and step==targets[ti]:
            lo=min(tape) if tape else 0; hi=max(tape) if tape else 0
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            out.append((step,pos-lo,st,lo,hi,s)); ti+=1
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None: out.append(('HALT',step)); break
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    return out
sa=[1000,2000,4000,8000,16000,32000,64000,128000]
for rec in snapshot(200000, sa):
    if rec[0]=='HALT': print("HALT at",rec[1]); break
    step,head,st,lo,hi,s=rec
    runs=re.findall(r'0+|1+',s)
    comp=' '.join(f"{c[0]}^{len(c)}" for c in runs)
    print(f"t={step:7d} st={chr(65+st)} head@{head} width={hi-lo+1}")
    print(f"   {comp[:220]}")
