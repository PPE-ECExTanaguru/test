import pytesseract
from PIL import Image

img1 = r"imagesPNG/panneau_vitesse_30.png"
img2 = r"imagesPNG/pandemic.png"
img3 = r"imagesPNG/keywords-letters.png"
img4 = r"imagesPNG/communication.png"
img5 = r"imagesPNG/buildings.png"
img6 = r"imagesPNG/signage.png"
img7 = r"imagesPNG/words.png"

text = pytesseract.image_to_string(Image.open(img6), lang="eng")
print(text)
