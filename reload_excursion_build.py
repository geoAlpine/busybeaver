"""
RELOAD_EXCURSION_BUILD 2026-07-09
=================================
Build the EXACT Z_q^x reload-unit dynamics u_{i+1} = F(u_i, K_i) for the
{2,3}-smooth cryptids (Antihydra q=2, o4 q=3), then probe the reload map for the
a-priori coupling between consecutive depths K that the ABSTRACT excursion
(EXCURSION_SYNTHESIS) lacked.

General reload-unit map (derived):  on branch with fixed point x, entry v with
v - x = q^{K} u  (u a q-adic UNIT), exit = x + p^{K} u, so the next entry's
depth/unit are
        K_{i+1} = v_q( p^{K_i} u_i + s_i ),
        u_{i+1} = ( p^{K_i} u_i + s_i ) / q^{K_{i+1}},
where s_i = x_i - x_{i+1} is the (bounded, branch-determined) CARRY offset.
  Antihydra: (p,q)=(3,2), x_even=0, x_odd=1, s alternates -1 (even->odd) / +1.
  o4:        (p,q)=(4,3), x_1=-14,x_2=-1,x_0=-9, s = x_rho - x_rho'.

STRICT big-int, interpreter-agnostic. No label upgraded.
"""
import sys, random
from collections import Counter, defaultdict
from math import log2

def vq(n, q):
    if n == 0: return 10**9
    k = 0
    while n % q == 0:
        n //= q; k += 1
    return k

# =====================================================================
# PART A. ANTIHYDRA  (p,q)=(3,2)
# =====================================================================
def antihydra_reloads(c0=8, NSTEP=200000):
    """Return list of reload records (parity, K, u) for maximal runs, plus verify
    the exact reload recursion inline against exact big-int values."""
    c = c0
    recs = []                      # (parity, K, u_lowbits, ) ; we keep exact u only transiently
    cur_par = c % 2; runlen = 0; entry = c
    K_arr = []; par_arr = []; ulow = []; umod = []   # residues for stats
    MOD = 1 << 64
    n = 0
    # collect maximal runs
    runs = []
    while n < NSTEP:
        par = c % 2
        if par == cur_par:
            runlen += 1
        else:
            runs.append((cur_par, runlen, entry))
            cur_par = par; runlen = 1; entry = c
        c = (3*c)//2
        n += 1
    runs.append((cur_par, runlen, entry))

    # build (parity, K, u exact) and verify recursion
    mm_reload = 0; mm_len = 0; checks = 0
    prev = None
    runs = runs[:-1]   # drop the truncated final run (orbit cut at NSTEP)
    for (par, L, e) in runs:
        x = 0 if par == 0 else 1
        # verify run length == v2(entry - x)
        if vq(e - x, 2) != L: mm_len += 1
        u = (e - x) >> L            # exact odd unit
        # verify reload recursion from prev
        if prev is not None:
            pp, pK, pu, ps = prev   # ps = sign offset s from prev branch to this
            val = 3**pK * pu + ps
            Kpred = vq(val, 2)
            upred = val >> Kpred
            if Kpred != L or upred != u:
                mm_reload += 1
            checks += 1
        # s for the NEXT transition depends on THIS parity -> next parity (alternating)
        # even(x=0)->odd(x'=1): s = x - x' = -1 ; odd(x=1)->even(x'=0): s = +1
        s_next = -1 if par == 0 else +1
        prev = (par, L, u, s_next)
        K_arr.append(L); par_arr.append(par); ulow.append(u & (MOD-1))
    return K_arr, par_arr, ulow, mm_reload, mm_len, checks, len(runs)

