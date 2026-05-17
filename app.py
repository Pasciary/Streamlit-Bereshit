import streamlit as st
from gui.telas import login

st.set_page_config(
    page_title="Bereshit",
    page_icon="⚔️",
    layout="wide",
)

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login.mostrar()
    st.stop()

if "tela" not in st.session_state:
    st.session_state.tela = "dashboard"

with st.sidebar:
    st.title("Bereshit")
    
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.tela = "dashboard"
        st.rerun()
    
    if st.button("📜 Fichas", use_container_width=True):
        st.session_state.tela = "fichas"
        st.rerun()

tela = st.session_state.tela

if tela == "dashboard":
    st.write("você está no dashboard")
elif tela == "fichas":
    st.write("você está nas fichas")
else:
    st.write(f"tela '{tela}' não existe ainda")