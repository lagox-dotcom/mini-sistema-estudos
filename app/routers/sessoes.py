from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models import Sessao, Aula
from app.schemas import SessaoCreate # Importando o validador que criamos acima

router = APIRouter(prefix="/sessoes", tags=["Sessoes"])

@router.get("/")
def listar_sessoes(db: Session = Depends(get_db)):
    # Retorna todas as sessões direto do banco de dados real
    return db.query(Sessao).all()

@router.post("/")
def criar_sessao(sessao_in: SessaoCreate, db: Session = Depends(get_db)):
    
    # 1. Busca a aula no "base_edital" para puxar a disciplina e o assunto
    aula_referencia = db.query(Aula).filter(Aula.id == sessao_in.aula_id).first()
    
    if not aula_referencia:
        raise HTTPException(status_code=404, detail="Aula não encontrada no edital.")

    # 2. Monta a sessão copiando os dados da aula
    nova_sessao = Sessao(
        data=sessao_in.data,
        disciplina=aula_referencia.disciplina, # Puxou automático!
        aula=aula_referencia.aula,             # Puxou automático!
        pagina_parada=sessao_in.pagina_parada,
        questoes_feitas=sessao_in.questoes_feitas,
        acertos=sessao_in.acertos,
        hora_inicio=sessao_in.hora_inicio,
        hora_fim=sessao_in.hora_fim,
        hora_liquida=sessao_in.hora_liquida,
        status=sessao_in.status
    )

    # 3. Salva no banco de dados
    db.add(nova_sessao)
    
    # Se a sessão foi marcada como concluída, já podemos atualizar o status da aula lá no edital
    if sessao_in.status.lower() == "concluída":
        aula_referencia.status = "Concluída"
        # Aqui você também poderia chamar aquele Motor 3R para já agendar a revisão!

    db.commit()
    db.refresh(nova_sessao)

    return {"mensagem": "Sessão registrada com sucesso!", "sessao_id": nova_sessao.id}