from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import random
import uuid
from datetime import datetime

app = FastAPI(title="Bereshit RPG API", version="1.0.0")

db = {
    "usuarios": {
        "mestre":   {"id": "mestre",   "nome": "Mestre",   "senha": "1234", "role": "mestre",  "ficha_id": None},
        "jogador1": {"id": "jogador1", "nome": "Jogador 1","senha": "1234", "role": "jogador", "ficha_id": None},
        "jogador2": {"id": "jogador2", "nome": "Jogador 2","senha": "1234", "role": "jogador", "ficha_id": None},
    },
    "personagem_ativo_turno": None,
    "fichas": {},
    "inventarios": {},
    "magias_conhecidas": {},
    "log_dados": [],
    "sessao_combate": {"ativa": False, "rodada": 0, "turno_atual": 0, "iniciativa": []},
    "notas": [],
    "itens_catalogo": [
        {"id": "1", "nome": "Espada Longa", "tipo": "arma", "dano": "1d8", "preco": 15, "peso": 3, "descricao": "Arma versátil de uma ou duas mãos"},
        {"id": "2", "nome": "Arco Curto", "tipo": "arma", "dano": "1d6", "preco": 25, "peso": 2, "descricao": "Arco para ataques à distância"},
        {"id": "3", "nome": "Armadura de Couro", "tipo": "armadura", "ca": 11, "preco": 10, "peso": 10, "descricao": "Proteção leve e silenciosa"},
        {"id": "4", "nome": "Cota de Malha", "tipo": "armadura", "ca": 16, "preco": 75, "peso": 55, "descricao": "Armadura média resistente"},
        {"id": "5", "nome": "Poção de Cura", "tipo": "consumivel", "efeito": "2d4+2 HP", "preco": 50, "peso": 0.5, "descricao": "Restaura pontos de vida"},
        {"id": "6", "nome": "Tocha", "tipo": "equipamento", "preco": 1, "peso": 1, "descricao": "Ilumina 6m por 1 hora"},
        {"id": "7", "nome": "Corda (15m)", "tipo": "equipamento", "preco": 1, "peso": 10, "descricao": "Corda resistente de cânhamo"},
        {"id": "8", "nome": "Grimório", "tipo": "equipamento", "preco": 50, "peso": 3, "descricao": "Livro de magias do mago"},
    ],
    "magias_catalogo": [
        {"id": "1", "nome": "Míssil Mágico", "nivel": 1, "escola": "Evocação", "alcance": "18m", "componentes": "V, S", "duracao": "Instantâneo", "descricao": "3 dardos de força causando 1d4+1 cada"},
        {"id": "2", "nome": "Bola de Fogo", "nivel": 3, "escola": "Evocação", "alcance": "45m", "componentes": "V, S, M", "duracao": "Instantâneo", "descricao": "Explosão de 8d6 de dano de fogo em raio de 6m"},
        {"id": "3", "nome": "Curar Ferimentos", "nivel": 1, "escola": "Evocação", "alcance": "Toque", "componentes": "V, S", "duracao": "Instantâneo", "descricao": "Restaura 1d8 + mod Sabedoria de HP"},
        {"id": "4", "nome": "Escudo", "nivel": 1, "escola": "Abjuração", "alcance": "Pessoal", "componentes": "V, S", "duracao": "1 rodada", "descricao": "+5 CA como reação"},
        {"id": "5", "nome": "Sono", "nivel": 1, "escola": "Encantamento", "alcance": "27m", "componentes": "V, S, M", "duracao": "1 minuto", "descricao": "Adormece criaturas com até 5d8 HP"},
        {"id": "6", "nome": "Luz", "nivel": 0, "escola": "Evocação", "alcance": "Toque", "componentes": "V, M", "duracao": "1 hora", "descricao": "Objeto emite luz por 6m"},
        {"id": "7", "nome": "Prestidigitação", "nivel": 0, "escola": "Transmutação", "alcance": "3m", "componentes": "V, S", "duracao": "Até 1 hora", "descricao": "Efeitos mágicos menores variados"},
    ],
    "monstros_catalogo": [
        {"id": "1", "nome": "Goblin", "hp": 7, "ca": 15, "ataque": "+4", "dano": "1d6+2", "cr": "1/4", "xp": 50},
        {"id": "2", "nome": "Orc", "hp": 15, "ca": 13, "ataque": "+5", "dano": "1d12+3", "cr": "1/2", "xp": 100},
        {"id": "3", "nome": "Esqueleto", "hp": 13, "ca": 13, "ataque": "+4", "dano": "1d6+2", "cr": "1/4", "xp": 50},
        {"id": "4", "nome": "Zumbi", "hp": 22, "ca": 8, "ataque": "+3", "dano": "1d6+1", "cr": "1/4", "xp": 50},
        {"id": "5", "nome": "Lobo", "hp": 11, "ca": 13, "ataque": "+4", "dano": "2d4+2", "cr": "1/4", "xp": 50},
        {"id": "6", "nome": "Dragão Jovem", "hp": 178, "ca": 18, "ataque": "+10", "dano": "2d10+6", "cr": "10", "xp": 5900},
    ]
}