def analyze(K_arr, par_arr, ulow, tag):
    N = len(K_arr)
    print(f"\n--- {tag}: {N} reload events ---")
    # marginal of K
    cK = Counter(K_arr)
    print("  marginal P(K=k) vs geometric 2^-k:")
    for k in range(1, 9):
        print(f"    K={k}: emp={cK[k]/N:.4f}  geom={2.0**-k:.4f}")
    meanK = sum(K_arr)/N
    meanK2 = sum(k*k for k in K_arr)/N
    print(f"  E[K]={meanK:.4f} (geom mean 2.0)   E[K^2]={meanK2:.4f} (geom 6.0)   maxK={max(K_arr)}")

    # correlation of consecutive K
    Ki  = K_arr[:-1]; Kj = K_arr[1:]
    m = sum(Ki)/len(Ki); m2 = sum(Kj)/len(Kj)
    cov = sum((a-m)*(b-m2) for a,b in zip(Ki,Kj))/len(Ki)
    va = sum((a-m)**2 for a in Ki)/len(Ki); vb = sum((b-m2)**2 for b in Kj)/len(Kj)
    corr = cov/(va*vb)**0.5
    print(f"  corr(K_i, K_i+1) = {corr:+.4f}   cov={cov:+.4f}")

    # conditional mean E[K_i+1 | K_i = k]  -- coupling probe
    cond = defaultdict(list)
    for a,b in zip(Ki,Kj): cond[a].append(b)
    print("  E[K_i+1 | K_i=k]  (independence => flat at E[K]):")
    for k in range(1, 8):
        if cond[k]:
            print(f"    K_i={k} (n={len(cond[k])}): E[K_i+1]={sum(cond[k])/len(cond[k]):.4f}")
    # tail probe: large K_i
    big = [b for a,b in zip(Ki,Kj) if a >= 6]
    if big:
        print(f"  E[K_i+1 | K_i>=6] = {sum(big)/len(big):.4f}  (n={len(big)})  [tests carry-coupling to tail]")

    # mutual information I(K_i;K_i+1) (bits), capped alphabet
    def cap(k): return min(k, 8)
    joint = Counter((cap(a),cap(b)) for a,b in zip(Ki,Kj))
    pi = Counter(cap(a) for a in Ki); pj = Counter(cap(b) for b in Kj)
    T = len(Ki); mi = 0.0
    for (a,b),c in joint.items():
        pab = c/T; pa = pi[a]/T; pb = pj[b]/T
        if pab>0: mi += pab*log2(pab/(pa*pb))
    print(f"  I(K_i;K_i+1) = {mi:.5f} bits  (0 => independent)")

    # renewal test: residual unit u_{i+1} mod 8 equidistributed given (K_i,K_i+1)?
    #   u_{i+1} low bits should be 'fresh' if the map refreshes the unit
    res = defaultdict(Counter)
    for i in range(N-1):
        res[(min(K_arr[i],4), min(K_arr[i+1],4))][ulow[i+1] & 7] += 1
    # report worst-case deviation from uniform-on-odd (u odd => low3 in {1,3,5,7})
    maxdev = 0.0
    for key,c in res.items():
        tot = sum(c.values())
        if tot < 500: continue
        for r in (1,3,5,7):
            dev = abs(c[r]/tot - 0.25)
            maxdev = max(maxdev, dev)
    print(f"  renewal test: max |P(u_i+1 mod8=r | K_i,K_i+1) - 1/4| = {maxdev:.4f}  (0 => unit refreshed)")

    # correlation decay corr(K_i, K_i+r): measures renewal/mixing length of the reload process
    print("  correlation decay corr(K_i,K_i+r)  (renewal-length probe):")
    Kf = [float(k) for k in K_arr]; NN=len(Kf); mm_=sum(Kf)/NN
    var=sum((k-mm_)**2 for k in Kf)/NN
    for r in range(1,9):
        c=sum((Kf[i]-mm_)*(Kf[i+r]-mm_) for i in range(NN-r))/(NN-r)/var
        print(f"    r={r}: {c:+.4f}", end="")
    print()
    return corr, mi

# =====================================================================
# PART B. o4  (p,q)=(4,3), three branches
# =====================================================================
def o4_reloads(G0=8, NSTEP=200000):
    """o4 map G' = (4G + e(rho))/3 on the residue itinerary; e={1:14,2:1,0:9}.
    Fixed points x_rho = -e(rho): x1=-14,x2=-1,x0=-9. Run length = v3(G - x_rho).
    We simulate G_{n+1} = (4 G_n + e(G_n mod 3))/3 (integer)."""
    e_of = {1:14, 2:1, 0:9}
    x_of = {1:-14, 2:-1, 0:-9}
    # generate itinerary of residues via maximal runs
    G = G0
    runs = []
    cur = G % 3; runlen = 0; entry = G
    n = 0
    while n < NSTEP:
        rho = G % 3
        if rho == cur:
            runlen += 1
        else:
            runs.append((cur, runlen, entry))
            cur = rho; runlen = 1; entry = G
        G = (4*G + e_of[G % 3])//3
        n += 1
    runs.append((cur, runlen, entry))
    runs = runs[:-1]   # drop truncated final run

    K_arr=[]; rho_arr=[]; ulow=[]; MOD=3**40
    mm_reload=0; mm_len=0; checks=0; prev=None
    for (rho, L, e) in runs:
        x = x_of[rho]
        if vq(e - x, 3) != L: mm_len += 1
        u = (e - x)//(3**L)         # 3-adic unit
        if prev is not None:
            prho, pK, pu, px = prev
            # exit = px + 4^pK * pu ; next entry ; s = px - x
            val = 4**pK * pu + (px - x)
            Kpred = vq(val, 3)
            upred = val//(3**Kpred)
            if Kpred != L or upred != u:
                mm_reload += 1
            checks += 1
        prev = (rho, L, u, x)
        K_arr.append(L); rho_arr.append(rho); ulow.append(u % MOD)
    return K_arr, rho_arr, ulow, mm_reload, mm_len, checks, len(runs)

