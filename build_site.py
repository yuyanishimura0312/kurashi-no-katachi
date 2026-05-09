#!/usr/bin/env python3
"""Build full kurashi-no-katachi site:
- articles.html (100-article roadmap)
- index.html (home page)
- Stub HTML for 90 unpublished episodes
"""
import os
from pathlib import Path
from roadmap import ROADMAP, get_part_for_ep, get_published_eps

ROOT = Path(__file__).parent
PUBLISHED = get_published_eps()

PARTS = {
    'prologue': {'label': 'PROLOGUE — 序 章', 'title': '学問を暮らしの言葉に翻訳する', 'tagline': '4部構成と暮らしのシーン27の地図'},
    'part-i':   {'label': 'PART I',  'title': '衣食住 ― 身体を包む環境', 'tagline': '食事・住宅・ファッション――身体を取り巻くものから'},
    'part-ii':  {'label': 'PART II', 'title': '暮らしの基盤 ― 一日を成り立たせるもの', 'tagline': '睡眠・家事・はたらく・教育の見えない働き'},
    'part-iii': {'label': 'PART III','title': '関係 ― 人と人のあいだ', 'tagline': '恋愛・結婚・育児・ペットを編む人間関係の科学'},
    'part-iv':  {'label': 'PART IV', 'title': 'ケアと遊 ― 身体・健康・余白', 'tagline': '医療・看護介護・スポーツ観戦・旅・祭り'},
    'part-v':   {'label': 'PART V',  'title': '文化と公共 ― 共有されるもの', 'tagline': '芸術・メディア・ショッピング・図書館博物館・公園広場・産業'},
    'final':    {'label': 'FINAL — 終 章', 'title': '読者の100話を編む', 'tagline': '100話の俯瞰と次の問いへ'},
}

# ============================================================================
# articles.html (full roadmap)
# ============================================================================

def build_articles_html() -> str:
    parts_html = []
    for part_key, part in PARTS.items():
        eps = [r for r in ROADMAP if get_part_for_ep(r[0]) == part_key]
        items = []
        for r in eps:
            ep_num, eyebrow, title_main, title_sub, scene, domain, status = r
            badge = '<span class="ep-badge published">公開中</span>' if status == 'published' else '<span class="ep-badge planned">公開予定</span>'
            link = f'ep{ep_num}.html'
            items.append(f'''        <a class="ep-item {status}" href="{link}" id="ep{ep_num}">
          <div class="ep-item-num">{ep_num}<span class="ep-item-num-total">/100</span></div>
          <div class="ep-item-body">
            <div class="ep-item-eyebrow">{eyebrow.split('・')[1].strip() if '・' in eyebrow else scene}</div>
            <div class="ep-item-title">{title_main}</div>
            <div class="ep-item-sub">― {title_sub}</div>
            <div class="ep-item-meta"><span>{domain}</span>{badge}</div>
          </div>
        </a>''')
        parts_html.append(f'''    <section class="part-section" id="{part_key}">
      <div class="part-header">
        <div class="part-label">{part["label"]}</div>
        <h2 class="part-title">{part["title"]}</h2>
        <p class="part-tagline">{part["tagline"]}</p>
        <div class="part-stats">{len(eps)}話 ／ 公開済 {sum(1 for e in eps if e[6]=="published")}話</div>
      </div>
      <div class="ep-list">
{chr(10).join(items)}
      </div>
    </section>''')

    parts_jump = '\n'.join(
        f'      <a class="part-jump-card" href="#{key}"><div class="part-jump-num">{p["label"].split()[1] if " " in p["label"] else p["label"]}</div><div class="part-jump-name">{p["title"]}</div><div class="part-jump-sub">{p["tagline"]}</div></a>'
        for key, p in PARTS.items() if key not in ('prologue', 'final')
    )

    total_published = sum(1 for r in ROADMAP if r[6] == 'published')
    progress_pct = round(total_published / 100 * 100)

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全100話 ロードマップ | 暮らしのかたち</title>
<meta name="description" content="連載「暮らしのかたち」全100話の地図。序章5話・PART I-V各18話・終章5話の構成。">
<meta property="og:title" content="全100話 ロードマップ | 暮らしのかたち">
<meta property="og:type" content="website">
<link rel="canonical" href="https://yuyanishimura0312.github.io/kurashi-no-katachi/articles.html">
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@300;400;500;600;700;900&family=Judson:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<style>
.page-banner {{ background: var(--bg); padding: 80px 24px 48px; border-bottom: 1px solid var(--line); }}
.page-banner-inner {{ max-width: 1080px; margin: 0 auto; }}
.page-banner-eyebrow {{ font-family: var(--sans); font-size: 11px; letter-spacing: 0.32em; color: var(--accent); font-weight: 700; display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }}
.page-banner-eyebrow::before {{ content: ""; width: 32px; height: 2px; background: var(--accent); }}
.page-banner-title {{ font-family: var(--serif); font-weight: 700; font-size: 40px; line-height: 1.45; letter-spacing: 0.04em; color: var(--ink); margin-bottom: 14px; }}
.page-banner-en {{ font-family: var(--display); font-weight: 400; font-size: 20px; color: var(--ink-mute); margin-bottom: 32px; }}
.page-stats {{ display: grid; grid-template-columns: repeat(4, auto); gap: 32px; align-items: baseline; padding-top: 24px; border-top: 1px solid var(--line); font-family: var(--sans); font-size: 11px; letter-spacing: 0.12em; color: var(--ink-mute); }}
.page-stats span {{ display: flex; flex-direction: column; gap: 4px; }}
.page-stats span strong {{ font-family: var(--display); font-weight: 700; font-size: 22px; color: var(--ink); letter-spacing: 0; }}

