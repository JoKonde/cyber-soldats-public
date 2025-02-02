import sqlite3
import os

DB_PATH = "recrutement.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Création de la table 'candidats'
        cursor.execute("""
        CREATE TABLE candidats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    postnom TEXT,
    prenom TEXT,
    telephone TEXT,
    email TEXT,
    profession TEXT,
    description_profession TEXT,
    adresse_residentielle TEXT,
    photo_base64 TEXT,
    mot_de_passe TEXT
)
""")
        conn.commit()
        conn.close()

def save_response(nom, score, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Convertir les amis en format JSON
    amis_data = json.dumps(data.get("amis", {}))

    cursor.execute("""
    INSERT INTO candidats (nom, telephone, email, photo, amis, score)
    VALUES (?, ?, ?, ?, ?, ?)""",
                   (data.get("nom"), data.get("telephone"), data.get("email"), 
                    data.get("photo_base64"), amis_data, score))
    
    conn.commit()
    conn.close()
