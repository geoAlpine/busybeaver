# D の rung タイル — `∀`-parametric に **[PROVEN]**(2026-07-26)

`lean/DMachine.lean`。`lake build` EXIT=0(コーパス 77 jobs 全緑)、公理は
`[propext, Quot.sound]` のみ、`sorryAx` 0、`Classical.choice` 0、`sorry`/`native_decide`/`decide`
いずれも不使用。

**D は依然 `[OPEN]`。本文書は機械を決着させず、ラベルを昇格させない。** 閉じたのは
`SYNTHESIS_2026-07-26.md` §6 Tier I-1 の着手項目 **(a) のみ**。

---

## §0 結果

```lean
theorem rungTile (u m c g : Nat) (p : Int) (TAIL REST : List Bool) :
    steps dT (6 * (u + m) + 21) (IN u (m + 1) c (g + 3) p TAIL REST)
      = some (IN (u + 2) m (c + 1) g (p + 3) TAIL REST)
```

`IN` の literal な引数で書けば `steps (6(u+m)+15) IN(u,m,c,g) = IN(u+2, m−1, c+1, g−3)` at `pos+3`
(`m ≥ 1`, `g ≥ 3`, `c ≥ 0`, `TAIL`/`REST` 任意)。D の epoch 33 セグメント中 30 を担う唯一の補題。

---

## §1 前セッションの記述に対する 2 つの訂正(いずれも実測が先)

### (1) `RungTile : Prop` の span が 6 歩不足していた — **修正済み**

前版は `steps dT (6*(u+m)+15) (IN u (m+1) …)` と書かれていた。`IN` の第2引数が `m+1` である
ぶん、正しい span は `6*(u+m)+21`。**kernel-`rfl` の3インスタンス(span 21/33/45)は最初から
正しく、誤っていたのは `Prop` の側だけ**だった。両読みを並べて再測定したのが
`d_rung_general.py §A`:

```
u=0 m_literal=1:  6(u+m)+15=21 -> OK   RungTile's 6(u+m-1)+15=15 -> FAIL
u=1 m_literal=2:  6(u+m)+15=33 -> OK   RungTile's 6(u+m-1)+15=27 -> FAIL
u=2 m_literal=3:  6(u+m)+15=45 -> OK   RungTile's 6(u+m-1)+15=39 -> FAIL
u=3 m_literal=1:  6(u+m)+15=39 -> OK   RungTile's 6(u+m-1)+15=33 -> FAIL
```

`RESUME_2026-07-26.md` §3 の「`d_tile_check.py` が最初の具体 span 15/27/39 を却下した」という
記録は、実は**この `Prop` のバグの目撃**だった。具体インスタンスを合わせる形で回避されたため、
`Prop` 側に残置していた。

### (2) 帰結の弱化:`c ≥ 1` は不要 — **`c = 0` でも成立**

外向き掃引は `0 0` ギャップで死に、`1^c` ブロックの手前1セルで止まる。よって `1`-カウンタは
**一度も読まれない**。`RungTile` の `c+1` を素の `c` に緩めた(`tile_c_zero` が `c=0` の
kernel インスタンス)。一方 `g ≥ 3` は本物の仮説で、`g = 2` では `F` に到達して turn しない
(`d_rung_general.py §B2`)。

---

## §2 実測した原子分解 — 原子は **2 種類**、1 種類ではない

`d_rung_atoms.py`(状態列を `u ≤ 4, 1 ≤ m ≤ 4` の全点で採取)。`u=2,m=3,c=2,g=4`, span 45:

```
ABEDABEDABEDAABEDABEDABEDABCBEBEBEBCBCBCBCBCD
(ABED)^{u+1} · A · (ABED)^{m} · A · (BC) · (BE)^{m} · (BC)^{u+2} · D
  4(u+1)       1     4m        1     2      2m         2(u+2)      3   = 6(u+m)+15
```

前セッションの RESUME §3 は残る 2 原子を **`E` 始点の `EB`** と **`C` 始点の `CB`** として
書き出していた。実測すると原子はどちらも **`B` 始点・`B` 終点**である:

| 原子 | 遷移 | 歩数 | head | 効果 |
|---|---|---|---|---|
| `swap10` (S1) | `B1→0RE`, `E0→1RB` | 2 | `+2` | `1 0 ↦ 0 1` |
| `swap01` (S2) | `B0→1RC`, `C1→0RB` | 2 | `+2` | `0 1 ↦ 1 0` |

`B` 始点で書くのが本質的だった。`B→B` なので**そのまま fold できる**(`sweep10`/`sweep01`)。
`E`/`C` 始点だと復路が2つの相に分断され、fold が phase 境界をまたげない。

