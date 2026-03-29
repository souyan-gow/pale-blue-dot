#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate PALE BLUE DOT test specification as PDF. v1.1"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ─── Font ─────────────────────────────────────────────────────────────────────
FONT_NAME = "Helvetica"
for path, name in [
    ("C:/Windows/Fonts/msgothic.ttc", "MSGothic"),
    ("C:/Windows/Fonts/meiryo.ttc",   "Meiryo"),
    ("C:/Windows/Fonts/YuGothR.ttc",  "YuGothic"),
]:
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont(name, path))
            FONT_NAME = name
            print(f"Using font: {name}")
            break
        except Exception as e:
            print(f"Font fail {name}: {e}")

# ─── Colors ───────────────────────────────────────────────────────────────────
C_DARK  = colors.HexColor("#1F4E79")
C_MID   = colors.HexColor("#2E75B6")
C_LBLUE = colors.HexColor("#D5E8F0")
C_HBKG  = colors.HexColor("#2E75B6")
C_ALT   = colors.HexColor("#F7FBFF")
C_GRAY  = colors.HexColor("#F2F2F2")
C_BRD   = colors.HexColor("#CCCCCC")
C_NAROW = colors.HexColor("#E8F0FA")  # light shade for N/A cells

def S(name):
    return {
        "title":    ParagraphStyle("t",  fontName=FONT_NAME, fontSize=22, textColor=C_DARK, alignment=TA_CENTER, spaceAfter=4),
        "sub":      ParagraphStyle("s",  fontName=FONT_NAME, fontSize=14, textColor=C_MID,  alignment=TA_CENTER, spaceAfter=12),
        "h1":       ParagraphStyle("h1", fontName=FONT_NAME, fontSize=13, textColor=C_DARK, spaceBefore=14, spaceAfter=6),
        "h2":       ParagraphStyle("h2", fontName=FONT_NAME, fontSize=11, textColor=C_MID,  spaceBefore=10, spaceAfter=4),
        "body":     ParagraphStyle("b",  fontName=FONT_NAME, fontSize=8,  spaceAfter=4),
        "small":    ParagraphStyle("sm", fontName=FONT_NAME, fontSize=7,  textColor=colors.HexColor("#595959"), spaceAfter=2),
        "cell":     ParagraphStyle("c",  fontName=FONT_NAME, fontSize=7,  leading=9),
        "cell_w":   ParagraphStyle("cw", fontName=FONT_NAME, fontSize=7,  textColor=colors.white, leading=9),
        "cell_ctr": ParagraphStyle("cc", fontName=FONT_NAME, fontSize=7,  leading=9, alignment=TA_CENTER),
        "cell_dim": ParagraphStyle("cd", fontName=FONT_NAME, fontSize=7,  textColor=colors.HexColor("#AAAAAA"), leading=9, alignment=TA_CENTER),
    }[name]

