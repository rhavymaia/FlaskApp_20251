from models.Pessoa import Pessoa
from datetime import date
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

    def __init__(self, nome: str, sobrenome: str, cpf: str, nascimento: date, email: str, matricula: str):
        super().__init__(nome, sobrenome, cpf, nascimento, email)
        self.matricula = matricula

    __mapper_args__ = {
        "polymorphic_identity": "aluno",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.matricula!r})"
