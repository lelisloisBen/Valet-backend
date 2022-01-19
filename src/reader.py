import cv2
import imutils
import numpy as np

#read and resize image
img = cv2.imread('/Users/danny/Desktop/Private Dev Projects/Valet/backend/payload/lptest.jpeg', cv2.IMREAD_COLOR)
img = cv2.resize(img, (620,480))

# convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 13, 15, 15)

# filter image to show contours
edged = cv2.Canny(gray, 30, 200)

# sort contours from large to small, and keep top ten enclosed shapes
contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
screenCnt = None

# loop through results to find the rectangle
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    if len(approx) == 4:
        screenCnt = approx
        break

# black out the image surrounding the vehicle tag
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1,)
new_image = cv2.bitwise_and(img, img, mask=mask)

# the following line of code is used only for testing
# cv2.imwrite('masked.jpg', new_image)