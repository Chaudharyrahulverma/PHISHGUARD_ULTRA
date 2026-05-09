from models.url_detector import URLDetector

detector = None

def init(dataset):
    global detector
    detector = URLDetector(dataset)

def scan(url):
    return detector.analyze(url)