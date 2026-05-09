// ========================================
// PHISHGUARD ULTRA - UI HANDLER (COMPLETE)
// Auto-size chat messages + All features
// ========================================

// ------------------------------
// LOADER FUNCTIONS
// ------------------------------
function showLoader(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loader"></div>';
    }
}

function hideLoader(elementId) {
    // Loader will be replaced by actual content in displayResult
}

// ------------------------------
// TOAST NOTIFICATION
// ------------------------------
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-5 left-5 z-50 px-4 py-2 rounded-lg shadow-lg text-white text-sm transition-opacity duration-300 opacity-100`;
    
    switch(type) {
        case 'error':
            toast.classList.add('bg-red-600');
            break;
        case 'success':
            toast.classList.add('bg-green-600');
            break;
        case 'warning':
            toast.classList.add('bg-yellow-500');
            break;
        default:
            toast.classList.add('bg-blue-600');
    }
    
    toast.innerHTML = `<i class="fas ${getToastIcon(type)} mr-2"></i>${message}`;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function getToastIcon(type) {
    switch(type) {
        case 'error': return 'fa-exclamation-triangle';
        case 'success': return 'fa-check-circle';
        case 'warning': return 'fa-exclamation-circle';
        default: return 'fa-info-circle';
    }
}

// ------------------------------
// RESULT DISPLAY
// ------------------------------
function displayResult(containerId, data, scanType) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (data.error) {
        container.innerHTML = `
            <div class="result-card result-error" style="border-left-color: #ef4444; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border-radius: 12px; padding: 20px; margin-top: 16px;">
                <div class="flex items-center gap-3 mb-2">
                    <i class="fas fa-exclamation-triangle text-red-500 text-xl"></i>
                    <span class="font-bold text-red-700">ERROR</span>
                </div>
                <p class="text-sm text-red-600">${escapeHtml(data.message || 'Unknown error occurred')}</p>
                <div class="copy-btn mt-3" onclick="copyToClipboard('${escapeHtml(JSON.stringify(data))}')">
                    <i class="fas fa-copy"></i> Copy Error
                </div>
            </div>
        `;
        return;
    }
    
    let verdict = '';
    let score = data.score || 0;
    let confidence = data.confidence || 'LOW';
    let reasons = data.reasons || [];
    let status = data.status || data.verdict || 'UNKNOWN';
    verdict = status;
    
    let bgGradient = '';
    let borderColor = '';
    let iconHtml = '';
    let verdictDisplay = '';
    let textColor = '';
    
    if (verdict === 'SAFE' || verdict === 'safe') {
        borderColor = '#22c55e';
        bgGradient = 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)';
        iconHtml = '<i class="fas fa-check-circle text-green-500 text-2xl"></i>';
        verdictDisplay = '✅ SAFE';
        textColor = 'text-green-700';
    } 
    else if (verdict === 'PHISHING' || verdict === 'SPAM' || verdict === 'phishing') {
        borderColor = '#ef4444';
        bgGradient = 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)';
        iconHtml = '<i class="fas fa-skull-crossbones text-red-500 text-2xl"></i>';
        verdictDisplay = '⚠️ PHISHING DETECTED ⚠️';
        textColor = 'text-red-700';
    } 
    else if (verdict === 'SUSPICIOUS' || verdict === 'suspicious') {
        borderColor = '#eab308';
        bgGradient = 'linear-gradient(135deg, #fefce8 0%, #fef3c7 100%)';
        iconHtml = '<i class="fas fa-exclamation-triangle text-yellow-500 text-2xl"></i>';
        verdictDisplay = '⚠️ SUSPICIOUS ⚠️';
        textColor = 'text-yellow-700';
    } 
    else {
        borderColor = '#6b7280';
        bgGradient = 'linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%)';
        iconHtml = '<i class="fas fa-question-circle text-gray-500 text-2xl"></i>';
        verdictDisplay = 'UNKNOWN';
        textColor = 'text-gray-700';
    }
    
    const hasStrongPasswords = data.strong_passwords && data.strong_passwords.length > 0;
    
    // TWO COLUMN LAYOUT for password results
    if (hasStrongPasswords) {
        let html = `<div style="border-left-color: ${borderColor}; background: ${bgGradient}; border-radius: 12px; padding: 20px; margin-top: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
                        ${iconHtml}
                        <div>
                            <div style="font-weight: bold; font-size: 1.25rem; ${textColor}">${verdictDisplay}</div>
                            ${score ? `<div style="font-size: 0.875rem; color: #4b5563; margin-top: 4px;">Risk Score: ${score}/100</div>` : ''}
                        </div>
                    </div>`;
        
        if (confidence) {
            let confColor = confidence === 'HIGH' ? 'background: #fee2e2; color: #b91c1c;' : (confidence === 'MEDIUM' ? 'background: #fef3c7; color: #b45309;' : 'background: #dcfce7; color: #166534;');
            html += `<div style="margin-bottom: 12px; font-size: 0.875rem;">
                <span style="font-weight: 500;">Confidence:</span> 
                <span style="padding: 2px 8px; border-radius: 9999px; ${confColor} margin-left: 8px;">${escapeHtml(confidence)}</span>
            </div>`;
        }
        
        if (reasons && reasons.length > 0) {
            html += `<div style="margin-bottom: 12px;">
                <span style="font-weight: 500;">Detection Reasons:</span>
                <ul style="list-style: disc; list-style-position: inside; margin-top: 4px; font-size: 0.875rem;">`;
            reasons.forEach(r => {
                html += `<li style="color: #4b5563; margin-top: 4px;">⚠️ ${escapeHtml(r)}</li>`;
            });
            html += `</ul></div>`;
        }
        
        if (data.suggestions && data.suggestions.length > 0) {
            html += `<div style="margin-top: 12px; padding: 12px; background: #fef3c7; border-radius: 8px; border: 1px solid #fde68a;">
                <span style="font-weight: 500; color: #b45309;">💡 Suggestions to Improve:</span>
                <ul style="list-style: disc; list-style-position: inside; margin-top: 4px; font-size: 0.875rem; color: #b45309;">`;
            data.suggestions.forEach(s => {
                html += `<li>${escapeHtml(s)}</li>`;
            });
            html += `</ul></div>`;
        }
        
        if (data.estimated_crack_time) {
            html += `<div style="margin-top: 12px; padding: 8px; background: #f3f4f6; border-radius: 8px;">
                <span style="font-weight: 500;">🔓 Estimated Crack Time:</span> 
                <span style="font-family: monospace; margin-left: 8px;">${escapeHtml(data.estimated_crack_time)}</span>
            </div>`;
        }
        
        html += `</div><div style="border-left: 1px solid #e5e7eb; padding-left: 24px;">
            <div style="margin-bottom: 12px;">
                <span style="font-weight: bold; font-size: 1.125rem; color: #2563eb;"><i class="fas fa-star" style="margin-right: 8px;"></i>Strong Password Suggestions</span>
                <p style="font-size: 0.75rem; color: #6b7280; margin-top: 4px;">Click any password to copy</p>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px;">`;
        
        const colors = ['#8b5cf6', '#ec4899', '#06b6d4', '#10b981', '#f97316'];
        
        data.strong_passwords.forEach((p, idx) => {
            const color = colors[idx % colors.length];
            html += `<div style="background: ${color}; border-radius: 12px; padding: 12px; cursor: pointer; transition: all 0.2s;" 
                           onclick="copyToClipboard('${escapeHtml(p).replace(/'/g, "\\'")}')"
                           onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.2)';"
                           onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <code style="color: white; font-family: monospace; font-size: 0.875rem;">${escapeHtml(p)}</code>
                            <i class="fas fa-copy" style="color: white; opacity: 0.7;"></i>
                        </div>
                    </div>`;
        });
        
        html += `</div></div></div>
            <div class="copy-btn" style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #e5e7eb; text-align: center; cursor: pointer; color: #2563eb;" onclick="copyToClipboard('${escapeHtml(JSON.stringify(data, null, 2)).replace(/'/g, "\\'")}')">
                <i class="fas fa-copy"></i> Copy Full Result
            </div>
        </div>`;
        container.innerHTML = html;
    } else {
        // SINGLE COLUMN LAYOUT
        let html = `<div style="border-left-color: ${borderColor}; background: ${bgGradient}; border-radius: 12px; padding: 20px; margin-top: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
                ${iconHtml}
                <div>
                    <div style="font-weight: bold; font-size: 1.25rem; ${textColor}">${verdictDisplay}</div>
                    ${score ? `<div style="font-size: 0.875rem; color: #4b5563; margin-top: 4px;">Risk Score: ${score}/100</div>` : ''}
                </div>
            </div>`;
        
        if (confidence) {
            let confColor = confidence === 'HIGH' ? 'background: #fee2e2; color: #b91c1c;' : (confidence === 'MEDIUM' ? 'background: #fef3c7; color: #b45309;' : 'background: #dcfce7; color: #166534;');
            html += `<div style="margin-bottom: 12px; font-size: 0.875rem;">
                <span style="font-weight: 500;">Confidence:</span> 
                <span style="padding: 2px 8px; border-radius: 9999px; ${confColor} margin-left: 8px;">${escapeHtml(confidence)}</span>
            </div>`;
        }
        
        if (reasons && reasons.length > 0) {
            html += `<div style="margin-bottom: 12px;">
                <span style="font-weight: 500;">Detection Reasons:</span>
                <ul style="list-style: disc; list-style-position: inside; margin-top: 4px; font-size: 0.875rem;">`;
            reasons.forEach(r => {
                html += `<li style="color: #4b5563; margin-top: 4px;">⚠️ ${escapeHtml(r)}</li>`;
            });
            html += `</ul></div>`;
        }
        
        if (data.suggestions && data.suggestions.length > 0) {
            html += `<div style="margin-top: 12px; padding: 12px; background: #fef3c7; border-radius: 8px; border: 1px solid #fde68a;">
                <span style="font-weight: 500; color: #b45309;">💡 Suggestions to Improve:</span>
                <ul style="list-style: disc; list-style-position: inside; margin-top: 4px; font-size: 0.875rem; color: #b45309;">`;
            data.suggestions.forEach(s => {
                html += `<li>${escapeHtml(s)}</li>`;
            });
            html += `</ul></div>`;
        }
        
        if (data.estimated_crack_time) {
            html += `<div style="margin-top: 12px; padding: 8px; background: #f3f4f6; border-radius: 8px;">
                <span style="font-weight: 500;">🔓 Estimated Crack Time:</span> 
                <span style="font-family: monospace; margin-left: 8px;">${escapeHtml(data.estimated_crack_time)}</span>
            </div>`;
        }
        
        if (data.extracted_text) {
            html += `<div style="margin-top: 12px;">
                <span style="font-weight: 500;">📝 Extracted Text:</span>
                <div style="background: white; border-radius: 8px; padding: 8px; margin-top: 4px; font-size: 0.875rem; max-height: 128px; overflow-y: auto;">${escapeHtml(data.extracted_text)}</div>
            </div>`;
        }
        
        if (data.urls_found && data.urls_found.length > 0) {
            html += `<div style="margin-top: 8px; font-size: 0.875rem;">
                <span style="font-weight: 500;">🔗 URLs Found:</span>
                <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px;">`;
            data.urls_found.forEach(u => {
                html += `<span style="background: #dbeafe; color: #1d4ed8; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem;">${escapeHtml(u)}</span>`;
            });
            html += `</div></div>`;
        }
        
        html += `<div class="copy-btn" style="margin-top: 16px; padding-top: 8px; border-top: 1px solid #e5e7eb; text-align: center; cursor: pointer; color: #2563eb;" onclick="copyToClipboard('${escapeHtml(JSON.stringify(data, null, 2)).replace(/'/g, "\\'")}')">
            <i class="fas fa-copy"></i> Copy Full Result
        </div></div>`;
        container.innerHTML = html;
    }
    
    if (verdict === 'PHISHING' || verdict === 'SPAM') {
        showToast('⚠️ PHISHING DETECTED! This is dangerous!', 'error');
    } else if (verdict === 'SUSPICIOUS') {
        showToast('⚠️ Suspicious content detected. Be careful!', 'warning');
    } else if (verdict === 'SAFE') {
        showToast('✅ Safe! No threats detected.', 'success');
    }
}

