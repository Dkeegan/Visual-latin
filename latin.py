import os
import requests
from flask import Flask, render_template, request
import random
import json

app = Flask(__name__)

PEXELS_API_KEY = os.getenv()  # Get your API key from https://www.pexels.com/api/

with open('data.json') as f:
    data = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def display_data():
    # Select a random word from the data
    random_word = random.choice(data)
    english_word = random_word['English']
    latin_word = random_word['Latin']
    derivative_word = random_word['Derivative']

    # Use the Pexels API to search for photos related to the English word
    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': english_word, 'per_page': 12}  # Get 12 photos instead of 1
    response = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()['photos']
        if results:
            photo_data = []
            for result in results:
                photo_url = result['src']['large']
                photo_photographer = result['photographer']
                photo_photographer_url = result['photographer_url']
                photo_data.append((photo_url, photo_photographer, photo_photographer_url))
        else:
            photo_data = None
    else:
        photo_data = None

    return render_template('display.html', english=english_word, latin=latin_word, derivative=derivative_word, photo_data=photo_data)

if __name__ == '__main__':
    app.run(debug=True)