.series-progress {{ max-width: 1080px; margin: 32px auto 0; padding: 0 24px; }}
.series-progress-bar-wrap {{ background: var(--bg-tint); height: 6px; position: relative; overflow: hidden; }}
.series-progress-bar-fill {{ background: var(--accent); height: 100%; width: {progress_pct}%; }}
.series-progress-meta {{ display: flex; justify-content: space-between; align-items: baseline; margin-top: 8px; font-family: var(--sans); font-size: 10.5px; color: var(--ink-mute); letter-spacing: 0.14em; }}
.series-progress-meta strong {{ color: var(--ink); font-weight: 700; }}

.parts-jump {{ max-width: 1080px; margin: 56px auto 0; padding: 0 24px; }}
.parts-jump-label {{ font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 0.26em; color: var(--accent); margin-bottom: 14px; }}
.parts-jump-title {{ font-family: var(--serif); font-weight: 700; font-size: 22px; color: var(--ink); margin-bottom: 24px; }}
.parts-jump-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }}
.part-jump-card {{ background: var(--bg); border: 1px solid var(--line); padding: 22px 20px; text-decoration: none; display: flex; flex-direction: column; gap: 8px; transition: border-color .15s, transform .15s; }}
.part-jump-card:hover {{ border-color: var(--accent); transform: translateY(-2px); text-decoration: none; }}
.part-jump-num {{ font-family: var(--display); font-weight: 700; font-size: 24px; color: var(--accent); line-height: 1; }}
.part-jump-name {{ font-family: var(--serif); font-weight: 700; font-size: 15px; color: var(--ink); line-height: 1.55; }}
.part-jump-sub {{ font-family: var(--sans); font-size: 10.5px; color: var(--ink-mute); line-height: 1.65; }}

.content-main {{ max-width: 1080px; margin: 64px auto 0; padding: 0 24px 80px; }}

.part-section {{ margin-bottom: 80px; }}
.part-section:last-child {{ margin-bottom: 0; }}
.part-header {{ padding-bottom: 24px; border-bottom: 2px solid var(--ink); margin-bottom: 32px; }}
.part-label {{ font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: 0.28em; color: var(--accent); margin-bottom: 12px; }}
.part-title {{ font-family: var(--serif); font-weight: 700; font-size: 26px; color: var(--ink); letter-spacing: 0.04em; margin-bottom: 8px; }}
.part-tagline {{ font-family: var(--serif); font-size: 14px; color: var(--ink-soft); line-height: 1.85; margin-bottom: 16px; }}
.part-stats {{ font-family: var(--sans); font-size: 11px; letter-spacing: 0.14em; color: var(--ink-mute); }}

