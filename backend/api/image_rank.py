import numpy as np
import imagehash
from PIL import Image
from io import BytesIO

def compute_hash(img_path):
    return list(imagehash.phash(Image.open(BytesIO(response.body))).hash.astype(int).flatten())

def hamming_distance(a1: np.ndarray, a2: np.ndarray) -> int:
    return np.count_nonzero(a1 != a2)

def rank(image_hashes, query_hash):
    return [
        { 'image_hash': image_hash, 'distance': hamming_distance(image_hash, query_hash) }
        for image_hash in image_hashes
    ]
