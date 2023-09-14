import logging
from io import BytesIO
from tempfile import TemporaryFile, NamedTemporaryFile

from flask import Flask, request, jsonify
from loko_extensions.model.components import Component, save_extensions
from PIL import Image
from loko_extensions.business.decorators import extract_value_args
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

from business.linesegmentation import lineSegmentation
import numpy as np

from doc.doc import handwritten_doc

app = Flask("new_ocr", static_url_path="/web", static_folder="/frontend/dist")

c = Component("handwritten", description=handwritten_doc)

save_extensions([c])

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# ocr_models = OCR.load_models()

# img, results = OCR.detection(img, ocr_models[2])

# bboxes, text = OCR.recoginition(img, results, ocr_models[0], ocr_models[1])

import cv2


@app.route("/", methods=["POST"])
@extract_value_args(_request=request, file=True)
def test2(file, args):
    fname = file.filename
    img = Image.open(file.stream)
    img = img.convert("RGB")
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    lines = lineSegmentation(img)
    texts = []

    for line in lines:
        try:
            with NamedTemporaryFile(suffix=".png") as ff:
                cv2.imwrite(ff.name, line)
                line = Image.open(ff.name)
                line = line.convert("RGB")
                pixel_values = processor(line, return_tensors="pt").pixel_values
                generated_ids = model.generate(pixel_values)

            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            texts.append(generated_text)
        except Exception as e:
            logging.exception(e)

    print("You have uploaded a file called:", fname)
    return jsonify(dict(msg=texts))


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
