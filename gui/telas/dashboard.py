import streamlit as st

from gui import client
from gui.components.status_bar import show_status_bar

def mostrar():
    usuario   = st.session_state.get("usuario", {})
    eh_mestre = usuario.get("role") == "mestre"

    c1, c2 = st.columns([5, 1])
    with c1:
        st.title("📊 Dashboard")
    with c2:
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()

    dados = client.dashboard()
    if "erro" in dados:
        st.error(dados["erro"])
        return

    # métricas
    cols = st.columns(5)
    cols[0].metric("📜 Fichas",      dados["total_fichas"])
    cols[1].metric("🎲 Rolagens",    dados["total_rolagens"])
    cols[2].metric("🌟 Críticos",    dados["criticos"])
    cols[3].metric("💀 Falhas",      dados["falhas_criticas"])
    cols[4].metric("📈 Média",       dados["media_rolagens"])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""<div class='hk-section-title'>Personagens</div>""", unsafe_allow_html=True)
        fichas = dados.get("fichas", [])

        # mestre vê todos, jogador só a própria
        if not eh_mestre:
            ficha_id_proprio = usuario.get("ficha_id")
            fichas = [f for f in fichas if f["id"] == ficha_id_proprio] if ficha_id_proprio else []

        if not fichas:
            st.info("Nenhuma ficha encontrada." if eh_mestre else "Você ainda não tem uma ficha criada.")
        else:
            for f in fichas:
                st.markdown(f"""
                <div class='hk-card'>
                    <div class='hk-card-title'>{f['nome']}</div>
                    <div class='hk-card-sub'>{f['raca']} · {f['classe']} · Nv {f['nivel']}</div>
                </div>
                """, unsafe_allow_html=True)

                status = f.get("status", {})
                vida_a = status.get("vida", {}).get("atual", f.get("hp_atual", 0))
                vida_m = status.get("vida", {}).get("maximo", f.get("hp_max", 1))
                show_status_bar("vida", vida_a, vida_m)

                if status.get("sanidade"):
                    show_status_bar("sanidade", status["sanidade"]["atual"], status["sanidade"]["maximo"])

                c_a, c_b = st.columns(2)
                with c_a:
                    if st.button("📖 Abrir", key=f"dash_abrir_{f['id']}", use_container_width=True):
                        st.session_state.ficha_id = f["id"]
                        st.session_state.tela = "ficha_detalhe"
                        st.rerun()
                with c_b:
                    if st.button("🎲 Jogar", key=f"dash_jogar_{f['id']}", use_container_width=True, type="primary"):
                        st.session_state.ficha_id = f["id"]
                        st.session_state.personagem_ativo = f
                        st.session_state.tela = "mesa"
                        st.rerun()

    with col2:
        st.markdown("""<div class='hk-section-title'>Últimas Rolagens</div>""", unsafe_allow_html=True)
        ultimas = dados.get("ultimas_rolagens", [])
        if not ultimas:
            st.info("Nenhuma rolagem ainda.")
        for r in reversed(ultimas):
            badge = "🌟" if r.get("critico") else "💀" if r.get("falha_critica") else "🎲"
            with st.container():
                st.markdown(f"""
                <div class='hk-card' style='margin-bottom:6px;'>
                    <div style='font-size:11px;color:#6a5a40;'>{badge} {r['personagem']} · {r['dado']}</div>
                    <div style='font-size:22px;font-weight:500;color:#c8b89a;font-family:Cinzel,serif;'>{r['total']}</div>
                    {'<div style="font-size:10px;color:#5a4a30;">'+r['motivo']+'</div>' if r.get('motivo') else ''}
                </div>
                """, unsafe_allow_html=True)