// ------------------------------
// COPY TO CLIPBOARD
// ------------------------------
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// ------------------------------
// DARK MODE
// ------------------------------
function initDarkMode() {
    const isDark = localStorage.getItem('darkMode') === 'true';
    if (isDark) {
        document.documentElement.classList.add('dark');
    }
    updateDarkModeIcon(isDark);
}

function toggleDarkMode() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', isDark);
    updateDarkModeIcon(isDark);
}

function updateDarkModeIcon(isDark) {
    const icon = document.getElementById('darkModeIcon');
    if (icon) {
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// ------------------------------
// TABS
// ------------------------------
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            tabButtons.forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
            btn.classList.add('active');
            const targetTab = document.getElementById(`tab-${tabId}`);
            if (targetTab) targetTab.classList.remove('hidden');
        });
    });
}

// ------------------------------
// CHAT FUNCTIONS (Auto-size messages)
// ------------------------------
function addChatMessage(message, sender) {
    const container = document.getElementById('chatMessages');
    if (!container) return;
    
    const messageDiv = document.createElement('div');
    
    if (sender === 'user') {
        messageDiv.className = 'mb-3 flex justify-end';
        messageDiv.innerHTML = `
            <div class="inline-block max-w-[85%] bg-blue-50 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-2xl rounded-tr-md px-4 py-2 shadow-sm break-words">
                <div class="text-sm whitespace-pre-wrap">${escapeHtml(message)}</div>
            </div>
        `;
    } else {
        messageDiv.className = 'mb-3 flex justify-start';
        messageDiv.innerHTML = `
            <div class="inline-block max-w-[85%] bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-2xl rounded-tl-md px-4 py-2 shadow-sm border border-gray-200 dark:border-gray-700 break-words">
                <div class="flex items-center gap-2 mb-1">
                    <i class="fas fa-robot text-xs text-gray-500 dark:text-gray-400"></i>
                    <span class="text-xs font-medium text-gray-500 dark:text-gray-400">PhishGuard AI</span>
                </div>
                <div class="text-sm whitespace-pre-wrap">${escapeHtml(message)}</div>
            </div>
        `;
    }
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function addTypingIndicator() {
    const container = document.getElementById('chatMessages');
    if (!container) return;
    
    const typingId = 'typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.id = typingId;
    typingDiv.className = 'mb-3 flex justify-start';
    typingDiv.innerHTML = `
        <div class="inline-block bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 rounded-2xl rounded-tl-md px-4 py-2 shadow-sm border border-gray-200 dark:border-gray-700">
            <div class="flex items-center gap-1">
                <i class="fas fa-robot text-xs"></i>
                <span class="text-xs">PhishGuard AI is typing</span>
                <span class="flex gap-0.5 ml-1">
                    <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"></span>
                    <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
                    <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
                </span>
            </div>
        </div>
    `;
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
    return typingId;
}

function removeTypingIndicator(typingId) {
    const element = document.getElementById(typingId);
    if (element) element.remove();
}

// ------------------------------
// POPUP CHAT FUNCTIONS
// ------------------------------
let isPopupOpen = false;

function toggleAIPopup() {
    const popup = document.getElementById('aiPopup');
    if (isPopupOpen) {
        popup.classList.add('hidden');
        isPopupOpen = false;
    } else {
        popup.classList.remove('hidden');
        isPopupOpen = true;
    }
}

function addPopupChatMessage(message, sender) {
    const container = document.getElementById('popupChatMessages');
    if (!container) return;
    
    const messageDiv = document.createElement('div');
    
    if (sender === 'user') {
        messageDiv.className = 'text-right mb-2';
        messageDiv.innerHTML = `
            <span class="inline-block max-w-[90%] bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 rounded-xl px-3 py-1.5 text-sm shadow-sm break-words">
                ${escapeHtml(message)}
            </span>
        `;
    } else {
        messageDiv.className = 'text-left mb-2';
        messageDiv.innerHTML = `
            <div class="inline-block max-w-[90%] bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-xl px-3 py-1.5 text-sm shadow-sm border border-gray-200 dark:border-gray-600 break-words">
                <div class="flex items-center gap-1 mb-0.5">
                    <i class="fas fa-robot text-xs text-gray-500"></i>
                    <span class="text-xs text-gray-500">AI</span>
                </div>
                <span class="whitespace-pre-wrap">${escapeHtml(message)}</span>
            </div>
        `;
    }
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function addPopupTypingIndicator() {
    const container = document.getElementById('popupChatMessages');
    if (!container) return;
    
    const typingId = 'popup-typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.id = typingId;
    typingDiv.className = 'text-left mb-2';
    typingDiv.innerHTML = `
        <div class="inline-block bg-gray-100 dark:bg-gray-700 text-gray-500 rounded-xl px-3 py-1.5 text-sm">
            <span class="flex gap-1">
                <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"></span>
                <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
                <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
            </span>
        </div>
    `;
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
    return typingId;
}

function removePopupTypingIndicator(typingId) {
    const element = document.getElementById(typingId);
    if (element) element.remove();
}

async function sendPopupChat() {
    const input = document.getElementById('popupChatInput');
    const message = input.value.trim();
    if (!message) return;
    
    addPopupChatMessage(message, 'user');
    input.value = '';
    
    const typingId = addPopupTypingIndicator();
    
    try {
        const response = await fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: 'popup_user', message: message })
        });
        const result = await response.json();
        removePopupTypingIndicator(typingId);
        const reply = result.reply || result.response || 'No response';
        addPopupChatMessage(reply, 'bot');
    } catch (error) {
        removePopupTypingIndicator(typingId);
        addPopupChatMessage('Network error. Backend running?', 'bot');
    }
}

// ------------------------------
// INITIALIZE
// ------------------------------
document.addEventListener('DOMContentLoaded', function() {
    const popupBtn = document.getElementById('aiPopupBtn');
    if (popupBtn) {
        popupBtn.addEventListener('click', toggleAIPopup);
    }
    const popupChatInput = document.getElementById('popupChatInput');
    if (popupChatInput) {
        popupChatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendPopupChat();
        });
    }
});

function clearResult(elementId) {
    const element = document.getElementById(elementId);
    if (element) element.innerHTML = '';
}

function clearAllResults() {
    clearResult('urlResult');
    clearResult('emailResult');
    clearResult('contentResult');
    clearResult('passwordResult');
    clearResult('imageResult');
}