.ep-list {{ display: flex; flex-direction: column; gap: 0; }}
.ep-item {{ display: grid; grid-template-columns: 64px 1fr; gap: 20px; padding: 22px 0; border-bottom: 1px solid var(--line-soft); text-decoration: none; transition: background .15s; }}
.ep-item:hover {{ background: var(--bg-soft); text-decoration: none; }}
.ep-item.planned {{ opacity: 0.66; }}
.ep-item-num {{ font-family: var(--display); font-weight: 700; font-size: 24px; color: var(--accent); line-height: 1; }}
.ep-item-num-total {{ font-family: var(--sans); font-size: 10px; color: var(--ink-mute); margin-left: 2px; letter-spacing: 0.06em; }}
.ep-item-body {{ display: flex; flex-direction: column; gap: 6px; }}
.ep-item-eyebrow {{ font-family: var(--sans); font-size: 9.5px; font-weight: 700; letter-spacing: 0.22em; color: var(--accent); text-transform: uppercase; }}
.ep-item-title {{ font-family: var(--serif); font-weight: 700; font-size: 17px; color: var(--ink); line-height: 1.55; letter-spacing: 0.04em; }}
.ep-item-sub {{ font-family: var(--serif); font-size: 13.5px; color: var(--ink-soft); line-height: 1.7; letter-spacing: 0.04em; }}
.ep-item-meta {{ display: flex; align-items: center; gap: 14px; margin-top: 4px; font-family: var(--sans); font-size: 10.5px; color: var(--ink-mute); letter-spacing: 0.08em; }}
.ep-badge {{ display: inline-block; padding: 3px 10px; font-family: var(--sans); font-size: 9.5px; font-weight: 700; letter-spacing: 0.16em; border: 1px solid var(--line); }}
.ep-badge.published {{ color: var(--accent); border-color: var(--accent); }}
.ep-badge.planned {{ color: var(--ink-mute); border-color: var(--ink-mute); }}

@media (max-width: 760px) {{
  .page-banner-title {{ font-size: 28px; }}
  .page-stats {{ grid-template-columns: repeat(2, auto); gap: 18px; }}
  .ep-item {{ grid-template-columns: 1fr; gap: 8px; }}
  .ep-item-title {{ font-size: 15px; }}
}}
</style>
</head>
<body>

<div class="site-header-strip"></div>
<header class="site-header">
  <div class="site-header-inner">
    <a href="index.html" class="site-brand">
      <div class="site-brand-mark"><img src="assets/miratuku-mark.png" alt="ミラツク"></div>
      <div class="site-brand-text">暮らしのかたち<small>KURASHI NO KATACHI / 学術が日々の暮らしに出会うとき</small></div>
    </a>
    <nav class="site-nav">
      <a href="index.html">ホーム</a>
      <a href="articles.html" class="active">全100話</a>
      <a href="index.html#newsletter">メルマガ</a>
    </nav>
  </div>
</header>

<section class="page-banner">
  <div class="page-banner-inner">
    <div class="page-banner-eyebrow">FULL ROADMAP</div>
    <h1 class="page-banner-title">全100話 ロードマップ</h1>
    <p class="page-banner-en">The Complete Map — From Everyday to Academia</p>
    <div class="page-stats">
      <span>EPISODES<strong>100</strong></span>
      <span>SCENES<strong>27</strong></span>
      <span>PARTS<strong>5+2</strong></span>
      <span>PUBLISHED<strong>{total_published}</strong></span>
    </div>
  </div>
</section>

<div class="series-progress">
  <div class="series-progress-bar-wrap"><div class="series-progress-bar-fill"></div></div>
  <div class="series-progress-meta"><span>連載進捗</span><strong>{total_published}/100話 ({progress_pct}%)</strong></div>
</div>

<section class="parts-jump">
  <div class="parts-jump-label">JUMP TO PART</div>
  <h2 class="parts-jump-title">5つの章から、暮らしと学問の交差点へ</h2>
  <div class="parts-jump-grid">
{parts_jump}
  </div>
</section>

<main class="content-main">
{chr(10).join(parts_html)}
</main>

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

