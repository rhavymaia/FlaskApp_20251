from models.Pessoa import Pessoa
from datetime import date

from marshmallow import Schema, fields, validate
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_restful import fields as flaskFields

aluno_fields = {
    'id':   flaskFields.Integer,
    'nome':   flaskFields.String,
    'sobrenome':   flaskFields.String,
    'cpf':   flaskFields.String,
    'nascimento':   flaskFields.String,
    'email':   flaskFields.String,
    'matricula':   flaskFields.Integer
}


class Aluno(Pessoa):
    __tablename__ = "tb_aluno"
    id: Mapped[int] = mapped_column(
        ForeignKey("tb_pessoa.id"), primary_key=True)
    matricula: Mapped[str]
    cre: Mapped[float]

    def __init__(self, nome: str, sobrenome: str, cpf: str, nascimento: date, email: str, matricula: str):
        super().__init__(nome, sobrenome, cpf, nascimento, email)
        self.matricula = matricula

    __mapper_args__ = {
        "polymorphic_identity": "aluno",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.matricula!r})"


class AlunoSchema(Schema):
    nome = fields.String(validate=validate.Length(min=2, max=200),
                         required=True, error_messages={"required": "Nome da Entidade é obrigatório."})
    sobrenome = fields.String(validate=validate.Length(min=2, max=200),
                              required=True, error_messages={"required": "Sobrenome da Entidade é obrigatório."})
    cpf = fields.String(validate=validate.Length(min=11, max=11),
                        required=True, error_messages={"required": "CPF da Entidade é obrigatório."})
    nascimento = fields.Date(required=True, error_messages={
                             "required": "Nascimento da Entidade é obrigatório."})
    email = fields.Email(validate=validate.Length(min=11, max=11),
                         required=True, error_messages={"required": "E-mail da Entidade é obrigatório."})
    matricula = fields.String(validate=validate.Length(min=12, max=12),
                              required=True, error_messages={"required": "Matrículas da Entidade é obrigatório."})
