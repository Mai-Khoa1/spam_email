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

function highlightKeywords(text, keywords) {
  if (!keywords || keywords.length === 0) return escapeHtml(text);
  let result = escapeHtml(text);
  const uniqueKeywords = [...new Set(keywords.map(k => String(k).trim()).filter(k => k.length > 1))]
    .sort((a, b) => b.length - a.length);

  uniqueKeywords.forEach(kw => {
    const escapedKeyword = escapeHtml(kw).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp('(^|[^\\p{L}\\p{N}_])(' + escapedKeyword + ')(?=$|[^\\p{L}\\p{N}_])', 'giu');
    result = result.replace(regex, '$1<mark class="spam-highlight">$2</mark>');
  });
  return result;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
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

  const btn = document.getElementById('analyzeBtn');
  const spinner = document.getElementById('spinner');
  const btnText = document.getElementById('btnText');
  const resultCard = document.getElementById('resultCard');
  const confidenceCard = document.getElementById('confidenceCard');
  const whyCard = document.getElementById('whyCard');
  const translateBadge = document.getElementById('translateBadge');
  const highlightBox = document.getElementById('highlightBox');

  btn.disabled = true;
  spinner.style.display = 'block';
  btnText.textContent = 'Đang phân tích...';
  resultCard.className = 'result-card loading';
  document.getElementById('resultIcon').textContent = '⏳';
  document.getElementById('resultVerdict').textContent = 'AI đang phân tích...';
  const slowNoticeTimer = setTimeout(() => {
    btnText.textContent = 'Đang dịch và tìm từ khóa...';
    document.getElementById('resultVerdict').textContent = 'Đang dịch và căn highlight...';
  }, 4500);
  confidenceCard.classList.remove('show');
  whyCard.classList.remove('show');
  if (translateBadge) translateBadge.style.display = 'none';
  if (highlightBox) highlightBox.style.display = 'none';

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

    if (translateBadge && data.translated) {
      translateBadge.style.display = 'inline-flex';
    }

    // Verdict
    resultCard.className = 'result-card ' + (isSpam ? 'spam' : 'safe');
    document.getElementById('resultIcon').textContent = isSpam ? '🚨' : '🛡️';
    document.getElementById('resultVerdict').textContent = isSpam ? 'Email Spam!' : 'Email An Toàn';

    // Confidence
    confidenceCard.classList.add('show');
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

    // Highlight keywords nếu là spam
    if (isSpam && highlightBox) {
      const alignedTerms = data.highlight_terms || [];
      const modelKeywords = data.model_keywords || [];
      const terms = data.translated ? alignedTerms : modelKeywords;

      if (terms.length > 0) {
        document.getElementById('highlightContent').innerHTML = highlightKeywords(text, terms);
        document.getElementById('keywordList').innerHTML = terms.map(k =>
          `<span class="kw-chip">🔴 ${k}</span>`
        ).join('');
        highlightBox.style.display = 'block';
      }
    }

    // Why
    whyCard.classList.add('show');
    document.getElementById('whyTitle').textContent = isSpam ? '⚠️ Tại sao bị đánh dấu spam?' : '✅ Tại sao email này an toàn?';
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
    clearTimeout(slowNoticeTimer);
    btn.disabled = false;
    spinner.style.display = 'none';
    btnText.textContent = '🔍 Phân Tích Ngay';
  }
}
