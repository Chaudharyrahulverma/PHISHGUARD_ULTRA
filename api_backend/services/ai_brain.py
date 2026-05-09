# =============================
# AI BRAIN (MEMORY + CONTEXT)
# =============================

from services.ai_llm import llm_reply

# -----------------------------
# MEMORY STORE
# -----------------------------
chat_memory = {}

def get_memory(user_id):
    return chat_memory.get(user_id, [])

def save_memory(user_id, message):
    if user_id not in chat_memory:
        chat_memory[user_id] = []

    chat_memory[user_id].append(message)

    # keep last 5 messages only
    chat_memory[user_id] = chat_memory[user_id][-5:]


def build_context(user_id):
    history = get_memory(user_id)

    # last 3 messages context
    return " | ".join(history[-3:])


# -----------------------------
# INTENT DETECT
# -----------------------------
def detect_intent(msg):

    if msg.startswith("http") or "www." in msg:
        return "url"

    if "@" in msg and "." in msg:
        return "email"

    if "password" in msg:
        return "password"

    return "general"


# -----------------------------
# SMART FOLLOW-UP DETECT
# -----------------------------
def is_follow_up(msg):
    keywords = ["more", "detail", "again", "explain more", "next"]

    return any(k in msg for k in keywords)


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def process_message(user_id, message):

    msg = message.lower().strip()

    # save memory first
    save_memory(user_id, message)

    # context
    context = build_context(user_id)

    # intent
    intent = detect_intent(msg)

    # -----------------------------
    # TOOL ROUTING
    # -----------------------------
    if intent == "url":
        return {
            "reply": "🔗 URL detected. Use URL Scanner for detailed analysis.",
            "intent": "url"
        }

    if intent == "email":
        return {
            "reply": "📧 Email detected. Use Email Scanner.",
            "intent": "email"
        }

    if intent == "password":
        return {
            "reply": "🔒 Use Password Checker tool.",
            "intent": "password"
        }

    # -----------------------------
    # FOLLOW-UP LOGIC
    # -----------------------------
    if is_follow_up(msg):
        full_context = f"Previous context: {context} | Follow-up: {message}"
    else:
        full_context = context

    # -----------------------------
    # AI RESPONSE
    # -----------------------------
    reply = llm_reply(full_context, message)

    return {
        "reply": reply,
        "intent": "ai"
    }
