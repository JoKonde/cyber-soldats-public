import streamlit as st
import sqlite3
import base64
from PIL import Image
import bcrypt

# Fonction pour se connecter à la base de données et récupérer les candidats
def get_candidates():
    conn = sqlite3.connect('recrutement.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidats")
    candidates = cursor.fetchall()
    conn.close()
    return candidates

# Fonction pour afficher l'image en base64
def display_image_from_base64(base64_str):
    img_data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(img_data))

# Fonction pour vérifier le mot de passe administrateur
def verify_password():
    password = st.text_input("Mot de passe administrateur", type="password")
    if password:
        # Le mot de passe administrateur est stocké sous forme hachée dans la base de données
        stored_hash = "$2b$12$XQeFzR8gd11YOJvjSgN2YOy28ijyqAGKl57RVZQ5sBsnVh9pVWvbe"  # exemple de hachage bcrypt
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
    return False

# Protection par mot de passe pour l'accès à l'admin
if not verify_password():
    st.error("Mot de passe incorrect. Accès refusé.")
else:
    st.title("Page d'administration")

    # Afficher les candidats
    candidates = get_candidates()
    if candidates:
        st.write("Liste des candidats inscrits :")
        for candidate in candidates:
            # Afficher les informations de base du candidat
            st.write(f"Nom: {candidate[1]} {candidate[2]} | Email: {candidate[4]} | Profession: {candidate[5]}")
            
            # Afficher la photo du candidat
            if candidate[8]:  # Vérifier si la photo existe
                st.image(display_image_from_base64(candidate[8]), caption="Photo du candidat", use_column_width=True)
            else:
                st.write("Aucune photo disponible.")
    else:
        st.write("Aucun candidat trouvé.")
