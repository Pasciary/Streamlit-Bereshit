import streamlit as st

from gui import client
from gui.components.status_bar import show_bloco_status, show_status_bar


@st.dialog("🎲 Rolar Dados", width="large")
def _modal_rolar_dados(usuario):
    DADOS_OPTS = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]
    for k, v in [("rolagem_dado", "d20"), ("rolagem_qtd", 1), ("rolagem_mod", 0), ("rolagem_motivo", "")]:
        if k not in st.session_state:
            st.session_state[k] = v
    if "dados_presets" not in st.session_state:
        st.session_state["dados_presets"] = []
    if "preset_sel" not in st.session_state:
        st.session_state["preset_sel"] = "— sem preset —"

    personagem_ativo = st.session_state.get("personagem_ativo")
    presets = st.session_state["dados_presets"]

    # ── selectbox de presets ──────────────────────────────────────────────────
    if presets:
        def _aplicar_preset():
            sel = st.session_state.get("preset_sel", "")
            p = next((x for x in st.session_state["dados_presets"] if x["nome"] == sel), None)
            if p:
                st.session_state["rolagem_dado"]   = p["dado"]
                st.session_state["rolagem_qtd"]    = p["qtd"]
                st.session_state["rolagem_mod"]    = p["mod"]
                st.session_state["rolagem_motivo"] = p["motivo"]

        opcoes = ["— sem preset —"] + [p["nome"] for p in presets]
        if st.session_state["preset_sel"] not in opcoes:
            st.session_state["preset_sel"] = "— sem preset —"

        preset_selecionado = st.session_state["preset_sel"]
        idx_preset = next((i for i, p in enumerate(presets) if p["nome"] == preset_selecionado), None)

        sp1, sp2, sp3 = st.columns([5, 1, 1])
        with sp1:
            st.selectbox("Preset salvo", opcoes, key="preset_sel",
                         on_change=_aplicar_preset, label_visibility="collapsed")
        with sp2:
            if st.button("✏️", help="Sobrescrever preset com os valores do formulário",
                         disabled=idx_preset is None, use_container_width=True):
                presets[idx_preset] = {
                    "nome":   presets[idx_preset]["nome"],
                    "dado":   st.session_state["rolagem_dado"],
                    "qtd":    int(st.session_state["rolagem_qtd"]),
                    "mod":    int(st.session_state["rolagem_mod"]),
                    "motivo": st.session_state["rolagem_motivo"],
                }
        with sp3:
            if st.button("🗑️", help="Excluir preset selecionado",
                         disabled=idx_preset is None, use_container_width=True):
                presets.pop(idx_preset)
                st.session_state["preset_sel"] = "— sem preset —"
        st.divider()

    # ── formulário ────────────────────────────────────────────────────────────
    st.selectbox("Dado", DADOS_OPTS, key="rolagem_dado")
    cq, cm = st.columns(2)
    with cq:
        st.number_input("Qtd", min_value=1, max_value=20, key="rolagem_qtd")
    with cm:
        st.number_input("Mod", min_value=-10, max_value=20, key="rolagem_mod")
    st.text_input("Motivo", placeholder="Ex: Ataque", key="rolagem_motivo")

    # ── ações ─────────────────────────────────────────────────────────────────
    resultado_atual = None
    cr, cs = st.columns([3, 2])
    with cr:
        if st.button("🎲 Rolar!", type="primary", use_container_width=True):
            dado_val   = st.session_state["rolagem_dado"]
            qtd_val    = int(st.session_state["rolagem_qtd"])
            mod_val    = int(st.session_state["rolagem_mod"])
            motivo_val = st.session_state["rolagem_motivo"]
            nome = personagem_ativo["nome"] if personagem_ativo else usuario.get("nome", "Anônimo")
            entrada = client.rolar_dados(dado=dado_val, quantidade=qtd_val, modificador=mod_val,
                ficha_id=personagem_ativo["id"] if personagem_ativo else None,
                personagem=nome, motivo=motivo_val)
            resultado_atual = {
                "total":     entrada["total"],
                "resultados": entrada["resultados"],
                "mod":       mod_val,
                "critico":   entrada["critico"],
                "falha":     entrada["falha_critica"],
            }
            st.session_state["_ultimo_resultado"] = resultado_atual
    with cs:
        if st.button("⭐ Salvar novo preset", use_container_width=True):
            st.session_state["_show_save_preset"] = True

    # ── resultado da rolagem ──────────────────────────────────────────────────
    show = resultado_atual or st.session_state.get("_ultimo_resultado")
    if show:
        if show["critico"]:
            st.success(f"🌟 CRÍTICO! **{show['total']}** — {show['resultados']} +{show['mod']}")
        elif show["falha"]:
            st.error(f"💀 FALHA CRÍTICA! **{show['total']}** — {show['resultados']}")
        else:
            st.info(f"🎲 **{show['total']}** — {show['resultados']} +{show['mod']}")

    # ── formulário de salvar preset (abre inline, sem fechar o popup) ─────────
    if st.session_state.get("_show_save_preset"):
        st.divider()
        nome_p = st.text_input("Nome do preset", key="novo_preset_nome",
                               placeholder="Ex: Ataque c/ espada")
        cc1, cc2 = st.columns([3, 1])
        with cc1:
            if st.button("✔ Confirmar e fechar", type="primary",
                         key="confirm_salvar_preset", use_container_width=True):
                if nome_p:
                    st.session_state["dados_presets"].append({
                        "nome":   nome_p,
                        "dado":   st.session_state["rolagem_dado"],
                        "qtd":    int(st.session_state["rolagem_qtd"]),
                        "mod":    int(st.session_state["rolagem_mod"]),
                        "motivo": st.session_state["rolagem_motivo"],
                    })
                    del st.session_state["_show_save_preset"]
                    st.rerun()
        with cc2:
            if st.button("✕", key="cancel_preset", use_container_width=True,
                         help="Cancelar"):
                del st.session_state["_show_save_preset"]


