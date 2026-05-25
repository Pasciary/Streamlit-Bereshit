"""
Paleta de cores unificada — tema Hollow Knight escuro
Usada em todo o projeto para manter consistência visual.
"""

# Cores base
BG_DEEP    = "#07070f"   # fundo mais escuro (sidebar, topbar)
BG_DARK    = "#0a0a12"   # fundo principal
BG_CARD    = "#0d0d1a"   # cards e painéis
BG_ITEM    = "#0a0a14"   # itens, linhas de lista
BG_HOVER   = "#12122a"   # hover

BORDER_DIM    = "#1a1a2a"   # bordas sutis
BORDER_MED    = "#2a2a3a"   # bordas médias
BORDER_GOLD   = "#3a3020"   # bordas douradas (HK)
BORDER_GOLD2  = "#5a4a30"   # bordas douradas mais fortes

TEXT_GOLD     = "#c8b89a"   # texto principal (dourado)
TEXT_MID      = "#8a7a6a"   # texto secundário
TEXT_DIM      = "#5a4a40"   # texto terciário
TEXT_ACCENT   = "#6a5a40"   # labels decorativos

# Semânticas
COLOR_SUCCESS = "#60d080"
COLOR_DANGER  = "#d06060"
COLOR_WARN    = "#c08040"
COLOR_INFO    = "#6080c0"

# CSS global injetado uma vez no app.py
GLOBAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&display=swap');

/* fundo geral */
body, .stApp {{ background-color: {BG_DARK}; color: {TEXT_GOLD}; }}

/* sidebar */
[data-testid="stSidebar"] {{
    background-color: {BG_DEEP} !important;
    border-right: 1px solid {BORDER_DIM};
}}
[data-testid="stSidebar"] * {{ color: {TEXT_MID}; }}
[data-testid="stSidebar"] .stButton button {{
    background: transparent;
    border: 0.5px solid transparent;
    color: {TEXT_MID};
    text-align: left;
    width: 100%;
    border-radius: 6px;
    transition: all .15s;
}}
[data-testid="stSidebar"] .stButton button:hover {{
    background: {BG_CARD};
    border-color: {BORDER_DIM};
    color: {TEXT_GOLD};
}}

/* topbar / header */
header[data-testid="stHeader"] {{ background: {BG_DEEP} !important; border-bottom: 1px solid {BORDER_DIM}; }}

/* inputs */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
    background-color: {BG_CARD} !important;
    color: {TEXT_GOLD} !important;
    border-color: {BORDER_MED} !important;
    border-radius: 6px !important;
}}

/* abas */
.stTabs [data-baseweb="tab-list"] {{ background: {BG_DEEP}; border-radius: 8px; padding: 2px; }}
.stTabs [data-baseweb="tab"] {{ background: transparent; color: {TEXT_DIM}; border-radius: 6px; }}
.stTabs [aria-selected="true"] {{ background: {BG_CARD}; color: {TEXT_GOLD}; }}

/* métricas */
div[data-testid="metric-container"] {{
    background: {BG_CARD};
    border: 0.5px solid {BORDER_DIM};
    border-radius: 8px;
    padding: 10px 14px;
}}
div[data-testid="metric-container"] label {{ color: {TEXT_DIM} !important; font-size: 11px !important; }}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {{ color: {TEXT_GOLD} !important; }}

/* containers / expanders */
.stExpander {{ background: {BG_CARD}; border: 0.5px solid {BORDER_DIM}; border-radius: 8px; }}
[data-testid="stVerticalBlock"] > div {{ color: {TEXT_GOLD}; }}

/* botões primários */
.stButton > button[kind="primary"] {{
    background: #1a2a1a !important;
    border-color: #2a4a2a !important;
    color: {COLOR_SUCCESS} !important;
}}
.stButton > button[kind="secondary"] {{
    background: {BG_CARD} !important;
    border-color: {BORDER_DIM} !important;
    color: {TEXT_MID} !important;
}}

/* progress bars */
.stProgress > div > div {{ background: {BORDER_GOLD2}; }}

/* divider */
hr {{ border-color: {BORDER_DIM}; }}

/* scrollbar */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: {BG_DEEP}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER_GOLD}; border-radius: 2px; }}

/* cards HK genéricos */
.hk-card {{
    background: {BG_CARD};
    border: 0.5px solid {BORDER_GOLD};
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 8px;
}}
.hk-card-title {{
    font-family: 'Cinzel', serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: .12em;
    color: {TEXT_GOLD};
    margin-bottom: 4px;
}}
.hk-card-sub {{
    font-size: 11px;
    color: {TEXT_DIM};
    letter-spacing: .06em;
}}
.hk-section-title {{
    font-family: 'Cinzel', serif;
    font-size: 9px;
    letter-spacing: .18em;
    color: {TEXT_ACCENT};
    margin: 12px 0 6px;
    text-transform: uppercase;
}}
.hk-badge {{
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 10px;
    background: {BG_CARD};
    color: {TEXT_DIM};
    border: 0.5px solid {BORDER_DIM};
    margin: 2px;
}}
.hk-badge-warn {{
    background: #1a1208;
    color: {COLOR_WARN};
    border-color: #3a2808;
}}
.hk-attr-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 6px;
    margin-bottom: 10px;
}}
.hk-attr-card {{
    background: {BG_ITEM};
    border: 0.5px solid {BORDER_GOLD};
    border-radius: 6px;
    padding: 8px 4px;
    text-align: center;
}}
.hk-attr-label {{ font-size: 10px; color: {TEXT_DIM}; letter-spacing:.05em; font-family:'Cinzel',serif; }}
.hk-attr-val   {{ font-size: 20px; font-weight: 500; color: {TEXT_GOLD}; line-height:1.2; font-family:'Cinzel',serif; }}
.hk-attr-mod   {{ font-size: 11px; color: {TEXT_MID}; }}
.hk-inv-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 10px;
    border: 0.5px solid {BORDER_GOLD};
    border-radius: 6px;
    background: {BG_ITEM};
    margin-bottom: 5px;
}}
.hk-inv-name {{ font-size: 13px; color: {TEXT_GOLD}; font-weight: 500; }}
.hk-inv-desc {{ font-size: 11px; color: {TEXT_DIM}; }}
</style>
"""
