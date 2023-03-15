import keras_ocr
import matplotlib.pyplot as plt
import cv2
from keras_ocr.tools import warpBox

pipeline = keras_ocr.pipeline.Pipeline()

images = [
    keras_ocr.tools.read("/media/fulvio/Data/Docs/Sample-handwritten-text-from-CVL-Database.png"),
    keras_ocr.tools.read("/media/fulvio/Data/Docs/Sample-handwritten-text-from-CVL-Database.png")
]

box_groups = pipeline.detector.detect(images)

for group in box_groups:
    print("group", group)

for image, group in zip(images, box_groups):
    for i, box in enumerate(group):
        # box = cv2.boundingRect(box)
        # cropped_image = image[box[1]:box[3], box[0]:box[2]]
        cropped_image = warpBox(image=image, box=box)
        try:
            cv2.imwrite(f"img{i}.jpeg", cropped_image)
        except Exception as inst:
            print(inst)

prediction_groups = pipeline.recognize(images)

# Plot the predictions
fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    print(predictions)
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

plt.show()
