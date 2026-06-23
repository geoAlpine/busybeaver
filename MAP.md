# BB — データ整理(2026-06-21)　目標: **BB(6) の証明**

このファイルが現状の唯一の地図。数値は `suite.py` 実行で再現できる authoritative 値のみ。

> **完全証明が何を要求するかの決定版 = `BB6_OPEN_CORE.md`**(2026-06-24 capstone)。
> 全 19 cryptid を統一停止述語(`×2^a/3^b` 軌道の base-2/3 carry が可動 frontier と整列)に還元、
> 相互還元不能な open クラスタ {Mahler 3/2, Erdős ternary, odometer} を特定。Antihydra と o18 は
> Antihydra 級に精密化済(`antihydra_attack.md` §4, `o18_attack.md`)。机 decide 0、偽証明 0。

---

## 0. 目標と現在地(正直に)

**目標 = BB(6) を証明する**(= 残る全 undecided 6状態機械の停止/非停止を健全に決着させる)。

現在地を3つの輪で:

| 輪 | 中身 | 現在地 |
|---|---|---|
| ① 自分で引いた 63体 (3状態 monster) | 自作の難残渣 | **61/63 健全証明・偽証明0**。残2は純カウンター |
| ② BB(6) 分野の最前線 | 本物の undecided 機械 | **未着手**。本物の seed DB / undecided index 未取得。既存 decider は community より弱い |
| ③ 唯一すでに得た資産 | **健全性の規律**(偽証明を構造で防ぐ) | 取得済。v3 撤回事件で確立。量子本線(genuineness)と直結 |

**BB(6) 証明の正味の壁** = 最後に残る cryptid(Antihydra 級 = Collatz 型 = 停止性が数学的に未解決)。
ここは decider を書く問題ではなく**新しい数学**。1・2 を完璧にしても 3 を解かねば BB(6) は証明されない。

---

## 1. 健全な数値(authoritative・全部 `suite.py` で再現可能)

- **63体の3状態 monster: 61/63 を健全に非停止証明、偽証明 0。**
  内訳: halt-unreachable **23** / single-bouncer **14** / word-bouncer **16** / wall-bouncer **3** / halt-segment **5**。
  残 HOLDOUT = **2**(純カウンター `1RB0LZ_1LC1RA_0RA0LC`, `1RB1LC_0LA0RB_1LA0LZ`)。
- **本物の BB(6) frontier 20体(Champion + 全 named Cryptid): 全部 HOLDOUT、偽証明 0。**
  Antihydra / Space Needle / Lucy's Moonlight 含む。→ 永久ゲート化済(`suite.py` CRYPTIDS)。
- **ランダム監査(健全性): 4/5状態を多数、全 NEVER_HALTS を trusted sim で照合、偽証明 0。**
  translated 単体で 10,383 claim / 0 false、word/wall 系も 0 false(本日の wbounce2 監査含む)。

> soundness の二重ゲート: ①cryptid 関門(open/停止 機械に NEVER_HALTS を出したら即アウト)
> ②ランダム監査(全 claim を sim 照合)。v3 は②だけ通って①で死んだ。両方必須。

---

## 2. ファイル地図

### A. 信頼できる中核(trusted)
| file | 役割 |
|---|---|
| `bb_sim.py` | **trusted simulator**。BB(5)=47,176,870 を厳密再現。全照合の oracle |
| `wsim.py` | **G1検証済** word-block シンボリック simulator(1600 ops 完全一致)。帰納証明の基盤 |
| `wchain.py` | 周期-q crossing の word-chain 抽出(具体コピーで検証) |
| `translated_cyclers.py` | bbchallenge S(5) reference の忠実移植。10,383-claim 監査 0 false |
| `halt_segment.py` | 後方到達可能性 decider(halt が blank start に後方到達しない) |
| `bouncer_prove_sound.py` | 単一記号 repeater bouncer prover |
| `wbounce.py` | 多記号 repeater bouncer prover(`wsim` 上) |
| **`wbounce2.py`** | **本日追加。壁に挟まれた周期-q repeater を2記録差分で検出**(`x1=(W)^m+x0`)。faithfulness ゲート付き。残4体のうち boundary-coupled bouncer 2体を割った |
| `suite.py` | **統一ランナー**。verdict 順 = sim→unreachable→translated→single→word→**wall**→segment。cryptid 関門 + 監査込み |
| `bbchallenge_run.py` | 標準フォーマットを任意状態数で実行。BB(4)=107 / BB(5) 再現 |

### B. カウンターエンジン(WIP・健全性critical・BB(6) の鍵)
| file | 役割 |
|---|---|
| `counter_prove.py` | G1検証済 単一変数 symbolic sim(基盤・停止主張なし) |
| `counter_inc.py` | 証明済 Inc 規則(self-loop chain ×2、head-contained) |
| `counter_sweep.py` | Sweep 規則(doubling f(m+1)=2f(m)+2 検証済、naive 帰納は未閉) |
| `counter_induct.py` | PIECE1(compress+chains, G1)+ PIECE2(detect_rules) |
| `counter_rule.py` | sligocki reference verifier(base case 検証済) |
| `counter_structure.py`, `counter_analyze.py` | STEP1 測定(構造のみ、主張なし) |
| `STEP2_COUNTER_PLAN.md` | nested multi-rule induction の設計(次の本線) |

