# services/ai_service.py

from ai_engine.chatbot import ChatBot

# single instance (performance better)
bot = ChatBot()


def chat(user_id, message):
    """
    Main AI chat function
    """

    try:
        result = bot.process(user_id, message)

        return {
            "reply": result.get("response"),
            "intent": result.get("intent")
        }

    except Exception as e:
        print("❌ AI Error:", e)

        return {
            "reply": "System error aaya hai, dubara try karo."
        }