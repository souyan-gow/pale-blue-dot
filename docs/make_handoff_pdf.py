#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate handoff PDF from Markdown content using reportlab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Japanese fonts
pdfmetrics.registerFont(TTFont('YuGothR', 'C:/Windows/Fonts/YuGothR.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('YuGothB', 'C:/Windows/Fonts/YuGothB.ttc', subfontIndex=0))

# Output path
OUT = os.path.join(os.path.dirname(__file__), 'handoff_performance_improvement.pdf')

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=20*mm, bottomMargin=20*mm
)

# Styles
styles = getSampleStyleSheet()
s_title = ParagraphStyle('Title_JP', fontName='YuGothB', fontSize=16, leading=22,
                         alignment=TA_CENTER, spaceAfter=6*mm)
s_subtitle = ParagraphStyle('Sub_JP', fontName='YuGothR', fontSize=9, leading=13,
                            alignment=TA_CENTER, textColor=HexColor('#666666'), spaceAfter=8*mm)
s_h1 = ParagraphStyle('H1_JP', fontName='YuGothB', fontSize=14, leading=19,
                       spaceBefore=8*mm, spaceAfter=4*mm, textColor=HexColor('#1a3a5c'))
s_h2 = ParagraphStyle('H2_JP', fontName='YuGothB', fontSize=12, leading=16,
                       spaceBefore=6*mm, spaceAfter=3*mm, textColor=HexColor('#2a5a8c'))
s_h3 = ParagraphStyle('H3_JP', fontName='YuGothB', fontSize=10, leading=14,
                       spaceBefore=4*mm, spaceAfter=2*mm)
s_body = ParagraphStyle('Body_JP', fontName='YuGothR', fontSize=9, leading=14, spaceAfter=2*mm)
s_code = ParagraphStyle('Code_JP', fontName='Courier', fontSize=7.5, leading=11,
                         spaceAfter=2*mm, leftIndent=8*mm,
                         backColor=HexColor('#f5f5f5'))
s_note = ParagraphStyle('Note_JP', fontName='YuGothR', fontSize=8, leading=12,
                         textColor=HexColor('#666666'), spaceAfter=2*mm, leftIndent=4*mm)

def tbl(data, col_widths=None, header=True):
    """Create a styled table."""
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'YuGothR'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('LEADING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]
    if header:
        style_cmds += [
            ('FONTNAME', (0, 0), (-1, 0), 'YuGothB'),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e8eef5')),
        ]
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(style_cmds))
    return t

# Build content
story = []

# Title
story.append(Paragraph('PALE BLUE DOT', s_title))
story.append(Paragraph('開発工程から保守工程（性能向上プロジェクト）への申し送り事項', s_subtitle))
story.append(Paragraph('作成日: 2026-04-07 &nbsp;&nbsp;|&nbsp;&nbsp; 作成者: 開発チーム（Claude Code 協働）', s_note))
story.append(HRFlowable(width='100%', thickness=1, color=HexColor('#cccccc')))
story.append(Spacer(1, 4*mm))

# Section 1: Project Overview
story.append(Paragraph('1. プロジェクト概要', s_h1))
story.append(Paragraph(
    '「Pale Blue Dot Delivery」は、カール・セーガンの「ペイル・ブルー・ドット」にインスパイアされた'
    'アンビエント宇宙探索ゲームのプロトタイプである。単一HTMLファイル（Three.js r128）で動作し、'
    '太陽系の惑星を自由に探索・着陸・写真撮影できる。', s_body))

story.append(Paragraph('<b>開発工程の成果:</b>', s_body))
for item in [
    '全惑星（水星〜海王星）＋月＋αケンタウリ系の実装完了',
    '地表ビュー（6層パララックス）全惑星対応',
    '写真撮影・アルバム・IndexedDB永続化',
    'Web Audio APIによるアンビエントサウンド',
    'v2.0テスト仕様書に基づく4回のテストサイクル完了（R-01〜R-58）',
]:
    story.append(Paragraph(f'・{item}', s_note))

# Section 2: Handoff Items
story.append(Paragraph('2. 性能向上への申し送り事項', s_h1))

# 2.1 Zoom
story.append(Paragraph('2.1 【必須】惑星ズーム距離の均一化', s_h2))
story.append(Paragraph(
    '惑星をクリックしてズームする際の距離が不均一である。木星・土星など大きな惑星はある程度近くまで'
    'ズームできるが、水星・地球などの小さな惑星は遠い地点でズームが止まってしまう。', s_body))
story.append(Paragraph('<b>根本原因:</b> navigateTo() 関数（約1,463行目）のズーム距離計算式が線形であるため。', s_body))
story.append(Paragraph('const targetR = pd.r > 0 ? pd.r * 12 + 30 : pd.orbitR * 0.5;', s_code))

story.append(Paragraph('各惑星のズーム距離（現状）:', s_body))
zoom_data = [
    ['惑星', '半径(r)', 'ズーム距離', '画面上の見え方'],
    ['水星', '0.383', '34.6', '非常に小さい'],
    ['金星', '0.950', '41.4', '小さい'],
    ['地球', '1.000', '42.0', '小さい'],
    ['火星', '0.532', '36.4', '非常に小さい'],
    ['木星', '10.973', '161.7', '適切'],
    ['土星', '9.140', '139.7', '適切'],
    ['天王星', '3.981', '77.8', 'やや小さい'],
    ['海王星', '3.865', '76.4', 'やや小さい'],
]
story.append(tbl(zoom_data, col_widths=[30*mm, 25*mm, 30*mm, 45*mm]))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(
    '<b>推奨修正方針:</b> 視野角ベースの計算に変更し、すべての惑星が画面上でほぼ同じ大きさに見えるようにする。'
    '影響範囲は navigateTo() 関数のみ。', s_body))

