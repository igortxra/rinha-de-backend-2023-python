import uuid
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr, validator
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId

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

@app.post("/pessoas", status_code=201)
async def create_person(person: PessoaBase):
    # person = PessoaComID(id=str(uuid.uuid4()), **dict(person))
    collection = get_collection()
    collection.insert_one(person.model_dump()).inserted_id
    return person

@app.get("/pessoas")
async def get_persons(t: str = ''):
    if not t:
        raise HTTPException(status_code=400, detail="Parâmetro de busca inválido")

    collection = get_collection()
    # Executando a consulta
    consulta = {
        "$or": [
            {"apelido": {"$regex": t, "$options": "i"}},
            {"nome": {"$regex": t, "$options": "i"}},
            {"stack": t}
        ]
    }
    results = collection.find(consulta).limit(50)
    # persons = [PessoaComID(**result) for result in results]

    persons = []
    for result in results:
        result["id"] = str(result.pop("_id"))  # Convertendo ObjectId para string
        persons.append(result)
    return persons

@app.get("/pessoas/{id}")
async def get_person_by_id(id:str):
    collection = get_collection()
    print(id)
    result = collection.find_one({"_id": ObjectId(id)})
    if result is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    result["id"] = str(result.pop("_id"))  # Convertendo ObjectId para string
    # return PessoaComID(**result) 
    return result 

@app.get("/contagem-pessoas")
async def get_count():
    return get_collection().count_documents({})

