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
spec="1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"
M=parse(spec)
# Run, capture full tape configs at the "milestone" (head at left frontier in a specific state).
# First just observe the orbit: record (step, state, head, leftmost-1 pos, tape value as int).
def run(maxsteps):
    tape={}; pos=0; st=0; lo=0; hi=0
    events=[]
    for step in range(maxsteps+1):
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None:
            return ('HALT',step,pos,st)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
        # milestone: when head reaches a new leftmost cell (extends left) -- the left frontier
        if pos<lo:
            # snapshot
            s=''.join(str(tape.get(i,0)) for i in range(pos,hi+1))
            events.append((step,ns,pos,hi,s))
    return events
ev=run(400000)
if ev[0]=='HALT':
    print("HALT",ev)
else:
    # show left-frontier-extension milestones: the number encoded and its base-3 form
    print("left-frontier extension milestones (step,state,leftpos,width,tape):")
    prev=None
    for step,st,lp,hi,s in ev[:40]:
        # interpret tape as binary number (value) ignoring leading structure
        val=int(s.replace('','') or '0',2) if set(s)<=set('01') else None
        runs=re.findall(r'0+|1+',s)
        comp=''.join(f"{c[0]}^{len(c)} " for c in runs)
        print(f" t={step:7d} st={chr(65+st)} L={lp:5d} w={hi-lp+1:4d} {comp[:80]}")
