# Paleta de cores
BG_DEEP    = "#07070f"
BG_DARK    = "#0a0a12"
BG_CARD    = "#0d0d1a"
BG_ITEM    = "#0a0a14"

BORDER_DIM    = "#1a1a2a"
BORDER_MED    = "#2a2a3a"
BORDER_GOLD   = "#3a3020"
BORDER_GOLD2  = "#5a4a30"

TEXT_GOLD   = "#c8b89a"
TEXT_MID    = "#8a7a6a"
TEXT_DIM    = "#5a4a40"
TEXT_ACCENT = "#6a5a40"

COLOR_SUCCESS = "#60d080"
COLOR_DANGER  = "#d06060"
COLOR_WARN    = "#c08040"
COLOR_INFO    = "#6080c0"

GLOBAL_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&display=swap');

body, .stApp {{ background-color: {BG_DARK}; color: {TEXT_GOLD}; }}

h1, h2, h3, h4 {{ color: {TEXT_GOLD} !important; font-family: 'Cinzel', serif; letter-spacing: .06em; }}

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

header[data-testid="stHeader"] {{ background: {BG_DEEP} !important; border-bottom: 1px solid {BORDER_DIM}; }}

.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {{
    background-color: {BG_CARD} !important;
    color: {TEXT_GOLD} !important;
    border-color: {BORDER_MED} !important;
    border-radius: 6px !important;
}}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label {{ color: {TEXT_MID} !important; font-size: 12px !important; }}

.stTabs [data-baseweb="tab-list"] {{ background: {BG_DEEP}; border-radius: 8px; padding: 2px; }}
.stTabs [data-baseweb="tab"] {{ background: transparent; color: {TEXT_DIM}; border-radius: 6px; }}
.stTabs [aria-selected="true"] {{ background: {BG_CARD}; color: {TEXT_GOLD}; }}

div[data-testid="metric-container"] {{
    background: {BG_CARD};
    border: 0.5px solid {BORDER_DIM};
    border-radius: 8px;
    padding: 10px 14px;
}}
div[data-testid="metric-container"] label {{ color: {TEXT_DIM} !important; font-size: 11px !important; }}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {{ color: {TEXT_GOLD} !important; }}

.stExpander {{ background: {BG_CARD}; border: 0.5px solid {BORDER_DIM}; border-radius: 8px; }}
[data-testid="stVerticalBlock"] > div {{ color: {TEXT_GOLD}; }}
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {BG_CARD} !important;
    border-color: {BORDER_GOLD} !important;
    border-radius: 8px !important;
}}

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

.stProgress > div > div {{ background: {BORDER_GOLD2}; }}
[data-testid="stProgressBar"] {{ background: {BORDER_DIM}; }}

hr {{ border-color: {BORDER_DIM}; }}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: {BG_DEEP}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER_GOLD}; border-radius: 2px; }}

.stAlert {{ background: {BG_CARD} !important; border-color: {BORDER_GOLD} !important; color: {TEXT_MID} !important; }}

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
    margin: 16px 0 8px;
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
.hk-attr-grid {{
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 6px;
    margin: 8px 0 16px;
}}
.hk-attr-card {{
    background: {BG_ITEM};
    border: 0.5px solid {BORDER_GOLD};
    border-radius: 6px;
    padding: 10px 4px;
    text-align: center;
}}
.hk-attr-label {{ font-size: 9px; color: {TEXT_DIM}; letter-spacing: .08em; font-family: 'Cinzel', serif; }}
.hk-attr-val   {{ font-size: 22px; font-weight: 600; color: {TEXT_GOLD}; line-height: 1.2; font-family: 'Cinzel', serif; }}
.hk-attr-mod   {{ font-size: 11px; color: {TEXT_MID}; margin-top: 2px; }}
</style>
"""
