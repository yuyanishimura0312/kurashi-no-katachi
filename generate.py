#!/usr/bin/env python3
"""Generate ep*.html files for kurashi-no-katachi sample articles."""
import os
from pathlib import Path

ROOT = Path(__file__).parent

PARTS = {
    'prologue': {'label': 'PROLOGUE — 序 章', 'title': '学問を暮らしの言葉に翻訳する', 'anchor': 'prologue'},
    'part-i':   {'label': 'PART I',  'title': '衣食住 ― 身体を包む環境', 'anchor': 'part-i'},
    'part-ii':  {'label': 'PART II', 'title': '暮らしの基盤 ― 一日を成り立たせるもの', 'anchor': 'part-ii'},
    'part-iii': {'label': 'PART III','title': '関係 ― 人と人のあいだ', 'anchor': 'part-iii'},
    'part-iv':  {'label': 'PART IV', 'title': 'ケアと遊 ― 身体・健康・余白', 'anchor': 'part-iv'},
    'part-v':   {'label': 'PART V',  'title': '文化と公共 ― 共有されるもの', 'anchor': 'part-v'},
    'final':    {'label': 'FINAL — 終 章', 'title': '読者の100話を編む', 'anchor': 'final'},
}


def render_toc(current_part: str, current_text: str) -> str:
    """Render TOC sidebar with current location highlighted."""
    sections = []
    for key, part in PARTS.items():
        is_current = (key == current_part)
        s = f'    <div class="toc-section">\n      <a class="toc-part" href="articles.html#{part["anchor"]}">{part["label"]}</a>'
        if part.get('title'):
            s += f'\n      <a class="toc-part-title" href="articles.html#{part["anchor"]}">{part["title"]}</a>'
        if is_current and current_text:
            s += f'\n      <span class="toc-current">{current_text}</span>'
        s += '\n    </div>'
        sections.append(s)
    return '\n'.join(sections)


def render_key_refs(refs: list) -> str:
    items = []
    for r in refs:
        items.append(f'          <li><strong>{r["cite"]}</strong><span class="ref-doi">{r["desc"]}</span></li>')
    return '\n'.join(items)


def render_signals(signals: list) -> str:
    items = []
    for i, s in enumerate(signals, 1):
        items.append(f'          <div class="signal-item">\n            <div class="signal-num">SIGNAL {i:02d}</div>\n            <p class="signal-text">{s}</p>\n          </div>')
    return '\n'.join(items)


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第{ep_num_int}話 ― {title_main} | 暮らしのかたち</title>
<meta name="description" content="暮らしのかたち第{ep_num_int}話。{title_sub_clean}">
<meta property="og:title" content="第{ep_num_int}話 ― {title_main}">
<meta property="og:description" content="{title_sub_clean}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://yuyanishimura0312.github.io/kurashi-no-katachi/{ep_id}.html">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://yuyanishimura0312.github.io/kurashi-no-katachi/{ep_id}.html">
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@300;400;500;600;700;900&family=Judson:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="read-progress" aria-hidden="true"><div class="read-progress-bar" id="readProgressBar"></div></div>

<div class="site-header-strip"></div>
<header class="site-header">
  <div class="site-header-inner">
    <a href="index.html" class="site-brand">
      <div class="site-brand-mark"><img src="assets/miratuku-mark.png" alt="ミラツク"></div>
      <div class="site-brand-text">暮らしのかたち<small>KURASHI NO KATACHI / 学術が日々の暮らしに出会うとき</small></div>
    </a>
    <nav class="site-nav">
      <a href="index.html">ホーム</a>
      <a href="articles.html">全100話</a>
      <a href="#newsletter">メルマガ</a>
    </nav>
  </div>
</header>

