import streamlit as st

from config import api
from gui.utils import calc_pct


def mostrar() -> None:
    """Render the dashboard screen for the current user."""
    usuario = st.session_state.usuario
    role = st.session_state.role
    dados = api.get_dashboard(usuario, role)

    if role == "mestre":
        _dashboard_mestre(dados)
    else:
        _dashboard_jogador(usuario, dados)


def _dashboard_mestre(dados: dict) -> None:
    """Render the master dashboard with aggregate metrics and per-player fichas."""
    st.title("Painel do Mestre")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Fichas", dados["total_fichas"])
    with col2:
        st.metric("Fichas Ativas", dados["fichas_ativas"])
    with col3:
        st.metric("Jogadores", len(dados["jogadores"]))

    st.divider()
    st.subheader("Fichas por Jogador")

    fichas_por_jogador: dict[str, list] = {}
    for ficha in dados["fichas"]:
        fichas_por_jogador.setdefault(ficha["jogador"], []).append(ficha)

    if not fichas_por_jogador:
        st.info("Nenhuma ficha cadastrada ainda.")
        return

    for jogador, fichas in fichas_por_jogador.items():
        with st.expander(f"👤 {jogador} — {len(fichas)} ficha(s)", expanded=True):
            for ficha in fichas:
                _card_ficha(ficha)


def _dashboard_jogador(usuario: str, dados: dict) -> None:
    """Render the player dashboard with their own fichas."""
    st.title(f"Bem-vindo, {usuario}!")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Suas Fichas", dados["total_fichas"])
    with col2:
        st.metric("Fichas Ativas", dados["fichas_ativas"])

    st.divider()
    st.subheader("Seus Personagens")

    if not dados["fichas"]:
        st.info("Você ainda não tem fichas. Crie uma na seção Fichas!")
        return

    for ficha in dados["fichas"]:
        _card_ficha(ficha)


def _card_ficha(ficha: dict) -> None:
    """Render a compact ficha card with HP/MP progress bars."""
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"**{ficha['nome']}**")
            st.caption(f"{ficha['raca']} · {ficha['classe']} · Nível {ficha['nivel']}")
        with col2:
            st.progress(
                calc_pct(ficha["hp_atual"], ficha["hp_max"]),
                text=f"HP {ficha['hp_atual']}/{ficha['hp_max']}",
            )
        with col3:
            st.progress(
                calc_pct(ficha["mp_atual"], ficha["mp_max"]),
                text=f"MP {ficha['mp_atual']}/{ficha['mp_max']}",
            )
