import requests
from io import BytesIO

from PIL import Image

import random
from src.utils import pil_to_base64, base64_to_pil, JPEG_QUALITY


def add_frame_on_image(origin_image, origin_frame):
    image = origin_image.copy()
    frame = origin_frame.copy()

    # Подгоним фрейм по ширине
    if frame.width != origin_image.width:
        frame = frame.resize((origin_image.width, int(frame.height*origin_image.width/frame.width)))

    if frame.height > image.height:
        frame = frame.crop((0, frame.height-image.height, frame.width, frame.height))
    elif frame.height < image.height:
        new_frame = Image.new(frame.mode, image.size)
        new_frame.paste(frame, (0, image.height-frame.height))
        frame = new_frame.copy()

    image.paste(frame, (0, 0), mask=frame)

    return image


def prepare_frames():
    frames = []
    frames.append(Image.open('./data/offers-type-has-offers-lamp.png'))
    frames.append(Image.open('./data/offers-type-has-offers-vasiliy.png'))
    frames.append(Image.open('./data/offers-type-has-offers-zebra.png'))

    return frames


def get_photo_from_1c(guid: str):
    url = "https://zumba24.ru/api/zumba24/v1/app/send-data/"
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'API-KEY': '79EQUL46LM4BVJR9'
    }
    payload = {
        'Команда': 'ФотоТовара',
        'guid': guid
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception('Ошибка {}: {} при получении фото {}'.format(response.status_code, response.text, guid))


def get_photo_from_site(guid: str):
    url = "https://zumba24.ru/upload/media/{}-original.jpg".format(guid)
    response = requests.get(url)
    if response.status_code == 200:
        image = BytesIO(response.content)
        return Image.open(image)
    else:
        raise Exception('Фото {} не получено. Ошибка {}'.format(guid, response.status_code))


def load_to_site(image, guid: str):
    url = "https://zumba24.ru/api/zumba24/v1/photos/offers/file/"
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'API-KEY': 'AQ2F7TW3FVU378M56LFM7LHLC9J8M3'
    }
    payload = {
        'Файл': '{}-with-information'.format(guid),
        'base64': pil_to_base64(image, JPEG_QUALITY)
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception('Фото {} не выгружено. Ошибка {}'.format(guid, response.status_code))


def run_add_image_on_frame(data):
    frames = prepare_frames()

    image = get_photo_from_site(data['guid'])
    if base64_to_pil(data['image']).size != image.size:
        raise Exception('На сайте отсутствует свежее фото')
    image = add_frame_on_image(image, frames[random.randint(0, 2)])

    load_to_site(image, data['guid'])

    return pil_to_base64(image)
