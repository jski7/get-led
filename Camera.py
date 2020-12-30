from picamera import PiCamera
from time import sleep, time

camera = PiCamera()
camera.rotation = 180
camera.resolution = (400, 300)
camera.framerate = 30
camera.brightness = 50 #0-100
camera.contrast = 80 #0-100

camera.image_effect = 'colorpoint'
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

camera.exposure_mode = 'off'
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

camera.awb_mode = 'cloudy'
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

x=time.time()
camera.capture('temp/camera.jpg')
print(x - time.time())
camera.start_preview()
#camera.capture()
sleep(3)
camera.stop_preview()