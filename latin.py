import json
import random
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
data = None
PEXELS_API_KEY = ''
WIKIPEDIA_API_URL = 'https://en.wikipedia.org/w/api.php'

def load_data():
    with open('parsed_latin.json',  encoding='utf-8') as f:
        return json.load(f)

def get_random_english_word(chapter):
    words = data[chapter]
    word = random.choice(words)
    print (word)
    return random.choice(words)['english']

def get_latin_word(chapter, english_word):
    words = data[chapter]
    for word in words:
        if word['english'] == english_word:
            return word['latin'],word['type']

def get_latin_sentence(chapter, english_word):
    words = data[chapter]
    for word in words:
        if word['english'] == english_word:
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
def get_wikipedia_photos(english_word):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'images',
        'titles': english_word
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params).json()
    page_id = list(response['query']['pages'].keys())[0]
    image_info = response['query']['pages'][page_id].get('images', [])
    image_titles = [image['title'] for image in image_info if 'File:' in image['title'] and not image['title'].endswith('.svg')]
    image_urls = []
    for image_title in image_titles:
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'imageinfo',
            'iiprop': 'url',
            'titles': image_title
        }
        response = requests.get(WIKIPEDIA_API_URL, params=params).json()
        page_id = list(response['query']['pages'].keys())[0]
        image_info = response['query']['pages'][page_id].get('imageinfo', [])
        image_urls.extend([info['url'] for info in image_info])
    return image_urls


data = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        chapter = request.form.get('chapter')
    else:
        chapter = list(data.keys())[0]
        
    englishWord = get_random_english_word(chapter)
    photo = random.choice(englishWord) # select one element from the list
    print(type(englishWord))
    print(englishWord)
    print(type(photo))
    print(photo)
    latinWord, latin_word_type = get_latin_word(chapter, englishWord)
    latinsentence = get_latin_sentence(chapter, englishWord)
    if latinsentence:
        latinsentence = random.choice(latinsentence)
    else:
        latinsentence = ''
    
    wiki_photos = get_wikipedia_photos(photo)

    #photo_data = get_photo_data(photo)
    photo_data = []
    
    return render_template('index.html', chapter=chapter, englishWord=englishWord, latinWord=latinWord,latin_word_type=latin_word_type, latinsentence=latinsentence, photo_data=photo_data,wiki_photos=wiki_photos,chapters=list(data.keys()))

if __name__ == '__main__':
    app.run(debug=True)