<script>
const NEWSLETTER_API = 'https://claude-code-manual-app.vercel.app/api/community';
function nlNext() {{
  const v = document.getElementById('nlEmail').value.trim();
  if (!v || !v.includes('@')) {{
    document.getElementById('nlEmail').style.borderColor = 'var(--accent)';
    document.getElementById('nlEmail').focus();
    setTimeout(() => document.getElementById('nlEmail').style.borderColor = '', 2000);
    return;
  }}
  document.getElementById('nlStep1').classList.remove('active');
  document.getElementById('nlStep2').classList.add('active');
  document.getElementById('nlName').focus();
}}
async function submitNl() {{
  const name = document.getElementById('nlName').value.trim();
  const org = document.getElementById('nlOrg').value.trim();
  const email = document.getElementById('nlEmail').value.trim();
  const consent = document.getElementById('nlConsent').checked;
  const btn = document.getElementById('nlBtn');
  if (!name) {{ document.getElementById('nlName').focus(); return; }}
  if (!consent) {{ alert('メールマガジン配信への同意が必要です'); return; }}
  btn.disabled = true;
  btn.textContent = '登録中…';
  try {{
    const res = await fetch(NEWSLETTER_API, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ name, org, email, source: 'kurashi-no-katachi/articles' }}),
    }});
    if (!res.ok) throw new Error('failed');
    document.getElementById('nlForm').classList.add('hide');
    document.getElementById('nlDone').classList.add('show');
  }} catch (e) {{
    alert('登録に失敗しました。少し時間をおいて再度お試しください。');
    btn.disabled = false;
    btn.textContent = '登録する';
  }}
}}
</script>

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

