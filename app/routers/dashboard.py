from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import date, timedelta

# Importamos do nosso ecossistema central
from app.database import get_db
from app.models import Sessao, Aula

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def dashboard(db: Session = Depends(get_db)):
    hoje = date.today()
    semana_passada = hoje - timedelta(days=7)

    # 1. Total de Horas na Semana (Usando o banco para somar)
    horas_semana = db.query(func.sum(Sessao.hora_liquida)).filter(
        Sessao.data >= semana_passada
    ).scalar()

    # 2. Total de Sessões
    total_sessoes = db.query(Sessao).count()

    # 3. Progresso por Disciplina (O SQL faz o agrupamento e a contagem de uma vez só!)
    # Isso substitui a função 'progresso_por_disciplina' em Python
    progresso_query = db.query(
        Aula.disciplina,
        func.count(Aula.id).label('total_aulas'),
        func.sum(
            # Se o status for concluída, soma 1. Se não, soma 0.
            case((Aula.status.ilike("concluída"), 1), else_=0)
        ).label('aulas_concluidas')
    ).group_by(Aula.disciplina).all()

    # Formata o resultado do banco para um dicionário bonitinho pro seu frontend
    progresso_disciplinas = {}
    for disciplina, total, concluidas in progresso_query:
        # Se for None, transforma em 0 por segurança
        concluidas = concluidas or 0 
        
        # Calcula a porcentagem de conclusão
        percentual = (concluidas / total * 100) if total > 0 else 0
        
        progresso_disciplinas[disciplina] = {
            "total": total,
            "concluidas": concluidas,
            "percentual_conclusao": round(percentual, 1) # Arredonda para 1 casa decimal
        }

    # 4. Retorna o pacote completo para a tela
    return {
        "resumo_semanal": {
            "horas_semana": horas_semana or 0,
            "total_sessoes": total_sessoes
        },
        "progresso_edital": progresso_disciplinas
    }