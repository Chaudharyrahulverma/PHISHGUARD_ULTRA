import json
import os

DATA_FILE = "models/ai_memory.json"


def load_memory():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def learn(question, answer):
    data = load_memory()
    data.append({
        "q": question.lower(),
        "a": answer
    })
    save_memory(data)


def search_memory(msg):
    data = load_memory()
    msg = msg.lower()

    for item in data:
        if item["q"] in msg:
            return item["a"]

    return None