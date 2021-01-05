from picamera import PiCamera
from time import sleep, time

camera = PiCamera()
sleep(1)
camera.rotation = 180
camera.resolution = (800, 600)
camera.framerate = 40
camera.brightness = 45 #0-100
camera.contrast = 80 #0-100
camera.image_effect = 'none'
camera.exposure_mode = 'off'
camera.shutter_speed = 5000
camera.iso = 500
camera.awb_mode = 'flash'

#camera.image_effect = 'colorpoint'
# none
# negative
# solarize
# sketch
# denoise
# emboss
# oilpaint
# hatch
# gpen
# pastel
# watercolor
# film
# blur
# saturation
# colorswap
# washedout
# posterise
# colorpoint
# colorbalance
# cartoon
# deinterlace1
# deinterlace2

#camera.exposure_mode = 'off'
# off
# auto
# night
# nightpreview
# backlight
# spotlight
# sports
# snow
# beach
# verylong
# fixedfps
# antishake
# fireworks

#camera.awb_mode = 'cloudy'
# off
# auto
# sunlight
# cloudy
# shade
# tungsten
# fluorescent
# incandescent
# flash
# horizon

# x=time.time()
# camera.capture('temp/camera.jpg')
# print(x - time.time())
camera.start_preview()
#camera.capture()
sleep(5)
camera.stop_preview()
print(camera)