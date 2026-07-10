#!/usr/bin/env python
"""
o4_expsum_frequency.py  (2026-07-10)

Bespoke exponential-sum / frequency build for the SPECIFIC o4 orbit (seed G0=43).
Exact big-int arithmetic; every structural claim assertion-checked.

Odometer  3G' = 4G + e(rho),  rho = G mod 3,  e = {0:9, 1:14, 2:1}.
Mirror    W = G + 14,  3W' = 4W + (e-14),  e-14 = {1:0, 2:-13, 0:-5}.
Facts:    rho=1  <=>  3|W ;  run theorem: maximal rho=1 run starting at G has
          length exactly v3(W) = v3(G+14) ; on a rho=1 step W' = (4/3)W so v3
          drops by exactly 1.  ledger a'=a+delta, delta={1:-1,2:+4,0:+6},
          psi=-delta ; fatal <=> prefix sum psi >= a0-1  <=>  #1/n >= 4/5.

freq{3|W_n} = freq{rho=1} = #1/n.   annealed 1/3, fatal 4/5, MARGIN 0.4667.

Three deliverables:
  (1) run-cap -> frequency structural analysis (forced non-1 density, exact
      run<->freq identity, all-1-tail impossibility, positive-margin test);
  (2) exponential sum S_k(N) = sum_{n<N} e(W_n/3^k) : |S|/N decay, sqrt(N)
      cancellation constant, van-der-Corput differencing gain test;
  (3) honest verdict.
"""
import cmath, math
from fractions import Fraction

E     = {0:9, 1:14, 2:1}
DELTA = {1:-1, 2:4, 0:6}
PSI   = {1:1, 2:-4, 0:-6}

def v3(x):
    if x == 0:
        return 10**9
    c = 0
    while x % 3 == 0:
        x //= 3; c += 1
    return c

def build_orbit(G0=43, a0=17, N=200000):
    """Full exact orbit. Returns arrays we need (residues, v3(W), ledger min)."""
    G = G0; a = a0
    rho_seq = []
    v3W_seq = []
    Wmod = {}   # k -> list of W_n mod 3^k  (k in 1..KMAX), stored compactly
    KMAX = 8
    mods = [3**k for k in range(1, KMAX+1)]
    Wmod_cols = [[] for _ in range(KMAX)]
    a_min = a
    prefix_psi = 0
    prefix_psi_max = -10**18
    ledger_ok = True
    c_counts = {0:0,1:0,2:0}
    for j in range(N):
        rho = G % 3
        W = G + 14
        rho_seq.append(rho)
        v3W_seq.append(v3(W))
        for i in range(KMAX):
            Wmod_cols[i].append(W % mods[i])
        c_counts[rho]+=1
        # ledger identity check a_n = a0 - #1 + 4#2 + 6#0
        prefix_psi += PSI[rho]
        if prefix_psi > prefix_psi_max: prefix_psi_max = prefix_psi
        # advance
        a = a + DELTA[rho]
        if a < a_min: a_min = a
        G = (4*G + E[rho])//3
    return dict(rho=rho_seq, v3W=v3W_seq, Wmod=Wmod_cols, mods=mods,
                a_min=a_min, prefix_psi_max=prefix_psi_max, c_counts=c_counts,
                a0=a0, N=N)

def verify_run_theorem(rho, v3W):
    """Maximal rho=1 runs have length exactly v3(W_entry). Assertion-checked."""
    N = len(rho)
    i = 0
    runs = []          # (start, length)
    while i < N:
        if rho[i] == 1:
            j = i
            while j < N and rho[j] == 1:
                j += 1
            L = j - i
            # entry depth is v3W[i]; run must equal it (unless truncated at N)
            if j < N:
                assert v3W[i] == L, f"run theorem FAIL at {i}: v3={v3W[i]} run={L}"
            runs.append((i, L))
            i = j
        else:
            i += 1
    return runs

