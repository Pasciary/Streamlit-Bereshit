import streamlit as st

from gui import client
from gui.theme import GLOBAL_CSS
from gui.telas import login, dashboard, fichas, ficha_detalhe, mesa, selecao_campanha

st.set_page_config(
    page_title="Bereshit",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

if client.MOCK_ATIVO:
    st.sidebar.info("🧪 Modo **mock** — dados fictícios (sem API).")

# estado inicial
if "logado" not in st.session_state:
    st.session_state.logado = False
if "tela" not in st.session_state:
    st.session_state.tela = "login"

def ir_para(tela):
    st.session_state.tela = tela
    st.rerun()

# login
if not st.session_state.logado:
    login.mostrar()
    st.stop()

usuario = st.session_state.get("usuario", {})
if not isinstance(usuario, dict):
    st.session_state.clear()
    st.rerun()

# ── GATE DE CAMPANHA ─────────────────────
if not st.session_state.get("campanha_ativa"):
    selecao_campanha.mostrar()
    st.stop()

campanha_ativa = st.session_state.get("campanha_ativa", {})
eh_mestre = usuario.get("role") == "mestre"

# ── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:8px 0 14px;border-bottom:1px solid #1a1a2a;margin-bottom:10px;'>
        <div style='font-size:26px;'>⚔️</div>
        <div style='font-family:Cinzel,serif;font-size:14px;letter-spacing:.18em;color:#c8b89a;font-weight:700;'>BERESHIT</div>
        <div style='font-size:12px;color:#5a4a30;letter-spacing:.06em;margin-top:2px;'>בְּרֵאשִׁית</div>
        <div style='font-size:9px;color:#3a3a5a;letter-spacing:.06em;margin-top:2px;'>v0.3 · protótipo</div>
        <div style='font-size:10px;color:#6a5a40;margin-top:8px;padding-top:6px;
                    border-top:1px solid #1a1a2a;'>{campanha_ativa.get('nome','')}</div>
    </div>
    <div style='font-size:9px;letter-spacing:.14em;color:#5a4a30;margin:0 0 6px 4px;'>
        {'— MESTRE —' if eh_mestre else '— JOGADOR —'}
    </div>
    """, unsafe_allow_html=True)

    tela = st.session_state.tela

    nav_items = [
        ("📊", "Dashboard",  "dashboard"),
        ("📜", "Fichas",     "fichas"),
        ("🎲", "Mesa",       "mesa"),
        ("📖", "Grimório",   "grimorio"),
        ("🗒️", "Notas",      "notas"),
    ]
    for icon, label, key in nav_items:
        ativo = tela in [key, f"{key}_detalhe"]
        if st.button(f"{icon} {label}", use_container_width=True,
                     type="primary" if ativo else "secondary", key=f"nav_{key}"):
            ir_para(key)

    st.divider()
    st.markdown(f"""
    <div style='padding:6px 4px;'>
        <div style='font-size:12px;color:#c8b89a;font-weight:500;'>{usuario.get('nome','?')}</div>
        <div style='font-size:10px;color:#5a4a30;'>{'Mestre de Jogo' if eh_mestre else 'Jogador'}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Trocar Campanha", use_container_width=True):
        del st.session_state["campanha_ativa"]
        st.session_state.tela = "dashboard"
        st.rerun()
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ── ROTEADOR ─────────────────────────────
tela = st.session_state.tela

if tela == "dashboard":
    dashboard.mostrar()
elif tela in ("fichas", "criar_ficha"):
    fichas.mostrar()
elif tela == "ficha_detalhe":
    ficha_detalhe.mostrar()
elif tela == "mesa":
    mesa.mostrar()
elif tela == "grimorio":
    st.title("📖 Grimório")
    st.info("Em construção — catálogo de magias em breve!")
elif tela == "notas":
    st.title("🗒️ Notas")
    st.info("Em construção — notas de campanha em breve!")
else:
    ir_para("dashboard")
