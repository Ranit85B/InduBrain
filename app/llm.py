from gemini_client import client


def generate_answer(question, context):
    prompt = f"""
You are an industrial knowledge assistant.

Answer the user's question using only the provided context.

If the answer is not available in the context, say:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
     model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text