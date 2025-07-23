from typing import List
from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from helpers.database import db


class Pessoa(db.Model):
    __tablename__ = "tb_pessoa"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    sobrenome: Mapped[str] = mapped_column(String)
    cpf: Mapped[str] = mapped_column(String(11))
    nascimento: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String)
    tipo: Mapped[str]

    enderecos: Mapped[List["Endereco"]] = relationship(
        back_populates="pessoa", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "pessoa",
        "polymorphic_on": "tipo",
    }

    def __init__(self, nome: str, sobrenome: str, cpf: str, nascimento: date, email: str):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.nascimento = nascimento
        self.email = email

    def __repr__(self):
        return f"{self.__class__.__name__}({self.nome!r})"


class Endereco(db.Model):
    __tablename__ = "tb_endereco"

    id: Mapped[int] = mapped_column(primary_key=True)
    logradouro: Mapped[str]
    pessoa_id: Mapped[int] = mapped_column(ForeignKey("tb_pessoa.id"))

    pessoa: Mapped["Pessoa"] = relationship(back_populates="enderecos")

    def __init__(self, logradouro, pessoa_id):
        self.logradouro = logradouro
        self.pessoa_id = pessoa_id

    def __repr__(self) -> str:
        return f"Endereco(id={self.id!r}, logradouro={self.logradouro!r})"