</body>
</html>
'''


# ============================================================================
# index.html (home page)
# ============================================================================

def build_index_html() -> str:
    total_published = sum(1 for r in ROADMAP if r[6] == 'published')
    # Pick first published episode as featured
    first_published = next((r for r in ROADMAP if r[6] == 'published'), None)
    featured_html = ''
    if first_published:
        ep_num, eyebrow, title_main, title_sub, scene, domain, status = first_published
        featured_html = f'''
    <section class="featured">
      <div class="featured-inner">
        <div class="featured-label">LATEST EPISODE — 最新話</div>
        <a class="featured-card" href="ep{ep_num}.html">
          <div class="featured-num">{ep_num}<span class="featured-num-total">/100</span></div>
          <div class="featured-eyebrow">{eyebrow}</div>
          <h2 class="featured-title">{title_main}</h2>
          <p class="featured-sub">― {title_sub}</p>
          <span class="featured-cta">この話を読む →</span>
        </a>
      </div>
    </section>'''

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>暮らしのかたち ― 学術が日々の暮らしに出会うとき</title>
<meta name="description" content="学術領域の歴史と最先端を、毎日の食卓・関係・身体・場へと翻訳する全100回連載。NPO法人ミラツク。">
<meta property="og:title" content="暮らしのかたち ― 学術が日々の暮らしに出会うとき">
<meta property="og:description" content="学術が日々の暮らしに出会うとき。全100回連載。">
<meta property="og:type" content="website">
<link rel="canonical" href="https://yuyanishimura0312.github.io/kurashi-no-katachi/">
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@300;400;500;600;700;900&family=Judson:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<style>
.hero {{ padding: 120px 24px 80px; background: var(--bg); border-bottom: 1px solid var(--line); }}
.hero-inner {{ max-width: 980px; margin: 0 auto; }}
.hero-eyebrow {{ font-family: var(--sans); font-size: 11.5px; letter-spacing: 0.36em; color: var(--accent); font-weight: 700; display: flex; align-items: center; gap: 14px; margin-bottom: 32px; }}
.hero-eyebrow::before {{ content: ""; width: 40px; height: 2px; background: var(--accent); }}
.hero-title {{ font-family: var(--serif); font-weight: 700; font-size: 56px; line-height: 1.4; letter-spacing: 0.02em; color: var(--ink); margin-bottom: 24px; }}
.hero-en {{ font-family: var(--display); font-size: 24px; color: var(--ink-mute); letter-spacing: 0.02em; margin-bottom: 32px; }}
.hero-tagline {{ font-family: var(--serif); font-size: 17px; line-height: 2; color: var(--ink-soft); max-width: 640px; padding-left: 22px; border-left: 3px solid var(--accent); margin-bottom: 40px; }}
.hero-cta {{ display: flex; gap: 14px; flex-wrap: wrap; }}
.hero-cta a {{ display: inline-flex; align-items: center; padding: 14px 28px; font-family: var(--sans); font-size: 12px; font-weight: 700; letter-spacing: 0.16em; text-decoration: none; transition: background .15s; }}
.hero-cta .primary {{ background: var(--accent); color: var(--bg); }}
.hero-cta .primary:hover {{ background: var(--accent-deep); text-decoration: none; }}
.hero-cta .secondary {{ background: transparent; color: var(--ink); border: 1px solid var(--ink); }}
.hero-cta .secondary:hover {{ background: var(--ink); color: var(--bg); text-decoration: none; }}

.intro {{ padding: 80px 24px; background: var(--bg-soft); border-bottom: 1px solid var(--line); }}
.intro-inner {{ max-width: 720px; margin: 0 auto; }}
.intro p {{ font-family: var(--serif); font-size: 16px; line-height: 2.1; color: var(--ink-soft); margin-bottom: 24px; }}
.intro p strong {{ color: var(--ink); font-weight: 600; }}

.featured {{ padding: 80px 24px; background: var(--bg); border-bottom: 1px solid var(--line); }}
.featured-inner {{ max-width: 720px; margin: 0 auto; }}
.featured-label {{ font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: 0.32em; color: var(--accent); margin-bottom: 24px; }}
.featured-card {{ display: block; padding: 40px 36px; background: var(--bg-tint); border: 1px solid var(--line); text-decoration: none; transition: border-color .15s, transform .15s; }}
.featured-card:hover {{ border-color: var(--accent); transform: translateY(-2px); text-decoration: none; }}
.featured-num {{ font-family: var(--display); font-weight: 700; font-size: 56px; color: var(--ink); line-height: 1; margin-bottom: 16px; }}
.featured-num-total {{ font-family: var(--sans); font-size: 14px; color: var(--ink-mute); margin-left: 4px; letter-spacing: 0.08em; }}
.featured-eyebrow {{ font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 0.22em; color: var(--accent); margin-bottom: 14px; }}
.featured-title {{ font-family: var(--serif); font-weight: 700; font-size: 26px; line-height: 1.55; color: var(--ink); margin-bottom: 12px; }}
.featured-sub {{ font-family: var(--serif); font-size: 15px; color: var(--ink-soft); line-height: 1.85; margin-bottom: 24px; }}
.featured-cta {{ font-family: var(--sans); font-size: 11.5px; font-weight: 700; letter-spacing: 0.16em; color: var(--accent); }}

.parts-overview {{ padding: 80px 24px; background: var(--bg); }}
.parts-overview-inner {{ max-width: 1080px; margin: 0 auto; }}
.parts-overview-label {{ font-family: var(--sans); font-size: 11px; font-weight: 700; letter-spacing: 0.32em; color: var(--accent); margin-bottom: 14px; }}
.parts-overview-title {{ font-family: var(--serif); font-weight: 700; font-size: 32px; color: var(--ink); margin-bottom: 40px; }}
.parts-overview-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; }}
.parts-overview-card {{ padding: 28px 24px; background: var(--bg-soft); border: 1px solid var(--line); text-decoration: none; transition: border-color .15s, transform .15s; }}
.parts-overview-card:hover {{ border-color: var(--accent); transform: translateY(-2px); text-decoration: none; }}
.parts-overview-card-num {{ font-family: var(--display); font-weight: 700; font-size: 22px; color: var(--accent); margin-bottom: 8px; }}
.parts-overview-card-title {{ font-family: var(--serif); font-weight: 700; font-size: 17px; color: var(--ink); line-height: 1.55; margin-bottom: 8px; }}
.parts-overview-card-sub {{ font-family: var(--sans); font-size: 11px; color: var(--ink-mute); line-height: 1.7; }}

@media (max-width: 760px) {{
  .hero-title {{ font-size: 32px; }}
  .hero-en {{ font-size: 18px; }}
  .featured-title {{ font-size: 20px; }}
  .featured-num {{ font-size: 40px; }}
}}
</style>
</head>
<body>

<header class="site-header">
  <div class="site-header-inner">
    <a href="index.html" class="site-brand">
      <div class="site-brand-mark"><img src="assets/miratuku-mark.png" alt="ミラツク"></div>
      <div class="site-brand-text">暮らしのかたち<small>KURASHI NO KATACHI / 学術が日々の暮らしに出会うとき</small></div>
    </a>
    <nav class="site-nav">
      <a href="index.html" class="active">ホーム</a>
      <a href="articles.html">全100話</a>
      <a href="#newsletter">メルマガ</a>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="hero-inner">
    <div class="hero-eyebrow">A SERIES OF ONE HUNDRED — 全100話連載</div>
    <h1 class="hero-title">暮らしのかたち</h1>
    <p class="hero-en">Forms of Life — Where Academia Meets Everyday Life</p>
    <p class="hero-tagline">学術領域の歴史と最先端を、毎日の食卓・関係・身体・場へと翻訳する全100回連載。気分の浮き沈みから建築の高さまで、4,000の研究領域を27の暮らしのシーンから読み解いていきます。</p>
    <div class="hero-cta">
      <a class="primary" href="ep001.html">第1話から読む →</a>
      <a class="secondary" href="articles.html">全100話の地図を見る</a>
    </div>
  </div>
</section>

<section class="intro">
  <div class="intro-inner">
    <p>日々生み出される研究成果は、そのままでは私たちの暮らしとどう繋がるのかが見えにくく、専門誌のなかで眠ったままになっています。<strong>暮らしのかたち</strong>は、その溝に小さな橋を架けていく試みです。</p>
    <p>NPO法人ミラツクが2021年に作成した<strong>「暮らしのシーンカード」全27シーン</strong>――食事、住宅、睡眠、家事、はたらく、教育、旅、祭り、恋愛、結婚、育児、医療、看護、芸術、メディア、農業、漁業など――を出発点に、関連する学問の系譜と最新研究を重ね、毎日の暮らしを別の角度から見直すための100話を編んでいきます。</p>
    <p>各記事は、<strong>暮らしの場面から始まり</strong>、研究者たちの系譜、最先端の発見、そして自分の毎日へと戻ってくる4部構成。Translational Editor の視点から、学問のドアを暮らしから開けていきます。</p>
  </div>
</section>

{featured_html}

<section class="parts-overview">
  <div class="parts-overview-inner">
    <div class="parts-overview-label">FIVE PARTS — 5つの章</div>
    <h2 class="parts-overview-title">暮らしを編む5つの大きな問い</h2>
    <div class="parts-overview-grid">
      <a class="parts-overview-card" href="articles.html#part-i"><div class="parts-overview-card-num">PART I</div><div class="parts-overview-card-title">衣食住 ― 身体を包む環境</div><div class="parts-overview-card-sub">食事・住宅・ファッション</div></a>
      <a class="parts-overview-card" href="articles.html#part-ii"><div class="parts-overview-card-num">PART II</div><div class="parts-overview-card-title">暮らしの基盤 ― 一日を成り立たせるもの</div><div class="parts-overview-card-sub">睡眠・家事・はたらく・教育</div></a>
      <a class="parts-overview-card" href="articles.html#part-iii"><div class="parts-overview-card-num">PART III</div><div class="parts-overview-card-title">関係 ― 人と人のあいだ</div><div class="parts-overview-card-sub">恋愛・結婚・育児・ペット</div></a>
      <a class="parts-overview-card" href="articles.html#part-iv"><div class="parts-overview-card-num">PART IV</div><div class="parts-overview-card-title">ケアと遊 ― 身体・健康・余白</div><div class="parts-overview-card-sub">医療・看護介護・スポーツ観戦・旅・祭り</div></a>
      <a class="parts-overview-card" href="articles.html#part-v"><div class="parts-overview-card-num">PART V</div><div class="parts-overview-card-title">文化と公共 ― 共有されるもの</div><div class="parts-overview-card-sub">芸術・メディア・図書館・公園・産業</div></a>
    </div>
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

<script>
const NEWSLETTER_API = 'https://claude-code-manual-app.vercel.app/api/community';

function nlNext() {{
  const v = document.getElementById('nlEmail').value.trim();
  if (!v || !v.includes('@')) {{
    document.getElementById('nlEmail').style.borderColor = 'var(--accent)';
    document.getElementById('nlEmail').focus();
    setTimeout(() => document.getElementById('nlEmail').style.borderColor = '', 2000);
    return;
  }}
  document.getElementById('nlStep1').classList.remove('active');
  document.getElementById('nlStep2').classList.add('active');
  document.getElementById('nlName').focus();
}}
async function submitNl() {{
  const name = document.getElementById('nlName').value.trim();
  const org = document.getElementById('nlOrg').value.trim();
  const email = document.getElementById('nlEmail').value.trim();
  const consent = document.getElementById('nlConsent').checked;
  const btn = document.getElementById('nlBtn');
  if (!name) {{ document.getElementById('nlName').focus(); return; }}
  if (!consent) {{ alert('メールマガジン配信への同意が必要です'); return; }}
  btn.disabled = true;
  btn.textContent = '登録中…';
  try {{
    const res = await fetch(NEWSLETTER_API, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ name, org, email, source: 'kurashi-no-katachi/index' }}),
    }});
    if (!res.ok) throw new Error('failed');
    document.getElementById('nlForm').classList.add('hide');
    document.getElementById('nlDone').classList.add('show');
  }} catch (e) {{
    alert('登録に失敗しました。少し時間をおいて再度お試しください。');
    btn.disabled = false;
    btn.textContent = '登録する';
  }}
}}
</script>

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

</body>
</html>
'''


