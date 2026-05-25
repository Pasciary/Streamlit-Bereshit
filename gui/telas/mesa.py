import streamlit as st
import random, time

from gui import client
from gui.components.status_bar import show_bloco_status, show_status_bar


def mostrar():
    usuario   = st.session_state.get("usuario", {})
    eh_mestre = usuario.get("role") == "mestre"

    c1, c2 = st.columns([5, 1])
    with c1:
        st.title("🎲 Mesa de Jogo")
    with c2:
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()

    combate = client.estado_combate()
    ativo   = client.personagem_ativo_turno()
    fichas  = client.listar_fichas()

    col_status, col_init, col_dado = st.columns([2, 1.5, 1.5])

    with col_status:
        _render_personagem_ativo(ativo, fichas)

    with col_init:
        if combate.get("ativa"):
            _render_combate_ativo(combate, ativo, fichas, eh_mestre)
        else:
            if eh_mestre:
                _render_iniciar_combate(fichas)
            else:
                st.info("Aguardando o mestre iniciar o combate...")

    with col_dado:
        _render_rolagem(usuario, fichas)
        st.divider()
        _render_log()

    if combate.get("ativa"):
        st.divider()
        _render_panorama(combate, fichas)

    intervalo = 3 if combate.get("ativa") else 8
    time.sleep(intervalo)
    st.rerun()


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
        st.markdown(f"""
        <div class='hk-card' style='border-color:#5a4a30;'>
            <div style='font-family:Cinzel,serif;font-size:16px;font-weight:700;letter-spacing:.2em;color:#c8b89a;'>
                {part.get('nome','?').upper()}
            </div>
            <div style='font-size:10px;color:#6a5a40;'>Sem ficha registrada</div>
        </div>
        """, unsafe_allow_html=True)


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
    st.markdown("<div class='hk-section-title'>Rolar Dados</div>", unsafe_allow_html=True)
    personagem_ativo = st.session_state.get("personagem_ativo")
    dado   = st.selectbox("Dado", ["d4", "d6", "d8", "d10", "d12", "d20", "d100"])
    qtd    = st.number_input("Qtd", 1, 20, 1)
    mod    = st.number_input("Mod", -10, 20, 0)
    motivo = st.text_input("Motivo", placeholder="Ex: Ataque")

    if st.button("🎲 Rolar!", type="primary", use_container_width=True):
        lados      = int(dado[1:])
        resultados = [random.randint(1, lados) for _ in range(int(qtd))]
        total      = sum(resultados) + int(mod)
        critico    = dado == "d20" and resultados[0] == 20
        falha      = dado == "d20" and resultados[0] == 1
        nome_personagem = personagem_ativo["nome"] if personagem_ativo else usuario.get("nome", "Anônimo")
        client.rolar_dados(dado=dado, quantidade=int(qtd), modificador=int(mod),
            ficha_id=personagem_ativo["id"] if personagem_ativo else None,
            personagem=nome_personagem, motivo=motivo)
        if critico:
            st.success(f"🌟 CRÍTICO! **{total}** ({resultados} +{mod})")
        elif falha:
            st.error(f"💀 FALHA! **{total}**")
        else:
            st.info(f"🎲 **{total}** ({resultados} +{mod})")


def _render_log():
    st.markdown("<div class='hk-section-title'>Últimas Rolagens</div>", unsafe_allow_html=True)
    logs = client.log_dados()
    if not logs:
        st.info("Nenhuma rolagem ainda.")
        return
    for r in logs[:8]:
        badge = "🌟" if r.get("critico") else "💀" if r.get("falha_critica") else "🎲"
        st.markdown(f"""
        <div class='hk-card' style='margin-bottom:6px;'>
            <div style='font-size:11px;color:#6a5a40;'>{badge} {r['personagem']} · {r['dado']}</div>
            <div style='font-size:22px;font-weight:500;color:#c8b89a;font-family:Cinzel,serif;'>{r['total']}</div>
            {'<div style="font-size:10px;color:#5a4a30;">'+r['motivo']+'</div>' if r.get('motivo') else ''}
        </div>
        """, unsafe_allow_html=True)
    if st.button("🗑️ Limpar log", use_container_width=True):
        client.limpar_log()
        st.rerun()


def _render_panorama(combate, fichas):
    st.markdown("<div class='hk-section-title'>Panorama do Combate</div>", unsafe_allow_html=True)
    participantes = combate.get("iniciativa", [])
    if not participantes:
        return
    turno_atual = combate.get("turno_atual", 0)
    cols = st.columns(len(participantes))
    for i, part in enumerate(participantes):
        eh_turno = i == turno_atual
        borda = "#2a4a2a" if eh_turno else "#1a1a2a"
        bg    = "#0d1a0d" if eh_turno else "#0a0a12"
        cor   = "#80d080" if eh_turno else "#c8b89a"
        icone = "👑" if part.get("tipo") == "jogador" else "👹"
        with cols[i]:
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {borda};border-radius:6px;
                        padding:8px;text-align:center;margin-bottom:6px;'>
                <div style='font-size:9px;color:#5a4a30;letter-spacing:.1em;'>
                    {"● TURNO" if eh_turno else f"init {part['iniciativa']}"}
                </div>
                <div style='font-family:Cinzel,serif;font-size:11px;font-weight:600;
                            color:{cor};margin:4px 0;letter-spacing:.08em;'>
                    {part['nome'].upper()}
                </div>
                <div style='font-size:14px;'>{icone}</div>
            </div>
            """, unsafe_allow_html=True)
            ficha = next((f for f in fichas if f["nome"] == part.get("nome")), None)
            if ficha:
                status = ficha.get("status", {})
                vida   = status.get("vida", {})
                if not vida:
                    vida = {"atual": ficha.get("hp_atual", 0), "maximo": ficha.get("hp_max", 1)}
                show_status_bar("vida", vida["atual"], vida["maximo"])
            else:
                hp = part.get("hp", "?")
                hp_max = part.get("hp_max", hp)
                st.markdown(f"<div style='font-size:11px;color:#6a5a40;text-align:center;padding:4px;'>HP {hp} / {hp_max}</div>", unsafe_allow_html=True)
