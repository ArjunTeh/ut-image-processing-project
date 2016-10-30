import cv2

img = cv2.imread("/home/arjun/Pictures/bird.jpg")
cv2.namedWindow("opencv")
cv2.imshow("opencv",img)
padded = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REPLICATE)
cv2.waitKey(0)
