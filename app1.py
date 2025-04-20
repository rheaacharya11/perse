# Claude + Harvard Art Frontend with Integrated Prompt
import os
from flask import Flask, request, render_template_string
from dotenv import load_dotenv
import os
import requests

# Load API key from .env
load_dotenv()
app = Flask(__name__)

HARVARD_API_KEY = os.getenv('HARVARD_API_KEY')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages'
API_URL = 'https://api.harvardartmuseums.org/object'

TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <title>Harvard Art Provenance Story</title>
</head>
<body style="font-family: Arial; margin: 50px;">
    <h1>Harvard Art Museums - Provenance Story Generator</h1>
    <form method="POST">
        <label for="object_id">Enter Object ID:</label>
        <input type="text" name="object_id" required>
        <input type="submit" value="Generate Story">
    </form>

    {% if image_url %}
        <h2>{{ title }} ({{ dated }})</h2>
        <p><strong>Artist:</strong> {{ artist }}<br>
           <strong>Culture:</strong> {{ culture }}<br>
           <strong>Medium:</strong> {{ medium }}</p>
        <img src="{{ image_url }}" alt="Art Image" style="max-width: 600px;">
        <h3>Provenance</h3>
        <p>{{ provenance }}</p>
        <h3>Story</h3>
        <p style="white-space: pre-line;">{{ story }}</p>
    {% elif error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

def fetch_art_data(object_id):
    params = {
        'apikey': HARVARD_API_KEY,
        'q': f'id:{object_id}'
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        records = data.get('records', [])
        if records:
            record = records[0]
            return {
                'image_url': record.get('primaryimageurl'),
                'title': record.get('title'),
                'artist': record['people'][0]['name'] if record.get('people') else 'Unknown',
                'dated': record.get('dated'),
                'culture': record.get('culture'),
                'medium': record.get('medium'),
                'provenance': record.get('provenance')
            }
    return None

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

    try:
        data = response.json()
        print("Claude API Response:", data)  # For debugging

        # Claude v3 format typically returns:
        # {'content': [{'type': 'text', 'text': '...'}]}
        for part in data.get("content", []):
            if part.get("type") == "text":
                return part.get("text")
        return "Claude API responded, but no story was returned."
    except Exception as e:
        print("Error parsing Claude response:", e)
        return f"Error generating story: {e}"



@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = error = title = artist = dated = culture = medium = provenance = story = None

    if request.method == 'POST':
        object_id = request.form['object_id']
        art = fetch_art_data(object_id)
        if art and art['image_url']:
            prompt = create_claude_prompt(art)
            story = call_claude(prompt)
            image_url = art['image_url']
            title = art['title']
            artist = art['artist']
            dated = art['dated']
            culture = art['culture']
            medium = art['medium']
            provenance = art['provenance']
        else:
            error = 'Artwork not found or no image available.'

    return render_template_string(TEMPLATE, image_url=image_url, title=title, artist=artist, dated=dated,
                                  culture=culture, medium=medium, provenance=provenance, story=story, error=error)

if __name__ == '__main__':
    app.run(debug=True)
