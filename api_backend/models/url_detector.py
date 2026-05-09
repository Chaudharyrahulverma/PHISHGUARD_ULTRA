import re
import json
from urllib.parse import urlparse
from collections import defaultdict
from difflib import SequenceMatcher

# =========================
# CONFIG
# =========================

DATA_FILE = "models/dataset/url_learning.json"

SUSPICIOUS_KEYWORDS = [
    "login","verify","secure","update","bank",
    "account","free","gift","bonus","urgent",
    "confirm","signin","reset","password"
]

BRANDS = [
    "paypal","google","facebook","amazon",
    "microsoft","apple","netflix","instagram",
    "sbi","hdfc","icici","axis"
]

RISKY_TLDS = ["tk","ml","ga","cf","xyz","top"]

TUNNEL_DOMAINS = [
    "ngrok", "trycloudflare", "serveo"
]

# =========================
# HELPERS
# =========================

def similarity(a,b):
    return SequenceMatcher(None,a,b).ratio()

def extract(url):
    parsed = urlparse(url)
    host = parsed.netloc.lower().split(":")[0]

    if host.startswith("www."):
        host = host[4:]

    parts = host.split(".")
    domain = parts[-2] if len(parts)>=2 else host
    tld = parts[-1] if len(parts)>=2 else ""

    return host, domain, tld, parsed.path.lower()

# =========================
# DETECTOR
# =========================

class URLDetector:

    def __init__(self, dataset):
        self.dataset = set(dataset)

        self.domain_set = set()
        for u in dataset:
            h,_,_,_ = extract(u)
            if h:
                self.domain_set.add(h)

        self.learning = defaultdict(int)
        self.load_learning()

    # -------------------------
    def load_learning(self):
        try:
            with open(DATA_FILE,"r") as f:
                self.learning = defaultdict(int,json.load(f))
        except:
            pass

    def save_learning(self):
        with open(DATA_FILE,"w") as f:
            json.dump(self.learning,f)

    # =========================
    def analyze(self,url):

        url = url.strip()

        if not url.startswith("http"):
            url = "http://" + url

        host, domain, tld, path = extract(url)

        score = 0
        reasons = []

        # -------------------------
        # LEARNING MEMORY
        # -------------------------
        if host in self.learning:
            score += self.learning[host]
            reasons.append("Learned suspicious domain")

        # -------------------------
        # DATASET MATCH
        # -------------------------
        if url in self.dataset:
            score += 120
            reasons.append("Exact dataset match")

        elif host in self.domain_set:
            score += 80
            reasons.append("Domain found in dataset")

        # -------------------------
        # TUNNEL DOMAIN (FIX)
        # -------------------------
        for td in TUNNEL_DOMAINS:
            if td in host:
                score += 50
                reasons.append("Tunnel domain (high risk)")

        # -------------------------
        # RANDOM SUBDOMAIN (FIX)
        # -------------------------
        sub = host.split(".")[0]

        if re.match(r"[a-z0-9\-]{10,}", sub):
            score += 25
            reasons.append("Random subdomain")

        # -------------------------
        # IP-LIKE PATTERN (FIX)
        # -------------------------
        if re.search(r"\d{1,3}[-\.]\d{1,3}[-\.]\d{1,3}", sub):
            score += 35
            reasons.append("IP-like pattern in domain")

        # -------------------------
        # RISKY TLD
        # -------------------------
        if tld in RISKY_TLDS:
            score += 30
            reasons.append(f"Risky TLD: {tld}")

        # -------------------------
        # KEYWORDS
        # -------------------------
        keyword_hits = 0
        for k in SUSPICIOUS_KEYWORDS:
            if k in url:
                keyword_hits += 1
                score += 10

        if keyword_hits:
            reasons.append(f"{keyword_hits} suspicious keywords")

        # -------------------------
        # BRAND + KEYWORD COMBO
        # -------------------------
        tokens = re.split(r"[-\.]", host)

        for b in BRANDS:
            if b in tokens:
                score += 25
                reasons.append(f"Brand: {b}")

                if keyword_hits:
                    score += 40
                    reasons.append("Brand + phishing combo")

        # -------------------------
        # LOOKALIKE DOMAIN
        # -------------------------
        for b in BRANDS:
            if similarity(domain,b) > 0.8 and domain != b:
                score += 50
                reasons.append(f"Looks like {b}")

        # -------------------------
        # STRUCTURE CHECKS
        # -------------------------
        if "@" in url:
            score += 40
            reasons.append("@ redirect")

        if host.count(".") > 3:
            score += 20
            reasons.append("Too many subdomains")

        if "-" in domain:
            score += 15
            reasons.append("Hyphen domain")

        if re.match(r"\d+\.\d+\.\d+\.\d+", host):
            score += 50
            reasons.append("IP URL")

        # ========== FIX: LIMIT SCORE TO 100 ==========
        # Ye hai important fix – score ko 100 se upar nahi jane denge
        if score > 100:
            score = 100
        
        # ========== SECONDARY FIX: Agar exact match hai to directly 100 ==========
        if url in self.dataset:
            score = 100
            reasons = ["Exact malicious URL match - Highly Dangerous"]

        # -------------------------
        # FINAL DECISION (STRICT)
        # -------------------------
        if score >= 80:
            status = "PHISHING"
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
        if status in ["PHISHING", "SUSPICIOUS"]:
            self.learning[host] += 10
            self.save_learning()

        return {
            "status": status,
            "score": score,
            "confidence": confidence,
            "reasons": list(set(reasons))
        }