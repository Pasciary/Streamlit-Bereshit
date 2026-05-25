import streamlit as st

from gui import client


def mostrar():
    usuario = st.session_state.get("usuario", {})

    st.markdown("""
    <div style='text-align:center;padding:32px 0 24px;'>
        <div style='font-size:32px;'>⚔️</div>
        <div style='font-family:Cinzel,serif;font-size:22px;letter-spacing:.22em;
                    color:#c8b89a;font-weight:700;margin-top:8px;'>BERESHIT</div>
        <div style='font-size:11px;color:#5a4a30;letter-spacing:.1em;margin-top:4px;'>בְּרֵאשִׁית · Escolha sua campanha</div>
    </div>
    """, unsafe_allow_html=True)

    campanhas = client.listar_campanhas_usuario(usuario.get("id", ""))

    if not campanhas:
        st.warning("Você não faz parte de nenhuma campanha.")
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        return

    for c in campanhas:
        role = c["minha_role"]
        badge = "👑 Mestre de Jogo" if role == "mestre" else "🎲 Jogador"
        badge_cor = "#c8a050" if role == "mestre" else "#5a8a60"

        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class='hk-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <div class='hk-card-title'>{c['nome']}</div>
                        <div class='hk-card-sub'>{c['descricao']}</div>
                    </div>
                    <div style='font-size:11px;color:{badge_cor};font-family:Cinzel,serif;
                                white-space:nowrap;padding-left:16px;'>{badge}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Entrar →", key=f"camp_{c['id']}", use_container_width=True, type="primary"):
                st.session_state.campanha_ativa = {"id": c["id"], "nome": c["nome"]}
                st.session_state.usuario["role"] = role
                st.session_state.usuario["ficha_id"] = c.get("minha_ficha_id")
                st.session_state.tela = "dashboard"
                st.rerun()

    st.divider()
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()
