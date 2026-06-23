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
    series=[]
    for step in range(maxsteps+1):
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        if step % 1000 == 0:
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            # leading 1-block length
            m=re.match(r'1+',s)
            klead=len(m.group()) if m else 0
            # any anomaly in interior (10)* region: 0-run>=2 (besides the 0^2 separator) or 1-run>=2
            interior=s[klead:]
            anos=[(mm.group()[0],len(mm.group()),mm.start()) for mm in re.finditer(r'0{2,}|1{2,}',interior)]
            series.append((step,klead,hi-lo+1,anos))
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None: return ('HALT',step)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    return series
s=track(2000000)
if s[0]=='HALT': print("HALT",s)
else:
    # print where klead changes, and any interior anomalies
    print("step, klead, width, #interior-anomalies (excluding none):")
    prevk=None
    for step,k,w,anos in s:
        extra=[a for a in anos]
        if k!=prevk or extra:
            tag=' '.join(f"{c}^{l}@{p}" for c,l,p in extra[:6])
            print(f"t={step:8d} k={k:3d} w={w:5d}  {tag}")
            prevk=k
