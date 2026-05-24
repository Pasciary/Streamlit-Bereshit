import streamlit as st

from gui import client


def mostrar():
    st.markdown("""
    <div style='text-align:center;padding:3rem 0 1.5rem;'>
        <div style='font-size:3.5rem;'>⚔️</div>
        <div style='font-family:Cinzel,serif;font-size:22px;letter-spacing:.22em;color:#c8b89a;margin:8px 0 4px;'>BERESHIT</div>
        <div style='font-size:12px;color:#5a4a30;letter-spacing:.1em;'>בְּרֵאשִׁית · Entre com suas credenciais</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("form_login"):
            usuario = st.text_input("Usuário", placeholder="mestre ou jogador1")
            senha   = st.text_input("Senha", type="password", placeholder="1234")
            entrar  = st.form_submit_button("Entrar", use_container_width=True, type="primary")

        if entrar:
            res = client.login(usuario, senha)
            if "erro" in res or not res.get("ok"):
                st.error(res.get("erro") or "Usuário ou senha inválidos")
            else:
                st.session_state.usuario  = res["usuario"]
                st.session_state.logado   = True
                st.session_state.tela     = "dashboard"
                st.rerun()

        st.markdown("""
        <div style='text-align:center;margin-top:12px;font-size:11px;color:#3a3a5a;'>
            💡 mestre / 1234 &nbsp;·&nbsp; jogador1 / 1234
        </div>
        """, unsafe_allow_html=True)
