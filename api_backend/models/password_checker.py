import re
import random
import string

class PasswordChecker:

    def __init__(self):
        self.common_patterns = [
            "123456", "password", "qwerty", "admin", "welcome",
            "12345678", "abc123", "password123", "admin123", "qwerty123"
        ]

    def analyze(self, password):
        score = 0
        reasons = []
        suggestions = []
        strength_score = 0  # This will be 0-100

        length = len(password)

        # ===== LENGTH =====
        if length < 6:
            strength_score -= 20
            reasons.append("Too short")
            suggestions.append("Use at least 8+ characters")
        elif length >= 8:
            strength_score += 20
        if length >= 12:
            strength_score += 15
        if length >= 16:
            strength_score += 10

        # ===== LOWERCASE =====
        if not re.search(r"[a-z]", password):
            reasons.append("Missing lowercase letters")
            suggestions.append("Add lowercase letters (a-z)")
        else:
            strength_score += 10

        # ===== UPPERCASE =====
        if not re.search(r"[A-Z]", password):
            reasons.append("Missing uppercase letters")
            suggestions.append("Add uppercase letters (A-Z)")
        else:
            strength_score += 10

        # ===== NUMBERS =====
        if not re.search(r"[0-9]", password):
            reasons.append("Missing numbers")
            suggestions.append("Add numbers (0-9)")
        else:
            strength_score += 10

        # ===== SYMBOLS =====
        if not re.search(r"[!@#$%^&*()_+=\-{};:'\",.<>?/]", password):
            reasons.append("Missing special symbols")
            suggestions.append("Add symbols (!@#$...)")
        else:
            strength_score += 15

        # ===== COMMON PATTERN =====
        for p in self.common_patterns:
            if p in password.lower():
                strength_score -= 30
                reasons.append("Common weak pattern detected")
                break

        # ===== REPEATED CHAR =====
        if re.search(r"(.)\1{2,}", password):
            strength_score -= 10
            reasons.append("Repeated characters detected")

        # ===== SEQUENTIAL =====
        if "123" in password or "abc" in password.lower():
            strength_score -= 10
            reasons.append("Sequential pattern detected")

        # ===== UNIQUE CHARACTERS =====
        unique_chars = len(set(password))
        if unique_chars > length * 0.7:
            strength_score += 10
        elif unique_chars < 3 and length > 0:
            strength_score -= 10
            reasons.append("Too many repeated characters")

        # ===== FIX: LIMIT SCORE TO 0-100 RANGE =====
        strength_score = max(0, min(strength_score, 100))

        # ===== STATUS BASED ON SCORE =====
        if strength_score < 40:
            status = "WEAK"
            confidence = "HIGH"
        elif strength_score < 70:
            status = "MEDIUM"
            confidence = "MEDIUM"
        else:
            status = "STRONG"
            confidence = "HIGH"

        # ===== CRACK TIME ESTIMATION =====
        crack_time = self.estimate_crack_time(password)

        # ===== GENERATE STRONG PASSWORDS =====
        strong_passwords = self.generate_strong_passwords(password)

        return {
            "status": status,
            "score": strength_score,  # Ye ab 0-100 range mein hoga
            "confidence": confidence,
            "reasons": reasons,
            "suggestions": suggestions,
            "estimated_crack_time": crack_time,
            "strong_passwords": strong_passwords
        }

    # ===== CRACK TIME ESTIMATION =====
    def estimate_crack_time(self, password):
        charset = 0

        if re.search(r"[a-z]", password):
            charset += 26
        if re.search(r"[A-Z]", password):
            charset += 26
        if re.search(r"[0-9]", password):
            charset += 10
        if re.search(r"[!@#$%^&*()_+=\-{};:'\",.<>?/]", password):
            charset += 32

        length = len(password)

        if charset == 0 or length == 0:
            return "Instantly cracked"

        combinations = charset ** length

        # Assume attacker speed = 1B guesses/sec
        seconds = combinations / 1_000_000_000

        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds/60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds/3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds/86400)} days"
        else:
            return "Years+"

    # ===== GENERATE 5 STRONG PASSWORDS =====
    def generate_strong_passwords(self, base):
        # Generate smart base from original password
        base_clean = re.sub(r'[^a-zA-Z]', '', base)
        
        if len(base_clean) < 3:
            base_clean = "Secure"
        else:
            base_clean = base_clean[:6].capitalize()

        passwords = set()  # Use set to avoid duplicates

        for _ in range(10):  # Generate more, then pick 5 unique
            random_part = ''.join(random.choices(
                string.ascii_letters + string.digits + "!@#$%", k=8))
            
            special_char = random.choice("!@#$%&*")
            number = str(random.randint(10, 99))
            
            strong = base_clean + random_part + special_char + number
            passwords.add(strong)

        return list(passwords)[:5]