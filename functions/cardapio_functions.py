import requests
import config
from db.mongo import db
from datetime import datetime
from helpers.exceptions import CustomException
from bson import ObjectId

def cadastro_item_cardapio(nome:str, valor: float, imagem:str, quantidade:int, tipo_alimento:str):

    collection_cardapio = db["cardapio"]


    collection_cardapio.insert_one({
        "nome": nome,
        "valor": "R$ {:.2f}".format(float(valor)),
        "valor_num": float(valor),
        "quantidade": int(quantidade),
        "imagem": imagem,
        "tipo_alimento": tipo_alimento,
        "status": "ativo",
        "data_cadastro": datetime.utcnow()
    })

    return "sucesso"


def listar_todo_cardapio():

    collection_cardapio = db["cardapio"]

    lista = list(collection_cardapio.find({
        "status": "ativo"
    }))

    for i in lista:
        i["_id"] = str(i["_id"])

    return lista

def atualizar_item(nome:str = None, valor = 0, quantidade = 0, id = "", tipo_alimento:str = None):
    collection_cardapio = db["cardapio"]

    if collection_cardapio.find_one({"_id": ObjectId(id)}):
        update = collection_cardapio.update_one({"_id": ObjectId(id)},{"$set": { "nome": nome, "valor": f"R$ {valor:.2f}", "valor_num": float(valor), "quantidade": int(quantidade), "tipo_alimento": tipo_alimento }})

        return "atualizado"
    else:
        return "nao_encontrado"
    
def deletar_item(id:str):
    collection_cardapio = db["cardapio"]

    collection_cardapio.update_one({
        "_id": ObjectId(id)
    },{"$set": {"status": "excluido"}})

    return "OK"


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS