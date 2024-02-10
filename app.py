from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')
db = client['your-database-name']
products_collection = db['products']  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate_and_search', methods=['POST'])
def translate_and_search():
    data = request.get_json()
    indic_text_input = data.get('indic_text_input', '')
    english_translation = translate_to_english(indic_text_input)
    backend_processing_result = process_backend(english_translation)

    matched_products = search_products(english_translation)

    indic_output = translate_to_indic(backend_processing_result)
    return jsonify({
        'indic_text_input': indic_text_input,
        'english_translation': english_translation,
        'backend_processing_result': backend_processing_result,
        'indic_output': indic_output,
        'matched_products': matched_products
    })

def translate_to_english(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def process_backend(text):
    return f"Processed: {text}"

def translate_to_indic(text, source_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=source_language)
    return translation.text

def search_products(query):
    
    result = products_collection.find({'name': {'$regex': f'.*{query}.*', '$options': 'i'}})
    return list(result)

if __name__ == "__main__":
    app.run(debug=True)
