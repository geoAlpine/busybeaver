# BB(6) 完全証明に向けた手法の総合 — 2026-07-26

全情報を再解析した統合文書。三角度(テンプレート島 / o4_ledger / 列挙ブリッジ)の並列調査
+ 本セッションの新規証明 + ライブビルド監査を統合する。

**健全性規律:** 全主張に `[PROVEN]` / `[MEASURED]` / `[OBSERVED]` / `[OPEN]` を付す。
偽証明ゼロ。No machine decided by this document. No label upgraded.

---

## §0 検証済みの現在地(本セッションで実測)

| 項目 | 実測値 |
|---|---|
| worktree / branch tip | `roadmap-post-closure-sync` / `d4df000`、main より 202 コミット先行、clean |
| Lean 定理・補題 総数 | **1630**(`.lake` 除く)、Lean v4.31.0、**Mathlib 不使用** |
| 公理監査(ライブ `lake build`) | `[propext, Quot.sound]` **561** / 公理フリー **127** |
| **`sorryAx`** | **0** |
| **`Classical.choice`** | **0** |
| `sorry`/`native_decide`/`admit` の実使用 | **0**(11ファイルの grep ヒットは全て docstring 内の言及) |

**決着済みの機械 `[PROVEN]`:**
- `x2 = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` — `T7Entry.lean:42 x2_nonhalt_blank : ∀ N, steps N init ≠ none`、
  ライブビルドで **`[propext, Quot.sound]` を確認**。無条件。
- `C = 1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD` — `CIso.lean:71 C_machine_nonhalt`。σ(x2)(x2 のグラフを
  状態 B から起動)だが 1104 リスト上は別エントリ。相対ラベリングは Lean 内で公理フリー。

> **重要な読み違い注意(本セッションで判明、記憶に記録済み)。** `X2.lean` 自身の散文は今も
> "`x2` remains `[OPEN]`" と述べ `[DESIGN ONLY]` の `carry_step` ギャップを持つ。これは **放棄された
> 初期構成**(直接 cascade-doubler `carry_step : CarryCfg(j)→(j+1)` の `Θ(2^{2K})` リップル、閉じなかった)
> の考古学的記録である。実際の決着は **別構成** = T7 モジュール群(`RegenLaw ∀k`, `oddSpineFull`,
> `doubPhaseOdd`, obligation H)+ 8チャンクの `entryM12` カーネル `rfl` エントリ区間 → `x2_nonhalt_blank`。
> また branch tip `d4df000` の "x2 and C are BOTH still open" は **コミュニティの 2026-06-29 holdout
> リスト上で未決着**(=我々の証明が新規)の意味であり、我々の Lean 証明が未完という意味ではない。

---

## §1 完全証明の依存木 — 4つの義務

権威ある台帳は `lean/Completion.lean`。組立ては既に `[PROVEN]`:

```
BB6_eq_championSteps (h : AllHoldoutsNonHalt) : BB6 = championSteps
  := Nat.le_antisymm (enumeration_upper h) champion_lower
```

残りの難しさは全て以下の4義務に隔離され、**うち2つは純工学、2つは未解決数学**:

| # | 義務 | 種別 | (K)壁に依存? | 規模 |
|---|---|---|---|---|
| **1** | `champion_lower : championSteps ≤ BB6` | 証明書1本(champion の停止+ステップ数) | **否** | 小 |
| **2** | `enumeration_upper : AllHoldoutsNonHalt → BB6 ≤ championSteps` | 検証済み TNF 列挙器 + デサイダ再検査 | **否** | Coq-BB5 規模 × 大、多人年 |
| **3** | 17 named `*_nonhalt` | 14=正規性 / o7,SN=一般化Collatz / o17=gate-timing | **是** | 未解決数学 |
| **4** | `holdouts1087_nonhalt` | 1087残余(実測では大半が (K)-like) | **大半が是** | コミュニティ規模+未解決数学 |

**§1.1 義務3の構造(schema collapse、機械検証済み).** 17 の連言は 5 スキーマ、うち3つは
1つのメタスキーマ `NormalityPQ p q seed` の3つの異なる素点への具体化:

