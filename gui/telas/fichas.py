import streamlit as st

from config import api
from gui.components.status_bar import show_status_bar, show_vida_sanidade

CLASSES = [
    "Guerreiro", "Mago", "Ladino", "Clerigo", "Bardo",
    "Druida", "Paladino", "Ranger", "Monge", "Feiticeiro",
]
RACAS = [
    "Humano", "Elfo", "Anao", "Halfling", "Gnomo",
    "Meio-Elfo", "Meio-Orc", "Tiefling", "Draconato",
]
ATRIBUTOS = ["forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma"]
LABELS: dict[str, str] = {
    "forca": "Força",
    "destreza": "Destreza",
    "constituicao": "Constituição",
    "inteligencia": "Inteligência",
    "sabedoria": "Sabedoria",
    "carisma": "Carisma",
}


def mostrar() -> None:
    """Route to the correct ficha sub-screen based on session state."""
    if "ficha_modo" not in st.session_state:
        st.session_state.ficha_modo = "lista"
    if "ficha_selecionada" not in st.session_state:
        st.session_state.ficha_selecionada = None

    modo = st.session_state.ficha_modo
    if modo == "lista":
        _tela_lista()
    elif modo == "ver":
        _tela_ver()
    elif modo == "criar":
        _tela_criar()
    elif modo == "editar":
        _tela_editar()


def _ir_para(modo: str, ficha_id: int | None = None) -> None:
    """Update session state to navigate to another ficha sub-screen."""
    st.session_state.ficha_modo = modo
    st.session_state.ficha_selecionada = ficha_id


def _validar_recursos(hp_atual: int, hp_max: int, mp_atual: int, mp_max: int) -> list[str]:
    """Return a list of validation error messages for HP/MP values."""
    erros: list[str] = []
    if hp_atual > hp_max:
        erros.append("HP atual não pode ser maior que HP máximo.")
    if mp_atual > mp_max:
        erros.append("MP atual não pode ser maior que MP máximo.")
    return erros


def _render_atributos(ficha: dict) -> None:
    """Render the 6 D&D attributes using a 3×2 HTML grid."""
    partes = []
    for attr in ATRIBUTOS:
        val = ficha["atributos"][attr]
        mod = (val - 10) // 2
        sinal = "+" if mod >= 0 else ""
        partes.append(
            f"<div class='hk-attr-card'>"
            f"<div class='hk-attr-label'>{LABELS[attr].upper()}</div>"
            f"<div class='hk-attr-val'>{val}</div>"
            f"<div class='hk-attr-mod'>{sinal}{mod}</div>"
            f"</div>"
        )
    st.markdown(
        f"<div class='hk-attr-grid'>{''.join(partes)}</div>",
        unsafe_allow_html=True,
    )


# ── Lista ────────────────────────────────────────────────────────────────────

def _tela_lista() -> None:
    """Render the ficha list with optional player filter for mestre."""
    usuario = st.session_state.usuario
    role = st.session_state.role

    col1, col2 = st.columns([5, 1])
    with col1:
        st.title("Fichas de Personagem")
    with col2:
        if role == "jogador":
            if st.button("+ Nova Ficha", use_container_width=True, type="primary"):
                _ir_para("criar")
                st.rerun()

    fichas = api.get_fichas(usuario, role)

    if not fichas:
        msg = "Nenhuma ficha cadastrada ainda."
        if role == "jogador":
            msg += " Crie sua primeira ficha!"
        st.info(msg)
        return

    if role == "mestre":
        jogadores = sorted({f["jogador"] for f in fichas})
        filtro = st.selectbox(
            "Filtrar por jogador", ["Todos"] + jogadores, label_visibility="collapsed"
        )
        if filtro != "Todos":
            fichas = [f for f in fichas if f["jogador"] == filtro]

    for ficha in fichas:
        _linha_ficha(ficha, role)


def _linha_ficha(ficha: dict, role: str) -> None:
    """Render a ficha card with ornamental status bars and a detail link."""
    with st.container(border=True):
        info = f"{ficha['raca']} · {ficha['classe']} · Nível {ficha['nivel']}"
        if role == "mestre":
            info += f" · 👤 {ficha['jogador']}"
        st.markdown(f"""
        <div class='hk-card-title'>{ficha['nome']}</div>
        <div class='hk-card-sub'>{info}</div>
        """, unsafe_allow_html=True)

        show_vida_sanidade(ficha["hp_atual"], ficha["hp_max"], ficha["mp_atual"], ficha["mp_max"])

        if st.button("📖 Ver Ficha", key=f"ver_{ficha['id']}", use_container_width=True):
            _ir_para("ver", ficha["id"])
            st.rerun()


