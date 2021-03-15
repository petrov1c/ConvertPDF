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

        return jsonify([{'picture': PILtoBase64(im)} for im in images])
    else:
        return jsonify({'error': descriptionError})

def transform_jpg(data):

    img = Image.open(BytesIO(data))

#    label = img.crop((790, 250, 955, 300)) # Хохлома черная
#    label = img.crop((790, 200, 955, 290)) # Хохлома белая
#    label = img.crop((145, 174, 250, 212)) # Бюджет
#    label = img.crop((155, 163, 324, 210)) # Florus
#    label = img.crop((150, 106, 320, 175)) # bdb

    picture = img.crop((0, 340, img.size[0], img.size[1]))

    #    rotate = label.rotate(180)


#    return jsonify({'label': PILtoBase64(rotate)})
    return jsonify({'picture': PILtoBase64(picture)})

#    return jsonify({'picture': PILtoBase64(picture), 'label': PILtoBase64(label)})
