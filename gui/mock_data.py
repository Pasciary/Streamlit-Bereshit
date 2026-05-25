"""
Dados fictícios para validar o front sem a API (uvicorn) rodando.

Ative o modo mock em gui/client.py (USE_MOCK = True)
ou defina a variável de ambiente: RPG_USE_MOCK=1
"""

ENABLE_MOCK = True

# ── usuários ─────────────────────────────────────────────────────────────
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
        "role": "jogador",
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

# ── campanhas ──────────────────────────────────────────────────────────────
CAMPANHAS = {
    "camp01": {
        "id": "camp01",
        "nome": "A Maldição de Ironthorn",
        "descricao": "Uma maldição ancestral ameaça a cidade mineira de Ironthorn. Heróis são convocados para desvendar o mistério.",
        "criado_em": "2026-05-01",
        "membros": [
            {"usuario_id": "zeny",       "role": "mestre",  "ficha_id": None},
            {"usuario_id": "duda",       "role": "jogador", "ficha_id": None},
            {"usuario_id": "leo",        "role": "jogador", "ficha_id": None},
            {"usuario_id": "marquinhos", "role": "jogador", "ficha_id": None},
        ],
    },
    "camp02": {
        "id": "camp02",
        "nome": "Sombras de Arendel",
        "descricao": "O reino de Arendel mergulha em trevas após o desaparecimento do rei. Uma conspiração se desenrola nas sombras.",
        "criado_em": "2026-05-08",
        "membros": [
            {"usuario_id": "zeny", "role": "mestre",  "ficha_id": None},
            {"usuario_id": "duda", "role": "jogador", "ficha_id": None},
            {"usuario_id": "leo",  "role": "jogador", "ficha_id": None},
        ],
    },
    "camp03": {
        "id": "camp03",
        "nome": "O Último Oráculo",
        "descricao": "O último oráculo vivo guarda segredos que podem destruir o mundo. Forças opostas correm para encontrá-lo.",
        "criado_em": "2026-05-15",
        "membros": [
            {"usuario_id": "duda",       "role": "mestre",  "ficha_id": None},
            {"usuario_id": "zeny",       "role": "jogador", "ficha_id": None},
            {"usuario_id": "marquinhos", "role": "jogador", "ficha_id": None},
        ],
    },
    "camp04": {
        "id": "camp04",
        "nome": "Crônicas de Hallownest",
        "descricao": "A campanha original — explorando as ruínas do antigo reino de Hallownest e seus segredos enterrados.",
        "criado_em": "2026-04-15",
        "membros": [
            {"usuario_id": "mestre",   "role": "mestre",  "ficha_id": None},
            {"usuario_id": "jogador1", "role": "jogador", "ficha_id": "a1b2c3d4"},
            {"usuario_id": "jogador2", "role": "jogador", "ficha_id": "e5f6g7h8"},
        ],
    },
}

# ── catálogos ────────────────────────────────────────────────────────────
ITENS_CATALOGO = [
    {"id": "1", "nome": "Espada Longa", "tipo": "arma", "dano": "1d8", "preco": 15, "peso": 3, "descricao": "Arma versátil de uma ou duas mãos"},
    {"id": "2", "nome": "Arco Curto", "tipo": "arma", "dano": "1d6", "preco": 25, "peso": 2, "descricao": "Arco para ataques à distância"},
    {"id": "3", "nome": "Armadura de Couro", "tipo": "armadura", "ca": 11, "preco": 10, "peso": 10, "descricao": "Proteção leve e silenciosa"},
    {"id": "4", "nome": "Cota de Malha", "tipo": "armadura", "ca": 16, "preco": 75, "peso": 55, "descricao": "Armadura média resistente"},
    {"id": "5", "nome": "Poção de Cura", "tipo": "consumivel", "efeito": "2d4+2 HP", "preco": 50, "peso": 0.5, "descricao": "Restaura pontos de vida"},
    {"id": "6", "nome": "Tocha", "tipo": "equipamento", "preco": 1, "peso": 1, "descricao": "Ilumina 6m por 1 hora"},
    {"id": "7", "nome": "Corda (15m)", "tipo": "equipamento", "preco": 1, "peso": 10, "descricao": "Corda resistente de cânhamo"},
    {"id": "8", "nome": "Grimório", "tipo": "equipamento", "preco": 50, "peso": 3, "descricao": "Livro de magias do mago"},
]