- `Normality32`(place ℤ₂、9 seeds):antihydra, o10, o2, o11, o13, o14, o16, o12, o8
- `Normality43`(place ℤ₃、3 seeds):**o4**, o3, o5
- `Normality83`(place ℤ₃、2 seeds):o15, o18
- `TwoPowerAvoidance`(2 instances):o7, Space Needle — 一般化 Collatz thin-set
- o17 gate-timing(1 instance):Nerode 指数 1,2,6,19,54,132 — 有限オートマトンなし

**正直なスコープ:** 形が同じでも境界は移らない(per-seed に開いた内容がある)。崩れるのは形状であって難度ではない。

**§1.2 o4 の特別な地位.** 17 のうち **o4 だけが Lean で end-to-end**:`o4_reduction`(a-ledger 予想 ⇒
o4 非停止)が `[PROVEN, propext/Quot.sound]`。残る公理は算術の `o4_ledger` 1本のみ。他の16は不透明 `Prop`。

---

## §2 手法目録 — 実際に機能するもの

### M1. テンプレート法 / 境界計算 ★ 唯一の実証済み機械決着エンジン
**実績 `[PROVEN]`:** x2, C の2台。

- **機械独立層 `TapeCalc.lean`**(41定理、772行、sorry 0):`lpad`/`rpad`/`lunpad`/`runpad`、
  `steps_rpad_dich`/`steps_lpad_dich`、`nonhalt_of_invariant`、**q-pinning**(∀-tail 転送が自身の
  translation を pin する技)。この層は x2 に一切言及しない = 全機械で verbatim 再利用可。
- **ワークフロー:** milestone 族の同定 → low phase → doubling phase(∀-parametric)→
  entry 区間(カーネル `rfl` チャンク)→ 組立て。
- **到達範囲:** carry-transparent(桁上げ透明)機械のみ = テンプレート島。
- **コスト較正 `[MEASURED]`:** 種(species)の初号機 ≈ 20,000 Lean 行(`X2.lean` 単体で 12,208)。
  **同種内の再具体化 ≈ 1,000 行**(C = `X2FromB` 809 + `CandC`/`CIso` 164、**新規動力学ゼロ**)。

### M2. ∀-parametric 規律 ★ C が無料だった理由
最初から**種内で変動する添字すべてについて ∀** で補題を建てる。これが「2台目の新規動力学ゼロ」を
生んだ唯一の要因。**最重要の移転可能教訓。**

### M3. シミュレータ先行の milestone/epoch リバースエンジニアリング
width ゲートでレジスタ形状を測定 → marker word 族を同定 → **その後で**形式化。
anti-vacuity アンカーと M4(cell-for-cell)ガードを必須とする。
**規律:** サブエージェント/文書の主張は *証拠* であって *評決* ではない — 生軌道から再導出する。

### M4. 付値恒等式法 ★ 本セッションで新規に確立
odometer 軌道の分岐写像のアフィン共役固定点を見つけ、**run 長を p 進付値として読む**。
o4 で `L(n) = v₃(G_n+14)` を与えた(§3)。この種の軌道に対する一般技法。

### M5. 公理隔離 / 条件付き完成定理
`Completion.lean` のアーキテクチャ:完全証明を条件付きで述べ、未解決内容を**文書化された同値性つきの
名前付き公理**に隔離する。進捗が可測になる(公理→定理の各格上げが可視の前進)。

### M6. スキーマ崩壊
17 連言 → 5 スキーマ → 3素点上の1メタスキーマ。監査が 16 個の不透明 `Prop` ではなく
共有された**形**(記号 `NormalityPQ` 1個)を露出する。

---

## §3 本セッションの新規結果 — o4 drain-run の付値恒等式

`o4_ledger_conjecture := ∀ n, 1 ≤ aseq n`。台帳 `aseq` は `Gseq n mod 3` に隷属して増減する
(`≡1`→ −1 が drain 分岐、`≡2`→ +4、`≡0`→ +6)。

**定理1(drain-run 付値恒等式)`[PROVEN]`.**
任意の drain ステップから始まる極大 drain-run の長さは
$$L(n) = v_3(G_n + 14).$$

