"""Cliente em memória — mesma interface de gui.client, usando gui.mock_data."""

import copy
import random
import uuid
from datetime import datetime

from gui import mock_data

_store = mock_data.seed_store()


def _sync_status_vida(ficha):
    hp = ficha.get("hp_atual", 0)
    hp_max = ficha.get("hp_max", 1)
    status = ficha.setdefault("status", {})
    status["vida"] = {"atual": hp, "maximo": hp_max, "variacao": status.get("vida", {}).get("variacao")}


# AUTH
def login(usuario, senha):
    u = _store["usuarios"].get(usuario)
    if not u or u["senha"] != senha:
        return {"erro": "Usuário ou senha inválidos"}
    return {"ok": True, "usuario": {k: v for k, v in u.items() if k != "senha"}}


def vincular_ficha(usuario_id, ficha_id):
    u = _store["usuarios"].get(usuario_id)
    if not u:
        return {"erro": "Usuário não encontrado"}
    u["ficha_id"] = ficha_id
    return {k: v for k, v in u.items() if k != "senha"}


# CAMPANHAS
def listar_campanhas_usuario(usuario_id):
    resultado = []
    for c in _store["campanhas"].values():
        for m in c["membros"]:
            if m["usuario_id"] == usuario_id:
                camp = copy.deepcopy(c)
                camp["minha_role"] = m["role"]
                camp["minha_ficha_id"] = m.get("ficha_id")
                resultado.append(camp)
                break
    return resultado


# FICHAS
def listar_fichas():
    return list(_store["fichas"].values())


def buscar_ficha(ficha_id):
    f = _store["fichas"].get(ficha_id)
    if not f:
        return {"erro": "Ficha não encontrada"}
    return copy.deepcopy(f)