# ─── Test data ─────────────────────────────────────────────────────────────────
TEST_CASES = [
    (1,  "ローディング", "プログレスバー表示",        "ページにアクセスする",                              "黒背景にプログレスバーと「初期化中...」メッセージが表示される",           "both"),
    (2,  "ローディング", "テクスチャ生成メッセージ",   "ローディング中に待機する",                          "「太陽を生成中...」等のメッセージが順番に切り替わる",                    "both"),
    (3,  "ローディング", "キーボードヒント表示",        "ローディング画面を確認する",                        "「P:撮影 N:目的地 A:アルバム M:ミュート ESC:閉じる」が表示される",        "pc"),
    (4,  "ローディング", "ロード完了・非表示",          "ロード完了後を確認する",                            "ローディング画面がフェードアウトし、3D宇宙が表示される",                  "both"),
    (5,  "3D描画",      "太陽系全体表示",              "ロード完了直後を確認する",                          "太陽・惑星・軌道ラインが表示され、惑星が公転している",                    "both"),
    (6,  "3D描画",      "軌道ドラッグ（PC）",          "マウスドラッグで画面を動かす",                      "カメラが回転し、視点が変わる",                                           "pc"),
    (7,  "3D描画",      "ズーム（PC）",                "マウスホイールを操作する",                          "カメラが前後に滑らかに移動する",                                         "pc"),
    (8,  "3D描画",      "星空背景",                    "カメラを任意の方向に向ける",                        "星空（スターフィールド）が全周に表示されている",                          "both"),
    (9,  "3D描画",      "土星リング",                  "土星に近づいてズームする",                          "リング・パーティクル・カッシーニの隙間が確認できる",                      "both"),
    (10, "3D描画",      "時間加速スライダー",           "スライダーを右に動かす",                            "惑星の公転速度が加速する。左に戻すと減速・停止する",                      "both"),
    (11, "タッチ操作",  "1本指ドラッグ",               "1本指でスワイプする",                               "カメラが回転し、視点が変わる",                                           "mob"),
    (12, "タッチ操作",  "ピンチズームイン",             "2本指を広げるピンチ操作をする",                     "カメラが近づく（ズームイン）",                                           "mob"),
    (13, "タッチ操作",  "ピンチズームアウト",           "2本指を縮めるピンチ操作をする",                     "カメラが遠ざかる（ズームアウト）",                                       "mob"),
    (14, "タッチ操作",  "タップで惑星選択",             "惑星を1本指でタップする",                           "惑星の情報パネルが表示される",                                           "mob"),
    (15, "タッチ操作",  "iOS ラバーバンド防止",         "画面端でスワイプする",                              "ブラウザの「戻る」動作が発生しない",                                     "mob"),
    (16, "惑星情報",    "クリックで情報パネル表示",     "惑星をクリック（またはタップ）する",                "右側に惑星名・事実・「この惑星を旅する」ボタンが表示される",              "both"),
    (17, "惑星情報",    "✕ボタンで閉じる",             "情報パネル右上の✕をクリックする",                   "パネルが閉じる",                                                         "both"),
    (18, "惑星情報",    "太陽は旅できない",             "太陽をクリックして情報パネルを確認する",            "「この惑星を旅する」ボタンが表示されない",                                "both"),
    (19, "着陸",        "ワープエフェクト",             "「この惑星を旅する」をクリックする",                "スピードライン→フラッシュ→着陸メッセージが表示される",                    "both"),
    (20, "着陸",        "ワープ音",                    "着陸ボタンを押した直後（音声ON時）",                "ワープ音（上昇するサウンド）が再生される",                                "both"),
    (21, "着陸",        "コックピットHUD表示",          "着陸完了後の画面を確認する",                        "コックピットフレーム・ALT/VEL/LOC/HDGが画面に表示される",                "both"),
    (22, "着陸",        "地表ドラッグ",                "地表モードでドラッグする",                          "コックピット視点が動く（全周見渡せる）",                                  "both"),
    (23, "着陸",        "「宇宙へ戻る」ボタン",         "地表で「宇宙へ戻る」をクリックする",                "コックピットが消え、軌道上に戻る",                                       "both"),
    (24, "撮影",        "撮影ボタン",                  "撮影ボタンをクリックする",                          "フラッシュ・シャッター音・撮影完了メッセージが表示される",                "both"),
    (25, "撮影",        "Pキーで撮影",                 "Pキーを押す",                                       "撮影と同じ動作が発生する",                                               "pc"),
    (26, "撮影",        "写真カウント増加",             "撮影後に写真カウントを確認する",                    "「N枚」の数字が増える",                                                  "both"),
    (27, "アルバム",    "アルバムを開く",               "アルバムボタンをクリックする",                      "コレクション12スロット＋フォトログが表示される",                          "both"),
    (28, "アルバム",    "Aキーでアルバム開閉",          "Aキーを押す",                                       "アルバムが開閉する",                                                     "pc"),
    (29, "アルバム",    "フォトログに写真が並ぶ",       "撮影後にアルバムを開く",                            "撮影した写真が「PHOTO LOG」欄にサムネイルで表示される",                   "both"),
    (30, "コレクション","旅立ちの日スロット獲得",       "最初の撮影を行う",                                  "旅立ちの日スロットが金色枠になり、チャイム音が鳴る",                      "both"),
    (31, "コレクション","惑星付近スロット獲得",         "各惑星付近で撮影する",                              "対応スロットが獲得済みになる",                                           "both"),
    (32, "コレクション","進捗カウント更新",             "スロット獲得後にアルバムを開く",                    "「N / 12」の数字が増える",                                               "both"),
    (33, "ナビ",        "目的地メニュー表示",           "目的地ボタンをクリックする",                        "全11天体のリストが左側に表示される（プロキシマbまで）",                   "both"),
    (34, "ナビ",        "Nキーでメニュー開閉",          "Nキーを押す",                                       "目的地メニューが開閉する",                                               "pc"),
    (35, "ナビ",        "HUD 近傍距離表示",             "任意の惑星に近づく",                                "「近傍: ○○ (N AU)」のように近傍天体と距離が表示される",                  "both"),
    (36, "ナビ",        "単位切替 AU→km",              "AUボタンを1回クリックする",                         "表示が「十億km」形式に変わる",                                           "both"),
    (37, "ナビ",        "単位切替 km→光年",             "kmボタンをもう1回クリックする",                     "表示が「光年」形式に変わる（近距離時はAUにフォールバック）",              "both"),
    (38, "ナビ",        "Uキーで単位切替",              "Uキーを押す",                                       "単位が切り替わる",                                                       "pc"),
    (39, "サウンド",    "初回クリックで音声開始",        "ページ表示後、最初にクリックする",                  "宇宙アンビエントドローンが聞こえ始める",                                  "both"),
    (40, "サウンド",    "ミュートボタン",               "ミュートボタンをクリックする",                      "音声がOFFになり、ミュートアイコンに変わる",                               "both"),
    (41, "サウンド",    "ミュート解除",                 "ミュートボタンを再クリックする",                    "音声が再開し、スピーカーアイコンに戻る",                                  "both"),
    (42, "サウンド",    "Mキーでミュート切替",           "Mキーを押す",                                       "ミュートが切り替わる",                                                   "pc"),
    (43, "サウンド",    "惑星共鳴音",                   "任意の惑星に非常に近づく",                          "惑星固有の共鳴音（音程）が微かに聞こえる",                               "both"),
    (44, "キーボード",  "ESCで全パネル閉じる",          "パネルを開いてESCを押す",                           "開いているパネルがすべて閉じる",                                         "pc"),
    (45, "星系",        "ヘリオポーズ通過メッセージ",   "太陽から遠く離れる（120AU付近）",                   "「ヘリオポーズを越えた」メッセージが表示される",                          "both"),
    (46, "星系",        "α星系3つの恒星表示",           "ケンタウルス座α付近まで移動する",                   "黄白（A）・橙（B）・赤（プロキシマ）3つの恒星が見える",                   "both"),
    (47, "星系",        "到達時の選択肢表示",            "α星系に接近する",                                   "「地球へ帰還する」「先へ進む」の選択肢が表示される",                      "both"),
    (48, "星系",        "プロキシマbへ着陸",            "目的地でプロキシマbを選択し旅する",                 "異星の地表にコックピットで着陸できる",                                    "both"),
    (49, "帰還",        "帰還シーケンス開始",            "「地球へ帰還する」を選択する",                      "帰還メッセージと惑星モンタージュが表示される",                            "both"),
    (50, "帰還",        "訪問惑星モンタージュ",          "帰還中の画面を確認する",                            "着陸した惑星を逆順に通過するメッセージが表示される",                      "both"),
    (51, "大気圏突入",  "突入メッセージ・速度表示",     "帰還後の大気圏突入開始を確認する",                  "「高度400km 速度7.8km/s」等のメッセージが表示される",                    "both"),
    (52, "大気圏突入",  "プラズマ火炎エフェクト",        "突入シーケンス中の画面を確認する",                  "画面周囲にオレンジ色の炎エフェクトが表示される",                          "both"),
    (53, "大気圏突入",  "カメラシェイク",               "プラズマ加熱フェーズを確認する",                    "カメラが小刻みに揺れる",                                                 "both"),
    (54, "大気圏突入",  "高度計表示",                   "突入中の画面下を確認する",                          "ALT/VEL/温度が画面下に表示される",                                       "both"),
    (55, "エンディング","エンディング画面表示",          "突入完了後を確認する",                              "カール・セーガンの引用文と旅の写真が表示される",                          "both"),
    (56, "エンディング","リスタートボタン",              "「もう一度旅をする」をクリックする",                "ページがリロードされ最初から始まる",                                      "both"),
    (57, "永続化",      "写真がリロード後も残る",        "撮影後にページをリロードする",                      "アルバムの写真カウントと写真が保持されている",                            "both"),
    (58, "永続化",      "コレクションがリロード後も残る","コレクション獲得後にリロードする",                   "獲得済みスロットが金色枠のまま保持される",                               "both"),
    (59, "モバイル",    "ボタンサイズ",                 "スマートフォンでHUDを確認する",                     "ボタンが指でタップしやすいサイズで表示される",                            "mob"),
    (60, "モバイル",    "レイアウト崩れなし",            "スマートフォンで全体レイアウトを確認する",           "テキストや要素がはみ出したり重なったりしない",                            "mob"),
    (61, "モバイル",    "アルバム3カラム表示",           "スマートフォンでアルバムを開く",                    "コレクショングリッドが3カラムで表示される",                               "mob"),
]

