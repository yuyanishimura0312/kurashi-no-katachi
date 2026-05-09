
const FEEDBACK_API = 'https://claude-code-manual-app.vercel.app/api/feedback';
const NEWSLETTER_API = 'https://claude-code-manual-app.vercel.app/api/community';
const EPISODE_ID = 'ep006';
const EPISODE_TITLE = '第6話 ― 気分を決めているのは、おなかかもしれない';

(function() {
  const article = document.getElementById('articleBody');
  const bar = document.getElementById('readProgressBar');
  const readTimeEl = document.getElementById('readTime');

  if (article && readTimeEl) {
    const text = article.innerText || article.textContent || '';
    const charCount = text.replace(/\s/g, '').length;
    const minutes = Math.max(1, Math.round(charCount / 280));
    readTimeEl.textContent = '推定読了 約' + minutes + '分';
  }

  if (article && bar) {
    function updateProgress() {
      const rect = article.getBoundingClientRect();
      const total = article.offsetHeight - window.innerHeight;
      const scrolled = -rect.top;
      const pct = total > 0 ? Math.max(0, Math.min(100, (scrolled / total) * 100)) : 0;
      bar.style.width = pct + '%';
    }
    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress, { passive: true });
    updateProgress();
  }
})();

function toggleTocDrawer() {
  const d = document.getElementById('tocDrawer');
  if (!d) return;
  const willOpen = !d.classList.contains('show');
  d.classList.toggle('show');
  document.body.style.overflow = willOpen ? 'hidden' : '';
  document.getElementById('tocOverlay')?.classList.toggle('show', willOpen);
  if (willOpen) {
    d.querySelector('.toc-drawer-close')?.focus();
    document.addEventListener('keydown', _tocEsc);
  } else {
    document.removeEventListener('keydown', _tocEsc);
    document.getElementById('tocFab')?.focus();
  }
}
function _tocEsc(e) { if (e.key === 'Escape') toggleTocDrawer(); }

async function submitFeedback() {
  const suggestion = document.getElementById('fbSuggestion').value.trim();
  const name = document.getElementById('fbName').value.trim();
  const email = document.getElementById('fbEmail').value.trim();
  const btn = document.getElementById('fbSubmit');
  if (!suggestion) {
    document.getElementById('fbSuggestion').focus();
    document.getElementById('fbSuggestion').style.borderColor = 'var(--accent)';
    return;
  }
  btn.disabled = true;
  btn.textContent = '送信中…';
  try {
    const res = await fetch(FEEDBACK_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        source: 'kurashi-no-katachi',
        episode: EPISODE_ID + ' ' + EPISODE_TITLE,
        suggestion, name, email,
      }),
    });
    if (!res.ok) throw new Error('failed');
    document.getElementById('fbForm').classList.add('hide');
    document.getElementById('fbDone').classList.add('show');
  } catch (e) {
    alert('送信に失敗しました。少し時間をおいて再度お試しください。');
    btn.disabled = false;
    btn.textContent = '送信する';
  }
}

function nlNext() {
  const v = document.getElementById('nlEmail').value.trim();
  if (!v || !v.includes('@')) {
    document.getElementById('nlEmail').style.borderColor = 'var(--accent)';
    document.getElementById('nlEmail').focus();
    setTimeout(() => document.getElementById('nlEmail').style.borderColor = '', 2000);
    return;
  }
  document.getElementById('nlStep1').classList.remove('active');
  document.getElementById('nlStep2').classList.add('active');
  document.getElementById('nlName').focus();
}
async function submitNl() {
  const name = document.getElementById('nlName').value.trim();
  const org = document.getElementById('nlOrg').value.trim();
  const email = document.getElementById('nlEmail').value.trim();
  const consent = document.getElementById('nlConsent').checked;
  const btn = document.getElementById('nlBtn');
  if (!name) { document.getElementById('nlName').focus(); return; }
  if (!consent) { alert('メールマガジン配信への同意が必要です'); return; }
  btn.disabled = true;
  btn.textContent = '登録中…';
  try {
    const res = await fetch(NEWSLETTER_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, org, email }),
    });
    if (!res.ok) throw new Error('failed');
    document.getElementById('nlForm').classList.add('hide');
    document.getElementById('nlDone').classList.add('show');
  } catch (e) {
    alert('登録に失敗しました。少し時間をおいて再度お試しください。');
    btn.disabled = false;
    btn.textContent = '登録する';
  }
}
