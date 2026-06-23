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
def track(maxsteps):
    tape={}; pos=0; st=0; lo=0; hi=0
    peaks=[]; lastmax=0; rising=False
    for step in range(maxsteps+1):
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        if step % 200 == 0:
            s=''.join(str(tape.get(i,0)) for i in range(lo,hi+1))
            mx=0
            for m in re.finditer(r'0{2,}',s):
                if len(m.group())>mx: mx=len(m.group())
            # detect a fresh peak: big jump up from a small value
            if mx>lastmax+20 and lastmax<30:
                peaks.append((step,mx))
            lastmax=mx
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None: return ('HALT',step)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    return peaks
p=track(3000000)
if p[0]=='HALT': print("HALT",p)
else:
    vals=[v for s,v in p]
    print("epoch peaks:", vals)
    print("ratios:", [round(vals[i+1]/vals[i],4) for i in range(len(vals)-1)])