@st.dialog("📋 Criar Ficha Rápida", width="large")
def _modal_criar_ficha(nome_inimigo):
    for k, v in [("cf_hp_max", 10), ("cf_hp_atual", 10), ("cf_ca", 10)]:
        if k not in st.session_state:
            st.session_state[k] = v

    st.markdown(
        "<div style='font-family:Cinzel,serif;font-size:13px;color:#c8b89a;"
        "letter-spacing:.12em;margin-bottom:8px;'>"
        + nome_inimigo.upper()
        + "</div>",
        unsafe_allow_html=True,
    )

    ch, cc = st.columns(2)
    with ch:
        st.number_input("HP Máximo", min_value=1, max_value=9999, key="cf_hp_max")
    with cc:
        st.number_input("CA", min_value=1, max_value=30, key="cf_ca")

    st.number_input("HP Atual", min_value=0, max_value=st.session_state["cf_hp_max"], key="cf_hp_atual")

    cb1, cb2 = st.columns([3, 1])
    with cb1:
        if st.button("✔ Criar e fechar", type="primary", use_container_width=True):
            client.criar_ficha_rapida(
                nome=nome_inimigo,
                hp_max=int(st.session_state["cf_hp_max"]),
                hp_atual=int(st.session_state["cf_hp_atual"]),
                ca=int(st.session_state["cf_ca"]),
            )
            for k in ("cf_hp_max", "cf_hp_atual", "cf_ca"):
                st.session_state.pop(k, None)
            st.rerun()
    with cb2:
        if st.button("✕", use_container_width=True, help="Cancelar"):
            for k in ("cf_hp_max", "cf_hp_atual", "cf_ca"):
                st.session_state.pop(k, None)
            st.rerun()


def mostrar():
    usuario   = st.session_state.get("usuario", {})
    eh_mestre = usuario.get("role") == "mestre"

    c1, c2 = st.columns([5, 1])
    with c1:
        st.title("🎲 Mesa de Jogo")
    with c2:
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()

    combate     = client.estado_combate()
    ativo       = client.personagem_ativo_turno()
    campanha_id = st.session_state.get("campanha_ativa", {}).get("id")
    fichas      = client.listar_fichas(campanha_id=campanha_id)

    col_esq, col_dir = st.columns([2, 2])

    with col_esq:
        _render_personagem_ativo(ativo, fichas)
        st.divider()
        if combate.get("ativa"):
            _render_combate_ativo(combate, ativo, fichas, eh_mestre)
        else:
            if eh_mestre:
                _render_iniciar_combate(fichas)
            else:
                st.info("Aguardando o mestre iniciar o combate...")

    with col_dir:
        _render_rolagem(usuario, fichas)
        st.divider()
        _render_log()

    if combate.get("ativa"):
        st.divider()
        _render_panorama(combate, fichas)


