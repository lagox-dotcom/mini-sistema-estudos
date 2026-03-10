from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importando a base do banco e nossos roteadores
from app.database import engine, Base
from app.routers import aulas, sessoes, dashboard, planner

# Garante que as tabelas sejam criadas no banco de dados ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Sistema de Gestão de Estudos",
    description="API para controle de revisões, sessões e ciclo de estudos.",
    version="1.0.0"
)

# Configuração de segurança para permitir que um frontend se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite acesso de qualquer lugar (útil para testar)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectando todos os "departamentos" do nosso sistema
app.include_router(aulas.router)
app.include_router(sessoes.router)
app.include_router(dashboard.router)
app.include_router(planner.router)

@app.get("/")
def root():
    return {"mensagem": "Motor de estudos 100% operante!"}

import os

@app.get("/setup-banco")
def setup_banco():
    # Isso faz o Render rodar o script por dentro da própria rede dele!
    os.system("python importar_base.py")
    return {"mensagem": "Ordem de importação executada por dentro da nuvem!"}