外向き側も一般化が効いた:`ABED` は着地セルを**読まない**ので `∀ b` で成立する
(`crawlB`)。同じ原子が `(0 1)^u` の走査と `[1,1]` マーカーの乗り越えを兼ねる — 前セッションが
「boundary event #1」として別扱いしていた相が、原子の一般化だけで消えた。

---

## §3 復路が往路を読み直せる理由 — 語の再位相化

往路は `(1 0)` を書き、復路は同じブロックを `(0 1)` として読む。これを支えるのが 1 本の恒等式:

```lean
theorem pow10_true : pow10 n ++ true :: R = true :: (pow01 n ++ R)
```

同型のもう1本 `pow01_shift : true :: (pow01 n ++ 0 :: 0 :: Z) = pow10 (n+1) ++ 0 :: Z` が、
マーカー通過後の左文脈 `1 · (0 1)^m · 0 0` を `(1 0)^{m+1} · 0` として読み直させ、**第2の外向き
掃引を単一の `crawlFold` にする**(ad-hoc な相を作らずに済む)。この2本が、9相のうち語の
辻褄が合う必要のある全箇所を賄っている。

---

## §4 9 相の構成(`rung_core`)

| # | 歩数 | 原子 | 内容 |
|---|---|---|---|
| 1 | `4u` | `crawlFold u` | `(0 1)^u` を外向き |
| 2 | `4` | `crawlB _ true` | `[1,1]` の第1の `1` を乗り越え |
| 3 | `1` | `marker` | 第2の `1` で `A1 → 0LA` |
| 4 | `4(m+1)` | `crawlFold (m+1)` | 櫛を外向き(`pow01_shift` で読み直し) |
| 5 | `1` | `turnaround` | `0 0` ギャップで `A0 → 1LB` |
| 6 | `2` | `swap01` | 復路の第1原子 |
| 7 | `2(m+1)` | `sweep10 m` | 櫛を復路 |
| 8 | `2(u+2)` | `sweep01 (u+1)` | 堆積を復路(`pow10_true` で再位相化) |
| 9 | `3` | `turn` | `+3` で `A` に着地 |

`rung_core` は 2 つの凍結文脈を裸のリスト変数 `W`/`Z` に抽象した形。可視窓は
`[p − 2(u+m_IN) − 4, p + 4]`(実測一致)なので `TAIL`/`REST` は任意で、
`TapeCalc.steps_lpad_dich`/`steps_rpad_dich` に直結する。

---

## §5 検証

1. **Python 網羅**(`d_rung_general.py §B`):`u ≤ 4 × 1 ≤ m ≤ 4 × 0 ≤ c ≤ 3 × 3 ≤ g ≤ 6`
   × `TAIL` 9 種 × `REST` 8 種 = **23040/23040 一致、0 不一致**。span+1 と `g = 0,1,2` の
   negative control は要求どおり失敗。
2. **相ごとの歩数会計**(`§D`):9 相の和が全点で `6(u+m)+15` と一致。
3. **Lean 内の二重証明**(`§5.1`):既存の kernel-`rfl` 3 インスタンスと*同一の命題*を、今度は
   一般法則の特化として証明(`tile_*_via_law`)。両者は証明を共有しない — 一方は kernel が `dT`
   を実行、他方は `rung_core` の 9 相合成。span 算術が 1 歩でも、語の帳尻が 1 セルでもずれれば
   型検査が通らない。
4. `anchor160`(実 blank orbit, `t=160`)が `dT` と `PHASEB_D_M0` 表を pin し続けている。

---

## §6 残っているもの(D を閉じるまで)

タイルが担うのは 33 セグメント中 30。残りは `SYNTHESIS_2026-07-26.md` §4 訂正枠と同じで、
**1 つも縮んでいない**:

1. **RF-4** epoch あたり `k+1` 個の turn 相 — 加法定数に閉形式なし。一様な `0`-run crawl 補題が
   必要。**最大の残リバースエンジニアリング・ギャップ。**
2. **RF-5** 偶 `k` の shifted `S1` セグメント 3 本 — 第2タイル、内部歩数則は未導出。
3. cascade level の内部帰納(epoch は `k+1` 相)。
4. entry セグメント: blank → `M1(4)` = 291,168 歩 ⇒ kernel-`rfl` 3〜4 チャンク。
5. `TapeCalc.nonhalt_of_invariant` による組立て。
6. milestone 族は `k=4..9` を pin。`k=1,2,3` は族外 ⇒ 帰納は `M1(4)` から入る。`k ≥ 10` 未実測。

---

## §7 追跡: タイルは**機械独立**だった — `RungCalc` と H

§6 で「安価な保険」として挙げた H の測定を、そのまま実行した。結果は予想より強い。

### (a) H のグラフは D の付け替えでは**ない**

`h_vs_d_tile.py §1`:状態置換の全探索(`D`/`Dᴿ` × `H`/`Hᴿ` の4通り、開始状態 A 固定)で
**同型 0 個**。つまり **C を無料にした機構(C は x2 のグラフだった)は H には適用されない**。
A の「安価な同種再実体化」主張は、*この意味では* 反証された。

