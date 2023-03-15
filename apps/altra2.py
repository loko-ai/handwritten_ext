import cv2

image = cv2.imread('/media/fulvio/Data/Docs/handwritten-text-2.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (59, 59))

dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

boundary = []
for c, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    boundary.append((x, y, w, h))
k = sorted(boundary)
print(boundary)
