from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

# Modelos
class Pessoa(BaseModel):
    id: str
    apelido: str
    nome: str
    nascimento: str
    stack: List[str]

# API e Rotas
app = FastAPI()

@app.post("/pessoas")
async def create_person():
    return {"message": "This action create a person"}


@app.get("/pessoas")
async def get_persons(t: str = None):
    if t is None:
        pass
        # Pega Tudo
    # Pega por filtro
    
    return {"message": f"This action return all peoples"}


@app.get("/contagem-pessoas")
async def get_count():
    return {"message": "This action return count of peoples"}

