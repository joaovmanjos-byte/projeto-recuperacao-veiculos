from fastapi import FastAPI

from database import Base, engine
from routers.veiculos import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Frota de Veiculos",
    description="Cadastro e gerenciamento de veiculos com persistencia SQLite.",
    version="1.0.0",
)

app.include_router(router)
