# PALE BLUE DOT — コード規約

> バージョン: 1.0
> 作成日: 2026-04-05
> 対象ファイル: `src/pale_blue_dot_prototype.html` / `index.html`

---

## 1. プロジェクト構成

### 1.1 ファイル構成

```
pale_blue_dot_delivery/
├── index.html                    # 公開用（src/からコピー）
├── src/
│   └── pale_blue_dot_prototype.html  # 開発用マスター
└── docs/
    ├── PALE_BLUE_DOT_テスト仕様書_v2.0.xlsx
    ├── PALE_BLUE_DOT_修正要望管理表.xlsx
    └── PALE_BLUE_DOT_コード規約.md
```

### 1.2 シングルファイル原則

- **すべてのコード（HTML/CSS/JS/テクスチャ生成）は1つのHTMLファイルに収める**
- 外部ファイル依存は Three.js CDN（`r128`）のみ
- 追加ライブラリは原則禁止（軽量さと移植性を優先）
- 編集は必ず `src/pale_blue_dot_prototype.html` に対して行い、完了後 `index.html` にコピーする

---

## 2. HTML/CSS 規約

### 2.1 セレクタ

- **グローバルな要素セレクタは使わない**
  Three.js や動的生成要素への意図しない適用を防ぐため、スタイルは必ず ID またはクラスで限定する
  ```css
  /* NG */
  canvas { position: fixed; ... }

  /* OK */
  #c { position: fixed; ... }
  ```

- **`:root` のカスタムプロパティは使わない**（実行時書き換えが発生しない変数はJS定数で管理）

### 2.2 z-index 階層

以下の階層に従って z-index を割り当てる。新規要素は必ずこの表を参照して値を決定すること。

| z-index | 用途 |
|---------|------|
| 0 | Three.js WebGL キャンバス（`#c`） |
| 10 | HUD（`#hud`） |
| 15 | 目的地メニュー（`#dest-menu`） |
| 16 | コックピットオーバーレイ（`#cockpit`） |
| 30 | アルバム（`#album`） |
| 40 | シーケンス（`#sequence`） |
| 45 | メッセージオーバーレイ（`#msg-overlay`） |
| 47 | スピードラインキャンバス（`#speed-lines-c`） |
| 48 | 着陸オーバーレイ（`#land-overlay`） |
| 50 | 情報パネル（`#info-panel`） / α星系選択肢（動的生成） |
| 55 | 地表キャンバス（`#surface-canvas`） |
| 56 | 地表UI（`#surface-ui`） |
| 60 | エンディング（`#ending`） |
| 100 | ローディング（`#loading`） |

> **ルール**: `#info-panel` は `#album`（z-index:30）より上に置く必要がある。
> 動的生成する全画面オーバーレイは z-index:50 を使う。

### 2.3 CSS セクション構造

CSS ブロックはコメントで機能単位に区切る:

```css
/* ── HUD ── */
/* ── DESTINATION MENU ── */
/* ── INFO PANEL ── */
/* ── ALBUM ── */
/* ── COCKPIT OVERLAY ── */
/* ── SEQUENCE OVERLAYS ── */
/* ── LANDING OVERLAY ── */
/* ── ENDING ── */
/* ── MOBILE RESPONSIVE ── */
/* ── LOADING ── */
```

---

## 3. JavaScript 規約

### 3.1 セクション構造

JS ブロックはすべて以下の区切りコメントで整理する:

```javascript
// ═══════════════════════════════════════════════════════════════════════
// セクション名
// ═══════════════════════════════════════════════════════════════════════
```

主なセクション一覧:

```
PLANET DATA
WEB AUDIO — AMBIENT SOUND SYSTEM
BUILD SOLAR SCENE
TEXTURE GENERATORS
MESH BUILDERS
INPUT HANDLING
INFO PANEL
DESTINATION MENU
SPEED CONTROL
SCALE UNIT SYSTEM
NAVIGATION / HUD
PHOTO SYSTEM
ALBUM
SPECIAL EVENTS
RETURN JOURNEY
MAIN ANIMATION LOOP
STARTUP
```

