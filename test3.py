import os
import cv2 as cv
import numpy as np

# Function to process individual image
def process_image(image_path):

    img = cv.imread(image_path)

    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(gray, threshold1=180, threshold2=200)

    #cv.imshow("canny",edges)
    #cv.waitKey()
    cv.imwrite('./canny.png',edges)  # Save required!
    _edges = cv.imread("./canny.png")

    #height,width,channel = _edges.shape

    _edges = cv.cvtColor(_edges, cv.COLOR_RGB2GRAY)
    _edges = cv.GaussianBlur(_edges, (5, 5), 0)

    contours, _ = cv.findContours(_edges, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)

    #temp_result = np.zeros((height, width, channel), dtype=np.uint8)
    #temp_result = cv.drawContours(temp_result, contours=contours, contourIdx=-1, color=(0, 255, 255))
    #cv.imshow("drawContours",temp_result)
    #cv.imwrite("./drawContours.png",temp_result)
    #cv.waitKey()

    output_folder_alphabat = "./alphabat_roi_images"
    output_folder_numeric = "./numeric_roi_images"
    idx = -1
    for contour in contours:

        area = cv.contourArea(contour)
        x, y, w, h = cv.boundingRect(contour)

        if (area >= 3000 and w/h >= 1) or (w/h <= 1 and area >= 14000): # area >= 4000 and w/h >= 1:로 고정

            idx += 1
            roi = img[y-1:y + h+1, x-1:x + w+1]

            #print("x",x,'y',y)
            #print("w/h", w/h)
            # Save the ROI_V1
            roi_filename = os.path.splitext(os.path.basename(image_path))[0] +f'_[idx_{idx}]_'+ os.path.splitext(os.path.basename(image_path))[0][idx]+'_roi.png'
            print("roi_filename",roi_filename)
            if idx == 0: # roi_image가 A~Z까지의 알파벳인 경우
                print("roi_char",os.path.splitext(os.path.basename(image_path))[0][idx])
                roi_output_path = os.path.join(output_folder_alphabat, roi_filename)


            else: # roi_image가 0~9까지의 숫자인 경우
                #print("roi_char",os.path.splitext(os.path.basename(image_path))[0][idx])
                roi_output_path = os.path.join(output_folder_numeric, roi_filename)

            #cv.imshow("roi", roi)
            #cv.waitKey(0)
            cv.imwrite(roi_output_path, roi)

            cv.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
            #cv.imshow("asdf",img)

    cv.imshow("BBox", img)
    cv.waitKey(0)

# Path to the directory containing PNG images
folder_path = "./csv_to_images"

# Process each PNG file in the directory
count = 0
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        count += 1
        print("count",count)
        print("filename",filename)
        image_path = os.path.join(folder_path, filename)
        process_image(image_path)