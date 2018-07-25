import cv2

img = cv2.imread('1.jpeg')

img = cv2.resize(img,(1500,999))
cv2.imwrite('new.jpeg',img)
print(img)