### C. 隔離(QUARANTINED — 絶対に信頼しない)
`bouncer_prove.py`(v1)/`bouncer_prove2.py`(v2)/`bouncer_prove3.py`(v3)/`lin_decider.py`。
step-trace を比較し1回の一致から「永遠」を外挿 → **Antihydra(open)と Lucy(停止)に偽証明**。詳細 `SOUNDNESS_INCIDENT.md`。
(注: `bouncer_prove2.parse/sim` は parse/sim ユーティリティとしてのみ各所で import — 証明エンジンは使わない)

### D. データ / 測定 / ドキュメント
`holdouts3_reps.txt`(63体)、`enumerate2/3.py`(2・3状態 universe 閉包)、`classify_monsters.py`/`bouncers.py`/`spacetime.py`/`hunt6.py`/`antihydra.py`(測定)、
`STATUS.md`/`SOUNDNESS.md`/`SOUNDNESS_INCIDENT.md`/`BB6.md`/`README.md`/このファイル。

---

## 3. BB(6) 証明までのクリティカルパス

```
[段1] 本物の undecided 集合を入手        ← 未着手(データ取得)
         88M seed DB + binary undecided index、または community の undecided machine リスト
            │
[段2] 健全スイートで削る                  ← 道具はある(suite.py)が、現状 community より弱い
         現状のままでは新規 1体も落ちない見込み。
         勝ち筋 = community が持たない強い decider を持つこと
         → 最有力: counter induction エンジン完成(段Bを健全化)
            │
[段3] 残る cryptid を割る                  ← BB(6) 証明の実体・新しい数学
         Antihydra 級 = Collatz 型 = 停止性未解決。
         ここを越えない限り BB(6) は未証明のまま
```

各段に効くファイル: 段1=`bbchallenge_run.py`(実行可)+ データ取得(欠)。段2=`suite.py` + counter エンジン(B)。段3=未着手(数学)。

---

## 4. 次の一手 — 2026-06-23 全面更新(decision アーク終了後)

**重要: BB(6) の "decide(機械を1体落とす)" 路線は、本アークで実証的に閉じた。**
- ① 自作 deciders は community より弱い(実 holdout 300体 → 0 decided, `BB6_PREP.md`②)。
- ② Collatz core 5体(Antihydra/o10/o15/o17/o18)を §3c 流に全還元 → **5/5 一様に Collatz-hard**(`CRYPTID_REDUCTIONS.md`)。最後の可解候補 o17 すら、埋め込み族 `0A01^k` が proven halter(k=6,12,15)を持つ Collatz 不規則停止で**正則証明書到達不能**と判明(`o17_attack.md`、健全 gate が偽 decide を阻止)。
- → **「新しい数学(cryptid の停止性)」を解かずに BB(6) を decide する道は無い。我々が今夜解くものではない。**

**残る唯一の BB(6) 寄与 = ⑥ certificate 階層理論("なぜ難しいか")** = 量子/SETI genuineness 限界定理の離散アバター。本アークの収穫:
- [PROVEN・予想非依存] 階層に2分離: k-window ⊊ REG ⊊ SLIN(witness: パリティカウンタ, EQ機械)。
- [PROVEN] Antihydra §3c: 厳密 2-adic 判定 `v2(c_n-1)≥balance_n+1`(`antihydra_attack.md`)。
- [資産] 5体 exact 還元カタログ + Mahler 乗数族 {3/2, 8/3}(4体) + o17 の proven-halter 非正則 witness。
- [OPEN] cryptid に tame 証明書なし(階層の頂点 = 限界そのもの)。

**次の一手の候補(入念検討用、いずれも理論。decide はもう無い):**
1. **新 PROVEN 段の追加** — brick(a)/(d) 流に、SLIN ⊊(次クラス)を予想非依存 witness 機で証明(EQ機械の1段上)。階層の背骨を太らせる唯一の proven 前進。**実質的研究、1セッション保証なし。**
2. **本線へ収穫(推奨)** — 5体カタログ+Mahler族+§3c+o17 witness を `docs/theory_certification_hierarchy.md` の統合理論に織込み、量子/SETI genuineness 限界の**離散アンカー**を太らせる。**確実・本線(OLCF/SETI)に payoff が落ちる。**
3. **本線へ復帰** — BB はアンカーとして十分発達。重心を OLCF(PAS 審査待ち)/SETI に戻す。

> 結論(正直): BB(6) decision アークは**証明済みで閉じた**(敗北でなく確定的 negative + 健全規律の勝利)。
> 残るのは理論のみで、その価値は**本線 genuineness 限界の離散アンカー**としての存在。
> → 推奨は **2(本線へ収穫)**: 今アークの豊かな成果を本線統合に変換し、必要なら 1(新段)を研究課題として後置。