*証明.* drain 分岐の写像は `φ(G)=⌊4G/3⌋+5 = (4G+14)/3`(`G=3m+1` で `4m+6`)。φ は**固定点 −14**
の周りで ×(4/3) に共役:`φ(G)+14 = (4/3)(G+14)`。run 継続中は `G_{n+k}+14=(4/3)^k(G_n+14)`。
ステップ `n+k` が drain ⟺ `3^{k+1} ∣ (G_n+14)`(4 は 3 と互いに素)。∎

**数値検証 `[MEASURED]`:** `o4_drain_run.py`、N=3×10⁵、**66687 runs で 0 ミスマッチ**。

**定理2(無条件・線形バウンド)`[PROVEN]`.** `3^{L(n)} ∣ (G_n+14) > 0` と `G_n = Θ((4/3)^n)` より
$$L(n) \le \log_3(G_n+14) \approx 0.262\,n.$$
測定傾き 0.2625 vs 理論 `log₃(4/3)=0.2619` 一致。

**位置づけ:** これは antihydra の depth `K=v₂(3c−1)` / crude `K≤0.585n` の **完全な base-4/3・3進ミラー**。

**`L(n)=O(log n)` は `[OPEN]`、(K)-hard.** ⟺ `v₃(G_n+14)=O(log n)` ⟺ 軌道が固定点 −14 に対数レート
より速く3進接近しない ⟺ 単一軌道の mod 3^L 均等分布 = `Normality43` = (K)-family。
**訂正:** 「Subspace 定理で O(log n) が出る」は誤り — Subspace が抑えるのはクリーンな幾何
`⌊α(4/3)^n⌋` の桁 run であって、`G_n` は cOdo 摂動が蓄積する**反復** odometer 軌道でクリーン幾何から
乖離する。frontier が antihydra の max-run で既に指摘した罠と同型。
数値上は真(max-run が `log₃N` を追う:N=10³→5, 10⁴→8, 10⁵→12; ヒスト geometric(1/3))だが証明は (K)。

---

## §4 三角度の評決

### 角度A — テンプレート島の掃討 `[MEASURED]`
1.2×10⁸ ステップで (2,4) シグネチャ(幅比→2 = 桁上げ連鎖ゼロ、時間比→4)を独立再測定:

| 機械 | 幅比 → | 時間比 → | レジスタ種 | 評決 |
|---|---|---|---|---|
| x2(対照) | 1.9961 | 3.971 | **CASCADE**(島の外れ値) | `[PROVEN]` |
| **D** | **2.005** | **4.01** | **純 `(1 0)` COMB**、milestone 状態 A / head −8 均一 | **(a) 形式化可** |
| **H** | 1.9967 | 4.009 | 純 `(1 0)` COMB(`1^3` cap)、状態 D / −16 | **(a) D の後で安価** |
| E | 2.0048 | 4.015 | COMB + 倍加ヘッドブロック `1^(2^k)` | (b) 追加作業 |
| F | 1.9912 | 3.983 | 不規則、可変 `0`-gap、**head-step 多重**(−8,−9,−12,−13,−16) | (b) 低優先 |
| **G, I** | 1.987 | **3.88 / 3.889(4 に未到達)** | 幅広 COMB、未収束 | **(c) 赤旗 — 形式化するな** |

- **G/I は棄却済み候補 A/B と同じ profile**(短スクリーンを通過後に破綻)。加えて **G と I は全測定尺度で
  幅/時間ラダーもレジスタも同一** — 1つの挙動である可能性が高い。
- **島は COMB doubler が支配的で、x2 は唯一の CASCADE 外れ値**。よって **x2 の cascade 代数
  (`uUnits`, `m1casc`, `descCascade`, `seamZ`)は島の他機に移転しない**。D は「x2 の移植」ではなく
  **サブテンプレートの初号機**。
- 島の規模:厳密スクリーンで **≥7 グラフ**、2スクリーンの合併で **≥10 グラフ**(いずれも下界)。

