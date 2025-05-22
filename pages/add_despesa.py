import streamlit as st
from datetime import date
from data_manager import load_data, save_data, add_despesa

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
    
st.set_page_config(page_title="Afegir despesa", layout="centered")

# ---------- Formulari ----------
with st.form("form_despesa"):
    st.markdown("#### ➕ Afegir nova despesa")
    data_d = st.date_input("Data", value=date.today())
    pagador = st.selectbox("Qui ha pagat?", opcions_pagador)
    import_d = st.number_input("Import (€)", min_value=0.0, step=1.0)
    descripcio = st.text_input("Descripció", max_chars=100)
    
    if st.form_submit_button("Guardar despesa") and pagador and data_d:
        data = add_despesa(data, cotxe_id, pagador, import_d, descripcio, data_d.isoformat())
        save_data(data)
        st.success("Despesa afegida correctament ✅")
        st.switch_page("pages/details.py")

# Botó per tornar
if st.button("← Tornar al detall"):
    st.switch_page("pages/details.py")