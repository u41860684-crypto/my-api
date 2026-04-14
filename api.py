from flask import Flask, request, jsonify
import json, os, random
from rapidfuzz import fuzz

app = Flask(__name__)

MEMORY_FILE = "memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}

def save():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def normalize(text):
    return text.lower().strip()

def search_memory(text):
    best, score_best = None, 0

    for key in memory:
        score = fuzz.token_set_ratio(text, key)
        if score > score_best:
            score_best = score
            best = key

    if score_best > 70:
        return random.choice(memory[best])

    return None

def fallback(text):
    if len(text.split()) == 1:
        return random.choice(["Понял 🙂", "Окей 😄", "Интересно"])
    return random.choice([
        "Интересно 🤔 расскажи подробнее",
        "А что дальше?",
        "Хм… звучит интересно",
        "О, прикольно 😄"
    ])

@app.route("/api", methods=["GET"])
def api():
    text = normalize(request.args.get("text", ""))

    if "=" in text:
        q, a = text.split("=", 1)
        memory.setdefault(q.strip(), []).append(a.strip())
        save()
        return jsonify({"response": "🧠 Запомнил"})

    answer = search_memory(text)

    if not answer:
        answer = fallback(text)

    return jsonify({"response": answer})

app.run(host="0.0.0.0", port=5000)