### 3.2 命名規則

| 対象 | 規則 | 例 |
|------|------|-----|
| 定数 | `UPPER_SNAKE_CASE` | `SUN_R`, `EARTH_ORBIT`, `UNIT_MODES` |
| グローバル変数 | `camelCase` | `simSpeed`, `camState`, `cockpitMode` |
| 関数 | `camelCase` 動詞始まり | `buildScene()`, `showInfoPanel()`, `updateAudio()` |
| DOM ID | `kebab-case` | `info-panel`, `speed-range`, `album-grid` |
| Three.js オブジェクト | `camelCase` + 型示唆 | `planetMeshes`, `orbitAngles`, `sunLight` |
| イベントコールバック | 無名関数を優先（1回限り）or 名前付き関数 | |

### 3.3 グローバル状態変数

以下はゲーム全体の状態を持つグローバル変数。変更は必ず所定の関数を通じて行う:

| 変数 | 型 | 説明 |
|------|----|------|
| `simSpeed` | number | 時間加速倍率（0=停止, 1=等速） |
| `camState` | string | カメラ状態: `'orbit'` / `'landing'` / `'surface'` / `'returning'` / `'reentry'` |
| `cockpitMode` | boolean | コックピット視点モード |
| `photos` | array | 撮影した写真オブジェクトの配列 |
| `collectionMap` | object | コレクションスロットID→写真のマップ |
| `photoDB` | IDBDatabase | IndexedDB インスタンス |
| `currentPlanetInfo` | object\|null | 現在表示中の惑星情報（null = パネル非表示） |

### 3.4 simSpeed の扱い

- **軌道運動** (`orbitAngles`): `simSpeed * dt` で更新 → 停止時に軌道も止まる
- **自転運動** (`rotation.y`): `Math.max(1, simSpeed) * dt` で更新 → 停止時でも最低1倍速で自転継続
- **音声更新** (`updateAudio`): simSpeed には依存しない

```javascript
// 軌道
orbitAngles[pd.id] += orbitSpeed * dt * s;

// 自転（simSpeed=0でも止まらない）
m.rotation.y += pd.rotSpeed * dt * Math.max(1, s);
```

### 3.5 非同期処理

- IndexedDB の操作は必ず Promise でラップし `async/await` で呼ぶ
- テクスチャ生成は `loadAllTextures()` 内で 1 フレームごとに `yield`（UI フリーズ防止）

```javascript
// OK
async function loadAllTextures() {
  for (const job of jobs) {
    TEXTURES[job.key] = job.fn();
    await new Promise(r => setTimeout(r, 0));  // yield to browser
  }
}
```

---

## 4. Three.js 規約

### 4.1 バージョン固定

- **Three.js r128** を使用（CDN: `cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`）
- r128 以降の API（例: `THREE.WebGLRenderer`の `outputEncoding` 削除）は使用しない

### 4.2 メッシュ管理

```javascript
// 惑星メッシュは planetMeshes[pd.id] で管理
const planetMeshes = {};

// メッシュ追加
planetMeshes[pd.id] = mesh;
scene.add(mesh);

// 重複追加禁止チェック
function buildPlanetMesh(pd) {
  if (pd.r === 0 || pd.isBoundary || pd.isStar || pd.isExoplanet) return;
  // ...
}
```

- `isExoplanet: true` フラグを持つ惑星は `buildPlanetMesh()` でスキップし、
  `buildProximaSystem()` 内で専用ロジックにより配置する

### 4.3 カメラ制御

```javascript
// spherical 座標系でカメラを管理
const spherical = new THREE.Spherical();
const orbitTarget = new THREE.Vector3();

function updateCamera() {
  // spherical + orbitTarget → camera.position
}
```

- ドラッグ: `spherical.theta` / `spherical.phi` を更新してから `updateCamera()`
- ズーム: `spherical.r` を clamp してから `updateCamera()`
- コックピット視点: `cockpitYaw` / `cockpitPitch` を `camera.rotation` に直接セット

