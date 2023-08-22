import json
import uuid
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.utils import create_cache

from app.db import collection
from app.cache import r
from app.models import PessoaBase

# API e Rotas
api = FastAPI()

@api.exception_handler(RequestValidationError)  # Captura exceções de valor inválido (incluindo JSONDecodeError)
async def validation_exception_handler(request, exc):
    status_code=422
    if exc._errors[0]["input"] is None:
        status_code=400
    return JSONResponse(
        status_code=status_code,
        content={},
    )

@api.post("/pessoas")
async def create_person(person: PessoaBase):

    if r.get(person.apelido) is not None:
        return JSONResponse(status_code=422, content={})
     
    person_id = str(uuid.uuid4())
    person_dict = person.model_dump()
    person_dict["id"] = person_id
    await create_cache(person_dict)
    collection.insert_one(person_dict)

    return JSONResponse(content={}, headers={"Location": f"/pessoas/{person_id}"}, status_code=201)

@api.get("/pessoas")
async def get_persons(t: str):
    # Consulta no banco
    consulta = {
        "$or": [
            {"apelido": {"$regex": t, "$options": "i"}},
            {"nome": {"$regex": t, "$options": "i"}},
            {"stack": t}
        ]
    }
    projection = {"_id": 0}  # Não retornar o campo "_id"
    results = collection.find(consulta, projection=projection).limit(50)
    persons = list(results)
    return persons

@api.get("/pessoas/{id}")
async def get_person_by_id(id:str):
    # Pega do cache se existir
    result = r.get(id)
    if result: return json.loads(result)
    return JSONResponse(status_code=404, content={"detail": "Pessoa não encontrada"})

@api.get("/contagem-pessoas")
async def get_count():
    return collection.count_documents({})

