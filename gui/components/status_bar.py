"""
Componente de barra de status estilo Hollow Knight para o sistema RPG.

Use show_status_bar() no Streamlit — SVG via st.markdown quebra o front (erro React).
"""

import math
import streamlit as st

# ─────────────────────────────────────────
# CONFIGURAÇÃO DOS STATUS
# ─────────────────────────────────────────

STATUS_CONFIG = {
    "vida":     {"label": "VIDA",     "descricao": "resistência física",                 "cor_inicio": "#e05050", "cor_fim": "#a02020", "simbolo": "vida"},
    "sanidade": {"label": "SANIDADE", "descricao": "resistência mental",                 "cor_inicio": "#4080d0", "cor_fim": "#1040a0", "simbolo": "sanidade"},
    "sangue":   {"label": "SANGUE",   "descricao": "reserva vital",                      "cor_inicio": "#c02030", "cor_fim": "#700010", "simbolo": "sangue"},
    "vigor":    {"label": "VIGOR",    "descricao": "poder físico · golpes especiais",    "cor_inicio": "#d08020", "cor_fim": "#805010", "simbolo": "vigor"},
    "mana":     {"label": "MANA",     "descricao": "magias básicas e intermediárias",    "cor_inicio": "#c0a0e0", "cor_fim": "#6030b0", "simbolo": "mana"},
    "ki":       {"label": "KI",       "descricao": "artes marciais · cultivadores",      "cor_inicio": "#c07820", "cor_fim": "#804800", "simbolo": "ki"},
    "arcana":   {"label": "ARCANA",   "descricao": "mana refinada · magias avançadas",   "cor_inicio": "#c0a0e0", "cor_fim": "#6030b0", "simbolo": "arcana"},
}

# ─────────────────────────────────────────
# CANTOS ORNAMENTAIS (compartilhado)
# ─────────────────────────────────────────

_CANTOS = """
    <polygon points="8,8 18,8 18,18 8,18" fill="#2a2010"/>
    <polygon points="8,8 15,8 15,11 11,11 11,15 8,15" fill="#5a4a30"/>
    <polygon points="52,8 42,8 42,18 52,18" fill="#2a2010"/>
    <polygon points="52,8 45,8 45,11 49,11 49,15 52,15" fill="#5a4a30"/>
    <polygon points="8,52 18,52 18,42 8,42" fill="#2a2010"/>
    <polygon points="8,52 15,52 15,49 11,49 11,45 8,45" fill="#5a4a30"/>
    <polygon points="52,52 42,52 42,42 52,42" fill="#2a2010"/>
    <polygon points="52,52 45,52 45,49 49,49 49,45 52,45" fill="#5a4a30"/>
"""

_CONECTOR = """
    <rect x="60" y="0"  width="10" height="60" fill="#0a0a0a"/>
    <rect x="60" y="0"  width="2"  height="60" fill="#3a3020"/>
    <rect x="60" y="0"  width="10" height="10" fill="#0d0b07"/>
    <rect x="60" y="9"  width="10" height="1"  fill="#3a3020"/>
    <rect x="60" y="50" width="10" height="10" fill="#0d0b07"/>
    <rect x="60" y="49" width="10" height="1"  fill="#3a3020"/>
    <rect x="63" y="28" width="4"  height="4"  fill="#2a2010"/>
    <rect x="63" y="28" width="4"  height="4"  fill="none" stroke="#4a3a22" stroke-width="0.7"/>
"""

# ─────────────────────────────────────────
# SÍMBOLOS SVG
# ─────────────────────────────────────────

