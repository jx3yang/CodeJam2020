import pandas as pd
from product_crawlers.settings import AMAZON_OUT_FILE, EBAY_OUT_FILE, IMAGE_HASH_FILE

def clean_price(x, offset):
    if x and not pd.isna(x):
        try:
            return float(x)
        except Exception:
            return float(x[offset:].replace(',', ''))
    return None

def get_amazon_df():
    df = pd.read_csv(AMAZON_OUT_FILE)[['title', 'url', 'image_url', 'price']]
    df['url'] = df['url'].apply(lambda x: f'https://www.amazon.ca{x}')
    df['price'] = df['price'].apply(lambda x: clean_price(x, 5))
    return df

def get_ebay_df():
    df = pd.read_csv(EBAY_OUT_FILE)[['title', 'url', 'image_url', 'price']]
    df['price'] = df['price'].apply(lambda x: clean_price(x, 1))
    return df

def get_image_hash_dict():
    df = pd.read_csv(IMAGE_HASH_FILE)
    return {
        row['url']: eval(row['image_hash']) for _, row in df.iterrows()
    }

if __name__ == '__main__':
    df_amazon, df_ebay, hash_dict = get_amazon_df(), get_ebay_df(), get_image_hash_dict()
    
    df_amazon['image_hash'] = df_amazon['image_url'].apply(lambda x: hash_dict.get(x))
    df_ebay['image_hash'] = df_ebay['image_url'].apply(lambda x: hash_dict.get(x))

    df_amazon['company'] = 'Amazon'
    df_ebay['company'] = 'Ebay'

    pd.concat([df_amazon, df_ebay]).to_csv('output/final.csv', index=False)
