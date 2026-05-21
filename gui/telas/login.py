import streamlit as st

from config import api


def mostrar() -> None:
    """Render the login screen and set session state on success."""
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.markdown("""
        <div style='text-align:center;padding:40px 0 28px;'>
            <div style='font-size:52px;margin-bottom:14px;'>⚔️</div>
            <div style='font-family:Cinzel,serif;font-size:28px;letter-spacing:.2em;color:#c8b89a;'>
                BERESHIT
            </div>
            <div style='font-size:10px;color:#3a3a5a;letter-spacing:.12em;margin-top:8px;'>
                SISTEMA DE CAMPANHA RPG
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_login"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", use_container_width=True, type="primary")

        if entrar:
            if not usuario or not senha:
                st.error("Preencha usuário e senha!")
            else:
                res = api.login(usuario, senha)
                if "erro" in res:
                    st.error(res["erro"])
                else:
                    st.session_state.logado = True
                    st.session_state.usuario = res["usuario"]
                    st.session_state.role = res["role"]
                    st.rerun()