MAGIAS_CATALOGO = [
    {"id": "1", "nome": "Míssil Mágico", "nivel": 1, "escola": "Evocação", "alcance": "18m", "componentes": "V, S", "duracao": "Instantâneo", "descricao": "3 dardos de força causando 1d4+1 cada"},
    {"id": "2", "nome": "Bola de Fogo", "nivel": 3, "escola": "Evocação", "alcance": "45m", "componentes": "V, S, M", "duracao": "Instantâneo", "descricao": "Explosão de 8d6 de dano de fogo em raio de 6m"},
    {"id": "3", "nome": "Curar Ferimentos", "nivel": 1, "escola": "Evocação", "alcance": "Toque", "componentes": "V, S", "duracao": "Instantâneo", "descricao": "Restaura 1d8 + mod Sabedoria de HP"},
    {"id": "4", "nome": "Escudo", "nivel": 1, "escola": "Abjuração", "alcance": "Pessoal", "componentes": "V, S", "duracao": "1 rodada", "descricao": "+5 CA como reação"},
    {"id": "5", "nome": "Sono", "nivel": 1, "escola": "Encantamento", "alcance": "27m", "componentes": "V, S, M", "duracao": "1 minuto", "descricao": "Adormece criaturas com até 5d8 HP"},
    {"id": "6", "nome": "Luz", "nivel": 0, "escola": "Evocação", "alcance": "Toque", "componentes": "V, M", "duracao": "1 hora", "descricao": "Objeto emite luz por 6m"},
    {"id": "7", "nome": "Prestidigitação", "nivel": 0, "escola": "Transmutação", "alcance": "3m", "componentes": "V, S", "duracao": "Até 1 hora", "descricao": "Efeitos mágicos menores variados"},
]

MONSTROS_CATALOGO = [
    {"id": "1", "nome": "Goblin", "hp": 7, "ca": 15, "ataque": "+4", "dano": "1d6+2", "cr": "1/4", "xp": 50},
    {"id": "2", "nome": "Orc", "hp": 15, "ca": 13, "ataque": "+5", "dano": "1d12+3", "cr": "1/2", "xp": 100},
    {"id": "3", "nome": "Esqueleto", "hp": 13, "ca": 13, "ataque": "+4", "dano": "1d6+2", "cr": "1/4", "xp": 50},
    {"id": "4", "nome": "Zumbi", "hp": 22, "ca": 8, "ataque": "+3", "dano": "1d6+1", "cr": "1/4", "xp": 50},
    {"id": "5", "nome": "Lobo", "hp": 11, "ca": 13, "ataque": "+4", "dano": "2d4+2", "cr": "1/4", "xp": 50},
    {"id": "6", "nome": "Dragão Jovem", "hp": 178, "ca": 18, "ataque": "+10", "dano": "2d10+6", "cr": "10", "xp": 5900},
]

# ── fichas ─────────────────────────────────────────────────────────────
FICHA_GUERREIRO = {
    "id": "a1b2c3d4",
    "nome": "Thorn Hollow",
    "raca": "Humano",
    "classe": "Guerreiro",
    "background": "Soldado",
    "alinhamento": "Leal e Bom",
    "historia": "Veterano das guerras do reino. Busca redenção após a queda de Hallownest.",
    "nivel": 3,
    "xp": 900,
    "xp_proximo": 2700,
    "atributos": {
        "forca": 16, "destreza": 12, "constituicao": 15,
        "inteligencia": 10, "sabedoria": 11, "carisma": 9,
    },
    "modificadores": {"forca": 3, "destreza": 1, "constituicao": 2, "inteligencia": 0, "sabedoria": 0, "carisma": -1},
    "hp_max": 28,
    "hp_atual": 19,
    "ca": 17,
    "bonus_proficiencia": 2,
    "iniciativa": 1,
    "movimento": 9,
    "tem_magia": False,
    "slots_magia": {},
    "slots_usados": {},
    "condicoes": ["Envenenado"],
    "criado_em": "2026-05-10T14:22:00",
    "status": {
        "vida": {"atual": 19, "maximo": 28, "variacao": -4},
        "sanidade": {"atual": 14, "maximo": 16},
        "sangue": {"atual": 3, "maximo": 5},
        "vigor": {"atual": 2, "maximo": 4},
    },
}

