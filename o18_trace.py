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
# Record EVERY time state F (idx5) reads a cell at the left frontier: was it 0 or 1?
# Also record the full left-frontier history to see how close to a '1' the F-read gets.
def run(maxsteps):
    tape={}; pos=0; st=0; lo=0; hi=0
    Freads=[]  # (step, cellpos, value_read, is_frontier)
    for step in range(maxsteps+1):
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        r=tape.get(pos,0)
        if st==5:  # state F about to read
            Freads.append((step,pos,r, pos<=lo))
        tr=M[st][r]
        if tr is None:
            return ('HALT',step,pos,Freads)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
    return ('RUN',maxsteps,None,Freads)
tag,last,hp,Fr=run(500000)
print("status",tag,"at",last)
# Among F-reads, find those at frontier and what value. Group by which 'epoch'.
# Show all F-reads with value 1 (these are halts) and the frontier F-reads.
frontier=[(s,p,v) for s,p,v,f in Fr if f]
print(f"total F-reads={len(Fr)}, frontier F-reads={len(frontier)}")
print("frontier F-reads (step,pos,value) -- value must always be 0 for non-halt:")
for s,p,v in frontier[:30]:
    print(f"  step={s:7d} pos={p:5d} read={v}")
ones=[x for x in Fr if x[2]==1]
print("ANY F-read==1 (=halt trigger)?", len(ones), ones[:5])
