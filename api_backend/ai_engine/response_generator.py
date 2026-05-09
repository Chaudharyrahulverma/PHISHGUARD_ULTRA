# =============================
# PRO RESPONSE GENERATOR (ENGLISH ONLY + TOOL AI)
# =============================

from services.ai_llm import llm_reply


def generate_response(intent, entity, message):

    msg = message.lower().strip()

    # ================= TOOL QUERY =================
    if intent == "tool_query":
        return llm_reply("", message)

    # ================= ATTACK =================
    if intent == "attack_query":
        return f"""⚠️ Attack: {entity.upper()}

This is a cybersecurity attack technique used to exploit systems.

Use it only for learning and ethical testing purposes.
"""

    # ================= URL =================
    if intent == "url_scan":
        return f"""🔗 URL detected: {entity}

Use the URL Scanner tool to analyze this link.
"""

    # ================= PASSWORD =================
    if intent == "password_help":
        return """🔒 Strong Password Tips:

- Use uppercase + lowercase
- Add numbers and symbols
- Minimum 10+ characters

Example: H@ck3r#2026
"""

    # ================= LAB =================
    if intent == "lab_query":
        return """🧠 Lab Approach:

1. Enumeration
2. Find vulnerabilities
3. Exploit carefully

Focus on learning, not shortcuts.
"""

    # ================= EXPLAIN =================
    if intent == "explain":
        return """📊 Paste your scan result.

I will explain whether it is safe or phishing.
"""

    # ================= GREETING =================
    if intent == "greeting":
        return "Hello 👋 I am your cybersecurity assistant. What do you want to learn?"

    # ================= DEFAULT (SMART AI) =================
    return llm_reply("", message)