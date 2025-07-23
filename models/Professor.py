from models.Pessoa import Pessoa
from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Professor(Pessoa):
    __tablename__ = "tb_professor"
    id: Mapped[int] = mapped_column(
        ForeignKey("tb_pessoa.id"), primary_key=True)
    siape: Mapped[str] = mapped_column(nullable=True)

    def __init__(self, nome: str, sobrenome: str, cpf: str, nascimento: date, email: str, siape: str):
        super().__init__(nome, sobrenome, cpf, nascimento, email)
        self.siape = siape

    __mapper_args__ = {
        "polymorphic_identity": "professor",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.siape!r})"