# 2.2 Surface
story.append(Paragraph('2.2 【必須】全惑星の地表描画の精巧化', s_h2))
story.append(Paragraph(
    '地表に降り立った際の描画（drawSurfaceView() 関数、約2,447〜2,840行目）が、全惑星でシンプルな'
    'パララックスレイヤー構成となっており、リアリティに欠ける。', s_body))

surface_data = [
    ['項目', '現状', '改善案', '優先度'],
    ['大気表現', 'なし', '遠方レイヤーに霞み（大気散乱）を追加', '高'],
    ['地形ディテール', 'fbmノイズのみ', 'クレーター・峡谷・岩石のテクスチャを重畳', '高'],
    ['惑星固有の演出', '土星の嵐のみ', '火星の砂嵐、金星の硫酸雲等を追加', '中'],
    ['空の表現', '単色グラデーション', '時間変化する空（薄明、星の瞬き）', '中'],
    ['地面テクスチャ', 'シルエットのみ', '前景レイヤーに岩肌・砂地テクスチャ追加', '中'],
]
story.append(tbl(surface_data, col_widths=[28*mm, 30*mm, 55*mm, 18*mm]))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(
    'テクスチャ参照元: src/solar_system_visualizer.html（1,230行）に高品質テクスチャの実装例あり。', s_note))

# 2.3 Texture Quality
story.append(Paragraph('2.3 テクスチャ品質の向上（3D惑星）', s_h2))
story.append(Paragraph(
    '11種類のプロシージャルテクスチャが512x512解像度で生成されている（362〜706行目）。'
    '4Kモニターではピクセルが目立つ。解像度を1024x1024に引き上げ、fbmノイズのオクターブ数増加で'
    '細部ディテールを追加することを推奨。起動時間への影響に注意。', s_body))

# 2.4 Startup Performance
story.append(Paragraph('2.4 起動時パフォーマンスの最適化', s_h2))
story.append(Paragraph(
    '11種のテクスチャを同期的に順次生成しているため起動に数秒かかる。ノイズ関数のルックアップテーブル化、'
    'テクスチャのIndexedDBキャッシュ、Web Workerへの移行等を検討。', s_body))

# 2.5 Render Loop
story.append(Paragraph('2.5 レンダリングループの最適化', s_h2))
story.append(Paragraph(
    'animate() 関数は毎フレーム全惑星の位置・回転を更新している。視錐台カリング、'
    '距離ベースの更新頻度制御、地球の雲回転頻度の削減等を検討。', s_body))

