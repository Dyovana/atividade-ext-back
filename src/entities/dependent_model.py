from pydantic import BaseModel


class Dependent(BaseModel):
    name: str
    cpf_responsavel: str
    description: str
