import json
import os
import urllib.request

def run_model(prompt: str):
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        response = json.loads(resp.read().decode("utf-8"))
    return response["choices"][0]["message"]["content"]