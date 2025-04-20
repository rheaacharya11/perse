import requests
import os


# Set up headers with the correct authentication format
headers = {
    'x-api-key': CLAUDE_API_KEY,
    'Content-Type': 'application/json',
    'anthropic-version': '2023-06-01'
}

# Minimal payload for testing
payload = {
    "model": "claude-3-7-sonnet-20250219",
    "max_tokens": 50,
    "messages": [
        {"role": "user", "content": "Say hello!"}
    ]
}

# Make the API request
res = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)

# Check response
print(f"Status code: {res.status_code}")

# Pretty print response if successful, otherwise show the error
if res.status_code == 200:
    print("Success!")
    print(res.json().get("content", []))
else:
    print("Error:")
    print(res.text)