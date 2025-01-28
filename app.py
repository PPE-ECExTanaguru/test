from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os

# Clé API pour OpenRouter
OPENROUTER_API_KEY = "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"
YOUR_APP_NAME = 'MonChatbotRGAA'
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Création de l'application Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "mysecretkey"  # Clé secrète pour sécuriser les sessions


# Fonction pour interagir avec l'IA
def analyze_code_with_ai(code, chat_history=None):
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

    # Ajouter le code à analyser
    messages.append({
        "role": "user",
        "content": f"Analyse le code suivant selon les critères RGAA pour l'accessibilité web :\n\n{code}"
    })

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


# Route pour servir le fichier HTML
@app.route('/')
def index():
    return render_template('RGAA_analyzer.html')


# Route pour analyser un code soumis par l'utilisateur
@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.json
    user_code = data.get('code')  # Code envoyé par l'utilisateur

    if user_code:
        # Récupérer l'historique des messages de la session
        chat_history = session.get('chat_history', [])

        # Obtenir l'analyse de l'IA
        ai_response = analyze_code_with_ai(user_code, chat_history)

        # Ajouter le code soumis et la réponse de l'IA à l'historique
        chat_history.append({"role": "user", "content": user_code})
        chat_history.append({"role": "assistant", "content": ai_response})

        # Mettre à jour l'historique dans la session
        session['chat_history'] = chat_history

        return jsonify({'response': ai_response})

    return jsonify({'response': "Aucun code fourni pour l'analyse."}), 400


# Route pour téléverser un fichier contenant du code
@app.route('/upload', methods=['POST'])
def upload_code_file():
    file = request.files.get('file')
    if file and file.filename:
        # Lire le contenu du fichier
        file_content = file.read().decode('utf-8')

        # Récupérer l'historique des messages de la session
        chat_history = session.get('chat_history', [])

        # Obtenir l'analyse de l'IA pour le contenu du fichier
        ai_response = analyze_code_with_ai(file_content, chat_history)

        # Ajouter le contenu soumis et la réponse de l'IA à l'historique
        chat_history.append({"role": "user", "content": file_content})
        chat_history.append({"role": "assistant", "content": ai_response})

        # Mettre à jour l'historique dans la session
        session['chat_history'] = chat_history

        return jsonify({'response': ai_response})

    return jsonify({'response': "Aucun fichier reçu ou fichier vide."}), 400


# Exécution de l'application Flask
if __name__ == "__main__":
    app.run(debug=True, port=7860)
