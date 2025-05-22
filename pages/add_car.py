import streamlit as st
from data_manager import load_data, save_data, add_car, add_user_to_car
import pandas as pd
st.set_page_config(page_title="Nou cotxe", layout="centered")

data = load_data()
with st.container(border=True):
    st.markdown("#### ➕ Afegir cotxe")

    # ---------- Inicialitzacions ----------
    st.session_state.setdefault("nou_usuari", "")
    st.session_state.setdefault("reset_nou_usuari", False)
    st.session_state.setdefault("nou_nom", "")
    st.session_state.setdefault("reset_nou_nom", False)
    st.session_state.setdefault("emoji_label", "🚗 Cotxe")
    st.session_state.setdefault("reset_emoji_label", False)
    st.session_state.setdefault("nou_cotxe_usuaris", [])

    # ---------- Resets abans de renderitzar ----------
    if st.session_state.reset_nou_usuari:
        st.session_state.nou_usuari = ""
        st.session_state.reset_nou_usuari = False

    if st.session_state.reset_nou_nom:
        st.session_state.nou_nom = ""
        st.session_state.reset_nou_nom = False

    if st.session_state.reset_emoji_label:
        st.session_state.emoji_label = "🚗 Cotxe"
        st.session_state.reset_emoji_label = False

    # ---------- Widgets ----------
    nou_nom = st.text_input("Nom del nou cotxe", key="nou_nom", max_chars=20)

    emoji_options = {
        "🚗 Cotxe": "🚗",
        "🚙 SUV": "🚙",
        "🚐 Furgoneta": "🚐",
        "🏍️ Moto": "🏍️",
        "🛵 Escúter": "🛵",
        "🚲 Bicicleta": "🚲",
        "🛻 Pickup": "🛻",
    }
    emoji_label = st.selectbox("Emoji", list(emoji_options.keys()), key="emoji_label")
    emoji = emoji_options[emoji_label]

    nou_usuari = st.text_input("Nom d'un usuari per afegir", key="nou_usuari", max_chars=20)

    if st.button("➕ Afegir usuari"):
        if nou_usuari.strip():
            st.session_state.nou_cotxe_usuaris.append(nou_usuari.strip())
            st.session_state.reset_nou_usuari = True
            st.rerun()
        else:
            st.warning("Introdueix un nom vàlid.")

    # ---------- Mostrar usuaris ----------
    if st.session_state.nou_cotxe_usuaris:
        st.markdown("### 👥 Usuaris afegits")

        # Construïm DataFrame editable
        df = pd.DataFrame({
            "Usuari": st.session_state.nou_cotxe_usuaris,
            "Eliminar": [False] * len(st.session_state.nou_cotxe_usuaris)
        })

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="fixed",
            hide_index=True,
        )

        # Detectar quins usuaris s'han marcat per eliminar
        files_a_eliminar = edited_df[edited_df["Eliminar"] == True].index.tolist()

        if files_a_eliminar:
            if st.button("🗑️ Elimina seleccionats"):
                for i in sorted(files_a_eliminar, reverse=True):  # Eliminar de darrere cap a davant
                    st.session_state.nou_cotxe_usuaris.pop(i)
                st.rerun()

    # ---------- Crear cotxe ----------
    if st.button("✅ Crear cotxe"):
        data, new_car_id = add_car(data, nou_nom, emoji)
        for nom in st.session_state.nou_cotxe_usuaris:
            data, _ = add_user_to_car(data, new_car_id, nom)
        save_data(data)

        st.session_state.nou_cotxe_usuaris = []
        st.session_state.current_car = new_car_id
        st.session_state.reset_nou_nom = True
        st.session_state.reset_emoji_label = True
        st.session_state.reset_nou_usuari = True

        st.success(f"Cotxe {emoji} {nou_nom} creat amb usuaris!")
        st.switch_page("app.py")

    # ---------- Tornar ----------
    if st.button("← Tornar a la llista"):
        st.switch_page("app.py")
