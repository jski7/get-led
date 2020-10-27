import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import skimage
from colorthief import ColorThief
import time

from skimage import io
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb, rgb2gray

def getSnapshot(stream_url):
    webcam = cv2.VideoCapture(0)

def detectLeds(file, detect_th, min_size, max_size):

    #   Init lamp test
    #   Get a photo from camera when leds are on
    #   Create dict with all leds positions
    leds = {}                       # led objects
       # range of sizes for detected objects
    image_rgb = io.imread(file)
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
            leds["led_"+str(region.label)] = {"led_state": "null", "dominant_color": ("null","null","null"), "top": minr,
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
        image_rgb = io.imread(file)
        cropped = image_rgb[leds_dict[key]["top"]:leds_dict[key]["bottom"], leds_dict[key]["left"]:leds_dict[key]["right"]]
        skimage.io.imsave("temp/" + str(str(key)) + ".jpg", cropped,  check_contrast=False)
        color_thief = ColorThief("temp/" + str(str(key)) + ".jpg")
        dominant_color = color_thief.get_color(quality=1)
        ## TBD: Set color boundaries for better recognition
        state = "not recognized"
        if sum(dominant_color) > brightness_th:
            if dominant_color[0] != dominant_color[1] and dominant_color[1] != dominant_color[2] and dominant_color[0] != dominant_color[2]:
                if dominant_color[0] > 200 and \
                        dominant_color[1] < 200 and \
                        dominant_color[2] < 140:
                    state = "red"
                elif dominant_color[0] > 200 and \
                        dominant_color[1] > 200:
                    state = "yellow"
                elif dominant_color[2] > 200:
                    state = "green"
            else:
                state = "not recognized"
        else:
            state = "off"
        leds[key]["dominant_color"] = dominant_color
        leds[key]["led_state"] = state
    return leds

def renameLed(name,  obj):
    #   Edit name id of one led
    leds[name] = leds[obj]
    leds.pop(obj)

url = 'http://192.168.0.54:8081'

leds = detectLeds(url, 0.27, 1400,2500)

while 1==1:
    leds = readStates(url, leds, 200)
    print()
    for led in leds:
        print(str(led) + " " + leds[led]["led_state"])
        #print(leds[led]["dominant_color"])
    time.sleep(1)

#from functions import detectLeds, readStates, renameLed, url