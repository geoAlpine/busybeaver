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
# Halt = state F reads 1. F is entered only from D-reads-1 (D:1->1LF). So halt <=> when D reads a 1,
# the cell to its LEFT is also 1 (F then reads it). Non-halt <=> EVERY 1 that D reads has a 0 to its left
# (D only reads the LEFT-END 1 of a run). Test this as a structural INVARIANT over the whole run.
SZ=1<<24; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; step=0; maxsteps=30_000_000
Dreads1=0; Dreads1_leftIs1=0
left_neighbor_when_D_reads1=[]
while step<maxsteps:
    r=tape[pos]
    if st==3 and r==1:  # D reads 1 -> goes to F; F will read pos-1
        Dreads1+=1
        leftcell=tape[pos-1]
        left_neighbor_when_D_reads1.append(leftcell)
        if leftcell==1: Dreads1_leftIs1+=1
    if st==5 and r==1:
        print("HALT",step); break
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
print(f"D-reads-1 events: {Dreads1}")
print(f"  of these, left neighbor == 1 (=> would halt): {Dreads1_leftIs1}")
print(f"  left neighbor == 0 (left-end 1, safe): {Dreads1 - Dreads1_leftIs1}")
print(f"\n=> INVARIANT 'D only reads left-end 1s (left neighbor 0)' holds for {Dreads1} events with {Dreads1_leftIs1} violations")
if Dreads1_leftIs1==0:
    print("   INVARIANT HOLDS empirically. Question: is it PROVABLE from the cycle structure?")
    print("   If yes => o18 decided NON-HALTING unconditionally (no equidistribution needed).")
