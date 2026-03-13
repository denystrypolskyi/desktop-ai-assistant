import requests

SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"

def ask_llm(prompt: str, max_tokens: int = 1024):
    system_message = (
        "You are Jarvis, a virtual assistant. "
        "You are friendly and polite. "
        "Avoid using unnecessary foreign words, and maintain a friendly tone."
    )

    payload = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    resp = requests.post(SERVER_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()

    choice = data['choices'][0]['message']
    return choice.get('content') or choice.get('reasoning_content') or ""