from helpers.exceptions import CustomException
from cryptography.fernet import Fernet
from functools import wraps
from flask import json, request
import config

def check_token(opcional = False):

    def wrapper(funcao_original):
        @wraps(funcao_original)
        def decorated(*args, **kwargs):

            token: str = request.headers.get("Authorization")
            token_dict = None
            if not token:
                if opcional:
                    return funcao_original(None)
                else:
                    raise CustomException("token ausente", status_code=401)

            segredo: str = config.env["SEGREDO"]

            fernet = Fernet(segredo)
        
            if token:

                token_bytes = token.encode()
                
                try:
                    token_dict_string = fernet.decrypt(token_bytes).decode("utf-8")
                except:
                    raise CustomException("token invalido", status_code=401)

                token_dict = json.loads(token_dict_string)
                
            return funcao_original(token_dict)

        return decorated
    
    return wrapper
