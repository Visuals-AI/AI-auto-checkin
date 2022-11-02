import cv2
import time

capture = cv2.VideoCapture(0)
time.sleep(1)

while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame,1)   #镜像操作
    cv2.imshow("video", frame)
    key = cv2.waitKey(50)
    #print(key)
    if key  == ord('q'):  #判断是哪一个键按下
        break
cv2.destroyAllWindows()