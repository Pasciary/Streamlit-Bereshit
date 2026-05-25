"""
Dados fictícios para validar o front sem a API (uvicorn) rodando.

Ative o modo mock em gui/client.py (ENABLE_MOCK = True)
ou defina a variável de ambiente: RPG_USE_MOCK=1

Para ajustar personagens, campanha e status sem editar Python:
  edite  gui/mock_config.ini
"""

import configparser
import copy
import os

ENABLE_MOCK = True

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "mock_config.ini")

# ── leitura do config ─────────────────────────────────────────────────────────

def _load_config():
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.read(_CONFIG_PATH, encoding="utf-8")
    return cfg


def _padroes_do_config(cfg):
    s = cfg["Status.Padrao"] if cfg.has_section("Status.Padrao") else {}
    def _f(key, default):
        try:
            return float(s.get(key, default))
        except (TypeError, ValueError):
            return float(default)
    return {
        "sangue":   _f("sangue_fator",   0.18),
        "sanidade": _f("sanidade_fator", 0.57),
        "vigor":    _f("vigor_fator",    0.14),
        "mana":     _f("mana_fator",     0.44),
        "ki":       _f("ki_fator",       0.14),
        "arcana":   _f("arcana_fator",   0.14),
    }


def _parse_status(s, key_max, key_at, hp_max, fator):
    """Retorna {"atual": X, "maximo": Y}. Campo vazio = 100% do máximo."""
    def _to_int(val, fallback):
        try:
            return int(str(val).strip())
        except (ValueError, TypeError):
            return fallback
    vmax = _to_int(s.get(key_max, ""), max(1, round(hp_max * fator)))
    vat  = _to_int(s.get(key_at,  ""), vmax)
    return {"atual": vat, "maximo": vmax}


def _fichas_do_config(cfg):
    padroes = _padroes_do_config(cfg)
    fichas  = {}
    for section in cfg.sections():
        if not section.lower().startswith("personagem."):
            continue
        s        = cfg[section]
        ficha_id = s.get("id", "").strip() or section.split(".", 1)[1]
        hp_max   = int(s.get("vida_maxima", "10").strip() or "10")

        raw_at = s.get("vida_atual", "").strip()
        hp_atual = int(raw_at) if raw_at else hp_max

        status = {
            "vida":     {"atual": hp_atual, "maximo": hp_max},
            "sangue":   _parse_status(s, "sangue_maxima",   "sangue_atual",   hp_max, padroes["sangue"]),
            "sanidade": _parse_status(s, "sanidade_maxima", "sanidade_atual", hp_max, padroes["sanidade"]),
            "vigor":    _parse_status(s, "vigor_maxima",    "vigor_atual",    hp_max, padroes["vigor"]),
        }
        for recurso in ("mana", "ki", "arcana"):
            if s.get(f"{recurso}_maxima", "").strip():
                status[recurso] = _parse_status(
                    s, f"{recurso}_maxima", f"{recurso}_atual", hp_max, padroes[recurso]
                )

        cond_raw   = s.get("condicoes", "").strip()
        condicoes  = [c.strip() for c in cond_raw.split(",") if c.strip()] if cond_raw else []

        def _int(key, default=0):
            try:
                return int(s.get(key, str(default)).strip() or str(default))
            except ValueError:
                return default

        fichas[ficha_id] = {
            "id":                 ficha_id,
            "nome":               s.get("nome",       "Personagem").strip(),
            "raca":               s.get("raca",       "Humano").strip(),
            "classe":             s.get("classe",     "Aventureiro").strip(),
            "background":         s.get("background", "").strip(),
            "alinhamento":        s.get("alinhamento","").strip(),
            "historia":           s.get("historia",   "").strip(),
            "nivel":              _int("nivel",  1),
            "xp":                 _int("xp",     0),
            "xp_proximo":         _int("xp_proximo", 300),
            "atributos":          {},
            "modificadores":      {},
            "hp_max":             hp_max,
            "hp_atual":           hp_atual,
            "ca":                 _int("ca",  10),
            "bonus_proficiencia": _int("bonus_proficiencia", 2),
            "iniciativa":         _int("iniciativa", 0),
            "movimento":          _int("movimento",  9),
            "tem_magia":          "mana" in status,
            "slots_magia":        {},
            "slots_usados":       {},
            "condicoes":          condicoes,
            "criado_em":          s.get("criado_em", "").strip(),
            "status":             status,
        }
    return fichas


