import sqlite3
from config import Config

def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table cultures
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cultures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            type_sol TEXT,
            periode_plantation TEXT,
            duree_croissance TEXT,
            conseils TEXT
        )
    ''')

    # Table maladies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maladies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            culture_affectee TEXT,
            symptomes TEXT,
            traitement TEXT
        )
    ''')

    # Table conversations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur TEXT,
            question TEXT,
            reponse TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée !")

if __name__ == '__main__':
    init_db()