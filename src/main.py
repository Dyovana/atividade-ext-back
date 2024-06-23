import sys
from pathlib import Path

from fastapi import FastAPI
from src.controllers.user import app as user_app
from src.controllers.dependent import app as dependent_app
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/user", user_app)
app.mount("/dependent", dependent_app)

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # endereço frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Métodos HTTP permitidos
    allow_headers=["Content-Type"],  # Headers permitidos
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the main API. Use /user or /dependent for specific operations."}
