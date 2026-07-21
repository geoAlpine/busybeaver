#!/usr/bin/env python3
"""
D9 probe, stage 1: generate the Antihydra induced (odd) orbit data.

c_0 = 8, c -> floor(3c/2).  D_i := v2(3*c_i - 1)  (this is 0 automatically on even c_i,
since 3c-1 is odd there), so the exact first-moment budget identity to verify is

    sum_{i<n} D_i  =  n + v2(c_n) - v2(c_0)                      [claimed exact]

Induced odd map: from odd o, next odd is o' = 3^{D-1}(3o-1)/2^D with D = v2(3o-1);
it consumes exactly D c-steps.

Outputs (npz):
  D    : uint8 array of induced depths D_j
  tc   : int64 array of the c-step index at which odd visit j occurs
  res  : int32 array (J x len(MODULI)) of o_j mod m
"""
import numpy as np, time, sys

MODULI = [3, 5, 7, 11, 13, 17, 19, 23]

def v2(x):
    return (x & -x).bit_length() - 1

def run(n_csteps, out):
    c = 8
    c0v2 = v2(c)
    budget = 0            # sum of D_i over c-steps
    Ds, tcs = [], []
    res = [[] for _ in MODULI]
    # track c mod m cheaply: c_{n+1} = (3c_n - odd)/2, so u <- (3u - odd)*inv2 mod m
    U = [8 % m for m in MODULI]
    INV2 = [pow(2, -1, m) for m in MODULI]
    bad = 0
    t0 = time.time()
    check_at = set(int(x) for x in np.unique(np.geomspace(1, n_csteps, 200).astype(np.int64)))
    ident_ok = True
    ident_checks = 0
    for n in range(n_csteps):
        odd = c & 1
        if odd:
            D = v2(3 * c - 1)
            Ds.append(D)
            tcs.append(n)
            for k in range(len(MODULI)):
                res[k].append(U[k])
        else:
            D = 0
        budget += D
        # step
        c = (3 * c) >> 1 if not odd else (3 * c - 1) >> 1
        for k, m in enumerate(MODULI):
            U[k] = ((3 * U[k] - odd) * INV2[k]) % m
        if (n + 1) in check_at:
            ident_checks += 1
            if budget != (n + 1) + v2(c) - c0v2:
                ident_ok = False
                bad += 1
        if (n % 200000) == 0:
            print(f"  n={n} bits={c.bit_length()} t={time.time()-t0:.1f}s", flush=True)
    print(f"identity checks={ident_checks} all_ok={ident_ok} failures={bad}")
    print(f"final: n={n_csteps} sumD={budget} n+v2(c_n)-v2(c_0)={n_csteps+v2(c)-c0v2}")
    D = np.array(Ds, dtype=np.uint8)
    tc = np.array(tcs, dtype=np.int64)
    R = np.array(res, dtype=np.int32).T
    np.savez_compressed(out, D=D, tc=tc, res=R, moduli=np.array(MODULI))
    print(f"induced steps J={len(D)}  mean D={D.mean():.6f}  max D={D.max()}  time={time.time()-t0:.1f}s")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    run(n, sys.argv[2] if len(sys.argv) > 2 else "d9_orbit.npz")