_SIMBOLOS = {
    "vida": f"""{_CANTOS}
        <path d="M30,46 Q14,34 12,24 Q10,13 20,11 Q27,9 30,19" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <path d="M30,46 Q46,34 48,24 Q50,13 40,11 Q33,9 30,19" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <polyline points="30,19 27,26 33,30 28,36 30,46" fill="none" stroke="#5a4a30" stroke-width="1.3"/>
        <path d="M30,21 Q26,14 20,14 Q13,16 13,24 Q13,32 28,43" fill="none" stroke="#4a3a22" stroke-width="0.8"/>
        <path d="M30,21 Q34,14 40,14 Q47,16 47,24 Q47,32 32,43" fill="none" stroke="#4a3a22" stroke-width="0.8"/>""",

    "sanidade": f"""{_CANTOS}
        <ellipse cx="30" cy="30" rx="18" ry="20" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <ellipse cx="30" cy="30" rx="13" ry="15" fill="#1a1408" stroke="#4a3a22" stroke-width="1"/>
        <path d="M19,30 Q24,25 30,30 Q36,35 41,30" fill="none" stroke="#5a4a30" stroke-width="1.8"/>
        <line x1="23" y1="27" x2="21" y2="22" stroke="#5a4a30" stroke-width="1.1"/>
        <line x1="27" y1="25" x2="26" y2="19" stroke="#5a4a30" stroke-width="1.1"/>
        <line x1="30" y1="24" x2="30" y2="18" stroke="#5a4a30" stroke-width="1.1"/>
        <line x1="33" y1="25" x2="34" y2="19" stroke="#5a4a30" stroke-width="1.1"/>
        <line x1="37" y1="27" x2="39" y2="22" stroke="#5a4a30" stroke-width="1.1"/>
        <line x1="30" y1="10" x2="30" y2="13" stroke="#5a4a30" stroke-width="1.2"/>
        <circle cx="30" cy="10" r="1.5" fill="#4a3a22"/>
        <line x1="30" y1="47" x2="30" y2="50" stroke="#5a4a30" stroke-width="1.2"/>
        <circle cx="30" cy="50" r="1.5" fill="#4a3a22"/>
        <line x1="10" y1="30" x2="13" y2="30" stroke="#5a4a30" stroke-width="1.2"/>
        <circle cx="10" cy="30" r="1.5" fill="#4a3a22"/>
        <line x1="50" y1="30" x2="47" y2="30" stroke="#5a4a30" stroke-width="1.2"/>
        <circle cx="50" cy="30" r="1.5" fill="#4a3a22"/>""",

    "sangue": f"""{_CANTOS}
        <path d="M30,14 Q22,24 22,32 Q22,41 30,43 Q38,41 38,32 Q38,24 30,14Z" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <path d="M30,19 Q24,27 24,33 Q24,39 30,40 Q36,39 36,33 Q36,27 30,19Z" fill="#1e0808" stroke="#4a3a22" stroke-width="1"/>
        <path d="M22,46 Q19,49 19,51 Q19,54 22,54 Q25,54 25,51 Q25,49 22,46Z" fill="none" stroke="#4a3a22" stroke-width="1"/>
        <path d="M38,46 Q35,49 35,51 Q35,54 38,54 Q41,54 41,51 Q41,49 38,46Z" fill="none" stroke="#4a3a22" stroke-width="1"/>
        <circle cx="30" cy="8" r="1.5" fill="#4a3a22"/>
        <line x1="30" y1="10" x2="30" y2="13" stroke="#3a3020" stroke-width="0.8"/>""",

    "vigor": f"""{_CANTOS}
        <polygon points="30,10 35,28 30,52 25,28" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <polygon points="30,15 33,28 30,48 27,28" fill="#1e1a0e" stroke="#4a3a22" stroke-width="1"/>
        <path d="M25,28 Q14,22 10,13 Q20,20 27,28" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <path d="M35,28 Q46,22 50,13 Q40,20 33,28" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <path d="M25,34 Q15,30 11,22 Q20,27 27,34" fill="none" stroke="#4a3a22" stroke-width="1"/>
        <path d="M35,34 Q45,30 49,22 Q40,27 33,34" fill="none" stroke="#4a3a22" stroke-width="1"/>
        <circle cx="30" cy="50" r="2" fill="#5a4a30"/>
        <circle cx="30" cy="11" r="1.5" fill="#6a5a38"/>""",

    "mana": f"""{_CANTOS}
        <circle cx="30" cy="30" r="16" fill="none" stroke="#4a3a22" stroke-width="1.5"/>
        <circle cx="30" cy="30" r="11" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <circle cx="30" cy="30" r="5"  fill="#2a1e0e" stroke="#6a5a38" stroke-width="1"/>
        <line x1="30" y1="13" x2="30" y2="17" stroke="#5a4a30" stroke-width="1.5"/>
        <line x1="30" y1="43" x2="30" y2="47" stroke="#5a4a30" stroke-width="1.5"/>
        <line x1="13" y1="30" x2="17" y2="30" stroke="#5a4a30" stroke-width="1.5"/>
        <line x1="43" y1="30" x2="47" y2="30" stroke="#5a4a30" stroke-width="1.5"/>
        <line x1="19" y1="19" x2="22" y2="22" stroke="#4a3a22" stroke-width="1"/>
        <line x1="38" y1="38" x2="41" y2="41" stroke="#4a3a22" stroke-width="1"/>
        <line x1="41" y1="19" x2="38" y2="22" stroke="#4a3a22" stroke-width="1"/>
        <line x1="22" y1="38" x2="19" y2="41" stroke="#4a3a22" stroke-width="1"/>""",

    "ki": f"""{_CANTOS}
        <ellipse cx="30" cy="28" rx="7" ry="9" fill="none" stroke="#5a4a30" stroke-width="1.5"/>
        <ellipse cx="30" cy="28" rx="4" ry="6" fill="#1a1408" stroke="#4a3a22" stroke-width="1"/>
        <line x1="25" y1="25" x2="35" y2="25" stroke="#4a3a22" stroke-width="0.8"/>
        <line x1="25" y1="28" x2="35" y2="28" stroke="#4a3a22" stroke-width="0.8"/>
        <polygon points="30,37 27,44 30,52 33,44" fill="none" stroke="#5a4a30" stroke-width="1.3"/>
        <polygon points="30,40 28,44 30,50 32,44" fill="#1e1a0e" stroke="#4a3a22" stroke-width="0.8"/>
        <path d="M25,24 Q12,13 8,20 Q12,27 25,26" fill="none" stroke="#5a4a30" stroke-width="1.3"/>
        <path d="M35,24 Q48,13 52,20 Q48,27 35,26" fill="none" stroke="#5a4a30" stroke-width="1.3"/>
        <path d="M25,28 Q14,24 10,29 Q14,34 25,32" fill="none" stroke="#4a3a22" stroke-width="1"/>
        <path d="M35,28 Q46,24 50,29 Q46,34 35,32" fill="none" stroke="#4a3a22" stroke-width="1"/>
        <ellipse cx="30" cy="18" rx="5" ry="4" fill="#1a1408" stroke="#5a4a30" stroke-width="1.3"/>
        <circle cx="28" cy="17" r="1.2" fill="#3a3020" stroke="#5a4a30" stroke-width="0.7"/>
        <circle cx="32" cy="17" r="1.2" fill="#3a3020" stroke="#5a4a30" stroke-width="0.7"/>
        <path d="M29,14 Q27,10 24,8" fill="none" stroke="#5a4a30" stroke-width="1.1"/>
        <path d="M31,14 Q33,10 36,8" fill="none" stroke="#5a4a30" stroke-width="1.1"/>
        <circle cx="24" cy="8" r="1.2" fill="#4a3a22"/>
        <circle cx="36" cy="8" r="1.2" fill="#4a3a22"/>""",

    "arcana": f"""{_CANTOS}
        <circle cx="30" cy="30" r="20" fill="none" stroke="#2a2010" stroke-width="0.8" stroke-dasharray="2,4"/>
        <circle cx="30" cy="30" r="15" fill="none" stroke="#3a3020" stroke-width="0.8"/>
        <line x1="30" y1="15" x2="30" y2="8"  stroke="#6a5a38" stroke-width="1.8"/>
        <line x1="30" y1="45" x2="30" y2="52" stroke="#6a5a38" stroke-width="1.8"/>
        <line x1="15" y1="30" x2="8"  y2="30" stroke="#6a5a38" stroke-width="1.8"/>
        <line x1="45" y1="30" x2="52" y2="30" stroke="#6a5a38" stroke-width="1.8"/>
        <line x1="19" y1="19" x2="14" y2="14" stroke="#6a5a38" stroke-width="1.8"/>
        <line x1="41" y1="19" x2="46" y2="14" stroke="#6a5a38" stroke-width="1.8"/>
        <line x1="19" y1="41" x2="14" y2="46" stroke="#6a5a38" stroke-width="1.8"/>
        <line x1="41" y1="41" x2="46" y2="46" stroke="#6a5a38" stroke-width="1.8"/>
        <line x1="23" y1="16" x2="22" y2="11" stroke="#5a4a30" stroke-width="1"/>
        <line x1="37" y1="16" x2="38" y2="11" stroke="#5a4a30" stroke-width="1"/>
        <line x1="23" y1="44" x2="22" y2="49" stroke="#5a4a30" stroke-width="1"/>
        <line x1="37" y1="44" x2="38" y2="49" stroke="#5a4a30" stroke-width="1"/>
        <line x1="16" y1="23" x2="11" y2="22" stroke="#5a4a30" stroke-width="1"/>
        <line x1="16" y1="37" x2="11" y2="38" stroke="#5a4a30" stroke-width="1"/>
        <line x1="44" y1="23" x2="49" y2="22" stroke="#5a4a30" stroke-width="1"/>
        <line x1="44" y1="37" x2="49" y2="38" stroke="#5a4a30" stroke-width="1"/>
        <circle cx="30" cy="30" r="8" fill="#1a1408" stroke="#5a4a30" stroke-width="1.3"/>
        <circle cx="30" cy="30" r="5" fill="#141008" stroke="#4a3a22" stroke-width="0.8"/>
        <ellipse cx="30" cy="30" rx="1.5" ry="4" fill="#2a2010" stroke="#6a5a38" stroke-width="0.7"/>
        <circle cx="29" cy="29" r="0.8" fill="#5a4a30" opacity="0.6"/>""",
}