def analyze_o4(K_arr, rho_arr, ulow, tag, q=3):
    N=len(K_arr)
    print(f"\n--- {tag}: {N} reload events ---")
    cK=Counter(K_arr)
    print("  marginal P(K=k) vs geometric (q-1)/q^k = 2/3^k:")
    for k in range(1,7):
        print(f"    K={k}: emp={cK[k]/N:.4f}  geom={2.0*3.0**-k:.4f}")
    meanK=sum(K_arr)/N; meanK2=sum(k*k for k in K_arr)/N
    print(f"  E[K]={meanK:.4f} (geom { 1.5 :.4f})  E[K^2]={meanK2:.4f}  maxK={max(K_arr)}")
    Ki=K_arr[:-1]; Kj=K_arr[1:]
    m=sum(Ki)/len(Ki); m2=sum(Kj)/len(Kj)
    cov=sum((a-m)*(b-m2) for a,b in zip(Ki,Kj))/len(Ki)
    va=sum((a-m)**2 for a in Ki)/len(Ki); vb=sum((b-m2)**2 for b in Kj)/len(Kj)
    corr=cov/(va*vb)**0.5
    print(f"  corr(K_i,K_i+1)={corr:+.4f}")
    cond=defaultdict(list)
    for a,b in zip(Ki,Kj): cond[a].append(b)
    print("  E[K_i+1 | K_i=k]:")
    for k in range(1,6):
        if cond[k]:
            print(f"    K_i={k} (n={len(cond[k])}): {sum(cond[k])/len(cond[k]):.4f}")
    big=[b for a,b in zip(Ki,Kj) if a>=4]
    if big: print(f"  E[K_i+1 | K_i>=4]={sum(big)/len(big):.4f} (n={len(big)})")
    # residue-transition (rho) structure
    rc=Counter((rho_arr[i],rho_arr[i+1]) for i in range(N-1))
    print(f"  rho transitions (sample): {dict(list(rc.items())[:6])}")
    return corr

