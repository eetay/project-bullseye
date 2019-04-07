import numpy as np
import cv2
import imutils

import asyncio
import websockets
import json
import time

xlb = 50000
xrb = 0
yub = 50000
ybb = 0
tot_width = 0
tot_height = 0
    
def BounderiesFrameProcess(frame):
    global xlb
    global xrb
    global yub
    global ybb
    global tot_width
    global tot_height

    # Convert frame to HSV
    img_hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color limits
    lower_g = np.array([30,100,50])
    upper_g = np.array([80,255,255])

    lower_r = np.array([0,50,50])
    upper_r = np.array([10,255,255])

    mask = cv2.inRange(img_hsv, lower_r, upper_r)

    output_img = frame.copy()
    output_img[np.where(mask==0)] = 0
    output_img[np.where(mask!=0)] = 255
    output_img = cv2.GaussianBlur(output_img, (11, 11), 0)

    # find objects in frame
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    tad_frame = output_img.copy()

    if len(cnts) < 2:
        return 0,tad_frame

    num = 0
    for cc in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(cc)
        if radius > 5:
            cv2.circle(tad_frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            num = num+1

    if num < 2:
        return 0,tad_frame

    for cc in cnts:
        ((x, y), radius) = cv2.minEnclosingCircle(cc)
        if radius > 5:
            print(xlb,xrb,x,yub,ybb,y,radius)
            xlb = min(x,xlb)
            xrb = max(x,xrb)
            yub = min(y,yub)
            ybb = max(y,ybb)

    print(xlb,xrb,yub,ybb)

    tot_width = xrb-xlb
    tot_height = ybb-yub

    greeting = json.dumps({'offsetTop':tot_height, 'offsetLeft':tot_width})
    websocket.send(greeting)

    # Display the resulting frame
    return xrb,tad_frame

def FrameProcess(frame, websocket):
    global xlb
    global xrb
    global yub
    global ybb
    global tot_width
    global tot_height

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

    tad_frame = frame.copy()

    if len(cnts) <= 0:
        return 0,tad_frame

    c = max(cnts, key=cv2.contourArea)
    found = False

    for cc in cnts:
        M = cv2.moments(cc)
        if not M["m00"]:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        if cX < xlb or cX > xrb or cY < yub or cY > ybb:
            continue
        
        found = True
        c = cc

    if not found:
        return 0,tad_frame

    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    
    if not M["m00"]:
        return 0,tad_frame

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    center = (cX, cY)

    refX = (x-xlb)/tot_width;
    refY = (y-yub)/tot_height;

    greeting = json.dumps({'offsetTop':refY, 'offsetLeft':refX})
    websocket.send(greeting)

    tad_frame =  output_img.copy() #frame.copy()

    cv2.circle(tad_frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    cv2.circle(tad_frame, center, 5, (0, 0, 255), -1)

    # Display the resulting frame
    return 1,tad_frame


def VideoProcess(websocket):
    ret = 0
    while ret == 0: 
        ret, frame = cap.read()
        ret,frame = BounderiesFrameProcess(frame)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    while True:
        ret, frame = cap.read()
        ret,frame = FrameProcess(frame, websocket)
        cv2.imshow('window', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

async def hello(websocket, path):
    print("Connected!!")
    VideoProcess(websocket)
    
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cap = cv2.VideoCapture(1)

start_server = websockets.serve(hello, 'localhost', 9999)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

#VideoProcess(0)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
