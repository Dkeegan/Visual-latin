import json
import random
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
data = None
PEXELS_API_KEY = ''

def load_data():
    with open('chapterSortedSortedSentences.json',  encoding='utf-8') as f:
        return json.load(f)

def get_random_english_word(chapter):
    words = data[chapter]
    #print (words)
    return random.choice(words)['English']

def get_latin_word(chapter, english_word):
    words = data[chapter]
    for word in words:
        if word['English'] == english_word:
            return word['Latin'],word['type']

def get_latin_sentence(chapter, english_word):
    words = data[chapter]
    for word in words:
        if word['English'] == english_word:
            print(len(word['sentences']))
            return word['sentences']

def get_photo_data(english_word):
    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': english_word, 'per_page': 12}
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
            return photo_data
        else:
            return None
    else:
        return None

data = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        chapter = request.form.get('chapter')
    else:
        chapter = list(data.keys())[0]
        
        
    englishWord = get_random_english_word(chapter)
    latinWord, latin_word_type = get_latin_word(chapter, englishWord)
    latinsentence = get_latin_sentence(chapter, englishWord)
    if latinsentence:
        latinsentence = random.choice(latinsentence)
    else:
        latinsentence = ''
    #photo_data = get_photo_data(englishWord)
    photo_data = []

    return render_template('display.html', chapter=chapter, englishWord=englishWord, latinWord=latinWord,latin_word_type=latin_word_type, latinsentence=latinsentence, photo_data=photo_data, chapters=list(data.keys()))

if __name__ == '__main__':
    app.run(debug=True)
