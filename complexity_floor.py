"""Push the proven floor up and locate the provable/Mahler boundary in COMPLEXITY terms.

STRUCTURAL LEMMA (verify): the coding map  phi_l : Z/2^l -> {0,1}^l,  phi_l(c) = (c mod 2, T(c) mod 2,
..., T^{l-1}(c) mod 2)  with T(c)=floor(3c/2),  is a BIJECTION (the base-3/2 odometer's unique coding).
=> the length-l parity factor starting at step n depends only on c_n mod 2^l, and DISTINCT residues give
DISTINCT factors. Hence  p(l) = #{ c_n mod 2^l : n >= 0 }  = number of residues mod 2^l the orbit visits.

PROVEN FLOOR (no Mahler):
  - r_n is not eventually periodic (proven_nonperiodic.py) => by MORSE-HEDLAND, p(l) >= l+1 for all l.
  - p(2)=4 (all four 2-blocks 00,01,10,11 occur -- exhibited explicitly) => NOT Sturmian (p(l)=l+1):
    the parity sits strictly above the minimal-complexity aperiodic (Sturmian) class too.
  - finite certificates: p(l) >= (#distinct length-l factors observed in a finite prefix), e.g. p(16)>=65526.
MAHLER-CLASS PART:
  - p(l) = 2^l for all l  <=>  the orbit visits EVERY residue mod 2^l  <=>  equidistribution of c_n mod 2^l
    => this is the specified-orbit equidistribution = Mahler. So 'maximal complexity / non-automatic' is
    exactly the Mahler barrier; the elementary floor stops at p(l) >= l+1 (+ finite certificates).
0 false proofs: the bijection is verified exhaustively for l<=14; floor facts are elementary; the maximal
part is labelled Mahler-class (not claimed proven).
"""

def T(c): return (3 * c) // 2

def phi(c, l):
    w = 0
    for i in range(l):
        w = (w << 1) | (c & 1)
        c = T(c)
    return w

# (1) verify phi_l : Z/2^l -> {0,1}^l is a bijection
print("(1) bijection check  phi_l: Z/2^l -> {0,1}^l  (base-3/2 odometer coding):")
allbij = True
for l in range(1, 15):
    seen = set()
    mod = 1 << l
    for c in range(mod):
        seen.add(phi(c, l))
    bij = (len(seen) == mod)
    allbij &= bij
    if l <= 6 or not bij:
        print(f"    l={l:>2}: |image|={len(seen):>5} of {mod:>5} -> {'bijection' if bij else 'NOT bijection'}")
print(f"    ... all l=1..14: {'ALL bijections' if allbij else 'FAILS somewhere'}")
print(f"    => length-l parity factor <-> c_n mod 2^l;  p(l) = #residues mod 2^l the orbit visits.")

# (2) proven floor: exhibit all four 2-blocks explicitly (=> p(2)=4, not Sturmian)
c = 8; pos = {}
seqpos = []
for n in range(100):
    seqpos.append(c & 1); c = T(c)
blocks2 = {}
for n in range(len(seqpos)-1):
    b = (seqpos[n], seqpos[n+1])
    blocks2.setdefault(b, n)
print("\n(2) proven floor -- all four 2-blocks exhibited in the first 100 steps (finite certificate):")
for b in [(0,0),(0,1),(1,0),(1,1)]:
    print(f"    block {b} first occurs at n={blocks2.get(b,'NOT FOUND')}")
print(f"    => p(2) = 4 > 3 = 2+1  => the parity is NOT Sturmian (strictly above minimal-complexity aperiodic).")

# (3) Morse-Hedlund corollary + the boundary statement
print("""
(3) PLACEMENT (provable/Mahler boundary in complexity terms):
    PROVEN (elementary, no Mahler):
      * r_n not eventually periodic (proven_nonperiodic.py)  =>  p(l) >= l+1 for ALL l  [Morse-Hedlund].
      * p(2)=4 (exhibited)  =>  NOT Sturmian: strictly above the minimal aperiodic class.
      * finite certificates: p(l) >= #distinct factors seen (p(16) >= 65526, measured earlier).
    MAHLER-CLASS (not elementary):
      * p(l) = 2^l for all l  <=>  orbit hits every residue mod 2^l  <=>  equidistribution of c_n mod 2^l.
        This 'maximal complexity / full non-automaticity' IS the specified-orbit equidistribution = Mahler.
    BOUNDARY: elementary methods give p(l) >= l+1 (linear floor) and 'not Sturmian'; the jump to the
    measured p(l)=2^l (maximal) is exactly the Mahler barrier. The certificate-hierarchy placement thus
    has a PROVEN lower part (above eventually-periodic and above Sturmian) and a Mahler-class upper part
    (maximal complexity / non-automatic). This locates precisely where the elementary floor stops.""")
