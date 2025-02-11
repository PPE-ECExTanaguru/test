# À EXÉCUTER :
# pip install easyocr opencv-python matplotlib

import easyocr
import cv2
import matplotlib.pyplot as plt

# On Charge le modèle OCR et on choisit également les langues à analyser (ici français et anglais car plus intéressant pour notre analyse)
reader = easyocr.Reader(['fr', 'en'], verbose=False)

# Les différentes images : Choisir ensuite la bonne chaîne pour analyser l'image souhaitée :
img1 = "images/panneau_vitesse_30.jpg"
img2 = "images/pandemic.jpg"
img3 = "images/keywords-letters.jpg"
img4 = "images/communication.jpg"
img5 = "images/buildings.jpg"
img6 = "images/signage.jpg"
img7 = "images/words.jpg"

image_path = img2
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# On récupère le texte détecté dans une liste de chaînes de caractères pour pouvoir l'afficher ensuite
results = reader.readtext(image)
text_list = [text for (_, text, _) in results]
print("Texte détecté :", text_list)

# On décide également d'afficher l'image avec le texte détecté :
for (bbox, text, prob) in results:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis("off")
plt.show()
