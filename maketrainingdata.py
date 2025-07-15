import os
import cv2
import pytesseract
# Folder containing your images
image_folder = "data"

# Supported image extensions
image_extensions = ('.png', '.jpg')

class Dummy:
    def __init__(self, name, iteration):
        self.name = name
        self.iteration = iteration
        self.imagePath = "images/" + name + ".png"
        self.value = "0"
        self.template = cv2.imread(self.imagePath, cv2.IMREAD_GRAYSCALE)
        assert self.template is not None, f"Template with name {self.name} could not be found."
    def match(self, target):
        screenshot = target
        result = cv2.matchTemplate(screenshot, self.template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        thresh = 255 - cv2.threshold(screenshot, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # roi means region of interest
        roi = screenshot[top_left[1] + 60:top_left[1] + 120, top_left[0] - 10:top_left[0] + 80]

        cv2.imshow('data/out/' + str(self.iteration) + "-" + self.name + ".png", roi)
        cv2.waitKey()
i = 0

for filename in os.listdir(image_folder):
    if filename.lower().endswith(image_extensions):
        image_path = os.path.join(image_folder, filename)
        i = i + 1
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print(f"Could not load image: {image_path}")
            continue

        print(f"Processing: {filename}")
        hh = Dummy("HeroHealth", i)
        hh.match(image)

        hs = Dummy("HeroSpeed", i)
        hs.match(image)

        hr = Dummy("HeroRate", i)
        hr.match(image)

        hd = Dummy("HeroDamage", i)
        hd.match(image)

        th = Dummy("TowerHealth", i)
        th.match(image)

        tra = Dummy("TowerRange", i)
        tra.match(image)

        tr = Dummy("TowerRate", i)
        tr.match(image)

        td = Dummy("TowerDamage", i)
        td.match(image)
        
        ab1 = Dummy("Ab1", i)
        ab1.match(image)

        ab2 = Dummy("Ab2", i)
        ab2.match(image)
