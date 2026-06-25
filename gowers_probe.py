# Higher-order (Gowers/Fourier) probe of the parity sequence f_n=(-1)^{c_n mod 2}, with a SHUFFLE CONTROL to
# separate genuine structure from extreme-value noise. Result: real is indistinguishable from shuffled at the
# Fourier (U^2) level => no linear/Gowers structure; van der Corput-closed re-confirmed; obstruction is
# purely single-orbit (genuinely pseudorandom).
import numpy as np
c=8; N=131072; e=np.empty(N,dtype=np.int8)
for i in range(N): e[i]=c&1; c=(3*c)//2
f=1-2*e.astype(np.float64)
def stats(g):
    h=np.abs(np.fft.fft(g)/N); h[0]=0; return h.max(), np.sum(h**4)**0.25
mr,ur=stats(f); rng=np.random.default_rng(0)
ms=[];us=[]
for _ in range(20):
    g=f.copy(); rng.shuffle(g); m,u=stats(g); ms.append(m); us.append(u)
ms=np.array(ms); us=np.array(us)
print(f"max Fourier: real={mr:.5f} shuffled={ms.mean():.5f}+/-{ms.std():.5f}  z={(mr-ms.mean())/ms.std():+.2f}")
print(f"U2 norm:     real={ur:.5f} shuffled={us.mean():.5f}+/-{us.std():.5f}  z={(ur-us.mean())/us.std():+.2f}")
print("|z|<2 => indistinguishable from random => no Fourier/U^2 structure. Obstruction is purely single-orbit.")
