from flask import Flask, render_template, jsonify, request
import json
import os
import random

app = Flask(__name__)

def load_words():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    words_file = os.path.join(script_dir, "words.json")
    try:
        with open(words_file, 'r') as file:
            data = json.load(file)
            return [word.lower() for word in data.values()]
    except Exception as e:
        print(f"Error loading words: {e}")
        return []

WORDS = load_words()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/word')
def get_word():
    if WORDS:
        return jsonify({'word': random.choice(WORDS)})
    return jsonify({'error': 'No words available'}), 500

@app.route('/api/find', methods=['POST'])
def find_words():
    data = request.json
    correct_letters = data.get('correctLetters', [])
    misplaced_letters = data.get('misplacedLetters', [])
    excluded_letters = data.get('excludedLetters', [])
    
    possible_words = WORDS.copy()
    
    for letter_info in correct_letters:
        possible_words = [word for word in possible_words 
                         if word[letter_info['position']] == letter_info['letter']]
    
    for letter_info in misplaced_letters:
        possible_words = [word for word in possible_words 
                         if letter_info['letter'] in word 
                         and word[letter_info['position']] != letter_info['letter']]
    
    for letter in excluded_letters:
        possible_words = [word for word in possible_words if letter not in word]
    
    return jsonify({'words': possible_words[:100]})

if __name__ == '__main__':
    app.run(debug=True)