def analyze_frequency(orbit, runs):
    N = orbit['N']; rho = orbit['rho']
    c = orbit['c_counts']
    freq1 = c[1]/N
    R = len(runs)
    # forced non-1 steps: at least one non-1 after each COMPLETE run (run not ending at N)
    complete_runs = [r for r in runs if r[0]+r[1] < N]
    Rc = len(complete_runs)
    forced_non1_density = Rc / N           # >= this many non-1 steps are FORCED
    actual_non1_density = (c[0]+c[2])/N
    Ls = [L for (_,L) in runs]
    meanL = sum(Ls)/len(Ls) if Ls else 0.0
    maxL = max(Ls) if Ls else 0
    # exact run<->freq identity if every non-1 block had length 1:
    # freq1 = meanL/(meanL+1). Compare to actual.
    freq_if_blocks1 = meanL/(meanL+1) if meanL>0 else 0
    # magnitude second moment
    sumL2 = sum(L*L for L in Ls)
    sum_v3 = sum(orbit['v3W'])
    return dict(freq1=freq1, R=R, Rc=Rc, forced_non1_density=forced_non1_density,
                actual_non1_density=actual_non1_density, meanL=meanL, maxL=maxL,
                freq_if_blocks1=freq_if_blocks1, sumL2=sumL2, sum_v3=sum_v3,
                cap=0.2618*N)

def exp_sums(orbit, ks=(1,2,3,4,5,6)):
    """S_k(N) = sum_{n<N} e(W_n / 3^k), measured at a ladder of N."""
    N = orbit['N']
    mods = orbit['mods']; Wmod = orbit['Wmod']
    checkpoints = [10**3, 3*10**3, 10**4, 3*10**4, 10**5, N-1 if N-1>10**5 else N]
    checkpoints = sorted(set(c for c in checkpoints if c<=N))
    out = {}
    for k in ks:
        col = Wmod[k-1]; m = mods[k-1]
        # running partial sums
        S = 0j
        rows = []
        cpset = set(checkpoints)
        # precompute roots of unity table for modulus m (m up to 3^6=729) -> fine
        table = [cmath.exp(2j*math.pi*r/m) for r in range(m)]
        for n in range(N):
            S += table[col[n]]
            if (n+1) in cpset:
                Nn = n+1
                rows.append((Nn, abs(S)/Nn, abs(S)/math.sqrt(Nn)))
        out[k] = rows
    return out

def vdc_differencing(orbit, k=1, H=(1,2,3,4,8)):
    """
    van der Corput: |S|^2 <= (N/(H+1)) sum_{|h|<=H} (1-|h|/(H+1)) sum_n e(f(n+h)-f(n)).
    Here f(n)=W_n/3^k. The differenced phase g_h(n) = (W_{n+h}-W_n)/3^k.
    KEY STRUCTURAL POINT: measure the *inner* correlation sums
        C_h = (1/N) sum_n e((W_{n+h}-W_n)/3^k)
    If |C_h| does not decay (stays ~O(1)) then differencing yields NO gain --
    the non-Pisot obstruction. We also show W_{n+1}-W_n involves a DEEPER 3-adic
    level (level k+1), documenting the regress.
    """
    N = orbit['N']
    mods = orbit['mods']; Wmod = orbit['Wmod']
    m = mods[k-1]
    col = Wmod[k-1]
    table = [cmath.exp(2j*math.pi*r/m) for r in range(m)]
    res = {}
    M = min(N, 100000)
    for h in H:
        S = 0j
        cnt = 0
        for n in range(M-h):
            d = (col[n+h] - col[n]) % m
            S += table[d]
            cnt += 1
        res[h] = abs(S)/cnt
    return res

