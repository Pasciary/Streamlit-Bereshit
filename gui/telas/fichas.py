import streamlit as st

from gui import client
from gui.components.status_bar import show_status_bar

RACAS    = ["Humano","Elfo","Anão","Halfling","Tiefling","Draconato","Gnomo","Meio-Elfo","Meio-Orc"]
CLASSES  = ["Bárbaro","Bardo","Bruxo","Clérigo","Druida","Feiticeiro","Guerreiro","Ladino","Mago","Monge","Paladino","Ranger"]
BACKGROUNDS  = ["Acólito","Artesão","Criminoso","Eremita","Entreter","Herói do Povo","Nobre","Sábio","Soldado"]
ALINHAMENTOS = [
    "Leal e Bom","Neutro e Bom","Caótico e Bom",
    "Leal e Neutro","Neutro Verdadeiro","Caótico e Neutro",
    "Leal e Mau","Neutro e Mau","Caótico e Mau",
]


def mostrar():
    usuario   = st.session_state.get("usuario", {})
    eh_mestre = usuario.get("role") == "mestre"

    if eh_mestre:
        tab1, tab2 = st.tabs(["📜 Todas as Fichas", "➕ Nova Ficha"])
        with tab1: _listar_fichas(eh_mestre, usuario)
        with tab2: _criar_ficha()
    else:
        tab1, tab2 = st.tabs(["📜 Minha Ficha", "➕ Nova Ficha"])
        with tab1: _listar_fichas(eh_mestre, usuario)
        with tab2: _criar_ficha()


def _listar_fichas(eh_mestre, usuario):
    c1, c2 = st.columns([5, 1])
    with c1:
        titulo = "📜 Todos os Personagens" if eh_mestre else "📜 Meu Personagem"
        st.subheader(titulo)
    with c2:
        if st.button("🔄", use_container_width=True):
            st.rerun()

    fichas = client.listar_fichas()
    if isinstance(fichas, dict) and "erro" in fichas:
        st.error(fichas["erro"])
        return

    if not eh_mestre:
        ficha_id_proprio = usuario.get("ficha_id")
        fichas = [f for f in fichas if f["id"] == ficha_id_proprio] if ficha_id_proprio else fichas[:1]

    if not fichas:
        msg = "Nenhuma ficha criada ainda." if eh_mestre else "Você ainda não tem ficha. Crie uma na aba 'Nova Ficha'!"
        st.info(msg)
        return

    for f in fichas:
        with st.container():
            st.markdown(f"""
            <div class='hk-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                        <div class='hk-card-title'>{f['nome']}</div>
                        <div class='hk-card-sub'>🧬 {f['raca']} &nbsp;·&nbsp; ⚔️ {f['classe']} &nbsp;·&nbsp; ⭐ Nível {f['nivel']}</div>
                    </div>
                    <div style='font-size:10px;color:#5a4a30;font-family:Cinzel,serif;'>XP {f['xp']} / {f['xp_proximo']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            status = f.get("status", {})
            vida_a = status.get("vida", {}).get("atual", f.get("hp_atual", 0))
            vida_m = status.get("vida", {}).get("maximo", f.get("hp_max", 1))
            show_status_bar("vida", vida_a, vida_m)

            if f.get("condicoes"):
                conds = " ".join([f"<span class='hk-badge hk-badge-warn'>{c}</span>" for c in f["condicoes"]])
                st.markdown(f"<div style='margin:4px 0;'>{conds}</div>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("📖 Abrir Ficha", key=f"abrir_{f['id']}", use_container_width=True):
                    st.session_state.ficha_id = f["id"]
                    st.session_state.tela = "ficha_detalhe"
                    st.rerun()
            with c2:
                if st.button("🎲 Jogar", key=f"jogar_{f['id']}", use_container_width=True, type="primary"):
                    st.session_state.ficha_id = f["id"]
                    st.session_state.personagem_ativo = f
                    st.session_state.tela = "mesa"
                    st.rerun()
            with c3:
                if eh_mestre:
                    if st.button("🗑️ Excluir", key=f"del_{f['id']}", use_container_width=True):
                        client.deletar_ficha(f["id"])
                        st.rerun()

            st.markdown("<hr style='border-color:#1a1a2a;margin:8px 0;'>", unsafe_allow_html=True)


def _criar_ficha():
    st.subheader("➕ Criar Personagem")

    with st.form("form_criar_ficha"):
        c1, c2 = st.columns(2)
        with c1:
            nome        = st.text_input("Nome do personagem *")
            raca        = st.selectbox("Raça", RACAS)
            classe      = st.selectbox("Classe", CLASSES)
        with c2:
            background  = st.selectbox("Background", BACKGROUNDS)
            alinhamento = st.selectbox("Alinhamento", ALINHAMENTOS)

        st.divider()
        st.subheader("🎯 Atributos")
        st.caption("Valores entre 8 e 15")

        c1, c2, c3 = st.columns(3)
        with c1:
            forca        = st.slider("💪 Força",        8, 15, 10)
            destreza     = st.slider("🏃 Destreza",     8, 15, 10)
        with c2:
            constituicao = st.slider("❤️ Constituição", 8, 15, 12)
            inteligencia = st.slider("🧠 Inteligência", 8, 15, 10)
        with c3:
            sabedoria    = st.slider("🦉 Sabedoria",    8, 15, 10)
            carisma      = st.slider("✨ Carisma",      8, 15, 10)

        st.divider()
        historia = st.text_area("📖 História", placeholder="Conte a história do personagem...")
        criar = st.form_submit_button("✨ Criar Personagem", type="primary", use_container_width=True)

    if criar:
        if not nome.strip():
            st.error("O nome é obrigatório!")
            return
        res = client.criar_ficha({
            "nome": nome, "raca": raca, "classe": classe,
            "background": background, "alinhamento": alinhamento,
            "historia": historia,
            "atributos": {
                "forca": forca, "destreza": destreza,
                "constituicao": constituicao, "inteligencia": inteligencia,
                "sabedoria": sabedoria, "carisma": carisma,
            },
        })
        if "erro" in res:
            st.error(res["erro"])
        else:
            st.success(f"✨ {res['nome']} criado!")
            st.balloons()
            st.session_state.ficha_id = res["id"]
            st.session_state.tela = "ficha_detalhe"
            st.rerun()
