from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Aula(Base):

    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)

    disciplina = Column(String)
    aula = Column(String)
    assunto = Column(String)

    dificuldade = Column(Integer)

    status = Column(String)

    proxima_revisao = Column(Date)

    prioridade = Column(Integer)


class Sessao(Base):

    __tablename__ = "sessoes"

    id = Column(Integer, primary_key=True, index=True)

    data = Column(Date)

    disciplina = Column(String)

    aula = Column(String)

    pagina_parada = Column(String)

    questoes_feitas = Column(Integer)

    acertos = Column(Integer)

    hora_inicio = Column(String)

    hora_fim = Column(String)

    hora_liquida = Column(Integer)

    status = Column(String)