import numpy as np
import cv2
import imutils

import asyncio
import websockets
import json
import time

def FrameProcess(frame, websocket):
    # Convert frame to HSV
    img_hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color limits
    lower_red = np.array([5,50,50])
    upper_red = np.array([15,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join the masks
    mask = mask0+mask1

    # convert image to black/white
    output_img = frame.copy()
    output_img[np.where(mask==0)] = 0
    output_img[np.where(mask!=0)] = 255
    output_img = cv2.GaussianBlur(output_img, (11, 11), 0)

    # find objects in frame
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) <= 0:
        return

    c = max(cnts, key=cv2.contourArea)

    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    
    if not M["m00"]:
        return

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    center = (cX, cY)

    if websocket != 0:
        greeting = json.dumps({'offsetTop':cY, 'offsetLeft':cX})
        websocket.send(greeting)

    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # Our operations on the frame come here
    
    # Display the resulting frame
    return frame
def VideoProcess(websocket):
    while True:
        ret, frame = cap.read()
        frame = FrameProcess(frame, websocket)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

async def hello(websocket, path):
    print("Connected!!")
    VideoProcess(websocket)
    
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cap = cv2.VideoCapture(0)

start_server = websockets.serve(hello, 'localhost', 9999)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



#VideoProcess(0)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()