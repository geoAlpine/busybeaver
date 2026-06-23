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
def run(maxsteps):
    tape={}; pos=0; st=0; lo=0; hi=0
    resets=[]   # (step, N=width) when tape == 0 1^(N-1) clean (state F, single 1-block)
    for step in range(maxsteps+1):
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        r=tape.get(pos,0); tr=M[st][r]
        if tr is None:
            return ('HALT',step,resets)
        w,mv,ns=tr; tape[pos]=w; pos+= 1 if mv=='R' else -1; st=ns
        if ns==5 and pos<lo+1:  # state F at/near left frontier
            # check clean single-block form 0 1^(w-1)
            s=''.join(str(tape.get(i,0)) for i in range(pos,hi+1))
            if s and s[0]=='0' and set(s[1:])=={'1'}:
                resets.append((step,len(s)))
    return ('RUN',maxsteps,resets)
tag,last,resets=run(5000000)
print("status",tag,"at",last)
Ns=[N for st,N in resets]
print("reset widths N_k:", Ns[:40])
# compare to clean map f(N)=floor(8N/3)+2 starting from first
def f(N): return (8*N)//3+2
pred=[Ns[0]]
for _ in range(len(Ns)-1): pred.append(f(pred[-1]))
breaks=[i for i in range(len(Ns)) if Ns[i]!=pred[i]]
print("predicted (8N/3+2):    ", pred[:40])
print("first break at index:", breaks[0] if breaks else None)
if breaks:
    i=breaks[0]
    print(f"  at epoch {i}: actual {Ns[i]} vs predicted {pred[i]}, diff {Ns[i]-pred[i]}")
    print("  N_{i-1} =", Ns[i-1], " N_{i-1} mod 3 =", Ns[i-1]%3, " mod 9=",Ns[i-1]%9)
# base-3 of N_k and digit pattern
print("\nN_k in base 3 (look for digit-2 events):")
def b3(n):
    d=[]
    while n: d.append(n%3); n//=3
    return ''.join(str(x) for x in reversed(d)) or '0'
for st,N in resets[:18]:
    print(f"  N={N:8d}  base3={b3(N)}  N mod3={N%3}")
