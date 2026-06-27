let history = [];

function updateCharCount() {
  const len = document.getElementById('text').value.length;
  document.getElementById('charCount').textContent = len.toLocaleString('vi-VN') + ' ký tự';
}

function handleDrag(e, over) {
  e.preventDefault();
  document.getElementById('dropZone').classList.toggle('dragover', over);
}

function handleDrop(e) {
  e.preventDefault();
  document.getElementById('dropZone').classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) readFile(file);
}

function handleFile(e) {
  const file = e.target.files[0];
  if (file) readFile(file);
}

function readFile(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    document.getElementById('text').value = e.target.result;
    updateCharCount();
  };
  reader.readAsText(file, 'UTF-8');
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function highlightKeywords(text, keywords) {
  if (!keywords || keywords.length === 0) return escapeHtml(text);
  let result = escapeHtml(text);
  const unique = [...new Set(keywords.map(k => String(k).trim()).filter(k => k.length > 1))]
    .sort((a, b) => b.length - a.length);
  unique.forEach(kw => {
    const esc = escapeHtml(kw).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp('(^|[^\\p{L}\\p{N}_])(' + esc + ')(?=$|[^\\p{L}\\p{N}_])', 'giu');
    result = result.replace(re, '$1<mark class="spam-highlight">$2</mark>');
  });
  return result;
}

function addHistory(text, isSpam) {
  const preview = text.substring(0, 55) + (text.length > 55 ? '...' : '');
  const now = new Date();
  const time = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
  history.unshift({ preview, isSpam, time });
  if (history.length > 10) history.pop();
  renderHistory();
}

function renderHistory() {
  const el = document.getElementById('historyList');
  if (!history.length) {
    el.innerHTML = '<div class="history-empty">Chưa có lịch sử kiểm tra</div>';
    return;
  }
  el.innerHTML = history.map(h => `
    <div class="history-item">
      <span class="h-badge ${h.isSpam ? 'spam' : 'safe'}">${h.isSpam ? 'SPAM' : 'AN TOÀN'}</span>
      <span class="h-text">${h.preview}</span>
      <span class="h-time">${h.time}</span>
    </div>
  `).join('');
}

function clearHistory() {
  history = [];
  renderHistory();
}

async function checkSpam() {
  const text = document.getElementById('text').value.trim();
  if (!text) { alert('Vui lòng nhập nội dung email cần kiểm tra.'); return; }

  const btn        = document.getElementById('analyzeBtn');
  const spinner    = document.getElementById('spinner');
  const btnText    = document.getElementById('btnText');
  const resultCard = document.getElementById('resultCard');
  const confCard   = document.getElementById('confidenceCard');
  const whyCard    = document.getElementById('whyCard');
  const hlBox      = document.getElementById('highlightBox');

  btn.disabled = true;
  spinner.style.display = 'block';
  btnText.textContent = 'Đang phân tích...';
  resultCard.className = 'result-card loading';
  document.getElementById('resultIcon').textContent = '⏳';
  document.getElementById('resultVerdict').textContent = 'AI đang phân tích...';
  confCard.classList.remove('show');
  whyCard.classList.remove('show');
  if (hlBox) hlBox.style.display = 'none';

  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        subject: document.getElementById('subject').value,
      })
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const isSpam = data.is_spam;
    const pct = Math.round((data.weighted_score || 0) * 100);

    // Verdict
    resultCard.className = 'result-card ' + (isSpam ? 'spam' : 'safe');
    document.getElementById('resultIcon').textContent = isSpam ? '🚨' : '🛡️';
    document.getElementById('resultVerdict').textContent = isSpam ? 'Email Spam!' : 'Email An Toàn';

    // Confidence
    confCard.classList.add('show');
    document.getElementById('confVal').textContent = pct + '%';
    document.getElementById('confVal').style.color = isSpam ? '#e11d48' : '#16a34a';
    document.getElementById('confDesc').textContent = isSpam ? 'Khả năng là spam' : 'Khả năng an toàn';
    document.getElementById('confFill').style.width = pct + '%';
    document.getElementById('confFill').style.background = isSpam
      ? 'linear-gradient(90deg,#f43f5e,#ec4899)'
      : 'linear-gradient(90deg,#22c55e,#16a34a)';

    // Votes
    const votes = data.votes || [];
    document.getElementById('votesGrid').innerHTML = votes.map(v => {
      const s = v.toLowerCase().includes('spam');
      return `<span class="vote-chip ${s ? 'spam-vote' : 'ham-vote'}">${s ? '🚨' : '✅'} ${v}</span>`;
    }).join('');

    // Highlight keywords
    whyCard.classList.add('show');
    if (isSpam && hlBox) {
      const keywords = data.model_keywords || [];
      if (keywords.length > 0) {
        document.getElementById('highlightTitle').textContent = '🔍 Từ khóa spam được phát hiện';
        document.getElementById('highlightContent').innerHTML = highlightKeywords(text, keywords);
        document.getElementById('keywordList').innerHTML = keywords.map(k =>
          `<span class="kw-chip">🔴 ${k}</span>`
        ).join('');
        hlBox.style.display = 'block';
      }
    }

    // Lý do
    document.getElementById('whyTitle').textContent = isSpam
      ? '⚠️ Tại sao bị đánh dấu spam?' : '✅ Tại sao email này an toàn?';
    const reasons = isSpam ? [
      'Chứa từ khóa đáng ngờ thường thấy trong spam',
      'Ngôn ngữ mang tính khẩn cấp hoặc cám dỗ bất thường',
      'Cấu trúc nội dung giống mẫu email spam phổ biến',
      pct > 80 ? 'Đa số mô hình AI đồng thuận là spam' : 'Một số mô hình AI phát hiện dấu hiệu spam',
    ] : [
      'Không chứa từ khóa spam phổ biến',
      'Nội dung tự nhiên, không có dấu hiệu lừa đảo',
      'Cấu trúc email bình thường, đáng tin cậy',
      'Các mô hình AI đánh giá là email hợp lệ',
    ];
    const dotClass = isSpam ? 'spam' : 'safe';
    document.getElementById('whyList').innerHTML = reasons.map(r =>
      `<div class="why-item"><div class="why-dot ${dotClass}"></div>${r}</div>`
    ).join('');

    addHistory(text, isSpam);

  } catch (err) {
    resultCard.className = 'result-card idle';
    document.getElementById('resultIcon').textContent = '❌';
    document.getElementById('resultVerdict').textContent = 'Lỗi kết nối, thử lại!';
  } finally {
    btn.disabled = false;
    spinner.style.display = 'none';
    btnText.textContent = '🔍 Phân Tích Ngay';
  }
}
