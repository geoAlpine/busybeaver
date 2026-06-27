import sys
from collections import Counter

def v2(n):
    # 2-adic valuation of positive int n
    return (n & -n).bit_length() - 1

def induced_step(o):
    # o odd -> T(o) = 3^{D-1}(3o-1)/2^D, D = v2(3o-1)
    x = 3*o - 1
    D = v2(x)
    m = x >> D            # odd
    return (pow(3, D-1) * m), D

def run(o0=27, N=50000, Kmax=16):
    o = o0
    Ds = []
    phis = []            # v2(o-1) at each visited o (before step)
    # we want residue stats and v2 stats over the orbit of o-values
    res_counts = {k: Counter() for k in range(2, Kmax+1)}
    # record sequence of D and the entry valuation after deep steps
    deep_next_phi = []   # v2(o_next -1) when current step is deep (D>=2)
    # run-length analysis of D=1
    # also verify run <=> cylinder: for each maximal D=1 run, compare length to v2(o_start-1)-1
    run_checks = []      # (run_len, v2(o_start-1)-1)
    prev_was_deep = True # so first run counts as "started after deep/boundary"
    cur_run_len = 0
    run_start_phi = None

    o_seq_phi = []
    Dseq = []
    o_values_mod = []  # not stored fully; we update counters online

    o_cur = o
    for j in range(N):
        phi = v2(o_cur - 1) if o_cur != 1 else 10**9
        # residue counts of o mod 2^k
        for k in range(2, Kmax+1):
            res_counts[k][o_cur & ((1<<k)-1)] += 1
        o_next, D = induced_step(o_cur)
        Dseq.append(D)
        o_seq_phi.append(phi)
        if D >= 2:
            deep_next_phi.append(v2(o_next - 1) if o_next != 1 else 10**9)
        o_cur = o_next

    # run-length distribution of D=1 (maximal runs)
    runs = []
    i = 0
    while i < len(Dseq):
        if Dseq[i] == 1:
            jstart = i
            while i < len(Dseq) and Dseq[i] == 1:
                i += 1
            L = i - jstart
            runs.append((jstart, L))
        else:
            i += 1

    # verify run <=> cylinder relation: L == phi(o_start)-1
    rc = []
    for (jstart, L) in runs:
        phi_start = o_seq_phi[jstart]
        rc.append((L, phi_start - 1, L == phi_start - 1))

    N1 = sum(1 for d in Dseq if d == 1)
    N2 = len(Dseq) - N1
    freqD1 = N1 / len(Dseq)
    runlens = [L for (_, L) in runs]
    run_dist = Counter(runlens)
    maxrun = max(runlens) if runlens else 0
    Emean_deep = sum(deep_next_phi)/len(deep_next_phi) if deep_next_phi else float('nan')

    print(f"N steps = {len(Dseq)}")
    print(f"freq(D=1) = {freqD1:.6f}   (target <= 1/2, margin {0.5-freqD1:+.6f})")
    print(f"mean D    = {sum(Dseq)/len(Dseq):.6f}")
    print(f"freq(D>=2)+freq(D>=3) = {N2/len(Dseq) + sum(1 for d in Dseq if d>=3)/len(Dseq):.6f}  (target >= 1/2)")
    print()
    print("D-value frequencies vs geometric 2^-d:")
    Dc = Counter(Dseq)
    for d in range(1,9):
        print(f"  D={d}: freq={Dc[d]/len(Dseq):.5f}  2^-d={2**-d:.5f}")
    print()
    print("run-length distribution of consecutive D=1 (maximal runs):")
    tot_runs = len(runs)
    for L in range(0, maxrun+1):
        c = run_dist.get(L,0)
        if c:
            print(f"  L={L:2d}: count={c:6d} frac={c/tot_runs:.5f}  geom(1/2) pred={0.5**(L)*0.5/ (0.5):.5f}" )
    print(f"  max run = {maxrun}")
    print(f"  mean run length E[L] = {sum(runlens)/len(runlens):.5f}  (freq(D=1)<=1/2 <=> E[L]<=1)")
    print()
    nbad = sum(1 for (_,_,ok) in rc if not ok)
    print(f"run<=>cylinder check  L == v2(o_start-1)-1 : {len(rc)-nbad}/{len(rc)} hold, {nbad} fail")
    print()
    print(f"E_deep[v2(o_next-1)] = {Emean_deep:.6f}   (freq(D=1)<=1/2 <=> this <= 2, Haar pred = 2)")
    # renewal identity: freq(D=1) =? freq(deep)*(E_deep[phi]-1)
    freq_deep = N2/len(Dseq)
    pred = freq_deep*(Emean_deep - 1)
    print(f"renewal identity check: freq(deep)*(E_deep-1) = {pred:.6f} vs freq(D=1)={freqD1:.6f}")
    print()
    print("freq(o == 1 mod 2^k)  (D=1 needs k>=2; deep cylinder occupancy):")
    for k in range(2, Kmax+1):
        c = res_counts[k][1]   # residue == 1 mod 2^k
        print(f"  k={k:2d}: freq(o==1 mod 2^k)={c/len(Dseq):.6f}  Haar=2^-(k-1)={2.0**-(k-1):.6f}")
    print()
    # equidistribution of o mod 4 and mod 8
    print("o mod 4 occupancy:", {r: round(res_counts[2][r]/len(Dseq),5) for r in (1,3)})
    print("o mod 8 occupancy:", {r: round(res_counts[3][r]/len(Dseq),5) for r in (1,3,5,7)})

    # test: are long D=1 runs followed by compensating deep step? (structurally yes: run always ends in deep)
    # check the deep step that ends each run, and its D, for the longest runs
    print()
    print("longest runs and the v2(o_start-1) that produced them (deterministic countdown):")
    rr = sorted(runs, key=lambda t:-t[1])[:8]
    for (jstart,L) in rr:
        print(f"  run len {L:2d} at step {jstart}, v2(o_start-1)={o_seq_phi[jstart]}  (L+1 == v2: {L+1==o_seq_phi[jstart]})")

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv)>1 else 50000
    run(N=N)
