# BB — データ整理(2026-06-21)　目標: **BB(6) の証明**

このファイルが現状の唯一の地図。数値は `suite.py` 実行で再現できる authoritative 値のみ。

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

## 4. 次の一手(候補)

1. **counter induction エンジン完成(PIECE 3)** — 残2 monster を閉じ、BB(6) 再利用可能な「community より強い」武器を1つ持つ。`STEP2_COUNTER_PLAN.md` の nested induction。**段2 の勝ち筋を作る唯一の現実路線。**
2. **本物の BB(6) undecided データ取得** — 段1。これがないと段2の実測(何体落ちるか)ができない。
3. (段3 は 1・2 で標的が具体化してから)

> 結論: BB(6) 証明は 3段で、3 が新しい数学。今できる前進は「community より強い健全 decider を持つ」=
> **counter エンジン完成**。それが段2を動かし、段3 の標的(どの cryptid で止まるか)を初めて可視化する。
