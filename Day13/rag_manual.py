from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Sample document
document = """
Python is a programming language used for web development, AI, and data science.
Machine learning is a subset of AI that allows systems to learn from data.
Pandas is a Python library used for data analysis and manipulation.
"""

# Step 1: Chunking
chunks = document.split(". ")

def retrieve(query):
    for chunk in chunks:
        if any(word.lower() in chunk.lower() for word in query.split()):
            return chunk
    return chunks[0]


def ask(question):
    context = retrieve(question)

    prompt = f"""
    Answer the question using the context below:
    
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


if __name__ == "__main__":
    q = input("Ask a question: ")
    ask(q)