// Content Script for Gmail Spam Detector AI

// References to observer and interval to clean them up if extension is reloaded
let domObserver = null;
let fallbackInterval = null;

// Helper to check if the extension context is still valid (not reloaded/invalidated)
function isContextValid() {
  if (typeof chrome === 'undefined' || !chrome.runtime || !chrome.runtime.id) {
    cleanupOrphanScript();
    return false;
  }
  return true;
}

// Function to clean up observers and intervals when the extension is reloaded/disabled
function cleanupOrphanScript() {
  console.log("Gmail Spam Detector AI: Extension context invalidated. Cleaning up listeners.");
  if (domObserver) {
    try {
      domObserver.disconnect();
    } catch (e) {
      // Ignore
    }
    domObserver = null;
  }
  if (fallbackInterval) {
    try {
      clearInterval(fallbackInterval);
    } catch (e) {
      // Ignore
    }
    fallbackInterval = null;
  }
}

// Helper to find all email message bodies using multiple fallback selectors
function getEmailBodies() {
  const selectors = [
    'div.a3s',                 // Primary Gmail selector
    'div[class*="aiL"]',       // Gmail dynamic layout wrapper
    '.ii.gt',                  // Gmail mail text container
    'div[class*="ii gt"]',     // Gmail layout variant
    'div.adn div[dir="ltr"]'   // Sibling check wrapper
  ];

  let foundElements = [];
  selectors.forEach(selector => {
    try {
      const elements = document.querySelectorAll(selector);
      elements.forEach(el => {
        if (el && !foundElements.includes(el)) {
          foundElements.push(el);
        }
      });
    } catch (e) {
      console.warn("Invalid selector: " + selector, e);
    }
  });

  // Filter out container elements that wrap other found body elements.
  // E.g. If both '.ii.gt' and 'div.a3s' are matched, 'div.a3s' is a child of '.ii.gt'.
  // We want to keep the inner-most child (div.a3s) for inserting the button directly.
  return foundElements.filter(el => {
    // If 'el' contains any other element in 'foundElements', it is a parent wrapper, so filter it out.
    const isParentWrapper = foundElements.some(other => other !== el && el.contains(other));
    return !isParentWrapper;
  });
}

// Helper to find email subject line using fallback selectors
function getEmailSubject() {
  const selectors = [
    'h2.hP',              // Gmail header subject class
    '.ha h2',             // Gmail alternative subject container
    'div[role="main"] h1', // General modern webmail heading
    'div[role="main"] h2'  // General webmail h2
  ];

  for (const selector of selectors) {
    try {
      const el = document.querySelector(selector);
      if (el && el.innerText.trim()) {
        return el.innerText.trim();
      }
    } catch (e) {
      console.warn("Failed selector: " + selector, e);
    }
  }
  return "";
}

// Function to inject "Check Spam" buttons into Gmail email bodies
function injectSpamCheckButtons() {
  if (!isContextValid()) {
    return;
  }

  const emailBodies = getEmailBodies();

  emailBodies.forEach(body => {
    // Prevent double injection: Check if attribute is set on body element itself
    if (body.getAttribute('data-spam-check-injected') === 'true') {
      return;
    }

    // Check if the previous element is already our spam checker bar (for double safety)
    if (body.previousElementSibling && body.previousElementSibling.classList.contains('spam-checker-container')) {
      // Mark it to prevent repeating DOM query
      body.setAttribute('data-spam-check-injected', 'true');
      return;
    }

    const parent = body.parentElement;
    if (!parent) return;

    // Check if the parent container already has a spam checker (dynamic updates check)
    if (parent.querySelector('.spam-checker-container')) {
      body.setAttribute('data-spam-check-injected', 'true');
      return;
    }

    // Create the container for the button and badge
    const container = document.createElement('div');
    container.className = 'spam-checker-container';

    // Create the button
    const button = document.createElement('button');
    button.className = 'spam-check-btn';
    button.innerHTML = '<span class="spam-btn-icon">🤖</span> <span class="spam-btn-text">Check Spam</span>';
    
    // Add event listener to trigger prediction
    button.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      performSpamCheck(body, button);
    });

    container.appendChild(button);

    // Insert container right before body
    parent.insertBefore(container, body);
    
    // Mark as injected
    body.setAttribute('data-spam-check-injected', 'true');
  });
}

