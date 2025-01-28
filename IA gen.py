from flask import Flask, render_template, request, jsonify, session
import requests
import json
import pytesseract
from PIL import Image
import PyPDF2
import os
import tempfile

# Clé API pour OpenRouter
OPENROUTER_API_KEY = "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"
YOUR_APP_NAME = 'MonChatbotHermes'
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Création de l'application Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "mysecretkey"  # Clé secrète pour sécuriser les sessions

# Fonction pour interagir avec l'IA
def chat_with_ai(prompt, chat_history=None):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "X-Title": YOUR_APP_NAME,
        "Content-Type": "application/json"
        
    }

    # Construire l'historique des messages
    messages = []
    if chat_history:
        for msg in chat_history:
            messages.append({"role": msg['role'], "content": msg['content']})
    
    # Ajouter le message utilisateur actuel à l'historique
    messages.append({"role": "user", "content": prompt})

    data = {
        "model": "nousresearch/hermes-3-llama-3.1-405b:free",
        "messages": messages
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Erreur : {response.status_code}, {response.text}"

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Fonction pour extraire le texte d'une image
def extract_text_from_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

# Route pour servir le fichier HTML
@app.route('/')
def index():
    return render_template('IA gen.html')

# Route pour gérer les messages du chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if user_message:
        # Récupérer l'historique des messages de la session
        chat_history = session.get('chat_history', [])

        # Obtenir la réponse de l'IA en utilisant l'historique des messages
        ai_response = chat_with_ai(user_message, chat_history)

        # Ajouter le message de l'utilisateur et la réponse de l'IA à l'historique
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": ai_response})

        # Mettre à jour l'historique des messages dans la session
        session['chat_history'] = chat_history

        return jsonify({'response': ai_response})

    return jsonify({'response': "Je n'ai pas compris votre message."}), 400

# Route pour téléverser un fichier et en extraire le texte
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and file.filename:
        # Création d'un fichier temporaire pour le téléversement
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            file_path = temp_file.name
            file.save(file_path)

        try:
            # Vérification du type de fichier et extraction du texte en conséquence
            if file.filename.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Prise en charge des fichiers d'image (PNG, JPG, JPEG)
                text = extract_text_from_image(file_path)
            else:
                return jsonify({'response': "Format de fichier non supporté."}), 400

            # Récupérer l'historique des messages de la session
            chat_history = session.get('chat_history', [])

            # Envoi du texte extrait à l'IA avec l'historique de la session
            ai_response = chat_with_ai(text, chat_history)

            # Ajouter le texte extrait et la réponse de l'IA à l'historique
            chat_history.append({"role": "user", "content": text})
            chat_history.append({"role": "assistant", "content": ai_response})

            # Mettre à jour l'historique des messages dans la session
            session['chat_history'] = chat_history

            return jsonify({'response': ai_response})

        finally:
            # Suppression du fichier après traitement
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError as e:
                    print(f"Erreur lors de la suppression du fichier : {e}")

    return jsonify({'response': "Aucun fichier reçu."}), 400

# Exécution de l'application Flask
if __name__ == "__main__":
    app.run(debug=True, port=7860)
