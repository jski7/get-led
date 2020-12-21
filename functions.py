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
        # state = "not recognized"
        # if sum(dominant_color) > brightness_th:
        #     if dominant_color[0] != dominant_color[1] and dominant_color[1] != dominant_color[2] and dominant_color[0] != dominant_color[2]:
        #         if dominant_color[0] in range(30, 50) and\
        #                 dominant_color[1] in range(200,230) and\
        #                 dominant_color[2] in range(215,255):
        #             state = "yellow"
        #         elif dominant_color[0] in range(30, 50) and \
        #                     dominant_color[1] in range(220, 255) and \
        #                     dominant_color[2] in range(5, 40):
        #             state = "green"
        #         elif dominant_color[0] in range(0, 30) and \
        #                     dominant_color[1] in range(0, 210) and \
        #                     dominant_color[2] in range(30, 255):
        #             state = "red"
        #     else:
        #         state = "not recognized"
        # else:
        #     state = "off"
        leds[key]["dominant_color"] = dominant_color
        # leds[key]["led_state"] = state
    return leds


def readStatesMeasured(file, leds_dict, measures):
    #   Get a photo
    #   Check state of leds
    #   put it into dict from detect leds
    for key in leds_dict.keys():
        image_rgb = file
        cropped = image_rgb[leds_dict[key]["top"]:leds_dict[key]["bottom"],
                  leds_dict[key]["left"]:leds_dict[key]["right"]]
        skimage.io.imsave("temp/" + str(str(key)) + ".jpg", cropped, check_contrast=False)
        color_thief = ColorThief("temp/" + str(str(key)) + ".jpg")
        dominant_color = color_thief.get_color(quality=1)
        ## TBD: Set color boundaries for better recognition
        for init_state in measures[key].keys():
            # image_rgb = io.imread(file)
            state = "not recognized"
            # print(measures[key][init_state]["brightness_low"], int(sum(dominant_color)/3))
            # print(measures[key][init_state]["r_low"], measures[key][init_state]["r_high"])
            # print(measures[key][init_state]["g_low"], measures[key][init_state]["g_high"])
            # print(measures[key][init_state]["b_low"], measures[key][init_state]["b_high"])
            if int(sum(dominant_color)) / 3 > measures[key][init_state]["brightness_low"]:
                if dominant_color[0] in range(measures[key][init_state]["r_low"], measures[key][init_state]["r_high"]) and \
                        dominant_color[1] in range(measures[key][init_state]["g_low"], measures[key][init_state]["g_high"]) and \
                        dominant_color[2] in range(measures[key][init_state]["b_low"], measures[key][init_state]["b_high"]):
                    state = init_state
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


