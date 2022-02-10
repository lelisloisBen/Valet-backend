import cv2
import imutils
import numpy as np
import pytesseract

#read and resize image
img = cv2.imread('/Users/danny/Desktop/Private Dev Projects/Valet/backend/payload/lptest.jpeg', cv2.IMREAD_COLOR)
img = cv2.resize(img, (620,480))

# test above code with ResizeWithAspectRatio function enabled

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

# need to create a way to handle null errors when no enclosed contours are found

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

# crop the tag out of the image
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
cropped = new_image[topx:bottomx + 1, topy:bottomy + 1]

# read the tag
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(cropped, config = '--psm 11')
print("Got your tag!", text)

# the following line of code is used only for testing
# cv2.imwrite('cropped.jpg', cropped)

# need to develop a way to handle failures