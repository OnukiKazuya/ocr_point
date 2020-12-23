from PIL import Image, ImageDraw, ImageFont
from PIL import Image
import sys
import pyocr
import pyocr.builders
import cv2
import math
 
def ocr(img_path="./public/test.png"):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]
    print(f"Will use tool {tool.get_name()}")
    txt = tool.image_to_string(
        Image.open(img_path),
        lang="eng",
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    print(txt)

def save_rectangle(save_img_path="./public/template.png"):
    im = Image.new("RGB", (250, 150), color=(255,255,255))
    draw = ImageDraw.Draw(im)
    draw.rectangle((10, 10, 210, 110), fill="white", outline="black")
    draw.rectangle((10, 10, 30, 30), fill="black")
    draw.rectangle((190, 10, 210, 30), fill="black")
    draw.rectangle((10, 90, 30, 110), fill="black")
    im.save(save_img_path)

def template_match(img_path="./public/test__90.png", template_path="./public/template.png"):
    # 画像読込
    img = cv2.imread(img_path)
    template = cv2.imread(template_path)
    _, w, h = template.shape[::-1]

    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    btm_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img,top_left, btm_right, 255, 2)

    cv2.imshow("test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import copy
    im = Image.new("RGB", (500, 500), color=(255, 255, 255))
    font = ImageFont.truetype("Keyboard.ttf", 32)
    draw = ImageDraw.Draw(im)
    draw.rectangle((250, 250, 450, 350), fill="white", outline="black")
    draw.rectangle((250, 250, 280, 280), fill="black")
    draw.rectangle((420, 250, 450, 280), fill="black")
    draw.rectangle((250, 320, 280, 350), fill="black")
    draw.text((300, 300), "96", fill="red",font=font)
    # im = im.rotate(90)
    im.save("./public/test.png")

    ## save template.png
    save_rectangle()

    ## template matching
    template_match()

    ##
    ocr("./public/test.png")