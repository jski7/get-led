import matplotlib.patches as mpatches
import skimage
from colorthief import ColorThief
from capture import captureSnap, cropSnap
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np

from skimage import io
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb, rgb2gray


def detectLeds(file, detect_th, min_size, max_size):

    #   Init lamp test
    #   Get a photo from camera when leds are on
    #   Create dict with all leds positions
    leds = {}                       # led objects
    #image_rgb = io.imread(file)
    image_rgb = file
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

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image_label_overlay)

    for region in regionprops(label_image):
        # take regions with large enough areas
        print("Size:" + str(region.area))
        if region.area in range(min_size, max_size):
            # draw rectangle around segmented item
            minr, minc, maxr, maxc = region.bbox
            leds["led_"+str(region.label)] = {"led_state": "null", "dominant_color": ("null", "null", "null"), "top": minr,
                                  "left": minc, "bottom": maxr, "right": maxc}
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            plt.text(minc, minr-8, "led_"+str(region.label), color="r")

    ax.set_axis_off()
    plt.tight_layout()

    plt.show()

    return leds

def readStates(file, leds_dict, brightness_th):
    #   Get a photo
    #   Check state of leds
    #   put it into dict from detect leds

    for key in leds_dict.keys():
        #image_rgb = io.imread(file)
        image_rgb = file
        cropped = image_rgb[leds_dict[key]["top"]:leds_dict[key]["bottom"], leds_dict[key]["left"]:leds_dict[key]["right"]]
        skimage.io.imsave("temp/" + str(str(key)) + ".jpg", cropped,  check_contrast=False)
        color_thief = ColorThief("temp/" + str(str(key)) + ".jpg")
        dominant_color = color_thief.get_color(quality=1)
        ## TBD: Set color boundaries for better recognition
        state = "not recognized"
        if sum(dominant_color) > brightness_th:
            if dominant_color[0] != dominant_color[1] and dominant_color[1] != dominant_color[2] and dominant_color[0] != dominant_color[2]:
                if dominant_color[0] in range(30, 50) and\
                        dominant_color[1] in range(200,230) and\
                        dominant_color[2] in range(215,255):
                    state = "yellow"
                elif dominant_color[0] in range(30, 50) and \
                            dominant_color[1] in range(220, 255) and \
                            dominant_color[2] in range(5, 40):
                    state = "green"
                elif dominant_color[0] in range(0, 30) and \
                            dominant_color[1] in range(0, 210) and \
                            dominant_color[2] in range(30, 255):
                    state = "red"
            else:
                state = "not recognized"
        else:
            state = "off"
        leds[key]["dominant_color"] = dominant_color
        leds[key]["led_state"] = state
    return leds


def readStatesMeasured(file, leds_dict, measures):
    #   Get a photo
    #   Check state of leds
    #   put it into dict from detect leds

    for key in leds_dict.keys():
        # image_rgb = io.imread(file)
        image_rgb = file
        cropped = image_rgb[leds_dict[key]["top"]:leds_dict[key]["bottom"],
                  leds_dict[key]["left"]:leds_dict[key]["right"]]
        skimage.io.imsave("temp/" + str(str(key)) + ".jpg", cropped, check_contrast=False)
        color_thief = ColorThief("temp/" + str(str(key)) + ".jpg")
        dominant_color = color_thief.get_color(quality=1)
        ## TBD: Set color boundaries for better recognition
        state = "not recognized"
        print(dominant_color, measures[key]["brightness_low"])
        print(measures[key]["r_low"], measures[key]["r_high"])
        print(measures[key]["g_low"], measures[key]["g_high"])
        print(measures[key]["b_low"], measures[key]["b_high"])
        if sum(dominant_color) / 3 > measures[key]["brightness_low"]:
            if dominant_color[0] != dominant_color[1] and dominant_color[1] != dominant_color[2] and dominant_color[0] != dominant_color[2]:
                if dominant_color[0] in range(measures[key]["r_low"], measures[key]["r_high"]) and \
                        dominant_color[1] in range(measures[key]["g_low"], measures[key]["g_high"]) and \
                        dominant_color[2] in range(measures[key]["b_low"], measures[key]["b_high"]):
                    state = "yellow"
                elif dominant_color[0] in range(measures[key]["r_low"], measures[key]["r_high"]) and \
                        dominant_color[1] in range(measures[key]["g_low"], measures[key]["g_high"]) and \
                        dominant_color[2] in range(measures[key]["b_low"], measures[key]["b_high"]):
                    state = "green"
                elif dominant_color[0] in range(measures[key]["r_low"], measures[key]["r_high"]) and \
                        dominant_color[1] in range(measures[key]["g_low"], measures[key]["g_high"]) and \
                        dominant_color[2] in range(measures[key]["b_low"], measures[key]["b_high"]):
                    state = "red"
            else:
                state = "not recognized"
        else:
            state = "off"
        leds[key]["dominant_color"] = dominant_color
        leds[key]["led_state"] = state
    return leds

