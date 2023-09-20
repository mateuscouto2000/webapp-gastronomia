import requests
import config
from db.mongo import db
from datetime import datetime
from helpers.exceptions import CustomException
from werkzeug.security import generate_password_hash, check_password_hash
from helpers.utils import criar_token_de_acesso

def login(email: str, senha: str, adm:str = None):
    collection_usuarios = db['usuarios']

    if adm == "user_adm":
        buscar_email = collection_usuarios.find_one({
            "email": email,
            "adm": True
        })
    else:
        buscar_email = collection_usuarios.find_one({
            "email": email,
            "adm": {"$exists": False}
        })

    if not buscar_email:
        if adm == "user_adm":
            return "Usuario admin não encontrado, por favor tente novamente"
        return "Usuario não encontrado, por favor tente novamente"
    
    senha_hash = buscar_email["senha"]
    validar_senha = check_password_hash(senha_hash, senha)

    if validar_senha and adm == None:

        token = {
            "nome": buscar_email["nome"],
            "email": email,
            "telefone_contato": buscar_email["telefone"],
            "rua": buscar_email["rua"],
            "bairro": buscar_email["bairro"],
            "cidade":buscar_email["cidade"],
            "numero_endereco": buscar_email["numero_endereco"],
            "cep": buscar_email["cep"],
            "user_adm": False,
            "expirado": False,
            "status": "ativo",
            "user_id": str(buscar_email["_id"])
        }

        token_encriptado = criar_token_de_acesso(token)

        return token_encriptado
    
    elif validar_senha and adm == "user_adm":
        token = {
            "nome": buscar_email["nome"],
            "email": email,
            "telefone_contato": buscar_email["telefone"],
            "expirado": False,
            "user_adm": True,
            "status": "ativo",
            "user_id": str(buscar_email["_id"])
        }

        token_encriptado = criar_token_de_acesso(token)

        return token_encriptado
    
    else:
        return "Usuario ou senha invalido, tente nomente."
    
def login_adm(email: str, senha: str):
    collection_usuarios = db['usuarios']

    buscar_email = collection_usuarios.find_one({
        "email": email
    })

    if not buscar_email:
        return "usuario não encontrado"
    
    if check_password_hash(buscar_email['senha'], senha):

        token = {
            "nome": buscar_email["nome"],
            "email": email,
            "expirado": False,
            "status": "ativo",
            "adm": True,
            "user_id": buscar_email["_id"]
        }

        token_encriptado = criar_token_de_acesso(token)

        return token_encriptado
    
def registrar_novo_usuario(email:str, senha:str, nome:str, rua:str, numero_endereco:str, cep:str, bairro:str, cidade:str, telefone:str):

    senha = generate_password_hash(senha,method='pbkdf2:sha256', salt_length=8)
    collection_usuarios = db['usuarios']

    buscar = collection_usuarios.find_one({
        "email": email
    })

    if buscar:
        return "email ja cadastrado"
    
    salvar = collection_usuarios.insert_one({
        "email": email,
        "nome": nome,
        "senha": senha,
        "rua": rua,
        "bairro": bairro,
        "cidade":cidade,
        "numero_endereco": numero_endereco,
        "cep": cep,
        "telefone": telefone
    })

    return "sucesso"

def registrar_novo_usuario_adm(email:str, senha:str, nome:str, telefone:str):

    senha = generate_password_hash(senha,method='pbkdf2:sha256', salt_length=8)
    collection_usuarios = db['usuarios']

    buscar = collection_usuarios.find_one({
        "email": email
    })

    if buscar:
        return "email ja cadastrado"
    
    salvar = collection_usuarios.insert_one({
        "email": email,
        "nome": nome,
        "senha": senha,
        "telefone": telefone,
        "adm": True
    })

    return "sucesso"


def atualizar_endereco(rua:str, bairro:str, cidade:str, numero:str, usuario:str, cep:str):
    collection_usuarios = db['usuarios']

    atualizar = collection_usuarios.update_one({
        "email":usuario
    },{"$set": {
        "rua": rua,
        "bairro": bairro,
        "cidade": cidade,
        "cep": cep,
        "numero_endereco": numero
    }})

    return "OK"


def exibir_endereco(usuario:str):
    collection_usuarios = db["usuarios"]

    buscar_dados_usuario = collection_usuarios.find_one({
        "email": usuario
    })

    dados = {
        "rua": buscar_dados_usuario["rua"],
        "cep": buscar_dados_usuario["cep"],
        "bairro": buscar_dados_usuario["bairro"],
        "cidade": buscar_dados_usuario["cidade"],
        "numero_endereco": buscar_dados_usuario["numero_endereco"],
    }

    return dados