# 2.6 Audio
story.append(Paragraph('2.6 オーディオシステムの改善', s_h2))
story.append(Paragraph(
    'Web Audio APIのオシレーター合成で音量が小さい（R-30, R-31で指摘済み）。'
    'マスターゲイン値の再調整、マスターリミッターの追加、プリレコーデッド音源への移行を検討。', s_body))

# 2.7 Architecture
story.append(Paragraph('2.7 コードアーキテクチャの改善（中長期）', s_h2))
story.append(Paragraph(
    '約2,920行のJavaScriptが単一のbuildScene()関数内に格納されたモノリシック構造。'
    '設定の外部化 → モジュール分割 → 状態管理一元化 → テスト導入の順で段階的に改善を推奨。'
    '現在の単一ファイル構造はプロジェクト要件に基づくため、バンドラー導入が前提。', s_body))

story.append(PageBreak())

# Section 3: Known Constraints
story.append(Paragraph('3. 既知の制約事項', s_h1))
constraint_data = [
    ['項目', '内容', '備考'],
    ['Three.js', 'r128（2022年リリース）', '最新r170+。アップグレード時は互換性テスト必須'],
    ['ブラウザ対応', 'Chrome/Firefox/Safari/Edge', 'IE非対応'],
    ['IndexedDB', 'ブラウザ依存（通常50MB〜）', '写真枚数が多い場合の上限に注意'],
    ['モバイル', 'タッチ操作実装済み', '性能面での最適化は未完了'],
    ['単一ファイル', '全コードが1ファイル内', 'バンドラー導入で解消可能'],
]
story.append(tbl(constraint_data, col_widths=[28*mm, 50*mm, 60*mm]))

# Section 4: Reference Docs
story.append(Paragraph('4. 参照ドキュメント', s_h1))
ref_data = [
    ['ドキュメント', 'パス', '内容'],
    ['アーキテクチャ', 'docs/architecture.md', 'ファイル構成・技術スタック・コードセクション'],
    ['依存関係マップ', 'docs/dependency-map.md', '8層レイヤー構造・関数間依存関係'],
    ['データフロー', 'docs/data-flow.md', '起動/メインループ/ユーザー操作フロー'],
    ['コード規約', 'docs/PALE_BLUE_DOT_コード規約.md', 'コーディング規約・命名規則'],
    ['修正要望管理表', 'docs/修正要望管理表.xlsx', 'R-01〜R-58の全修正履歴'],
    ['GDD', 'docs/pale_blue_dot_gdd_v3.docx', 'ゲームデザインの詳細仕様'],
]
story.append(tbl(ref_data, col_widths=[28*mm, 48*mm, 60*mm]))

# Section 5: Lessons Learned
story.append(Paragraph('5. 開発工程で得られた知見', s_h1))
lessons = [
    ('drawIconFrame() の描画座標',
     'Canvas 2Dの drawImage() 描画先座標はクリップ領域との整合性に注意。R-40→R-52→R-58と3回の修正を要した。'),
    ('月の軌道実装',
     '地球の rotation.z が子オブジェクトに継承されるため、月の軌道リングは独立 Object3D（moonOrbitPivot）で実装。'),
    ('潮汐固定',
     'm.rotation.y = Math.PI - a で軌道角度に応じた回転を直接設定。rotSpeed: 0.0 で汎用回転処理を無効化。'),
    ('テスト→修正サイクル',
     '4回のテストサイクルでR-01〜R-58の58件を処理。Excel管理表とgitの連携運用が有効だった。'),
    ('PostToolUseフック',
     'src編集時に自動的にindex.htmlへコピーするフックが有効に機能した。'),
]
for title, desc in lessons:
    story.append(Paragraph(f'<b>{title}:</b> {desc}', s_body))

story.append(Spacer(1, 10*mm))
story.append(HRFlowable(width='100%', thickness=0.5, color=HexColor('#cccccc')))
story.append(Paragraph(
    '本ドキュメントは開発工程の完了に伴い、保守工程（性能向上プロジェクト）への引き継ぎを目的として作成されました。',
    s_note))

# Build PDF
doc.build(story)
print(f'PDF generated: {OUT}')
