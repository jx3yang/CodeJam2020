import json
import os

import numpy as np
import pandas as pd
from PIL import Image
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import time

from api.image_rank import compute_hash
from api.image_rank import rank as image_rank
from api.text_rank import rank as text_rank
from api.text_rank import tokenize, tokenize_corpus
from api.segmentation import Segmenter, segment_clothes

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

shuffled = all_data.sample(frac=1)
nums_per_page = 50

corpus = list(all_data['title'])
bm25 = tokenize_corpus(corpus)

segmenter = Segmenter()

@app.route('/')
def ping():
    return { 'success': True }

def get_save_file_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

def upload_image():
    image = request.files['file']
    filename = f'{int(time.time())}-{image.filename}'
    image.save(get_save_file_path(filename))
    return filename

def get_file_path(filename):
    return f'http://localhost:{PORT}/dir/{filename}'

@app.route('/upload', methods=['POST'])
def upload():
    if request.files:
        filename = upload_image()
        return {
            'success': True,
            'imagePath': get_file_path(filename)
        }
    return {
        'success': False
    }

@app.route('/segment', methods=['POST'])
def segment():
    if request.files:
        filename = upload_image()
        image_path = get_file_path(filename)
        segments = segment_clothes(segmenter, image_path)

        def get_segment_file(name, image):
            im = Image.fromarray(image)
            ts = int(time.time())
            fn = f'{ts}-{name}.jpg'
            im.save(get_save_file_path(fn))
            return get_file_path(fn)

        return {
            'success': True,
            'imagePath': get_file_path(filename),
            'segments': [
                { 'name': clothe_segment['name'], 'imageUrl': get_segment_file(clothe_segment['name'], clothe_segment['image']) }
                for clothe_segment in segments
            ]
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

@app.route('/products')
def get_products():
    page = request.args.get('page', default = 1, type = int)
    product_slice = shuffled.iloc[(page-1) * nums_per_page:page * nums_per_page]
    return {
        'success': True,
        'data': [
            {
                'url': url,
                'title': title,
                'price': '' if pd.isna(price) else price,
                'imageUrl': '' if pd.isna(image_url) else image_url,
                'company': company
            }
            for url, title, price, image_url, company
            in zip(product_slice['url'], product_slice['title'], product_slice['price'], product_slice['image_url'], product_slice['company'])
        ],
        'total': len(shuffled),
        'size': nums_per_page
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