# ============================================================================
# Stub HTML for unpublished episodes
# ============================================================================

def build_stub_html(ep_num: str, eyebrow: str, title_main: str, title_sub: str, scene: str, domain: str) -> str:
    part_key = get_part_for_ep(ep_num)
    part = PARTS[part_key]

    # Determine adjacent episodes
    all_eps = [r[0] for r in ROADMAP]
    idx = all_eps.index(ep_num)
    prev_ep = all_eps[idx - 1] if idx > 0 else None
    next_ep = all_eps[idx + 1] if idx < len(all_eps) - 1 else None

    prev_link = f'ep{prev_ep}.html' if prev_ep else '#'
    next_link = f'ep{next_ep}.html' if next_ep else '#'

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第{int(ep_num)}話 ― {title_main} | 暮らしのかたち</title>
<meta name="description" content="暮らしのかたち第{int(ep_num)}話。{title_sub}（執筆中）">
<meta property="og:title" content="第{int(ep_num)}話 ― {title_main}">
<meta property="og:type" content="article">
<link rel="canonical" href="https://yuyanishimura0312.github.io/kurashi-no-katachi/ep{ep_num}.html">
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@300;400;500;600;700;900&family=Judson:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<style>
.stub-notice {{ max-width: 720px; margin: 80px auto; padding: 56px 40px; background: var(--bg-tint); border: 1px solid var(--line); border-left: 4px solid var(--accent); }}
.stub-eyebrow {{ font-family: var(--sans); font-size: 10.5px; font-weight: 700; letter-spacing: 0.26em; color: var(--accent); margin-bottom: 18px; }}
.stub-num {{ font-family: var(--display); font-weight: 700; font-size: 64px; color: var(--ink); line-height: 1; margin-bottom: 18px; }}
.stub-num-total {{ font-family: var(--sans); font-size: 16px; color: var(--ink-mute); margin-left: 4px; }}
.stub-title {{ font-family: var(--serif); font-weight: 700; font-size: 28px; line-height: 1.5; color: var(--ink); margin-bottom: 14px; }}
.stub-sub {{ font-family: var(--serif); font-size: 16px; color: var(--ink-soft); line-height: 1.85; margin-bottom: 28px; }}
.stub-meta {{ font-family: var(--sans); font-size: 11.5px; color: var(--ink-mute); letter-spacing: 0.1em; padding-top: 22px; border-top: 1px solid var(--line); margin-bottom: 28px; }}
.stub-message {{ font-family: var(--serif); font-size: 14.5px; color: var(--ink-soft); line-height: 2; padding-top: 22px; border-top: 1px solid var(--line); }}
.stub-cta {{ margin-top: 32px; display: flex; gap: 14px; flex-wrap: wrap; }}
.stub-cta a {{ display: inline-flex; padding: 12px 22px; font-family: var(--sans); font-size: 11.5px; font-weight: 700; letter-spacing: 0.16em; text-decoration: none; }}
.stub-cta .primary {{ background: var(--accent); color: var(--bg); }}
.stub-cta .secondary {{ background: transparent; color: var(--ink); border: 1px solid var(--ink); }}
</style>
</head>
<body>

