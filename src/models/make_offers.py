import requests
import random
from glob import glob
from io import BytesIO
from typing import Dict

from PIL import Image
from src.utils import pil_to_base64, JPEG_QUALITY


def add_frame_on_image(origin_image, offer):
    image = origin_image.copy()

    # Если есть несколько вариантов шильдиков, выбираем из них
    frames = glob('./data/offers-qty-{}-{}-*.png'.format(offer['count'], offer['type']))
    if len(frames):
        frame = frames[random.randint(0, len(frames)-1)]
    else:
        frame = './data/offers-qty-{}-{}.png'.format(offer['count'], offer['type'])
    frame = Image.open(frame)

    # Подгоним фрейм по ширине
    if frame.width != origin_image.width:
        frame = frame.resize((origin_image.width, int(frame.height * origin_image.width / frame.width)))

    if frame.height > image.height:
        frame = frame.crop((0, frame.height - image.height, frame.width, frame.height))
    elif frame.height < image.height:
        new_frame = Image.new(frame.mode, image.size)
        new_frame.paste(frame, (0, image.height - frame.height))
        frame = new_frame.copy()

    image.paste(frame, (0, 0), mask=frame)

    return image


def get_photo_from_site(guid: str):
    url = "https://zumba24.ru/upload/media/{}-original.jpg".format(guid)
    response = requests.get(url)
    if response.status_code == 200:
        image = BytesIO(response.content)
        return Image.open(image)
    else:
        raise Exception('Фото {} не получено. Ошибка {}'.format(guid, response.status_code))


def load_to_site(image, offer: Dict):
    url = "https://zumba24.ru/api/zumba24/v1/photos/offers/file/"
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'API-KEY': 'AQ2F7TW3FVU378M56LFM7LHLC9J8M3'
    }
    payload = {
        'Файл': '{}-{}'.format(offer['guid'], offer['type']),
        'base64': pil_to_base64(image, JPEG_QUALITY)
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception('Фото {} не выгружено. Ошибка {}'.format(offer['guid'], response.status_code))


def make_offers(data):

    offers = []
    main_image = get_photo_from_site(data['guid'])
    for offer in data['offers']:
        image = add_frame_on_image(main_image, offer)
        load_to_site(image, offer)

        offers.append(
            {
                'image': pil_to_base64(image, JPEG_QUALITY),
                'guid': offer['guid'],
                'count': offer['count'],
            }
        )

    return offers
