from cryptography.fernet import Fernet
from werkzeug.datastructures import FileStorage
import config
import json

def criar_token_de_acesso(payload: dict):
    segredo: str = config.env["SEGREDO"]

    segredo_bytes = segredo.encode()

    fernet = Fernet(segredo_bytes)

    token_bytes = json.dumps(payload).encode()

    token_encriptado = fernet.encrypt(token_bytes)

    return token_encriptado.decode("utf-8")
