import sys; sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, check_anchors
assert check_anchors(verbose=False)
cap={}
def hk(step, st, pos, tape, origin):
    if step==732733:
        # right tape = cells strictly right of head, up to the rightmost visited
        hi=len(tape)-1
        while hi>pos and tape[hi]==0: hi-=1
        cap['r']=''.join(str(tape[i]) for i in range(pos+1,hi+1))
        cap['l']=(pos, origin)
run(732734, hook=hk, hook_from=732733)
real=cap['r']
lean=open('/tmp/meven0.txt').read().strip()
print(f"real M1(2) right (trimmed of trailing 0s): {len(real)}")
print(f"MEven 0 [] right                          : {len(lean)}")
print(f"prefix match: {lean.startswith(real)}")
if lean.startswith(real):
    rest=lean[len(real):]
    print(f"remainder length {len(rest)}, all zeros: {set(rest) <= {'0'}}")
else:
    for i,(a,b) in enumerate(zip(real,lean)):
        if a!=b: print(f"first mismatch at {i}: real={a} lean={b}"); print(" real:",real[max(0,i-20):i+20]); print(" lean:",lean[max(0,i-20):i+20]); break
