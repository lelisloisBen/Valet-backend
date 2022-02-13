from flask import jsonify, url_for
import hashlib
import cv2
import imutils
import numpy as np
import pytesseract

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def sha256(string):
    m = hashlib.sha256()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def readTag(myImg):
    #read and resize image
    img = cv2.imdecode(np.fromstring(myImg.read(), np.uint8), cv2.IMREAD_COLOR)
    # img = cv2.imread(myImg, cv2.IMREAD_COLOR)
    img = ResizeWithAspectRatio(img, width=620)

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
    tagtText = pytesseract.image_to_string(cropped, config = '--psm 11')
    return tagtText