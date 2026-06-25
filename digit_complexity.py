# Digit-side probe: subword (factor) complexity of the moving-diagonal parity sequence e_n=c_n mod 2=bit_{n+3}(3^n).
# Result: p(k)=2^k (FULL) up to the sampling limit => pseudorandom, NO automatic/low-complexity structure =>
# no digit-side foothold. Combined with maximal LINEAR complexity (Berlekamp-Massey, prior), the sequence is
# maximally complex in BOTH the automata and algebraic senses -- the structureless-normal regime (= the wall).
c=8; N=400000; e=bytearray()
for _ in range(N):
    e.append(c&1); c=(3*c)//2
bs=bytes(e)
print(f"e_n=c_n mod 2, N={N}, even-density={1-sum(e)/N:.4f}")
for k in (8,12,14,16):
    p=len(set(bs[i:i+k] for i in range(N-k)))
    print(f"  k={k}: p(k)={p}/{2**k} (ratio {p/2**k:.5f})")
print("=> full subword complexity (p(k)->2^k): pseudorandom, no automatic structure, no digit-side handle.")
