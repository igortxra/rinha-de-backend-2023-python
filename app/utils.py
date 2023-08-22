import json
from app.cache import r

async def create_cache(person_dict):
    r.set(person_dict["id"], json.dumps(person_dict))
    r.set(person_dict["apelido"], "1")