class LoginInput(BaseModel):
    usuario: str
    senha: str

class FichaInput(BaseModel):
    nome: str
    raca: str
    classe: str
    background: str
    alinhamento: str
    historia: Optional[str] = ""
    atributos: dict

class ItemInventarioInput(BaseModel):
    nome: str
    quantidade: int = 1
    descricao: Optional[str] = ""
    tipo: Optional[str] = "item"

class RolagemInput(BaseModel):
    ficha_id: Optional[str] = None
    personagem: Optional[str] = "Anônimo"
    dado: str
    quantidade: int = 1
    modificador: int = 0
    motivo: Optional[str] = ""

class IniciativaInput(BaseModel):
    participantes: list

class NotaInput(BaseModel):
    titulo: str
    conteudo: str
    categoria: str = "geral"

class HPUpdateInput(BaseModel):
    hp_atual: int

class CondicaoInput(BaseModel):
    condicao: str


@app.post("/auth/login")
def login(dados: LoginInput):
    usuario = db["usuarios"].get(dados.usuario)
    if not usuario or usuario["senha"] != dados.senha:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    return {"ok": True, "usuario": usuario}

@app.get("/auth/usuarios")
def listar_usuarios():
    return list(db["usuarios"].values())

@app.get("/combate/ativo")
def personagem_ativo():
    combate = db["sessao_combate"]
    if not combate["ativa"] or not combate["iniciativa"]:
        return {"ativo": None}
    idx = combate["turno_atual"]
    part = combate["iniciativa"][idx] if idx < len(combate["iniciativa"]) else None
    return {"ativo": part, "rodada": combate["rodada"], "turno": idx}

@app.post("/auth/vincular-ficha")
def vincular_ficha(usuario_id: str, ficha_id: str):
    usuario = db["usuarios"].get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario["ficha_id"] = ficha_id
    return usuario

@app.get("/fichas")
def listar_fichas():
    return list(db["fichas"].values())

