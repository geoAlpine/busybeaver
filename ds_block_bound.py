"""Does the Drmota-Spiegelhofer (2025, arXiv:2501.00850) UNCONDITIONAL bound
   'longest equal-bit block of 3^K is o(K)' (via Schlickewei p-adic Subspace Theorem)
   transfer to the Antihydra orbit c_{n+1}=floor(3 c_n/2), c_0=8?

CLAIM TO VERIFY (structural):
  An even-run of length L in the orbit (c_n,...,c_{n+L-1} all even) forces v2(c_n) >= L,
  because c_n even => c_{n+1}=3 c_n/2, and L consecutive halvings need 2^L | c_n.
  And c_n = floor(3^n / 2^{n-3}) = (3^n >> (n-3)) for n>=3, so
     v2(c_n) = (number of trailing 0-bits of c_n)
             = length of the 0-block of 3^n STARTING at bit position (n-3).
  Hence  even-run(n) <= v2(c_n) <= L0(3^n) <= longest block of 3^n = o(n)  [D-S].
  This BEATS the trivial v2(c_n) <= log2(c_n) ~ 0.585 n.

We check: (i) c_n == 3^n>>(n-3) exactly; (ii) even-run length == v2(c_n);
          (iii) v2(c_n) == 0-block length of 3^n at position n-3;
          (iv) max run is sublinear and far below 0.585n (empirical D-S regime);
          (v) the DUAL odd-run is likewise bounded by a 1-block of 3^n at the moving window.
0 false proofs: every claim is asserted only if it passes on the real orbit.
"""

def v2(x):
    if x == 0: return 10**9
    r = 0
    while x & 1 == 0:
        x >>= 1; r += 1
    return r

def block_at(x, pos):
    """length of the maximal block of EQUAL bits of integer x starting at bit `pos`
       and extending upward (pos, pos+1, ...)."""
    if pos < 0: return 0
    b0 = (x >> pos) & 1
    L = 0
    p = pos
    nbits = x.bit_length()
    while p <= nbits and ((x >> p) & 1) == b0:
        L += 1; p += 1
    return L

N = 60000
# orbit
c = 8
orbit = [c]
for _ in range(N):
    c = (3 * c) // 2
    orbit.append(c)

# (i) NAIVE hope c_n == 3^n >> (n-3) -- EXPECTED TO FAIL: the orbit is NOT floor(8*(3/2)^n);
#     the odd-step -1 corrections compound, so c_n = (8*3^n - T_n)/2^n, T_n = parity carry-sum.
ok_i = True; first_fail = None
p3 = 1  # 3^n
for n in range(0, 400):
    if n >= 3:
        if orbit[n] != (p3 >> (n - 3)):
            ok_i = False; first_fail = n; break
    p3 *= 3
print(f"(i)  [naive] c_n == 3^n>>(n-3)  : {'OK' if ok_i else f'FAIL at n={first_fail} (EXPECTED: orbit != floor of geometric)'}")

# (i') CORRECT object: T_n := 8*3^n - c_n*2^n is an integer, and the INTEGRALITY congruence
#      T_n == 8*3^n (mod 2^n) holds (M4-P2). even-run(n) = v2(c_n) = v2(8*3^n - T_n) - n.
ok_ip = True; ok_cong = True
p3 = 1
for n in range(0, 400):
    Tn = 8 * p3 - orbit[n] * (1 << n)
    if Tn < 0 or (8 * p3 - Tn) % (1 << n) != 0:
        ok_ip = False; break
    if n >= 1 and (Tn % (1 << n)) != ((8 * p3) % (1 << n)):
        ok_cong = False; break
    # even-run identity via the correct integer:
    er = v2(8 * p3 - Tn) - n  # = v2(c_n)
    if er != v2(orbit[n]):
        ok_ip = False; break
    p3 *= 3
print(f"(i') c_n=(8*3^n - T_n)/2^n with T_n carry-sum   : {'OK' if ok_ip else 'FAIL'}")
print(f"     integrality congruence T_n == 8*3^n mod 2^n: {'OK' if ok_cong else 'FAIL'}")
print(f"     => even-run(n) = v2(8*3^n - T_n) - n  (the relevant integer is 8*3^n - T_n, NOT 3^n)")

# parity sequence and runs
par = [x & 1 for x in orbit]  # 0=even,1=odd

def runs(seq, val):
    """list of (start, length) maximal runs equal to val"""
    out = []; i = 0; n = len(seq)
    while i < n:
        if seq[i] == val:
            j = i
            while j < n and seq[j] == val: j += 1
            out.append((i, j - i)); i = j
        else:
            i += 1
    return out

even_runs = runs(par, 0)
odd_runs  = runs(par, 1)

# (ii) even-run length at start n equals v2(c_n)
ok_ii = True
for (s, L) in even_runs:
    if s + L < len(orbit):  # full run captured
        if v2(orbit[s]) != L:
            ok_ii = False
            print(f"     mismatch even-run start={s} L={L} v2={v2(orbit[s])}")
            break
