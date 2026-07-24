# 完全証明への手法総当たり — 攻撃カタログ (2026-07-24)

前提（FEASIBILITY_2026-07-24.md）: 完全証明 = **数学の壁 1 枚（(K) 核）+ 工学の山 2 つ
（[B][D]）+ 有限作業（x2, o7/SN/o17）** の連言。外部接触は用いない（オーナー方針）。
本書は着想の網羅であり、何も証明しない。ラベル: **[墓標]**（クラスごと反駁済み — 再挑戦禁止）/
**[部分]**（試行済み・未完部あり）/ **[未試行]** / **[核の言換え]**（同じ壁の別表現）/
**[工学]**。墓標の各項は該当 no-go 文書を参照のこと。

---

## I. (K) 核への攻撃（14 機の律速。核 = 単一指定軌道の ×3/2 一様分布・その片側弱形）

### 枯れた道 [墓標] — 参照のみ、再挑戦しない
1. 構造/輸送証明書 REG⊊SLIN⊊automatic⊊CF⊊CS（decider-preemption + 階層分離）
2. 有界メモリ不変量 / carry-coboundary（CARRY_* no-go）
3. スペクトル/コアイソメトリ埋め込み（EUE_COISOMETRY_NOGO）
4. AIU / joinings / skew 回転（AIU_* 障害定理）
5. エントロピー・次元剛性 Hochman/L-Y/Pesin-Margulis（ENT_* 障害）
6. Baker 線形形式・Diophantine ceiling（RUNCEILING no-go）
7. annealed→quenched モーメント集中（√階層 D10/D11: CLT 典型、特定軌道に手がかりなし）
8. 単一指標 Fourier/Rajchman 鎖（NONPISOT_FOURIER_CHAIN — 停滞）
9. Skolem–Mahler–Lech / dynamical Mordell–Lang / p進補間（SCOUT_ARITH_DYNAMICS:
   floor 写像は非代数的・2進膨張、頻度でなく構造しか制御しない — NOT-APPLICABLE）
10. liminf 密度 ≥ c の直接証明（任意の c で到達不能 — potential telescoping collapse）
11. Tao-Syracuse 転写（TAO_SYRACUSE_DRILL — almost-all と single-orbit の溝そのもの）

### 再開可能 [部分]
12. **NEWMATH solenoid 内在的一意エルゴード性**（ENDOGENOUS_UE_BUILD 系）— 骨組みは
    構築済み・閉じていない。何が欠けたかの精密な再監査から
13. one-char cancellation / EK2 二次モーメント partials — banked、拡張余地の再査定
14. Mauduit–Rivat 型 digit-sum 手法（ATTACK_MAUDUIT_RIVAT）— 3^n の digit 問題は
    field でも開。我々の弱形（片側・power-saving）に特化した再攻撃
15. Furstenberg corner / rank-2 埋め込み（FURSTENBERG_CORNER_QUESTION）— ×3/2 単独は
    rank-1 amenable（rigidity エンジン圏外）。×2×3 rank-2 系への埋め込みで我々の軌道が
    何かを等分布させるか — 問いの立て直しから

### 新規攻撃候補 [未試行]（優先度順、根拠付き）
16. **「ほぼ輸送」ハイブリッド（almost-transport objects）** — 最有力・最も我々の形。
    x2 で実証したテンプレート/輸送法は carry-透明機で厳密に働く。(K) 機で失敗する理由は
    carry の不透明性 = 例外時刻の存在。**「密度 o(1) の例外集合の外で成り立つ輸送法則」**
    という混成対象は未定義・未探索。no-go は「厳密輸送 ≠ 頻度文」を言うが、測度付き輸送は
    その前提の外。我々だけが持つ道具（実証済みテンプレート法 + M 系計測規律）の自然延長。
    最初の一歩: x2 で証明済みの輸送群を「例外集合ゼロの almost-transport」として再表現し、
    (K) 最弱機（o4: マージン 1519 倍）で例外集合の実測・成長律の測定から。
17. **FFY / Stewart 片側結果の接続**（CORE_DIGITS3N_FRONTIER で「未着手 attach」と明記）—
    (3/2)^n mod 1 の片側稠密性（Flatto–Lagarias–Pollington 系, Dubickas, 秋山）は
    我々の核の**片側弱形と同形**。既存片側定理の証明機構を o4-first スカラー
    （freq{ρ=1} < 0.8、1519 倍マージン）に移植できるかの精査 — 文献技術の内在化であって
    外部接触ではない