<section class="ep-hero">
  <div class="ep-hero-inner">
    <div class="ep-hero-eyebrow">{eyebrow}</div>
    <div class="ep-hero-num">{ep_num}.<span class="ep-hero-num-total">/ 100</span></div>
    <h1 class="ep-hero-title">{title_main}</h1>
    <p class="ep-hero-subtitle">{title_sub}</p>
    <p class="ep-hero-en">{title_en}</p>
    <p class="ep-hero-lead">{lead}</p>
    <div class="ep-hero-meta">
      <span class="ep-hero-author"><strong>西村 勇也</strong>（NPO法人ミラツク 代表理事）</span>
      <span class="ep-hero-date">2026年5月8日</span>
      <span class="read-time" id="readTime">推定読了 約8分</span>
      <span style="color: var(--ink-mute);">学術領域: {domain}</span>
    </div>
  </div>
</section>

<div class="ep-layout">

  <aside class="toc-sidebar" aria-label="連載目次">
    <div class="toc-label">FULL SERIES — 全100話</div>
{toc_sections}
  </aside>

  <article class="ep-body" id="articleBody">

{body_paragraphs}

    <details class="reading-lens" id="lens-academic-deep">
      <summary class="reading-lens-trigger">
        <span class="reading-lens-label">DEEPER</span>
        <span class="reading-lens-title">学術的な観点で深めると</span>
        <span class="reading-lens-arrow">▾</span>
      </summary>
      <div class="reading-lens-body">
        <p>{academic_deep}</p>
        <div class="signal-list">
{signals}
        </div>
      </div>
    </details>

    <details class="reading-lens" id="lens-key-reference">
      <summary class="reading-lens-trigger">
        <span class="reading-lens-label">KEY REFERENCE</span>
        <span class="reading-lens-title">この回の典拠</span>
        <span class="reading-lens-arrow">▾</span>
      </summary>
      <div class="reading-lens-body">
        <ul class="ref-list">
{key_refs}
        </ul>
      </div>
    </details>

    <section class="ep-question">
      <div class="ep-question-label">QUESTION FOR NEXT — 次号への問い</div>
      <p class="ep-question-q">{question}</p>
      <div class="ep-question-next">
        <span class="ep-question-next-meta">NEXT EPISODE</span>
        <span class="ep-question-next-title">{next_ep_title}</span>
        <a class="ep-question-next-link" href="articles.html#{next_ep_anchor}">公開を待つ →</a>
      </div>
    </section>

  </article>
</div>

<section class="ep-actions" aria-label="読了後アクション">
  <div class="ep-actions-inner">
    <a class="ep-action-btn primary" href="#newsletter">メルマガで次話を受け取る</a>
    <a class="ep-action-btn" href="#comments">この話に感想を送る</a>
    <a class="ep-action-btn" href="articles.html">全100話の地図へ</a>
  </div>
</section>

<nav class="ep-nav">
  <div class="ep-nav-inner">
    <a class="ep-nav-link{prev_disabled}" href="{prev_link}"{prev_aria}>
      <span class="ep-nav-label">← PREV</span>
      <span class="ep-nav-title">{prev_title}</span>
    </a>
    <a class="ep-nav-link next" href="{next_link}">
      <span class="ep-nav-label">NEXT →</span>
      <span class="ep-nav-title">{next_ep_title}（公開予定）</span>
    </a>
  </div>
</nav>

<section class="feedback-section" id="comments">
  <div class="feedback-inner">
    <div class="feedback-label">COMMENTS ・ 感想・コメント</div>
    <h2 class="feedback-title">この話に感想を送る</h2>
    <p class="feedback-desc">読んで感じたこと、気になった一文、ご質問、関連する話題――どのようなものでも歓迎します。編集長（西村）に直接届きます。</p>
    <form class="feedback-form" id="fbForm" onsubmit="return false;">
      <div class="feedback-field">
        <label for="fbSuggestion">コメント <span style="color:var(--accent);">*</span></label>
        <textarea id="fbSuggestion" placeholder="ご自由にお書きください" required></textarea>
      </div>
      <div class="feedback-row">
        <div class="feedback-field"><label for="fbName">お名前（任意）</label><input type="text" id="fbName" autocomplete="name" placeholder="匿名でも構いません"></div>
        <div class="feedback-field"><label for="fbEmail">メール（任意・返信が必要なときのみ）</label><input type="email" id="fbEmail" autocomplete="email" placeholder="返信不要なら空欄で"></div>
      </div>
      <button type="button" class="feedback-submit" id="fbSubmit" onclick="submitFeedback()">送信する</button>
    </form>
    <div class="feedback-done" id="fbDone">ありがとうございました。コメントを受け取りました。</div>
  </div>
