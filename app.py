import streamlit as st
from data_manager import (
    ensure_data_file, load_data, save_data,
    add_car, add_user_to_car
)

# Configuració i càrrega de dades
st.set_page_config(page_title="Cotxes compartits", layout="centered")
ensure_data_file()
data = load_data()

# Inject minimal CSS to center the button
st.markdown("""
    <style>
        .center-button-container {
            display: flex;
            justify-content: center;
            margin-top: 2rem;
        }
        .st-key-centered-btn {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        .centered-btn {
            font-size: 1.1rem;
            padding: 0.6rem 1.5rem;
            border-radius: 10px;
            border: 1px solid #ccc;
            background-color: white;
            cursor: pointer;
        }
        .centered-btn:hover {
            background-color: #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)


top = st.container()
car_list = st.container()
bottom = st.container()

# Inicialitzem cotxe seleccionat
if "current_car" not in st.session_state:
    st.session_state.current_car = None

with top:
    st.title("🚗 Cotxes")

# Llista de cotxes ordenats pel nom
cotxes = sorted(data["cars"].values(), key=lambda c: c["nom"])
with car_list:
    for cotxe in cotxes:
        if st.button(f"{cotxe['emoji']} {cotxe['nom']}", use_container_width=True):
            st.session_state.current_car = cotxe["id"]
            st.switch_page("pages/details.py")

with bottom:
    st.markdown("""
        <div class="center-button-container">
            <form action="/add_car">
                <button type="submit" class="centered-btn">➕</button>
            </form>
        </div>
        <style>
            .center-button-container {
                display: flex;
                justify-content: center;
                margin-top: 2rem;
            }
            .centered-btn {
                font-size: 1rem;
                padding: 0.6rem 0.6rem;
                border-radius: 30px;
                border: 1px solid #ccc;
                background-color: white;
                cursor: pointer;
            }
            .centered-btn:hover {
                background-color: #f0f0f0;
            }
        </style>
    """, unsafe_allow_html=True)
