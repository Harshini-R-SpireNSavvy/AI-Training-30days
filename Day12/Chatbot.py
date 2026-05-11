from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a friendly career advisor chatbot.
You help users with career guidance, skills, and job advice.
Keep responses simple, clear, and helpful.
"""

chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat():
    print("Career Advisor Chatbot (type 'reset' or 'exit')")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "reset":
            chat_history.clear()
            chat_history.append({"role": "system", "content": SYSTEM_PROMPT})
            print("Chat reset!")
            continue

        chat_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=chat_history
        )

        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})

        print("\nBot:", reply)


if __name__ == "__main__":
    chat()