### 4.4 CanvasTexture 生成

```javascript
function mkCanvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return c;
}

function texXxx() {
  const c = mkCanvas(1024, 1024), g = c.getContext('2d');
  // ... Canvas 2D 描画 ...
  return new THREE.CanvasTexture(c);
}
```

- テクスチャは `TEXTURES` オブジェクトにキャッシュ（再生成禁止）
- 解像度基準: 主要惑星 1024×1024 / 星空背景 2048×1024

---

## 5. Web Audio 規約

### 5.1 ノード構成

```
oscillators → droneFilter → droneGain ─┐
                                        ├→ master → AudioContext.destination
proxOsc → proxFilter → proxGain ───────┤
noiseSrc → noiseFilter → noiseGain ────┘
```

### 5.2 初期化

- `initAudio()` は **ユーザー操作（ミュートボタン押下）** の後に呼ぶ
  （ブラウザの Autoplay Policy 対応）
- `audioStarted` フラグで二重初期化を防ぐ

### 5.3 ゲイン基準値

| ノード | 通常値 | 備考 |
|--------|--------|------|
| `master.gain` | 0.5 | 全体音量 |
| `droneGain.gain` | 0.35 | アンビエントドローン |
| `proxGain.gain` | 0〜0.45 | 惑星接近時に上昇 |
| `noiseGain.gain` | 0〜0.04 | 地表風音 |

### 5.4 フェード規則

- ゲインの急変は禁止。必ず `linearRampToValueAtTime` を使う

```javascript
// OK
audioNodes.droneGain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.3);

// NG（クリックノイズが発生）
audioNodes.droneGain.gain.value = 0;
```

### 5.5 アンビエントサウンドの ON/OFF 制御

以下の状態では droneGain / proxGain を 0 にフェードアウトすること:

- `camState === 'surface'`（地表ビュー中）
- `#album` が表示中（アルバム閲覧中）
- `#ending` が表示中（エンディング画面）

---

## 6. Canvas 2D テクスチャ生成規約

### 6.1 共通ヘルパー

```javascript
function mkCanvas(w, h) { ... }  // キャンバス作成
function lerp(a, b, t) { ... }   // 線形補間
function clamp(v, lo, hi) { ... } // 値のクランプ
```

### 6.2 命名

テクスチャ生成関数は `tex` プレフィックスで統一:

```javascript
texStarfield()  // 星空
texSun()        // 太陽
texEarth()      // 地球
// ...
```

### 6.3 パフォーマンス

- テクスチャ生成はロード時（`loadAllTextures()`）に一度だけ行う
- ゲームループ内での Canvas 2D 操作はスピードラインと地表ビューのみ
- `requestAnimationFrame` でアニメーションするキャンバスは必ず `cancelAnimationFrame` でクリーンアップ

---

## 7. IndexedDB / localStorage 規約

### 7.1 DB 構成

```
DB名: PaleBlueDotPhotos
ObjectStore: photos
  keyPath: id (自動採番)
  index: slotId (コレクションスロット識別子)
```

### 7.2 セッション管理

| キー | ストア | 用途 |
|------|--------|------|
| `pbd_session` | localStorage | セッション継続フラグ（存在する場合は写真を引き継ぐ） |

- `pbd_session` が存在しない場合: IndexedDB クリア → 新規セッション
- ハードリロード検出: `performance.getEntriesByType('navigation')[0].transferSize > 0`

### 7.3 写真オブジェクト構造

```javascript
{
  id: number,          // DB 自動採番
  dataUrl: string,     // Base64 PNG
  label: string,       // 写真タイトル
  location: string,    // 撮影場所（惑星名など）
  dist: number,        // 撮影時の距離（scene units）
  slotId: string|null, // コレクションスロットID（例: 'earth', 'departure'）
  timestamp: number    // Date.now()
}
```

### 7.4 メモリ同期

IndexedDB の変更は必ずメモリ上の `photos` 配列と `collectionMap` にも同期すること:

