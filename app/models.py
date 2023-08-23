from pydantic import BaseModel, constr
from typing import List

# Modelos
class Pessoa(BaseModel):
    apelido: constr(max_length=32)
    nome: constr(max_length=100)
    nascimento: constr(pattern=r'^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$')
    stack: List[constr(max_length=32)] | None
