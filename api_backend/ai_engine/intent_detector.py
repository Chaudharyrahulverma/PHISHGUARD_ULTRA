# ai_engine/intent_detector.py

import re


def detect_intent(message):
    """
    Detect user intent + entity
    Returns: (intent, entity)
    """

    msg = message.lower()

    # ================= GREETING =================
    if any(word in msg for word in ["hi", "hello", "hey", "namaste"]):
        return "greeting", None

    # ================= URL DETECT =================
    url_pattern = r"(https?://\S+|www\.\S+|\S+\.(com|net|org|tk|xyz|in))"
    url_match = re.search(url_pattern, msg)
    if url_match:
        return "url_scan", url_match.group()

    # ================= TOOL QUERY =================
    tools = ["nmap", "sqlmap", "burp", "wireshark", "hydra"]
    for tool in tools:
        if tool in msg:
            return "tool_query", tool

    # ================= ATTACK QUERY =================
    attacks = [
        "phishing",
        "sql injection",
        "sqli",
        "xss",
        "csrf",
        "brute force",
        "ddos"
    ]
    for attack in attacks:
        if attack in msg:
            return "attack_query", attack

    # ================= LAB QUERY =================
    if any(word in msg for word in ["tryhackme", "hackthebox", "portswigger", "lab"]):
        return "lab_query", None

    # ================= SCAN EXPLAIN =================
    if any(word in msg for word in ["why", "reason", "kaise", "kyu"]):
        return "explain", None

    # ================= PASSWORD =================
    if "password" in msg:
        return "password_help", None

    # ================= DEFAULT =================
    return "unknown", None