def _orn(tipo: str, espelhar: bool = False) -> str:
    mirror = 'style="transform:scaleX(-1)"' if espelhar else ''
    return f"""<svg {mirror} width="70" height="60" viewBox="0 0 70 60"
        xmlns="http://www.w3.org/2000/svg"
        style="flex-shrink:0;display:block;">
        <rect width="60" height="60" fill="#141008"/>
        <rect x="0" y="0" width="60" height="60" fill="none" stroke="#3a3020" stroke-width="1"/>
        {_SIMBOLOS.get(tipo, _SIMBOLOS['mana'])}
        {_CONECTOR}
    </svg>"""


def _deco() -> str:
    return """<svg width="100%" height="10" viewBox="0 0 400 10"
        preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="0" y1="5" x2="400" y2="5" stroke="#3a3020" stroke-width="0.8" stroke-dasharray="3,5"/>
        <rect x="90"  y="2" width="18" height="6" fill="none" stroke="#4a3a22" stroke-width="0.8"/>
        <rect x="93"  y="3" width="12" height="4" fill="#1a1408"/>
        <rect x="191" y="1" width="18" height="8" fill="none" stroke="#5a4a30" stroke-width="0.8"/>
        <polygon points="200,1 204,5 200,9 196,5" fill="none" stroke="#4a3a22" stroke-width="0.7"/>
        <rect x="292" y="2" width="18" height="6" fill="none" stroke="#4a3a22" stroke-width="0.8"/>
        <rect x="295" y="3" width="12" height="4" fill="#1a1408"/>
        <rect x="15"  y="3" width="6"  height="4" fill="#2a2010" rx="1"/>
        <rect x="379" y="3" width="6"  height="4" fill="#2a2010" rx="1"/>
    </svg>"""


