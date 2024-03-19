import os
import sys
import math
import cv2 as cv
import numpy as np

# Function to process individual image
def process_image(image_path):

    img = cv.imread(image_path)

    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(gray, threshold1=180, threshold2=200)

    cv.imwrite('./canny.png',edges)  # Save required!
    _edges = cv.imread("./canny.png")


    _edges = cv.cvtColor(_edges, cv.COLOR_RGB2GRAY)
    _edges = cv.GaussianBlur(_edges, (5, 5), 0)

    contours, _ = cv.findContours(_edges, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)

    output_folder_alphabat = "./alphabat_roi_images"
    output_folder_numeric = "./numeric_roi_images"
    idx = -1
    margin = 0
    pre_y1 = 0
    pre_y2 = 0
    for contour in contours:

        area = cv.contourArea(contour)
        x, y, w, h = cv.boundingRect(contour)

        # BBox의 중심 좌표를 계산
        after_y1 = h
        height = after_y1 + pre_y1

        after_y2 = y
        _height = abs( (after_y2 - h) - pre_y2) # after_y2 - h : OpenCV의 좌표계는 Y축이 위로 갈수록 값이 더 작아 진다


        if (w/h >= 1 and area >= 4000) or (w/h <= 1 and area >= 14000) or ((w/h) >= 2 and area >= 2000):
            print("area_0",area)
            print("w/h",w/h)


        if (w/h >= 1 and area >= 4000) or (w/h <= 1 and area >= 14000) or ((w/h) >= 2 and area >= 2000) and height <= _height: # (area >= 4000 and w/h >= 1)에서 (area >= 3000 and w/h >= 1) or (w/h <= 1 and area >= 14000)로 변경
                                                                                                                               # (w/h) <= 1을 만족하는 문자도 존재(ex. W )

            idx += 1
            roi = img[y-margin:y + h + margin, x-margin:x + w + margin]

            pre_y1 = after_y1
            pre_y2 = after_y2

            #print("pre_y1",pre_y1,"pre_y2",pre_y2)
            #cv.imshow("c",roi)
            #cv.waitKey()
            #print("height",height)
            print("x",x,'y',y,'w',w,'h',h)
            print("pre_y1(h)",pre_y1,"pre_y2(y)",pre_y2)
            print("w/h", w/h)
            print("height",height,"_height",_height)
            # Save the ROI_V1
            roi_filename = os.path.splitext(os.path.basename(image_path))[0] +f'_[idx_{idx}]_'+ os.path.splitext(os.path.basename(image_path))[0][idx]+'_roi.png'
            print("roi_filename",roi_filename)
            print()
            print("======================================")
            if idx == 0: # roi_image가 A~Z까지의 알파벳인 경우
                roi_output_path = os.path.join(output_folder_alphabat, roi_filename)

            else: # roi_image가 0~9까지의 숫자인 경우
                roi_output_path = os.path.join(output_folder_numeric, roi_filename)

            cv.imwrite(roi_output_path, roi)

            cv.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
            #cv.imshow("asdf",img)
            #cv.waitKey()

    if idx != 5:
        sys.exit("문자 분할이 정상적으로 이루어지지 않음")
    #cv.imshow("BBox", img)
    #cv.waitKey(0)

# Path to the directory containing PNG images
folder_path = "./csv_to_images"

# Process each PNG file in the directory
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        print("filename",filename)
        image_path = os.path.join(folder_path, filename)
        process_image(image_path)