# o18: dissect one generation's compressed event stream -> identify sweep cycles + body word,
# check affine chunk counts across N (prep for the certified body lemma).
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_template_scan import run_epoch, compress, l2, M

names = "ABCDEF"

def tokname(b):
    return f"{names[b // 2]}{b % 2}"

for N in ([int(x) for x in sys.argv[1:]] or [30, 33, 31, 34, 32, 35]):
    status, toks, land, steps, unsafe = run_epoch(N)
    ch = compress(toks)
    out = l2(ch)
    print(f"\n=== N={N} (mod3={N%3}) status={status} land={land} steps={steps} ===")
    for c in out:
        if c[0] == 'B':
            body = c[1]
            desc = ' '.join(('[' + ''.join(tokname(b) for b in u) + ']') if tt == 'R' else tokname(u)
                            for tt, u in body)
            print(f"  BODY x{c[2]}: {desc}")
        elif c[0] == 'R':
            print(f"  SWEEP [{''.join(tokname(b) for b in c[1])}]")
        else:
            print(f"  {tokname(c[1])}")
    # sweep-length affinity: counts of each 'R' chunk unit at level 1
    from collections import defaultdict
    lens = defaultdict(list)
    for cc in ch:
        if cc[0] == 'R':
            lens[bytes(cc[1])].append(cc[2])
    for u, ks in sorted(lens.items()):
        nm = ''.join(tokname(b) for b in u)
        print(f"  L1 cycle [{nm}]: counts {ks[:14]}{'...' if len(ks) > 14 else ''}")
