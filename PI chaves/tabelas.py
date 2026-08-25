from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, Boolean, Time, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy

#Criando conexao com o banco de dados
engine = create_engine(
    "mysql+pymysql://root:@localhost:3306/db_chave",
    echo=True
)

#Criando tabela banco de dados chave
Base=declarative_base()
class Chave(Base):
    __tablename__    = "tb_chave"
    id_chave         = Column(Integer, primary_key=True)
    id_ambiente      = Column(Integer)
    observacao_chave = Column(String(250))
    status           = Column(Boolean)
    nome_chave       = Column(String(150))
Base.metadata.create_all(engine)


#Criando tabela banco de dados usuarios
class Usuario(Base):
    __tablename__ = "tb_usuario"
    id_usuario    = Column(Integer, primary_key=True)
    email         = Column(String(250))
    senha_usuario = Column(String(250))
    id_perfil     = Column(Integer)
    nivel         = Column(String(60))
Base.metadata.create_all(engine)

#Criando tabela banco de dados perfil
class Perfil(Base):
    __tablename__ = "tb_perfil"
    id_perfil     = Column(Integer, primary_key=True)
    nome_perfil   = Column(String(250))
    matricula     = Column(String(250))
    cargo         = Column(String(200))
    status_perfil = Column(Boolean)
    foto_perfil   = Column(String(250), default="icon_user.png")
Base.metadata.create_all(engine)

#Criando tabela banco de dados ambiente
class Ambiente(Base):
    __tablename__       = "tb_ambiente"
    id_ambiente         = Column(Integer, primary_key=True)
    nome_sala           = Column(String(150))
    status_ambiente     = Column(Boolean)
    observacao_ambiente = Column(String(250))
    tipo                = Column(String(150))
    localizacao         = Column(String(250))
Base.metadata.create_all(engine)


#Criando tabela banco de dados movimentacao
class Movimentacao(Base):
    __tablename__      = "tb_movimentacao"
    id_movimentacao    = Column(Integer, primary_key=True)
    id_chave           = Column(Integer)
    id_perfil          = Column(Integer)
    codigo_reserva     = Column(String(250))
    date_hora_reserva  = Column(DateTime)
    date_hora_retirada = Column(DateTime)
    date_hora_devolucao = Column(DateTime)
    date_hora_devolucao_prev =Column(DateTime)
    status             =Column(String(50))
Base.metadata.create_all(engine)


