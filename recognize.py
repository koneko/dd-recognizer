import cv2
import pytesseract
from matplotlib import pyplot as plt

shouldShowROIandThresh = False
shouldShowTemplateMatch = False
image = "working.png"

class Statistic:
    def __init__(self, name):
        self.name = name
        self.imagePath = "images/" + name + ".png"
        self.value = "0"
        self.template = cv2.imread(self.imagePath, cv2.IMREAD_GRAYSCALE)
        assert self.template is not None, f"Template with name {self.name} could not be found."
    def match(self, target):
        screenshot = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screenshot, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        thresh = 255 - cv2.threshold(screenshot, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # roi means region of interest
        roi = thresh[top_left[1] + 45:top_left[1] + 80, top_left[0]:top_left[0] + 62]
        # roi = thresh[top_left[1]:top_left[1] + 80, top_left[0]:top_left[0] + 60]
        data = pytesseract.image_to_string(roi, lang='eng',config='--psm 8 -c tessedit_char_whitelist=0123456789x')
        data = data[:-1]

        if shouldShowROIandThresh:
            cv2.imshow('thresh', thresh)
            cv2.imshow('ROI', roi)
            cv2.waitKey()    
        
        if shouldShowTemplateMatch:
            w, h = self.template.shape[::-1]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(screenshot,top_left, bottom_right, 255, 2)
            plt.subplot(121),plt.imshow(result,cmap = 'gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(screenshot,cmap = 'gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.show()

        if not data:
            return

        dataInt = 0

        try:
            dataInt = int(data)
        except:
            print("Statistic is possibly censored.")
        
        if data[0] == "$" or dataInt > 999 or len(data) > 3:
            data = data[1:]

        if len(data) > 3:
            data = data[1:]

        self.value = data
        
        print(self.name + " " + self.value)

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
