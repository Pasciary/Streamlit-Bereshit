import streamlit as st

def mostrar():
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.title("BERESHIT")
        
    with st.form("form_login"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")

    if entrar:
        if not usuario or not senha:
            st.error("Preencha usuário e senha!")
        elif usuario == "mestre" and senha == "1234":
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos!")