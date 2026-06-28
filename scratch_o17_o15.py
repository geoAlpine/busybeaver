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
O15="1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"   # halt = A reads 1

def run(spec, init_cells=None, init_state=0, init_pos=None, maxsteps=5_000_000,
        halt_state=5, halt_sym=0, SZbits=22):
    """Generic sim. init_cells: dict offset->sym placed around start. Returns (halted, step, lo,hi,tape,off)."""
    M=parse(spec)
    SZ=1<<SZbits; tape=bytearray(SZ); off=SZ//2
    if init_cells:
        for k,v in init_cells.items():
            tape[off+k]=v
    pos=off+(init_pos if init_pos is not None else 0); st=init_state
    lo=hi=pos
    step=0
    while step<maxsteps:
        r=tape[pos]
        if st==halt_state and r==halt_sym:
            return True, step, lo,hi,tape,off
        cell=M[st][r]
        if cell is None:
            return True, step, lo,hi,tape,off
        w,_,d,ns=cell
        tape[pos]=w; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return False, step, lo,hi,tape,off

# ---------------- PART A: o17 from blank, decode odometer ----------------
def decode_o17(s):
    """s = tape string. settled (non-last) 1-blocks length L -> digit (L-2)/3 if L%3==2."""
    s2=s.strip('0')
    blocks=re.findall(r'1+', s2)
    if len(blocks)<1: return None
    settled=blocks[:-1]
    digits=[]
    ok=True
    for b in settled:
        L=len(b)
        if L%3==2: digits.append((L-2)//3)
        else: ok=False; digits.append(('?',L))
    active=len(blocks[-1])
    return digits, active, ok

print("="*70)
print("PART A1: o17 from blank — width vs steps, decode odometer, growth law")
print("="*70)
M=parse(O17)
SZ=1<<23; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=hi=pos; step=0
maxsteps=30_000_000
# sample at geometric times
sample_times=sorted(set(int(10**(i/4)) for i in range(8,30)))
si=0
prev_digits=None
macro=[]  # (step,width,decoded value)
last_val=None
while step<maxsteps:
    r=tape[pos]
    if st==5 and r==0:
        print("HALT at",step); break
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo: lo=pos
    if pos>hi: hi=pos
    if si<len(sample_times) and step>=sample_times[si]:
        s=''.join(chr(48+tape[i]) for i in range(lo,hi+1))
        dec=decode_o17(s)
        width=hi-lo+1
        if dec:
            digits,active,ok=dec
            val=sum(dd*(3**i) for i,dd in enumerate(digits) if isinstance(dd,int)) if ok else None
            print(f" t={step:9d} w={width:5d} settled_digits(lsb->msb)={digits[:12]} active={active} val={val}")
        si+=1
# final structure
s=''.join(chr(48+tape[i]) for i in range(lo,hi+1))
rle=re.findall(r'0+|1+',s)
print("final RLE (first 40 runs):", ' '.join(f"{c[0]}^{len(c)}" for c in rle[:40]))

# ---------------- PART A2: o17 — is increment +1 (pure odometer) or geometric? ----------------
print()
print("="*70)
print("PART A2: o17 — track decoded VALUE over macro-steps to get increment law")
print("="*70)
M=parse(O17)
SZ=1<<22; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=hi=pos; step=0
vals=[]
last_active=-1
last_recorded=None
step_cap=3_000_000
while step<step_cap:
    r=tape[pos]
    if st==5 and r==0: break
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo: lo=pos
    if pos>hi: hi=pos
    # record value whenever head returns to right frontier in state... sample sparsely
    if step%5000==0:
        s=''.join(chr(48+tape[i]) for i in range(lo,hi+1))
        dec=decode_o17(s)
        if dec:
            digits,active,ok=dec
            if ok:
                val=sum(dd*(3**i) for i,dd in enumerate(digits))
                # incorporate active block as least-significant partial digit
                full=val
                if last_recorded is None or full!=last_recorded:
                    vals.append((step,full,active))
                    last_recorded=full
print("decoded settled-value samples (step, settled_val, active_len):")
for x in vals[:25]: print("  ",x)
if len(vals)>3:
    seq=[v for _,v,_ in vals if v>0]
    print("settled-value sequence:",seq[:25])
    diffs=[seq[i+1]-seq[i] for i in range(len(seq)-1)]
    print("consecutive diffs:",diffs[:24])

sys.stdout.flush()
