# app.py — Flask App for Visual Art Provenance Storytelling

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# === CONFIG ===
HARVARD_API_KEY = 'YOUR_HARVARD_API_KEY'
CLAUDE_API_KEY = 'YOUR_CLAUDE_API_KEY'
CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages'

# === HELPERS ===
def fetch_art_data(title):
    params = {
        'apikey': HARVARD_API_KEY,
        'title': title,
        'size': 1,
        'hasimage': 1
    }
    r = requests.get('https://api.harvardartmuseums.org/object', params=params)
    data = r.json()
    if not data['records']:
        return None
    record = data['records'][0]
    return {
        'image_url': record.get('primaryimageurl'),
        'title': record.get('title'),
        'artist': record['people'][0]['name'] if record.get('people') else 'Unknown',
        'dated': record.get('dated'),
        'culture': record.get('culture'),
        'medium': record.get('medium'),
        'provenance': record.get('provenance')
    }

def create_claude_prompt(art):
    return f"""
You are an art historian and creative storyteller.

Here is an image of an artwork from the Harvard Art Museums: {art['image_url']}

Title: {art['title']}
Artist: {art['artist']}
Date: {art['dated']}
Culture: {art['culture']}
Medium: {art['medium']}

Provenance: {art['provenance']}

Please tell me a vivid and historically grounded story about the artwork — how it might have been created, who owned it, and what it has seen. Use the provenance details as anchors in the timeline, but feel free to interpret and imagine. Capture the emotional resonance, cultural shifts, and the significance of each chapter in the painting’s journey.

End with a reflection on what the painting means now, and what it might be thinking as it hangs in the Harvard Art Museums.
"""

def call_claude(prompt):
    headers = {
        'Authorization': f'Bearer {CLAUDE_API_KEY}',
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01'
    }
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=payload)
    return response.json()['content'][0]['text']

# === ROUTES ===
@app.route('/', methods=['GET', 'POST'])
def index():
    story = None
    art = None
    if request.method == 'POST':
        title = request.form['title']
        art = fetch_art_data(title)
        if art:
            prompt = create_claude_prompt(art)
            story = call_claude(prompt)
    return render_template('index.html', art=art, story=story)

if __name__ == '__main__':
    app.run(debug=True)
