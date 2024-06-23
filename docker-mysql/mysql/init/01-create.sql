create database atividade_extensionista;

CREATE TABLE atividade_extensionista.dependente (
    id_dependente INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150),
    cpf_responsavel VARCHAR(11) NOT NULL,
    description VARCHAR(350)
) DEFAULT CHARSET=utf8;

CREATE TABLE atividade_extensionista.usuario (
    cpf VARCHAR(11) PRIMARY KEY,
    full_name VARCHAR(150),
    phone_number VARCHAR(20),
    city VARCHAR(100),
    address VARCHAR(150) NULL,
    email VARCHAR(150),
    password VARCHAR(100)
) DEFAULT CHARSET=utf8;