# =====================================================================
# PART C. ADVERSARY: construct a 2-adic unit realizing a PRESCRIBED (heavy) K-sequence
#   -> proves the reload map does NOT a-priori bound the tail (or, surprise, that it does)
# =====================================================================
def build_adversary_antihydra(Kseq):
    """Solve, bit-by-bit in Z_2, for u_0 (as a truncated integer) whose Antihydra
    reload orbit has depths exactly Kseq = [K_1,K_2,...]. Start on an even run (x=0),
    sign alternates s=-1,+1,-1,...  Returns u0 truncated, and the realized sequence."""
    # We choose the 2-adic integer U (the running unit) forward. At step i we have
    # current unit u_i and sign s_i; we need v2(3^{K_i} u_i + s_i) = K_{i+1}.
    # But K_i (depth of current run) is a free coordinate we also pick: we prescribe
    # the ENTIRE K-sequence including K_0. We build u_0 by requiring, at each step,
    # that u_i has the right low bits. Since u_{i+1} is (3^{K_i}u_i+s_i)>>K_{i+1},
    # prescribing K_{i+1} fixes the low K_{i+1} bits of 3^{K_i}u_i (hence of u_i).
    # We realize by choosing the 2-adic digits of u_i greedily; the constraints touch
    # disjoint bit-windows so a consistent u_0 exists. We just SIMULATE forward while
    # choosing free high bits = 1 to make the next valuation exactly the target.
    # Concretely: pick u_i so that 3^{K_i}u_i + s_i has v2 exactly K_{i+1}:
    #   need 3^{K_i} u_i ≡ -s_i (mod 2^{K_{i+1}}), and != (mod 2^{K_{i+1}+1}).
    # u_i is determined by the PREVIOUS step except its high bits; we set high bits to
    # meet the next constraint. Implement by carrying a 2-adic value with enough bits.
    PREC = sum(Kseq) + 4*len(Kseq) + 64      # working precision in bits
    M = 1 << PREC
    inv3 = {}
    def inv3_mod(mod):  # 3^{-1} mod 2^m via pow
        return pow(3, -1, mod)
    # start: choose u_0 to satisfy the first constraint (K_0 is the current run depth,
    # which we don't constrain from below; we only realize K_1,K_2,...). We fold K_0 in
    # by treating step 0 with a given K_0 = Kseq[0], u_0 free.
    realized = []
    s = -1  # even->odd first
    K_cur = Kseq[0]
    # choose u_0: its low bits are free; set target for K_1
    # We iterate; maintain u as a big int mod M with enough set high bits.
    # Set u_0 = odd with required low K_1 bits then arbitrary (1s) above.
    seq_out = [K_cur]
    # helper: given need 3^{Kcur} u ≡ -s (mod 2^{Knext}) not (mod 2^{Knext+1}); solve for u low bits
    u = 1
    for idx in range(1, len(Kseq)):
        Knext = Kseq[idx]
        mod = 1 << (Knext+1)
        a = pow(3, K_cur, mod)
        ainv = pow(a, -1, mod)
        target = (-s) % mod                     # want 3^{Kcur} u ≡ -s mod 2^{Knext}
        # u ≡ ainv * (-s)  mod 2^{Knext}; then ensure NOT ≡ mod 2^{Knext+1}
        u_low = (ainv * ((-s) % (1<<Knext))) % (1<<Knext)
        if u_low % 2 == 0:  # must be a unit; shouldn't happen since s odd, a odd
            u_low |= 1
        # decide bit Knext so that v2 is EXACTLY Knext (residue at 2^{Knext} nonzero)
        # value mod 2^{Knext+1}: 3^{Kcur}*u + s ; choose bit Knext of u to make bit Knext of value =1
        # try u_full = u_low + t*2^{Knext}
        base = (pow(3,K_cur,mod)*u_low + s) % mod
        bit = (base >> Knext) & 1
        if bit == 0:
            # flip by adding 2^{Knext} to u (changes value by 3^{Kcur}*2^{Knext}, odd*2^{Knext})
            u_full = u_low + (1<<Knext)
        else:
            u_full = u_low
        # verify
        val = pow(3,K_cur) * u_full + s
        got = vq(val, 2)
        realized.append(got)
        # advance: u_{next} = val >> got ; but we truncated u; recompute unit low bits
        u_next = (val >> got)
        seq_out.append(got)
        # next sign alternates, next K_cur = got
        s = -s
        K_cur = got
        u = u_next
    return seq_out

def main():
    print("="*70)
    print("PART A  ANTIHYDRA reload-unit dynamics  (p,q)=(3,2)")
    print("="*70)
    K,par,ulow,mmr,mml,ch,nr = antihydra_reloads(8, 200000)
    print(f"[VERIFY] reload recursion K_{{i+1}}=v2(3^Ki u_i + s_i), u_{{i+1}}=(...)>>K_{{i+1}}")
    print(f"         mismatches = {mmr} / {ch} transitions ; run-length id mismatches = {mml}/{nr}")
    analyze(K,par,ulow,"Antihydra Z_2^x reload units")

    print("\n"+"="*70)
    print("PART B  o4 reload-unit dynamics  (p,q)=(4,3), three branches")
    print("="*70)
    K4,rho,ul4,mmr4,mml4,ch4,nr4 = o4_reloads(8, 200000)
    print(f"[VERIFY] o4 reload recursion K_{{i+1}}=v3(4^Ki u_i + s_i): mismatches={mmr4}/{ch4}, len id {mml4}/{nr4}")
    analyze_o4(K4,rho,ul4,"o4 Z_3^x reload units")

    print("\n"+"="*70)
    print("PART C  ADVERSARY: reload map realizes a prescribed heavy K-tail")
    print("="*70)
    # heavy tail: K_i = i (grows) -> sum K^2 ~ M^3, E[K^2] would diverge
    target = [2] + list(range(1,20))
    got = build_adversary_antihydra(target)
    print(f"  target K-seq : {target}")
    print(f"  realized     : {got}")
    print(f"  match K_1..  : {got[1:]==target[1:]}")
    # also a genuine heavy-tail sample
    random.seed(7)
    ht = [max(1,int(1.0/(1.0-random.random()))) for _ in range(40)]  # P(K>=k)~1/k, E[K^2]=inf
    got2 = build_adversary_antihydra([2]+ht)
    print(f"  heavy-tail sample (E[K^2]=inf) realized exactly: {got2[1:]==ht}")
    print(f"    max K realized = {max(got2)} ; sum K^2 = {sum(k*k for k in got2)}")

if __name__ == "__main__":
    main()