> ### ⚠ 訂正(同日、深掘り測定 + 統合者による独立再測定)— D は「純 COMB」ではない
>
> 上表の「純 `(1 0)` COMB、1反復単位、`0^33 ++ pow10 k`」という読みは **truncated reading の誤り**。
> `D_SPEC_2026-07-26.md`(`d_spec.py`)と**統合者の独立スクリプト**が一致して示すのは、D のレジスタが
> **成長する 0-gap で区切られた comb ブロックの連鎖**であること:
> ```
> M1(4) t=291168 : (10)^65 1 0^112 (10)^308 1
> M1(5) t=1196412: (10)^3 1 0^6 (10)^14 1 0^61 (10)^131 1 0^223 (10)^620 1
> M1(6) t=4846662: (10)^65 1 0^79 (10)^263 1 0^448 (10)^1244 1
> ```
> ブロック数は 1,2,1,3,2,4,3 とパリティ依存で線形に増える。**⇒ D は一パラメータ `pow10 k` ではなく
> 再帰的な語(x2 の `descCascade` 類似)を要する CASCADE 種の初号機**。epoch も 5 相ではなく **k+1 相**
> (cascade level 上の内部帰納が必要)。**下の §6 Tier I-1 のコスト見積りは低すぎた** — D は
> 「安価な再具体化」ではない。H が「同種で安い」という期待も、D が純 COMB でない以上、
> **未検証の仮定に格下げ**。
>
> **それでも D は最良ターゲットである**(理由は下方修正されたが消えていない):
> - **∀-parametric な rung タイル 1本が測定 33 セグメント中 30 をカバー**。局所性窓が厳密に測定され
>   (`[p − 2(u+m) − 4, p + 4]`、`ones c` の内部を読まず右に丁度4はみ出す)、`TAIL`/`REST` が任意 ⇒
>   **`steps_lpad_dich`/`steps_rpad_dich` に直結**。これが doubling 機構の全体。
> - milestone 族は k=4..9 で**両側とも厳密に pin 済み**(左語は空、閉形式 `a(k)=39·2^{k−1}−4` 等)。
>   `k=1,2,3` は族外 ⇒ **帰納は M1(4) から入る**。
> - **entry 区間は x2 の 40%**(blank→M1(4) = 291,168 歩 vs x2 の 732,733)、3–4 チャンク見込み。
> - epoch span アンカーが exact(52,776 / 224,262 / 905,244 / 3,650,250 / 14,641,536 / …、
>   k=2..6 で未計上ステップ ゼロ)、失敗すべきコントロール5本すべて失敗を確認。
>
> **未解決リスク(正直に):** (i) `k ≥ 10` 未測定(再帰は6レベルで固定、証明ではない);
> (ii) epoch あたり k+1 個の turn 相の加法定数に**閉形式がない** — 最大の残リバースエンジニアリング
> ギャップ; (iii) 偶 k の `S1` 3セグメントが第2のシフト済みタイルを使う(k=2,4,6 で bit 一致、
> 同じ exit 則に従うが内部ステップ則は未導出); (iv) **非停止論法はまだ存在しない**。

### 角度B — o4_ledger の subcritical 攻撃 `[評決 (c)]`
- **厳密な還元 `[PROVEN]`:** `aseq n = 18 + 6n − 7D − 2T ≥ 18 + 4n − 5D` より
  `o4_ledger ⟸ limsup D(n)/n ≤ 4/5`(drain 事象 `{G≡1 mod 3}` の base-4/3 上密度)。
- **margin 2.4 は無効。** 障害は「**未決定の頻度**」— feasible-measure 集合 M が drain 頻度 1 > 4/5 に
  到達するため、structure-only データは境界を証明できない。境界までの距離ではない
  (antihydra の `liminf ed ≥ ε` が任意の ε>0 で (K)-hard だったのと同じ理由の鏡像)。
- **本物の収穫 `[MEASURED + 構造的]`:** subcriticality は **antihydra を証明不能にしている
  second-moment / E[K²] 巨大run 障害を除去する**。o4 の running minimum は n=1(=17、失敗線まで16単位の
  余裕)、drift +3 で +∞ へ escape、最大 run ≈ log₃n ≪ 3n。
  ⇒ **o4 は first-moment(密度)の理由でのみ (K)-hard** — ×3/2 kernel より厳密に軟らかい。

