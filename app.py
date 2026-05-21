import logging

import streamlit as st

from gui import db
from gui.theme import GLOBAL_CSS
from gui.telas import dashboard, fichas, login

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

st.set_page_config(
    page_title="Bereshit",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


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

usuario    = st.session_state.usuario
role       = st.session_state.role
eh_mestre  = role == "mestre"

with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:8px 0 14px;border-bottom:1px solid #1a1a2a;margin-bottom:10px;'>
        <div style='font-size:26px;'>⚔️</div>
        <div style='font-family:Cinzel,serif;font-size:14px;letter-spacing:.18em;color:#c8b89a;font-weight:700;'>BERESHIT</div>
        <div style='font-size:12px;color:#5a4a30;letter-spacing:.06em;margin-top:2px;'>בְּרֵאשִׁית</div>
        <div style='font-size:9px;color:#3a3a5a;letter-spacing:.06em;margin-top:2px;'>v0.3 · protótipo</div>
    </div>
    <div style='font-size:9px;letter-spacing:.14em;color:#5a4a30;margin:0 0 6px 4px;'>
        {'— MESTRE —' if eh_mestre else '— JOGADOR —'}
    </div>
    """, unsafe_allow_html=True)

    tela = st.session_state.tela
    nav_items = [
        ("📊", "Dashboard", "dashboard"),
        ("📜", "Fichas",    "fichas"),
    ]
    for icon, label, key in nav_items:
        ativo = tela == key or (key == "fichas" and tela in ("fichas",))
        if st.button(
            f"{icon} {label}",
            use_container_width=True,
            type="primary" if ativo else "secondary",
            key=f"nav_{key}",
        ):
            st.session_state.tela = key
            st.rerun()

    st.divider()
    st.markdown(f"""
    <div style='padding:6px 4px;'>
        <div style='font-size:12px;color:#c8b89a;font-weight:500;'>{usuario}</div>
        <div style='font-size:10px;color:#5a4a30;'>{'Mestre de Jogo' if eh_mestre else 'Jogador'}</div>
    </div>
    """, unsafe_allow_html=True)

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
