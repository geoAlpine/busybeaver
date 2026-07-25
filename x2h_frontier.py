import sys; sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, check_anchors
assert check_anchors(verbose=False)
MS = {732733:'M1(2)', 2852091:'M1(3)', 11329301:'M1(4)'}
st_={}; mx={'v':-10**9}; cur={'seg':None}
def hk(step, st, pos, tape, origin):
    r = pos-origin
    if r > mx['v']: mx['v']=r
    if step in MS:
        st_[step]=(r, mx['v'])
run(11329302, hook=hk, hook_from=0)
prev=None
for s in sorted(MS):
    p, mxv = st_[s]
    print(f"{MS[s]:>6} @{s:>9}  headpos={p:>5}  max-head-so-far={mxv:>8}"
          + (f"   right-frontier ahead of head = {mxv-p}" if True else ""))
    if prev: print(f"        advance since previous milestone: {mxv-prev}")
    prev=mxv
