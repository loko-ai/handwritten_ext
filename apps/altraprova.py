from itertools import groupby
from operator import itemgetter

import cv2
import numpy as np

# import image
image = cv2.imread('/media/fulvio/Data/Docs/handwritten-text-2.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Find contours in the thresholded image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get the bounding boxes for each contour
bboxes = [cv2.boundingRect(cnt) for cnt in contours]

# Filter out bounding boxes that are too small
min_area = 10
bboxes = [bbox for bbox in bboxes if bbox[2] * bbox[3] > min_area]
print(len(bboxes))

# Sort the bounding boxes by their y-coordinate
bboxes.sort(key=lambda x: x[1])

# Group the bounding boxes that belong to the same line
grouped_bboxes = []


def mround(a):
    temp = int(a)
    if a - temp > .5:
        return temp + 1
    else:
        return temp


for _, group in groupby(bboxes, key=lambda x: mround(x[1] / 30)):
    line_bboxes = list(group)
    line_bboxes.sort(key=lambda x: x[0])
    grouped_bboxes.append(line_bboxes)

print(len(grouped_bboxes))
print(grouped_bboxes)
# Extract each line as a separate image
for i, line_bboxes in enumerate(grouped_bboxes):
    line_image = np.zeros(image.shape[:2], dtype=np.uint8)
    x = min(bbox[0] for bbox in line_bboxes)
    y = min(bbox[1] for bbox in line_bboxes)
    w = max(bbox[0] + bbox[2] for bbox in line_bboxes) - x
    h = max(bbox[1] + bbox[3] for bbox in line_bboxes) - y

    cv2.rectangle(line_image, (x, y), (x + w, y + h), color=255, thickness=-1)
    line_image = cv2.bitwise_and(gray, gray, mask=line_image)
    cropped_image = line_image[y:y + h, x:x + w]
    cv2.imwrite(f'line_{i}.png', cropped_image)
