from pydantic import BaseModel, constr, validator
from datetime import datetime
from typing import List

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
