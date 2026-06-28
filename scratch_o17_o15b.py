import re, sys

def parse(spec):
    M=[]
    for st in spec.split('_'):
        ts=[st[i:i+3] for i in (0,3)]; row=[]
        for t in ts:
            if t[0]=='-' or t[2]=='Z': row.append(None)
            else: row.append((int(t[0]), t[1], 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M

O17="1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"   # halt = F reads 0

# ---------- PART B: embedded family 0 A 0 1^k ----------
# find the config interpretation reproducing k=6 -> halt at 206 (per o17_attack.md)
def sim_from(spec, cells, start_off, start_state, maxsteps, halt_state=5, halt_sym=0):
    M=parse(spec)
    SZ=1<<22; tape=bytearray(SZ); off=SZ//2
    for k,v in cells.items(): tape[off+k]=v
    pos=off+start_off; st=start_state; step=0
    lo=hi=pos
    while step<maxsteps:
        r=tape[pos]
        if st==halt_state and r==halt_sym:
            return ('HALT',step)
        cell=M[st][r]
        if cell is None: return ('HALT',step)
        w,_,d,ns=cell
        tape[pos]=w; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return ('NOHALT',step)

print("Calibrate embedded-family config against anchor k=6 -> HALT at 206:")
# interpretation: head state A at position 0 reading 0; cell -1 =0(blank); cells +1.. = 1^k ; with a 0 separator?
# try several layouts
def layout_A(k):  # 0(blank left) [A:0] 1^k   (A reads a 0 with k ones to right)
    return {i+1:1 for i in range(k)}
def layout_B(k):  # [A:0] 0 1^k  (A on 0, then 0, then 1^k)
    c={1:0};
    for i in range(k): c[2+i]=1
    return c
def layout_C(k):  # 0 [A:0] 0 1^k with explicit left 0 too
    c={-1:0,1:0}
    for i in range(k): c[2+i]=1
    return c
for name,lay in [('A',layout_A),('B',layout_B),('C',layout_C)]:
    r=sim_from(O17, lay(6), 0, 0, 2_000_000)
    print(f"  layout {name}: k=6 -> {r}")

# pick the layout matching 206; if none, scan
print()
chosen=None
for name,lay in [('A',layout_A),('B',layout_B),('C',layout_C)]:
    r=sim_from(O17, lay(6), 0, 0, 2_000_000)
    if r[0]=='HALT' and r[1]==206:
        chosen=(name,lay); print(f"  -> using layout {name} (matches 206)")
        break
if chosen is None:
    # try with start one cell right (A reading the first 1?) or other anchors; just report all k for layout A
    print("  no exact 206 match; defaulting to layout A and reporting full table")
    chosen=('A',layout_A)

name,lay=chosen
print()
print(f"Embedded family 0A01^k (layout {name}), k=1..60, budget 5e6:")
BUD=5_000_000
res={}
for k in range(1,61):
    r=sim_from(O17, lay(k), 0, 0, BUD)
    res[k]=r
    tag = f"HALT@{r[1]}" if r[0]=='HALT' else f"NOHALT(>{BUD})"
    print(f"  k={k:3d} (k%3={k%3}): {tag}")

print()
print("Summary by residue:")
for rclass in (0,1,2):
    ks=[k for k in res if k%3==rclass]
    halted=[k for k in ks if res[k][0]=='HALT']
    print(f"  k%3=={rclass}: halted {len(halted)}/{len(ks)} -> {halted}")
print("k%3==0 halters with times:", {k:res[k][1] for k in res if k%3==0 and res[k][0]=='HALT'})

sys.stdout.flush()
