from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

# --- SCHEMAS DE AULAS ---

class AulaBase(BaseModel):
    aula: str
    disciplina: str
    assunto: str
    status: str
    dificuldade: int

class AulaCreate(AulaBase):
    pass 

class AulaResponse(AulaBase):
    id: int
    proxima_revisao: Optional[date] = None
    prioridade: Optional[int] = None

    # Aqui está o nosso ConfigDict devidamente importado e funcionando!
    model_config = ConfigDict(from_attributes=True) 


# --- SCHEMAS DE SESSÕES ---

class SessaoCreate(BaseModel):
    aula_id: int  
    data: date
    hora_inicio: str
    hora_fim: str
    hora_liquida: int 
    pagina_parada: Optional[str] = None
    questoes_feitas: int = 0
    acertos: int = 0
    status: str