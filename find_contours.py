import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
#import exel_to_image as eti ### 이 패키지는 실행 시간을 매~~우 느리게 한다 -> exe_to_image.py 내의 모든 코드를 실행을 하기 떄문!
import sys


########### Find Contours을 하기 이전의 image 전처리(img_thresh 생성) #################
exel_to_image = cv.imread('./exel_to_image.jpg')

if exel_to_image is None:
    sys.exit("No Such Image File")

height,width,channel = exel_to_image.shape

img = np.array(exel_to_image)
img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

img_blurred = cv.GaussianBlur(gray, ksize=(3,3), sigmaX=0)
img_thresh = cv.adaptiveThreshold(
        img_blurred,
        maxValue=255.0,
        adaptiveMethod=cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv.THRESH_BINARY_INV,
        blockSize=19,
        C=10
    )

plt.figure(figsize=(12, 10))
plt.imshow(img_thresh, cmap='gray')  # img_tresh : (y X x) = 1192 x 399
plt.show()

########### Find Contours #################
contours, _ = cv.findContours(
    img_thresh,
    mode=cv.RETR_LIST,
    method=cv.CHAIN_APPROX_SIMPLE
)
#0으로 초기화된 temp_result에 countor 좌표를 점으로 찍은 것에 불과
temp_result = np.zeros((height,width,channel), dtype = np.uint8)
temp_result = cv.drawContours(temp_result,contours=contours, contourIdx=-1, color=(0,255,255))
cv.imwrite('./drawContours.jpg',temp_result)
plt.figure(figsize=(12,10))
plt.imshow(temp_result)
plt.show()

############## Prepare Data ####################

temp_result = np.zeros((height, width, channel), dtype=np.uint8)
contours_dict = []
for contour in contours:

    x, y, w, h = cv.boundingRect(contour)

    cv.rectangle(exel_to_image, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)

    # insert to dict
    contours_dict.append({
        'contour': contour,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'cx': x + (w / 2),
        'cy': y + (h / 2)
    })

plt.figure(figsize=(12, 10))
plt.imshow(exel_to_image, cmap='gray')
plt.show()

