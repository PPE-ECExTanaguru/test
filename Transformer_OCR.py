# À EXÉCUTER :
# pip install torch torchvision transformers pillow

#Ne semble pas très bien marcher de mon côté.

import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image


processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")


image_path = "test_image.jpg"
image = Image.open(image_path).convert("RGB")

pixel_values = processor(images=image, return_tensors="pt").pixel_values

with torch.no_grad():
    generated_ids = model.generate(pixel_values)

# Conversion en texte
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(f"Texte reconnu : {generated_text}")
