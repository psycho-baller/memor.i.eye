import boto3
import time
import json
import requests

from PIL import Image
import base64
from io import BytesIO


def upload_img(image, fixation_point, fixating_time):
    # # upload to s3
    # path = f'/home/james/Dev/htn/eyes/app/fixations/{file_name}.jpg'

    # s3_bucket_name = 'eyes-htn'

    # client = boto3.client('s3', region_name='us-west-2',
    #                       aws_access_key_id='...',
    #                       aws_secret_access_key='...'
    #                       )

    # client.upload_file(path, s3_bucket_name, f'{file_name}.jpg')

    # ###########

    # # ping local server
    # image = Image.open(path)
    # buffered = BytesIO()
    # image.save(buffered, format="JPEG")

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    # url = 'https://b808-2620-101-f000-700-ba91-69c3-c3d3-7100.ngrok.io/upload'
    url = 'http://20.25.130.61/test_photo'
    params = {
        # 'url': f'https://eyes-htn.s3.us-east-2.amazonaws.com/{file_name}.jpg',
        # 'url': f'https://eyes-htn.s3.us-east-2.amazonaws.com/{file_name}.jpg',
        'time': time.time(),
        'gaze_x': int(fixation_point[0]),
        'gaze_y': int(fixation_point[1]),
        'fixating_time': fixating_time,
        'latitude': 0,
        'longitude': 0,
    }

    # data = {
    #     'image': image,
    # }

    x = requests.post(url, data=image, headers=headers, params=params)
    return x
