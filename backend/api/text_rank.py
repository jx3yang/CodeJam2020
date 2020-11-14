import re
import functools
from rank_bm25 import BM25Okapi

def tokenize(text: str) -> str:
    replacements = [
        {
            'pattern': r'\(|\)|\[|\]|\&|\,| \- |\/|\<|\>',
            'target': ' '
        },
        {
            'pattern': r'\'|\-|\.',
            'target': ''
        }
    ]
    text = text.lower()
    for replacement in replacements:
        text = re.sub(replacement.get('pattern'), replacement.get('target'), text)
    return text

def tokenize_corpus(corpus):
    return BM25Okapi(
        [tokenize(entry) for entry in corpus]
    )

def rank(bm25, corpus, query, n):
    return bm25.get_top_n(tokenize(query), corpus, n=n)
