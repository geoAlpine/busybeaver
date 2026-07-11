# Adjudication with BOUNDED gap-walk (cap 40 -- big doubling gaps irrelevant to the {4..22} question).
spec="1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
T={}
for si,blk in enumerate(spec.split('_')):
    st="ABCDEF"[si]
    for sym in (0,1):
        f=blk[sym*3:sym*3+3]; T[(st,sym)]=None if f=='---' else (int(f[0]),f[1],f[2])
tape={}; head=0; st='A'; steps=0; CAP=1_000_000
early=set(); late=set(); tg=tape.get
while steps<CAP:
    sym=tg(head,0); tr=T[(st,sym)]
    if tr is None: print("HALT",steps); break
    if st=='E' and sym==0 and tg(head-1,0)==1:
        L=1; p=head+1
        while L<=41 and tg(p,0)==0: L+=1; p+=1   # BOUNDED walk
        if 3<=L<=40:
            (early if steps<200000 else late).add(L)
    w,mv,nx=tr; tape[head]=w; head+=(1 if mv=='R' else -1); st=nx; steps+=1
print(f"reached {steps} steps")
print(f"  EARLY (<200k): {sorted(early)}")
print(f"  LATE (>=200k): {sorted(late)}")
print(f"  ONLY early (transient): {sorted(early-late)}   ONLY late: {sorted(late-early)}")
print("No machine decided. No label upgraded.")
