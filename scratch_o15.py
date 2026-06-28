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
O15="1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"  # halt = state A (idx0) reads 1
M=parse(O15)
SZ=1<<25; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=hi=pos; step=0
maxsteps=120_000_000
# milestone: state A about to read at right frontier (halt test). record full RLE + width + leading V
mile=[]
last_w=None
while step<maxsteps:
    r=tape[pos]
    if st==0 and r==1:
        print("HALT at",step); break
    if st==0 and pos>=hi-1:
        s=''.join(chr(48+tape[i]) for i in range(lo,hi+1))
        rle=re.findall(r'0+|1+',s)
        comp=tuple((c[0],len(c)) for c in rle)
        m=re.match(r'1+',s); V=len(m.group()) if m else 0
        w=hi-lo+1
        if w!=last_w:
            mile.append((step,w,V,comp))
            last_w=w
    w_,_,d,ns=M[st][r]; tape[pos]=w_; pos+=d; st=ns; step+=1
    if pos>hi: hi=pos
    if pos<lo: lo=pos
# dedupe by width
print("o15 milestones (step, width, leadblockV, blockstructure):")
seen=[]; lastV=None
for s,w,V,comp in mile:
    seen.append((s,w,V,comp))
for s,w,V,comp in seen[:30]:
    cs=' '.join(f"{a}^{b}" for a,b in comp[:14])
    print(f"  t={s:10d} w={w:7d} V={V:7d} | {cs}")
ws=[w for s,w,V,comp in seen]
print("\nwidth ratios:",[round(ws[i+1]/ws[i],4) for i in range(min(15,len(ws)-1))])
Vs=[V for s,w,V,comp in seen]
print("leadblock V seq:",Vs[:25])
print("V parity:",[V%2 for V in Vs[:25]])
print("V mod 3:",[V%3 for V in Vs[:25]])
# count A-visits to right frontier (halt tests) and what they read
sys.stdout.flush()
