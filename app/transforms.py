from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from flask import jsonify
import cv2
import numpy as np

import base64
from io import BytesIO


def convert_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("UTF-8")


def fix_pdf(data):
    stream = BytesIO(data)

    pdf_reader = PdfReader(stream)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    buffered = BytesIO()
    pdf_writer.write(buffered)

    buffered = base64.b64encode(buffered.getvalue()).decode("UTF-8")

    return jsonify({'pdf': buffered})


def pdf_to_jpg(data):

    try:
        images = convert_from_bytes(data)
        pictures = [im.crop((0, 0, im.size[0], im.size[1]//2)) for im in images]
        return jsonify([{'picture': convert_to_base64(im)} for im in pictures])

    except Exception as exc:
        description_error = f'не получилось преобразовать pdf в jpg: {str(exc)}'
        return jsonify({'error': description_error})


def resize(data):

    img = base64.b64decode(data['image'])
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)

    height, width = img.shape[:2]

    if height/width > data['height']/data['width']:
        ratio = data['height']/height
        new_height = data['height']
        new_width = int(width * ratio)
    else:
        ratio = data['width']/width
        new_height = int(height * ratio)
        new_width = data['width']

    img = cv2.resize(img, (new_width, new_height))
    new_image = np.zeros((data['height'], data['width'], 3), dtype=np.uint8)
    new_image += 255

    if new_width == data['width']:
        start_point = (data['height']-new_height)//2
        new_image[start_point:start_point+new_height, ...] = img
    else:
        start_point = (data['width']-new_width)//2
        new_image[:, start_point:start_point+new_width, :] = img

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]

    result, imgencode = cv2.imencode(".jpg", new_image, encode_param)
    img_data = base64.b64encode(imgencode).decode("UTF-8")

    return jsonify({'image': img_data})
