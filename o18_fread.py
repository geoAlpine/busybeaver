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
N=1<<25
tape=bytearray(N); off=N//2
pos=off; st=0; lo=pos; hi=pos
step=0; maxsteps=40_000_000
Fread0=0; Fread1=0
Finterior=[]   # F reads that are NOT at the current frontier
epoch=0
while step<maxsteps:
    r=tape[pos]
    if st==5:
        if r==1:
            print(">>> F reads 1 (HALT) at step",step,"pos",pos-off); break
        else:
            Fread0+=1
            if pos>lo:  # interior F-read (not at left frontier)
                Finterior.append((step,pos-off,'interior'))
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo: lo=pos
    if pos>hi: hi=pos
print(f"steps={step}")
print(f"F-reads of 0 (frontier or interior): {Fread0}")
print(f"interior F-reads (NOT at frontier): {len(Finterior)}")
for x in Finterior[:20]: print("  ",x)
