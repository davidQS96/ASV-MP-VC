import numpy as np
import cv2

#https://www.codingforentrepreneurs.com/blog/open-cv-python-change-video-resolution-or-scale
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)





### https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
##cap = cv2.VideoCapture('vid1.mp4')
##cv2.namedWindow('image',cv2.WINDOW_NORMAL)
##
##while(cap.isOpened()):
##    ret, frame = cap.read()
##
##    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
##
##    cv2.imshow('Vid1', frame)
##    if cv2.waitKey(1) & 0xFF == ord('q'):
##        break


cap = cv2.VideoCapture('vid1.mp4')

while True:
    rect, frame = cap.read()
    nframe = rescale_frame(frame, percent = 25)
    cv2.imshow('nframe', nframe)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
##    frame150 = rescale_frame(frame, percent=150)
##    cv2.imshow('frame150', frame150)


    

cap.release()
cv2.destroyAllWindows()
