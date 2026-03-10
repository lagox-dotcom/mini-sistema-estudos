import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Busca a URL do banco na nuvem. Se não achar, usa o SQLite local.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./estudos.db")

# 2. Correção de segurança: o SQLAlchemy mais recente exige 'postgresql://', 
# mas algumas vezes o Render entrega 'postgres://'. Isso resolve o conflito:
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. O SQLite exige 'check_same_thread', mas o PostgreSQL não aceita esse argumento.
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()