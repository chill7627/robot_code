import cv2
import numpy as np
from matplotlib import pyplot as plt


image = cv2.imread("line4.jpg")
assert image is not None, "Unable to read file"

resized = cv2.resize(image, (320, 240))
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
# now blur the image to remove noise, in this case 5x5 chunks
blurred = cv2.blur(gray, (5, 5))

# images stored as top row of image 0 and bottom as max image height (240 in this case)
row = blurred[180].astype(np.int32) # picked row 180
# get list of diffs for every pixel in the row
diff = np.diff(row)
# find the max and min peaks in image
max_d = np.amax(diff, 0)
min_d = np.amin(diff, 0)
# find the indexes of maximums in the arrays, assuming there is only one global min and max
highest = np.where(diff == max_d)[0][0]
lowest = np.where(diff == min_d)[0][0]
middle = (highest + lowest)//2

# plot diffs and middle line between peaks
x = np.arange(len(diff)) # 0 to image width
plt.plot(x, diff)
plt.plot([middle, middle], [max_d, min_d], "r-")
plt.plot([lowest, lowest], [max_d, min_d], "g--")
plt.plot([highest, highest], [max_d, min_d], "g--")
plt.savefig("located_lines.png")