</section>

<section class="newsletter" id="newsletter">
  <div class="newsletter-inner">
    <div class="newsletter-eyebrow">EMERGING FUTURE NEWSLETTER</div>
    <h2 class="newsletter-title">新しい話の公開を、まずメールで。</h2>
    <p class="newsletter-desc">本連載「暮らしのかたち」の更新通知、ミラツクの未来洞察・学術翻訳の最新情報をお届けします。配信停止はいつでも可能です。</p>
    <form class="nl-form" id="nlForm" onsubmit="return false;">
      <div class="nl-step active" id="nlStep1">
        <div class="nl-field"><input type="email" id="nlEmail" placeholder="メールアドレス" autocomplete="email"></div>
        <button type="button" class="nl-btn" onclick="nlNext()">次へ →</button>
        <div class="nl-trust">連載更新・実践事例・関連トピックをお届けします</div>
      </div>
      <div class="nl-step" id="nlStep2">
        <div class="nl-row">
          <div class="nl-field"><input type="text" id="nlName" placeholder="お名前" autocomplete="name"></div>
          <div class="nl-field"><input type="text" id="nlOrg" placeholder="所属（任意）" autocomplete="organization"></div>
        </div>
        <label class="nl-consent"><input type="checkbox" id="nlConsent" checked> メールマガジン配信に同意します。配信停止はいつでも可能です。</label>
        <button type="button" class="nl-btn" id="nlBtn" onclick="submitNl()">登録する</button>
      </div>
    </form>
    <div class="nl-done" id="nlDone">ようこそ。確認メールをお送りしました。<br>これから一緒に「暮らしのかたち」を読み解いていきましょう。</div>
  </div>
</section>

<footer class="site-footer">
  <div class="site-footer-inner">
    <div class="site-footer-cols">
      <div class="site-footer-col">
        <h4>ABOUT</h4>
        <p><strong>暮らしのかたち ― 学術が日々の暮らしに出会うとき</strong></p>
        <p style="margin-top:8px;color:var(--ink-mute);">学術領域の歴史と最先端を、毎日の食卓・関係・身体・場へと翻訳する全100回連載。NPO法人ミラツク代表理事・西村勇也。</p>
      </div>
      <div class="site-footer-col">
        <h4>NAVIGATION</h4>
        <ul>
          <li><a href="index.html">ホーム</a></li>
          <li><a href="articles.html">全100話 一覧</a></li>
          <li><a href="#newsletter">メルマガ登録</a></li>
        </ul>
      </div>
      <div class="site-footer-col">
        <h4>MIRA TUKU</h4>
        <ul>
          <li><a href="https://emerging-future.org/" target="_blank" rel="noopener">emerging-future.org</a></li>
          <li><a href="https://github.com/yuyanishimura0312/kurashi-no-katachi" target="_blank" rel="noopener">GitHub</a></li>
        </ul>
      </div>
    </div>
    <div class="site-disclaimer" style="padding: 24px 0; border-top: 1px solid var(--line); font-family: var(--serif); font-size: 12.5px; line-height: 1.95; color: var(--ink-mute); letter-spacing: 0.04em;">
      <p style="margin-bottom: 6px;"><strong style="color: var(--ink-soft);">本連載の利用について</strong></p>
      <p>本連載で紹介する研究内容は2024年時点までの公表知見に基づくもので、その後の研究で更新される可能性があります。引用した数値・効果は集団の傾向であり、個人差が大きいことが前提です。健康・医療・心理・育児に関わる判断は、必ず専門家にご相談ください。研究の存在・年代・著者は実在検証を行っていますが、解釈や要約に誤りを発見された場合はコメント欄からご指摘ください。</p>
    </div>
    <div class="site-footer-bottom">
      <span>© 2026 NPO法人ミラツク</span>
      <span>暮らしのかたち ― 学術が日々の暮らしに出会うとき</span>
    </div>
  </div>
