# Frequency-axis check: the run-depth sequence of an explicit x(p/q) orbit is white +
# conditionally structureless (2026-07-08). Reproduces FREQUENCY_AXIS_PROBE_2026-07-08.md.
# By the uniform fixed-point theorem, the run-depth d_i = v_q(entry_i - x_branch); this
# script measures that sequence's autocorrelation and conditional entropy for the o4 orbit.
import math, statistics
from collections import Counter

e = {0: 9, 1: 14, 2: 1}                      # o4 odometer 3G' = 4G + e(rho)
def step(G):
    r = G % 3
    return r, (4 * G + e[r]) // 3

def run_depths(G0, N):
    G = G0; ds = []; cur = None; L = 0
    for _ in range(N):
        r, G = step(G)
        if r == cur:
            L += 1
        else:
            if cur is not None: ds.append(L)
            cur = r; L = 1
    return ds

def report(ds, name):
    mu = sum(ds) / len(ds); var = statistics.pvariance(ds)
    print(f"{name}: n={len(ds)}, mean={mu:.4f} (geom(1/q) mean; here 1.5), max={max(ds)}")
    for lag in (1, 2, 3, 5, 10):
        c = sum((ds[i]-mu)*(ds[i+lag]-mu) for i in range(len(ds)-lag))/((len(ds)-lag)*var)
        print(f"  autocorr lag {lag:>2}: {c:+.4f}")
    cap = lambda x: min(x, 6)
    cds = [cap(x) for x in ds]; tot = len(cds)
    marg = Counter(cds)
    Hm = -sum((v/tot)*math.log2(v/tot) for v in marg.values())
    ctx = Counter(); joint = Counter()
    for i in range(3, len(cds)):
        k = tuple(cds[i-3:i]); ctx[k] += 1; joint[(k, cds[i])] += 1
    Hcond = 0.0
    for (k, d), n in joint.items():
        Hcond -= (n/(len(cds)-3)) * math.log2(n/ctx[k])
    print(f"  H(d_n)={Hm:.4f}  H(d_n|last3)={Hcond:.4f}  gap={Hm-Hcond:.4f} ({100*(Hm-Hcond)/Hm:.2f}%)")
    ok = abs(sum((ds[i]-mu)*(ds[i+1]-mu) for i in range(len(ds)-1))/((len(ds)-1)*var)) < 0.01 and (Hm-Hcond) < 0.01
    print(f"  WHITE + CONDITIONALLY STRUCTURELESS: {ok}")
    return ok

if __name__ == "__main__":
    ds = run_depths(43, 2_000_000)[:300000]
    ok = report(ds, "o4 run-depth (x4/3, v3)")
    print("VERIFIED [OBSERVED]: the run-depth sequence is white and finite-memory-free"
          if ok else "UNEXPECTED -- investigate")
    print("No machine decided. No label upgraded.")
