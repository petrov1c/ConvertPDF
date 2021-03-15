from pdf2image import convert_from_bytes
from flask import jsonify

from PIL import Image

import base64
from io import BytesIO

def PILtoBase64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("UTF-8")

def pdf_to_jpg(data):

    fault = False
    descriptionError = ''

    try:
        images = convert_from_bytes(data)
    except Exception as exc:
        fault = True
        descriptionError = 'не получилось преобразовать pdf в jpg'+  str(exc)

    if not fault:

        pictures = [im.crop((0, 0, im.size[0], im.size[1]/2)) for im in images]
        return jsonify([{'picture': PILtoBase64(im)} for im in pictures])
    else:
        return jsonify({'error': descriptionError})

def transform_jpg(data):

    img = Image.open(BytesIO(data))

    picture = img.crop((0, 340, img.size[0], img.size[1]))

    #    rotate = label.rotate(180)


#    return jsonify({'label': PILtoBase64(rotate)})
    return jsonify({'picture': PILtoBase64(picture)})
#    return jsonify({'picture': PILtoBase64(picture), 'label': PILtoBase64(label)})
