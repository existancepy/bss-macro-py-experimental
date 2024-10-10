'''
import cv2
from PIL import Image

# Load the image
image_path = "test.png"
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to binarize the image (black and white)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Remove noise using a morphological operation (optional for cleaner text)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

cv2.imshow("final", morphed)
cv2.waitKey(0)
'''

from modules.submacros.hourlyReport import *
data = [7050303864024, 7005520975432, 7005526398974, 7009064072607, 7016030458099, 7022679645362, 7024981182451, 7025015837441, 7025651286620, 7026110228369, 7026385276441, 7026740054996, 7027156498221, 7027785697980, 7028080115983, 7028428510948, 7029098258219, 7029243723063, 7035319556762, 7042920045972, 7046457509998, 7046459100685, 7046870270990, 7047803314949, 7047956128467, 7048304113809, 7048683223478, 7049086769688, 7049714248069, 7050052974164]
print([millify(x) for x in data])
generateHourlyReport()