### 角度C — 列挙ブリッジ `[評決:分裂する]`
- **`enumeration_upper` 単体は (a) 純工学、(K) 独立。** これは holdout を*決定しない* —
  仮説の中に*隔離する*だけの還元。Coq-BB5(BB(5)=47,176,870、Coq 27,274行 + 638補題、
  181,385,789 機械の TNF 列挙)がテンプレート。BB(6) は部分的な Rocq 証明のみ存在、未完。
  **多人年、新数学ゼロ、数学的リスクゼロ。**
- **ただし残余の掃討全体は (c):(K)壁が 14 機どころか残余の過半を封じている。**
  - 1104 エントリ = **909 個の相異なる遷移グラフ**(170 グラフが 365 エントリに重複。**必ずグラフ正準形で
    dedup すること** — C が新規に見えて x2 のグラフだった件で1ターン浪費している)。
  - **909 中 557(61%)が 3×10⁷ でも未解決** ⇒ census は暫定であって評決ではない。
  - 1104 中 **924 が digit-string 機械**(値は base-(p/q) odometer の*桁列*内で ×(p/q) 成長、テープ幅はほぼ一定)。
    粗い幅比プローブはこの多数派の乗数に**構造的に盲目** — これは o4 自身の構造でもある。
  - 解決した分の比のヒストグラムは **奇素数を含む小分数が支配的**(5/4, 8/7, 7/6, 3/2, 9/8, 4/3, 6/5)。
    奇素数 Mahler 乗数 = 桁上げ不透明 = **(K)-like**。
  - **既存デサイダは残余に実質 0/300**。理由は計算量ではなく構造:残余はまさにそのデサイダ族の
    生存集合として定義されている。`DECIDER_PREEMPTION` は Kind R(正則/閉テープ言語)証明書が
    レジスタ (C2) 位相不変量、Kind W(重み付きカウンタ)が (C1) sub-action であり、
    両者とも (K) 型機械上で実行不能であることをほぼ定理として論じる。

---

## §5 No-go 台帳 — 証明付きで機能しないもの

(K) 側で閉じている登録簿(`bb6-frontier-state` に完全版):

- **構造のみ/annealed/first-moment:** No-Structure 定理 (C1) 有界 sub-action の LP 実行不能
  (ergodic-optimization β=+½)、(C2) specification による非普遍性(Birkhoff 値を全実現、full-dim 違反者)、
  (C3) a.e. 真だが seed-null。**magnitude-aware 非有界 Lyapunov も adelic 版も閉鎖済み**(積公式)。
- **スペクトル:** annealed 作用素が全奇指標を消す(`L_ann χ_odd ≡ 0`)。新定理は annealed 縮小からは来ない。
- **励起/Kac、adelic budget、integrality:** a-priori 励起評価は全滅(heavy-tailed 敵対者が
  全ドリフトで実軌道と識別不能)。
- **デサイダ族:** Kind R / Kind W とも (K) 機械上で先取り済み。
- **交差分野 ~19 分野 + 2 プローブ**(Siegel (p,q)-adic Wiener Tauberian、非Pisot diffraction)
  すべて同じ annealed/a.e. 段で停止。

**帰結:** 障害は証明付きで**軌道特異的**。structure-only / all-orbits / 有限証明書のいずれの証明も存在し得ない。

---

## §6 実行計画 — ランク付き

