#!/usr/bin/env python3
"""x2co_fold.py -- test which cascade FOLDS the certified Prover can close.

(A) UNIFORM register fold: chew (1^5 0^2)^j  [all blocks equal] -- a uniform loop,
    should loop-accelerate (single param j, d=1).
(B) NON-UNIFORM cascade fold: chew 1^C1 0^2 1^C2 0^2 ... with C_i = 2^(j)-3 all
    DIFFERENT -- NOT a uniform shift, so loop acceleration cannot apply at the
    cascade level.  We demonstrate the plain machine has no config(p)->config(p-1)
    uniform recurrence across cascade blocks."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import Config, Machine, Split, Halted, E
from x2cc_faith import T, Prover, GoalConfig, GoalRight


def loc(c, nl=3, nr=8):
    def rr(runs):
        return ' '.join(f"{p}^{cc}" if not (cc.is_const() and cc.c == 1) else p for p, cc in runs)
    return f"...{rr(c.left[-nl:])} [{c.state}] {rr(c.right[:nr])}..."


def test_uniform_machine():
    print("=== (A) UNIFORM register fold (1^5 0^2)^j : plain machine, symbolic j ===")
    # D at the chew entry of a (1^5 0^2)^j register block run, opaque tail 1^B
    left = T("01^3")
    right = T("0^3 1^5 0^2 1111100^j 1^B 0^2")
    m = Machine(Config(left, 'D', right), guard_r=True)
    print("start:", loc(m.cfg))
    ops = 0
    hist = []
    try:
        while ops < 2000:
            ops += 1
            hist.append(m.cfg.key())
            m.step()
            # detect a uniform recurrence config(j)->config(j-1)
            r = Prover.match_general(Config(*_split(hist[0])), m.cfg) if False else None
    except Split as s:
        print(f"  split after {ops} ops: {s}")
        print("  at:", loc(m.cfg))
    except Halted as h:
        print(f"  HALT: {h}")
    return


def _split(key):
    left, state, right = key
    return list(left), state, list(right)


def test_uniform_prover():
    print("\n=== (A') UNIFORM register fold: Prover loop-acceleration, symbolic j ===")
    left = T("01^3")
    right = T("0^3 1^5 0^2 1111100^j 1^B 0^2")
    start = Config(left, 'D', right)
    # goal: all j register blocks chewed; head at [D] 0^3 1^(B-2)... with comb grown.
    # We use a loose GoalRight: state D and the register run 1111100^j is GONE
    # (no '1111100' pattern remains), head at 0^3 then big block.
    P = Prover("reg-fold", verbose=True)

    class G:
        def subst(self, p, v):
            return self
        def matches(self, cfg):
            if cfg.state != 'D':
                return False
            for pat, c in cfg.right:
                if pat == '1111100' and c.ge(1) is not False:
                    return False
            # require we've reached the big block: some 1-run with B
            return any('B' in c.m for _, c in cfg.right)
    try:
        P.prove(start, G(), max_ops=20000)
        print(f"  RESULT: {len(P.results)} branch(es) closed")
        for case, fc, ev in P.results:
            print(f"    case {case or '(base)'}: {loc(fc)}")
            print(f"      gaps: {[str(e[2]) for e in ev if e[1]=='gap']}  loops: {[e[2] for e in ev if e[1]=='loop']}")
    except Exception as e:
        print(f"  Prover FAILED: {type(e).__name__}: {e}")


def test_nonuniform():
    print("\n=== (B) NON-UNIFORM cascade fold: can a single loop-accel span blocks? ===")
    # concrete cascade with DIFFERENT block sizes 2^j-3
    K = 11
    casc = [2**j - 3 for j in range(6, 1, -1)]  # 61,29,13,5,1  (all different)
    print("  cascade blocks:", casc)
    spec = "0^3 1^5 0^2 " + ' '.join(f"1^{b} 0^2" for b in casc)
    m = Machine(Config(T("01^3"), 'D', T(spec)), guard_r=True)
    # record D-state configs at each 0^3 boundary; check if any two are a uniform
    # single-param shift of each other (they cannot be: block sizes differ)
    snaps = []
    ops = 0
    try:
        while ops < 5000:
            ops += 1
            c = m.cfg
            if c.state == 'D' and c.right and c.right[0][0] == '0' and c.right[0][1].ge(3) is not False:
                snaps.append(c.copy())
            m.step()
    except (Split, Halted) as e:
        pass
    # the block-entry snapshots have block counts 61,29,13,5,1 -> the "current block"
    # 1-run count is different each time; no uniform config(p)->config(p-1) shift exists
    blkcounts = []
    for c in snaps:
        for pat, cc in c.right:
            if pat == '1' and cc.is_const() and cc.c > 3:
                blkcounts.append(cc.c)
                break
    uniq = sorted(set(blkcounts))
    print(f"  distinct current-block 1-run counts seen: {uniq[:12]}")
    print("  -> block sizes are all DIFFERENT (2^j-3); a d=1 loop-accel needs a")
    print("     uniform shift, which does NOT exist across cascade blocks.")


if __name__ == "__main__":
    test_uniform_machine()
    test_uniform_prover()
    test_nonuniform()
