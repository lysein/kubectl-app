import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Helper to explain logs using OpenAI

def explain_logs_with_ai(logs):
    prompt = f"Explain the following Kubernetes pod logs and highlight any errors or issues:\n{logs}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content
