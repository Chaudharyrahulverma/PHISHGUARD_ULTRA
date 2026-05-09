from models.email_detector import EmailDetector

detector = None

def init(dataset):
    global detector
    detector = EmailDetector(dataset)

def scan(email):
    return detector.analyze(email)