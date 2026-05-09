import re
import json
from collections import defaultdict

LEARN_FILE = "models/dataset/email_learning.json"

DISPOSABLE = [
    "tempmail", "10minutemail", "mailinator",
    "guerrillamail", "trashmail"
]

KEYWORDS = [
    "support","secure","verify","update","bank",
    "login","account","alert","billing"
]

class EmailDetector:

    def __init__(self, dataset):
        self.dataset = set(dataset)
        self.learning = defaultdict(int)
        self.load_learning()

    def load_learning(self):
        try:
            with open(LEARN_FILE, "r") as f:
                self.learning = defaultdict(int, json.load(f))
        except:
            pass

    def save_learning(self):
        with open(LEARN_FILE, "w") as f:
            json.dump(self.learning, f)

    def analyze(self, email):

        email = email.lower().strip()
        score = 0
        reasons = []

        # -------------------------
        # FORMAT
        # -------------------------
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            return {
                "status": "SUSPICIOUS",
                "score": 60,
                "confidence": "LOW",
                "reasons": ["Invalid format"]
            }

        user, domain = email.split("@")

        # -------------------------
        # DATASET BLACKLIST
        # -------------------------
        if email in self.dataset:
            score += 100
            reasons.append("Blacklisted email")

        # -------------------------
        # LEARNING MEMORY
        # -------------------------
        if email in self.learning:
            score += self.learning[email]
            reasons.append("Learned risky email")

        # -------------------------
        # DISPOSABLE DOMAIN
        # -------------------------
        for d in DISPOSABLE:
            if d in domain:
                score += 50
                reasons.append("Disposable email")

        # -------------------------
        # KEYWORD IN USER
        # -------------------------
        for k in KEYWORDS:
            if k in user:
                score += 15
                reasons.append(f"Keyword: {k}")

        # -------------------------
        # RANDOM USER
        # -------------------------
        if re.match(r"[a-z0-9]{8,}$", user):
            score += 20
            reasons.append("Random username")

        # -------------------------
        # NUMBER HEAVY EMAIL
        # -------------------------
        if sum(c.isdigit() for c in user) > 4:
            score += 15
            reasons.append("Too many numbers")

        # -------------------------
        # DOMAIN RISK
        # -------------------------
        if domain.endswith((".xyz",".top",".tk",".ml")):
            score += 30
            reasons.append("Risky domain")

        # -------------------------
        # FINAL
        # -------------------------
        if score >= 90:
            status = "SPAM"
            confidence = "HIGH"
        elif score >= 50:
            status = "SUSPICIOUS"
            confidence = "MEDIUM"
        else:
            status = "SAFE"
            confidence = "LOW"

        # -------------------------
        # SELF LEARNING
        # -------------------------
        if status in ["SPAM","SUSPICIOUS"]:
            self.learning[email] += 10
            self.save_learning()

        return {
            "status": status,
            "score": score,
            "confidence": confidence,
            "reasons": list(set(reasons))
        }