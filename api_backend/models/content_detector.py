import re
import json
import os

# 📂 Learning file path
LEARNING_FILE = "models/dataset/content_learning.json"

# 🧠 Suspicious keywords (base knowledge)
SUSPICIOUS_KEYWORDS = [
    "urgent", "verify", "suspend", "account locked", "click here",
    "login now", "update details", "bank", "otp", "password",
    "limited time", "security alert", "confirm identity"
]

# 🚩 Risky domains
SUSPICIOUS_DOMAINS = [".tk", ".ml", ".ga", ".cf"]

# 📊 Load learning data
def load_learning():
    if not os.path.exists(LEARNING_FILE):
        return []
    with open(LEARNING_FILE, "r") as f:
        return json.load(f)

# 💾 Save learning data
def save_learning(data):
    with open(LEARNING_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 🔍 Main detection function
def analyze_content(text):

    text_lower = text.lower()
    score = 0
    reasons = []

    # 🚨 Keyword detection
    for word in SUSPICIOUS_KEYWORDS:
        if word in text_lower:
            score += 10
            reasons.append(f"Keyword detected: {word}")

    # 🔗 URL detection
    urls = re.findall(r'(https?://[^\s]+)', text_lower)
    if urls:
        score += 15
        reasons.append("Contains URL")

        for url in urls:
            for domain in SUSPICIOUS_DOMAINS:
                if domain in url:
                    score += 20
                    reasons.append(f"Suspicious domain: {domain}")

    # ⚠️ Urgency pattern
    if re.search(r'urgent|immediately|within \d+ hours', text_lower):
        score += 15
        reasons.append("Urgency pressure detected")

    # 🏦 Brand phishing pattern
    if re.search(r'(sbi|hdfc|icici|paypal|google|amazon)', text_lower):
        if "http" in text_lower:
            score += 20
            reasons.append("Brand + link combo (phishing pattern)")

    # 📈 Normalize score
    if score > 100:
        score = 100

    # 🎯 Result
    if score > 60:
        verdict = "PHISHING"
        confidence = "HIGH"
    elif score > 30:
        verdict = "SUSPICIOUS"
        confidence = "MEDIUM"
    else:
        verdict = "SAFE"
        confidence = "LOW"

    return {
        "verdict": verdict,
        "score": score,
        "confidence": confidence,
        "reasons": reasons
    }


# 🤖 Self-learning (future ready)
def learn_from_report(text, label):
    data = load_learning()
    data.append({
        "text": text,
        "label": label
    })
    save_learning(data)