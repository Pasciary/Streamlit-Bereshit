"""
Cliente da API RPG System.

Modo mock (sem backend): USE_MOCK em gui/mock_data.py ou RPG_USE_MOCK=1
Modo API real: USE_MOCK=False e uvicorn main:app --reload
"""

import os

from gui import mock_data


def _use_mock() -> bool:
    env = os.getenv("RPG_USE_MOCK")
    if env is not None:
        return env.strip().lower() in ("1", "true", "yes", "on")
    return mock_data.ENABLE_MOCK


if _use_mock():
    from gui import mock_client as _impl
else:
    import httpx

    BASE_URL = "http://localhost:8000"

    def _get(path, params=None):
        try:
            r = httpx.get(f"{BASE_URL}{path}", params=params, timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"erro": str(e)}

    def _post(path, json=None):
        try:
            r = httpx.post(f"{BASE_URL}{path}", json=json, timeout=5)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            return {"erro": e.response.json().get("detail", str(e))}
        except Exception as e:
            return {"erro": str(e)}

    def _patch(path, json=None):
        try:
            r = httpx.patch(f"{BASE_URL}{path}", json=json, timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"erro": str(e)}

    def _delete(path):
        try:
            r = httpx.delete(f"{BASE_URL}{path}", timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"erro": str(e)}

    class _impl:
        @staticmethod
        def login(usuario, senha):
            return _post("/auth/login", {"usuario": usuario, "senha": senha})

        @staticmethod
        def listar_fichas():
            return _get("/fichas")

        @staticmethod
        def buscar_ficha(ficha_id):
            return _get(f"/fichas/{ficha_id}")

        @staticmethod
        def criar_ficha(dados):
            return _post("/fichas", dados)

        @staticmethod
        def atualizar_hp(ficha_id, hp_atual):
            return _patch(f"/fichas/{ficha_id}", {"hp_atual": hp_atual})

        @staticmethod
        def deletar_ficha(ficha_id):
            return _delete(f"/fichas/{ficha_id}")

        @staticmethod
        def adicionar_condicao(ficha_id, condicao):
            return _post(f"/fichas/{ficha_id}/condicao", {"condicao": condicao})

        @staticmethod
        def remover_condicao(ficha_id, condicao):
            return _delete(f"/fichas/{ficha_id}/condicao/{condicao}")

        @staticmethod
        def descanso(ficha_id, tipo):
            return _post(f"/fichas/{ficha_id}/descanso/{tipo}")

        @staticmethod
        def listar_inventario(ficha_id):
            return _get(f"/fichas/{ficha_id}/inventario")

        @staticmethod
        def adicionar_item(ficha_id, nome, quantidade, descricao="", tipo="item"):
            return _post(f"/fichas/{ficha_id}/inventario", {
                "nome": nome, "quantidade": quantidade,
                "descricao": descricao, "tipo": tipo,
            })

        @staticmethod
        def remover_item(ficha_id, item_id):
            return _delete(f"/fichas/{ficha_id}/inventario/{item_id}")

        @staticmethod
        def listar_magias_ficha(ficha_id):
            return _get(f"/fichas/{ficha_id}/magias")

        @staticmethod
        def aprender_magia(ficha_id, magia_id):
            return _post(f"/fichas/{ficha_id}/magias/{magia_id}")

        @staticmethod
        def esquecer_magia(ficha_id, magia_id):
            return _delete(f"/fichas/{ficha_id}/magias/{magia_id}")

        @staticmethod
        def usar_slot(ficha_id, nivel):
            return _post(f"/fichas/{ficha_id}/slots/{nivel}/usar")

        @staticmethod
        def catalogo_itens():
            return _get("/catalogo/itens")

        @staticmethod
        def catalogo_magias():
            return _get("/catalogo/magias")

        @staticmethod
        def catalogo_monstros():
            return _get("/catalogo/monstros")

        @staticmethod
        def rolar_dados(dado, quantidade, modificador, ficha_id=None, personagem="Anônimo", motivo=""):
            return _post("/dados/rolar", {
                "dado": dado, "quantidade": quantidade,
                "modificador": modificador, "ficha_id": ficha_id,
                "personagem": personagem, "motivo": motivo,
            })

        @staticmethod
        def log_dados():
            return _get("/dados/log")

        @staticmethod
        def limpar_log():
            return _delete("/dados/log")

        @staticmethod
        def estado_combate():
            return _get("/combate")

        @staticmethod
        def iniciar_combate(participantes):
            return _post("/combate/iniciar", {"participantes": participantes})

        @staticmethod
        def proximo_turno():
            return _post("/combate/proximo")

        @staticmethod
        def encerrar_combate():
            return _post("/combate/encerrar")

        @staticmethod
        def listar_notas():
            return _get("/notas")

        @staticmethod
        def criar_nota(titulo, conteudo, categoria="geral"):
            return _post("/notas", {"titulo": titulo, "conteudo": conteudo, "categoria": categoria})

        @staticmethod
        def deletar_nota(nota_id):
            return _delete(f"/notas/{nota_id}")

        @staticmethod
        def dashboard():
            return _get("/dashboard")

        @staticmethod
        def personagem_ativo_turno():
            return _get("/combate/ativo")

        @staticmethod
        def vincular_ficha(usuario_id, ficha_id):
            return _post(f"/auth/vincular-ficha?usuario_id={usuario_id}&ficha_id={ficha_id}")

        @staticmethod
        def listar_campanhas_usuario(usuario_id):
            return _get(f"/campanhas?usuario_id={usuario_id}")


# reexporta funções para `from gui import client` / `client.login(...)`
login = _impl.login
listar_fichas = _impl.listar_fichas
buscar_ficha = _impl.buscar_ficha
criar_ficha = _impl.criar_ficha
atualizar_hp = _impl.atualizar_hp
deletar_ficha = _impl.deletar_ficha
adicionar_condicao = _impl.adicionar_condicao
remover_condicao = _impl.remover_condicao
descanso = _impl.descanso
listar_inventario = _impl.listar_inventario
adicionar_item = _impl.adicionar_item
remover_item = _impl.remover_item
listar_magias_ficha = _impl.listar_magias_ficha
aprender_magia = _impl.aprender_magia
esquecer_magia = _impl.esquecer_magia
usar_slot = _impl.usar_slot
catalogo_itens = _impl.catalogo_itens
catalogo_magias = _impl.catalogo_magias
catalogo_monstros = _impl.catalogo_monstros
rolar_dados = _impl.rolar_dados
log_dados = _impl.log_dados
limpar_log = _impl.limpar_log
estado_combate = _impl.estado_combate
iniciar_combate = _impl.iniciar_combate
proximo_turno = _impl.proximo_turno
encerrar_combate = _impl.encerrar_combate
listar_notas = _impl.listar_notas
criar_nota = _impl.criar_nota
deletar_nota = _impl.deletar_nota
dashboard = _impl.dashboard
personagem_ativo_turno = _impl.personagem_ativo_turno
vincular_ficha = _impl.vincular_ficha
listar_campanhas_usuario = _impl.listar_campanhas_usuario

MOCK_ATIVO = _use_mock()
