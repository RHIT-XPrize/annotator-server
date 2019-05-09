import requests
import json
import base64
from PIL import Image
import cv2
import io
import numpy as np


class ImageLoader():
    def send_post_request(self, url, payload = {}):
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()

    def load_image(self):
        raise NotImplemented('Image loaders must implement `load image` method')

class KinectImageLoader(ImageLoader):
    HOST_NAME = 'localhost'
    PORT = '56814'
    ROUTE = 'api/StereoCalibrate'
    SOURCE_URL = 'http://' + HOST_NAME + ':' + PORT + '/' + ROUTE

    def load_image(self):
        response_json = self.send_post_request(self.SOURCE_URL)
        encoded_img_str = response_json['EncodedImage']
        width = int(response_json['ImageWidth'])
        height = int(response_json['ImageHeight'])

        img_data = base64.b64decode(encoded_img_str)
        stream = io.BytesIO(img_data)
        img = Image.open(stream)
        img.save('test.png')
        return img
