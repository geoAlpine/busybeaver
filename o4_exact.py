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
# Exact: at every step compute max 0-run; record true epoch peaks (run hits local max then collapses).
def track(maxsteps):
    tape={}; pos=0; st=0
    lo=0; hi=0
    series=[]
    for step in range(maxsteps+1):
        # cheap incremental extent
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        if step % 100 == 0:
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            mx=0
            for m in re.finditer(r'0{2,}',s):
                if len(m.group())>mx: mx=len(m.group())
            series.append((step,mx))
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None: return ('HALT',step)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    return series
s=track(260000)
if s[0]=='HALT': print("HALT",s)
else:
    # true peaks: value greater than both neighbors and > 10
    peaks=[]
    for i in range(1,len(s)-1):
        if s[i][1]>=s[i-1][1] and s[i][1]>s[i+1][1] and s[i][1]>10:
            peaks.append(s[i])
    # collapse adjacent equal peaks
    seq=[p[1] for p in peaks]
    print("true epoch peak 0-run lengths:")
    print(seq)