def _render_personagem_ativo(ativo, fichas):
    st.markdown("<div class='hk-section-title'>Personagem no Turno Atual</div>", unsafe_allow_html=True)
    part = ativo.get("ativo") if ativo else None

    if not part:
        st.markdown("""
        <div class='hk-card' style='text-align:center;'>
            <div style='font-family:Cinzel,serif;font-size:12px;color:#5a4a30;letter-spacing:.15em;'>
                — NENHUM COMBATE ATIVO —
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    rodada = ativo.get("rodada", 1)
    icone  = "👑" if part.get("tipo") == "jogador" else "👹"

    st.markdown(f"""
    <div style='font-size:9px;letter-spacing:.16em;color:#5a4a30;font-family:Cinzel,serif;margin-bottom:4px;'>
        RODADA {rodada} &nbsp;·&nbsp; init {part.get('iniciativa','?')} &nbsp;{icone}
    </div>
    """, unsafe_allow_html=True)

    ficha_ativa = next((f for f in fichas if f["nome"] == part.get("nome")), None)

    if ficha_ativa:
        status = ficha_ativa.get("status", {})
        if "vida" not in status:
            status["vida"] = {"atual": ficha_ativa.get("hp_atual", 0), "maximo": ficha_ativa.get("hp_max", 1)}
        ficha_ativa["status"] = status
        show_bloco_status(ficha_ativa, colunas=1)
    else:
        nome_part = part.get("nome", "?")
        st.markdown(
            "<div class='hk-card' style='border-color:#5a4a30;'>"
            "<div style='font-family:Cinzel,serif;font-size:16px;font-weight:700;"
            "letter-spacing:.2em;color:#c8b89a;'>"
            + nome_part.upper()
            + "</div>"
            "<div style='font-size:10px;color:#6a5a40;'>Sem ficha registrada</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("📋 Criar Ficha", key=f"criar_ficha_{nome_part}", use_container_width=True):
            _modal_criar_ficha(nome_part)


def _render_combate_ativo(combate, ativo, fichas, eh_mestre):
    st.markdown("<div class='hk-section-title'>Ordem de Iniciativa</div>", unsafe_allow_html=True)
    turno_atual = combate.get("turno_atual", 0)
    for i, part in enumerate(combate.get("iniciativa", [])):
        eh_turno = i == turno_atual
        cor_bg  = "#0d1a0d" if eh_turno else "#0a0a14"
        cor_brd = "#2a4a2a" if eh_turno else "#1a1a2a"
        cor_txt = "#80d080" if eh_turno else "#6a7aaa"
        icone   = "●" if eh_turno else "○"
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;padding:7px 12px;
             background:{cor_bg};border:0.5px solid {cor_brd};border-radius:6px;margin-bottom:4px;'>
            <div style='color:{cor_txt};font-size:10px;'>{icone}</div>
            <div style='flex:1;font-size:13px;color:{cor_txt};font-weight:{"600" if eh_turno else "400"};'>{part['nome']}</div>
            <div style='font-size:11px;color:#3a4a6a;'>init {part['iniciativa']}</div>
        </div>
        """, unsafe_allow_html=True)

    if eh_mestre:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⏭️ Próximo Turno", use_container_width=True, type="primary"):
                client.proximo_turno()
                st.rerun()
        with c2:
            if st.button("🏁 Encerrar Combate", use_container_width=True):
                client.encerrar_combate()
                st.rerun()