# ─── PDF ──────────────────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "PALE_BLUE_DOT_テスト仕様書.pdf")
PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CW = PAGE_W - MARGIN * 2  # content width

doc = SimpleDocTemplate(
    output_path, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=15*mm, bottomMargin=15*mm,
    title="PALE BLUE DOT テスト仕様書 v1.1",
    author="souyan-gow / Claude",
)

story = []

# ── Title ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 8*mm))
story.append(Paragraph("PALE BLUE DOT", S("title")))
story.append(Paragraph("テスト仕様書　v1.1", S("sub")))
story.append(HRFlowable(width=CW, thickness=2, color=C_MID))
story.append(Spacer(1, 4*mm))

def info_tbl(rows):
    data = [[Paragraph(r[0], S("cell")), Paragraph(r[1], S("cell"))] for r in rows]
    t = Table(data, colWidths=[45*mm, CW-45*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,-1), C_GRAY),
        ("FONTNAME",      (0,0),(-1,-1), FONT_NAME),
        ("FONTSIZE",      (0,0),(-1,-1), 8),
        ("GRID",          (0,0),(-1,-1), 0.5, C_BRD),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 4),
    ]))
    return t

# ── 0. 修正履歴 ───────────────────────────────────────────────────────────────
story.append(Paragraph("0. 修正履歴", S("h1")))
rev_data = [
    [Paragraph(h, S("cell_w")) for h in ["バージョン", "日付", "修正者", "修正内容"]],
    [Paragraph(v, S("cell")) for v in ["1.0", "2026/03/28", "souyan-gow", "初版作成"]],
    [Paragraph(v, S("cell")) for v in ["1.1", "2026/03/28", "souyan-gow", "修正履歴表を追加。PC/SP別の結果列を追加。凡例から□を削除。"]],
]
rev_tbl = Table(rev_data, colWidths=[18*mm, 28*mm, 32*mm, CW-78*mm])
rev_tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), C_HBKG),
    ("FONTNAME",      (0,0),(-1,-1), FONT_NAME),
    ("FONTSIZE",      (0,0),(-1,-1), 8),
    ("GRID",          (0,0),(-1,-1), 0.5, C_BRD),
    ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0),(-1,-1), 3),
    ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ("LEFTPADDING",   (0,0),(-1,-1), 4),
]))
story.append(rev_tbl)
story.append(Spacer(1, 4*mm))

