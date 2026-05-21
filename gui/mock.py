"""Mock API layer with bcrypt password verification and SQLite persistence."""
import logging

import bcrypt

from gui import db

logger = logging.getLogger(__name__)

# Hashes pre-computados com bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
# Senhas originais: mestre="01234", jogador1/jogador2="1234"
_USUARIOS: dict[str, dict] = {
    "mestre": {
        "senha_hash": "$2b$12$rJ5PLuGVsoXQ3OrK0G5gOuDOu3/oz6nctkq0Z2GXANi2hFyCdorWq",
        "role": "mestre",
    },
    "jogador1": {
        "senha_hash": "$2b$12$3JfWByMwK58x6OWoDUCB5.2aUyZk05Vosb1oNBquJMMbqKyhtTEqe",
        "role": "jogador",
    },
    "jogador2": {
        "senha_hash": "$2b$12$3JfWByMwK58x6OWoDUCB5.2aUyZk05Vosb1oNBquJMMbqKyhtTEqe",
        "role": "jogador",
    },
}


def login(usuario: str, senha: str) -> dict:
    """Authenticate a user. Returns session data on success or an error dict."""
    u = _USUARIOS.get(usuario)
    if not u or not bcrypt.checkpw(senha.encode(), u["senha_hash"].encode()):
        logger.warning("Tentativa de login inválida para usuário: %s", usuario)
        return {"erro": "Usuário ou senha inválidos"}
    logger.info("Login bem-sucedido: %s (%s)", usuario, u["role"])
    return {"ok": True, "usuario": usuario, "role": u["role"]}


def get_fichas(usuario: str, role: str) -> list[dict]:
    """Return all fichas for mestre, or only the user's fichas for jogador."""
    return db.fetch_fichas(usuario, role)


def get_ficha(ficha_id: int) -> dict | None:
    """Return a single ficha by ID, or None if not found."""
    return db.fetch_ficha(ficha_id)


def criar_ficha(dados: dict) -> dict:
    """Create a new ficha and return it."""
    ficha = db.insert_ficha(dados)
    logger.info("Ficha criada: id=%s nome=%s", ficha["id"], ficha["nome"])
    return {"ok": True, "ficha": ficha}


def atualizar_ficha(ficha_id: int, dados: dict) -> dict:
    """Update an existing ficha and return it, or an error dict if not found."""
    ficha = db.update_ficha(ficha_id, dados)
    if not ficha:
        return {"erro": "Ficha não encontrada"}
    logger.info("Ficha atualizada: id=%s", ficha_id)
    return {"ok": True, "ficha": ficha}


def deletar_ficha(ficha_id: int) -> dict:
    """Delete a ficha by ID."""
    if not db.delete_ficha(ficha_id):
        return {"erro": "Ficha não encontrada"}
    logger.info("Ficha deletada: id=%s", ficha_id)
    return {"ok": True}


def get_dashboard(usuario: str, role: str) -> dict:
    """Return aggregated dashboard data for the given user."""
    fichas = get_fichas(usuario, role)
    jogadores = sorted({f["jogador"] for f in fichas})
    return {
        "total_fichas": len(fichas),
        "fichas_ativas": sum(1 for f in fichas if f["status"] == "ativa"),
        "jogadores": jogadores,
        "fichas": fichas,
    }
