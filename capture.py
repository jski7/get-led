import cv2

# Original code
#
# while True:
#   ret, frame = cap.read()
#   cv2.imshow('Video', frame)
#
#   if cv2.waitKey(1) == 27:
#     exit(0)

def captureSnap(url):
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()
    cv2.imwrite('temp/snap.jpg', frame)
    #cv2.imshow('Video', frame)
    return frame

# Example usage:
#
# url = 'http://192.168.0.54:8081/frame.mjpg'
# frame = captureSnap(url)
# cv2.imshow('Video', frame)
# if cv2.waitKey(0) == 27:
#     exit(0)

def cropSnap(file):
    if __name__ == '__main__':
        # Read image
        img = cv2.imread(file)
        # Select ROI
        r = cv2.selectROI(img)
        # Crop image
        imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        # Display cropped image
        cv2.imshow("Image", imCrop)
    return imCrop
