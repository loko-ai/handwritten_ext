from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from doctr.models import detection_predictor
from doctr.io.image import read_img_as_tensor
from doctr.models import obj_detection

predictor = ocr_predictor(pretrained=True)
predictor = detection_predictor('db_resnet50')
model = obj_detection.fasterrcnn_mobilenet_v3_large_fpn(pretrained=True, num_classes=5).eval()

u = "img0.jpeg"

img = read_img_as_tensor(u).unsqueeze(0)

result = model(img)

print(result)

# print(result.show(doc))
