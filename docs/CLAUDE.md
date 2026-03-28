# PALE BLUE DOT — Claude Code 引き継ぎ書
# CLAUDE.md

このドキュメントはClaude Codeが本プロジェクトを引き継いで開発を継続するための引き継ぎ書です。

---

## プロジェクトの本質を忘れないために

このゲームは「情報」でも「刺激」でもなく、**感動の体験**を届けるものです。

カール・セーガンの言葉が起点：
> 「あの点の上で、人類の歴史のすべてが起きた。
> お互いをもっと大切にし、われわれが唯一の故郷である、
> この淡い青い点を、守り慈しまなければならない。」

コードを書くとき、常に「プレイヤーがその瞬間に何を感じるか」を考えてください。
技術的な正確さと、体験の美しさを、両立させてください。

---

## ディレクトリ構成

```
pale_blue_dot_delivery/
├── docs/
│   ├── requirements.md          ← 要件定義書（本プロジェクトの全仕様）
│   ├── CLAUDE.md                ← この引き継ぎ書
│   └── pale_blue_dot_gdd_v3.docx ← ゲームデザインドキュメント（企画書）
├── src/
│   ├── pale_blue_dot_prototype.html  ← ゲームプロトタイプ（骨格）★メイン
│   └── solar_system_visualizer.html  ← 3Dビジュアライザー（資産）
└── concept_art/
    ├── image_01_departure.png         ← 出発前の地球
    ├── image_02_pale_blue_dot.png     ← 火星からのPale Blue Dot
    ├── image_03_heliopause.png        ← ヘリオポーズを越える
    ├── image_04_pale_yellow_dot.png   ← ケンタウルス座αから振り返る
    └── image_05_reentry.png           ← 大気圏突入・帰還
```

---

## 開発の起点

### メインファイル
**`src/pale_blue_dot_prototype.html`** — これが本ゲームのプロトタイプです。
単一のHTMLファイルにすべて（Three.js描画・ゲームロジック・UI）が含まれています。
まずこのファイルをブラウザで開いて動作を確認してください。

### 資産ファイル
**`src/solar_system_visualizer.html`** — 高品質な惑星テクスチャと土星リングの実装が含まれています。
プロトタイプの惑星テクスチャをアップグレードする際は、このファイルのコードを参照・移植してください。

---

## 現在の実装状況（プロトタイプ）

### ✅ 実装済み

**航行システム**
- 目的地メニュー（全惑星＋ヘリオポーズ＋ケンタウルス座α）
- カメラの滑らかなアニメーション移動
- ドラッグ回転・ホイールズーム
- 時間加速スライダー（×0〜×100,000）

**惑星表現**
- 8惑星のプロシージャルテクスチャ（軽量版256〜512px）
- 太陽の周縁減光・グロー
- 土星リング（テクスチャ＋パーティクル8,000個）
- 地球の雲レイヤー・大気圏

**ゲームシステム**
- 惑星クリック→情報パネル表示
- 「この惑星を旅する」→着陸シーケンス（3フェーズ）
- 地表視点（コックピットモード・ドラッグで視点操作）
- 写真撮影（canvas snapshot）・アルバム表示
- ヘリオポーズ通過イベント
- ケンタウルス座α到達→帰還/前進の選択UI
- 帰還モンタージュ（主要惑星を巡る）
- 大気圏突入エフェクト
- エンディング（セーガンの言葉＋写真スライドショー）

### ❌ 未実装（優先順で）

**Phase 1（最初に取り組む）**
- 惑星テクスチャの高解像度化（solar_system_visualizer.htmlから移植）
- 宇宙船の視覚的表現
- ヘリオポーズ〜ケンタウルス座αのスケール切替（AU↔光年）
- 時間加速時の惑星軌道の正確な計算

**Phase 2**
- Pale Blue Dot図鑑（12枠コレクション）
- 各惑星からの「他の惑星の見え方」計算
- 写真のIndexedDB保存

**Phase 3**
- ケンタウルス座α星系の詳細表現
- プロキシマbへの着陸・地表ビュー
- ボイジャーモード

