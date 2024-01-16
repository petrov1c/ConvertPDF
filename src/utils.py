import base64
from io import BytesIO
from typing import Optional

import cv2
import numpy as np
import cpbd

from src.models.srgan import SRGAN

# Важно, PIL по умолчанию сохраняет jpg с 75% качеством, cv2 с 95%.
# Надо по умолчанию сохранять с 95. 100% качество ставить не надо, так как при этом отключаются некоторые функции сжатия
# и мы получаем просто файл большого размера
JPEG_QUALITY = 95


def delete_background(image: np.ndarray, threshold: int = 245) -> np.ndarray:

    # Надо получить маску и обрезать по маске, так как на фотках не всегда чисто белый цвет
    new_image = np.array(image)

    mask = cv2.cvtColor(new_image, cv2.COLOR_RGB2GRAY)
    mask = mask > threshold

    for idx in range(1, mask.shape[0]):
        if not np.all(mask[idx]):
            mask = mask[idx-1:]
            new_image = new_image[idx-1:]
            break

    height = mask.shape[0]
    for idx in range(1, height):
        if not np.all(mask[height-idx]):
            mask = mask[:height-idx+1]
            new_image = new_image[:height-idx+1]
            break

    for idx in range(1, mask.shape[1]):
        if not np.all(new_image[:, idx]):
            mask = mask[:, idx - 1:]
            new_image = new_image[:, idx-1:]
            break

    width = mask.shape[1]
    for idx in range(1, width):
        if not np.all(new_image[:, width-idx]):
            mask = mask[:, :width - idx + 1]
            new_image = new_image[:, :width-idx+1]
            break

    return new_image


def pil_to_base64(pil_img, quality: int = JPEG_QUALITY):
    # PIL по умолчанию сохраняет с 75% качеством,
    # чтобы сохранить картинку как есть и при этом использовать сжатие jpeg надо сохранять с 95%
    img_buffer = BytesIO()
    pil_img.save(img_buffer, format='JPEG', quality=quality)
    byte_data = img_buffer.getvalue()

    return base64.b64encode(byte_data).decode("UTF-8")


def base64_cv2(data):
    image = base64.b64decode(data)
    return cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)


def cv2_base64(cv2_img, quality: int = JPEG_QUALITY):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, img_encode = cv2.imencode(".jpg", cv2_img, encode_param)

    return base64.b64encode(img_encode).decode("UTF-8")


def super_resolution(image, resize_width: Optional[int] = None):
    srgan = SRGAN()
    sr_image = srgan(image)
    if isinstance(resize_width, int) and sr_image.width > resize_width:
        resize_height = int(resize_width/sr_image.width*sr_image.height)
        sr_image = cv2.resize(np.asarray(sr_image), (resize_width, resize_height), interpolation=cv2.INTER_AREA)
    else:
        sr_image = np.array(sr_image)

    return sr_image


def get_quality(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    return cpbd.compute(image)
