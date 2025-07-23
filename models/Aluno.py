from models.Pessoa import Pessoa
from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Aluno(Pessoa):
    __tablename__ = "tb_aluno"
    id: Mapped[int] = mapped_column(
        ForeignKey("tb_pessoa.id"), primary_key=True)
    matricula: Mapped[str]

    def __init__(self, nome: str, sobrenome: str, nascimento: date, email: str, matricula: str):
        super().__init__(nome, sobrenome, nascimento, email)
        self.matricula = matricula

    __mapper_args__ = {
        "polymorphic_identity": "aluno",
    }
