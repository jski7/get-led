import os  # biblioteka do obsługi systemu
from math import sqrt  # pierwiastek
import skimage
from skimage import io
import matplotlib.pyplot as plt  # create plot
from skimage.color import rgb2gray
from skimage.feature import blob_dog, blob_log, blob_doh  # algorytmy wykrywamnia

filename = os.path.join(skimage.data_dir, 'leds2.jpg')
image = io.imread(filename)
image_gray = rgb2gray(image)

#min, max sigma dopasować do wielkości ledów

blobs_log = blob_log(image_gray, min_sigma=5, max_sigma=6, num_sigma=5, threshold=.2, overlap=0.05)
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

blobs_dog = blob_dog(image_gray, min_sigma=5, max_sigma=6, threshold=.4, overlap=0.05)
blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

blobs_list = [blobs_log, blobs_dog]
colors = ['yellow', 'lime']
titles = ['Laplacian of Gaussian', 'Difference of Gaussian']
sequence = zip(blobs_list, colors, titles)

fig, axes = plt.subplots(1, 2, figsize=(9, 3), sharex=True, sharey=True)
ax = axes.ravel()

for idx, (blobs, color, title) in enumerate(sequence):
    ax[idx].set_title(title)
    ax[idx].imshow(image)
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
        ax[idx].add_patch(c)
    ax[idx].set_axis_off()

plt.tight_layout()
plt.show()