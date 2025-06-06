import cv2
import pytesseract
import numpy as np
from matplotlib import pyplot as plt

class Statistic:
    def __init__(self, name):
        self.name = name
        self.imagePath = "images/" + name + ".png"
        self.value = "0"
        self.template = cv2.imread(self.imagePath, cv2.IMREAD_GRAYSCALE)
        assert self.template is not None, f"Template with name {self.name} could not be found."
    def match(self, target):
        screenshot = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screenshot, self.template, cv2.TM_CCOEFF)
        threshold = 0.8  
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        thresh = 255 - cv2.threshold(screenshot, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        roi = thresh[top_left[1] + 50:top_left[1] + 80, top_left[0]:top_left[0] + 62]
        # roi = thresh[top_left[1]:top_left[1] + 80, top_left[0]:top_left[0] + 60]
        data = pytesseract.image_to_string(roi, lang='eng',config='--psm 8 -c tessedit_char_whitelist=0123456789x')
        if not data:
            return
        if data[0] == "$" or int(data) > 999:
            data = data[1:]
        self.value = data
        print(self.name + " " + self.value)
        cv2.imshow('thresh', thresh)
        cv2.imshow('ROI', roi)
        cv2.waitKey()    
        # w, h = self.template.shape[::-1]
        # bottom_right = (top_left[0] + w, top_left[1] + h)
        # cv2.rectangle(screenshot,top_left, bottom_right, 255, 2)
        # plt.subplot(121),plt.imshow(result,cmap = 'gray')
        # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(screenshot,cmap = 'gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # plt.show()

image = "im4.png"

hh = Statistic("HeroHealth")
hh.match(image)

hs = Statistic("HeroSpeed")
hs.match(image)

hr = Statistic("HeroRate")
hr.match(image)

hd = Statistic("HeroDamage")
hd.match(image)

th = Statistic("TowerHealth")
th.match(image)

tra = Statistic("TowerRange")
tra.match(image)

tr = Statistic("TowerRate")
tr.match(image)

td = Statistic("TowerDamage")
td.match(image)
