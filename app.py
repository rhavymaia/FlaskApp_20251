from flask import Flask, request, jsonify
import sqlite3

from models.InstituicaoEnsino import InstituicaoEnsino

app = Flask(__name__)


@app.route("/")
def index():
    versao = {"versao": "0.0.1"}
    return jsonify(versao), 200


@app.get("/instituicoes")
def instituicoesResource():
    print("Get - Instituições")

    try:
        instituicoesEnsino = []

        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tb_instituicao')
        resultSet = cursor.fetchall()

        for row in resultSet:
            # Montar o conjunto de instituições.
            id = row[0]
            no_entidade = row[1]
            co_entidade = row[2]
            qt_mat_bas = row[3]

            instituicaoEnsino = InstituicaoEnsino(
                id, no_entidade, co_entidade, qt_mat_bas)
            instituicoesEnsino.append(instituicaoEnsino.toDict())

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

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
    instituicaoJson = request.get_json()

    isValido = validarInstituicao(instituicaoJson)
    if (isValido):

        no_entidade = instituicaoJson['no_entidade']
        co_entidade = instituicaoJson['co_entidade']
        qt_mat_bas = instituicaoJson['qt_mat_bas']

        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tb_instituicao (no_entidade, co_entidade, qt_mat_bas) VALUES(?, ?, ?)', (no_entidade, co_entidade, qt_mat_bas))
        conn.commit()

        id = cursor.lastrowid

        instituicaoEnsino = InstituicaoEnsino(
            id, no_entidade, co_entidade, qt_mat_bas)

        conn.close()

        return jsonify(instituicaoEnsino.toDict()), 200

    return jsonify({"mensagem": "Não cadastrado"}), 406


@app.route("/instituicoes/<int:id>", methods=["DELETE"])
def instituicaoRemocaoResource(id):
    pass


@app.route("/instituicoes/<int:id>", methods=["PUT"])
def instituicaoAtualizacaoResource(id):
    print("Put - Instituição")
    instituicoes = [
        {"nome": "IFPB - Guarabira"},
        {"nome": "UEPB - Guarabira"}
    ]
    return jsonify(instituicoes), 200


@app.route("/instituicoes/<int:id>", methods=["GET"])
def instituicoesByIdResource(id):
    try:
        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tb_instituicao WHERE id = ?', (id, ))
        row = cursor.fetchone()

        # Montar a de instituição.
        id = row[0]
        no_entidade = row[1]
        co_entidade = row[2]
        qt_mat_bas = row[3]

        instituicaoEnsino = InstituicaoEnsino(
            id, no_entidade, co_entidade, qt_mat_bas)

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify(instituicaoEnsino.toDict()), 200
