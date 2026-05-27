import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login_page():
    if session.get('user_id'):
        return redirect(url_for('main.index'))
    return render_template('login.html')

@auth.route('/register')
def register_page():
    if session.get('user_id'):
        return redirect(url_for('main.index'))
    return render_template('register.html')

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    mot_de_passe = data.get('mot_de_passe', '')
    if not email or not mot_de_passe:
        return jsonify({'erreur': 'Email et mot de passe requis'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utilisateurs WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    if not user or not check_password_hash(user['mot_de_passe'], mot_de_passe):
        return jsonify({'erreur': 'Email ou mot de passe incorrect'}), 401
    session['user_id'] = user['id']
    session['user_nom'] = user['nom']
    session['user_province'] = user['province']
    return jsonify({'success': True, 'nom': user['nom']})

@auth.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    nom = data.get('nom', '').strip()
    email = data.get('email', '').strip()
    mot_de_passe = data.get('mot_de_passe', '')
    telephone = data.get('telephone', '')
    province = data.get('province', '')
    if not nom or not email or not mot_de_passe:
        return jsonify({'erreur': 'Tous les champs sont requis'}), 400
    if len(mot_de_passe) < 6:
        return jsonify({'erreur': 'Mot de passe trop court (6 caractères minimum)'}), 400
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO utilisateurs (nom, email, mot_de_passe, telephone, province) VALUES (?, ?, ?, ?, ?)',
            (nom, email, generate_password_hash(mot_de_passe), telephone, province)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        session['user_id'] = user_id
        session['user_nom'] = nom
        session['user_province'] = province
        return jsonify({'success': True, 'nom': nom})
    except Exception as e:
        conn.close()
        return jsonify({'erreur': 'Email deja utilise'}), 400

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login_page'))

@auth.route('/api/user')
def get_user():
    if session.get('user_id'):
        return jsonify({'connecte': True, 'nom': session.get('user_nom'), 'province': session.get('user_province')})
    return jsonify({'connecte': False})
