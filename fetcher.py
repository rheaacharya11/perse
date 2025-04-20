import requests

# Replace with your actual Harvard Art Museums API key
API_KEY = 'your_api_key_here'

# Base URL for the objects endpoint
BASE_URL = 'https://api.harvardartmuseums.org/object'

# Define query parameters
params = {
    'apikey': API_KEY,
    'size': 5,           # Number of results to return
    'hasimage': 1        # Only return objects that have images
}

# Make the API request
response = requests.get(BASE_URL, params=params)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    for obj in data['records']:
        print(f"Title: {obj.get('title')}")
        print(f"Object ID: {obj.get('id')}")
        print(f"Image URL: {obj.get('primaryimageurl')}")
        print(f"Culture: {obj.get('culture')}")
        print('-' * 40)
else:
    print(f"Error: {response.status_code}")
