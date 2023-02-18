import json
import random
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
data = None
PEXELS_API_KEY = ''

with open('data.json') as f:
    data = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        chapter = request.form.get('chapter')
    else:
        chapter = random.choice(list(data.keys()))
        
    words = data[chapter]
    englishWord = random.choice(words)['English']
    latinWord = None
    for word in words:
        if word['English'] == englishWord:
            latinWord = word['Latin']
            break

    # Get 12 images from Pexels using the English word as a search term
    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': englishWord, 'per_page': 12}  # Get 12 photos instead of 1
    response = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()['photos']
        if results:
            photo_data = []
            for result in results:
                photo_url = result['src']['medium']
                photo_photographer = result['photographer']
                photo_photographer_url = result['photographer_url']
                photo_data.append((photo_url, photo_photographer, photo_photographer_url))
        else:
            photo_data = None
    else:
        photo_data = None

    return render_template('display.html', chapter=chapter, englishWord=englishWord, latinWord=latinWord, photo_data=photo_data, chapters=list(data.keys()))

if __name__ == '__main__':
    app.run(debug=True)
