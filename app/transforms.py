from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from flask import jsonify

import base64
from io import BytesIO


def convert_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("UTF-8")


def fix_pdf(data):
    pdf_reader = PdfReader(data)
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
        pictures = [im.crop((0, 0, im.size[0], im.size[1])) for im in images]
        return jsonify([{'picture': convert_to_base64(im)} for im in pictures])

    except Exception as exc:
        description_error = f'не получилось преобразовать pdf в jpg: {str(exc)}'
        return jsonify({'error': description_error})