# ── Ver ──────────────────────────────────────────────────────────────────────

def _tela_ver() -> None:
    """Render the full detail view for a single ficha."""
    ficha_id = st.session_state.ficha_selecionada
    ficha = api.get_ficha(ficha_id)
    role = st.session_state.role
    usuario = st.session_state.usuario

    if not ficha:
        st.error("Ficha não encontrada.")
        _ir_para("lista")
        st.rerun()
        return

    col_back, col_titulo = st.columns([1, 7])
    with col_back:
        if st.button("← Voltar"):
            _ir_para("lista")
            st.rerun()
    with col_titulo:
        st.markdown(f"""
        <div style='font-family:Cinzel,serif;'>
            <div style='font-size:22px;font-weight:700;letter-spacing:.15em;color:#c8b89a;'>{ficha['nome'].upper()}</div>
            <div style='font-size:11px;color:#5a4a30;letter-spacing:.08em;'>
                {ficha['raca']} · {ficha['classe']} · Nível {ficha['nivel']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    aba_status, aba_info = st.tabs(["⚔️ Status", "📝 Info"])

    with aba_status:
        col1, col2 = st.columns(2)
        with col1:
            show_status_bar("vida", ficha["hp_atual"], ficha["hp_max"])
            show_status_bar("sanidade", ficha["mp_atual"], ficha["mp_max"])

            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Classe", ficha["classe"])
            c2.metric("Raça", ficha["raca"])
            c3.metric("Nível", ficha["nivel"])

        with col2:
            st.markdown("<div class='hk-section-title'>Atributos</div>", unsafe_allow_html=True)
            _render_atributos(ficha)

    with aba_info:
        st.markdown(f"""
        <div class='hk-card'>
            <table style='width:100%;font-size:12px;border-collapse:collapse;'>
                <tr><td style='color:#5a4a30;padding:5px 0;width:35%'>Nome</td><td style='color:#c8b89a;'>{ficha['nome']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Raça</td><td style='color:#c8b89a;'>{ficha['raca']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Classe</td><td style='color:#c8b89a;'>{ficha['classe']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Nível</td><td style='color:#c8b89a;'>{ficha['nivel']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Jogador</td><td style='color:#c8b89a;'>{ficha['jogador']}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        if ficha.get("historia"):
            st.divider()
            st.markdown("<div class='hk-section-title'>História</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='hk-card'>
                <div style='font-size:13px;color:#8a7a6a;line-height:1.8;'>{ficha['historia']}</div>
            </div>
            """, unsafe_allow_html=True)

    pode_editar = role == "mestre" or ficha["jogador"] == usuario
    if pode_editar:
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Editar Ficha", use_container_width=True, type="primary"):
                _ir_para("editar", ficha_id)
                st.rerun()
        with col2:
            if role == "mestre":
                if st.button("Excluir Ficha", use_container_width=True):
                    res = api.deletar_ficha(ficha_id)
                    if "ok" in res:
                        st.success("Ficha excluída.")
                        _ir_para("lista")
                        st.rerun()
                    else:
                        st.error(res.get("erro"))


# ── Criar ────────────────────────────────────────────────────────────────────

def _tela_criar() -> None:
    """Render the new ficha creation form."""
    col_back, col_titulo = st.columns([1, 7])
    with col_back:
        if st.button("← Voltar"):
            _ir_para("lista")
            st.rerun()
    with col_titulo:
        st.title("Nova Ficha")

    usuario = st.session_state.usuario

    with st.form("form_criar_ficha"):
        nome = st.text_input("Nome do Personagem")

        col1, col2, col3 = st.columns(3)
        with col1:
            classe = st.selectbox("Classe", CLASSES)
        with col2:
            raca = st.selectbox("Raça", RACAS)
        with col3:
            nivel = st.number_input("Nível", min_value=1, max_value=20, value=1)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            hp_max = st.number_input("HP Máximo", min_value=1, value=10)
        with col2:
            hp_atual = st.number_input("HP Atual", min_value=0, value=10)
        with col3:
            mp_max = st.number_input("MP Máximo", min_value=0, value=10)
        with col4:
            mp_atual = st.number_input("MP Atual", min_value=0, value=10)

        st.markdown("<div class='hk-section-title'>Atributos</div>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        atributos: dict[str, int] = {}
        for i, attr in enumerate(ATRIBUTOS):
            with [col_a, col_b, col_c][i % 3]:
                atributos[attr] = st.number_input(
                    LABELS[attr], min_value=1, max_value=20, value=10, key=f"c_{attr}"
                )

        historia = st.text_area("História do Personagem", height=150)
        submit = st.form_submit_button("Criar Ficha", use_container_width=True, type="primary")

    if submit:
        if not nome:
            st.error("Informe o nome do personagem!")
            return
        erros = _validar_recursos(int(hp_atual), int(hp_max), int(mp_atual), int(mp_max))
        for e in erros:
            st.error(e)
        if erros:
            return
        res = api.criar_ficha({
            "nome": nome,
            "jogador": usuario,
            "classe": classe,
            "raca": raca,
            "nivel": nivel,
            "hp_atual": hp_atual,
            "hp_max": hp_max,
            "mp_atual": mp_atual,
            "mp_max": mp_max,
            "atributos": atributos,
            "historia": historia,
        })
        if "ok" in res:
            st.success("Ficha criada com sucesso!")
            _ir_para("ver", res["ficha"]["id"])
            st.rerun()
        else:
            st.error(res.get("erro", "Erro ao criar ficha."))


# ── Editar ───────────────────────────────────────────────────────────────────

def _tela_editar() -> None:
    """Render the ficha edit form pre-populated with current values."""
    ficha_id = st.session_state.ficha_selecionada
    ficha = api.get_ficha(ficha_id)

    if not ficha:
        st.error("Ficha não encontrada.")
        _ir_para("lista")
        st.rerun()
        return

    col_back, col_titulo = st.columns([1, 7])
    with col_back:
        if st.button("← Voltar"):
            _ir_para("ver", ficha_id)
            st.rerun()
    with col_titulo:
        st.title(f"Editando: {ficha['nome']}")

    with st.form("form_editar_ficha"):
        nome = st.text_input("Nome do Personagem", value=ficha["nome"])

        col1, col2, col3 = st.columns(3)
        with col1:
            idx_classe = CLASSES.index(ficha["classe"]) if ficha["classe"] in CLASSES else 0
            classe = st.selectbox("Classe", CLASSES, index=idx_classe)
        with col2:
            idx_raca = RACAS.index(ficha["raca"]) if ficha["raca"] in RACAS else 0
            raca = st.selectbox("Raça", RACAS, index=idx_raca)
        with col3:
            nivel = st.number_input("Nível", min_value=1, max_value=20, value=ficha["nivel"])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            hp_max = st.number_input("HP Máximo", min_value=1, value=ficha["hp_max"])
        with col2:
            hp_atual = st.number_input("HP Atual", min_value=0, value=ficha["hp_atual"])
        with col3:
            mp_max = st.number_input("MP Máximo", min_value=0, value=ficha["mp_max"])
        with col4:
            mp_atual = st.number_input("MP Atual", min_value=0, value=ficha["mp_atual"])

        st.markdown("<div class='hk-section-title'>Atributos</div>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        atributos: dict[str, int] = {}
        for i, attr in enumerate(ATRIBUTOS):
            with [col_a, col_b, col_c][i % 3]:
                atributos[attr] = st.number_input(
                    LABELS[attr], min_value=1, max_value=20,
                    value=ficha["atributos"][attr], key=f"e_{attr}",
                )

        historia = st.text_area("História do Personagem", value=ficha["historia"], height=150)
        submit = st.form_submit_button("Salvar Alterações", use_container_width=True, type="primary")

    if submit:
        if not nome:
            st.error("Informe o nome do personagem!")
            return
        erros = _validar_recursos(int(hp_atual), int(hp_max), int(mp_atual), int(mp_max))
        for e in erros:
            st.error(e)
        if erros:
            return
        res = api.atualizar_ficha(ficha_id, {
            "nome": nome,
            "classe": classe,
            "raca": raca,
            "nivel": nivel,
            "hp_atual": hp_atual,
            "hp_max": hp_max,
            "mp_atual": mp_atual,
            "mp_max": mp_max,
            "atributos": atributos,
            "historia": historia,
        })
        if "ok" in res:
            st.success("Ficha atualizada!")
            _ir_para("ver", ficha_id)
            st.rerun()
        else:
            st.error(res.get("erro", "Erro ao atualizar ficha."))
