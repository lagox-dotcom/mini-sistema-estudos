from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Importações do seu próprio sistema
from app.database import get_db
from app.models import Aula
from app.core.motor_3r import calcular_proxima_revisao # O cérebro da operação!

router = APIRouter(prefix="/aulas", tags=["Aulas"])

@router.post("/{aula_id}/concluir")
def concluir_aula(aula_id: int, db: Session = Depends(get_db)):
    
    # 1. Busca a aula
    aula = db.query(Aula).filter(Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada na base")

    # 2. Atualiza o status
    aula.status = "Concluída"

    # 3. Chama o Motor 3R para fazer o trabalho pesado
    # Passamos a aula inteira para o motor, pois ele pode querer olhar a 'dificuldade'
    aula = calcular_proxima_revisao(aula)

    # 4. Salva no banco
    db.commit()
    db.refresh(aula) # Atualiza o objeto com os dados novos do banco

    return {"mensagem": f"Aula {aula.aula} concluída! Revisão programada para {aula.proxima_revisao}"}