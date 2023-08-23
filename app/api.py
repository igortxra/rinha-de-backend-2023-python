import uuid
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.db import collection
from app.models import Pessoa

api = FastAPI()

@api.exception_handler(RequestValidationError) 
async def validation_exception_handler(request, exc):
    status_code=422
    if exc._errors[0]["input"] is None:
        status_code=400
    return JSONResponse(
        status_code=status_code,
        content={},
    )

@api.post("/pessoas")
async def create_person(person: Pessoa):

    result = collection.find_one({"apelido": person.apelido})
    if result is not None: 
        return JSONResponse(status_code=422, content={})
     
    person_id = str(uuid.uuid4())

    person_dict = person.model_dump()
    person_dict["id"] = person_id
 
    collection.insert_one(person_dict)

    return JSONResponse(content={}, headers={"Location": f"/pessoas/{person_id}"}, status_code=201)

@api.get("/pessoas")
async def get_persons(t: str):
    consulta = {
        "$or": [
            {"apelido": {"$regex": t, "$options": "i"}},
            {"nome": {"$regex": t, "$options": "i"}},
            {"stack": t}
        ]
    }
    projection = {"_id": 0}
    results = collection.find(consulta, projection=projection).limit(50)
    persons = list(results)
    return persons

@api.get("/pessoas/{id}")
async def get_person_by_id(id:str):
    result = collection.find_one({"id": id})
    if result is None:
        return JSONResponse(status_code=404, content={})
    result.pop("_id")  # Convertendo ObjectId para string
    return result 

@api.get("/contagem-pessoas")
async def get_count():
    return collection.count_documents({})

