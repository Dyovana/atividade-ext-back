from fastapi import FastAPI, Depends, status

from src.entities.user_model import RegisterUser
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


@app.post("/register-user", status_code=status.HTTP_201_CREATED)
def register_user(data: RegisterUser, service_db: MySqlConnectionHandle = Depends(get_db)):
    service_db.insert_user(data)


@app.get("/info")
def get_user(email: str, encoded_password, service_db: MySqlConnectionHandle = Depends(get_db)):
    result = service_db.get_user(email, encoded_password)
    return result


@app.put("/{cpf}")
def update_user(cpf: str, data: dict, service_db: MySqlConnectionHandle = Depends(get_db)):
    service_db.update_user(cpf, data)


@app.get("/all-info/{cpf}")
def get_all_info(cpf: str, service_db: MySqlConnectionHandle = Depends(get_db)):
    result = service_db.get_all_info(cpf)
    return result