**Phase 4**
- サウンド実装（Web Audio API）
- 環境音エンジン

**Phase 5**
- モバイル対応
- パフォーマンス最適化

---

## コードの重要な定数・設計

### スケール定数（変更禁止）

```javascript
const SUN_R = 109.3;           // 太陽半径（地球=1の場合の比率）
const EARTH_ORBIT = 409.3;     // 地球軌道半径（scene units）= 1 AU

// 各惑星の軌道半径 = EARTH_ORBIT * realAU
// これにより距離比は実際のAU比と完全に一致する
```

### 惑星データ構造

```javascript
{
  id: 'earth',           // 識別子（小文字）
  nameJa: '地球',        // 日本語名
  nameEn: 'EARTH',       // 英語名
  color: 0x2a6fd4,       // Three.js色（数値）
  colorHex: '#2a6fd4',   // CSS色（文字列）
  r: 1.000,              // 半径（scene units、地球=1）
  orbitR: 409.3,         // 軌道半径（scene units）= EARTH_ORBIT * realAU
  period: 10,            // 公転周期（ゲーム内時間単位）
  tilt: 23.4,            // 自転軸の傾き（度）
  ring: true,            // リングの有無（土星のみ）
  facts: [...],          // 情報パネルに表示するデータ
  noTravel: true,        // trueの場合「旅する」ボタンを非表示
  isBoundary: true,      // ヘリオポーズ等の境界天体
  isStar: true,          // 恒星（ケンタウルス座α等）
}
```

### カメラ制御

```javascript
// 通常時（軌道視点）
let spherical = {theta, phi, r};  // 球面座標
let orbitTarget = new THREE.Vector3();  // 注目点
updateCamera();  // spherical → camera.position に変換

// 地表視点（コックピットモード）
cockpitMode = true;
cockpitYaw = 0;    // 左右
cockpitPitch = 0;  // 上下
// camera.rotation.set(cockpitPitch, cockpitYaw, 0, 'YXZ') をループ内で適用
```

### ゲーム状態

```javascript
let camState = 'orbit';
// 'orbit'     - 通常の太陽系ビュー
// 'landing'   - 着陸シーケンス中
// 'surface'   - 地表ビュー中
// 'returning' - 帰還旅行中
// 'reentry'   - 大気圏突入中
// 'ending'    - エンディング表示中
```

---

## テクスチャ生成の設計

プロトタイプでは軽量版のテクスチャを使用しています。
`solar_system_visualizer.html` には以下の高品質版が実装されています：

| テクスチャ | プロトタイプ | ビジュアライザー |
|-----------|------------|----------------|
| 太陽 | 512px・グラニュレーション | 2048px・周縁減光・黒点・フレア |
| 地球 | 512px・大陸・海洋 | 1024px・バイオーム・極冠 |
| 木星 | 256px・縞 | 2048px・大赤斑6層・Oval BA |
| 土星 | 256px・縞 | 2048px・極六角形・Dragon Storm |
| 土星リング | 512px | 2048px・カッシーニ間隙・エンケ間隙 |
| 海王星 | 256px・縞 | 1024px・大暗斑・スクーター |

移植手順：
1. `solar_system_visualizer.html` から `texXxx()` 関数をコピー
2. `warpFbm`, `lerp`, `clamp`, `mix3` ヘルパー関数も一緒にコピー
3. プロトタイプの `TEXTURES.xxx` に代入する部分を更新

---

## 重要な演出の実装メモ

### 「太陽が星になる」シーン
木星軌道（orbitR 2129.6）を通過後に発火。
カメラが太陽から `2129.6 * 1.5` 以上離れたとき。

```javascript
// 実装場所: checkSpecialEvents() 内
if(!sunBecomesStar && camera.position.length() > 2129.6 * 1.5) {
  sunBecomesStar = true;
  // BGMをフェードアウト
  // テキスト表示: "太陽まで光で○○分"
}
```

### ヘリオポーズ通過
距離が `HP_DIST * 0.95` を超えたとき（現在実装済み）。

