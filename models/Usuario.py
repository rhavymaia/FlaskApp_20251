from typing import List
from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from helpers.database import db


class Usuario(db.Model):
    __tablename__ = "tb_usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    sobrenome: Mapped[str] = mapped_column()
    nascimento: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String)

    enderecos: Mapped[List["Endereco"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )

    def __init__(nome: str):
        pass


class Endereco(db.Model):
    __tablename__ = "tb_endereco"

    id: Mapped[int] = mapped_column(primary_key=True)
    logradouro: Mapped[str]
    usuario_id: Mapped[int] = mapped_column(ForeignKey("tb_usuario.id"))

    usuario: Mapped["Usuario"] = relationship(back_populates="enderecos")

    def __repr__(self) -> str:
        return f"Endereco(id={self.id!r}, logradouro={self.logradouro!r})"
