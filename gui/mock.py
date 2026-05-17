USUARIOS = {
    "mestre": {"senha": "01234", "role": "mestre"},
    "jogador1": {"senha": "1234", "role": "jogador"},
    "jogador2": {"senha": "1234", "role": "jogador"},
}

def login(usuario: str, senha: str) -> dict:
    u = USUARIOS.get(usuario)
    if not u or u["senha"] != senha:
        return {"erro": "Usuário ou senha inválidos"}
    return {"ok": True, "usuario": usuario, "role": u["role"]}