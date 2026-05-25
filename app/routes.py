import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, render_template
from app.chatbot import chatbot_repondre

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        question = data.get('message', '')
        if not question:
            return jsonify({'erreur': 'Message vide'}), 400
        reponse = chatbot_repondre(question)
        return jsonify({'reponse': reponse})
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500

@main.route('/historique', methods=['GET'])
def historique():
    try:
        from app.database import get_db
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT question, reponse, date FROM conversations ORDER BY date DESC LIMIT 20"
        )
        conversations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(conversations)
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500

@main.route('/alertes', methods=['GET'])
def alertes():
    try:
        ville = request.args.get('ville', 'Ouagadougou')
        culture = request.args.get('culture', '')
        from app.meteo import verifier_alertes_meteo, verifier_alertes_maladies
        toutes_alertes = []
        toutes_alertes += verifier_alertes_meteo(ville)
        if culture:
            toutes_alertes += verifier_alertes_maladies(culture)
        return jsonify(toutes_alertes)
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500

@main.route('/historique-page')
def historique_page():
    return render_template('historique.html')