</footer>

<script src="script.js"></script>
<script>
const EPISODE_ID = '{ep_id}';
const EPISODE_TITLE = '第{ep_num_int}話 ― {title_main}';
</script>

</body>
</html>
'''


def render_article(a: dict) -> str:
    body_html = '\n\n'.join(f'    <p>{p}</p>' for p in a['body_paragraphs'])
    toc = render_toc(a['current_part'], a.get('toc_current_text', ''))
    refs = render_key_refs(a['key_references'])
    signals_html = render_signals(a['signals'])
    title_sub_clean = a['title_sub'].replace('― ', '').replace('—', '').strip()
    return HTML_TEMPLATE.format(
        ep_id=a['ep_id'],
        ep_num=a['ep_num'],
        ep_num_int=int(a['ep_num']),
        eyebrow=a['eyebrow'],
        title_main=a['title_main'],
        title_sub=a['title_sub'],
        title_sub_clean=title_sub_clean,
        title_en=a['title_en'],
        lead=a['lead'],
        domain=a['domain'],
        toc_sections=toc,
        body_paragraphs=body_html,
        academic_deep=a['academic_deep'],
        signals=signals_html,
        key_refs=refs,
        question=a['question'],
        next_ep_title=a['next_ep_title'],
        next_ep_anchor=a.get('next_ep_anchor', 'next'),
        prev_link=a.get('prev_link', '#'),
        prev_disabled=' disabled' if a.get('is_first') else '',
        prev_aria=' aria-disabled="true"' if a.get('is_first') else '',
        prev_title=a.get('prev_title', '― 連載のはじまり ―'),
        next_link=a.get('next_link', f'articles.html#{a.get("next_ep_anchor", "next")}'),
    )


# ============================================================================
# ARTICLES DATA
# ============================================================================

from articles_data import ARTICLES as _BASE
from articles_batch1 import ARTICLES_BATCH1
from articles_batch2 import ARTICLES_BATCH2
from articles_batch3 import ARTICLES_BATCH3
from articles_batch4 import ARTICLES_BATCH4
from articles_batch5 import ARTICLES_BATCH5
from articles_batch6 import ARTICLES_BATCH6
from articles_batch7 import ARTICLES_BATCH7
from articles_batch8 import ARTICLES_BATCH8
from articles_batch9 import ARTICLES_BATCH9
from articles_batch10 import ARTICLES_BATCH10
from articles_batch11 import ARTICLES_BATCH11
from articles_batch12 import ARTICLES_BATCH12
from articles_batch13 import ARTICLES_BATCH13
from articles_batch14 import ARTICLES_BATCH14
from articles_batch15 import ARTICLES_BATCH15
from articles_batch16 import ARTICLES_BATCH16
from articles_batch17 import ARTICLES_BATCH17
from articles_batch18 import ARTICLES_BATCH18
ARTICLES = _BASE + ARTICLES_BATCH1 + ARTICLES_BATCH2 + ARTICLES_BATCH3 + ARTICLES_BATCH4 + ARTICLES_BATCH5 + ARTICLES_BATCH6 + ARTICLES_BATCH7 + ARTICLES_BATCH8 + ARTICLES_BATCH9 + ARTICLES_BATCH10 + ARTICLES_BATCH11 + ARTICLES_BATCH12 + ARTICLES_BATCH13 + ARTICLES_BATCH14 + ARTICLES_BATCH15 + ARTICLES_BATCH16 + ARTICLES_BATCH17 + ARTICLES_BATCH18

# ============================================================================
# RUN
# ============================================================================

if __name__ == '__main__':
    print(f'Generating {len(ARTICLES)} HTML files...')
    for a in ARTICLES:
        out = ROOT / f'{a["ep_id"]}.html'
        html = render_article(a)
        out.write_text(html, encoding='utf-8')
        body_chars = sum(len(p) for p in a['body_paragraphs'])
        print(f'  {a["ep_id"]}.html — {body_chars}字 / {len(a["body_paragraphs"])}段落 — {a["title_main"]}')
    print('Done.')
