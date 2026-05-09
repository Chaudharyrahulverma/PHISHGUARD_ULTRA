# ai_engine/chatbot.py

from ai_engine.intent_detector import detect_intent
from ai_engine.response_generator import generate_response


class ChatBot:
    def __init__(self):
        pass

    def process(self, user_id, message):
        """
        Main entry point for chatbot
        """

        # 1️⃣ Clean message
        message = message.strip().lower()

        # 2️⃣ Detect intent
        intent, entity = detect_intent(message)

        # 3️⃣ Generate response
        response = generate_response(intent, entity, message)

        return {
            "user_id": user_id,
            "intent": intent,
            "response": response
        }