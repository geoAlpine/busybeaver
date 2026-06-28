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

O17="1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"
O15="1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"

def sim_from(spec, cells, start_off, start_state, maxsteps, halt_state=5, halt_sym=0):
    M=parse(spec)
    SZ=1<<23; tape=bytearray(SZ); off=SZ//2
    for k,v in cells.items(): tape[off+k]=v
    pos=off+start_off; st=start_state; step=0
    lo=hi=pos
    while step<maxsteps:
        r=tape[pos]
        if st==halt_state and r==halt_sym: return ('HALT',step)
        cell=M[st][r]
        if cell is None: return ('HALT',step)
        w,_,d,ns=cell; tape[pos]=w; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return ('NOHALT',step)

def layout_A(k): return {i+1:1 for i in range(k)}

# (1) push apparent non-halters of k%3==0 to bigger budget
print("="*70)
print("(1) o17 embedded family: push k%3==0 apparent non-halters to 2e8")
print("="*70)
for k in [3,9,18,27,33,39,42,48,54,60,63,66,69,72,75]:
    r=sim_from(O17, layout_A(k), 0, 0, 30_000_000)
    print(f"  k={k:3d}: {r[0]}@{r[1]}")
sys.stdout.flush()

# (3) Reduce k=3j subfamily: relation between k (halt) and halt time, and the j-pattern
print()
print("="*70)
print("(3) o17 k=3j halting pattern, j=1..40 (budget 5e7)")
print("="*70)
jhalt=[]
for j in range(1,41):
    k=3*j
    r=sim_from(O17, layout_A(k), 0, 0, 10_000_000)
    jhalt.append((j,k,r[0],r[1]))
    print(f"  j={j:2d} k={k:3d}: {r[0]}@{r[1]}")
halters_j=[j for j,k,s,t in jhalt if s=='HALT']
nonh_j=[j for j,k,s,t in jhalt if s!='HALT']
print("halter j:",halters_j)
print("nonhalter j:",nonh_j)
sys.stdout.flush()

# (5) subword complexity of o17 SETTLED-DIGIT string from blank at a large time
print()
print("="*70)
print("(5) o17 settled-digit string subword complexity (decidability signal)")
print("="*70)
M=parse(O17); SZ=1<<23; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=hi=pos; step=0
while step<20_000_000:
    r=tape[pos]
    if st==5 and r==0: break
    w,_,d,ns=M[st][r]; tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo: lo=pos
    if pos>hi: hi=pos
s=''.join(chr(48+tape[i]) for i in range(lo,hi+1)).strip('0')
blocks=re.findall(r'1+', s)
settled=blocks[:-1]
# digit string from settled blocks (length%3 -> digit). keep only those ==2 mod3; mark others
digstr=[]
for b in settled:
    L=len(b)
    digstr.append(str((L-2)//3) if L%3==2 else 'X')
digstr=''.join(d for d in digstr if d!='X')  # the clean base-3 digits
print(f"#settled blocks={len(settled)}, clean-digit length={len(digstr)}")
print("digit string (lsb..) first 120:", digstr[:120])
# subword complexity p(L)
for L in range(1,9):
    subs=set(digstr[i:i+L] for i in range(len(digstr)-L+1))
    print(f"  p({L}) = {len(subs)} distinct length-{L} factors (alphabet up to 3^{L}={3**L})")
# distribution of digits
from collections import Counter
print("digit freq:",Counter(digstr))
sys.stdout.flush()
