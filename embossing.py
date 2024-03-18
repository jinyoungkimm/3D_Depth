import cv2 as cv
import numpy as np

img = cv.imread('./0.JPG') # 391 x 1782(y,x)
img = cv.resize(img,(80,80),interpolation=cv.INTER_LINEAR) # INTER_CUBIC이라는 선택지도 있음.

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY) # gray scale로 변환
cv.imshow('gray',gray)

emboss1 = np.array([[-1.0, -1.0, 0.0],
                    [-1.0, 0.0, 1.0],
                    [0.0, 1.0, 1.0]])

emboss2 = np.array([[-1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0]])

gray16 = np.int16(gray)
emboss_1 = np.uint8(np.clip(cv.filter2D(gray16,-1,emboss1)+128,0,255))
emboss_2 = np.uint8(np.clip(cv.filter2D(gray16,-1,emboss2)+128,0,255))
cv.imshow("emboss_1",emboss_1)
cv.imshow("emboss_2",emboss_2)

cv.waitKey(0)
cv.destroyAllWindows()





