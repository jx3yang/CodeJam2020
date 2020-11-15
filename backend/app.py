import json
import os

import numpy as np
import pandas as pd
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import time

from api.image_rank import compute_hash
from api.image_rank import rank as image_rank
from api.text_rank import rank as text_rank
from api.text_rank import tokenize, tokenize_corpus

app = Flask(__name__)
PORT = 5000
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads')
cors = CORS(app)

top_n = 5
distance_threshold = 15

def eval_hash(img_hash):
    if isinstance(img_hash, float):
        return np.array([])
    return np.array(eval(img_hash))

def hash_to_int(img_hash_array):
    result = 0
    for index, bit in enumerate(reversed(img_hash_array)):
        result += bit * 2**index
    return result

all_data = pd.read_csv('final.csv')
all_data = all_data[pd.notna(all_data['image_url'])]
all_data['image_hash'] = all_data['image_hash'].apply(eval_hash)
all_data['int_hash'] = all_data['image_hash'].apply(hash_to_int)

corpus = list(all_data['title'])
bm25 = tokenize_corpus(corpus)

@app.route('/')
def ping():
    return { 'success': True }

@app.route('/upload', methods=['POST'])
def upload():
    if request.files:
        image = request.files['file']
        filename = f'{int(time.time())}-{image.filename}'
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {
            'success': True,
            'imagePath': f'http://localhost:{PORT}/dir/{filename}'
        }
    return {
        'success': False
    }

@app.route('/dir/<path:path>', methods=['GET'])
def serve(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)

@app.route('/image_search', methods=['POST'])
def image_search():
    data = request.get_json(force=True)
    img_hash = compute_hash(data.get('imagePath'))
    ranks = image_rank(all_data['image_hash'], img_hash)
    top_results = {
        hash_to_int(x['image_hash']): x['distance']
        for x in sorted(ranks, key=lambda x: x['distance']) if x['distance'] <= distance_threshold
    }

    top_data = [
        {
            'url': row['url'],
            'title': row['title'],
            'imageUrl': '' if pd.isna(row['image_url']) else row['image_url'],
            'price': '' if pd.isna(row['price']) else row['price'],
            'company': row['company'],
            'distance': top_results.get(row['int_hash'])
        }
        for _, row in all_data[all_data.int_hash.isin(top_results)].iterrows()
    ]

    return {
        'success': True,
        'data': top_data
    }

@app.route('/text_search', methods=['POST'])
def text_search():
    data = request.get_json(force=True)
    query = data.get('query')
    top_results = set(text_rank(bm25, corpus, query, top_n))

    top_data = [
        {
            'url': row['url'],
            'title': row['title'],
            'price': '' if pd.isna(row['price']) else row['price'],
            'imageUrl': '' if pd.isna(row['image_url']) else row['image_url'],
            'company': row['company']
        }
        for _, row in all_data[all_data.title.isin(top_results)].iterrows()
    ]

    return {
        'success': True,
        'data': top_data
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