18. **no-go 前提の補集合マイニング** — 系統的新攻撃生成器。各不可能性定理の前提を
    条項単位で列挙し、前提を破る攻撃形の空間を機械的に張る（例: √階層 no-go の前提は
    モーメント法 — モーメントでない量（大偏差レート、one-sided tilt、KL 距離）は圏外）。
    「思いつき」でなく墓標自体から未試行域を導出する
19. **周期軌道 shadowing** — ×3/2 の周期点（6-smooth 分母の有理点）は等分布する。
    我々の軌道が等分布周期列を summable 誤差で shadow するかは未検討。2 進距離での
    shadowing 誤差の実測から
20. **機械側の豊かな不変量言語** — Coverage no-go が閉じた証明書言語の正確な外側:
    p 進解析的不変量、ℤ₂ 上多項式イデアル + 付値ガード、Parikh 自動機。1 本の probe で
    適用可否を判定できる（薄いが安価）
21. **軌道間クロス恒等式の採掘** — 単一軌道内の信号は noise-floor 確認済みだが、
    **異なる cryptid 軌道間**の厳密関係（O15/O18 同一性の類）は部分的にしか掘っていない。
    17 機の軌道を同一計器で並べ、cross-correlation でなく厳密一致・写像関係を探す
22. **独立性ルート**（LOGIC_INDEPENDENCE_PROBE: 概ね行き止まりと査定済み）— ただし
    「完全証明」の代替解決（BB(6) 値の PA/ZFC 独立性証明）としては概念的に別枠。
    現行技術（自己言及型）は我々の Π⁰₁ 具体文に届かない。[薄い・保留]

## II. o7 / SpaceNeedle / o17（(K) 外の 3 named — 新着想待ちだが内部案件）
23. **[未試行・安価] 2026-07 計器での再測定** — 3 機の既存 probe はすべて M 系規律
    （フルシェイプ走査・予告先行・前置詞剥がし・カット原則）の**確立前**のもの。x2 で
    descLaw/tail 構造を割ったのと同じ手順での再攻撃は、装備更新後の未実施事項
24. o17: ≥298 状態下界の Lean 形式化（E-tier 銀行、確実に緑にできる）+ ゲートタイミングの
    ω-正則性の再判定
25. o7/SN: thin-set 到達の p 進構造再測定（旧結論の前提を M1 級計器で再確認）

## III. 工学の山 [工学] — 数学ではなく規模。自前で登る
26. **[C] champion 停止検証** — E2 査定 GO（3–6 週、`Reaches` 層から）。着手可能
27. **[D] 全列挙の Lean パイプライン** — Coq-BB5 体制の Lean 移植。TNF 列挙 + certified
    decider 群（suite は既存）+ 残差の人手/AI 分類。年単位・並列化可能・進捗が可測
28. **[B] ~1087 holdouts** — x2 テンプレート法の工業化: 種別分類 → 族ごとの decider。
    carry 島 ~5–8 機が最初の畑。x2 閉鎖の直接の続き
29. x2 本体の完了（g=2 ゲート → ∀g → 発火）— 必要条件のうち最安

## IV. 実行順の提案
| 優先 | 項目 | 理由 |
|---|---|---|
| 1 | x2 g=2 ゲート → 完了 (#29) | 必要条件・最安・道具の実証 |
| 2 | o7/SN/o17 の計器再測定 (#23) | 安価・装備更新後未実施・3 必要条件に触る |
| 3 | almost-transport の定義と o4 実測 (#16) | (K) への唯一の「我々の形」の新対象 |
| 4 | no-go 補集合マイニング (#18) | 新攻撃の系統的生成 |
| 5 | FFY/Stewart 内在化 (#17) | 未着手 attach、片側同形 |
| 6 | champion E2 着手 (#26) | 工学の最初の山、独立進行可 |
| 7 | NEWMATH 再監査 (#12) | 何が欠けたかの精密化 |

**機械は未決定。ラベルは未昇格。x2 は [OPEN]、(K) は開いたまま。**
