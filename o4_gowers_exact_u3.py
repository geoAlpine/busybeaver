#!/usr/bin/env python
"""Exact full-h U^3 cross-check (no shift sampling) for f=e(W_n/3), o4 seed 43,
comparing f vs shuffle controls under identical treatment, at N=8192, 16384.
Also injected quadratic control to confirm exact-U3 detects genuine 2-step structure."""
import numpy as np, math, time
OMEGA=np.exp(2j*np.pi/3); E={0:9,1:14,2:1}
def resid(N,G0=43):
    G=G0; r=np.empty(N,dtype=np.int8)
    for n in range(N):
        r[n]=(G+14)%3; G=(4*G+E[G%3])//3
    return r
def U3_exact(f):
    N=len(f); fc=np.conj(f); acc=0.0
    for h in range(N):
        F=np.fft.fft(np.roll(f,-h)*fc)/N
        acc+=np.sum(np.abs(F)**4).real
    return (acc/N)**0.125
def U2(f):
    F=np.fft.fft(f)/len(f); return (np.sum(np.abs(F)**4).real)**0.25
for N in (8192,16384):
    r=resid(N); f=OMEGA**r.astype(np.int64)
    t=time.time(); u3=U3_exact(f)
    rng=np.random.default_rng(0); ss=[]
    for _ in range(8):
        g=f.copy(); rng.shuffle(g); ss.append(U3_exact(g))
    ss=np.array(ss)
    # injected quadratic (genuine 2-step) as positive control
    n=np.arange(N); fq=np.exp(2j*np.pi*((math.sqrt(5)-1)/2)*n*n)
    print(f"N={N}: U3(f)={u3:.7e}  shuffle={ss.mean():.7e}+/-{ss.std():.1e}"
          f"  z={(u3-ss.mean())/ss.std():+.2f}  U2(f)={U2(f):.5e}"
          f"  | U3(quad)={U3_exact(fq):.5e} U2(quad)={U2(fq):.5e}  ({time.time()-t:.0f}s)")