# ── 1. テスト概要 ─────────────────────────────────────────────────────────────
story.append(Paragraph("1. テスト概要", S("h1")))
story.append(info_tbl([
    ("テスト対象URL",  "https://souyan-gow.github.io/pale-blue-dot/"),
    ("作成日",         "2026年3月28日"),
    ("最終更新",       "2026年3月28日（v1.1）"),
    ("テストケース数", f"{len(TEST_CASES)}件"),
    ("対象ブラウザ",   "Chrome / Firefox / Edge / Safari"),
    ("対象端末",       "PC（デスクトップ/ノート）/ スマートフォン（iOS・Android）"),
    ("テスト実施者",   ""),
    ("テスト実施日",   ""),
]))
story.append(Spacer(1, 4*mm))

# ── 2. テスト環境 ─────────────────────────────────────────────────────────────
story.append(Paragraph("2. テスト環境", S("h1")))
env_data = [
    [Paragraph(h, S("cell_w")) for h in ["区分", "詳細"]],
    [Paragraph("PC / ブラウザ", S("cell")),
     Paragraph("Google Chrome（最新版）必須。Firefox / Edge / Safari も推奨。WebGL・Web Audio・IndexedDB が有効であること。", S("cell"))],
    [Paragraph("スマートフォン", S("cell")),
     Paragraph("iOS: Safari（iPhone/iPad）/ Android: Google Chrome。音声はタップ後に有効化。WebGLサポート端末必須。", S("cell"))],
]
env_t = Table(env_data, colWidths=[35*mm, CW-35*mm])
env_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), C_HBKG),
    ("FONTNAME",      (0,0),(-1,-1), FONT_NAME),
    ("FONTSIZE",      (0,0),(-1,-1), 8),
    ("GRID",          (0,0),(-1,-1), 0.5, C_BRD),
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("TOPPADDING",    (0,0),(-1,-1), 3),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("LEFTPADDING",   (0,0),(-1,-1), 4),
]))
story.append(env_t)
story.append(Spacer(1, 4*mm))

