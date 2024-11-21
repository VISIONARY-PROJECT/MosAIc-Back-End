import random
import numpy as np
import cv2
import app
from PIL import ImageFont, ImageDraw, Image


def text_out(path):
    
    reader = app.text_model.Reader(['ko'], gpu = False)
    result = reader.readtext(path)

    texts = [i[1] for i in result]
    print("Detected Texts:", texts)

    combined_text = " ".join(texts)
    print("Combined Text:", combined_text)

    combined_text_file_path = "static/text/combined_text.txt"
    with open(combined_text_file_path, "w", encoding="utf-8") as file:
        file.write(combined_text)
    
    return combined_text 

# img = cv2.imread('/Users/hwiseon/Desktop/test2.jpg')
# img = Image.fromarray(img)
# font = ImageFont.truetype('font/hello.ttf', size=20)
# draw = ImageDraw.Draw(img)


# np.random.seed(42)
# COLORS = np.random.randint(0,255, size=(255,3),dtype = "uint8")

# for i in result:
#   x = i[0][0][0]
#   y = i[0][0][1]
#   w = i[0][1][0] - i[0][0][0]
#   h = i[0][2][1] - i[0][1][1]

#   color_idx = random.randint(0,254)
#   color = [int(c) for c in COLORS[color_idx]]


#   draw.rectangle(((x,y),(x+w,y+h)), outline=tuple(color), width = 2)
#   draw.text((int((x+x+w)/2), y-2), str(i[1]), font = font, fill =tuple(color))

# plt.imshow(img)
# plt.show()

