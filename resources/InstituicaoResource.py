from flask import jsonify, request
from flask_restful import Resource, marshal
from marshmallow import ValidationError
import sqlite3

from helpers.database import getConnection
from helpers.logging import logger

from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema, instituicao_fields


class InstituicoesResource(Resource):
    def get(self):
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
                instituicoesEnsino.append(instituicaoEnsino)

        except sqlite3.Error as e:
            return {"mensagem": "Problema com o banco de dados."}, 500

        return marshal(instituicoesEnsino, instituicao_fields), 200

    def post(self):
        logger.info("Post - Instituição")

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
                f"INSERT INTO tb_instituicao (no_entidade, co_entidade, qt_mat_bas) VALUES('{no_entidade}', {co_entidade}, {qt_mat_bas})")
            conn.commit()

            instituicaoEnsino = InstituicaoEnsino(
                0, no_entidade, co_entidade, qt_mat_bas)

            return marshal(instituicaoEnsino, instituicao_fields), 200

        except ValidationError as err:
            return {"mensagem": "Problema na validação."}, 400
        except sqlite3.Error as e:
            return {"mensagem": "Problema com o banco de dados."}, 500


class InstituicaoResource(Resource):
    def get(self, id):
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
                return {"mensagem": "Instituição não encontrada."}, 404

        except sqlite3.Error as e:
            return {"mensagem": "Problema com o banco de dados."}, 500

        return marshal(instituicaoEnsino, instituicao_fields), 200

    def put(self, id):
        pass

    def delete(self, id):
        pass
