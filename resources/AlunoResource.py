from helpers.logging import logger
from helpers.database import db
from flask import request
from flask_restful import Resource, marshal
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from models.Aluno import Aluno, AlunoSchema, aluno_fields


class AlunosResource(Resource):
    def get(self):
        logger.info("Get - Alunos")

        try:
            # alunos = Aluno.query.all()

            stmt = db.select(Aluno)
            result = db.session.execute(stmt).scalars()
            alunos = result.all()

        except SQLAlchemyError as e:
            return {"mensagem": "Problema com o banco de dados."}, 500

        return marshal(alunos, aluno_fields), 200

    def post(self):
        logger.info("Post - Aluno")

        alunoSchema = AlunoSchema()

        alunoData = request.get_json()

        try:
            alunoJson = alunoSchema.load(alunoData)

            # Aluno
            nome = alunoJson['nome']
            sobrenome = alunoJson['sobrenome']
            cpf = alunoJson['cpf']
            email = alunoJson['email']
            nascimento = alunoJson['nascimento']
            matricula = alunoJson['matricula']
            aluno = Aluno(nome, sobrenome, cpf, nascimento, email, matricula)

            # Inserir na base de dados
            db.session.add(aluno)
            db.session.commit()

            return marshal(aluno, aluno_fields), 200

        except ValidationError as err:
            return {"mensagem": "Problema na validação."}, 400


class AlunoResource(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass
