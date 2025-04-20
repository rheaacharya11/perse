import requests

CLAUDE_API_KEY = "your_claude_api_key_here"

headers = {
    'x-api-key': CLAUDE_API_KEY,
    'Content-Type': 'application/json',
    'anthropic-version': '2023-06-01'
}

payload = {
    "model": "claude-3-opus-20240229",
    "max_tokens": 50,
    "messages": [
        {"role": "user", "content": "Say hello!"}
    ]
}

res = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
print(res.status_code)
print(res.json())
