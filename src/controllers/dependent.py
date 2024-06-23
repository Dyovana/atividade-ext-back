from fastapi import FastAPI, Depends, status

from src.entities.dependent_model import Dependent
from src.models.mysql.connection.mysql_connection import MySqlConnectionHandle

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_db():
    db = MySqlConnectionHandle()
    try:
        yield db
    finally:
        db.close_connection()


@app.post("/register-dependent", status_code=status.HTTP_201_CREATED)
def register_dependent(data: Dependent, service_db: MySqlConnectionHandle = Depends(get_db)):
    service_db.insert_dependent(data)


@app.get("/{cpf_r}")
def get_dependent(cpf_r: str, service_db: MySqlConnectionHandle = Depends(get_db)):
    result = service_db.get_dependent(cpf_r)
    return result


@app.put("/{cpf_r}")
def update_dependent(cpf_r: str, data: dict, service_db: MySqlConnectionHandle = Depends(get_db)):
    service_db.update_dependent(cpf_r, data)
