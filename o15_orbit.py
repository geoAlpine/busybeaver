def parse(spec):
    M=[]
    for st in spec.split('_'):
        ts=[st[i:i+3] for i in (0,3)]; row=[]
        for t in ts:
            if t[0]=='-' or t[2]=='Z': row.append(None)
            else: row.append((int(t[0]), t[1], 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M
spec="1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"
M=parse(spec)
import re
SZ=1<<24; tape=bytearray(SZ); off=SZ//2
pos=off; st=0; lo=pos; hi=pos
step=0; maxsteps=80_000_000
# milestone: state A reading at the right frontier (the halt-test). Record total width then.
orbit=[]
while step<maxsteps:
    r=tape[pos]
    if st==0 and r==1:
        print("HALT",step); break
    if st==0 and pos>=hi-1:  # A near right frontier = halt-test milestone
        # record leading-1 block length and full width
        s=''.join(chr(48+tape[i]) for i in range(lo,hi+1))
        m=re.match(r'1+',s)
        V=len(m.group()) if m else 0
        interior_zeros=s.count('0')-s.count('01')  # rough
        z=sum(1 for i in range(1,len(s)-1) if s[i]=='0' and s[i-1]=='1' and s[i+1]=='1' and i< (m.end() if m else 0))
        orbit.append((step,hi-lo+1,V))
    w,_,d,dn=M[st][r]
    tape[pos]=w; pos+=d; st=dn; step+=1
    if pos>hi: hi=pos
    if pos<lo: lo=pos
# dedupe consecutive
seen=[]; last=None
for s,w,V in orbit:
    if V!=last: seen.append((s,w,V)); last=V
print("milestone (step,width,leadblock V):")
for s,w,V in seen[:30]: print(f"  t={s:9d} w={w:7d} V={V}")
Vs=[V for s,w,V in seen if V>3]
print("\nV sequence:",Vs[:20])
if len(Vs)>3:
    print("ratios:",[round(Vs[i+1]/Vs[i],3) for i in range(min(10,len(Vs)-1))])
