import time
import picamera
import picamera.array
import cv2
from fractions import Fraction
from skimage import io
import skimage
from dominant_color_detection import detect_colors


camera = picamera.PiCamera()
camera.rotation = 180
camera.resolution = (416, 304)
#camera.framerate = 40
camera.brightness = 70  # 0-100
camera.contrast = 80  # 0-100
camera.exposure_compensation = 0
camera.image_effect = 'none'
camera.exposure_mode = 'off'
camera.shutter_speed = 20000
camera.saturation = 0
camera.sharpness = -100
camera.iso = 0
# camera.awb_mode = 'auto'
camera.awb_mode = 'off'
camera.awb_gains = (Fraction(77, 64), Fraction(793, 256))
with picamera.array.PiRGBArray(camera) as stream:
    camera.capture(stream, format='bgr')
    time.sleep(1)
    # At this point the image is available as stream.array
    image = stream.array
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

from dominantcolors import get_image_dominant_colors
dominant_colors = tuple(get_image_dominant_colors(image_path='temp/led_1.jpg',num_colors=1)[0])
print(dominant_colors)
from colorthief import ColorThief
color_thief = ColorThief("temp/led_1.jpg")
thief = color_thief.get_color(quality=1)
print(thief)

# import time
# import picamera
# import picamera.array
# import cv2
#
# with picamera.PiCamera() as camera:
#     camera.rotation = 180
#     camera.resolution = (800, 600)
#     camera.framerate = 24
#     camera.brightness = 45  # 0-100
#     camera.contrast = 80  # 0-100
#     camera.image_effect = 'none'
#     camera.exposure_mode = 'off'
#     camera.shutter_speed = 5000
#     camera.iso = 500
#     camera.awb_mode = 'auto'
#     with picamera.array.PiRGBArray(camera) as stream:
#         camera.capture(stream, format='bgr')
#         image = stream.array
#         cv2.imshow('image', image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import time
# import cv2
#
#
# # initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# time.sleep(0.5)
# rawCapture = PiRGBArray(camera)
# # allow the camera to warmup
# time.sleep(0.5)
# # grab an image from the camera
# camera.capture(rawCapture, format="rgb")
# image = rawCapture.array
# # display the image on screen and wait for a keypress
# cv2.imshow("Image", image)
# cv2.waitKey(0)
# camera.release()

# # import the opencv library
# import cv2
#
# # define a video capture object
# vid = cv2.VideoCapture(0)
#
# while (True):
#
#     # Capture the video frame
#     # by frame
#     ret, frame = vid.read()
#
#     # Display the resulting frame
#     cv2.imshow('frame', frame)
#
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # After the loop release the cap object
# vid.release()
# # Destroy all the windows
# cv2.destroyAllWindows()