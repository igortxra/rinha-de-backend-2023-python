import uuid
from datetime import datetime
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, constr, validator
from pymongo import MongoClient
from pymongo.collection import Collection

# Database
DB_URI = "mongodb://root:root@db:27017/person_db?authSource=admin"
 
def get_collection() -> Collection:
    client = MongoClient(DB_URI)
    db = client.person_db
    collection = db.pessoas
    return collection

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

class PessoaComID(PessoaBase):
    id: str | None

# API e Rotas
app = FastAPI()

@app.post("/pessoas")
async def create_person(person: PessoaBase):
    person = PessoaComID(id=str(uuid.uuid4()), **dict(person))
    collection = get_collection()
    collection.insert_one(person.model_dump())
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

