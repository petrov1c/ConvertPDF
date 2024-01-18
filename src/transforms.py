from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from flask import jsonify

import cv2
import numpy as np

import base64
from io import BytesIO
from src import utils


def fix_pdf(data, mode='to_jpg'):
    pdf_writer = PdfWriter()
    if mode == 'to_jpg':
        images = convert_from_bytes(data, grayscale=True)
        for image in images:
            buffered = BytesIO()
            image.save(buffered, format="pdf")

            pdf_reader = PdfReader(buffered)
            pdf_writer.append_pages_from_reader(pdf_reader)
    else:
        stream = BytesIO(data)
        pdf_reader = PdfReader(stream)
        pdf_writer.append_pages_from_reader(pdf_reader)

    buffered = BytesIO()
    pdf_writer.write(buffered)

    buffered = base64.b64encode(buffered.getvalue()).decode("UTF-8")

    return jsonify({'pdf': buffered})


def pdf_to_jpg(data):
    try:
        images = convert_from_bytes(data)
        pictures = [im.crop((0, 0, im.size[0], im.size[1]//2)) for im in images]
        return jsonify([{'picture': utils.pil_to_base64(im)} for im in pictures])
    except Exception as exc:
        description_error = f'не получилось преобразовать pdf в jpg: {str(exc)}'
        return jsonify({'error': description_error})


def resize(data):
    img = utils.base64_cv2(data['image'])

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

    img_data = utils.cv2_base64(new_image)
    return jsonify({'image': img_data})


def delete_background(data):
    image = utils.base64_cv2(data['image'])
    new_image = utils.delete_background(image)

    return jsonify({'image': utils.cv2_base64(new_image)})


def super_resolution(data):
    image = utils.base64_cv2(data['image'])
    new_image = utils.super_resolution(image)

    return jsonify({'image': utils.cv2_base64(new_image)})


def get_quality(data):
    image = utils.base64_cv2(data['image'])
    quality = utils.get_quality(image)

    return jsonify({'quality': quality})


def pipeline(data):
    image = utils.base64_cv2(data['image'])
    image = utils.delete_background(image, threshold=data['background_threshold'])
    image = utils.super_resolution(image)
    width = image.shape[1]
    height = image.shape[0]
    if 'resize_width' in data and width > data['resize_width']:
        new_width = data['resize_width']
        new_height = int(new_width/width*height)
        image = cv2.resize(np.asarray(image), (new_width, new_height), interpolation=cv2.INTER_AREA)

    return jsonify(
        {
            'image': utils.cv2_base64(image),
            'quality': utils.get_quality(image),
            'guid': data['guid'],
        }
    )
