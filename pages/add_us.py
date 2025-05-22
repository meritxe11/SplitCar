import streamlit as st
from datetime import date
from data_manager import load_data, save_data, add_usu

# Comprovació de cotxe seleccionat
if "current_car" not in st.session_state:
    st.error("No hi ha cap cotxe seleccionat. Torna a la pàgina principal.")
    st.stop()

cotxe_id = st.session_state.current_car
data = load_data()
cotxe = data["cars"].get(cotxe_id)
# Llista d’usuaris disponibles
usuaris = cotxe.get("usuaris", [])
opcions_pagador = [u["nom"] for u in usuaris]


if cotxe is None:
    st.error("Aquest cotxe no existeix.")
    st.stop()
if not opcions_pagador:
    st.warning("Aquest cotxe no té cap usuari registrat.")
    st.stop()
    
st.set_page_config(page_title="Afegir ús", layout="centered")

# ---------- Formulari ----------
with st.form("form_despesa"):
    st.markdown("#### ➕ Afegir nou ús")
    data_u = st.date_input("Data", value=date.today())
    conductor = st.selectbox("Conductor", opcions_pagador)
    km_fets = st.number_input("Km recorreguts", min_value=1, step=1)
    descripcio = st.text_input("Descripció", max_chars=100)
    
    if st.form_submit_button("Guardar us") and conductor and data_u:
        data = add_usu(data, cotxe_id, conductor, km_fets, descripcio, data_u.isoformat())
        save_data(data)
        st.success("Ús afegit correctament ✅")
        st.switch_page("pages/details.py")

# Botó per tornar
if st.button("← Tornar al detall"):
    st.switch_page("pages/details.py")