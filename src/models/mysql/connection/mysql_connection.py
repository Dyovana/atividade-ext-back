from typing import Optional
from fastapi import HTTPException
import mysql.connector

from src.entities.dependent_model import Dependent
from src.entities.user_model import User


class MySqlConnectionHandle:

    def __init__(self):
        self.__connection = mysql.connector.connect(
            user='root',
            password='password',
            host='localhost',
            port='3306',
            database='atividade_extensionista'
        )

        print("DB connected")
        self.__cursor = self.__connection.cursor()

    def execute_sql_transaction(self, sql, values):
        try:
            self.__cursor.execute(sql, values)
            self.__connection.commit()
            print("successfully")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.__connection.rollback()
            raise HTTPException(status_code=500, detail=err)

    def insert_user(self, user: User):
        sql = """
            INSERT INTO usuario (cpf, full_name, phone_number, city, address, email, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user.cpf,
            user.full_name,
            user.phone_number,
            user.city,
            user.address,
            user.email,
            user.password
        )

        self.execute_sql_transaction(sql, values)

    def get_user(self, email: str, encoded_password: str) -> Optional[User]:
        sql = """
            SELECT cpf, full_name, phone_number, city, address, email
            FROM usuario
            WHERE email = %s AND password = %s
        """
        try:
            self.__cursor.execute(sql, (email, encoded_password))
            result = self.__cursor.fetchone()
            if result:
                user = User(
                    cpf=result[0],
                    full_name=result[1],
                    phone_number=result[2],
                    city=result[3],
                    address=result[4],
                    email=result[5],
                )
                return user
            else:
                raise HTTPException(status_code=404, detail="Item not found")

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=err)

    def update_user(self, cpf, fields_to_update):
        sql = "UPDATE usuario SET "
        values = []
        for key, value in fields_to_update.items():
            sql += f"{key} = %s, "
            values.append(value)
        sql = sql[:-2]  # Remove a última vírgula e espaço extra
        sql += " WHERE cpf = %s"
        values.append(cpf)

        self.execute_sql_transaction(sql, tuple(values))

    def insert_dependent(self, dep: Dependent):
        sql = """
            INSERT INTO dependente (cpf_responsavel, name, description)
            VALUES (%s, %s, %s)
        """
        values = (
            dep.cpf_responsavel,
            dep.name,
            dep.description
        )

        self.execute_sql_transaction(sql, values)

    def get_dependent(self, cpf_r: str) -> Optional[Dependent]:
        sql = """
            SELECT name, cpf_responsavel, description
            FROM dependente
            WHERE cpf_responsavel = %s
        """
        try:
            self.__cursor.execute(sql, (cpf_r,))
            result = self.__cursor.fetchone()
            if result:
                dependent = Dependent(
                    name=result[0],
                    cpf_responsavel=result[1],
                    description=result[2],
                )
                return dependent
            else:
                raise HTTPException(status_code=404, detail="Item not found")

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=err)

    def update_dependent(self, cpf_r, fields_to_update):
        sql = "UPDATE dependente SET "
        values = []
        for key, value in fields_to_update.items():
            sql += f"{key} = %s, "
            values.append(value)
        sql = sql[:-2]  # Remove a última vírgula e espaço extra
        sql += " WHERE cpf_responsavel = %s"
        values.append(cpf_r)

        self.execute_sql_transaction(sql, tuple(values))

    def get_all_info(self, cpf):
        final_result = {}
        sql = """
            SELECT cpf, full_name, phone_number, city, address, email
            FROM usuario
            WHERE cpf = %s
        """

        try:
            self.__cursor.execute(sql, (cpf, ))
            result = self.__cursor.fetchone()
            if result:
                user = User(
                    cpf=result[0],
                    full_name=result[1],
                    phone_number=result[2],
                    city=result[3],
                    address=result[4],
                    email=result[5],
                )
                final_result["user"] = user
            else:
                raise HTTPException(status_code=404, detail="Item not found")

            final_result["dependent"] = self.get_dependent(cpf)

            return final_result

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=err)

    def close_connection(self):
        self.__cursor.close()
        self.__connection.close()
        print("DB connection closed")
