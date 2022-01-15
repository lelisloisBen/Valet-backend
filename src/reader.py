import cv2

img = cv2.imread('/Users/danny/Desktop/Private Dev Projects/Valet/backend/payload/lptest.jpeg', cv2.IMREAD_COLOR)
img = cv2.resize(img, (620,480))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def img_test(img):
    if img is None:
        result = 'Nope, that didnt work'
    else:
        result = 'Its working!!!'
    return result

print(img_test(img))