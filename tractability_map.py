# Tractability map: cousins of Antihydra where single-orbit equidistribution/structure is PROVABLE, and what 3/2 lacks.
import mpmath as mp
mp.mp.dps=800
phi=(1+mp.sqrt(5))/2; psi=(1-mp.sqrt(5))/2
print("PISOT phi: {phi^n}->0/1 via archimedean conjugate psi=%.3f decay:"%float(psi))
for n in (10,30,60,100): print(f"  n={n}: frac={float(mp.frac(phi**n)):.6f} |psi^n|={float(abs(psi)**n):.1e}")
print("3/2 (non-Pisot): frac((3/2)^n)=(3^n mod 2^n)/2^n, generic, no decay:")
for n in (10,30,60,100): print(f"  n={n}: frac={(pow(3,n,2**n))/2**n:.6f}")
print("adelic-Pisot test: |(3/2)^n|_3=3^-n->0 but archimedean dist-to-integer is GENERIC (Pisot mechanism fails):")
for n in (10,30,60):
    v=mp.mpf(3)**n/mp.mpf(2)**n; print(f"  n={n}: dist_to_int={float(min(mp.frac(v),1-mp.frac(v))):.6f}")
print("3/2 lacks {unique ergodicity, linearity, archimedean conjugate decay}; new tool must supply a substitute.")