def _combate_do_config(cfg, fichas):
    if not cfg.has_section("Combate"):
        return copy.deepcopy(SESSAO_COMBATE)

    s     = cfg["Combate"]
    ativa = s.get("ativa", "false").strip().lower() in ("true", "1", "yes", "sim")
    if not ativa:
        return {"ativa": False, "rodada": 0, "turno_atual": 0, "iniciativa": []}

    def _int(key, default=0):
        try:
            return int(s.get(key, str(default)).strip() or str(default))
        except ValueError:
            return default

    rodada    = _int("rodada", 1)
    turno     = _int("turno_atual", 0)
    raw       = s.get("participantes", "").strip()
    por_nome  = {f["nome"]: f for f in fichas.values()}

    participantes = []
    for parte in raw.split(","):
        campos = [c.strip() for c in parte.strip().split(":")]
        if len(campos) < 3:
            continue
        nome, tipo, init = campos[0], campos[1], campos[2]
        try:
            init = int(init)
        except ValueError:
            init = 0
        entry = {"nome": nome, "tipo": tipo, "iniciativa": init}
        if nome in por_nome:
            f = por_nome[nome]
            entry["hp"]     = f["hp_atual"]
            entry["hp_max"] = f["hp_max"]
        participantes.append(entry)

    return {"ativa": True, "rodada": rodada, "turno_atual": turno, "iniciativa": participantes}


# ── carrega config uma vez na importação ──────────────────────────────────────
_cfg = _load_config()

# Fatores exportados — mock_client.criar_ficha() usa para novas fichas
STATUS_PADROES = _padroes_do_config(_cfg)


# ── usuários (hardcoded — senhas não vão para o config) ──────────────────────
USUARIOS = {
    "mestre": {
        "id": "mestre",
        "nome": "Mestre",
        "senha": "1234",
        "role": "mestre",
        "ficha_id": None,
    },
    "jogador1": {
        "id": "jogador1",
        "nome": "Jogador 1",
        "senha": "1234",
        "role": "jogador",
        "ficha_id": "a1b2c3d4",
    },
    "jogador2": {
        "id": "jogador2",
        "nome": "Jogador 2",
        "senha": "1234",
        "role": "jogador",
        "ficha_id": "e5f6g7h8",
    },
    "zeny": {
        "id": "zeny",
        "nome": "Zeny",
        "senha": "002502",
        "role": "mestre",
        "ficha_id": None,
    },
    "duda": {
        "id": "duda",
        "nome": "Duda",
        "senha": "1234",
        "role": "jogador",
        "ficha_id": None,
    },
    "leo": {
        "id": "leo",
        "nome": "Leo",
        "senha": "1234",
        "role": "jogador",
        "ficha_id": None,
    },
    "marquinhos": {
        "id": "marquinhos",
        "nome": "Marquinhos",
        "senha": "1234",
        "role": "jogador",
        "ficha_id": None,
    },
}

# ── campanhas ─────────────────────────────────────────────────────────────────
def _campanhas_do_config(cfg):
    if not cfg.has_section("Campanha"):
        return copy.deepcopy(CAMPANHAS_PADRAO)

    s       = cfg["Campanha"]
    titulo  = s.get("titulo",    "Campanha").strip()
    descr   = s.get("descricao", "").strip()
    mestre  = s.get("mestre",    "mestre").strip()
    jogs    = [j.strip() for j in s.get("jogadores", "").split(",") if j.strip()]

    membros = [{"usuario_id": mestre, "role": "mestre", "ficha_id": None}]
    for j in jogs:
        membros.append({"usuario_id": j, "role": "jogador", "ficha_id": None})

    return {
        "camp01": {
            "id": "camp01",
            "nome": titulo,
            "descricao": descr,
            "criado_em": "2026-05-01",
            "membros": membros,
        }
    }


CAMPANHAS_PADRAO = {
    "camp01": {
        "id": "camp01",
        "nome": "A Maldição de Ironthorn",
        "descricao": "Uma maldição ancestral ameaça a cidade mineira de Ironthorn.",
        "criado_em": "2026-05-01",
        "membros": [
            {"usuario_id": "zeny",       "role": "mestre",  "ficha_id": None},
            {"usuario_id": "duda",       "role": "jogador", "ficha_id": None},
            {"usuario_id": "leo",        "role": "jogador", "ficha_id": None},
            {"usuario_id": "marquinhos", "role": "jogador", "ficha_id": None},
        ],
    },
}

