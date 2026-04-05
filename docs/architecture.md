# PALE BLUE DOT — プロジェクトアーキテクチャ

## ファイル構成

```
pale_blue_dot_delivery/
├── index.html                               ← 本番ファイル（src のコピー、GitHub Pages 配信元）
├── README.md
│
├── src/
│   ├── pale_blue_dot_prototype.html         ← 開発マスター（全コード 2,925 行、ここを編集する）
│   └── solar_system_visualizer.html         ← テクスチャ・3D表現の参照元（1,230 行）
│
├── docs/
│   ├── CLAUDE.md                            ← Claude 向けハンドオフドキュメント
│   ├── architecture.md                      ← このファイル：ファイル構成・技術スタック
│   ├── dependency-map.md                    ← コード内部の層構造と依存関係
│   ├── data-flow.md                         ← ユーザー操作からデータ更新までのフロー
│   ├── requirements.md                      ← ゲーム全仕様書
│   ├── pale_blue_dot_gdd_v3.docx            ← 企画書（ゲームデザインドキュメント）
│   ├── PALE_BLUE_DOT_コード規約.md          ← コーディング規約
│   ├── PALE_BLUE_DOT_テスト仕様書_v2.0.xlsx ← テスト仕様（最新）
│   ├── PALE_BLUE_DOT_修正要望管理表.xlsx    ← 修正要望トラッカー（最新シート: v2.3）
│   └── PALE_BLUE_DOT_バグ報告書.docx        ← バグ報告テンプレート
│
├── concept_art/
│   ├── image_01_departure.png               ← 出発：地球全景
│   ├── image_02_pale_blue_dot.png           ← 火星から見た地球
│   ├── image_03_heliopause.png              ← ヘリオポーズ通過
│   ├── image_04_pale_yellow_dot.png         ← プロキシマ・ケンタウリ付近
│   └── image_05_reentry.png                 ← 大気圏突入
│
└── .claude/
    └── launch.json                          ← 開発サーバー設定（npx serve src -l 3000）
```

---

## 技術スタック

| 分類 | 技術 | バージョン | 用途 |
|------|------|-----------|------|
| 3D レンダリング | Three.js | r128 (CDN) | 太陽系・惑星メッシュ描画 |
| 2D レンダリング | HTML5 Canvas API | — | 地表ビュー・テクスチャ生成 |
| 音声 | Web Audio API | — | アンビエントサウンド・効果音 |
| 永続化 | IndexedDB | — | 写真データの保存・復元 |
| セッション管理 | localStorage | — | 起動時の初期化判定フラグ |
| ビルドツール | なし | — | ビルド不要、ブラウザで直接実行 |
| 開発サーバー | npx serve | — | ローカルテスト用のみ |

---

## 主要ファイルの役割

### `src/pale_blue_dot_prototype.html`（開発マスター）
- HTML / CSS / JavaScript がすべて1ファイルに収まるモノリシック構成
- **2,925 行**、単一の `<script>` ブロック内に全ロジックを含む
- 編集後は必ず `index.html` へコピーして本番に反映する

### `index.html`（本番ファイル）
- `src/pale_blue_dot_prototype.html` の**完全コピー**
- GitHub Pages から配信されるエントリーポイント
- 直接編集しない（src を編集 → コピーするワークフロー）

### `src/solar_system_visualizer.html`（参照用）
- 高品質テクスチャ・惑星描画の実装参照元
- ゲーム本体には含まれない独立ファイル

---

## 外部依存（CDN）

```html
<!-- Three.js r128（唯一の外部ライブラリ） -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

npm パッケージへの依存はゼロ。ブラウザのみで動作する。

---

## コード内セクション構成（pale_blue_dot_prototype.html）

| セクション | 行範囲（目安） | 内容 |
|-----------|--------------|------|
| 定数・天体データ | 282–320 | `PLANETS[]`, `PLANET_MAP{}`, 物理定数 |
| Three.js セットアップ | 320–342 | renderer / scene / camera |
| ノイズ・数学ユーティリティ | 342–358 | fbm / lerp / clamp |
| プロシージャルテクスチャ生成 | 358–706 | 11 関数（各惑星・月・星空） |
| テクスチャローダー | 706–735 | `loadAllTextures()` 非同期ロード |
| `buildScene()` 開始 | 740– | 以降全コードがこの関数スコープ内 |
| Web Audio | 740–812 | `initAudio()` / `playSfx()` / `updateAudio()` |
| 惑星メッシュ構築 | 953–1090 | `buildPlanetMesh(pd)` |
| アルファ・ケンタウリ系 | 1090–1195 | 連星系・プロキシマb 配置 |
| カメラ・入力 | 1195–1295 | spherical 座標・マウス/タッチ |
| 情報パネル | 1295–1375 | `showInfoPanel()` / `drawIconFrame()` |
| 目的地メニュー | 1375–1435 | `buildDestMenu()` / `navigateTo()` |
| 速度コントロール | 1435–1450 | simSpeed スライダー |
| スケール・単位系 | 1450–1515 | km / AU / 光年 表示 |
| IndexedDB 永続化 | 1515–1600 | `dbSavePhoto()` 等 |
| コレクションスロット | 1600–1650 | 12 実績スロット |
| 写真システム | 1650–1790 | `takePhoto()` / `generateTitle()` |
| アルバム UI | 1790–1960 | `updateAlbum()` / `makePhotoCard()` |
| 着陸シーケンス | 1960–2040 | `startLanding()` フェーズ 1〜3 |
| 地表モード | 2040–2115 | `enterSurfaceMode()` / `leaveSurfaceMode()` |
| 特殊イベント | 2115–2165 | ヘリオポーズ / αケンタウリ到達 |
| 帰還・エンディング | 2165–2395 | `startReturnJourney()` / `triggerEnding()` |
| 地表ビュー描画（2D） | 2395–2840 | `drawSurfaceView()` / `drawStormOverlay()` |
| メインアニメーションループ | 2840–2915 | `animate()` |
| 起動処理 | 2915–2923 | タイムアウト後に `animate()` 開始 |
| `buildScene()` 終了 | 2862 | `} // end buildScene()` |
| 起動エントリーポイント | 2865 | `loadAllTextures().then(()=>buildScene())` |
