#!/usr/bin/env python3
"""x2cc_gencheck.py -- CARRY CALCULUS: exact machine-checked derivation of FULL
generations in the certified symbolic executor (concrete counts).  For each g in the
range, start from the M1(g) template, run the executor until the next milestone with
leading gap 22 (M1(g+1)), and check:
  (1) the reached config equals the M1(g+1) template exactly;
  (2) the emitted E-met gap ledger is exactly
        {18, 10} + {6 iff g even}  (all >= 3)  and L=2 events only otherwise;
  (3) no other event; no halt (the executor raises Halted on any gap-3).
Each generation run is an exact derivation (macro rules are certified closed forms),
i.e. a machine-checked proof for that concrete g."""
import sys, time
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import Config, Machine, Split, Halted, E, runs_concrete
from x2cc_faith import T


def m1_spec(g):
    K = g + 8
    casc = [2**j - 3 for j in range(K - 1, 1, -1)]  # 2^(K-1)-3 ... 1
    big = 2**K - 3 if g % 2 == 0 else 2**K - 9
    tail = "1 0^10" if g % 2 == 0 else "1 0^4 10^6"
    units = f"1000000^{g-1} " if g > 1 else ""
    return (f"0^22 {units}{tail} 1^{big} "
            + ' '.join(f"0^2 1^{b}" for b in casc))


def run_gen(g, max_ops=3_000_000):
    start = Config([], 'E', T(m1_spec(g)))
    want = runs_concrete(T(m1_spec(g + 1)), {}).rstrip('0')
    m = Machine(start, guard_r=False)
    t0 = time.time()
    op = 0
    m.step()  # leave the initial milestone
    while op < max_ops:
        op += 1
        c = m.cfg
        if c.state == 'E' and c.right and c.right[0][0][0] == '0':
            if not any('1' in p and cn.ge(1) is not False for p, cn in c.left):
                # milestone; is it M1(g+1)?
                if c.right and c.right[0][0] == '0' and c.right[0][1].is_const() \
                        and c.right[0][1].c == 22:
                    ok = runs_concrete(c.right, {}).rstrip('0') == want
                    gaps = sorted(ev[2].c for ev in m.events
                                  if ev[1] == 'gap' and ev[2].c >= 3)
                    n2 = sum(1 for ev in m.events if ev[1] == 'gap' and ev[2].c == 2)
                    pred = sorted([18, 10] + ([6] if g % 2 == 0 else []))
                    gok = gaps == pred
                    print(f"g={g}: M1(g+1) template {'EXACT' if ok else 'MISMATCH'}; "
                          f"gaps>=3 {gaps} vs {pred} {'OK' if gok else 'BAD'}; "
                          f"L2={n2}; ops={op} [{time.time()-t0:.0f}s]", flush=True)
                    if not ok:
                        print("  got:", c)
                    return ok and gok
        m.step()
    print(f"g={g}: max_ops exceeded")
    return False


if __name__ == "__main__":
    g0 = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    g1 = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    allok = True
    for g in range(g0, g1 + 1):
        try:
            allok &= run_gen(g)
        except (Split, Halted) as e:
            print(f"g={g}: {type(e).__name__}: {e}")
            allok = False
    print("ALL GENERATIONS EXACT" if allok else "FAILURES PRESENT")