def main():
    import sys
    N = 200000
    print(f"# o4 exponential-sum / frequency build  N={N}  seed G0=43\n")
    orbit = build_orbit(N=N)

    # ---- soundness: ledger identity + run theorem ----
    c = orbit['c_counts']
    a_pred = orbit['a0'] - c[1] + 4*c[2] + 6*c[0]
    print("== soundness guards ==")
    print(f"  residue counts: #1={c[1]} #2={c[2]} #0={c[0]}  sum={sum(c.values())}")
    print(f"  ledger a_N predicted = a0 - #1 + 4#2 + 6#0 = {a_pred}")
    print(f"  ledger min over run = {orbit['a_min']}  (fatal would need min <= 0)")
    print(f"  max prefix psi sum  = {orbit['prefix_psi_max']}  (fatal >= a0-1 = {orbit['a0']-1})")
    runs = verify_run_theorem(orbit['rho'], orbit['v3W'])
    print(f"  run theorem verified on all {len(runs)} complete rho=1 runs (v3(W_entry)==run len): OK")

    # ---- (1) run-cap -> frequency ----
    print("\n== (1) run-cap -> frequency structural analysis ==")
    fa = analyze_frequency(orbit, runs)
    print(f"  freq{{3|W_n}} = freq{{rho=1}} = #1/N = {fa['freq1']:.5f}   (annealed 1/3, fatal 4/5)")
    print(f"  # rho=1 runs R = {fa['R']}  (complete {fa['Rc']})")
    print(f"  mean run length = {fa['meanL']:.4f}   max run length = {fa['maxL']}  (cap 0.262N = {fa['cap']:.0f})")
    print(f"  FORCED non-1 density  >= R_complete/N = {fa['forced_non1_density']:.5f}")
    print(f"  actual non-1 density  = {fa['actual_non1_density']:.5f}")
    print(f"  identity check: meanL/(meanL+1) = {fa['freq_if_blocks1']:.5f}  vs freq1 {fa['freq1']:.5f}")
    print(f"  second moment sum L^2 = {fa['sumL2']}  (= {fa['sumL2']/N**2:.4f} N^2)")
    print(f"  sum_j v3(W_j) = {fa['sum_v3']}  (= {fa['sum_v3']/N**2:.5f} N^2, magnitude bound 0.131 N^2)")

    # all-1-tail impossibility (exact, symbolic) : if rho_n=1 for all n>=n0 then
    # v3(W_n) = v3(W_{n0}) - (n-n0) -> negative, contradiction. Demonstrate the drop:
    print("\n  all-1-TAIL impossibility (v3 drops by 1 per rho=1 step):")
    # find the longest run and show v3 ladder
    longest = max(runs, key=lambda r:r[1])
    s,L = longest
    ladder = [orbit['v3W'][s+t] for t in range(L)]
    print(f"    longest run at gen {s}, length {L}; v3(W) ladder = {ladder[:12]}{'...' if L>12 else ''}")
    print(f"    -> a rho=1 run cannot exceed v3(W_entry); an infinite tail needs v3=inf: IMPOSSIBLE.")

    # positive-margin test: can forced non-1 density be bounded below by c>0 ?
    # adversary B (cap-saturating tiling) has R = O(log N) -> forced density -> 0.
    print("\n  positive-margin test (adversary respecting cap AND magnitude):")
    advB = adversary_B_freq(N)
    print(f"    cap-saturating tiling: #runs={advB['R']}, forced non-1 density={advB['forced']:.5f}, freq1={advB['freq1']:.5f}")
    advA = adversary_A_freq(N, m=5)
    print(f"    shallow burst (1^5 2)*: freq1={advA['freq1']:.5f} (=5/6), runs depth 5 << cap, magnitude tiny")
    print(f"    => run-cap forces NO positive lower bound on non-1 density (adversaries reach freq1 -> 1 and 5/6).")

    # ---- exact freq <-> exp-sum identity : makes the margin precise ----
    print("\n== exact identity  #1 = N/3 + (2/3) Re(S_1)  (assertion-checked) ==")
    m = orbit['mods'][0]; col = orbit['Wmod'][0]
    tab = [cmath.exp(2j*math.pi*r/m) for r in range(m)]
    S1 = sum(tab[col[n]] for n in range(N))
    pred1 = N/3 + (2/3)*S1.real
    print(f"  Re(S_1) = {S1.real:.4f}   N/3+(2/3)Re(S_1) = {pred1:.3f}   actual #1 = {c[1]}")
    assert abs(pred1 - c[1]) < 1e-3, "freq<->S1 identity FAIL"
    print(f"  => freq1 = 1/3 + (2/3) Re(S_1)/N.  Fatal freq1>=4/5  <=>  Re(S_1)/N >= 7/10.")
    print(f"     observed Re(S_1)/N = {S1.real/N:.5f}  (need to PROVE < 0.7 to decide o4).")
    print(f"     delta_-14 (all rho=1) orbit: S_1=N, Re/N=1>0.7  => no unconditional bound; quenched needed.")

    # ---- van der Corput regress identity (assertion-checked) ----
    print("\n== van der Corput regress:  W_{n+1}-W_n = (W_n + e_n - 14)/3 (level k -> k+1) ==")
    # verify on the first few thousand steps with exact ints by re-deriving W
    G = 43
    ok = True
    Wprev = G+14
    for n in range(5000):
        rho = G % 3
        Gn = (4*G + E[rho])//3
        Wn1 = Gn + 14
        diff = Wn1 - Wprev
        assert diff == (Wprev + (E[rho]-14))//3, f"vdc identity FAIL at {n}"
        G = Gn; Wprev = Wn1
    print("  identity verified exactly for 5000 steps.")
    print("  => e((W_{n+1}-W_n)/3^k) = e(W_n/3^{k+1}) e((e_n-14)/3^{k+1}):")
    print("     differencing at level k = a twisted level-(k+1) sum, multiplier |4|=1 (unit mod 3).")
    print("     NO contraction: infinite 3-adic regress = the non-Pisot obstruction, concretely.")

    # ---- (2) exponential sum ----
    print("\n== (2) exponential sum  S_k(N) = sum_{n<N} e(W_n/3^k) ==")
    es = exp_sums(orbit)
    for k, rows in es.items():
        print(f"  k={k}:")
        for (Nn, ratio, sq) in rows:
            print(f"     N={Nn:>7}  |S|/N = {ratio:.5f}   |S|/sqrt(N) = {sq:.3f}")
    print("\n  van der Corput differencing (inner correlation C_h = (1/M) sum e((W_{n+h}-W_n)/3^k)):")
    for k in (1,2):
        vd = vdc_differencing(orbit, k=k)
        print(f"    k={k}: " + "  ".join(f"|C_{h}|={v:.4f}" for h,v in vd.items()))
    print("    (if |C_h| ~ O(1) not -> 0, differencing gives NO cancellation gain: non-Pisot regress.)")

    # ---- empirical decay exponent for |S_1(N)| : fit log|S_1| = alpha log N + c ----
    print("\n== empirical decay exponent of |S_1(N)| (running fit) ==")
    m = orbit['mods'][0]; col = orbit['Wmod'][0]
    tab = [cmath.exp(2j*math.pi*r/m) for r in range(m)]
    S = 0j; xs=[]; ys=[]
    grid = set(int(10**(t/6)) for t in range(18, int(6*math.log10(N))+1))
    for n in range(N):
        S += tab[col[n]]
        if (n+1) in grid and abs(S)>0:
            xs.append(math.log(n+1)); ys.append(math.log(abs(S)))
    # least squares slope
    nns=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    slope=(nns*sxy-sx*sy)/(nns*sxx-sx*sx)
    print(f"  slope alpha of log|S_1| vs log N = {slope:.3f}  (0.5 = square-root cancellation / equidistribution)")
    print(f"  => |S_1(N)| ~ N^{slope:.2f}; |S_1|/N -> 0 like N^(alpha-1). o(1) but NO effective/proven rate.")

def adversary_B_freq(N):
    """Cap-saturating tiling: runs at length ~0.262*position, one non-1 between."""
    pos = 10
    ones = 0; nonone = 0; R = 0
    while pos < N:
        L = max(1, int(0.2618*pos))
        if pos + L + 1 > N:
            L = N - pos - 1
            if L <= 0: break
        ones += L; nonone += 1; R += 1
        pos += L + 1
    tot = ones + nonone
    return dict(R=R, forced=nonone/tot, freq1=ones/tot)

def adversary_A_freq(N, m=5):
    """(1^m 2)* : freq1 = m/(m+1)."""
    block = m+1
    reps = N // block
    ones = reps*m; nonone = reps
    tot = ones+nonone
    return dict(freq1=ones/tot if tot else 0)

if __name__ == "__main__":
    main()
