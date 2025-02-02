import streamlit as st
import json
import base64
from PIL import Image
import database
import os

# Charger les questions
with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)["questions"]

# Initialiser la base de données
database.init_db()

if "page" not in st.session_state:
    st.session_state.page = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}

st.title("🔹 Recrutement - Cyber Soldats")

# Page 0 : Informations personnelles
if st.session_state.page == 0:
    st.subheader("📝 Informations personnelles")

    # Récupérer les informations personnelles du candidat
    st.session_state.responses["nom"] = st.text_input("Nom *", "")
    st.session_state.responses["telephone"] = st.text_input("Téléphone *", "")
    st.session_state.responses["email"] = st.text_input("Email *", "")

    # Ajout du champ photo
    photo = st.file_uploader("Télécharger votre photo", type=["jpg", "png", "jpeg"])
    if photo:
        # Vérification de la taille de l'image (max 3 Mo)
        if len(photo.getvalue()) > 3 * 1024 * 1024:
            st.error("La photo ne doit pas dépasser 3 Mo.")
        else:
            image = Image.open(photo)
            st.image(image, caption="Photo téléchargée", use_column_width=True)
            img_bytes = photo.read()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            st.session_state.responses["photo_base64"] = img_base64
    
    # Ajout des amis
    st.session_state.responses["amis"] = {
        "père": st.text_input("Nom du père (ou proche 1)", ""),
        "mère": st.text_input("Nom de la mère (ou proche 2)", ""),
        "frères_soeurs": st.text_input("Nom des frères et sœurs (ou proche 3)", "")
    }

# Pages suivantes : Questions
elif st.session_state.page > 0:
    start = (st.session_state.page - 1) * 5
    end = start + 5
    for i, question in enumerate(questions[start:end]):
        st.session_state.responses[f"q{start + i + 1}"] = st.radio(
            question, ["Très bon", "Bon", "Neutre", "Mauvais", "Très mauvais"], index=2
        )

# Navigation
col1, col2 = st.columns(2)

if st.session_state.page > 0:
    if col1.button("⬅ Précédent"):
        st.session_state.page -= 1
        st.rerun()

if st.session_state.page < (len(questions) // 5):
    if col2.button("Suivant ➡"):
        st.session_state.page += 1
        st.rerun()
else:
    if st.button("✅ Soumettre"):
        score = sum([5 - ["Très bon", "Bon", "Neutre", "Mauvais", "Très mauvais"].index(ans) 
                     for k, ans in st.session_state.responses.items() if k.startswith("q")])
        
        # Sauvegarde des réponses dans la base de données
        database.save_response(st.session_state.responses["nom"], score, st.session_state.responses)
        st.success("✅ Votre réponse a été enregistrée avec succès ! Un administrateur analysera votre profil.")
