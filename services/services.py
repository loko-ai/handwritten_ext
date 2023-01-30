from flask import Flask, request, jsonify
from loko_extensions.model.components import Component, save_extensions
from PIL import Image
from loko_extensions.business.decorators import extract_value_args
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

app = Flask("new_ocr", static_url_path="/web", static_folder="/frontend/dist")

c = Component("handwritten")

save_extensions([c])

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")


# ocr_models = OCR.load_models()

# img, results = OCR.detection(img, ocr_models[2])

# bboxes, text = OCR.recoginition(img, results, ocr_models[0], ocr_models[1])


@app.route("/", methods=["POST"])
@extract_value_args(_request=request, file=True)
def test2(file, args):
    fname = file.filename
    img = Image.open(file.stream)
    img = img.convert("RGB")

    pixel_values = processor(img, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)

    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    print("You have uploaded a file called:", fname)
    return jsonify(dict(msg=generated_text))


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
