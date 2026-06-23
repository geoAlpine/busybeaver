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
# Track the max 0-run length over time at fine resolution; detect epoch peaks.
def track(maxsteps):
    tape={}; pos=0; st=0
    series=[]
    for step in range(maxsteps+1):
        if step % 500 == 0:
            lo=min(tape) if tape else 0; hi=max(tape) if tape else 0
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            zr=[ (len(m.group()),m.start()+lo) for m in re.finditer(r'0{3,}',s)]
            maxz=max(zr) if zr else (0,0)
            series.append((step,maxz[0],maxz[1]))
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None: return ('HALT',step)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    return series
s=track(300000)
if s[0]=='HALT': print("HALT",s)
else:
    # find local maxima (epoch peaks): where 0-run jumps up after being small
    prev=0
    peaks=[]
    for step,L,p in s:
        if L>prev+3 and prev<6:  # jumped up from near-zero = new epoch
            peaks.append((step,L,p))
        prev=L
    print("epoch peaks (step, 0-run length, position):")
    for pk in peaks: print(" ",pk)
    print("\npeak lengths:", [pk[1] for pk in peaks])
    print("peak positions:", [pk[2] for pk in peaks])
