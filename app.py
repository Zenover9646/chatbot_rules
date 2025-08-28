from flask import Flask, render_template, request, jsonify
import json
import re
import random
app = Flask(__name__)

# Charger les données depuis le fichier JSON
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Trouver une réponse appropriée
def get_response(user_input):
    data = load_data()
    user_input = user_input.lower()
    
    for item in data['responses']:
        for pattern in item['patterns']:
            if re.search(r'\b' + re.escape(pattern) + r'\b', user_input):
                return random.choice(item['responses'])
    
    return "Désolé, je n'ai pas compris. Pouvez-vous reformuler votre question sur les recettes ?"

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour recevoir les messages et renvoyer les réponses
@app.route('/get_response', methods=['POST'])
def bot_response():
    user_message = request.form['user_message']
    bot_reply = get_response(user_message)
    return jsonify({'response': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)