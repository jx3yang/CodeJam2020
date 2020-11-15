import numpy as np
import imagehash
import requests
from .utils import get_image_from_url

def compute_hash(img_path):
    return list(imagehash.phash(get_image_from_url(img_path)).hash.astype(int).flatten())

def hamming_distance(a1: np.ndarray, a2: np.ndarray) -> int:
    if (len(a1) == 0 or len(a2) == 0):
        return 64
    return np.count_nonzero(a1 != a2)

def rank(image_hashes, query_hash):
    return [
        { 'image_hash': image_hash, 'distance': hamming_distance(image_hash, query_hash) }
        for image_hash in image_hashes
    ]
