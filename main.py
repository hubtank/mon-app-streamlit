import streamlit as st
from BiblioUnique import Database

bd = Database("data.db")
bd.creer_table("users", {"id": "integer primary key", "nom": "text", "age": "integer"})

st.title("App Streamlit + SQLite")
st.write("Bienvenue sur l'application Streamlit + SQLite")

name = st.text_input("Nom")
age = st.number_input("Âge", min_value=0, max_value=120)

if st.button("Ajouter"):
    bd.insert("users", {"nom": name, "age": age})
    st.success("Utilisateur ajouté avec succès")

st.write("Liste des utilisateurs")
users = bd.select("users")
for user in users:
    st.write(user)