# ── 3. 凡例（□を削除） ───────────────────────────────────────────────────────
story.append(Paragraph("3. 凡例", S("h1")))
leg_data = [
    [Paragraph(h, S("cell_w")) for h in ["記号 / 区分", "意味"]],
    [Paragraph("環境列 PC",       S("cell")), Paragraph("PCブラウザのみで確認",                             S("cell"))],
    [Paragraph("環境列 SP",       S("cell")), Paragraph("スマートフォンのみで確認",                         S("cell"))],
    [Paragraph("環境列 両方",     S("cell")), Paragraph("PC・スマートフォン両方で確認",                     S("cell"))],
    [Paragraph("PC結果 / SP結果", S("cell")), Paragraph("それぞれの環境のテスト結果を記入する欄",           S("cell"))],
    [Paragraph("○",              S("cell")), Paragraph("期待結果通りに動作した",                           S("cell"))],
    [Paragraph("×",              S("cell")), Paragraph("期待結果と異なる動作をした（バグ）",               S("cell"))],
    [Paragraph("△",              S("cell")), Paragraph("おおむね動作するが確認事項あり",                   S("cell"))],
    [Paragraph("ー",              S("cell")), Paragraph("その環境では対象外（N/A）",                        S("cell"))],
]
leg_t = Table(leg_data, colWidths=[38*mm, CW-38*mm])
leg_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), C_HBKG),
    ("BACKGROUND",    (0,1),(0,-1), C_GRAY),
    ("FONTNAME",      (0,0),(-1,-1), FONT_NAME),
    ("FONTSIZE",      (0,0),(-1,-1), 8),
    ("GRID",          (0,0),(-1,-1), 0.5, C_BRD),
    ("TOPPADDING",    (0,0),(-1,-1), 3),
    ("BOTTOMPADDING", (0,0),(-1,-1), 3),
    ("LEFTPADDING",   (0,0),(-1,-1), 4),
]))
story.append(leg_t)

story.append(PageBreak())

# ── 4. テストケース一覧 ───────────────────────────────────────────────────────
story.append(Paragraph("4. テストケース一覧", S("h1")))
story.append(Paragraph(
    f"全{len(TEST_CASES)}件。PC結果・SP結果欄に ○ / × / △ を記入してください（対象外は「ー」）。",
    S("small")))
story.append(Spacer(1, 2*mm))

# Column widths (total = CW ≈ 180mm)
# No:7, Cat:17, Item:28, Op:33, Exp:52, Env:9, PC:17, SP:17 = 180
col_w = [7*mm, 17*mm, 28*mm, 33*mm, 52*mm, 9*mm, 17*mm, 17*mm]

hdr_row = [Paragraph(h, S("cell_w"))
           for h in ["No.", "カテゴリ", "テスト項目", "操作手順", "期待結果", "環境", "PC\n結果", "SP\n結果"]]
rows = [hdr_row]

