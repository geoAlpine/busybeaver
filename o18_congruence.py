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
SZ=1<<26; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=pos; hi=pos
step=0; maxsteps=30_000_000
Freads=[]
while step<maxsteps:
    r=tape[pos]
    if st==5:  # state F reading
        Freads.append((step, pos-off, r, pos-off>=hi-off-1))  # (step, position, value, is-frontier)
        if r==1: print("HALT",step); break
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo: lo=pos
    if pos>hi: hi=pos
print(f"all F-reads up to step {step}: (step, position, value, frontier?)")
for s,p,v,f in Freads:
    print(f"  step={s:9d} pos={p:6d} read={v} {'FRONTIER' if f else 'INTERIOR'}  pos%2={p%2} pos%3={p%3}")
# the interior reads are the halt-relevant ones. Check their position residues.
interior=[(s,p,v) for s,p,v,f in Freads if not f]
print(f"\ninterior F-reads: {len(interior)}")
for s,p,v in interior:
    print(f"  pos={p}: pos%2={p%2}, pos%3={p%3}, value read={v}")
# Frontier reads (always 0): their positions
fr=[(p) for s,p,v,f in Freads if f]
print(f"\nfrontier F-read positions (parities): {[(p,p%2) for p in fr]}")
