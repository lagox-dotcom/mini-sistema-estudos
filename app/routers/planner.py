from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import asc

from app.database import get_db
from app.models import Aula
from app.core.planner import gerar_plano_diario # Importando o nosso motor

router = APIRouter(prefix="/planner", tags=["Planner"])

@router.get("/hoje")
def planner_hoje(db: Session = Depends(get_db)):
    hoje = date.today()

    # 1. Puxa TODAS as revisões atrasadas
    revisoes = db.query(Aula).filter(
        Aula.proxima_revisao <= hoje
    ).order_by(asc(Aula.proxima_revisao)).all()

    # 2. Puxa um lote de aulas novas pendentes para o motor analisar
    # Pegamos umas 10 do banco para o algoritmo ter margem de escolha entre fáceis, médias e difíceis
    aulas_pendentes = db.query(Aula).filter(
        Aula.status.ilike("pendente")
    ).order_by(asc(Aula.id)).limit(10).all()

    # 3. Entrega os dados para o algoritmo montar o prato do dia!
    plano_de_hoje = gerar_plano_diario(revisoes, aulas_pendentes)

    return plano_de_hoje