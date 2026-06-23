import re
def parse(spec):
    M=[]
    for st in spec.split('_'):
        ts=[st[i:i+3] for i in (0,3)]; row=[]
        for t in ts:
            if t[0]=='-' or t[2]=='Z': row.append(None)
            else: row.append((int(t[0]), t[1], ord(t[2])-ord('A')))
        M.append(row)
    return M
spec="1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE"
M=parse(spec)
def track(maxsteps):
    tape={}; pos=0; st=0; lo=0; hi=0
    peaks=[]; lastmax=0
    samples=[]
    for step in range(maxsteps+1):
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        if step % 200 == 0:
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            # find dominant anomaly: longest 0-run and longest 1-run
            mz=max((len(m.group()) for m in re.finditer(r'0{2,}',s)),default=0)
            mo=max((len(m.group()) for m in re.finditer(r'1{2,}',s)),default=0)
            if step in (2000,8000,32000,128000,512000):
                runs=re.findall(r'0+|1+',s)
                comp=' '.join(f"{c[0]}^{len(c)}" for c in runs)
                samples.append((step,hi-lo+1,comp[:160]))
            if mz>lastmax+20 and lastmax<30:
                peaks.append((step,mz))
            lastmax=mz
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None: return ('HALT',step,None)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    return peaks,samples
res=track(2000000)
if res[0]=='HALT': print("HALT",res)
else:
    peaks,samples=res
    print("=== o16 tape samples ===")
    for step,w,comp in samples:
        print(f"t={step:7d} width={w}\n   {comp}")
    vals=[v for s,v in peaks]
    print("\n0-run epoch peaks:", vals[:30])
    if len(vals)>3:
        print("ratios:", [round(vals[i+1]/vals[i],3) for i in range(min(12,len(vals)-1))])