// Function to handle the actual spam checking process
function performSpamCheck(bodyElement, buttonElement) {
  if (!isContextValid()) {
    alert("Extension đã được cập nhật hoặc tải lại. Vui lòng F5 (tải lại trang) Gmail để tiếp tục sử dụng.");
    return;
  }

  // 1. Get the email content
  const emailText = bodyElement.innerText || bodyElement.textContent || "";
  
  // 2. Get the email subject with fallbacks
  const subjectText = getEmailSubject();

  if (!emailText.trim()) {
    showOverlay({
      success: false,
      error: "Không thể trích xuất nội dung từ email này. Thư có thể trống hoặc chỉ chứa hình ảnh."
    });
    return;
  }

  // 3. Set button loading state
  buttonElement.disabled = true;
  buttonElement.classList.add('loading');
  const buttonTextSpan = buttonElement.querySelector('.spam-btn-text');
  const originalBtnText = buttonTextSpan.innerText;
  buttonTextSpan.innerText = "Đang phân tích...";

  // 4. Send message to background.js (service worker)
  chrome.runtime.sendMessage({
    action: "predictSpam",
    text: emailText,
    subject: subjectText
  }, (response) => {
    // Check context again inside async callback
    if (!isContextValid()) {
      return;
    }

    // Restore button state
    buttonElement.disabled = false;
    buttonElement.classList.remove('loading');
    buttonTextSpan.innerText = originalBtnText;

    // Handle runtime errors (e.g. service worker inactive or disconnected)
    if (chrome.runtime.lastError) {
      console.error("Chrome Runtime Error:", chrome.runtime.lastError);
      showOverlay({
        success: false,
        error: `Lỗi kết nối extension: ${chrome.runtime.lastError.message}. Hãy thử tải lại trang Gmail.`
      });
      return;
    }

    // 5. Handle Flask API response
    if (response && response.success) {
      // Show details in overlay popup
      showOverlay({
        success: true,
        data: response.data
      });
      
      // Update the inline badge next to the button
      updateInlineBadge(buttonElement.parentElement, response.data);
    } else {
      showOverlay({
        success: false,
        error: response ? response.error : "Không nhận được phản hồi từ background script."
      });
    }
  });
}

// Update the inline badge right next to the "Check Spam" button for instant visual history
function updateInlineBadge(container, data) {
  if (!isContextValid()) return;

  // Remove existing badge if any
  const existingBadge = container.querySelector('.spam-inline-badge');
  if (existingBadge) {
    existingBadge.remove();
  }

  const badge = document.createElement('span');
  
  // Decide class and text based on backend response
  const isSpam = data.is_spam;
  badge.className = `spam-inline-badge ${isSpam ? 'is-spam' : 'is-ham'}`;
  
  const icon = isSpam ? '⚠️' : '✅';
  const label = isSpam ? 'Spam' : 'Không Spam';
  const confidence = data.confidence !== undefined ? data.confidence : 0;
  
  badge.innerHTML = `${icon} ${label} (${confidence}%)`;
  container.appendChild(badge);
}