FICHA_MAGO = {
    "id": "e5f6g7h8",
    "nome": "Lyra Nocturne",
    "raca": "Elfo",
    "classe": "Mago",
    "background": "Sábio",
    "alinhamento": "Neutro e Bom",
    "historia": "Estudiosa do grimório ancestral. Especialista em evocação e abjuração.",
    "nivel": 3,
    "xp": 850,
    "xp_proximo": 2700,
    "atributos": {
        "forca": 8, "destreza": 14, "constituicao": 12,
        "inteligencia": 17, "sabedoria": 13, "carisma": 11,
    },
    "modificadores": {"forca": -1, "destreza": 2, "constituicao": 1, "inteligencia": 3, "sabedoria": 1, "carisma": 0},
    "hp_max": 18,
    "hp_atual": 18,
    "ca": 14,
    "bonus_proficiencia": 2,
    "iniciativa": 2,
    "movimento": 9,
    "tem_magia": True,
    "slots_magia": {1: 4, 2: 2, 3: 0, 4: 0, 5: 0},
    "slots_usados": {1: 1, 2: 0, 3: 0, 4: 0, 5: 0},
    "condicoes": [],
    "criado_em": "2026-05-12T09:15:00",
    "status": {
        "vida": {"atual": 18, "maximo": 18},
        "sanidade": {"atual": 20, "maximo": 20},
        "mana": {"atual": 5, "maximo": 8, "variacao": -1},
        "arcana": {"atual": 2, "maximo": 3},
    },
}

FICHA_LADINO = {
    "id": "i9j0k1l2",
    "nome": "Silas Quickfinger",
    "raca": "Halfling",
    "classe": "Ladino",
    "background": "Criminoso",
    "alinhamento": "Caótico e Neutro",
    "historia": "Ladrão de guilda que virou aventureiro por uma dívida com o mestre.",
    "nivel": 2,
    "xp": 450,
    "xp_proximo": 900,
    "atributos": {
        "forca": 10, "destreza": 17, "constituicao": 12,
        "inteligencia": 12, "sabedoria": 10, "carisma": 14,
    },
    "modificadores": {"forca": 0, "destreza": 3, "constituicao": 1, "inteligencia": 1, "sabedoria": 0, "carisma": 2},
    "hp_max": 16,
    "hp_atual": 11,
    "ca": 15,
    "bonus_proficiencia": 2,
    "iniciativa": 3,
    "movimento": 7,
    "tem_magia": False,
    "slots_magia": {},
    "slots_usados": {},
    "condicoes": [],
    "criado_em": "2026-05-15T18:40:00",
    "status": {
        "vida": {"atual": 11, "maximo": 16},
        "vigor": {"atual": 1, "maximo": 3},
        "ki": {"atual": 0, "maximo": 2},
    },
}

INVENTARIOS = {
    "a1b2c3d4": [
        {"id": "inv01", "nome": "Espada Longa", "quantidade": 1, "descricao": "Arma principal", "tipo": "arma"},
        {"id": "inv02", "nome": "Cota de Malha", "quantidade": 1, "descricao": "Armadura equipada", "tipo": "armadura"},
        {"id": "inv03", "nome": "Poção de Cura", "quantidade": 2, "descricao": "2d4+2 HP", "tipo": "consumivel"},
    ],
    "e5f6g7h8": [
        {"id": "inv04", "nome": "Grimório", "quantidade": 1, "descricao": "Livro de magias", "tipo": "equipamento"},
        {"id": "inv05", "nome": "Componentes arcanos", "quantidade": 1, "descricao": "Bolsa de componentes", "tipo": "equipamento"},
    ],
    "i9j0k1l2": [
        {"id": "inv06", "nome": "Adaga", "quantidade": 2, "descricao": "Par de adagas", "tipo": "arma"},
        {"id": "inv07", "nome": "Ferramentas de ladrão", "quantidade": 1, "descricao": "", "tipo": "equipamento"},
    ],
}