@app.get("/fichas/{ficha_id}")
def buscar_ficha(ficha_id: str):
    ficha = db["fichas"].get(ficha_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    return ficha

@app.post("/fichas", status_code=201)
def criar_ficha(dados: FichaInput):
    ficha_id = str(uuid.uuid4())[:8]
    atributos = dados.atributos
    mods = {k: (v - 10) // 2 for k, v in atributos.items()}
    hp_base = {
        "Guerreiro": 10, "Paladino": 10, "Ranger": 10,
        "Mago": 6, "Feiticeiro": 6,
        "Clérigo": 8, "Druida": 8, "Ladino": 8, "Bardo": 8,
        "Bárbaro": 12, "Monge": 8, "Bruxo": 8
    }.get(dados.classe, 8)
    hp_max = hp_base + mods.get("constituicao", 0)
    tem_magia = dados.classe in ["Mago", "Clérigo", "Druida", "Bardo", "Feiticeiro", "Bruxo", "Paladino", "Ranger"]
    ficha = {
        "id": ficha_id, "nome": dados.nome, "raca": dados.raca, "classe": dados.classe,
        "background": dados.background, "alinhamento": dados.alinhamento, "historia": dados.historia,
        "nivel": 1, "xp": 0, "xp_proximo": 300, "atributos": atributos, "modificadores": mods,
        "hp_max": max(1, hp_max), "hp_atual": max(1, hp_max),
        "ca": 10 + mods.get("destreza", 0), "bonus_proficiencia": 2,
        "iniciativa": mods.get("destreza", 0), "movimento": 9,
        "tem_magia": tem_magia,
        "slots_magia": {1: 2, 2: 0, 3: 0, 4: 0, 5: 0} if tem_magia else {},
        "slots_usados": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} if tem_magia else {},
        "condicoes": [], "criado_em": datetime.now().isoformat(),
        "status": {"vida": {"atual": max(1, hp_max), "maximo": max(1, hp_max)}},
    }
    db["fichas"][ficha_id] = ficha
    db["inventarios"][ficha_id] = []
    db["magias_conhecidas"][ficha_id] = []
    return ficha

@app.patch("/fichas/{ficha_id}")
def atualizar_ficha(ficha_id: str, dados: HPUpdateInput):
    ficha = db["fichas"].get(ficha_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    ficha["hp_atual"] = max(0, min(dados.hp_atual, ficha["hp_max"]))
    return ficha

@app.post("/fichas/{ficha_id}/condicao")
def adicionar_condicao(ficha_id: str, dados: CondicaoInput):
    ficha = db["fichas"].get(ficha_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    if dados.condicao not in ficha["condicoes"]:
        ficha["condicoes"].append(dados.condicao)
    return ficha

@app.delete("/fichas/{ficha_id}/condicao/{condicao}")
def remover_condicao(ficha_id: str, condicao: str):
    ficha = db["fichas"].get(ficha_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    ficha["condicoes"] = [c for c in ficha["condicoes"] if c != condicao]
    return ficha

@app.delete("/fichas/{ficha_id}")
def deletar_ficha(ficha_id: str):
    if ficha_id not in db["fichas"]:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    del db["fichas"][ficha_id]
    db["inventarios"].pop(ficha_id, None)
    db["magias_conhecidas"].pop(ficha_id, None)
    return {"ok": True}

@app.post("/fichas/{ficha_id}/descanso/{tipo}")
def descanso(ficha_id: str, tipo: str):
    ficha = db["fichas"].get(ficha_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    if tipo == "curto":
        dado = random.randint(1, 8)
        mod = ficha["modificadores"].get("constituicao", 0)
        recuperado = max(1, dado + mod)
        ficha["hp_atual"] = min(ficha["hp_max"], ficha["hp_atual"] + recuperado)
        return {"tipo": "curto", "hp_recuperado": recuperado, "hp_atual": ficha["hp_atual"]}
    elif tipo == "longo":
        ficha["hp_atual"] = ficha["hp_max"]
        ficha["slots_usados"] = {k: 0 for k in ficha["slots_usados"]}
        ficha["condicoes"] = []
        return {"tipo": "longo", "hp_atual": ficha["hp_atual"], "msg": "HP e recursos totalmente restaurados"}
    raise HTTPException(status_code=400, detail="Tipo de descanso inválido")

@app.get("/fichas/{ficha_id}/inventario")
def listar_inventario(ficha_id: str):
    return db["inventarios"].get(ficha_id, [])

@app.post("/fichas/{ficha_id}/inventario", status_code=201)
def adicionar_item(ficha_id: str, item: ItemInventarioInput):
    if ficha_id not in db["inventarios"]:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    novo = {"id": str(uuid.uuid4())[:8], **item.dict()}
    db["inventarios"][ficha_id].append(novo)
    return novo

@app.delete("/fichas/{ficha_id}/inventario/{item_id}")
def remover_item(ficha_id: str, item_id: str):
    db["inventarios"][ficha_id] = [i for i in db["inventarios"].get(ficha_id, []) if i["id"] != item_id]
    return {"ok": True}

@app.get("/fichas/{ficha_id}/magias")
def listar_magias_ficha(ficha_id: str):
    return db["magias_conhecidas"].get(ficha_id, [])

@app.post("/fichas/{ficha_id}/magias/{magia_id}")
def aprender_magia(ficha_id: str, magia_id: str):
    magia = next((m for m in db["magias_catalogo"] if m["id"] == magia_id), None)
    if not magia:
        raise HTTPException(status_code=404, detail="Magia não encontrada")
    conhecidas = db["magias_conhecidas"].get(ficha_id, [])
    if not any(m["id"] == magia_id for m in conhecidas):
        conhecidas.append(magia)
        db["magias_conhecidas"][ficha_id] = conhecidas
    return magia

@app.delete("/fichas/{ficha_id}/magias/{magia_id}")
def esquecer_magia(ficha_id: str, magia_id: str):
    db["magias_conhecidas"][ficha_id] = [m for m in db["magias_conhecidas"].get(ficha_id, []) if m["id"] != magia_id]
    return {"ok": True}

@app.post("/fichas/{ficha_id}/slots/{nivel}/usar")
def usar_slot(ficha_id: str, nivel: int):
    ficha = db["fichas"].get(ficha_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    slots = ficha["slots_magia"].get(nivel, 0)
    usados = ficha["slots_usados"].get(nivel, 0)
    if usados >= slots:
        raise HTTPException(status_code=400, detail="Sem slots disponíveis neste nível")
    ficha["slots_usados"][nivel] = usados + 1
    return ficha

@app.get("/catalogo/itens")
def catalogo_itens():
    return db["itens_catalogo"]

@app.get("/catalogo/magias")
def catalogo_magias():
    return db["magias_catalogo"]

@app.get("/catalogo/monstros")
def catalogo_monstros():
    return db["monstros_catalogo"]

@app.post("/dados/rolar")
def rolar_dados(dados: RolagemInput):
    lados = int(dados.dado[1:])
    resultados = [random.randint(1, lados) for _ in range(dados.quantidade)]
    total = sum(resultados) + dados.modificador
    critico = dados.dado == "d20" and resultados[0] == 20
    falha   = dados.dado == "d20" and resultados[0] == 1
    entrada = {
        "id": str(uuid.uuid4())[:8], "ficha_id": dados.ficha_id, "personagem": dados.personagem,
        "dado": dados.dado, "quantidade": dados.quantidade, "resultados": resultados,
        "modificador": dados.modificador, "total": total, "motivo": dados.motivo,
        "critico": critico, "falha_critica": falha, "hora": datetime.now().strftime("%H:%M:%S"),
    }
    db["log_dados"].append(entrada)
    if len(db["log_dados"]) > 100:
        db["log_dados"] = db["log_dados"][-100:]
    return entrada

@app.get("/dados/log")
def log_dados():
    return list(reversed(db["log_dados"][-30:]))

@app.delete("/dados/log")
def limpar_log():
    db["log_dados"] = []
    return {"ok": True}

@app.get("/combate")
def estado_combate():
    return db["sessao_combate"]

@app.post("/combate/iniciar")
def iniciar_combate(dados: IniciativaInput):
    ordenados = sorted(dados.participantes, key=lambda x: x["iniciativa"], reverse=True)
    db["sessao_combate"] = {"ativa": True, "rodada": 1, "turno_atual": 0, "iniciativa": ordenados}
    return db["sessao_combate"]

@app.post("/combate/proximo")
def proximo_turno():
    combate = db["sessao_combate"]
    if not combate["ativa"]:
        raise HTTPException(status_code=400, detail="Nenhum combate ativo")
    combate["turno_atual"] += 1
    if combate["turno_atual"] >= len(combate["iniciativa"]):
        combate["turno_atual"] = 0
        combate["rodada"] += 1
    return combate

@app.post("/combate/encerrar")
def encerrar_combate():
    db["sessao_combate"] = {"ativa": False, "rodada": 0, "turno_atual": 0, "iniciativa": []}
    return {"ok": True}

@app.get("/notas")
def listar_notas():
    return db["notas"]

@app.post("/notas", status_code=201)
def criar_nota(nota: NotaInput):
    nova = {
        "id": str(uuid.uuid4())[:8], "titulo": nota.titulo, "conteudo": nota.conteudo,
        "categoria": nota.categoria, "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    db["notas"].append(nova)
    return nova

@app.delete("/notas/{nota_id}")
def deletar_nota(nota_id: str):
    db["notas"] = [n for n in db["notas"] if n["id"] != nota_id]
    return {"ok": True}

@app.get("/dashboard")
def dashboard():
    fichas = list(db["fichas"].values())
    logs   = db["log_dados"]
    criticos  = sum(1 for l in logs if l.get("critico"))
    falhas    = sum(1 for l in logs if l.get("falha_critica"))
    media     = round(sum(l["total"] for l in logs) / len(logs), 1) if logs else 0
    return {
        "total_fichas": len(fichas), "total_rolagens": len(logs),
        "criticos": criticos, "falhas_criticas": falhas, "media_rolagens": media,
        "fichas": fichas, "ultimas_rolagens": list(reversed(logs[-5:])),
    }
