import os
from groq import Groq
from dotenv import load_dotenv

# Load env
load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(user_input):
    try:
        response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
        {"role": "system", "content": "You are a helpful assistant. Give short and clear answers."},
        {"role": "user", "content": user_input}
    ]
)

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {str(e)}"


def main():
    print(" Groq LLM CLI Tool (type 'exit' to quit)\n")

    while True:
        user_input = input("Enter your prompt: ")

        if user_input.lower() == "exit":
            print("Goodbye !")
            break

        response = generate_response(user_input)
        print("\n Response:\n", response, "\n")


if __name__ == "__main__":
    main()