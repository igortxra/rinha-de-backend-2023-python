import uuid
from datetime import datetime
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, constr, validator

# Modelos
class PessoaBase(BaseModel):
    apelido: constr(max_length=32)
    nome: constr(max_length=100)
    nascimento: str
    stack: List[constr(max_length=32)] | None

    @validator("nascimento")
    def valida_formato_data(cls, valor):
        try:
            datetime.strptime(valor, '%Y-%m-%d')
            return valor
        except ValueError:
            raise ValueError("Formato de data inválido")

class PessoaRead(PessoaBase):
    id: str | None

# API e Rotas
app = FastAPI()

@app.post("/pessoas")
async def create_person(person: PessoaBase):
    person = PessoaRead(id=str(uuid.uuid4()), **dict(person))
    # ok = insere_pessoa
    # if ok:
    return person

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

