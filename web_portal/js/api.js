// ========================================
// PHISHGUARD ULTRA - API HANDLER
// ========================================

// Change this to your backend URL
const API_BASE_URL = 'http://localhost:5000';

// Helper function for JSON API calls
async function apiCall(endpoint, data) {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        return result;
        
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        return {
            error: true,
            message: error.message || 'Network error. Make sure backend is running on ' + API_BASE_URL
        };
    }
}

// Helper function for file upload (multipart/form-data)
async function apiFileUpload(endpoint, formData) {
    const options = {
        method: 'POST',
        body: formData
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        return result;
        
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        return {
            error: true,
            message: error.message || 'Network error. Make sure backend is running on ' + API_BASE_URL
        };
    }
}

// ================= URL SCANNER =================
async function scanUrl() {
    const urlInput = document.getElementById('urlInput');
    const url = urlInput?.value.trim();
    
    if (!url) {
        showToast('Please enter a URL', 'error');
        return;
    }
    
    showLoader('urlResult');
    
    const result = await apiCall('/check-url', { url });
    
    hideLoader('urlResult');
    displayResult('urlResult', result, 'url');
}

// ================= EMAIL SCANNER =================
async function scanEmail() {
    const emailInput = document.getElementById('emailInput');
    const email = emailInput?.value.trim();
    
    if (!email) {
        showToast('Please enter an email address', 'error');
        return;
    }
    
    // Basic email validation
    if (!email.includes('@') || !email.includes('.')) {
        showToast('Please enter a valid email address', 'error');
        return;
    }
    
    showLoader('emailResult');
    
    const result = await apiCall('/check-email', { email });
    
    hideLoader('emailResult');
    displayResult('emailResult', result, 'email');
}

// ================= CONTENT SCANNER =================
async function scanContent() {
    const contentInput = document.getElementById('contentInput');
    const text = contentInput?.value.trim();
    
    if (!text) {
        showToast('Please enter text content to scan', 'error');
        return;
    }
    
    showLoader('contentResult');
    
    const result = await apiCall('/check-content', { text });
    
    hideLoader('contentResult');
    displayResult('contentResult', result, 'content');
}

// ================= PASSWORD CHECKER =================
async function checkPassword() {
    const passwordInput = document.getElementById('passwordInput');
    const password = passwordInput?.value;
    
    if (!password) {
        showToast('Please enter a password to check', 'error');
        return;
    }
    
    showLoader('passwordResult');
    
    const result = await apiCall('/check-password', { password });
    
    hideLoader('passwordResult');
    displayResult('passwordResult', result, 'password');
}

// ================= IMAGE SCANNER =================
async function scanImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput?.files[0];
    
    if (!file) {
        showToast('Please select an image to scan', 'error');
        return;
    }
    
    // Check file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
        showToast('Please select a PNG or JPG image', 'error');
        return;
    }
    
    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showToast('Image size should be less than 5MB', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoader('imageResult');
    
    const result = await apiFileUpload('/check-image', formData);
    
    hideLoader('imageResult');
    displayResult('imageResult', result, 'image');
}

// ================= AI CHAT =================
async function sendChat() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput?.value.trim();
    
    if (!message) {
        return;
    }
    
    // Add user message to chat
    addChatMessage(message, 'user');
    chatInput.value = '';
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    const result = await apiCall('/chat', { 
        user_id: 'web_user_' + Date.now(),
        message: message 
    });
    
    // Remove typing indicator
    removeTypingIndicator(typingId);
    
    // Extract reply from response
    const reply = result.reply || result.response || 'No response from server';
    addChatMessage(reply, 'bot');
}

// ================= REPORT SUBMIT (Optional) =================
async function submitReport(type, value, feedback) {
    const data = {
        type: type,
        value: value,
        wrong_detection: feedback.wrong_detection || false,
        missing_reason: feedback.missing_reason || false,
        poor_explanation: feedback.poor_explanation || false,
        feedback: feedback.text || ''
    };
    
    const result = await apiCall('/submit-report', data);
    return result;
}