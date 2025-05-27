from flask import jsonify
import sqlite3

from helpers.application import app, api
from helpers.database import getConnection
from helpers.logging import logger
from helpers.CORS import cors

from resources.InstituicaoResource import InstituicoesResource, InstituicaoResource
from resources.IndexResource import IndexResource

cors.init_app(app)

api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicaoResource, '/instituicoes/<int:id>')


@app.route("/instituicoes/<int:id>", methods=["DELETE"])
def instituicaoRemocaoResource(id):
    try:
        conn = getConnection()
        c = conn.cursor()
        c.execute('DELETE FROM tb_instituicao WHERE id = ?', (id,))
        conn.commit()
        return ({"mensagem": "Removido com sucesso."}, 200)
    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500


@app.route("/instituicoes/<int:id>", methods=["PUT"])
def instituicaoAtualizacaoResource(id):
    print("Put - Instituição")
    instituicoes = [
        {"nome": "IFPB - Guarabira"},
        {"nome": "UEPB - Guarabira"}
    ]

    # Verificar se o ID existe.
    # Caso o item exista, atualize.
    return jsonify(instituicoes), 200
