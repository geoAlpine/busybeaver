import sys; sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, rle, check_anchors
assert check_anchors(verbose=False), "instrument FAILED"
# even: low-phase span at g=2 is 267+38*(2*0+2) = 343; M6(2) is at 733076.
# odd:  low-phase span at g=3 is 419+76*0     = 419; odA(0) = M6(3).
targets = {732733:'M1(2)?  (=733076-343)', 733076:'M6(2)', 2852091:'M1(3)'}
out={}
def hk(step, st, pos, tape, origin):
    if step in targets:
        out[step]=(('ABCDEF'[st]), pos-origin, rle(tape,pos,maxruns=3),
                   ''.join(str(tape[pos-d]) for d in range(1,9)))
run(2852092, hook=hk, hook_from=min(targets))
for s in sorted(targets):
    if s in out:
        st,p,r,l = out[s]
        print(f"{s:>9} {targets[s]:<22} st={st} pos={p} right={r} left(1..8)={l}")
