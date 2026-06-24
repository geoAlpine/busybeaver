import re
def parse(spec):
    M=[]
    for st in spec.split('_'):
        ts=[st[i:i+3] for i in (0,3)]; row=[]
        for t in ts:
            if t[0]=='-' or t[2]=='Z': row.append(None)
            else: row.append((int(t[0]), t[1], 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M
spec="1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"
M=parse(spec)
SZ=1<<22; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=pos; hi=pos
step=0; maxsteps=20_000_000
worst_sep=0; bad_blocks=0; checks=0; halted=False
while step<maxsteps:
    r=tape[pos]
    if st==5 and r==0:   # F reads 0 = HALT
        print("HALT at step",step); halted=True; break
    w,_,d,ns=M[st][r]
    tape[pos]=w; pos+=d; st=ns; step+=1
    if pos<lo: lo=pos
    if pos>hi: hi=pos
    if step % 2_000_000 == 0:
        s=''.join(chr(48+tape[i]) for i in range(lo,hi+1)).strip('0')
        seps=re.findall(r'0+', s)
        msep=max((len(x) for x in seps),default=0)
        worst_sep=max(worst_sep,msep)
        # settled (non-last) 1-blocks ≡2 mod 3?
        blocks=re.findall(r'1+', s)
        settled=blocks[:-1] if len(blocks)>1 else []
        bad=sum(1 for b in settled if len(b)%3!=2)
        bad_blocks+=bad; checks+=1
        print(f"  step={step:9d}: max 0-separator={msep} (00 gap if >1), settled blocks not≡2mod3: {bad}/{len(settled)}")
if not halted:
    print(f"\nNO HALT in {maxsteps} steps. worst 0-separator ever = {worst_sep} (1 => no 00 gap EVER formed)")
    print(f"settled-block mod-3 violations total: {bad_blocks}")
    print("=> invariant (single separators + blocks≡2mod3) holds robustly => o17 non-halt LIKELY,")
    print("   decidable IF the mod-3 counting invariant is certified inductive (counting-DFA, not m-gram).")