def _render_iniciar_combate(fichas):
    st.markdown("<div class='hk-section-title'>Iniciar Combate</div>", unsafe_allow_html=True)
    with st.expander("⚔️ Configurar participantes"):
        participantes = []
        st.write("**Personagens:**")
        for f in fichas:
            c1, c2 = st.columns([3, 1])
            c1.write(f["nome"])
            init = c2.number_input("Init", -5, 30, f["iniciativa"], key=f"init_{f['id']}")
            participantes.append({"nome": f["nome"], "iniciativa": init, "tipo": "jogador", "ficha_id": f["id"]})

        st.write("**Monstros / NPCs:**")
        n_monstros = st.number_input("Quantidade de monstros", 0, 10, 0)
        catalogo   = client.catalogo_monstros()
        for i in range(int(n_monstros)):
            c1, c2, c3 = st.columns([3, 2, 1])
            tipo  = c1.selectbox("Tipo", [m["nome"] for m in catalogo], key=f"m_tipo_{i}")
            nome  = c2.text_input("Nome", value=f"{tipo} {i+1}", key=f"m_nome_{i}")
            init  = c3.number_input("Init", -5, 30, 10, key=f"m_init_{i}")
            participantes.append({"nome": nome, "iniciativa": init, "tipo": "monstro"})

        if st.button("⚔️ Iniciar Combate!", type="primary", use_container_width=True):
            if participantes:
                client.iniciar_combate(participantes)
                st.rerun()


def _render_rolagem(usuario, fichas):
    if st.button("🎲 Rolar Dados", use_container_width=True, type="primary"):
        st.session_state.pop("_show_save_preset", None)
        _modal_rolar_dados(usuario)


def _render_log():
    st.markdown("<div class='hk-section-title'>Últimas Rolagens</div>", unsafe_allow_html=True)
    logs = client.log_dados()
    if not logs:
        st.info("Nenhuma rolagem ainda.")
        return

    personagens = sorted(set(r["personagem"] for r in logs))
    f_col1, f_col2 = st.columns([3, 2])
    with f_col1:
        filtro = st.selectbox(
            "filtro",
            ["Todos", "Última Rolagem"] + personagens,
            key="mesa_filtro_pers",
            label_visibility="collapsed",
        )

    if filtro == "Última Rolagem":
        rolagens = logs[:1]
    else:
        with f_col2:
            ordem = st.selectbox(
                "ordem",
                ["Mais recente", "Mais antigo"],
                key="mesa_filtro_ordem",
                label_visibility="collapsed",
            )
        rolagens = logs if filtro == "Todos" else [r for r in logs if r["personagem"] == filtro]
        if ordem == "Mais antigo":
            rolagens = list(reversed(rolagens))

    if not rolagens:
        st.info("Nenhuma rolagem encontrada.")
    else:
        for r in rolagens:
            badge       = "🌟" if r.get("critico") else "💀" if r.get("falha_critica") else "🎲"
            resultados  = r.get("resultados", [r.get("total")])
            res_str     = " / ".join(str(x) for x in resultados)
            mod         = r.get("modificador", 0)
            total       = r.get("total", "?")
            if mod != 0:
                mod_txt = f"+{mod}" if mod > 0 else str(mod)
                detalhe = f"= {total} ({mod_txt})"
            elif len(resultados) > 1:
                detalhe = f"= {total}"
            else:
                detalhe = ""
            st.markdown(
                "<div class='hk-card' style='margin-bottom:6px;'>"
                "<div style='font-size:11px;color:#6a5a40;'>" + badge + " " + r["personagem"] + " · " + r["dado"] + "</div>"
                "<div style='font-size:22px;font-weight:500;color:#c8b89a;font-family:Cinzel,serif;'>" + res_str + "</div>"
                + ("<div style='font-size:10px;color:#7a6a50;'>" + detalhe + "</div>" if detalhe else "")
                + ("<div style='font-size:10px;color:#5a4a30;'>" + r["motivo"] + "</div>" if r.get("motivo") else "")
                + "</div>",
                unsafe_allow_html=True,
            )

    if st.button("🗑️ Limpar log", use_container_width=True):
        client.limpar_log()
        st.rerun()


