from PIL import Image
from io import BytesIO
import requests


def get_image_from_url(img_url):
    return Image.open(
        BytesIO(requests.get(img_url).content)
    )