<header class="site-header">
  <div class="site-header-inner">
    <a href="index.html" class="site-brand">
      <div class="site-brand-mark"><img src="assets/miratuku-mark.png" alt="ミラツク"></div>
      <div class="site-brand-text">暮らしのかたち<small>KURASHI NO KATACHI / 学術が日々の暮らしに出会うとき</small></div>
    </a>
    <nav class="site-nav">
      <a href="index.html">ホーム</a>
      <a href="articles.html">全100話</a>
      <a href="index.html#newsletter">メルマガ</a>
    </nav>
  </div>
</header>

<div class="stub-notice">
  <div class="stub-eyebrow">{eyebrow}</div>
  <div class="stub-num">{ep_num}<span class="stub-num-total">/100</span></div>
  <h1 class="stub-title">{title_main}</h1>
  <p class="stub-sub">― {title_sub}</p>
  <div class="stub-meta">学術領域: {domain} ／ 暮らしのシーン: {scene}</div>
  <div class="stub-message">
    本記事は<strong>執筆中</strong>です。連載「暮らしのかたち」は全100話で構成され、現在公開中の話と公開予定の話があります。新しい話の公開通知はメールマガジンでお届けしています。
  </div>
  <div class="stub-cta">
    <a class="primary" href="index.html#newsletter">公開通知を受け取る</a>
    <a class="secondary" href="articles.html">全100話の地図を見る</a>
  </div>
