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
spec="1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---"
M=parse(spec)
# Find anomalies: the steady background is "10" repeating. Defects = deviations.
# Detect: long 0-runs (>=2) and long 1-runs (>=2), record (position_in_runs, length).
def anomalies(maxsteps, sample_at):
    tape={}; pos=0; st=0; targets=sorted(sample_at); ti=0; res=[]
    for step in range(maxsteps+1):
        if ti<len(targets) and step==targets[ti]:
            lo=min(tape) if tape else 0; hi=max(tape) if tape else 0
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            # list anomalous runs with their left-coordinate (relative to lo)
            anos=[]
            for m in re.finditer(r'0{2,}|1{2,}',s):
                anos.append((m.group()[0], len(m.group()), m.start()+lo))
            res.append((step,st,lo,hi,pos,anos)); ti+=1
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None: res.append(('HALT',step,pos)); break
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    return res
sa=[2**k*1000 for k in range(8)]
prev=None
for rec in anomalies(300000, sa):
    if rec[0]=='HALT': print("HALT",rec); break
    step,st,lo,hi,pos,anos=rec
    print(f"t={step:7d} st={chr(65+st)} head@{pos} [{lo},{hi}] width={hi-lo+1}")
    for ch,ln,p in anos:
        print(f"     {ch}^{ln} @abs{p}")