def _render_panorama(combate, fichas):
    st.markdown("<div class='hk-section-title'>Status do Combate</div>", unsafe_allow_html=True)
    participantes = combate.get("iniciativa", [])
    if not participantes:
        return
    turno_atual = combate.get("turno_atual", 0)

    STATUS_CORES = {
        "vida":     ("#e05050", "#a02020"),
        "sangue":   ("#c02030", "#700010"),
        "sanidade": ("#4080d0", "#1040a0"),
        "vigor":    ("#d08020", "#805010"),
        "mana":     ("#c0a0e0", "#6030b0"),
        "ki":       ("#c07820", "#804800"),
        "arcana":   ("#c0a0e0", "#6030b0"),
    }
    ORDEM = ["vida", "sangue", "sanidade", "vigor", "mana", "ki", "arcana"]

    def _barra_html(tipo, status):
        dados = status.get(tipo)
        if not dados:
            return ""
        atual  = dados.get("atual", 0)
        maximo = max(dados.get("maximo", 1), 1)
        pct    = max(0, min(100, atual / maximo * 100))
        cs, ce = STATUS_CORES.get(tipo, ("#888", "#444"))
        label  = tipo[:2].upper()
        numero = f"{atual}/{maximo}"
        return (
            "<div style=\"display:flex;align-items:center;gap:5px;margin-bottom:3px;\">"
            "<span style=\"font-size:9px;color:#7a6a50;width:16px;text-align:right;"
            "flex-shrink:0;font-family:Cinzel,serif;letter-spacing:.04em;\">"
            + label
            + "</span>"
            "<div style=\"flex:1;height:16px;background:#0d0b08;border:1px solid #2a2418;"
            "border-radius:3px;overflow:hidden;position:relative;\">"
            "<div style=\"position:absolute;top:0;left:0;height:100%;width:" + f"{pct:.0f}" + "%;"
            "background:linear-gradient(to right," + cs + "," + ce + ");"
            "opacity:0.85;\"></div>"
            "<div style=\"position:absolute;inset:0;display:flex;align-items:center;"
            "justify-content:center;font-size:9px;font-weight:600;color:#e8dcc8;"
            "font-family:Cinzel,serif;letter-spacing:.05em;"
            "text-shadow:0 0 4px #000,1px 1px 0 #000,-1px -1px 0 #000;\">"
            + numero
            + "</div>"
            "</div>"
            "</div>"
        )

    linhas = []
    for i, part in enumerate(participantes):
        eh_turno = i == turno_atual
        icone    = "👑" if part.get("tipo") == "jogador" else "👹"
        ficha    = next((f for f in fichas if f["nome"] == part.get("nome")), None)
        status   = ficha.get("status", {}) if ficha else {}

        if ficha and "vida" not in status:
            status["vida"] = {"atual": ficha.get("hp_atual", 0), "maximo": ficha.get("hp_max", 1)}

        barras = "".join(_barra_html(t, status) for t in ORDEM if status.get(t))
        sem_ficha = "<span style=\"font-size:10px;color:#3a3a5a;\">sem ficha</span>"

        conds = ""
        if ficha and ficha.get("condicoes"):
            conds = "<div style=\"margin-top:3px;\">" + "".join(
                "<span style=\"font-size:8px;background:#2a1a08;border:1px solid #5a3a10;"
                "border-radius:3px;padding:1px 4px;color:#c8a060;margin-right:2px;\">"
                + c + "</span>"
                for c in ficha["condicoes"]
            ) + "</div>"

        bg_row  = "#0d1a0d" if eh_turno else "transparent"
        brd_row = "#2a4a2a" if eh_turno else "#1a1a2a"
        cor_nom = "#80d080" if eh_turno else "#c8b89a"
        badge   = (
            "<span style=\"font-size:8px;background:#1a4a1a;border:1px solid #2a6a2a;"
            "border-radius:3px;padding:1px 5px;color:#80d080;margin-left:6px;\">&#9679; TURNO</span>"
            if eh_turno else ""
        )

        linhas.append(
            "<div style=\"display:grid;grid-template-columns:20px 180px 1fr;align-items:start;"
            "gap:8px;padding:7px 10px;background:" + bg_row + ";"
            "border:0.5px solid " + brd_row + ";border-radius:6px;margin-bottom:3px;\">"
            "<div style=\"font-size:16px;text-align:center;padding-top:2px;\">" + icone + "</div>"
            "<div>"
            "<div style=\"font-family:Cinzel,serif;font-size:11px;font-weight:600;"
            "color:" + cor_nom + ";letter-spacing:.06em;\">"
            + part["nome"] + badge
            + "</div>"
            "<div style=\"font-size:9px;color:#3a4a6a;margin-top:1px;\">init " + str(part["iniciativa"]) + "</div>"
            + conds
            + "</div>"
            "<div style=\"padding-top:2px;\">" + (barras if barras else sem_ficha) + "</div>"
            "</div>"
        )

    st.html("".join(linhas))
