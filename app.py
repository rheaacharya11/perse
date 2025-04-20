from flask import Flask, request, render_template_string
from dotenv import load_dotenv
import os
import requests

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('HARVARD_API_KEY')

app = Flask(__name__)

API_URL = 'https://api.harvardartmuseums.org/object'

TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <title>Harvard Art Image Lookup</title>
</head>
<body style="font-family: Arial; margin: 50px;">
    <h1>Harvard Art Museums - Object Image Lookup</h1>
    <form method="POST">
        <label for="object_id">Enter Object ID:</label>
        <input type="text" name="object_id" required>
        <input type="submit" value="Get Image">
    </form>

    {% if image_url %}
        <h2>Image for Object ID {{ object_id }}</h2>
        <img src="{{ image_url }}" alt="Art Image" style="max-width: 600px;">
    {% elif error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    error = None
    object_id = None

    if request.method == 'POST':
        object_id = request.form['object_id']
        params = {
            'apikey': API_KEY,
            'q': f'id:{object_id}'
        }

        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            if records:
                image_url = records[0].get('primaryimageurl')
                if not image_url:
                    error = 'No image found for this object.'
            else:
                error = 'Object not found.'
        else:
            error = f'API request failed. Status code: {response.status_code}'

    return render_template_string(TEMPLATE, image_url=image_url, object_id=object_id, error=error)

if __name__ == '__main__':
    app.run(debug=True)