</div>

<nav class="ep-nav">
  <div class="ep-nav-inner">
    <a class="ep-nav-link{' disabled' if not prev_ep else ''}" href="{prev_link}">
      <span class="ep-nav-label">← PREV</span>
      <span class="ep-nav-title">第{int(prev_ep) if prev_ep else 1}話</span>
    </a>
    <a class="ep-nav-link next{' disabled' if not next_ep else ''}" href="{next_link}">
      <span class="ep-nav-label">NEXT →</span>
      <span class="ep-nav-title">第{int(next_ep) if next_ep else 100}話</span>
    </a>
  </div>
</nav>

<footer class="site-footer">
  <div class="site-footer-inner">
    <div class="site-footer-cols">
      <div class="site-footer-col">
        <h4>ABOUT</h4>
        <p><strong>暮らしのかたち ― 学術が日々の暮らしに出会うとき</strong></p>
      </div>
      <div class="site-footer-col">
        <h4>NAVIGATION</h4>
        <ul><li><a href="index.html">ホーム</a></li><li><a href="articles.html">全100話 一覧</a></li></ul>
      </div>
      <div class="site-footer-col">
        <h4>MIRA TUKU</h4>
        <ul><li><a href="https://emerging-future.org/" target="_blank" rel="noopener">emerging-future.org</a></li></ul>
      </div>
    </div>
    <div class="site-footer-bottom">
      <span>© 2026 NPO法人ミラツク</span>
      <span>暮らしのかたち ― 学術が日々の暮らしに出会うとき</span>
    </div>
  </div>
</footer>

</body>
</html>
'''


if __name__ == '__main__':
    print('Building site...')

    # Write articles.html
    (ROOT / 'articles.html').write_text(build_articles_html(), encoding='utf-8')
    print('  articles.html')

    # Write index.html
    (ROOT / 'index.html').write_text(build_index_html(), encoding='utf-8')
    print('  index.html')

    # Write stub HTML for all unpublished episodes
    stub_count = 0
    for r in ROADMAP:
        ep_num, eyebrow, title_main, title_sub, scene, domain, status = r
        if status == 'planned':
            (ROOT / f'ep{ep_num}.html').write_text(
                build_stub_html(ep_num, eyebrow, title_main, title_sub, scene, domain),
                encoding='utf-8'
            )
            stub_count += 1
    print(f'  {stub_count} stub episodes (ep002-ep100 minus 9 published)')

    print('Done.')
