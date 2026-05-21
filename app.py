import logging

import streamlit as st

from gui import db
from gui.telas import dashboard, fichas, login

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

st.set_page_config(
    page_title="Bereshit",
    page_icon="⚔️",
    layout="wide",
)


@st.cache_resource
def _init_db() -> None:
    db.init_db()


_init_db()

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login.mostrar()
    st.stop()

if "tela" not in st.session_state:
    st.session_state.tela = "dashboard"

with st.sidebar:
    st.title("⚔️ Bereshit")
    st.caption(f"👤 {st.session_state.usuario} · {st.session_state.role}")

    st.divider()

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.tela = "dashboard"
        st.rerun()

    if st.button("📜 Fichas", use_container_width=True):
        st.session_state.tela = "fichas"
        st.rerun()

    st.divider()

    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()

tela = st.session_state.tela

if tela == "dashboard":
    dashboard.mostrar()
elif tela == "fichas":
    fichas.mostrar()
else:
    st.error(f"Tela '{tela}' não encontrada.")