# ── catálogos (hardcoded — são dados do sistema de jogo) ─────────────────────
ITENS_CATALOGO = [
    {"id": "1", "nome": "Espada Longa",       "tipo": "arma",       "dano": "1d8",   "preco": 15,  "peso": 3,    "descricao": "Arma versátil de uma ou duas mãos"},
    {"id": "2", "nome": "Arco Curto",          "tipo": "arma",       "dano": "1d6",   "preco": 25,  "peso": 2,    "descricao": "Arco para ataques à distância"},
    {"id": "3", "nome": "Armadura de Couro",   "tipo": "armadura",   "ca": 11,        "preco": 10,  "peso": 10,   "descricao": "Proteção leve e silenciosa"},
    {"id": "4", "nome": "Cota de Malha",       "tipo": "armadura",   "ca": 16,        "preco": 75,  "peso": 55,   "descricao": "Armadura média resistente"},
    {"id": "5", "nome": "Poção de Cura",       "tipo": "consumivel", "efeito": "2d4+2 HP", "preco": 50, "peso": 0.5, "descricao": "Restaura pontos de vida"},
    {"id": "6", "nome": "Tocha",               "tipo": "equipamento","preco": 1,  "peso": 1,  "descricao": "Ilumina 6m por 1 hora"},
    {"id": "7", "nome": "Corda (15m)",         "tipo": "equipamento","preco": 1,  "peso": 10, "descricao": "Corda resistente de cânhamo"},
    {"id": "8", "nome": "Grimório",            "tipo": "equipamento","preco": 50, "peso": 3,  "descricao": "Livro de magias do mago"},
]

MAGIAS_CATALOGO = [
    {"id": "1", "nome": "Míssil Mágico",    "nivel": 1, "escola": "Evocação",      "alcance": "18m",   "componentes": "V, S",    "duracao": "Instantâneo", "descricao": "3 dardos de força causando 1d4+1 cada"},
    {"id": "2", "nome": "Bola de Fogo",     "nivel": 3, "escola": "Evocação",      "alcance": "45m",   "componentes": "V, S, M", "duracao": "Instantâneo", "descricao": "Explosão de 8d6 de dano de fogo em raio de 6m"},
    {"id": "3", "nome": "Curar Ferimentos", "nivel": 1, "escola": "Evocação",      "alcance": "Toque", "componentes": "V, S",    "duracao": "Instantâneo", "descricao": "Restaura 1d8 + mod Sabedoria de HP"},
    {"id": "4", "nome": "Escudo",           "nivel": 1, "escola": "Abjuração",     "alcance": "Pessoal","componentes": "V, S",   "duracao": "1 rodada",    "descricao": "+5 CA como reação"},
    {"id": "5", "nome": "Sono",             "nivel": 1, "escola": "Encantamento",  "alcance": "27m",   "componentes": "V, S, M", "duracao": "1 minuto",    "descricao": "Adormece criaturas com até 5d8 HP"},
    {"id": "6", "nome": "Luz",              "nivel": 0, "escola": "Evocação",      "alcance": "Toque", "componentes": "V, M",    "duracao": "1 hora",      "descricao": "Objeto emite luz por 6m"},
    {"id": "7", "nome": "Prestidigitação",  "nivel": 0, "escola": "Transmutação",  "alcance": "3m",    "componentes": "V, S",    "duracao": "Até 1 hora",  "descricao": "Efeitos mágicos menores variados"},
]

MONSTROS_CATALOGO = [
    {"id": "1", "nome": "Goblin",       "hp": 7,   "ca": 15, "ataque": "+4",  "dano": "1d6+2",  "cr": "1/4", "xp": 50},
    {"id": "2", "nome": "Orc",          "hp": 15,  "ca": 13, "ataque": "+5",  "dano": "1d12+3", "cr": "1/2", "xp": 100},
    {"id": "3", "nome": "Esqueleto",    "hp": 13,  "ca": 13, "ataque": "+4",  "dano": "1d6+2",  "cr": "1/4", "xp": 50},
    {"id": "4", "nome": "Zumbi",        "hp": 22,  "ca": 8,  "ataque": "+3",  "dano": "1d6+1",  "cr": "1/4", "xp": 50},
    {"id": "5", "nome": "Lobo",         "hp": 11,  "ca": 13, "ataque": "+4",  "dano": "2d4+2",  "cr": "1/4", "xp": 50},
    {"id": "6", "nome": "Dragão Jovem", "hp": 178, "ca": 18, "ataque": "+10", "dano": "2d10+6", "cr": "10",  "xp": 5900},
]

# ── inventários / magias (hardcoded, vinculados por ficha_id fixo) ───────────
INVENTARIOS = {
    "a1b2c3d4": [
        {"id": "inv01", "nome": "Espada Longa",   "quantidade": 1, "descricao": "Arma principal",   "tipo": "arma"},
        {"id": "inv02", "nome": "Cota de Malha",  "quantidade": 1, "descricao": "Armadura equipada","tipo": "armadura"},
        {"id": "inv03", "nome": "Poção de Cura",  "quantidade": 2, "descricao": "2d4+2 HP",         "tipo": "consumivel"},
    ],
    "e5f6g7h8": [
        {"id": "inv04", "nome": "Grimório",            "quantidade": 1, "descricao": "Livro de magias",       "tipo": "equipamento"},
        {"id": "inv05", "nome": "Componentes arcanos", "quantidade": 1, "descricao": "Bolsa de componentes",  "tipo": "equipamento"},
    ],
    "i9j0k1l2": [
        {"id": "inv06", "nome": "Adaga",                 "quantidade": 2, "descricao": "Par de adagas", "tipo": "arma"},
        {"id": "inv07", "nome": "Ferramentas de ladrão", "quantidade": 1, "descricao": "",              "tipo": "equipamento"},
    ],
}

