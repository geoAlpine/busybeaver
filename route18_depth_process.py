"""
Route #18: the Antihydra DEPTH PROCESS for the eventual-transparency / finite-certificate hybrid.

Kernel (K): c0 = 8, c -> floor(3c/2). Halt predicate lives in the parity sequence
b_n = c_n mod 2 (even-density >= 1/3). The 2-adic 'carry depth' that a template-style
x2-transport would have to absorb is

        D_n := v2(c_n - 1)   (2-adic valuation of c_n - 1).

D_n = 0 exactly when c_n is even (c_n - 1 odd). D_n >= 1 when c_n is odd.

We test the eventual-transparency hypothesis:
  (1) Structure of D_n: is it a countdown/sawtooth renewal process? measure jump depths K_i.
  (2) Tail of the jump-depth K: P(K >= k). Does the heavy (geometric) tail persist at ALL
      scales, or does the orbit eventually enter a bounded-carry window?
  (3) Running max jump depth M(N) and where the record runs occur -> giant runs i.o.?
  (4) E[K], E[K^2] running estimates: converge or drift (the (K)-adjacent 2nd-moment).
  (5) mean depth (1/N) sum D_n and its liminf.

All arithmetic exact (Python big int).
"""
import sys, time
sys.set_int_max_str_digits(100_000_000)
from collections import Counter

def v2(x):
    # x > 0
    return (x & -x).bit_length() - 1

def run(N, report=True):
    c = 8
    t0 = time.time()
    # depth stream
    # We record: D_n, parity, and detect renewal (c even <=> D=0).
    D_prev = None
    jump_depths = []          # K_i: depth at the START of each odd-run (the 'entry depth')
    run_len = []              # length of each maximal odd run (should equal K_i under countdown)
    # streaming stats
    sumD = 0
    cntD = Counter()          # distribution of D_n
    # running mean-depth worst (liminf tracker)
    worst_run_avg = 10**9
    worst_at = -1
    # jump-depth tail via running max
    maxK = 0
    record_positions = []     # (n, K) when a new record jump depth appears
    # for sawtooth verification
    countdown_violations = 0
    # odd-run tracking
    in_run = False
    cur_run_start_depth = 0
    cur_run_len = 0
    prevD = None

    for n in range(N):
        d = v2(c - 1) if c != 1 else 10**9  # c=1 is the fixed point (halt-adjacent); never hit for seed 8
        sumD += d
        cntD[min(d, 40)] += 1

        # sawtooth / countdown check: within an odd run, depth should decrease by exactly 1
        if prevD is not None and prevD >= 1 and d >= 1:
            if d != prevD - 1:
                countdown_violations += 1

        # odd-run (D>=1) bookkeeping
        if d >= 1:
            if not in_run:
                in_run = True
                cur_run_start_depth = d
                cur_run_len = 1
            else:
                cur_run_len += 1
        else:  # d == 0, renewal (c even)
            if in_run:
                jump_depths.append(cur_run_start_depth)
                run_len.append(cur_run_len)
                if cur_run_start_depth > maxK:
                    maxK = cur_run_start_depth
                    record_positions.append((n - cur_run_len, cur_run_start_depth))
                in_run = False

        # running mean-depth (liminf tracker), only after warmup
        if n >= 50:
            avg = sumD / (n + 1)
            if avg < worst_run_avg:
                worst_run_avg = avg
                worst_at = n

        prevD = d
        # advance
        c = (3 * c) >> 1  # floor(3c/2): 3c then floor-div 2

    elapsed = time.time() - t0
    if report:
        print(f"N={N}  final c has {c.bit_length()} bits ({len(str(c))} dec digits)  time={elapsed:.1f}s")
    return dict(
        N=N, sumD=sumD, cntD=cntD, jump_depths=jump_depths, run_len=run_len,
        worst_run_avg=worst_run_avg, worst_at=worst_at, maxK=maxK,
        record_positions=record_positions, countdown_violations=countdown_violations,
        final_bits=c.bit_length(),
    )

def analyze(R):
    N = R["N"]
    K = R["jump_depths"]
    RL = R["run_len"]
    print(f"\n=== DEPTH PROCESS ANALYSIS (Antihydra seed 8, N={N}) ===")
    print(f"mean depth (1/N)sum D_n = {R['sumD']/N:.5f}")
    print(f"worst (liminf) running mean depth = {R['worst_run_avg']:.5f} at n={R['worst_at']}")
    print(f"countdown/sawtooth violations (D should step -1 inside odd runs): {R['countdown_violations']}")
    print(f"run_len == jump_depth for every run? {all(a==b for a,b in zip(RL,K))}  (#runs={len(K)})")

    print(f"\n-- D_n marginal distribution (vs geometric 2^-(d+1)) --")
    tot = sum(R['cntD'].values())
    for d in range(0, 16):
        emp = R['cntD'].get(d,0)/tot
        geo = 0.5**(d+1)
        print(f"  D={d:2d}: emp={emp:.6f}  geom={geo:.6f}  ratio={emp/geo if geo>0 else 0:.3f}")

    print(f"\n-- jump depth K (entry depth of odd runs): #={len(K)} --")
    print(f"  E[K]   = {sum(K)/len(K):.5f}")
    print(f"  E[K^2] = {sum(k*k for k in K)/len(K):.5f}")
    print(f"  E[K^3] = {sum(k**3 for k in K)/len(K):.5f}")
    print(f"  max K  = {R['maxK']}")
    ck = Counter(K)
    print(f"  tail P(K>=k) vs geometric 2^-(k-1):")
    cum = 0
    srt = sorted(ck.items())
    total = len(K)
    for k in range(1, R['maxK']+1):
        pk = sum(v for kk,v in ck.items() if kk>=k)/total
        geo = 0.5**(k-1)
        print(f"    P(K>={k:2d})={pk:.6f}  geom={geo:.6f}  ratio={pk/geo if geo>0 else 0:.3f}")
        if pk == 0: break

    print(f"\n-- record jump depths (running max K, giant runs) --")
    for (pos, k) in R['record_positions']:
        print(f"    n~{pos:9d}: new record K={k}   (2^-(k-1) expected ~1 per {2**(k-1)} runs)")

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    R = run(N)
    analyze(R)
