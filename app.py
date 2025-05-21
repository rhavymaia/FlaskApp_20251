from flask import request, jsonify, g
import sqlite3
from marshmallow import ValidationError

from helpers.application import app
from helpers.database import getConnection
from helpers.logging import logger
from helpers.CORS import cors

from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema

cors.init_app(app)


@app.route("/")
def index():
    versao = {"versao": "0.0.1"}
    return jsonify(versao), 200


@app.get("/instituicoes")
def instituicoesResource():
    logger.info("Get - Instituições")

    try:
        instituicoesEnsino = []
        cursor = getConnection().cursor()
        cursor.execute(
            'SELECT * FROM tb_instituicao')
        resultSet = cursor.fetchall()

        for row in resultSet:
            # Montar o conjunto de instituições.
            logger.info(row)
            id = row[0]
            no_entidade = row[1]
            co_entidade = row[2]
            qt_mat_bas = row[3]

            instituicaoEnsino = InstituicaoEnsino(
                id, no_entidade, co_entidade, qt_mat_bas)
            instituicoesEnsino.append(instituicaoEnsino.toDict())

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicoesEnsino), 200


def validarInstituicao(content):
    isValido = True
    # if (content['co_uf'] < 11 and content['co_uf'] > 53):
    #     isValido = False
    if (len(content['no_entidade']) < 3 or content['no_entidade'].isdigit()):
        isValido = False

    if (not (content['co_entidade'].isdigit())):
        isValido = False

    if (not (content['qt_mat_bas'].isdigit())):
        isValido = False

    return isValido


@app.post("/instituicoes")
def instituicaoInsercaoResource():
    print("Post - Instituição")
    instituicaoEnsinoSchema = InstituicaoEnsinoSchema()

    instituicaoData = request.get_json()

    try:
        instituicaoJson = instituicaoEnsinoSchema.load(instituicaoData)

        no_entidade = instituicaoJson['no_entidade']
        co_entidade = instituicaoJson['co_entidade']
        qt_mat_bas = instituicaoJson['qt_mat_bas']

        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tb_instituicao (no_entidade, co_entidade, qt_mat_bas) VALUES(?, ?, ?)', (no_entidade, co_entidade, qt_mat_bas))
        conn.commit()

        id = cursor.lastrowid

        instituicaoEnsino = InstituicaoEnsino(
            id, no_entidade, co_entidade, qt_mat_bas)

        return jsonify(instituicaoEnsino.toDict()), 200

    except ValidationError as err:
        return jsonify(err.messages), 400
    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify({"mensagem": "Não cadastrado"}), 406


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


@app.route("/instituicoes/<int:id>", methods=["GET"])
def instituicoesByIdResource(id):
    try:
        cursor = getConnection().cursor()
        cursor.execute(
            'SELECT * FROM tb_instituicao WHERE id = ?', (id, ))
        row = cursor.fetchone()

        if row is not None:
            # Montar a de instituição.
            id = row[0]
            no_entidade = row[1]
            co_entidade = row[2]
            qt_mat_bas = row[3]

            instituicaoEnsino = InstituicaoEnsino(
                id, no_entidade, co_entidade, qt_mat_bas)
        else:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicaoEnsino.toDict()), 200
