from helpers.logging import logger
from flask_restful import Resource, marshal
from sqlalchemy.exc import SQLAlchemyError

from models.Aluno import Aluno, aluno_fields


class AlunosResource(Resource):
    def get(self):
        logger.info("Get - Alunos")

        try:
            alunos = Aluno.query.all()
        except SQLAlchemyError as e:
            return {"mensagem": "Problema com o banco de dados."}, 500

        return marshal(alunos, aluno_fields), 200

    def post(self):
        pass


class AlunoResource(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass
