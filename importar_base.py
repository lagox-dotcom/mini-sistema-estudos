import csv
import sys
import os

# Garante que o Python reconheça a pasta 'app' como um módulo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import Base, Aula # <-- A correção está aqui!

# Cria as tabelas no banco de dados, caso ainda não existam
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    with open("base_edital.csv", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        print("Colunas encontradas no CSV:", reader.fieldnames)

        for row in reader:
            # Garante que a dificuldade seja salva como número (Integer)
            nivel_dificuldade = int(row["Dificuldade"].strip()) if row["Dificuldade"].strip().isdigit() else 0

            aula = Aula(  # <-- E aqui também!
                aula=row["Aula"].strip(),
                disciplina=row["Matéria"].strip(),
                assunto=row["Assunto"].strip(),
                status=row["Status"].strip(),
                dificuldade=nivel_dificuldade
            )
            db.add(aula)

    db.commit()
    print("Base do edital importada com sucesso para o banco de dados!")
    
except Exception as e:
    print(f"Ocorreu um erro durante a importação: {e}")
    db.rollback()
finally:
    db.close()