```javascript
// 削除時
photos.splice(idx, 1);
if (slotId) delete collectionMap[slotId];
await dbDeletePhoto(id);
updateAlbum();

// クリア時（clearAllPhotos()）
photos.length = 0;
Object.keys(collectionMap).forEach(k => delete collectionMap[k]);
```

---

## 8. イベントハンドリング規約

### 8.1 キーボード

```javascript
window.addEventListener('keydown', e => {
  if (e.repeat) return;  // キーリピートは無視
  const key = e.key.toLowerCase();
  switch (key) {
    case 'p': /* 撮影 */ break;
    case 'n': /* 目的地メニュー */ break;
    case 'a': /* アルバム */ break;
    case 'm': /* ミュート */ break;
    case 'u': /* 単位切替 */ break;
    case 'escape': /* 全パネル閉じる */ break;
  }
});
```

### 8.2 マウス

- **クリック判定**: `mousedown` 時に `clickStart` を記録し、`mouseup` 時に移動距離 < 5px ならクリックと判定
- **ドラッグ**: `mousemove` で `isDragging` フラグが true の間のみ処理
- **ホイール**: `e.preventDefault()` + `passive: false` オプション必須

```javascript
canvas.addEventListener('wheel', e => {
  if (cockpitMode) return;
  if (e.ctrlKey) {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -1 : 1;  // 上回し=ズームイン
    // ...
  }
}, { passive: false });
```

### 8.3 タッチ

- ピンチズームは `touchStartDist` で開始距離を記録し、`touchmove` で比率を計算
- `e.preventDefault()` を `touchstart` と `touchmove` の両方に付ける（`passive: false`）

### 8.4 イベント対象

- メインキャンバス（`#c`）: ドラッグ・ホイール・クリック判定
- 地表キャンバス（`#surface-canvas`）: 地表ビュー中のドラッグ（cockpitYaw/cockpitPitch 更新）
- HUD ボタン類: 通常の `addEventListener('click', ...)`

---

## 9. ゲームループ規約

### 9.1 animate() の責務

`animate()` は以下の順序で処理する:

```javascript
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.05);  // dt 上限: 50ms（タブ非活性対策）
  const s = simSpeed;

  // 1. 惑星の軌道・自転更新
  // 2. カメラ制御（cockpitMode の場合）
  // 3. 再突入シェイク適用
  // 4. 特殊イベントチェック（checkSpecialEvents）
  // 5. HUD・コックピットHUD 更新
  // 6. オーディオ更新
  // 7. renderer.render()
}
```

### 9.2 dt の扱い

- `dt` は `clock.getDelta()` で取得し、**0.05秒（50ms）を上限にクランプ**する
  （タブが非アクティブになった後に戻ると巨大な dt が来るため）
- **物理演算や位置更新には必ず `dt` を掛ける**（フレームレート非依存）

### 9.3 camState 遷移

```
'orbit' ──(旅する)──→ 'landing' ──(着陸完了)──→ 'surface'
                                                      ↓(宇宙へ戻る)
'reentry' ←──(帰還)── 'returning' ←──(地球へ帰還)── 'orbit'
    ↓(突入完了)
  ending
```

---

## 10. 禁止事項

| 禁止 | 理由 |
|------|------|
| `document.write()` | DOM 破壊リスク |
| `eval()` | セキュリティリスク |
| `innerHTML` へのユーザー入力直接代入 | XSS リスク |
| グローバルな `canvas{}` CSS ルール | Three.js / アルバム canvas への意図しない適用 |
| `setTimeout(fn, 0)` のゲームループ代替 | `requestAnimationFrame` を使うこと |
| Three.js r128 以外のバージョン | API 互換性の維持 |
| 外部 CDN の追加（Three.js 以外） | シングルファイル原則の維持 |

---

## 11. 変更フロー

```
1. src/pale_blue_dot_prototype.html を編集
2. ブラウザで動作確認
3. テスト仕様書の関連 TC をチェック
4. 問題なければ index.html にコピー
   cp src/pale_blue_dot_prototype.html index.html
5. git add / commit / push
6. 修正要望管理表のステータスを「完了」に更新
```
