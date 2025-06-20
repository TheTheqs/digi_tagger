# database/engine.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base

# Importando os models para registrar as tabelas
from database.models.tag import Tag
from database.models.tag_type import TagType
from database.models.sprite import Sprite
from database.models.configuration import Configuration
from database.models.configuration_tags import configuration_tags

# Criando pasta para o banco (se não existir)
os.makedirs("data", exist_ok=True)

# Definindo o caminho do banco
DATABASE_URL = "sqlite:///data/eyeing.db"

# Criando a engine
engine = create_engine(DATABASE_URL, echo=False)

# Criando o session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para inicializar o banco
def init_db():
    Base.metadata.create_all(bind=engine)