def criar_ficha(dados):
    ficha_id = str(uuid.uuid4())[:8]
    atributos = dados["atributos"]
    mods = {k: (v - 10) // 2 for k, v in atributos.items()}
    hp_base = {
        "Guerreiro": 10, "Paladino": 10, "Ranger": 10,
        "Mago": 6, "Feiticeiro": 6,
        "Clérigo": 8, "Druida": 8, "Ladino": 8, "Bardo": 8,
        "Bárbaro": 12, "Monge": 8, "Bruxo": 8,
    }.get(dados["classe"], 8)
    hp_max = max(1, hp_base + mods.get("constituicao", 0))
    tem_magia = dados["classe"] in [
        "Mago", "Clérigo", "Druida", "Bardo", "Feiticeiro", "Bruxo", "Paladino", "Ranger",
    ]
    sangue_max  = max(3, hp_max // 5)
    sanidade_max = max(8, 10 + mods.get("sabedoria", 0))
    vigor_max    = max(2, 2 + mods.get("constituicao", 0))
    status_base = {
        "vida":     {"atual": hp_max,      "maximo": hp_max},
        "sangue":   {"atual": sangue_max,  "maximo": sangue_max},
        "sanidade": {"atual": sanidade_max,"maximo": sanidade_max},
        "vigor":    {"atual": vigor_max,   "maximo": vigor_max},
    }
    if tem_magia:
        mana_max = max(4, 4 + mods.get("inteligencia", 0) + mods.get("sabedoria", 0))
        status_base["mana"] = {"atual": mana_max, "maximo": mana_max}
    if dados["classe"] == "Monge":
        ki_max = max(2, 2 + mods.get("sabedoria", 0))
        status_base["ki"] = {"atual": ki_max, "maximo": ki_max}
    if dados["classe"] in ["Mago", "Feiticeiro", "Bruxo"]:
        arcana_max = max(2, 2 + mods.get("inteligencia", 0))
        status_base["arcana"] = {"atual": arcana_max, "maximo": arcana_max}
    ficha = {
        "id": ficha_id,
        "nome": dados["nome"],
        "raca": dados["raca"],
        "classe": dados["classe"],
        "background": dados["background"],
        "alinhamento": dados["alinhamento"],
        "historia": dados.get("historia", ""),
        "nivel": 1,
        "xp": 0,
        "xp_proximo": 300,
        "atributos": atributos,
        "modificadores": mods,
        "hp_max": hp_max,
        "hp_atual": hp_max,
        "ca": 10 + mods.get("destreza", 0),
        "bonus_proficiencia": 2,
        "iniciativa": mods.get("destreza", 0),
        "movimento": 9,
        "tem_magia": tem_magia,
        "slots_magia": {1: 2, 2: 0, 3: 0, 4: 0, 5: 0} if tem_magia else {},
        "slots_usados": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} if tem_magia else {},
        "condicoes": [],
        "criado_em": datetime.now().isoformat(),
        "status": status_base,
    }
    _store["fichas"][ficha_id] = ficha
    _store["inventarios"][ficha_id] = []
    _store["magias_conhecidas"][ficha_id] = []
    return copy.deepcopy(ficha)


def atualizar_hp(ficha_id, hp_atual):
    f = _store["fichas"].get(ficha_id)
    if not f:
        return {"erro": "Ficha não encontrada"}
    f["hp_atual"] = max(0, min(hp_atual, f["hp_max"]))
    _sync_status_vida(f)
    return copy.deepcopy(f)


def deletar_ficha(ficha_id):
    if ficha_id not in _store["fichas"]:
        return {"erro": "Ficha não encontrada"}
    del _store["fichas"][ficha_id]
    _store["inventarios"].pop(ficha_id, None)
    _store["magias_conhecidas"].pop(ficha_id, None)
    return {"ok": True}


def adicionar_condicao(ficha_id, condicao):
    f = _store["fichas"].get(ficha_id)
    if not f:
        return {"erro": "Ficha não encontrada"}
    if condicao not in f["condicoes"]:
        f["condicoes"].append(condicao)
    return copy.deepcopy(f)


def remover_condicao(ficha_id, condicao):
    f = _store["fichas"].get(ficha_id)
    if not f:
        return {"erro": "Ficha não encontrada"}
    f["condicoes"] = [c for c in f["condicoes"] if c != condicao]
    return copy.deepcopy(f)


def descanso(ficha_id, tipo):
    f = _store["fichas"].get(ficha_id)
    if not f:
        return {"erro": "Ficha não encontrada"}
    if tipo == "curto":
        recuperado = max(1, random.randint(1, 8) + f["modificadores"].get("constituicao", 0))
        f["hp_atual"] = min(f["hp_max"], f["hp_atual"] + recuperado)
        _sync_status_vida(f)
        return {"tipo": "curto", "hp_recuperado": recuperado, "hp_atual": f["hp_atual"]}
    if tipo == "longo":
        f["hp_atual"] = f["hp_max"]
        f["slots_usados"] = {k: 0 for k in f.get("slots_usados", {})}
        f["condicoes"] = []
        _sync_status_vida(f)
        return {"tipo": "longo", "hp_atual": f["hp_atual"], "msg": "HP e recursos totalmente restaurados"}
    return {"erro": "Tipo de descanso inválido"}


# INVENTÁRIO
def listar_inventario(ficha_id):
    return _store["inventarios"].get(ficha_id, [])


def adicionar_item(ficha_id, nome, quantidade, descricao="", tipo="item"):
    if ficha_id not in _store["inventarios"]:
        return {"erro": "Ficha não encontrada"}
    novo = {"id": str(uuid.uuid4())[:8], "nome": nome, "quantidade": quantidade, "descricao": descricao, "tipo": tipo}
    _store["inventarios"][ficha_id].append(novo)
    return novo


def remover_item(ficha_id, item_id):
    inv = _store["inventarios"].get(ficha_id, [])
    _store["inventarios"][ficha_id] = [i for i in inv if i["id"] != item_id]
    return {"ok": True}


# MAGIAS
def listar_magias_ficha(ficha_id):
    return _store["magias_conhecidas"].get(ficha_id, [])


def aprender_magia(ficha_id, magia_id):
    magia = next((m for m in _store["magias_catalogo"] if m["id"] == magia_id), None)
    if not magia:
        return {"erro": "Magia não encontrada"}
    conhecidas = _store["magias_conhecidas"].setdefault(ficha_id, [])
    if not any(m["id"] == magia_id for m in conhecidas):
        conhecidas.append(copy.deepcopy(magia))
    return magia


def esquecer_magia(ficha_id, magia_id):
    conhecidas = _store["magias_conhecidas"].get(ficha_id, [])
    _store["magias_conhecidas"][ficha_id] = [m for m in conhecidas if m["id"] != magia_id]
    return {"ok": True}


def usar_slot(ficha_id, nivel):
    f = _store["fichas"].get(ficha_id)
    if not f:
        return {"erro": "Ficha não encontrada"}
    slots = f["slots_magia"].get(nivel, 0)
    usados = f["slots_usados"].get(nivel, 0)
    if usados >= slots:
        return {"erro": "Sem slots disponíveis neste nível"}
    f["slots_usados"][nivel] = usados + 1
    return copy.deepcopy(f)


# CATÁLOGOS
def catalogo_itens():
    return _store["itens_catalogo"]


def catalogo_magias():
    return _store["magias_catalogo"]


def catalogo_monstros():
    return _store["monstros_catalogo"]


# DADOS
def rolar_dados(dado, quantidade, modificador, ficha_id=None, personagem="Anônimo", motivo=""):
    lados = int(dado[1:])
    resultados = [random.randint(1, lados) for _ in range(quantidade)]
    total = sum(resultados) + modificador
    critico = dado == "d20" and resultados[0] == 20
    falha = dado == "d20" and resultados[0] == 1
    entrada = {
        "id": str(uuid.uuid4())[:8],
        "ficha_id": ficha_id,
        "personagem": personagem,
        "dado": dado,
        "quantidade": quantidade,
        "resultados": resultados,
        "modificador": modificador,
        "total": total,
        "motivo": motivo,
        "critico": critico,
        "falha_critica": falha,
        "hora": datetime.now().strftime("%H:%M:%S"),
    }
    _store["log_dados"].append(entrada)
    if len(_store["log_dados"]) > 100:
        _store["log_dados"] = _store["log_dados"][-100:]
    return entrada


def log_dados():
    return list(reversed(_store["log_dados"][-30:]))


def limpar_log():
    _store["log_dados"] = []
    return {"ok": True}


# COMBATE
def estado_combate():
    return copy.deepcopy(_store["sessao_combate"])


def iniciar_combate(participantes):
    ordenados = sorted(participantes, key=lambda x: x["iniciativa"], reverse=True)
    _store["sessao_combate"] = {
        "ativa": True,
        "rodada": 1,
        "turno_atual": 0,
        "iniciativa": ordenados,
    }
    return copy.deepcopy(_store["sessao_combate"])


def proximo_turno():
    c = _store["sessao_combate"]
    if not c["ativa"]:
        return {"erro": "Nenhum combate ativo"}
    c["turno_atual"] += 1
    if c["turno_atual"] >= len(c["iniciativa"]):
        c["turno_atual"] = 0
        c["rodada"] += 1
    return copy.deepcopy(c)


def encerrar_combate():
    _store["sessao_combate"] = {"ativa": False, "rodada": 0, "turno_atual": 0, "iniciativa": []}
    return {"ok": True}


def personagem_ativo_turno():
    c = _store["sessao_combate"]
    if not c["ativa"] or not c["iniciativa"]:
        return {"ativo": None}
    idx = c["turno_atual"]
    part = c["iniciativa"][idx] if idx < len(c["iniciativa"]) else None
    return {"ativo": part, "rodada": c["rodada"], "turno": idx}


# NOTAS
def listar_notas():
    return _store["notas"]


def criar_nota(titulo, conteudo, categoria="geral"):
    nova = {
        "id": str(uuid.uuid4())[:8],
        "titulo": titulo,
        "conteudo": conteudo,
        "categoria": categoria,
        "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    _store["notas"].append(nova)
    return nova


def deletar_nota(nota_id):
    _store["notas"] = [n for n in _store["notas"] if n["id"] != nota_id]
    return {"ok": True}


# DASHBOARD
def dashboard():
    fichas = list(_store["fichas"].values())
    logs = _store["log_dados"]
    criticos = sum(1 for l in logs if l.get("critico"))
    falhas = sum(1 for l in logs if l.get("falha_critica"))
    media = round(sum(l["total"] for l in logs) / len(logs), 1) if logs else 0
    return {
        "total_fichas": len(fichas),
        "total_rolagens": len(logs),
        "criticos": criticos,
        "falhas_criticas": falhas,
        "media_rolagens": media,
        "fichas": copy.deepcopy(fichas),
        "ultimas_rolagens": list(reversed(logs[-30:])),
    }
