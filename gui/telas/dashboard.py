import streamlit as st
from config import api


def mostrar():
    usuario = st.session_state.usuario
    role = st.session_state.role
    dados = api.get_dashboard(usuario, role)

    if role == "mestre":
        _dashboard_mestre(dados)
    else:
        _dashboard_jogador(usuario, dados)


def _dashboard_mestre(dados):
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


def _dashboard_jogador(usuario: str, dados: dict):
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


def _card_ficha(ficha: dict):
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"**{ficha['nome']}**")
            st.caption(f"{ficha['raca']} · {ficha['classe']} · Nível {ficha['nivel']}")
        with col2:
            hp_pct = ficha["hp_atual"] / ficha["hp_max"] if ficha["hp_max"] > 0 else 0
            st.progress(min(hp_pct, 1.0), text=f"HP {ficha['hp_atual']}/{ficha['hp_max']}")
        with col3:
            mp_pct = ficha["mp_atual"] / ficha["mp_max"] if ficha["mp_max"] > 0 else 0
            st.progress(min(mp_pct, 1.0), text=f"MP {ficha['mp_atual']}/{ficha['mp_max']}")
