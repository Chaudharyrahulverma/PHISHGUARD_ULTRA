import json
import os

MODEL_PATH = "ml_model.json"

class MLEngine:

    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "w") as f:
                json.dump({}, f)

        with open(MODEL_PATH, "r") as f:
            self.model = json.load(f)

    def update(self, key, label):
        if key not in self.model:
            self.model[key] = {"phishing": 0, "safe": 0}

        self.model[key][label] += 1

        with open(MODEL_PATH, "w") as f:
            json.dump(self.model, f)

    def predict(self, key):
        if key in self.model:
            data = self.model[key]
            if data["phishing"] > data["safe"]:
                return "PHISHING"
        return None