"""x2rm_regen_reach.py -- symbol-by-symbol: does regen{4,5}_transport's OUT
equal descent_glue's IN at a=4 / a=5?  Parses the EXACT cons-lists out of
lean/X2.lean (no hand transcription) and compares as run-length words.
Read-only on lean/.
"""
import re, sys

SRC = open("lean/X2.lean").read()

def grab(name):
    i = SRC.index("theorem " + name)
    j = SRC.index(":= by", i)
    return SRC[i:j]

def parse_cons(s):
    """Parse a Lean cons-chain of true/false/ones n/zeros n/pow01 n/pow10 n/descCascade n/L/R
    into a list of tokens. Returns list of ('lit',bool) / ('sym',name,arg)."""
    toks = []
    # normalise
    s = s.replace("\n", " ")
    for part in [p.strip() for p in s.split("::")]:
        part = part.strip()
        if part.startswith("(") and not part.endswith(")"):
            part = part.lstrip("(").strip()
        part = part.strip("() ").strip()
        if part == "true": toks.append(True)
        elif part == "false": toks.append(False)
        elif part: toks.append(part)   # tail expression (may contain ++)
    return toks

def ones(n): return [True]*n
def zeros(n): return [False]*n
def pow01(n): return [False,True]*n
def pow10(n): return [True,False]*n
def descCascade(d):
    if d == 0: return ones(1)
    return ones(2**(d+2+1-1+0) - 3) if False else ones(2**(d+3-1) - 3) + [False,False] + descCascade(d-1)
# careful: def descCascade | (d+1) => ones (2^(d+3) - 3) ++ 0::0::descCascade d
def descCascade(d):
    if d == 0: return ones(1)
    dd = d - 1                    # d = dd+1
    return ones(2**(dd+3) - 3) + [False, False] + descCascade(dd)

def rle(w):
    out=[]
    for b in w:
        if out and out[-1][0]==b: out[-1][1]+=1
        else: out.append([b,1])
    return [(("1" if b else "0")+"^"+str(n)) for b,n in out]

# ---- descent_glue IN (read from source, line ~5889) ----
# right = 0::0::0::(ones (2N+1) ++ 0::0::(descCascade (d+1) ++ 0::0::(zeros 7 ++ R)))
# left  = pow01 (Lc+N) ++ marker
def glue_in_right(N, dp1):
    return zeros(3) + ones(2*N+1) + zeros(2) + descCascade(dp1) + zeros(2) + zeros(7)   # ++ R
def glue_in_left(LcN):
    return pow01(LcN)   # ++ marker

# ---- extract regen OUT tails from the Lean source ----
def out_of(name):
    st = grab(name)
    # OUT is the RHS of "= some <cfg>"
    k = st.index("= some")
    return st[k:]

def explicit_prefix(toks):
    """leading run of literal bools before the first symbolic tail"""
    pre=[]
    for t in toks:
        if isinstance(t,bool): pre.append(t)
        else: return pre, t
    return pre, None

report = []
for name, a in (("regen4_transport",4), ("regen5_transport",5)):
    body = out_of(name)
    # cfg = ⟨.E, pos, ⟨LEFT, head, RIGHT⟩⟩ ; split on the inner ⟨ ⟩
    pos = re.search(r"some\s*⟨\.E,\s*(-?\d+),", body).group(1)
    inner = body[body.index("⟨", body.index("⟨")+1)+1:]
    # split top-level commas of the tape triple
    depth=0; parts=[]; cur=""
    for ch in inner:
        if ch in "(⟨": depth+=1
        if ch in ")⟩":
            if depth==0: break
            depth-=1
        if ch=="," and depth==0: parts.append(cur); cur=""; continue
        cur+=ch
    parts.append(cur)
    left_s, head_s, right_s = parts[0], parts[1].strip(), parts[2]
    lt = parse_cons(left_s); rt = parse_cons(right_s)
    lpre, ltail = explicit_prefix(lt)
    rpre, rtail = explicit_prefix(rt)

    N = 2**(a-1) - 2
    dp1 = a - 3
    want_r = glue_in_right(N, dp1)
    want_l = glue_in_left(None) if False else None

    report.append((name, a, pos, head_s, lpre, ltail, rpre, rtail, N, dp1, want_r))

for (name,a,pos,head,lpre,ltail,rpre,rtail,N,dp1,want_r) in report:
    print("="*72)
    print(f"{name}   (target: descent_glue IN at a={a}: N={N}, d+1={dp1})")
    print(f"  OUT pos = {pos}   head = {head}")
    print(f"  OUT left  explicit = {rle(lpre)}  ++ tail `{ltail}`")
    print(f"  OUT right explicit = {rle(rpre)}  ++ tail `{rtail}`")
    print(f"  GLUE IN right (before R) = {rle(want_r)}")
    print(f"  GLUE IN left  (before marker) = pow01(Lc+{N}) = {rle(pow01(N))} (Lc=0 shown)")
    # RIGHT check: is want_r a prefix-compatible match?
    n = min(len(rpre), len(want_r))
    if rpre == want_r[:len(rpre)]:
        resid = want_r[len(rpre):]
        print(f"  RIGHT: OUT explicit is a PREFIX of GLUE IN. residue needed = {rle(resid)}  "
              f"=> instantiate regen R := zeros {len(resid)} ++ R'    [{'MATCH' if all(x==False for x in resid) else 'MISMATCH-nonzero residue'}]")
    else:
        for i,(x,y) in enumerate(zip(rpre,want_r)):
            if x!=y:
                print(f"  RIGHT: FIRST DIVERGENCE at cell {i}: OUT={int(x)} GLUE={int(y)}")
                break
        else:
            print(f"  RIGHT: GLUE IN is prefix of OUT explicit; OUT has extra {rle(rpre[len(want_r):])}")
    # LEFT check
    wl = pow01(64)   # long enough
    if lpre == wl[:len(lpre)]:
        print(f"  LEFT : OUT explicit {rle(lpre)} agrees with pow01 prefix -> instantiate "
              f"L := (pow01 tail from cell {len(lpre)}) ++ marker   [MATCH]")
    else:
        print(f"  LEFT : DIVERGES from pow01 at cell "
              f"{next(i for i,(x,y) in enumerate(zip(lpre,wl)) if x!=y)}  [MISMATCH]")
