# Utilisation de SceneTextRecognition.py

Cela permet de détecter du texte de plsuieurs langues sur les images. Ce n'est pas ultra performant mais ça marche quand même plutôt bien.
C'est très limité lorsque le texte est penché ou quand des polices particulières sont utilisées.
Également, il peut avoir la fâcheuse tendance à séparer des caractères qui appartiennent à la même chaîne.

Donc à retravailler mais c'est déjà un début

# Transformer_OCR.py

Pour l'instant, ça ne marche pas bien du tout.
Mais on peut y injecter son propre dataset afin de réentraîner le modèle sur les données qu'on a choisi.
Pour le futur ce serait intéressant d'annoter des images, d'envoyer le dataset CSV au modèle et voir si cela nous permet d'avoir des meilleurs performances.