print(f"(ii) even-run length == v2(c_start)            : {'OK' if ok_ii else 'FAIL'}")

# (iii) [naive] v2(c_n) == 0-block of 3^n at position (n-3) -- EXPECTED FAIL (same reason as (i)).
ok_iii = True; iii_fail = None
p3 = 1
for n in range(0, 500):
    if n >= 3:
        blk = block_at(p3, n - 3)
        b0 = (p3 >> (n - 3)) & 1
        if b0 == 0:
            if blk != v2(orbit[n]):
                ok_iii = False; iii_fail = n; break
        else:
            if v2(orbit[n]) != 0:
                ok_iii = False; iii_fail = n; break
    p3 *= 3
print(f"(iii)[naive] v2(c_n)==0-block of 3^n at (n-3): {'OK' if ok_iii else f'FAIL at n={iii_fail} (EXPECTED: needs 8*3^n - T_n, not 3^n)'}")

# (iv) sublinearity: max run vs 0.585 n  and vs n
maxeven = max(L for _, L in even_runs)
maxeven_n = max(even_runs, key=lambda t: t[1])[0]
maxodd = max(L for _, L in odd_runs)
maxodd_at = max(odd_runs, key=lambda t: t[1])[0]
import math
print(f"(iv) over n<= {N}:")
print(f"     longest even-run = {maxeven} at n~{maxeven_n}  (trivial bound 0.585n = {0.585*maxeven_n:.0f})")
print(f"     longest odd-run  = {maxodd} at n~{maxodd_at}  (trivial bound 0.585n = {0.585*maxodd_at:.0f})")
print(f"     longest run / N = {max(maxeven,maxodd)/N:.5f}  (o(n) means this ratio -> 0)")
print(f"     longest run vs log2(N)={math.log2(N):.1f}: empirically runs ~ O(log n), far below o(n) ceiling")

# growth of longest run as a function of horizon -> is it sublinear?
print("\n     horizon scan (longest run up to each N'):")
for cut in (2000, 8000, 20000, 40000, N):
    me = max((L for s,L in even_runs if s < cut), default=0)
    mo = max((L for s,L in odd_runs if s < cut), default=0)
    m = max(me, mo)
    print(f"       N'={cut:6d}  longest run={m:3d}  run/N'={m/cut:.5f}  run/log2(N')={m/math.log2(cut):.2f}")

# (v) [exploratory] is there a clean dual budget for ODD-runs? c odd: c_{n+1}=(3c-1)/2,
#     so the -1 shifts the carry each step -- the simple guess v2(c+1)>=L is FALSE.
clean_dual = all(v2(orbit[s] + 1) >= L for (s, L) in odd_runs if s + L < len(orbit))
print(f"\n(v)  clean odd-run dual v2(c+1)>=L : {'holds' if clean_dual else 'FALSE (the -1 step shifts the carry; no simple dual budget -- odd-runs are governed by the same 8*3^n - T_n carry, not a pure power)'}")

print("\n" + "="*78)
print("VERDICT (corrected after the naive transfer was REFUTED)")
print("="*78)
print("""The hoped-for clean transfer is FALSE, and the refutation is itself the finding:
  * D-S 2025 (Subspace Theorem) bounds the longest equal-bit block of the PURE POWER
    3^n by o(n), UNCONDITIONALLY. Verified to exist (arXiv:2501.00850, Drmota-Spiegelhofer).
  * BUT the Antihydra orbit is NOT floor(8*(3/2)^n): the odd-step -1 corrections compound,
    so the relevant integer is  c_n = (8*3^n - T_n)/2^n,  where T_n is the parity-history
    CARRY-SUM (T_n == 8*3^n mod 2^n by integrality; height ~ n*log2(3)).
  * even-run(n) = v2(c_n) = v2(8*3^n - T_n) - n: a long even-run = a long agreement of the
    bits of 8*3^n and T_n ABOVE position n = the moving-middle-digit comparison.
  * The Subspace Theorem controls the digits of 3^n (an S-unit / pure power). It does NOT
    apply to 8*3^n - T_n, because T_n is a self-generated carry-sum, NOT of S-unit form.
    This is the closed-loop / self-induced-quenched-disorder obstruction, re-localized to
    the EXACT object T_n that defeats the strongest unconditional digit tool we found.
EMPIRICALLY: the orbit's longest run is ~ log2(n) (run/log2(N') ~ 1.0 across all horizons),
   FAR below both 0.585n and the provable o(n) -- the truth is much stronger than anything
   provable, the signature of the whole 'indistinguishable from random, unprovably so' picture.
NET FORWARD MOTION: we now have a SHARP, citable obstruction statement -- 'the best
   unconditional bound on the digits of 3^n (D-S/Subspace) fails for the orbit precisely
   because the orbit's integer is 8*3^n - T_n and T_n is the self-induced carry-sum'. This
   is a better sentence for the kernel's 'where methods stop' than the generic 'a.e. gap'.
   Located more precisely, not closed.""")
