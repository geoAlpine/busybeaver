# `Atoms` 走査 — 残余 1104 のうち **17 台**が rung タイルを取得(2026-07-26)

`RESUME_2026-07-26.md` §3 Option A の実行結果。`lean/RungCalc.lean` が「`Atoms T sA sB` を満たす
任意の機械に rung タイルを与える」ので、**島の再利用性が初めて見積りではなく測定になった。**

`lake build` EXIT=0(コーパス 83 jobs)、公理は `[propext, Quot.sound]` のみ、`sorryAx` 0、
`Classical.choice` 0。

**17 台はいずれも `[OPEN]`。本文書は機械を決着させず、ラベルを昇格させない。**

---

## §0 結果

| 測定 | 値 |
|---|---|
| 走査対象 | `_bbdata/bb6_holdouts_1104.txt`(2026-06 curated residual、1104 エントリ) |
| 走査方法 | 両向き(as-written / reversed)× 6 状態すべてを `sA` 候補として `Atoms` を判定 |
| **`Atoms` 完全充足** | **17 / 1104** |
| 5/6(1原子だけ不足) | 1(`turn` のみ不足) |
| 4/6 | 4 |
| 3/6 | 31 |
| 2/6 | 377 |
| 1/6 | 674 |
| Lean 化 | `lean/IslandTiles.lean`(自動生成)に **17 台すべてのタイルを `[PROVEN]`**、build 0.6 秒 |

`1094`(2026-07 リスト)でも同じ 17 台。

名前付き島候補との対応:

| 候補 | 結果 |
|---|---|
| `D` | **6/6**(既に `lean/DMachine.lean`) |
| `E` | **6/6** ← 新規ヒット |
| `H` | **6/6**(既に `lean/HMachine.lean`) |
| `x2` | 1/6 |
| `F` | 2/6 |
| `G` | 2/6 |
| `I` | 1/6 |

**`x2` が 1/6 であることは重要**:このタイルは x2 の機構では**ない**。島は単一種ではない。

---

## §1 `Atoms` は見た目より遥かに狭い制約(正直な留保)

`sA` を決めると**残りは全部強制される**。`sA` の read 0 の遷移は一意で、それを `turnaround`
(`sB` を名付ける)と `crawl` の第1歩が共有するため:

```
 1. sA,0 -> (1,L,b)      turnaround + crawl 1
 2. sA,1 -> (0,L,sA)     marker
 3.  b,1 -> (0,R,e)      crawl 2 + swap10 1
 4.  e,1 -> (0,L,d)      crawl 3
 5.  d,0 -> (1,L,sA)     crawl 4
 6.  e,0 -> (1,R,b)      swap10 2
 7.  b,0 -> (1,R,c)      swap01 1 + turn 1
 8.  c,1 -> (0,R,b)      swap01 2
 9.  c,0 -> (0,R,f)      turn 2
10.  f,0 -> (1,L,sA)     turn 3
```

6状態機械の遷移 12 エントリのうち **9〜10 を固定する**(`sA,b,e,d,c,f` が全て異なるとき 10、
`d=f` のとき 9)。したがって:

* **「機械独立」は「任意の機械」ではない。** `Atoms` が記述する族は構造的に狭く、17 台は
  `Atoms` が自由に残す 2〜3 エントリと、`d=f` か `d≠f` かでしか違わない。
* 「固定部分が一致するクラスタが2つ」という集計は**トートロジー**である(`Atoms` が各エントリを
  厳密に指定しているのだから当然一致する)。唯一の非自明な構造的自由度は
  **`d=f`(17台中12)か `d≠f`(5)**:`d=f` は crawl の閉じ状態と turn の閉じ状態を1状態に
  まとめる(D の形)、`d≠f` は分ける(H の形)。**H が D の付け替えでないのはこの一点である。**

つまり 17 という数は「島の広さ」ではなく、**この1つのタイルが到達しうる上限**である。

---

## §2 タイルは「真である」だけでなく「その機械の話をしている」

`Atoms` が成り立つことは、タイルがその機械についての**真な補題**であることしか意味しない。
実際に**役に立つ**かは別の測定可能な問いである:blank 軌道が IN 配置族に入るか。

`atoms_island_scan.py §3`(各 300k 歩):

* 17 台すべて **300k 歩で停止せず**、すべて右向きに成長。
* 実軌道上の IN 形配置は 231〜398 個/台。
* **そのすべてでタイルが発火**(264/264, 328/328, …, 398/398 — **全台 100%**)。

D は `anchor160`、H は `anchor17` で kernel `rfl` として軌道進入を pin 済み。残る 15 台は
シミュレータ証拠(kernel 検証ではない)であり、そのようにラベルする。

---

## §3 Lean 側

`lean/IslandTiles.lean` は `gen_island_tiles.py` による**自動生成**(手編集せず再生成する)。
1台あたりの内容は遷移表 + `Atoms` の6フィールド(各 `rfl`)+ タイル1行 + 非空虚性の
kernel `rfl` 1本。9相合成の再掲は**1行もない** — それは `lean/RungCalc.lean` に一度だけある。

```
theorem tileMnn : Tile TMnn St.X := tile_holds AMnn
```

`all_tiles` が 17 本の連言を1つの定理にまとめてあり、本数が一目で検算できる。

---

## §4 これで何が変わり、何が変わらないか

**変わった:** 「テンプレート島 ≥ 7〜10 グラフ」という*見積り*の一部が数になった。この rung タイル
に関しては **17/1104**、しかも 1台 6 `rfl` で取得済み。5/6 の near-miss 1 台
(`1RB0RF_0LC0RA_1LE1RD_0RC---_1LA0LE_1RA0LC`、`sA=E`、`turn` のみ不足)は、turn 原子の変種を
1本足せば 18 台目になる可能性がある — 安価な次の一手。

**変わらない:** **タイルは1補題。** D の経験が示したとおり、難所はその先(RF-4 の `k+1` turn 相、
RF-5、cascade 帰納、entry セグメント)にあり、**17 台のいずれについてもそこは未測定**である。
17 台の epoch anatomy / milestone 族 / entry は一切測っていない。
17 台すべて `[OPEN]` のままであり、BB(6) の4義務のうち開いている2つは1ミリも縮んでいない。

---

*計器(repo root, committed): `atoms_island_scan.py`(制約導出・残余走査・勾配分布・
狭さの定量・軌道関連性)、`gen_island_tiles.py`(Lean 生成器)。
Lean: `lean/RungCalc.lean`(機械独立層)、`lean/IslandTiles.lean`(17台)、
`lean/DMachine.lean`、`lean/HMachine.lean`。*

**No machine decided by this document. No label upgraded. All 17 remain `[OPEN]`.**
