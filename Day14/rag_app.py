from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load documents
docs = [
    "Python is widely used in AI and automation.",
    "SQL is used for managing databases.",
    "Machine learning models learn from data.",
    "APIs allow communication between systems.",
    "Pandas helps analyze structured data."
]

# Chunking (simple)
chunks = docs


def retrieve(query):
    best_chunk = ""
    max_score = 0

    for chunk in chunks:
        score = sum(word.lower() in chunk.lower() for word in query.split())
        if score > max_score:
            max_score = score
            best_chunk = chunk

    return best_chunk


def ask(question):
    context = retrieve(question)

    prompt = f"""
    Use the context to answer:

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    print("\nAnswer:", response.choices[0].message.content)


def main():
    print(" RAG App (type 'exit')")
    while True:
        q = input("\nAsk: ")
        if q == "exit":
            break
        ask(q)


if __name__ == "__main__":
    main()