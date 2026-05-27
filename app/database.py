import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3

def get_db_path():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base, 'database')
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'agriculteur.db')

def get_db():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur TEXT,
            question TEXT,
            reponse TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            telephone TEXT,
            province TEXT,
            alertes_sms INTEGER DEFAULT 1,
            date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("OK Base de donnees initialisee !")

if __name__ == '__main__':
    init_db()
