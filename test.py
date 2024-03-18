import cv2 as cv
import numpy as np

# Load the image (replace 'your_image_path.jpg' with the actual path)
image_path = './exel_to_image.jpg'
image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

# Threshold the image to separate numbers from background
_, binary_image = cv.threshold(image, 128, 255, cv.THRESH_BINARY_INV)

mser = cv.MSER_create()
regions, _ = mser.detectRegions(binary_image)

hulls = [cv.convexHull(p.reshape(-1, 1, 2)) for p in regions]
removed_BBox = []

for i, c1 in enumerate(hulls):

    x, y, w, h = cv.boundingRect(c1)

    r1_start = (x, y)

    r1_end = (x + w, y + h)

    for j, c2 in enumerate(hulls):

        if (i == j):
            continue

        x, y, w, h = cv.boundingRect(c2)
        r2_start = (x, y)
        r2_end = (x + w, y + h)



        if r1_start[0] > r2_start[0] and r1_start[1] > r2_start[1] and r1_end[0] < r2_end[0] and r1_end[1] < r2_end[1]:
            removed_BBox.append(i)

for j, cnt in enumerate(hulls):

    if j in removed_BBox:
        continue

    x, y, w, h = cv.boundingRect(cnt)

    margin = 8

    roi = image[y - margin:y + h + margin, x - margin:x + w + margin]

    if len(roi) >= 1:
        cv.imshow("d",roi)
        cv.waitKey(0)
        
"""""""""
# Find contours of the numbers
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw filled black rectangles over the numbers
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)

# Save the modified image (replace 'output_image.jpg' with your desired output path)
output_path = './output_image.jpg'
cv2.imshow("t",image)
cv2.waitKey(0)

#cv2.imwrite(output_path, image)

#print(f"Processed image saved at {output_path}")
"""""""""