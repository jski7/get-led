import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import skimage
from colorthief import ColorThief

from skimage import data, io
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb, rgb2gray

leds = {}

def detectLeds():

    #   Init lamp test
    #   Get a photo from camera when leds are on
    #   Create dict with all leds positions

    leds = {}                       # led objects
    detect_th = 0.87                # detection threshold - manipulate this parameter to get correct detections
    detect_sizes = range(400,600)    # range of sizes for detected objects

    image_rgb = io.imread('examples/leds_on.jpg')
    image = rgb2gray(image_rgb)
    # apply threshold
    bw = closing(image > detect_th, square(3))
    # remove artifacts connected to image border
    cleared = clear_border(bw)
    # label image regions
    label_image = label(cleared)
    # to make the background transparent, pass the value of `bg_label`,
    # and leave `bg_color` as `None` and `kind` as `overlay`
    image_label_overlay = label2rgb(label_image, image=image, bg_label=0)

    for region in regionprops(label_image):
        # take regions with large enough areas
        if region.area in detect_sizes:
            # draw rectangle around segmented item
            minr, minc, maxr, maxc = region.bbox
            leds[region.label] = {"led_state": "null", "dominant_color": "null", "top": minr,
                                  "left": minc, "bottom": maxr, "right": maxc}
    return leds

def readStates(file, leds_dict):
    #   Get a photo
    #   Check state of leds
    #   put it into dict from detect leds

    for key in leds_dict:
        image_rgb = io.imread(file)
        cropped = image_rgb[leds_dict[key]["top"]:leds_dict[key]["bottom"], leds_dict[key]["left"]:leds_dict[key]["right"]]
        skimage.io.imsave("temp/" + str(str(key)) + ".jpg", cropped)
        color_thief = ColorThief("temp/" + str(str(key)) + ".jpg")
        dominant_color = color_thief.get_color(quality=1)
        max_channel_index = dominant_color.index(max(dominant_color))
        brightness_th = 400 #range 0 - 764
        ## TBD: Set color boundaries for better recognition
        if sum(dominant_color) > brightness_th:
            if dominant_color[0] != dominant_color[1] and dominant_color[1] != dominant_color[2] and dominant_color[
                0] != dominant_color[2]:
                if dominant_color[0] > 140 and dominant_color[1] < 120 and dominant_color[2] < 120:
                    state = "red";
                elif dominant_color[0] > 180 and dominant_color[1] > 180:
                    state = "yellow";
                elif dominant_color[2] > 140:
                    state = "blue";
            else:
                state = "not recognized";
        else:
            state = "off"
        leds[key]["dominant_color"] = dominant_color
        leds[key]["led_state"] = state
    return leds


#TBD thresholds
leds = detectLeds()
leds = readStates('examples/leds_off.jpg', leds)
print(leds)
leds = readStates('examples/leds_on.jpg', leds)
print(leds)

def renameLed(id, name): {
    #   Edit name id of one led
}