### 「Pale Blue Dot」になる瞬間
海王星軌道（12307.7）付近でカメラが地球を向いているとき。
地球が画面の数ピクセル以下になったとき自動発火が理想。

### 帰還モンタージュ
現在の実装は固定順序（neptune → saturn → jupiter → mars → earth）。
**理想の実装**：プレイヤーが実際に訪問した惑星を記録し、その順番で映像を再生する。

```javascript
// 訪問記録の追跡
const visitedPlanets = [];  // ['earth', 'mars', 'saturn', ...]
// 帰還時はvisitedPlanetsを逆順に巡る
```

### 大気圏突入エフェクト
現在は単純なdiv要素でのオーバーレイ。
強化案：Three.jsのパーティクルシステムでプラズマを表現。

---

## デプロイ方法

### 最小構成（静的ホスティング）

単一HTMLファイルで動作。Three.jsはCDNから読み込む。

```bash
# Vercel
vercel deploy --name pale-blue-dot

# Netlify
netlify deploy --dir . --prod

# GitHub Pages
# リポジトリにpushしてSettings→Pages→Deploy from branch
```

### 本番環境で変えるべきこと

1. CDNからのThree.jsをローカルファイルにする（オフライン対応）
2. テクスチャ生成をワーカースレッドに移動（UI freeze防止）
3. テクスチャをキャッシュする（LocalStorageまたはIndexedDB）

---

## 科学的正確さのチェックリスト

新機能を追加するとき、以下を必ず確認：

- [ ] 軌道半径は `EARTH_ORBIT * realAU` になっているか
- [ ] 惑星半径は地球比で正確か（地球=1.0）
- [ ] 惑星のデータは実際のNASAデータと一致しているか
- [ ] 距離の表示は「光が届く時間」で表現されているか
- [ ] 科学的仮説（プロキシマbの地表など）には「仮説」と明記されているか

---

## ゲームデザインの原則（コードに反映すること）

1. **失敗させない** — 燃料切れ・敵・ゲームオーバーは存在しない
2. **強制しない** — どの惑星に行くか、いつ写真を撮るか、すべてプレイヤーが決める
3. **静寂を大切に** — 演出過多にならない。余白が感動を生む
4. **数字より体感** — 「8億km」より「光で44分」で表現する
5. **偶然の美を残す** — 土星リングの影など、計算された演出でない美しさを守る

---

## よくある質問

**Q: なぜ単一HTMLファイルなのか？**  
A: インストール不要・デプロイが簡単・ファイル間の依存関係がない。
プロトタイプ段階ではこのシンプルさが最重要。本番ではバンドラーの導入を検討。

**Q: Three.jsのバージョンはr128固定か？**  
A: プロトタイプではr128を使用。CDNのURLを変えれば更新可能。
ただし大きなAPIの変更があるため、アップデート前にテストが必要。

**Q: テクスチャを画像ファイルに変えられるか？**  
A: `THREE.CanvasTexture(canvas)` の代わりに `THREE.TextureLoader().load('url')` を使えば可能。
ただしCORSの問題があるため、同一ドメインにファイルを置く必要がある。

**Q: ケンタウルス座αまでの距離が正しく表示されないのはなぜか？**  
A: 現在のscene unitsが `109,000,000`（4.24光年）程度になる。
Three.jsのfloat精度の問題が出る可能性がある。スケール層の分離が必要。

---

## 連絡事項

このプロジェクトは会話の中で設計・開発が進められました。
企画書（GDD v3）、要件定義書、プロトタイプがすべて揃っています。

次のステップとして推奨するのは：

1. **まず動かして確認** — `pale_blue_dot_prototype.html` をブラウザで開く
2. **高解像度テクスチャの移植** — `solar_system_visualizer.html` から
3. **Phase 1の実装** — 要件定義書のPhase 1リストを順番に

何かわからないことがあれば、`docs/requirements.md` と `docs/pale_blue_dot_gdd_v3.docx` を参照してください。

---

*"The cosmos is within us. We are made of star-stuff."*  
*— Carl Sagan*
