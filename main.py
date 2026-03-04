from fastapi import FastAPI
from routers import sessoes

app = FastAPI()

app.include_router(sessoes.router)

@app.get("/")
def home():
    return {"mensagem": "Mini Sistema de Gestão de Estudos está rodando 🚀"}