# ─────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────

HK_CSS_RULES = """
.hk-label-row{font-family:'Cinzel',Georgia,serif;font-size:10px;letter-spacing:.18em;color:#6a5a40;margin-bottom:3px;display:flex;align-items:center;gap:6px;}
.hk-label-row span{color:#4a3a22;}
.hk-painel{display:flex;align-items:stretch;background:#0e0e0e;border-top:2px solid #5a4a30;border-bottom:2px solid #5a4a30;margin-bottom:2px;}
.hk-zona{flex:1;background:#0a0a0a;border-left:2px solid #3a3020;border-right:2px solid #3a3020;display:flex;flex-direction:column;}
.hk-deco-top{height:10px;flex-shrink:0;background:#0d0b07;border-bottom:1px solid #3a3020;overflow:hidden;}
.hk-deco-bot{height:10px;flex-shrink:0;background:#0d0b07;border-top:1px solid #3a3020;overflow:hidden;}
.hk-mid{flex:1;padding:4px 8px;background:#080806;display:flex;flex-direction:column;justify-content:center;}
.hk-outer{background:#050504;border:1.5px solid #4a3a22;padding:4px;box-shadow:inset 0 2px 8px rgba(0,0,0,0.9);}
.hk-track{height:24px;background:#0d0b08;border:1px solid #252018;position:relative;overflow:hidden;clip-path:polygon(3px 0%,calc(100% - 3px) 0%,100% 3px,100% calc(100% - 3px),calc(100% - 3px) 100%,3px 100%,0% calc(100% - 3px),0% 3px);}
.hk-track::before{content:'';position:absolute;inset:0;box-shadow:inset 2px 2px 10px rgba(0,0,0,0.95);z-index:3;pointer-events:none;}
.hk-fill{position:absolute;top:0;left:0;height:100%;z-index:1;transition:width 0.4s ease;}
.hk-fill::after{content:'';position:absolute;top:0;left:0;right:0;height:40%;background:rgba(255,255,255,0.12);pointer-events:none;}
.hk-fill::before{content:'';position:absolute;bottom:0;left:0;right:0;height:30%;background:rgba(0,0,0,0.3);pointer-events:none;}
.hk-text{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:6px;font-family:'Cinzel',Georgia,serif;font-size:11px;font-weight:600;letter-spacing:.08em;color:#e8dcc8;text-shadow:0 0 6px rgba(0,0,0,1),1px 1px 0 #000,-1px -1px 0 #000;white-space:nowrap;z-index:4;}
.hk-var{color:#8a7850;font-size:9px;}
.hk-nome{font-family:'Cinzel',Georgia,serif;font-size:16px;font-weight:700;letter-spacing:.22em;color:#c8b89a;text-align:center;margin-bottom:10px;text-shadow:0 0 12px rgba(200,184,154,0.2);}
"""

