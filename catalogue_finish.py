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
MACHS=[
 ("Space Needle","1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"),
 ("o2","1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA"),
 ("o3","1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC"),
 ("o11","1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF"),
 ("o12","1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB"),
 ("o13","1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA"),
 ("o14","1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE"),
]
def analyze(spec,maxsteps=600000):
    M=parse(spec)
    tape={}; pos=0; st=0; lo=0; hi=0
    samples=[]; widths=[]
    sample_t=[8000,32000,128000,512000]
    # track max anomaly run (the "defect"): longest 0-run and longest 1-run excluding background
    defect_series=[]
    for step in range(maxsteps+1):
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        if step in sample_t:
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            runs=re.findall(r'0+|1+',s)
            comp=' '.join(f"{c[0]}^{len(c)}" for c in runs)
            samples.append((step,hi-lo+1,comp[:120]))
        if step>0 and step%2000==0:
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            mz=max((len(m.group()) for m in re.finditer(r'0{3,}',s)),default=0)
            mo=max((len(m.group()) for m in re.finditer(r'1{3,}',s)),default=0)
            defect_series.append((step,hi-lo+1,mz,mo))
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None: return ('HALT',step)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    # envelope: width at sample times -> doubling per 4x time => sqrt(t) (sawtooth) ; faster => geometric
    ws=[w for t,w,c in samples]
    env = "sqrt-t/sawtooth" if len(ws)>=2 and ws[-1]<ws[0]*5 else "geometric-ish"
    # defect peak growth: max defect over windows
    return samples, defect_series, env
for name,spec in MACHS:
    res=analyze(spec)
    if res[0]=='HALT':
        print(f"### {name}: HALT at {res[1]} !!"); continue
    samples,ds,env=res
    print(f"### {name}  envelope={env}")
    for t,w,c in samples:
        print(f"   t={t:7d} w={w:5d}  {c}")
    # defect peaks: sample max defect every ~10 windows
    peaks=[max(d[2],d[3]) for d in ds]
    # crude growth: peaks at quartiles
    n=len(peaks)
    qs=[peaks[i] for i in (n//8,n//4,n//2,3*n//4,n-1)] if n>8 else peaks
    print(f"   defect-max samples (growing?): {qs}")
    print()
