from openai import OpenAI
import json
import os

# print(os.getenv("OPENAI_API_KEY"))
client = OpenAI()  # uses OPENAI_API_KEY from env

def ask_llm(prompt: str, model = "gpt-5-mini") -> dict:
    # model = "gpt-5-mini"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    return {
        "prompt": prompt,
        "answer": response.choices[0].message.content,
        "model": response.model,
        "usage": response.usage.model_dump()
    }

# result = ask_llm("Explain REST APIs in one paragraph.")

# print(json.dumps(result, indent=2))
