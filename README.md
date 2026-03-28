# PALE BLUE DOT
## A Journey Through the Solar System — and Beyond

---

## すぐに動かす

```bash
# ブラウザで開くだけ（サーバー不要）
open src/pale_blue_dot_prototype.html
```

または、ファイルをダブルクリックでブラウザに開く。

---

## このパッケージに含まれるもの

```
├── docs/
│   ├── CLAUDE.md               ← Claude Code 引き継ぎ書（開発者必読）
│   ├── requirements.md          ← 要件定義書（全仕様）
│   └── pale_blue_dot_gdd_v3.docx ← ゲームデザインドキュメント（企画書）
│
├── src/
│   ├── pale_blue_dot_prototype.html  ← ゲームプロトタイプ ★これを開く
│   └── solar_system_visualizer.html  ← 3Dビジュアライザー（テクスチャ資産）
│
└── concept_art/
    ├── image_01_departure.png         ← 出発前の地球
    ├── image_02_pale_blue_dot.png     ← 火星からのPale Blue Dot
    ├── image_03_heliopause.png        ← ヘリオポーズを越える
    ├── image_04_pale_yellow_dot.png   ← ケンタウルス座αから振り返る
    └── image_05_reentry.png           ← 大気圏突入・帰還
```

---

## プロトタイプの操作方法

| 操作 | 方法 |
|------|------|
| 視点回転 | マウスドラッグ |
| ズーム | マウスホイール |
| 惑星クリック | 情報パネルが開く |
| 目的地選択 | 左上「🗺 目的地」 |
| 着陸 | 情報パネルの「🚀 この惑星を旅する」 |
| 写真撮影 | 「📷 撮影」ボタン |
| アルバム | 「🖼 アルバム」ボタン |
| 時間加速 | スライダーで調整 |

**旅の目標：** ケンタウルス座αまで旅して、地球へ帰還する。

---

## 開発を続ける場合

`docs/CLAUDE.md` を Claude Code に読ませてから開発を開始してください。

```bash
# Claude Code での開発開始
claude --dangerously-skip-permissions
# 最初に CLAUDE.md を読むよう指示する
```

---

## 技術情報

- **Three.js r128**（CDN読み込み）
- **単一HTMLファイル**（サーバー不要）
- **WebGL 1.0 対応**

---

*「お互いをもっと大切にし、われわれが唯一の故郷である、*  
*この淡い青い点を、守り慈しまなければならない。」*  
*— カール・セーガン 1990*