def measureStates(count, leds_dict):

    # dict={
    #     led:{
    #         state:
    #             {thresholds
    #              }
    #     }
    # }

    temp_measures = {}
    for led in leds_dict.keys():
        temp_measures[led] = {"brightness": [], "r": [], "g": [], "b": []}

    fig, ax = plt.subplots()
    ax.set(xlabel='measurements', title='values measured for red led')

    for i in range(0, count):
        print("measurement " + str(i))
        snap = captureSnap(url)
        imCrop = snap[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        leds_dict = readStates(imCrop, leds_dict, 30)

        print()
        d = 0  # distance between leds_dict on chart
        for led_name in leds_dict.keys():
            temp_measures[led_name]["brightness"].append((int((sum(leds_dict[led_name]["dominant_color"])) / 3)))
            temp_measures[led_name]["r"].append(leds_dict[led_name]["dominant_color"][0])
            temp_measures[led_name]["g"].append(leds_dict[led_name]["dominant_color"][1])
            temp_measures[led_name]["b"].append(leds_dict[led_name]["dominant_color"][2])
            temp_measures[led_name]["index"] = list(temp_measures.keys()).index(led_name)

            # for measurement purpouses historic measures
            # brightness in 0-255
            ax.plot(temp_measures[led_name]["brightness"],
                np.zeros_like(temp_measures[led_name]["brightness"]) + int(temp_measures[led_name]["index"]) + d, '*',
                temp_measures[led_name]["r"],
                np.zeros_like(temp_measures[led_name]["r"]) + int(temp_measures[led_name]["index"]) + (2 / 4) + d, '*',
                temp_measures[led_name]["g"],
                np.zeros_like(temp_measures[led_name]["g"]) + int(temp_measures[led_name]["index"]) + (3 / 4) + d, '*',
                temp_measures[led_name]["b"],
                np.zeros_like(temp_measures[led_name]["b"]) + int(temp_measures[led_name]["index"]) + 1 + d, '*', )
            d += 1
    #plt.show()

    if 'meas_dict' not in locals():
        meas_dict = {}

    for led_name in leds_dict.keys():
        init_state = input("What is the current state of led " + led_name + " ?\n")
        if led_name not in meas_dict:
            meas_dict[led_name] = {}
        if init_state not in meas_dict[led_name]:
            meas_dict[led_name][init_state] = temp_measures[led_name]
        else:
            meas_dict[led_name][init_state]["brightness"].append(temp_measures[led_name]["brightness"])
            meas_dict[led_name][init_state]["r"].append(temp_measures[led_name]["brightness"])
            meas_dict[led_name][init_state]["g"].append(temp_measures[led_name]["brightness"])
            meas_dict[led_name][init_state]["b"].append(temp_measures[led_name]["brightness"])
            meas_dict[led_name][init_state]["index"].append(temp_measures[led_name]["brightness"])

        meas_dict[led_name][init_state]["brightness_low"] = int(0.5 * min(meas_dict[led_name][init_state]["brightness"]))
        meas_dict[led_name][init_state]["r_low"] = int(0.9 * min(meas_dict[led_name][init_state]["r"]) - 2)
        meas_dict[led_name][init_state]["r_high"] = int(1.1 * max(meas_dict[led_name][init_state]["r"]) + 2)
        meas_dict[led_name][init_state]["g_low"] = int(0.9 * min(meas_dict[led_name][init_state]["g"]) - 2)
        meas_dict[led_name][init_state]["g_high"] = int(1.1 * max(meas_dict[led_name][init_state]["g"]) + 2)
        meas_dict[led_name][init_state]["b_low"] = int(0.9 * min(meas_dict[led_name][init_state]["b"]) - 2)
        meas_dict[led_name][init_state]["b_high"]= int(1.1 * min(meas_dict[led_name][init_state]["b"]) + 2)

    return meas_dict
### Program


#init = 'examples/init.jpg'
url = 'http://192.168.8.105/html/cam_pic_new.php?time=1604595629853&pDelay=40000'

snap = captureSnap(url)
r = cv2.selectROI("ROI", snap)
cv2.destroyWindow('ROI')
imCrop = snap[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
leds = detectLeds(imCrop, 0.05, 1500, 2200)
#translateDictionary(leds)
measurement_dict = measureStates(5, leds)
print(measurement_dict)
while 1==1:
    t = time.time()
    snap = captureSnap(url)
    print(time.time() - t)
    t = time.time()
    imCrop = snap[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    print(time.time() - t)
    t = time.time()
    leds = readStatesMeasured(imCrop, leds, measurement_dict)
    print(time.time() - t)
    t = time.time()
    for key in leds.keys():
        print(leds[key]["led_state"])
    print(time.time() - t)
# leds = measureStates(imCrop, leds, measurement_dict)
#
# # for led in leds:
# #     print(led["dominant_color"], measurement_dict[led]["r_low"], measurement_dict[led]["r_high"], measurement_dict[led]["g_low"], measurement_dict[led]["g_high"], measurement_dict[led]["b_low"], measurement_dict[led]["b_high"])
#
# for led in leds.keys():
#     print(led + " state is: " + leds[led]["led_state"])

#from functions import detectLeds, readStates, renameLed, url