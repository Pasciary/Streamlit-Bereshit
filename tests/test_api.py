"""Unit tests for the mock API layer."""
import gui.mock as api

_FICHA_NOVA = {
    "nome": "Thalia Ventoluz",
    "jogador": "jogador1",
    "classe": "Mago",
    "raca": "Elfo",
    "nivel": 2,
    "hp_atual": 12,
    "hp_max": 12,
    "mp_atual": 20,
    "mp_max": 20,
    "atributos": {
        "forca": 8,
        "destreza": 14,
        "constituicao": 10,
        "inteligencia": 18,
        "sabedoria": 13,
        "carisma": 12,
    },
    "historia": "Uma maga estudante da escola de evocação.",
}


# ── Login ─────────────────────────────────────────────────────────────────────

def test_login_mestre_sucesso():
    res = api.login("mestre", "01234")
    assert res.get("ok") is True
    assert res["role"] == "mestre"


def test_login_jogador_sucesso():
    res = api.login("jogador1", "1234")
    assert res.get("ok") is True
    assert res["role"] == "jogador"


def test_login_senha_errada():
    res = api.login("mestre", "senha_errada")
    assert "erro" in res
    assert "ok" not in res


def test_login_usuario_inexistente():
    res = api.login("ninguem", "qualquer")
    assert "erro" in res


# ── get_fichas ────────────────────────────────────────────────────────────────

def test_get_fichas_mestre_retorna_todas():
    fichas = api.get_fichas("mestre", "mestre")
    assert len(fichas) == 3


def test_get_fichas_jogador1_retorna_apenas_proprias():
    fichas = api.get_fichas("jogador1", "jogador")
    assert len(fichas) == 2
    assert all(f["jogador"] == "jogador1" for f in fichas)


def test_get_fichas_jogador2_retorna_apenas_proprias():
    fichas = api.get_fichas("jogador2", "jogador")
    assert len(fichas) == 1
    assert fichas[0]["jogador"] == "jogador2"


# ── get_ficha ─────────────────────────────────────────────────────────────────

def test_get_ficha_existente():
    ficha = api.get_ficha(1)
    assert ficha is not None
    assert ficha["nome"] == "Aldric Ferrovenas"
    assert "atributos" in ficha


def test_get_ficha_inexistente():
    assert api.get_ficha(9999) is None


# ── criar_ficha ───────────────────────────────────────────────────────────────

def test_criar_ficha_sucesso():
    res = api.criar_ficha(_FICHA_NOVA)
    assert res.get("ok") is True
    ficha = res["ficha"]
    assert ficha["nome"] == "Thalia Ventoluz"
    assert ficha["id"] is not None


def test_criar_ficha_persiste():
    res = api.criar_ficha(_FICHA_NOVA)
    ficha_id = res["ficha"]["id"]
    recuperada = api.get_ficha(ficha_id)
    assert recuperada is not None
    assert recuperada["nome"] == "Thalia Ventoluz"


def test_criar_ficha_atributos_preservados():
    res = api.criar_ficha(_FICHA_NOVA)
    at = res["ficha"]["atributos"]
    assert at["inteligencia"] == 18
    assert at["forca"] == 8


# ── atualizar_ficha ───────────────────────────────────────────────────────────

def test_atualizar_ficha_nivel():
    res = api.atualizar_ficha(1, {"nivel": 10})
    assert res.get("ok") is True
    assert res["ficha"]["nivel"] == 10


def test_atualizar_ficha_atributos():
    res = api.atualizar_ficha(1, {"atributos": {"forca": 20}})
    assert res.get("ok") is True
    assert res["ficha"]["atributos"]["forca"] == 20


def test_atualizar_ficha_inexistente():
    res = api.atualizar_ficha(9999, {"nivel": 1})
    assert "erro" in res


# ── deletar_ficha ─────────────────────────────────────────────────────────────

def test_deletar_ficha_sucesso():
    res = api.deletar_ficha(1)
    assert res.get("ok") is True
    assert api.get_ficha(1) is None


def test_deletar_ficha_remove_da_lista():
    api.deletar_ficha(1)
    fichas = api.get_fichas("mestre", "mestre")
    assert all(f["id"] != 1 for f in fichas)


def test_deletar_ficha_inexistente():
    res = api.deletar_ficha(9999)
    assert "erro" in res


# ── get_dashboard ─────────────────────────────────────────────────────────────

def test_dashboard_mestre():
    dados = api.get_dashboard("mestre", "mestre")
    assert dados["total_fichas"] == 3
    assert dados["fichas_ativas"] == 3
    assert set(dados["jogadores"]) == {"jogador1", "jogador2"}


def test_dashboard_jogador1():
    dados = api.get_dashboard("jogador1", "jogador")
    assert dados["total_fichas"] == 2
    assert dados["fichas_ativas"] == 2


def test_dashboard_jogador_sem_fichas():
    api.deletar_ficha(3)
    dados = api.get_dashboard("jogador2", "jogador")
    assert dados["total_fichas"] == 0
    assert dados["jogadores"] == []
