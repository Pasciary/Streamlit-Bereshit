import streamlit as st

st.set_page_config(
    # Configuração da página
    page_title="Bereshit",
    page_icon="⚔️",
    layout="wide",
)

from gui.telas import login

# Define o estado inicial do login
if "logado" not in st.session_state:
    st.session_state.logado = False

# Se não estiver logado, mostra a tela de login e para login completo
if not st.session_state.logado:
    login.mostrar()
    st.stop()

with st.sidebar:
    st.title("Bereshit")
    
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.tela = "dashboard"
        st.rerun()
    
    if st.button("📜 Fichas", use_container_width=True):
        st.session_state.tela = "fichas"
        st.rerun()



if "tela" not in st.session_state:
    st.session_state.tela = "dashboard"

tela = st.session_state.tela


if tela == "dashboard":
    st.write("você está no dashboard")
elif tela == "fichas":
    st.write("você está nas fichas")
else:
    st.write(f"tela '{tela}' não existe ainda")