// Display the beautiful glassmorphism popup card overlay
function showOverlay(result) {
  if (!isContextValid()) return;

  // Remove existing overlay first
  const existingOverlay = document.getElementById('spam-detector-overlay');
  if (existingOverlay) {
    existingOverlay.remove();
  }

  // Create new overlay container
  const overlay = document.createElement('div');
  overlay.id = 'spam-detector-overlay';
  overlay.className = 'spam-overlay-card';

  let htmlContent = '';

  if (!result.success) {
    // Render connection error UI
    htmlContent = `
      <div class="spam-card-header">
        <span class="spam-card-title">⚠️ Lỗi kết nối API</span>
        <button class="spam-card-close" id="spam-close-overlay">&times;</button>
      </div>
      <div class="spam-card-body error-body">
        <p>${result.error}</p>
        <div class="spam-error-tips">
          <strong>Hướng dẫn khắc phục:</strong>
          <ul>
            <li>Chạy backend Flask: <code>python app.py</code></li>
            <li>Kiểm tra xem API tại <code>http://localhost:5000/predict</code> có phản hồi không.</li>
          </ul>
        </div>
      </div>
    `;
  } else {
    // Render prediction result UI
    const data = result.data;
    const isSpam = data.is_spam;
    const confidence = data.confidence !== undefined ? data.confidence : 0;
    const keywords = data.model_keywords || data.highlight_terms || [];
    const modelName = data.model || "Mô hình AI Phân Loại";
    
    // UI details depending on spam vs ham
    const bannerClass = isSpam ? 'verdict-spam' : 'verdict-ham';
    const bannerIcon = isSpam ? '🚨' : '🛡️';
    const bannerTitle = isSpam ? 'Cảnh báo: EMAIL SPAM!' : 'EMAIL AN TOÀN';
    const bannerDesc = isSpam 
      ? `Email này chứa nhiều dấu hiệu của thư rác.` 
      : `Email này an toàn để đọc tiếp.`;

    // Render list of suspicious keywords if available
    let keywordsHTML = '';
    if (keywords && keywords.length > 0) {
      keywordsHTML = `
        <div class="spam-section-title">Từ khóa đáng ngờ được phát hiện:</div>
        <div class="spam-keywords-list">
          ${keywords.map(kw => `<span class="spam-keyword-tag">${escapeHtml(kw)}</span>`).join('')}
        </div>
      `;
    }

    htmlContent = `
      <div class="spam-card-header">
        <span class="spam-card-title">🤖 AI Spam Detector</span>
        <button class="spam-card-close" id="spam-close-overlay">&times;</button>
      </div>
      <div class="spam-card-body">
        <div class="spam-verdict-banner ${bannerClass}">
          <span class="verdict-icon">${bannerIcon}</span>
          <div class="verdict-text-group">
            <div class="verdict-status">${bannerTitle}</div>
            <div class="verdict-sub">${bannerDesc}</div>
          </div>
        </div>

        <div class="spam-metric-section">
          <div class="spam-metric-label">
            <span>Độ tin cậy của AI</span>
            <span>${confidence}%</span>
          </div>
          <div class="spam-progress-bg">
            <div class="spam-progress-bar ${isSpam ? 'bar-spam' : 'bar-ham'}" style="width: ${confidence}%"></div>
          </div>
        </div>

        ${keywordsHTML}

        <div class="spam-footer-info">
          <span>Công nghệ: ${escapeHtml(modelName)}</span>
        </div>
      </div>
    `;
  }

  overlay.innerHTML = htmlContent;
  document.body.appendChild(overlay);

  // Trigger animation next tick
  requestAnimationFrame(() => {
    overlay.classList.add('active');
  });

  // Attach close button click handler
  const closeBtn = overlay.querySelector('#spam-close-overlay');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      overlay.classList.remove('active');
      overlay.classList.add('closing');
      setTimeout(() => {
        overlay.remove();
      }, 300);
    });
  }
}

// Utility to escape HTML to prevent XSS from email content injection
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// --- Dynamic Injection Handling in Gmail's SPA interface ---

// Run once immediately on load
if (isContextValid()) {
  injectSpamCheckButtons();

  // Setup MutationObserver to watch for newly rendered email bodies in Gmail
  domObserver = new MutationObserver((mutations) => {
    injectSpamCheckButtons();
  });

  domObserver.observe(document.body, {
    childList: true,
    subtree: true
  });

  // Fallback interval to ensure robustness (e.g. back/forward navigation or panel switching in Gmail)
  fallbackInterval = setInterval(injectSpamCheckButtons, 1500);
}

console.log("Gmail Spam Detector AI extension script successfully loaded.");
