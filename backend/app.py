import json
import os

import numpy as np
import pandas as pd
from flask import Flask, request, send_from_directory
from flask_cors import CORS

from api.image_rank import compute_hash
from api.image_rank import rank as image_rank
from api.text_rank import rank as text_rank
from api.text_rank import tokenize, tokenize_corpus

app = Flask(__name__)
PORT = 5000
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads')
cors = CORS(app)

def eval_hash(img_hash):
    if isinstance(img_hash, float):
        return np.array([])
    return np.array(eval(img_hash))

all_data = pd.read_csv('final.csv')
all_data['image_hash'] = all_data['image_hash'].apply(eval_hash)

corpus = list(all_data['title'])
bm25 = tokenize_corpus(corpus)

@app.route('/')
def ping():
    return json.dumps({ 'success': True })

@app.route('/upload', methods=['POST'])
def upload():
    if request.files:
        image = request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        return json.dumps({
            'success': True,
            'image_path': f'http://localhost:{PORT}/dir/{image.filename}'
        })
    return json.dumps({
        'success': False
    })

@app.route('/dir/<path:path>', methods=['GET'])
def serve(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)

@app.route('/image_search')
def image_search():
    data = request.get_json(force=True)
    img_hash = compute_hash(data.get('image_path'))
    ranks = image_rank(data['image_hash'], img_hash)
    top20 = {
        x['image_hash']: x['distance'] for x in sorted(ranks, key=lambda x: x['distance'])[:20]
    }

    top_data = [
        {
            'url': row['url'],
            'title': row['title'],
            'image_url': row['image_url'],
            'price': row['price'],
            'company': row['company'],
            'distance': top20.get(row['image_hash'])
        }
        for _, row in all_data[all_data.image_hash.isin(top20)].iterrows()
    ]

    return json.dumps({
        'success': True,
        'data': top_data
    })

@app.route('/text_search')
def text_search():
    data = request.get_json(force=True)
    query = data.get('query')
    top20 = set(text_rank(bm25, corpus, query, 20))

    top_data = [
        {
            'url': row['url'],
            'title': row['title'],
            'price': row['price'],
            'company': row['company']
        }
        for _, row in all_data[all_data.title.isin(top20)].iterrows()
    ]

    return json.dumps({
        'success': True,
        'data': top_data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
