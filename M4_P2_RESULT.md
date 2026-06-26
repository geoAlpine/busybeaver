# M4-P2 の結果 ＋ P2+P3 の verdict（2026-06-27）
会議決定（主線 P2 純代数、副線 P3、禁構造＝biased parity＋dual carry congruence＋integer output、最初の実験＝
人工偏り parity を整数性合同に通す）を実行した記録。`M4_P2_congruence.py`。誤証明ゼロ。

## 手計算（検証済）
`T_n = 3 T_{n-1} + 2^{n-1} r_{n-1}`、`T_{n-1} ≡ 8·3^{n-1} mod 2^{n-1}`。整数性合同 `T_n ≡ 8·3^n mod 2^n` は
```
r_{n-1} ≡ ((8·3^n − 3 T_{n-1}) / 2^{n-1})  mod 2
```
を強制 ＝ **各 parity bit が履歴から一意に決まる**。

## P2 実験の結果
- **再構成した「唯一の整数性両立 parity」＝ 実軌道**（2000/2000 完全一致、検証済）。
- **人工偏り parity（Bernoulli p=0.3–0.5、all-0、all-1）は n=1–4 で即違反**。実軌道は違反なし（自動的に満たす）。
- ⇒ **「任意の偏った parity ＋ 整数出力」は不可能**＝整数制約が全列を pin する genuine な剛性。

## P2 の正直な限界（rigidity だが bias-blind）
- **実軌道の parity は、その偏りが何であれ、合同を自動的に満たす**。だから「偏ると整数でいられない」は
  **軌道自身の偏りについては偽**。整数 seed 8 の even-density が ≥1/3 か否かは整数性では決まらない
  （停止する整数 cryptid も原理的に存在しうる）。
- **強制 bit の正体**：`r_{n-1} = bit_{n-1}(8·3^n − 3 T_{n-1}) ≈ bit_{n-1}(A·3^n) = 動く中央桁
  （moving-middle-digit）＝ マーラー core`。整数性はそれを self-consistent にするが、その平均（even-density）を
  **bound しない**。
- **VERDICT(P2)**：**整数性 ＝ 剛性（unique orbit、任意偏りを禁止）を与えるが、bias の bound は与えない
  （軌道を pin するが偏りには blind）。** P2 は「軌道の偏りを bound」を「軌道は合同の唯一整数解」に再エンコード
  するだけ。新しい bound を生まない＝funnel（最も Antihydra 固有の角度から、同じ moving-middle-digit へ）。

## P2+P3 の verdict
- P3（自律偏り ⇒ 深 cylinder 異常滞在 ⇒ 整数 run 長 ≤ 0.585n で禁）を P2 の剛性と組む自然な次手：
  「唯一の整数解の growth/run-length 構造が even-density ≥ 1/3 を**強制**するか」。
- **既出の解析（`EVEN_DENSITY_PARTIAL.md`）で marginal に不足**：maximal geometric-run シナリオ
  （run 長 = 0.585·position、O(log n) 個の幾何増大 run）が `Σ run = n` を**境界で**達成し、even-density → 0 が
  整数の run 長制約と**marginal に両立**する（n=1e9 で sum=0.99999n を確認済）。⇒ growth/整数性だけでは
  even-density → 0 を排除できない。
- **VERDICT(P2+P3)**：**整数性の剛性 ＋ run-length/growth は、even-density ≥ 1/3 を強制するには marginal に
  不足。** geometric-run の bad case が整数制約とギリギリ両立するため、P2+P3 でも壁は破れない。

## 全体の honest な結論
最も Antihydra 固有の角度（整数性の純代数）でも：
- **得たもの**：強い剛性（整数性両立 parity は唯一＝実軌道、任意偏りは即違反）。
- **得られないもの**：軌道自身の even-density の bound（強制 bit ＝ moving-middle-digit ＝ マーラー core、整数性は
  bias-blind、run-length は marginal に不足）。
- ⇒ **整数性だけでは Antihydra を decide できない**ことを precise に確定。M4（逆問題・整数性）も、他の全ルートと
  同じく moving-middle-digit ＝ マーラー core に funnel する。
- **構造的価値**：これで「順問題（端→中央）」「逆問題（整数性）」の**両方向**が閉じ、どちらからも壁＝
  moving-middle-digit ＝ マーラー core に到達することが確定した。新数学の唯一の核心は、この中央桁を
  （端からでも整数性からでもなく）**それ自身の構造から**制御すること。

## 次に残るもの
- moving-middle-digit を**直接**攻める（＝既存の open frontier、マーラー 3/2 / AEV 正規性予想）。
- toy cryptid（人工 toy → o17 / 8/3）で、整数性の剛性が**強い**ミニモデルで「P2+P3 が本当に効く最小例」を探す
  （Antihydra より整数制約が tight な人工機械なら、剛性＋run-length が bias を強制しうるか）。これが M4 に残る
  唯一の建設的次手。
