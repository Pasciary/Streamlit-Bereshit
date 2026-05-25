import streamlit as st

from gui import client
from gui.components.status_bar import show_status_bar

CONDICOES = ["Amedrontado","Agarrado","Atordoado","Caído","Cego",
             "Enfeitiçado","Envenenado","Exausto","Incapacitado",
             "Invisível","Paralisado","Petrificado","Surdo"]

def mostrar():
    usuario   = st.session_state.get("usuario", {})
    eh_mestre = usuario.get("role") == "mestre"

    ficha_id = st.session_state.get("ficha_id")
    if not ficha_id:
        st.error("Nenhuma ficha selecionada.")
        return

    ficha = client.buscar_ficha(ficha_id)
    if "erro" in ficha:
        st.error(ficha["erro"])
        return

    # jogador só vê a própria ficha
    if not eh_mestre:
        ficha_id_proprio = usuario.get("ficha_id")
        if ficha_id_proprio and ficha["id"] != ficha_id_proprio:
            st.error("Você não tem permissão para ver esta ficha.")
            st.session_state.tela = "fichas"
            st.rerun()
            return

    # cabeçalho
    c1, c2, c3 = st.columns([1, 5, 2])
    with c1:
        if st.button("←", use_container_width=True):
            st.session_state.tela = "fichas"
            st.rerun()
    with c2:
        st.markdown(f"""
        <div style='font-family:Cinzel,serif;'>
            <div style='font-size:20px;font-weight:700;letter-spacing:.15em;color:#c8b89a;'>{ficha['nome']}</div>
            <div style='font-size:11px;color:#5a4a30;letter-spacing:.08em;'>{ficha['raca']} · {ficha['classe']} · {ficha['alinhamento']} · Nível {ficha['nivel']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        if st.button("🎲 Jogar", use_container_width=True, type="primary"):
            st.session_state.personagem_ativo = ficha
            st.session_state.tela = "mesa"
            st.rerun()

    if ficha.get("condicoes"):
        conds = " · ".join(ficha["condicoes"])
        st.warning(f"⚠️ Condições ativas: **{conds}**")

    st.divider()

    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        "⚔️ Status", "🎒 Inventário", "📖 Magias", "😴 Descanso", "📝 Info"
    ])
    with aba1: _aba_status(ficha, eh_mestre)
    with aba2: _aba_inventario(ficha, eh_mestre)
    with aba3: _aba_magias(ficha, eh_mestre)
    with aba4: _aba_descanso(ficha)
    with aba5: _aba_info(ficha)


def _aba_status(ficha, eh_mestre):
    status = ficha.get("status", {})
    vida_a = status.get("vida", {}).get("atual", ficha.get("hp_atual", 0))
    vida_m = status.get("vida", {}).get("maximo", ficha.get("hp_max", 1))

    show_status_bar("vida", vida_a, vida_m)
    for tipo in ["sanidade", "sangue", "vigor", "mana", "ki", "arcana"]:
        d = status.get(tipo)
        if d:
            show_status_bar(tipo, d["atual"], d["maximo"], d.get("variacao"))

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='hk-section-title'>Ajustar Vida</div>", unsafe_allow_html=True)

        # só mestre (ou o próprio jogador) pode editar
        novo_hp = st.number_input("HP Atual", 0, vida_m, vida_a, key="hp_input")
        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            dano = st.number_input("Dano", 0, 999, 0, key="dano_input")
            if st.button("Aplicar Dano", use_container_width=True):
                client.atualizar_hp(ficha["id"], max(0, vida_a - dano))
                st.rerun()
        with ca2:
            cura = st.number_input("Cura", 0, 999, 0, key="cura_input")
            if st.button("Aplicar Cura", use_container_width=True):
                client.atualizar_hp(ficha["id"], min(vida_m, vida_a + cura))
                st.rerun()
        with ca3:
            st.write("")
            st.write("")
            if st.button("💾 Salvar", use_container_width=True, type="primary"):
                client.atualizar_hp(ficha["id"], novo_hp)
                st.rerun()

        st.divider()
        st.markdown("<div class='hk-section-title'>Combate</div>", unsafe_allow_html=True)
        cb1, cb2, cb3 = st.columns(3)
        cb1.metric("Armadura", ficha["ca"])
        cb2.metric("Iniciativa", f"+{ficha['iniciativa']}" if ficha['iniciativa'] >= 0 else str(ficha['iniciativa']))
        cb3.metric("Prof.", f"+{ficha['bonus_proficiencia']}")

        # condições — só mestre edita
        if eh_mestre:
            st.divider()
            st.markdown("<div class='hk-section-title'>Condições</div>", unsafe_allow_html=True)
            nova = st.selectbox("Adicionar condição", [""] + CONDICOES, key="nova_cond")
            if nova and st.button("Adicionar"):
                client.adicionar_condicao(ficha["id"], nova)
                st.rerun()
            if ficha.get("condicoes"):
                for cond in ficha["condicoes"]:
                    cc1, cc2 = st.columns([4, 1])
                    cc1.write(f"⚠️ {cond}")
                    if cc2.button("✕", key=f"rm_{cond}"):
                        client.remover_condicao(ficha["id"], cond)
                        st.rerun()
        else:
            if ficha.get("condicoes"):
                st.divider()
                st.markdown("<div class='hk-section-title'>Condições Ativas</div>", unsafe_allow_html=True)
                for c in ficha["condicoes"]:
                    st.markdown(f"<span class='hk-badge hk-badge-warn'>⚠️ {c}</span>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='hk-section-title'>Atributos</div>", unsafe_allow_html=True)
        NOMES = {
            "forca":"💪 Força","destreza":"🏃 Destreza","constituicao":"❤️ Constituição",
            "inteligencia":"🧠 Inteligência","sabedoria":"🦉 Sabedoria","carisma":"✨ Carisma"
        }
        attr_cards = []
        for chave, label in NOMES.items():
            val = ficha["atributos"].get(chave, 10)
            mod = ficha["modificadores"].get(chave, 0)
            sinal = "+" if mod >= 0 else ""
            attr_cards.append(
                f"<div class='hk-attr-card'>"
                f"<div class='hk-attr-label'>{label}</div>"
                f"<div class='hk-attr-val'>{val}</div>"
                f"<div class='hk-attr-mod'>{sinal}{mod}</div></div>"
            )
        st.markdown("<div class='hk-attr-grid'>" + "".join(attr_cards) + "</div>", unsafe_allow_html=True)

        st.markdown("<div class='hk-section-title'>Progressão</div>", unsafe_allow_html=True)
        xp_pct = ficha["xp"] / ficha["xp_proximo"] if ficha["xp_proximo"] > 0 else 0
        st.progress(xp_pct, text=f"XP: {ficha['xp']} / {ficha['xp_proximo']}")
        st.metric("Nível", ficha["nivel"])
        st.metric("Movimento", f"{ficha['movimento']}m")


def _aba_inventario(ficha, eh_mestre):
    st.subheader("🎒 Inventário")

    # catálogo rápido
    with st.expander("🛒 Adicionar do Catálogo"):
        catalogo = client.catalogo_itens()
        for item in catalogo:
            cc1, cc2, cc3 = st.columns([4, 1, 1])
            cc1.write(f"**{item['nome']}** — {item.get('descricao','')}")
            cc2.write(f"💰{item['preco']}po")
            if cc3.button("+ Pegar", key=f"cat_{item['id']}"):
                client.adicionar_item(ficha["id"], item["nome"], 1, item.get("descricao",""), item["tipo"])
                st.rerun()

    with st.expander("➕ Item personalizado"):
        with st.form("form_item"):
            ci1, ci2 = st.columns([3, 1])
            with ci1:
                nome_item = st.text_input("Nome")
                desc_item = st.text_input("Descrição")
            with ci2:
                qtd = st.number_input("Qtd", 1, 99, 1)
            if st.form_submit_button("Adicionar") and nome_item:
                client.adicionar_item(ficha["id"], nome_item, qtd, desc_item)
                st.rerun()

    st.divider()
    itens = client.listar_inventario(ficha["id"])
    if not itens:
        st.info("Inventário vazio.")
        return

    for item in itens:
        with st.container():
            st.markdown(f"""
            <div class='hk-inv-item'>
                <div style='flex:1;'>
                    <div class='hk-inv-name'>{item['nome']}</div>
                    {'<div class="hk-inv-desc">'+item["descricao"]+'</div>' if item.get("descricao") else ''}
                </div>
                <div style='font-size:12px;color:#5a4a30;'>x{item['quantidade']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗑️ Remover", key=f"del_item_{item['id']}"):
                client.remover_item(ficha["id"], item["id"])
                st.rerun()


def _aba_magias(ficha, eh_mestre):
    if not ficha.get("tem_magia"):
        st.info(f"A classe **{ficha['classe']}** não usa magia.")
        return

    st.subheader("🔮 Slots de Magia")
    slots  = ficha.get("slots_magia", {})
    usados = ficha.get("slots_usados", {})

    cols = st.columns(5)
    for i, nivel in enumerate([1,2,3,4,5]):
        total = slots.get(nivel, 0)
        gasto = usados.get(nivel, 0)
        disp  = total - gasto
        with cols[i]:
            st.metric(f"Nível {nivel}", f"{disp}/{total}")
            if disp > 0:
                if st.button(f"Usar", key=f"slot_{nivel}"):
                    client.usar_slot(ficha["id"], nivel)
                    st.rerun()

    st.divider()
    st.subheader("📖 Magias Conhecidas")
    magias_ficha = client.listar_magias_ficha(ficha["id"])
    catalogo     = client.catalogo_magias()
    ids_conhecidos = [m["id"] for m in magias_ficha]

    with st.expander("✨ Aprender nova magia"):
        for m in catalogo:
            if m["id"] not in ids_conhecidos:
                mm1, mm2 = st.columns([4, 1])
                mm1.write(f"**{m['nome']}** (Nv.{m['nivel']}) — {m['escola']}")
                mm1.caption(m["descricao"])
                if mm2.button("Aprender", key=f"aprender_{m['id']}"):
                    client.aprender_magia(ficha["id"], m["id"])
                    st.rerun()

    if not magias_ficha:
        st.info("Nenhuma magia aprendida.")
        return

    for m in magias_ficha:
        nivel_label = "Truque" if m["nivel"] == 0 else f"Nível {m['nivel']}"
        with st.container():
            st.markdown(f"""
            <div class='hk-card'>
                <div style='display:flex;justify-content:space-between;'>
                    <div class='hk-card-title'>{m['nome']}</div>
                    <span class='hk-badge'>{nivel_label} · {m['escola']}</span>
                </div>
                <div style='font-size:11px;color:#5a4a30;margin:4px 0;'>🎯 {m['alcance']} &nbsp;·&nbsp; ⏱ {m['duracao']} &nbsp;·&nbsp; 🔮 {m['componentes']}</div>
                <div style='font-size:12px;color:#8a7a6a;'>{m['descricao']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Esquecer", key=f"esquecer_{m['id']}"):
                client.esquecer_magia(ficha["id"], m["id"])
                st.rerun()


def _aba_descanso(ficha):
    st.subheader("😴 Descanso")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='hk-card'>
            <div class='hk-card-title'>☕ Descanso Curto</div>
            <div class='hk-card-sub'>~1 hora · rola 1d8+CON de HP</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Iniciar Descanso Curto", use_container_width=True, type="primary"):
            res = client.descanso(ficha["id"], "curto")
            if "erro" in res:
                st.error(res["erro"])
            else:
                st.success(f"Recuperou {res['hp_recuperado']} HP! HP atual: {res['hp_atual']}")
    with c2:
        st.markdown("""<div class='hk-card'>
            <div class='hk-card-title'>🌙 Descanso Longo</div>
            <div class='hk-card-sub'>~8 horas · restaura tudo</div>
        </div>""", unsafe_allow_html=True)
        st.warning("Use apenas ao final do dia de aventura!")
        if st.button("Iniciar Descanso Longo", use_container_width=True):
            res = client.descanso(ficha["id"], "longo")
            if "erro" in res:
                st.error(res["erro"])
            else:
                st.success("HP e recursos totalmente restaurados!")
                st.balloons()
                st.rerun()


def _aba_info(ficha):
    st.subheader("📝 Informações")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='hk-card'>
            <table style='width:100%;font-size:12px;border-collapse:collapse;'>
                <tr><td style='color:#5a4a30;padding:5px 0;width:40%'>Nome</td><td style='color:#c8b89a;'>{ficha['nome']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Raça</td><td style='color:#c8b89a;'>{ficha['raca']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Classe</td><td style='color:#c8b89a;'>{ficha['classe']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Background</td><td style='color:#c8b89a;'>{ficha['background']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Alinhamento</td><td style='color:#c8b89a;'>{ficha['alinhamento']}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='hk-card'>
            <table style='width:100%;font-size:12px;border-collapse:collapse;'>
                <tr><td style='color:#5a4a30;padding:5px 0;width:40%'>Nível</td><td style='color:#c8b89a;'>{ficha['nivel']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>XP</td><td style='color:#c8b89a;'>{ficha['xp']} / {ficha['xp_proximo']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>CA</td><td style='color:#c8b89a;'>{ficha['ca']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Iniciativa</td><td style='color:#c8b89a;'>+{ficha['iniciativa']}</td></tr>
                <tr><td style='color:#5a4a30;padding:5px 0;'>Movimento</td><td style='color:#c8b89a;'>{ficha['movimento']}m</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    if ficha.get("historia"):
        st.divider()
        st.subheader("📖 História")
        st.markdown(f"""
        <div class='hk-card'>
            <div style='font-size:13px;color:#8a7a6a;line-height:1.8;'>{ficha['historia']}</div>
        </div>
        """, unsafe_allow_html=True)
