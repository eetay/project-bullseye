import numpy as np
import cv2
import imutils

cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    img_hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([5,50,50])
    upper_red = np.array([15,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)


    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)


    # join my masks
    mask = mask0+mask1
 #   mask=mask0

    # set my output img to zero everywhere except my mask
    output_img = frame.copy()
    output_img[np.where(mask==0)] = 0
    output_img[np.where(mask!=0)] = 255

    output_img = cv2.GaussianBlur(output_img, (11, 11), 0)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) <= 0:
        continue

    center = None

    c = max(cnts, key=cv2.contourArea)

    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    
    if not M["m00"]:
        continue

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    center = (cX, cY)

    cv2.circle(output_img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    cv2.circle(output_img, center, 5, (0, 0, 255), -1)


    # Our operations on the frame come here
    

    # Display the resulting frame
    cv2.imshow('frame', output_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