style_cmds = [
    ("BACKGROUND",    (0,0),(-1,0), C_HBKG),
    ("FONTNAME",      (0,0),(-1,-1), FONT_NAME),
    ("FONTSIZE",      (0,0),(-1,-1), 7),
    ("GRID",          (0,0),(-1,-1), 0.4, C_BRD),
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("TOPPADDING",    (0,0),(-1,-1), 2),
    ("BOTTOMPADDING", (0,0),(-1,-1), 2),
    ("LEFTPADDING",   (0,0),(-1,-1), 2),
    ("ALIGN",         (0,0),(0,-1), "CENTER"),
    ("ALIGN",         (5,0),(7,-1), "CENTER"),
]

for idx, (no, cat, item, op, exp, env) in enumerate(TEST_CASES, start=1):
    pc_val = "" if env in ("pc",  "both") else "ー"
    sp_val = "" if env in ("mob", "both") else "ー"
    env_disp = "PC" if env == "pc" else ("SP" if env == "mob" else "両方")
    pc_style = S("cell_ctr") if pc_val == "" else S("cell_dim")
    sp_style = S("cell_ctr") if sp_val == "" else S("cell_dim")
    row = [
        Paragraph(str(no),   S("cell_ctr")),
        Paragraph(cat,       S("cell")),
        Paragraph(item,      S("cell")),
        Paragraph(op,        S("cell")),
        Paragraph(exp,       S("cell")),
        Paragraph(env_disp,  S("cell_ctr")),
        Paragraph(pc_val,    pc_style),
        Paragraph(sp_val,    sp_style),
    ]
    rows.append(row)
    ri = idx  # row index in table (1-based since header is 0)
    if idx % 2 == 0:
        style_cmds.append(("BACKGROUND", (0,ri),(-1,ri), C_ALT))
    # Gray out N/A cells
    if pc_val == "ー":
        style_cmds.append(("BACKGROUND", (6,ri),(6,ri), C_NAROW))
    if sp_val == "ー":
        style_cmds.append(("BACKGROUND", (7,ri),(7,ri), C_NAROW))

tc_t = Table(rows, colWidths=col_w, repeatRows=1)
tc_t.setStyle(TableStyle(style_cmds))
story.append(tc_t)

story.append(PageBreak())

# ── 5. バグ記録シート ─────────────────────────────────────────────────────────
story.append(Paragraph("5. バグ記録シート", S("h1")))
story.append(Paragraph("テスト中に発見したバグをここに記録してください。", S("small")))
story.append(Spacer(1, 3*mm))

bug_cw = [8*mm, 14*mm, 55*mm, 15*mm, 15*mm, 15*mm, CW-122*mm]
bug_hdr = [Paragraph(h, S("cell_w")) for h in ["No.", "TC番号", "バグ内容", "環境", "優先度", "状態", "備考"]]
bug_rows = [bug_hdr] + [[Paragraph(str(i), S("cell_ctr"))] + [Paragraph("", S("cell"))]*6 for i in range(1,12)]
bug_t = Table(bug_rows, colWidths=bug_cw, repeatRows=1)
bug_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0), C_HBKG),
    ("FONTNAME",      (0,0),(-1,-1), FONT_NAME),
    ("FONTSIZE",      (0,0),(-1,-1), 7),
    ("GRID",          (0,0),(-1,-1), 0.4, C_BRD),
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("TOPPADDING",    (0,0),(-1,-1), 10),
    ("BOTTOMPADDING", (0,0),(-1,-1), 10),
    ("LEFTPADDING",   (0,0),(-1,-1), 3),
    ("ALIGN",         (0,0),(0,-1), "CENTER"),
]))
story.append(bug_t)
story.append(Spacer(1, 8*mm))

# ── 6. テスト結果サマリー ─────────────────────────────────────────────────────
story.append(Paragraph("6. テスト結果サマリー", S("h1")))
story.append(info_tbl([
    ("テスト実施日",  ""),
    ("実施者",        ""),
    ("総テスト数",    f"{len(TEST_CASES)}件"),
    ("PC ○ 合格",   ""),
    ("PC × 不合格", ""),
    ("SP ○ 合格",   ""),
    ("SP × 不合格", ""),
    ("△ 要確認",    ""),
    ("総合判定",     "合格 / 条件付き合格 / 不合格"),
    ("コメント",     ""),
]))

doc.build(story)
print(f"PDF generated: {output_path}")
print(f"Test cases: {len(TEST_CASES)}")
