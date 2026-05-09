from models.password_checker import PasswordChecker

checker = PasswordChecker()

def scan(password):
    return checker.analyze(password)