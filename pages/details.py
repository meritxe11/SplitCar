import streamlit as st
import pandas as pd
from datetime import date
from data_manager import (
    load_data, save_data,
    add_despesa, add_usu, calcular_balanc
)

# Comprovació de cotxe seleccionat
if "current_car" not in st.session_state:
    st.error("No hi ha cap cotxe seleccionat. Torna a la pàgina principal.")
    if st.button("Torna a la pàgina principal"):
        st.switch_page("app.py")
    st.stop()

cotxe = st.session_state.current_car


# Carreguem dades des de fitxer
data = load_data()
cotxe_data = data["cars"].get(cotxe, {"despeses": [], "usos": []})
cotxe_nom = cotxe_data.get("nom", "Cotxe")
cotxe_emoji = cotxe_data.get("emoji", "🚗")

# Llista d’usuaris disponibles
st.header(f"{cotxe_emoji} {cotxe_nom}")
if st.button(" ← ", type="tertiary" ):
    st.switch_page("app.py")
tab1, tab2, tab3 = st.tabs(["⛽️ Dipòsits", "🛣️ Usos", "📊 Balanç"])

# --- ⛽️ Dipòsits ---
with tab1:
    st.markdown("### 📅 Historial de dipòsits")
    if st.button("➕ Afegir despesa", use_container_width=True):
        st.switch_page("pages/add_despesa.py")

    if cotxe_data["despeses"]:
        df_d = pd.DataFrame({
            "Data": [d["data"] for d in cotxe_data["despeses"]],
            "Usuari": [d["usuari"] for d in cotxe_data["despeses"]],
            "Import": [f"{d["import"]} €" for d in cotxe_data["despeses"]],
            "Descripció": [d["descripcio"] for d in cotxe_data["despeses"]],
            "Eliminar": [False] * len(cotxe_data["despeses"])
        }).sort_values(by="Data", ascending=False)
        edited_df_d = st.data_editor(
            df_d,
            use_container_width=True,
            num_rows="fixed",
            hide_index=True,
        )
        files_a_eliminar_d = edited_df_d[edited_df_d["Eliminar"] == True].index.tolist()
        if files_a_eliminar_d:
            if st.button("🗑️ Elimina les despeses seleccionades"):
                for i in sorted(files_a_eliminar_d, reverse=True):
                    cotxe_data["despeses"].pop(i)
                data["cars"][cotxe] = cotxe_data
                save_data(data)
                st.rerun()
    else:
        st.info("Encara no hi ha cap despesa registrada.")
    

# --- 🛣️ Usos ---
with tab2:
    st.markdown("### 📅 Historial d'usos")
    if st.button("➕ Afegir ús", use_container_width=True):
        st.switch_page("pages/add_us.py")
    if cotxe_data["usos"]:
        df_u = pd.DataFrame({
            "Data": [d["data"] for d in cotxe_data["usos"]],
            "Usuari": [d["usuari"] for d in cotxe_data["usos"]],
            "Km": [f"{d["km"]} Km" for d in cotxe_data["usos"]],
            "Descripció": [d["descripcio"] for d in cotxe_data["usos"]],
            "Eliminar": [False] * len(cotxe_data["usos"])
        }).sort_values(by="Data", ascending=False)
        edited_df_u = st.data_editor(
            df_u,
            use_container_width=True,
            num_rows="fixed",
            hide_index=True,
        )
        files_a_eliminar_u = edited_df_u[edited_df_u["Eliminar"] == True].index.tolist()
        if files_a_eliminar_u:
            if st.button("🗑️ Elimina els usos seleccionats"):
                for i in sorted(files_a_eliminar_u, reverse=True):
                    cotxe_data["usos"].pop(i)
                data["cars"][cotxe] = cotxe_data
                save_data(data)
                st.rerun()
                st.rerun()
    else:
        st.info("Encara no hi ha cap ús registrat.")


# --- 📊 Balanç ---
with tab3:
    # st.markdown("### 💰 Balanç de despeses")
    despeses = cotxe_data["despeses"]
    usos = cotxe_data["usos"]
    
    resum_general, resum_per_usuari = calcular_balanc(despeses, usos, cotxe_data.get("usuaris", []))

    with st.container(border=True):
        st.markdown(f"### 📊 Resum del cotxe")
        st.markdown(f"- **Total despeses:** {resum_general['total_despesa']} €")
        st.markdown(f"- **Total quilòmetres:** {resum_general['total_km']} km")
    
    with st.container(border=True):
        st.markdown("### 👤 Resum per persona")
        for p in resum_per_usuari:
            difer = p["diferencia"]
            color = "green" if difer >= 0 else "red"
            emoji = "🟢" if difer >= 0 else "🔴"
            label = f""" {emoji} {p['usuari']}  :{color}[{difer:+.2f} €] """
            with st.expander(label, expanded=False):
                st.write(f"🛣️ **Km fets:** {p['km_fets']} km ({p['percentatge_km']}%)")
                st.write(f"💸 **Ha pagat:** {p['ha_pagat']} €")
                st.write(f"🧾 **Hauria de pagar:** {p['hauria_de_pagar']} €")
                st.write(f"📉 **Diferència:** `{difer:+.2f} €`")