MAGIAS_CONHECIDAS_PADRAO = {
    "e5f6g7h8": [MAGIAS_CATALOGO[0], MAGIAS_CATALOGO[2], MAGIAS_CATALOGO[3], MAGIAS_CATALOGO[5]],
    "a1b2c3d4": [],
    "i9j0k1l2": [],
}

LOG_DADOS = [
    {"id": "r001", "ficha_id": "a1b2c3d4", "personagem": "Thorn Hollow",    "dado": "d20", "quantidade": 1, "resultados": [20], "modificador": 5, "total": 25, "motivo": "Ataque com espada",        "critico": True,  "falha_critica": False, "hora": "15:10:02"},
    {"id": "r002", "ficha_id": "e5f6g7h8", "personagem": "Lyra Nocturne",   "dado": "d20", "quantidade": 1, "resultados": [1],  "modificador": 3, "total": 4,  "motivo": "Salvaguarda de Destreza",  "critico": False, "falha_critica": True,  "hora": "15:11:44"},
    {"id": "r003", "ficha_id": None,        "personagem": "Mestre",          "dado": "d6",  "quantidade": 2, "resultados": [4, 6], "modificador": 0, "total": 10, "motivo": "Dano do Goblin",         "critico": False, "falha_critica": False, "hora": "15:12:30"},
    {"id": "r004", "ficha_id": "i9j0k1l2", "personagem": "Silas Quickfinger","dado": "d20", "quantidade": 1, "resultados": [14], "modificador": 7, "total": 21, "motivo": "Furtividade",             "critico": False, "falha_critica": False, "hora": "15:14:08"},
    {"id": "r005", "ficha_id": "a1b2c3d4", "personagem": "Thorn Hollow",    "dado": "d8",  "quantidade": 1, "resultados": [6],  "modificador": 3, "total": 9,  "motivo": "Dano da espada",           "critico": False, "falha_critica": False, "hora": "15:15:22"},
]

SESSAO_COMBATE = {
    "ativa": True,
    "rodada": 2,
    "turno_atual": 1,
    "iniciativa": [
        {"nome": "Lyra Nocturne",    "iniciativa": 18, "tipo": "jogador", "hp": 18, "hp_max": 18},
        {"nome": "Thorn Hollow",     "iniciativa": 14, "tipo": "jogador", "hp": 19, "hp_max": 28},
        {"nome": "Goblin",           "iniciativa": 12, "tipo": "monstro", "hp": 4,  "hp_max": 7},
        {"nome": "Silas Quickfinger","iniciativa": 9,  "tipo": "jogador", "hp": 11, "hp_max": 16},
    ],
}

NOTAS = [
    {
        "id": "n01",
        "titulo": "A masmorra de Greenpath",
        "conteudo": "Os jogadores encontraram um altar antigo. Próxima sessão: boss do guardião.",
        "categoria": "campanha",
        "criado_em": "12/05/2026 20:00",
    },
]


# ── seed_store ────────────────────────────────────────────────────────────────

def seed_store():
    """Retorna o estado inicial mutável lido do mock_config.ini (ou fallback hardcoded)."""
    cfg = _load_config()

    # fichas: config-driven se houver seções [Personagem.X]
    fichas_cfg = _fichas_do_config(cfg)
    fichas     = fichas_cfg if fichas_cfg else {}

    # inventários: usa hardcoded se o ficha_id existir; caso contrário, vazio
    inventarios = {}
    magias_conhecidas = {}
    for fid in fichas:
        inventarios[fid]       = copy.deepcopy(INVENTARIOS.get(fid, []))
        magias_conhecidas[fid] = copy.deepcopy(MAGIAS_CONHECIDAS_PADRAO.get(fid, []))

    combate = _combate_do_config(cfg, fichas)
    campanhas = _campanhas_do_config(cfg)

    return {
        "usuarios":          copy.deepcopy(USUARIOS),
        "campanhas":         campanhas,
        "fichas":            fichas,
        "inventarios":       inventarios,
        "magias_conhecidas": magias_conhecidas,
        "log_dados":         copy.deepcopy(LOG_DADOS),
        "sessao_combate":    combate,
        "notas":             copy.deepcopy(NOTAS),
        "itens_catalogo":    copy.deepcopy(ITENS_CATALOGO),
        "magias_catalogo":   copy.deepcopy(MAGIAS_CATALOGO),
        "monstros_catalogo": copy.deepcopy(MONSTROS_CATALOGO),
    }