### (b) それでも D の rung タイルは H で**そのまま発火する**

`h_tile_fire.py`:D の `IN` 族を H のテープに置き、H の状態 `D` から走らせる。

| 検査 | 結果 |
|---|---|
| §A 全開始状態 6 通り × 144 点 | **`D` から 144/144**、他の5状態は 0/144 |
| §C D の証明と同一グリッド 23040 点(`c=0`・敵対的 TAIL/REST 含む) | **23040/23040**、不一致 0(D^R の control も 23040/23040) |
| §D negative control | `g=0,1,2` 不一致、span+1 不一致 — D と同じく要求どおり失敗 |
| §B H の**実軌道**の走査(300k 歩) | IN 形の配置 319 個すべてで `st=D d=+3 tape_ok=True` |

しかも itinerary が**同一の語**である:

```
D^R : ABEDABEDABEDAABEDABEDABEDABCBEBEBEBCBCBCBCBCD
H   : DAEFDAEFDAEFDDAEFDAEFDAEFDABAEAEAEABABABABABC
```

対応は関数ではない。**H は D が使い回している状態を2つに割っている**:`Dᴿ` の `D` は
`E` から(crawl 内)と `C` から(turn 内)の両方に入るが、H はその2役に `F` と `C` を使う。
**グラフは違い、原子は同じ。**

### (c) なぜそうなるか — そして Lean での帰結

タイルの6原子の*インタフェース*に現れる状態名は **2つだけ**(外向き掃引状態 `sA`、
復路状態 `sB`)。他の全状態は原子の**内側に隠れる**。したがってタイルは遷移グラフを見ていない
— 6つの局所書き換え事実だけを見ている。

そこで機械独立層 **`lean/RungCalc.lean`** を新設した(`TapeCalc` の上の第2の機械独立層):

* 語彙 `pow10`/`pow01`/`ones` と4つの語恒等式;
* **`Atoms T sA sB`** — 6原子インタフェース(`Prop` 値 structure);
* `crawlFold` / `sweep10` / `sweep01` — 3つの `∀`-一様 fold;
* **`rung_core` / `tile`** — rung タイル、**`Atoms` を満たす任意の機械に対して `[PROVEN]`**。

結果、機械ごとの負担は **`Atoms` の6フィールド = 6個の閉じた kernel `rfl`** だけになった:

| ファイル | 機械固有の内容 | タイル |
|---|---|---|
| `lean/DMachine.lean` | `dT` + `dAtoms` (`sA=A`, `sB=B`) | `RungCalc.tile dAtoms` |
| `lean/HMachine.lean` | `hT` + `hAtoms` (`sA=D`, `sB=A`) | `RungCalc.tile hAtoms` |

**H の rung タイルは `[PROVEN]`**(`HMachine.rungTile`、9相合成の再掲は1行もない)。
`anchor17` が H の**実 blank 軌道**が 17 歩でタイルの配置族に入ること(左語が `u=0,m=1,c=1`)を
kernel `rfl` で pin し、`tile_*` の rfl インスタンスと `tile_*_via_law` の二重証明、
`tile_span_control`、`tile_c_zero` も D と同じ構成で揃えた。

コーパス全体 `lake build` EXIT=0(81 jobs)、公理は `[propext, Quot.sound]` のみ、
`sorryAx` 0、`Classical.choice` 0。

### (d) 何が言えて、何が言えないか

**言える:** COMB-doubler の rung タイルは、グラフ同型より粗い同値
(**原子内部で同じ振る舞いをする状態の融合を法とした同値**)の不変量である。島の他の候補にも
`Atoms` を試すのは各 6 `rfl` で済む — これは *測定* 可能な安価さになった。

**言えない:** **H は依然 `[OPEN]`。** タイルは1補題である。H の epoch anatomy、entry セグメント、
milestone 族、cascade level の内部帰納は**本セッションでは一切測っていない**。D の経験の
正直な読みは「タイルは安い部分だった」であり、H でも同じと見るべき。§6 の残項目1〜6 は
D について1つも縮んでいないし、H については未着手のままである。

---

*計器(repo root, committed): `d_rung_atoms.py`(状態列と原子分解)、`d_rung_general.py`
(span 判定・仮説緩和・negative control・相会計)、`h_vs_d_tile.py`(グラフ同型全探索・原子motif
探索・head-delta census)、`h_tile_fire.py`(H でのタイル発火:直接・実軌道走査・全強度掃引・
negative control・itinerary 比較)。
Lean: `lean/RungCalc.lean`(機械独立層)、`lean/DMachine.lean`、`lean/HMachine.lean`。*

**No machine decided by this document. No label upgraded. `D` and `H` both remain `[OPEN]`.**