### Tier I(即実行可、(K) 独立、機械を実際に決着させる)
1. **D の形式化** ★ 単一最良ターゲット。**[コスト訂正済み — §4 の訂正枠を参照]** D は純 COMB ではなく
   **CASCADE 種の初号機**(再帰語、epoch は k+1 相)。仕様は `D_SPEC_2026-07-26.md` に cell 解像度で確定:
   milestone 族 k=4..9 両側 pin 済み(状態 A、head-step −8k、左語 空、閉形式 `a(k)=39·2^{k−1}−4` 他)、
   **帰納は M1(4) から**(k=1,2,3 は族外)、entry = 291,168 歩(x2 の 40%)。
   反転形 `D^R = 1LB0LA_1RC0RE_0RD0RB_1LA0RF_1RB0LD_1RD---` で作業。
   **着手順:** (a) `∀`-parametric rung タイル(33 中 30 セグメントをカバー、局所性窓測定済 ⇒
   `steps_lpad_dich`/`steps_rpad_dich` 直結)を最初に建てる — これが doubling 機構の全体;
   (b) turn 相の加法定数(閉形式なし = 最大の残ギャップ)を潰す; (c) 偶 k `S1` の第2タイル;
   (d) cascade level 上の内部帰納; (e) entry 3–4 チャンク; (f) 組立て。
   *正直な見積り:* 種の初号機コスト = 複数セッション。C の「ゼロ新規動力学」は再現しない
   (C が無料だったのは*それが x2 のグラフだったから*)。
2. **H**(D の後):`[未検証の期待に格下げ]` A は H を「D と同じ純 COMB クラス ⇒ 安価」と評価したが、
   D 自身が純 COMB でなかった以上、**H の種と再利用率は測り直しが必要**。D の rung タイルが H でも
   発火するかを、D 着手前か並行で測定するのが安い保険。
3. **定理1・定理2 の Lean 形式化**(§3):`Gseq` に関する純算術 ∀-命題。
   `o4_ledger` は閉じないが、コーパスに実在の PROVEN 部分結果を追加する。

### Tier II(大規模だが (K) 独立、新数学ゼロ)
4. **`enumeration_upper` の構築** — 検証済み TNF 列挙器。2案:
   (i) Coq-BB5 アーキテクチャを Lean 4 に移植し 6 状態へ拡張(正直な [C]+[D])。
   (ii) 証明書輸入方式:コミュニティの列挙が生むデサイダ証明書と holdout 表を Lean が再検査。
   Lean コードは激減するが、列挙の完全性(全葉を訪問した)を別途検査しない限りその主張は輸入物に移る。
   → **BB(6) を「1104 が停止しないことを示せ」に、完全に機械検証された形で還元する。**
5. **深 census の完遂**(557 未測定グラフを大予算で)。島の規模を下界から事実に変える。

### Tier III(壁 — 外部数学、世代的)
6. 14 の (K)-band + 残余の (K)-like 過半 + o7/SN + o17。
   **最軟の rung は o4**(first-moment のみで hard、E[K²] 障害は除去済み)。外部連携の対象は
   AEV 著者 / Einsiedler–Lindenstrauss–Host 圏。

---

## §7 正直な総括

**BB(6) は「工学だけで終わる距離」にはない。** 列挙器と島を終えても、残余の掃討は named 19 を
封じているのと同じ正規性の壁に合流する。

しかし本セッションの再解析は、進捗が**測れる構造**を確認した:

- 完全証明の4義務のうち **2つ(champion_lower, enumeration_upper)は (K) 独立の純工学**。
- 残る2つのうち **機械的に閉じられる部分はテンプレート島**(≥7〜10 グラフ、うち 2 台決着済み)。
  そのエンジン(`TapeCalc` + ∀-parametric 規律)は**構築済みで再利用可能**。
- **o4 は 17 named のうち唯一 Lean で end-to-end**、単一の算術公理に還元され、
  さらに本セッションで **first-moment 障害のみが残る**ことが鋭く裏付けられた。

次の一手として最も価値が高いのは **D の形式化**(Tier I-1)である。これは COMB doubler という
**島の支配的種の初号機**であり、成功すれば H 以降が安くなる — つまり残余の最大かつ最清潔な
部分集団を到達可能な作業に変換する。

---

*Evidence (repo root, committed): `o4_drain_run.py`(定理1・2の検証)、`island_preflight.py`、
`candD_deep.py` / `candEF_deep.py` / `candGHI_deep.py`(ラダー再測定)、`o4_ledger_measure.py`。
Lean: `lean/Completion.lean`(台帳)、`lean/TapeCalc.lean`(機械独立層)、`lean/T7Entry.lean`(x2)、
`lean/CIso.lean`(C)。*

**No machine decided by this document. No label upgraded.**
