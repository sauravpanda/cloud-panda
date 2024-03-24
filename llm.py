import os
from litellm import completion


def generate_llm_resp(PROMPT):
    messages = [
        {"role": "system", "content": "You are an expert Python Software developer helping other review, document and improve codes."},
        {"role": "user", "content": PROMPT}
    ]
    response = completion(model="claude-3-opus-20240229", messages=messages, max_tokens=4000)
    return response["choices"][0]["message"]["content"]