"""
Most code from https://colab.research.google.com/drive/1Tc9vCcajKGlmnyUwfkQIjOHJdMay9EUB?usp=sharing
"""

import base64
import json
from io import BytesIO

import imgaug as ia
import numpy as np
import pandas as pd
import requests
from PIL import Image

from .utils import get_image_from_url

ID_TO_CLASSES = {
    1: 'Shirt',
    9: 'Skirt'
}

class ImageByteEncoder:
    """Class that provides functionalities to encode an image to bytes and
    decode back to image
    """

    def encode(self, img):
        """Encode

        Arguments:
            img {Image} -- PIL Image to be encode

        Returns:
            str -- image encoded as a string
        """
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        img_bytes = base64.b64encode(img_bytes).decode('utf8')
        return img_bytes

    def decode(self, img_str):
        """Decode

        Arguments:
            img_str {str} -- Image str as encoded by self.encode

        Returns:
            Image -- PIL Image
        """
        img_bytes = bytes(img_str, encoding='utf8')
        img_bytes = base64.b64decode(img_bytes)
        img = Image.open(BytesIO(img_bytes))
        return img


class Segmenter:
    def __init__(self):
        self.inference_url = 'https://models.samasource.com/fashion-seg/invocations'
        self.encoder = ImageByteEncoder()

    def _predict(self, req_json):
        # Request
        response = requests.post(
            url=self.inference_url,
            data=req_json,
            headers={ "Content-Type": "application/json" }
        )
        response = json.loads(response.text)[0]

        # Decode the seg info
        seg_str = response['Mask']
        id_to_class = json.loads(response['Mapping'])
        seg = self.encoder.decode(seg_str)
        return seg, id_to_class

    def predict_on_image(self, img):
        # Encode image as Byte String
        img_str = self.encoder.encode(img)

        # Create json request for the service according to pandas schema
        req_df = pd.DataFrame({'Image': [img_str]})
        req_json = req_df.to_json(orient='split')
        return self._predict(req_json)

    def predict_on_url(self, url):
        # Create json request for the service according to pandas schema
        req_df = pd.DataFrame({'Image_url': [url]})
        req_json = req_df.to_json(orient='split')
        return self._predict(req_json)

def segment_clothes(segmenter, image_url):
    image = get_image_from_url(image_url)
    img = np.array(image)
    segmap, id_to_class = segmenter.predict_on_image(image)
    segmap = np.array(segmap)
    print(id_to_class)
    _ids = [_id for _id in ID_TO_CLASSES if str(_id) in id_to_class]

    def extract(_id):
        seg = np.array(segmap)
        seg[seg != _id] = 0
        seg[seg == _id] = 1
        portion = np.array(img)
        for z in range(3):
            portion[:,:,z] = np.multiply(portion[:,:,z], seg)
        portion[portion == 0] = 255
        return portion

    return [
        { 'name': ID_TO_CLASSES[_id], 'image': extract(_id) } for _id in _ids
    ]
