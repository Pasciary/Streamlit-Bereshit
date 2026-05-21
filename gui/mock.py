USUARIOS = {
    "mestre": {"senha": "01234", "role": "mestre"},
    "jogador1": {"senha": "1234", "role": "jogador"},
    "jogador2": {"senha": "1234", "role": "jogador"},
}

_FICHAS = [
    {
        "id": 1,
        "nome": "Aldric Ferrovenas",
        "jogador": "jogador1",
        "classe": "Guerreiro",
        "raca": "Humano",
        "nivel": 5,
        "hp_atual": 45,
        "hp_max": 52,
        "mp_atual": 10,
        "mp_max": 10,
        "atributos": {
            "forca": 16,
            "destreza": 12,
            "constituicao": 14,
            "inteligencia": 10,
            "sabedoria": 8,
            "carisma": 11,
        },
        "historia": "Nascido em uma família de ferreiros, Aldric descobriu seu talento para o combate após defender sua aldeia de um ataque de goblins. Desde então percorre o mundo em busca de desafios dignos de sua lâmina.",
        "status": "ativa",
    },
    {
        "id": 2,
        "nome": "Lyra Sussurro-das-Sombras",
        "jogador": "jogador1",
        "classe": "Ladino",
        "raca": "Elfa",
        "nivel": 3,
        "hp_atual": 22,
        "hp_max": 28,
        "mp_atual": 15,
        "mp_max": 15,
        "atributos": {
            "forca": 10,
            "destreza": 18,
            "constituicao": 12,
            "inteligencia": 14,
            "sabedoria": 13,
            "carisma": 15,
        },
        "historia": "Espiã élfica a serviço de uma guilda secreta, Lyra carrega segredos que poderiam mudar o destino de reinos inteiros. Ninguém sabe ao certo a quem ela serve de verdade.",
        "status": "ativa",
    },
    {
        "id": 3,
        "nome": "Brom Martelo-de-Pedra",
        "jogador": "jogador2",
        "classe": "Clerigo",
        "raca": "Anao",
        "nivel": 4,
        "hp_atual": 38,
        "hp_max": 42,
        "mp_atual": 20,
        "mp_max": 30,
        "atributos": {
            "forca": 14,
            "destreza": 9,
            "constituicao": 16,
            "inteligencia": 12,
            "sabedoria": 18,
            "carisma": 10,
        },
        "historia": "Sacerdote anão dedicado ao deus da forja, Brom busca recuperar um artefato sagrado roubado de seu templo há séculos. Sua fé é inabalável, mas seu temperamento, nem tanto.",
        "status": "ativa",
    },
]

_next_id = 4


def login(usuario: str, senha: str) -> dict:
    u = USUARIOS.get(usuario)
    if not u or u["senha"] != senha:
        return {"erro": "Usuário ou senha inválidos"}
    return {"ok": True, "usuario": usuario, "role": u["role"]}


def get_fichas(usuario: str, role: str) -> list:
    if role == "mestre":
        return list(_FICHAS)
    return [f for f in _FICHAS if f["jogador"] == usuario]


def get_ficha(ficha_id: int) -> dict | None:
    return next((f for f in _FICHAS if f["id"] == ficha_id), None)


def criar_ficha(dados: dict) -> dict:
    global _next_id
    ficha = {**dados, "id": _next_id, "status": "ativa"}
    _next_id += 1
    _FICHAS.append(ficha)
    return {"ok": True, "ficha": ficha}


def atualizar_ficha(ficha_id: int, dados: dict) -> dict:
    ficha = get_ficha(ficha_id)
    if not ficha:
        return {"erro": "Ficha não encontrada"}
    ficha.update(dados)
    return {"ok": True, "ficha": ficha}


def deletar_ficha(ficha_id: int) -> dict:
    for i, f in enumerate(_FICHAS):
        if f["id"] == ficha_id:
            _FICHAS.pop(i)
            return {"ok": True}
    return {"erro": "Ficha não encontrada"}


def get_dashboard(usuario: str, role: str) -> dict:
    fichas = get_fichas(usuario, role)
    jogadores = sorted({f["jogador"] for f in fichas})
    return {
        "total_fichas": len(fichas),
        "fichas_ativas": sum(1 for f in fichas if f["status"] == "ativa"),
        "jogadores": jogadores,
        "fichas": fichas,
    }
