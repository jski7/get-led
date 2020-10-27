import cv2

def captureSnap(url):
    cap = cv2.VideoCapture('http://192.168.0.54:8081/frame.mjpg')
    #while True:
    ret, frame = cap.read()
    cv2.imshow('Video', frame)
    cv2.imwrite('temp/snap.jpg', frame)
    return frame