MAGIAS_CONHECIDAS = {
    "e5f6g7h8": [
        MAGIAS_CATALOGO[0],
        MAGIAS_CATALOGO[2],
        MAGIAS_CATALOGO[3],
        MAGIAS_CATALOGO[5],
    ],
    "a1b2c3d4": [],
    "i9j0k1l2": [],
}

LOG_DADOS = [
    {
        "id": "r001", "ficha_id": "a1b2c3d4", "personagem": "Thorn Hollow",
        "dado": "d20", "quantidade": 1, "resultados": [20], "modificador": 5,
        "total": 25, "motivo": "Ataque com espada", "critico": True, "falha_critica": False,
        "hora": "15:10:02",
    },
    {
        "id": "r002", "ficha_id": "e5f6g7h8", "personagem": "Lyra Nocturne",
        "dado": "d20", "quantidade": 1, "resultados": [1], "modificador": 3,
        "total": 4, "motivo": "Salvaguarda de Destreza", "critico": False, "falha_critica": True,
        "hora": "15:11:44",
    },
    {
        "id": "r003", "ficha_id": None, "personagem": "Mestre",
        "dado": "d6", "quantidade": 2, "resultados": [4, 6], "modificador": 0,
        "total": 10, "motivo": "Dano do Goblin", "critico": False, "falha_critica": False,
        "hora": "15:12:30",
    },
    {
        "id": "r004", "ficha_id": "i9j0k1l2", "personagem": "Silas Quickfinger",
        "dado": "d20", "quantidade": 1, "resultados": [14], "modificador": 7,
        "total": 21, "motivo": "Furtividade", "critico": False, "falha_critica": False,
        "hora": "15:14:08",
    },
    {
        "id": "r005", "ficha_id": "a1b2c3d4", "personagem": "Thorn Hollow",
        "dado": "d8", "quantidade": 1, "resultados": [6], "modificador": 3,
        "total": 9, "motivo": "Dano da espada", "critico": False, "falha_critica": False,
        "hora": "15:15:22",
    },
]

SESSAO_COMBATE = {
    "ativa": True,
    "rodada": 2,
    "turno_atual": 1,
    "iniciativa": [
        {"nome": "Lyra Nocturne", "iniciativa": 18, "tipo": "jogador", "hp": 18, "hp_max": 18},
        {"nome": "Thorn Hollow", "iniciativa": 14, "tipo": "jogador", "hp": 19, "hp_max": 28},
        {"nome": "Goblin", "iniciativa": 12, "tipo": "monstro", "hp": 4, "hp_max": 7},
        {"nome": "Silas Quickfinger", "iniciativa": 9, "tipo": "jogador", "hp": 11, "hp_max": 16},
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

def seed_store():
    """Retorna uma cópia mutável do estado inicial (espelha o db do main.py)."""
    import copy
    return {
        "usuarios": copy.deepcopy(USUARIOS),
        "campanhas": copy.deepcopy(CAMPANHAS),
        "fichas": {
            FICHA_GUERREIRO["id"]: copy.deepcopy(FICHA_GUERREIRO),
            FICHA_MAGO["id"]: copy.deepcopy(FICHA_MAGO),
            FICHA_LADINO["id"]: copy.deepcopy(FICHA_LADINO),
        },
        "inventarios": copy.deepcopy(INVENTARIOS),
        "magias_conhecidas": copy.deepcopy(MAGIAS_CONHECIDAS),
        "log_dados": copy.deepcopy(LOG_DADOS),
        "sessao_combate": copy.deepcopy(SESSAO_COMBATE),
        "notas": copy.deepcopy(NOTAS),
        "itens_catalogo": copy.deepcopy(ITENS_CATALOGO),
        "magias_catalogo": copy.deepcopy(MAGIAS_CATALOGO),
        "monstros_catalogo": copy.deepcopy(MONSTROS_CATALOGO),
    }