def translateDictionary(dict):
    translate = {}
    for k, v in dict.items():
        print("This is the key: '%s' and this is the value '%s'" % (k, v))
        new_key = str(input("Please enter a new key: \n"))
        print("\n")
        translate[k] = new_key

    for old, new in translate.items():
        dict[new] = dict.pop(old)


def chartLeds(count, leds_dict):
    meas_dict = {}
    for led in leds_dict:
        meas_dict[led] = {"brightness": [], "r": [], "g": [], "b": []}

    print(meas_dict)

    fig, ax = plt.subplots()
    ax.set(xlabel='measurements', title='values measured for red led')

    i = 0
    while i < count:
        i += 1
        snap = captureSnap(url)
        imCrop = snap[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        leds_dict = readStates(imCrop, leds_dict, 30)

        print()
        for led in leds_dict:
            print(str(led) + " " + leds_dict[led]["led_state"])
            print(leds_dict[led]["dominant_color"])

        # for measurement purpouses historic measures
        d = 0  # distance between leds_dict on chart
        for led_name in leds_dict:
            meas_dict[led_name]["index"] = list(meas_dict.keys()).index(led_name)
            meas_dict[led_name]["brightness"].append(((leds_dict[led_name]["dominant_color"][0] +
                                                       leds_dict[led_name]["dominant_color"][1] +
                                                       leds_dict[led_name]["dominant_color"][2]) / 3) // 1)
            meas_dict[led_name]["r"].append(leds_dict[led_name]["dominant_color"][0])
            meas_dict[led_name]["g"].append(leds_dict[led_name]["dominant_color"][1])
            meas_dict[led_name]["b"].append(leds_dict[led_name]["dominant_color"][2])

            # brightness in 0-255

            ax.plot(meas_dict[led_name]["brightness"],
                    np.zeros_like(meas_dict[led_name]["brightness"]) + int(meas_dict[led_name]["index"]) + d, '*',
                    meas_dict[led_name]["r"],
                    np.zeros_like(meas_dict[led_name]["r"]) + int(meas_dict[led_name]["index"]) + (2 / 4) + d, '*',
                    meas_dict[led_name]["g"],
                    np.zeros_like(meas_dict[led_name]["g"]) + int(meas_dict[led_name]["index"]) + (3 / 4) + d, '*',
                    meas_dict[led_name]["b"],
                    np.zeros_like(meas_dict[led_name]["b"]) + int(meas_dict[led_name]["index"]) + 1 + d, '*', )
            d += 1
        print(i)

    print(meas_dict)
    plt.show()
    for led in meas_dict.keys():
        meas_dict[led]["brightness_low"] = int(0.5 * min(meas_dict[led]["brightness"]))
        meas_dict[led]["r_low"] = int(0.9 * min(meas_dict[led]["r"]))
        meas_dict[led]["r_high"] = int(1.1 * max(meas_dict[led]["r"]))
        meas_dict[led]["g_low"] = int(0.9 * min(meas_dict[led]["g"]))
        meas_dict[led]["g_high"] = int(1.1 * max(meas_dict[led]["g"]))
        meas_dict[led]["b_low"] = int(0.9 * min(meas_dict[led]["b"]))
        meas_dict[led]["b_high"] = int(1.1 * max(meas_dict[led]["b"]))
    return meas_dict
### Program


#init = 'examples/init.jpg'
url = 'http://192.168.8.105/html/cam_pic_new.php?time=1604595629853&pDelay=40000'

snap = captureSnap(url)
r = cv2.selectROI("ROI", snap)
cv2.destroyWindow('ROI')
imCrop = snap[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
leds = detectLeds(imCrop, 0.05, 1500, 2200)
translateDictionary(leds)
measurement_dict = chartLeds(5, leds)
print(measurement_dict)
leds = readStatesMeasured(imCrop, leds, measurement_dict)

# for led in leds:
#     print(led["dominant_color"], measurement_dict[led]["r_low"], measurement_dict[led]["r_high"], measurement_dict[led]["g_low"], measurement_dict[led]["g_high"], measurement_dict[led]["b_low"], measurement_dict[led]["b_high"])

for led in leds.keys():
    print(led + " state is: " + leds[led]["led_state"])

#from functions import detectLeds, readStates, renameLed, url