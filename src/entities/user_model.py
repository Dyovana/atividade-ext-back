from pydantic import BaseModel


class User(BaseModel):
    cpf: str
    full_name: str
    phone_number: int
    city: str
    address: str
    email: str


class RegisterUser(User):
    password: str


class Login(BaseModel):
    email: str
    encoded_password: str
