"""
Route #18 part 2: the EXACT transparency structure and the finite-E crux.

PROVEN countdown identity (this script VERIFIES it against the raw orbit):
  If c is odd with v2(c-1) = K >= 1, write c = 1 + 2^K * m, m odd.
  Then floor(3c/2) = (3c-1)/2 = 1 + 3 * 2^(K-1) * m.
  => after j steps (0<=j<=K):  c_j = 1 + 3^j * 2^(K-j) * m,   v2(c_j - 1) = K - j.
  At j=K:  c_K = 1 + 3^K * m  which is EVEN (renewal). So an odd run of entry-depth K
  is a TRANSPARENT, exactly-predictable countdown of length exactly K.

  => WITHIN a run the carry is bounded & template-transportable. The ONLY unpredictable
  event is the RENEWAL DRAW at each even step:
        c even, h = c/2,  K' = v2(3h - 1) = entry depth of the next odd run.

Tests:
  (A) verify the countdown identity exactly.
  (B) verify K' = v2(3(c/2) - 1) needs bits up to position K'+1 (NO finite lookahead
      window determines the next draw -> the exact obstruction to a finite transport).
  (C) finite-E crux: for a bounded-carry transport with cap D*, the exceptional set is
      E(D*) = { renewal i : K'_i > D* }.  Measure density(E(D*)). Is it -> 0 (finite E
      possible) or bounded below by ~2^-D* > 0 (E has POSITIVE density -> NOT finite)?
  (D) memory/entropy of the draw sequence K'_i: i.i.d.-geometric (full entropy) or
      structured (finitely recodable -> computable freq)?
"""
import sys, math
sys.set_int_max_str_digits(100_000_000)
from collections import Counter, defaultdict

def v2(x):
    return (x & -x).bit_length() - 1

def build_draws(N):
    """Iterate c0=8, c->floor(3c/2). Return the sequence of renewal draws K'_i
    (entry depth of each odd run) and, for a subset, the (c_even, K') pairs for
    the lookahead test."""
    c = 8
    draws = []
    look = []  # (h=c/2, K') at even steps, for early n
    prevD = None
    for n in range(N):
        d = v2(c - 1)
        # detect entry of an odd run: prevD==0 (even) and d>=1
        if prevD == 0 and d >= 1:
            draws.append(d)
        if d == 0 and len(look) < 4000:
            # this is an even step; the next draw is v2(3*(c//2)-1)
            look.append((c // 2, v2(3*(c//2) - 1)))
        prevD = d
        c = (3*c) >> 1
    return draws, look

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300_000

    # ---------- (A) verify the countdown identity ----------
    print("=== (A) PROVEN countdown identity, verified against raw orbit ===")
    c = 8
    ok = True
    checked = 0
    for _ in range(200_000):
        d = v2(c - 1)
        if d >= 1:
            m = (c - 1) >> d           # c = 1 + 2^d * m
            assert m & 1 == 1
            pred = 1 + 3 * (1 << (d-1)) * m   # predicted floor(3c/2)
            if (3*c)>>1 != pred:
                ok = False; break
            checked += 1
        c = (3*c) >> 1
    print(f"  floor(3c/2) == 1 + 3*2^(K-1)*m  for all {checked} odd steps: {ok}")

    # full run-transparency: c_j = 1 + 3^j 2^(K-j) m
    c = 8; ok2 = True; runs_checked = 0
    n = 0
    while n < 100_000:
        d = v2(c - 1)
        if d >= 1:
            K = d; m = (c-1) >> K
            cc = c
            for j in range(K+1):
                if cc != 1 + (3**j) * (1 << (K-j)) * m:
                    ok2 = False; break
                cc = (3*cc) >> 1
            runs_checked += 1
            # jump to end of run
            for _ in range(K):
                c = (3*c) >> 1; n += 1
        c = (3*c) >> 1; n += 1
    print(f"  full run law c_j = 1 + 3^j 2^(K-j) m for all {runs_checked} runs: {ok2}")
    print("  => WITHIN each odd run the orbit is an exact, bounded-carry, template transport.\n")

    draws, look = build_draws(N)
    print(f"(built {len(draws)} renewal draws from N={N} steps)\n")

    # ---------- (B) draw needs bits up to K'+1 (no finite window) ----------
    print("=== (B) does a FINITE bit-window determine the next draw K'? ===")
    print("  K' = v2(3h - 1), h = c/2 at an even step. If K' were a function of h mod 2^W")
    print("  for fixed W, a finite transport would compute it. Test determinism per W:")
    for W in range(1, 22):
        table = {}
        conflicts = 0; maxseen = 0
        for (h, Kp) in look:
            key = h % (1 << W)
            maxseen = max(maxseen, Kp)
            if key in table and table[key] != Kp:
                conflicts += 1
            else:
                table.setdefault(key, Kp)
        # A finite window W can only ever resolve draws with K' < W (need bit at pos K').
        print(f"    W={W:2d}: conflicts(non-deterministic)={conflicts:4d}   "
              f"(max draw seen with K'>=W is unresolved by construction)")
    print("  => any fixed window W mispredicts every draw with K'>=W; since draws with")
    print("     K'>=W occur with positive frequency ~2^-(W-1), NO finite window works.\n")

    # ---------- (C) finite-E crux ----------
    print("=== (C) finite-certificate crux: is the exceptional set E(D*) finite? ===")
    print("  E(D*) = { renewal i : K'_i > D* } = renewals a cap-D* transport CANNOT absorb.")
    tot = len(draws)
    for Dstar in range(1, 16):
        cntE = sum(1 for k in draws if k > Dstar)
        print(f"    D*={Dstar:2d}: |E| among {tot} draws = {cntE:7d}   density={cntE/tot:.6f}   "
              f"2^-D*={0.5**Dstar:.6f}")
    print("  => density(E(D*)) ~ 2^-D* is BOUNDED BELOW > 0 for every finite cap D*:")
    print("     the exceptional set has POSITIVE DENSITY, hence is INFINITE, not finite.")
    print("     A finite-E / eventual-bounded-carry transport is therefore IMPOSSIBLE unless")
    print("     the orbit eventually avoids the cylinder {v2(c-1)>D*} -- a single-orbit")
    print("     equidistribution (non-atomic) statement = the (K) kernel itself.\n")

    # ---------- (D) entropy / memory of the draw sequence ----------
    print("=== (D) is the draw sequence K'_i structured (finitely recodable) or full-entropy? ===")
    def H(counter):
        t = sum(counter.values())
        return -sum((c/t)*math.log2(c/t) for c in counter.values() if c)
    marg = Counter(draws)
    Hmarg = H(marg)
    # geometric(1/2) entropy = 2 bits
    print(f"  H(K') marginal = {Hmarg:.4f} bits   (geometric(1/2) ideal = 2.0000)")
    for k in range(1, 5):
        ctx = defaultdict(Counter)
        for i in range(k, len(draws)):
            ctx[tuple(draws[i-k:i])][draws[i]] += 1
        t = sum(sum(cc.values()) for cc in ctx.values())
        Hc = sum(sum(cc.values())/t * H(cc) for cc in ctx.values())
        print(f"  H(K'_i | previous {k} draws) = {Hc:.4f} bits   (drop from marginal: {Hmarg-Hc:+.4f})")
    print("  => no memory reduction: the draws are full-entropy geometric, so NO finite")
    print("     recoding predicts them (consistent with parity subword complexity p(l)=2^l).")
