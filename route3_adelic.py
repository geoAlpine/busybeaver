# Route 3 resolved: x->(3/2)x is a HYPERBOLIC automorphism of the solenoid (R x Q_2 x Q_3)/Z[1/6].
# |3/2|_inf=3/2, |3/2|_2=2 (expanding); |3/2|_3=1/3 (contracting=stable). Product=1 (hyperbolic, no neutral dir).
# => ergodic+mixing => a.e. orbit equidistributes (provable). Single orbit (seed 8) = the a.e.->specific wall.
import mpmath as mp
mp.mp.dps=50
inf=mp.mpf(3)/2; p2=mp.mpf(2); p3=mp.mpf(1)/3
print(f"|3/2|_inf={float(inf)} (EXP), |3/2|_2={float(p2)} (EXP), |3/2|_3={float(p3):.4f} (CONTRACT=stable)")
print(f"product formula |3/2|_inf*|3/2|_2*|3/2|_3 = {float(inf*p2*p3)} (=1 => hyperbolic automorphism of the solenoid)")
print("=> hyperbolic => ergodic/mixing => a.e. orbit equidistributes [provable]; single specified orbit = wall.")
print("Named target: rank-1 single-orbit equidistribution on a hyperbolic S-arithmetic solenoid (homogeneous dynamics).")
