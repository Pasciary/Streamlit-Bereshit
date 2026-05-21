"""SQLite persistence layer for Bereshit."""
import logging
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

logger = logging.getLogger(__name__)

DB_PATH = Path(os.getenv("BERESHIT_DB", str(Path(__file__).parent.parent / "bereshit.db")))

_CREATE_FICHAS = """
CREATE TABLE IF NOT EXISTS fichas (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT    NOT NULL,
    jogador      TEXT    NOT NULL,
    classe       TEXT    NOT NULL,
    raca         TEXT    NOT NULL,
    nivel        INTEGER NOT NULL DEFAULT 1,
    hp_atual     INTEGER NOT NULL,
    hp_max       INTEGER NOT NULL,
    mp_atual     INTEGER NOT NULL,
    mp_max       INTEGER NOT NULL,
    forca        INTEGER NOT NULL DEFAULT 10,
    destreza     INTEGER NOT NULL DEFAULT 10,
    constituicao INTEGER NOT NULL DEFAULT 10,
    inteligencia INTEGER NOT NULL DEFAULT 10,
    sabedoria    INTEGER NOT NULL DEFAULT 10,
    carisma      INTEGER NOT NULL DEFAULT 10,
    historia     TEXT    NOT NULL DEFAULT '',
    status       TEXT    NOT NULL DEFAULT 'ativa'
)
"""

_SEED_FICHAS = [
    (
        "Aldric Ferrovenas", "jogador1", "Guerreiro", "Humano", 5,
        45, 52, 10, 10, 16, 12, 14, 10, 8, 11,
        "Nascido em uma família de ferreiros, Aldric descobriu seu talento para o "
        "combate após defender sua aldeia de um ataque de goblins. Desde então "
        "percorre o mundo em busca de desafios dignos de sua lâmina.",
        "ativa",
    ),
    (
        "Lyra Sussurro-das-Sombras", "jogador1", "Ladino", "Elfa", 3,
        22, 28, 15, 15, 10, 18, 12, 14, 13, 15,
        "Espiã élfica a serviço de uma guilda secreta, Lyra carrega segredos que "
        "poderiam mudar o destino de reinos inteiros. Ninguém sabe ao certo a quem "
        "ela serve de verdade.",
        "ativa",
    ),
    (
        "Brom Martelo-de-Pedra", "jogador2", "Clerigo", "Anao", 4,
        38, 42, 20, 30, 14, 9, 16, 12, 18, 10,
        "Sacerdote anão dedicado ao deus da forja, Brom busca recuperar um artefato "
        "sagrado roubado de seu templo há séculos. Sua fé é inabalável, mas seu "
        "temperamento, nem tanto.",
        "ativa",
    ),
]

_INSERT_SQL = """
    INSERT INTO fichas
        (nome, jogador, classe, raca, nivel,
         hp_atual, hp_max, mp_atual, mp_max,
         forca, destreza, constituicao, inteligencia, sabedoria, carisma,
         historia, status)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""


@contextmanager
def _conn() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create tables and seed initial data if the database is empty."""
    with _conn() as conn:
        conn.execute(_CREATE_FICHAS)
        if conn.execute("SELECT COUNT(*) FROM fichas").fetchone()[0] == 0:
            conn.executemany(_INSERT_SQL, _SEED_FICHAS)
            logger.info("Banco de dados inicializado com dados de exemplo.")


def _row_to_ficha(row: sqlite3.Row) -> dict:
    """Convert a SQLite row to the ficha dict with nested atributos."""
    d = dict(row)
    d["atributos"] = {
        attr: d.pop(attr)
        for attr in ("forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma")
    }
    return d


def fetch_fichas(usuario: str, role: str) -> list[dict]:
    """Return all fichas for mestre, or only the user's fichas for jogador."""
    with _conn() as conn:
        if role == "mestre":
            rows = conn.execute("SELECT * FROM fichas").fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM fichas WHERE jogador = ?", (usuario,)
            ).fetchall()
    return [_row_to_ficha(r) for r in rows]


def fetch_ficha(ficha_id: int) -> dict | None:
    """Return a single ficha by ID, or None if not found."""
    with _conn() as conn:
        row = conn.execute("SELECT * FROM fichas WHERE id = ?", (ficha_id,)).fetchone()
    return _row_to_ficha(row) if row else None


def insert_ficha(dados: dict) -> dict:
    """Insert a new ficha and return it with its generated ID."""
    at = dados["atributos"]
    with _conn() as conn:
        cur = conn.execute(
            _INSERT_SQL,
            (
                dados["nome"], dados["jogador"], dados["classe"], dados["raca"],
                dados["nivel"], dados["hp_atual"], dados["hp_max"],
                dados["mp_atual"], dados["mp_max"],
                at["forca"], at["destreza"], at["constituicao"],
                at["inteligencia"], at["sabedoria"], at["carisma"],
                dados.get("historia", ""), "ativa",
            ),
        )
        new_id = cur.lastrowid
    return fetch_ficha(new_id)


def update_ficha(ficha_id: int, dados: dict) -> dict | None:
    """Update an existing ficha and return the updated version, or None if not found."""
    ficha = fetch_ficha(ficha_id)
    if not ficha:
        return None
    ficha.update({k: v for k, v in dados.items() if k != "atributos"})
    if "atributos" in dados:
        ficha["atributos"].update(dados["atributos"])
    at = ficha["atributos"]
    with _conn() as conn:
        conn.execute(
            """UPDATE fichas SET
               nome=?, classe=?, raca=?, nivel=?,
               hp_atual=?, hp_max=?, mp_atual=?, mp_max=?,
               forca=?, destreza=?, constituicao=?, inteligencia=?,
               sabedoria=?, carisma=?, historia=?, status=?
               WHERE id=?""",
            (
                ficha["nome"], ficha["classe"], ficha["raca"], ficha["nivel"],
                ficha["hp_atual"], ficha["hp_max"],
                ficha["mp_atual"], ficha["mp_max"],
                at["forca"], at["destreza"], at["constituicao"],
                at["inteligencia"], at["sabedoria"], at["carisma"],
                ficha["historia"], ficha["status"],
                ficha_id,
            ),
        )
    return fetch_ficha(ficha_id)


def delete_ficha(ficha_id: int) -> bool:
    """Delete a ficha by ID. Returns True if a row was deleted."""
    with _conn() as conn:
        cur = conn.execute("DELETE FROM fichas WHERE id = ?", (ficha_id,))
    return cur.rowcount > 0
