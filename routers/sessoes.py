from fastapi import APIRouter

router = APIRouter(prefix="/sessoes", tags=["Sessoes"])

sessoes_db = []

@router.get("/")
def listar_sessoes():
    return sessoes_db

@router.post("/")
def criar_sessao(sessao: dict):
    sessoes_db.append(sessao)
    return {"mensagem": "Sessão criada com sucesso"}