HK_CSS = f"<style>{HK_CSS_RULES}</style>"


def _html_doc(body: str, height: int = 0) -> None:
    """Renderiza HTML+SVG via st.html (substitui components.v1.html depreciado)."""
    doc = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&display=swap">
<style>
html,body{{margin:0;padding:0;background:transparent;overflow:hidden;}}
{HK_CSS_RULES}
</style></head><body>{body}</body></html>"""
    st.html(doc)


def show_status_bar(tipo: str, atual: int, maximo: int, variacao: int = None) -> None:
    _html_doc(render_status_bar(tipo, atual, maximo, variacao))


def show_bloco_status(ficha: dict, colunas: int = 2) -> None:
    nome = ficha.get("nome", "Personagem")
    status = ficha.get("status", {})
    ordem = ["vida", "sangue", "sanidade", "vigor", "mana", "ki", "arcana"]
    cells = []
    for tipo in ordem:
        dados = status.get(tipo)
        if dados:
            bar_html = render_status_bar(
                tipo=tipo,
                atual=dados.get("atual", 0),
                maximo=dados.get("maximo", 1),
                variacao=dados.get("variacao"),
            )
            cells.append(f"<div style='min-width:0'>{bar_html}</div>")
    if not cells:
        return
    grid = (
        f"<div style='display:grid;grid-template-columns:repeat({colunas},1fr);gap:4px 8px;'>"
        + "".join(cells)
        + "</div>"
    )
    _html_doc(f"<div class='hk-nome'>{nome.upper()}</div>{grid}")


# ─────────────────────────────────────────
# FUNÇÕES PÚBLICAS
# ─────────────────────────────────────────

def render_status_bar(tipo: str, atual: int, maximo: int, variacao: int = None) -> str:
    """Renderiza uma única barra de status."""
    cfg = STATUS_CONFIG.get(tipo, STATUS_CONFIG["vida"])
    pct = max(0.0, min(100.0, (atual / maximo * 100) if maximo > 0 else 0))

    var_html = ""
    if variacao is not None and variacao != 0:
        seta = "↓" if variacao < 0 else "↑"
        var_html = f'<span class="hk-var">( {seta} {abs(variacao)} )</span>'

    d = _deco()
    return f"""
    <div class="hk-label-row">— {cfg['label']} — <span>{cfg['descricao']}</span></div>
    <div class="hk-painel">
        {_orn(cfg['simbolo'])}
        <div class="hk-zona">
            <div class="hk-deco-top">{d}</div>
            <div class="hk-mid"><div class="hk-outer"><div class="hk-track">
                <div class="hk-fill" style="width:{pct:.1f}%;background:linear-gradient(to right,{cfg['cor_inicio']},{cfg['cor_fim']});"></div>
                <div class="hk-text">{cfg['label']} {atual} {var_html} <span class="hk-var">/ {maximo}</span></div>
            </div></div></div>
            <div class="hk-deco-bot">{d}</div>
        </div>
        {_orn(cfg['simbolo'], espelhar=True)}
    </div>"""


def render_bloco_status(ficha: dict) -> str:
    """Renderiza todas as barras de status de uma ficha completa."""
    nome   = ficha.get("nome", "Personagem")
    status = ficha.get("status", {})
    ordem  = ["vida", "sangue", "sanidade", "vigor", "mana", "ki", "arcana"]

    barras = ""
    for tipo in ordem:
        dados = status.get(tipo)
        if dados:
            barras += render_status_bar(
                tipo=tipo,
                atual=dados.get("atual", 0),
                maximo=dados.get("maximo", 1),
                variacao=dados.get("variacao"),
            )

    return f"{HK_CSS}<div class='hk-nome'>{nome.upper()}</div>{barras}"
