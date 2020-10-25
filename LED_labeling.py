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

detect_th = 0.25

image_rgb = io.imread('http://192.168.0.192:8080/shot.jpg')
#image_rgb = io.imread('examples/leds_off.jpg')
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

leds = {} #led objects

for region in regionprops(label_image):
    # take regions with large enough areas

    if region.area > 1000:
        # draw rectangle around segmented item
        minr, minc, maxr, maxc = region.bbox

        cropped = image_rgb[minr:maxr, minc:maxc]
        skimage.io.imsave("temp/" + str(region.label)+".jpg", cropped)
        color_thief = ColorThief("temp/" + str(region.label)+".jpg")
        dominant_color = color_thief.get_color(quality=1)
        max_channel_index = dominant_color.index(max(dominant_color))

        brightness_th = 100
        print(region.area)
        ## TBD: Set color boundaries for better recognition
        if max(dominant_color) > brightness_th:
            if dominant_color[0] != dominant_color[1] and dominant_color[1] != dominant_color[2] and dominant_color[0] != dominant_color[2]:
                if dominant_color[0] > 140 and dominant_color[1] < 120 and dominant_color[2] < 120: state = "red";
                elif dominant_color[0] > 180 and dominant_color[1] > 180: state = "yellow";
                elif dominant_color[2] > 140: state = "blue";
            else: state = "not recognized";
        else: state = "off"

        leds[region.label] = {"led_state":state, "dominant_color":dominant_color, "top_border":minr, "left_border":minc, "bottom_border":maxr, "right_border":maxc}
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)
        plt.text(minc, minr, leds[region.label]['led_state'], color = "r")

ax.set_axis_off()
plt.tight_layout()
plt.show()

