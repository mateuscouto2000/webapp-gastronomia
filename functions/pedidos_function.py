import requests
import config
from db.mongo import db
from datetime import datetime
from helpers.exceptions import CustomException
from bson.objectid import ObjectId

def fazer_pedido(nome:str, telefone_contato: str, user_id: str, item_id: str, quantidade_item_pedido:int, mesa: int = 0, entrega:bool = False, novo_endereco:bool = False, rua:str = "", cep:str = "", numero_endereco:str = "", bairro: str = "", cidade: str = ""):

    collection_controle_pedidos = db["controle_pedidos"]
    collection_cardapio = db["cardapio"]
    collection_usuario = db["usuarios"]

    buscar_dados_usuario = collection_usuario.find_one({
        "_id": ObjectId(user_id)
    })

    buscar_dados_usuario['_id'] = str(buscar_dados_usuario['_id'])

    buscar_item_cardapio = collection_cardapio.find_one({
        "_id": ObjectId(item_id)
    })

    buscar_item_cardapio['_id'] = str(buscar_item_cardapio['_id'])

    quantidade = buscar_item_cardapio["quantidade"]

    if entrega:
        if novo_endereco:
            if quantidade > 0:
                registrar_pedido = collection_controle_pedidos._insert_one({
                    "nome_usuario": nome,
                    "usuario_id": buscar_dados_usuario['_id'],
                    "rua_entrega": rua,
                    "cep_entrega": cep,
                    "bairro": bairro,
                    "cidade": cidade,
                    "numero_endereco_entrega": numero_endereco,
                    "telefone_contato": telefone_contato,
                    "item_cardapio": buscar_item_cardapio,
                    "quantidade_item_pedido": quantidade_item_pedido,
                    "data_pedido": datetime.utcnow(),
                    "data_pedido_finalizado": "",
                    "dados_usuario": buscar_dados_usuario,
                    "finalizado": False,
                    "comer_no_local": False,
                    "pago": False
                })
                quantidade = quantidade - quantidade_item_pedido
                collection_cardapio.update_one({
                    "_id": ObjectId(item_id)
                },{"$set": {"quantidade": quantidade }})
                
                return "sucesso"
            else:
                return "acabou"
        else:

            if quantidade > 0:
                registrar_pedido = collection_controle_pedidos._insert_one({
                    "nome_usuario": nome,
                    "usuario_id": buscar_dados_usuario['_id'],
                    "rua_entrega": buscar_dados_usuario["rua"],
                    "cep_entrega": buscar_dados_usuario["cep"],
                    "bairro": buscar_dados_usuario["bairro"],
                    "cidade": buscar_dados_usuario["cidade"],
                    "numero_endereco_entrega": buscar_dados_usuario["numero_endereco"],
                    "telefone_contato": telefone_contato,
                    "item_cardapio": buscar_item_cardapio,
                    "quantidade_item_pedido": quantidade_item_pedido,
                    "data_pedido": datetime.utcnow(),
                    "data_pedido_finalizado": "",
                    "dados_usuario": buscar_dados_usuario,
                    "finalizado": False,
                    "comer_no_local": False,
                    "pago": False
                })

                quantidade = quantidade - quantidade_item_pedido
                collection_cardapio.update_one({
                    "_id": ObjectId(item_id)
                },{"$set": {"quantidade": quantidade }})

                return "sucesso"
            else:
                return "acabou"
            
    else:
        if quantidade > 0:
            registrar_pedido = collection_controle_pedidos.insert_one({
                "nome_usuario": nome,
                "usuario_id": buscar_dados_usuario['_id'],
                "telefone_contato": telefone_contato,
                "item_cardapio": buscar_item_cardapio,
                "quantidade_item_pedido": quantidade_item_pedido,
                "data_pedido": datetime.utcnow(),
                "data_pedido_finalizado": "",
                "dados_usuario": buscar_dados_usuario,
                "mesa": mesa,
                "finalizado": False,
                "comer_no_local": True,
                "pago": False
            })

            quantidade = quantidade - quantidade_item_pedido
            collection_cardapio.update_one({
                "_id": ObjectId(item_id)
            },{"$set": {"quantidade": quantidade }})

            return "sucesso"
        else:
            return "acabou"

def parse_float_with_comma(value):
    cleaned_value = str(value).replace(',', '.')  # Convertemos para string e depois substituímos a vírgula por ponto
    return float(cleaned_value) if cleaned_value else 0.0
        
def montar_dados_dash():
    collection_controle_pedidos = db["controle_pedidos"]
    collection_cardapio = db["cardapio"]
    collection_usuario = db["usuarios"]

    quantide_pendentes_comer_no_local = 0
    quantide_pendentes_para_entrega = 0
    total_finalizados = 0
    total_pagos = 0

    # pipeline = [
    # {
    #     "$match": {
    #         "finalizado": True,
    #         "pago": False
    #     }
    # },
    # {
    #     "$group": {
    #         "_id": "$cliente_id",
    #         "usuario_id": { "$first": "$usuario_id" },
    #         "cliente": { "$first": "$nome_usuario" },
    #         "mesa": { "$first": "$mesa" },  # Adiciona a mesa como parte do resultado do grupo
    #         "nomes_itens": { "$addToSet": "$item_cardapio.nome" },
    #         "valor_total_cliente": {
    #             "$sum": {
    #                 "$multiply": [
    #                     {
    #                         "$toDouble": "$item_cardapio.valor_num"
    #                     },
    #                     "$quantidade_item_pedido"
    #                 ]
    #             }
    #         }
    #     }
    # }
    # ]

    pipeline = [
    {
        "$match": {
            "finalizado": True,
            "pago": False
        }
    },
    {
        "$group": {
            "_id": "$usuario_id",
            "cliente": { "$first": "$nome_usuario" },
            "mesa": { "$first": "$mesa" },
            "nomes_itens": { "$addToSet": "$item_cardapio.nome" },
            "valor_total_cliente": {
                "$sum": {
                    "$multiply": [
                        {
                            "$toDouble": "$item_cardapio.valor_num"
                        },
                        "$quantidade_item_pedido"
                    ]
                }
            }
            # "usuario_id": { "$usuario_id" }
            # "usuario_id": { "$first": "$usuario_id" }
        }
    }
    ]
    pedidos_para_pagar = list(collection_controle_pedidos.aggregate(pipeline))

    for p in pedidos_para_pagar:
        p["_id"] = str(p["_id"])
        p["nomes_itens_formatado"] = ', '.join(p["nomes_itens"])

    pedidos_finalizados = list(collection_controle_pedidos.find({
        "finalizado": True
    }))

    total_finalizados = len(pedidos_finalizados)

    pedidos_pagos = list(collection_controle_pedidos.find({
        "pago": True
    }))

    total_pagos = len(pedidos_pagos)

    valor_total_faturado = 0

    # for doc in pedidos_pagos:
    #     valor_total_faturado = valor_total_faturado + float(doc['item_cardapio']['valor_num']) * doc["quantidade_item_pedido"]

    for doc in pedidos_pagos:
        valor_num = doc['item_cardapio']['valor_num']
        quantidade_item_pedido = doc['quantidade_item_pedido']
        
        try:
            valor_num_float = parse_float_with_comma(valor_num)
            valor_total_faturado += valor_num_float * quantidade_item_pedido
        except ValueError:
            return 'BUG'
        
    valor_total_faturado = round(valor_total_faturado, 2);

    pedidos_pendentes_para_entrega = list(collection_controle_pedidos.find({
        "finalizado": False,
        "comer_no_local": False
    }))

    for p in pedidos_pendentes_para_entrega:
        p["_id"] = str(p["_id"])
        p["item_cardapio"]["_id"] = str(p["item_cardapio"]["_id"])
        p["dados_usuario"]["_id"] = str(p["dados_usuario"]["_id"])

    quantide_pendentes_para_entrega = len(pedidos_pendentes_para_entrega)

    pedidos_pendentes_para_comer_no_local = list(collection_controle_pedidos.find({
        "finalizado": False,
        "comer_no_local": True
    }))

    for pe in pedidos_pendentes_para_comer_no_local:
        pe["_id"] = str(pe["_id"])
        pe["item_cardapio"]["_id"] = str(pe["item_cardapio"]["_id"])
        pe["dados_usuario"]["_id"] = str(pe["dados_usuario"]["_id"])

    quantide_pendentes_comer_no_local = len(pedidos_pendentes_para_comer_no_local)

    itens_ativos_no_cardapio = collection_cardapio.count_documents({
        "status": "ativo"
    })

    todo_cardapio = list(collection_cardapio.find({'status':'ativo'}))

    for i in todo_cardapio:
        i["_id"] = str(i["_id"])

    total_pendetes = quantide_pendentes_comer_no_local + quantide_pendentes_para_entrega

    dados = {
        "pedidos_pendentes_para_entrega": pedidos_pendentes_para_entrega,
        "pedidos_pendentes_para_comer_no_local": pedidos_pendentes_para_comer_no_local,
        "quantide_pendentes_para_entrega": quantide_pendentes_para_entrega,
        "quantide_pendentes_para_comer_no_local": quantide_pendentes_comer_no_local,
        "itens_ativos_no_cardapio": itens_ativos_no_cardapio,
        "total_pendentes": total_pendetes,
        "todo_cardapio": todo_cardapio,
        "total_finalizados": total_finalizados,
        "total_pagos": total_pagos,
        "total_faturado": valor_total_faturado,
        "pedidos_para_pagar": pedidos_para_pagar
    }

    return dados

def finalizar_pedido(id):
    collection_controle_pedidos = db["controle_pedidos"]

    finalizar = collection_controle_pedidos.update_one({"_id": ObjectId(id)},{"$set": {"finalizado": True, "data_pedido_finalizado": datetime.utcnow()}})

    return "OK"

def pagar_pedidosuser(userId: str):
    try:
        collection_controle_pedidos = db["controle_pedidos"]

        buscar_pendentes_pagamento = list(collection_controle_pedidos.update_many({
            'usuario_id': userId,
            'pago': False
        },{'$set':{
            'pago': True
        }}))

        return "OK"
    except Exception as e:
        return f"Erro: {str(e)}"

def montarRecibo(userID:str, nome:str):

    collection_controle_pedidos = db["controle_pedidos"]

    buscar_pendentes_pagamento = list(collection_controle_pedidos.find({
        'usuario_id': userID,
        'pago': False
    }))

    doc_retorno = {}
    lista_itens = []
    total = 0

    for doc in buscar_pendentes_pagamento:
        doc['_id'] = str(doc['_id'])
        doc['data_pedido_str'] = doc['data_pedido'].strftime("%d/%m/%Y")
        total = total + float(doc['item_cardapio']['valor_num']) * doc["quantidade_item_pedido"]

    total = round(total, 2)

    for doc in buscar_pendentes_pagamento:
        doc['valor_total'] = total
        
        doc['valor_total_str'] = f'R$ {str(total)}'

    if len(buscar_pendentes_pagamento) > 0:
        return buscar_pendentes_pagamento
    else:
        return "Sem pedidos pendentes de pagamento"
    
def processar_pagamento(tipoPagamento:str, cardNumero:str, cardNome:str, mes:str, ano:str, cvc:str, userId:str, nomeUser:str):

    collection_controle_pedidos = db["controle_pedidos"]

    # aqui entra a lógica de pagamentos

    buscar_pendentes_pagamento = list(collection_controle_pedidos.update_many({
        'usuario_id': userId,
        'pago': False
    },{'$set':{
        'pago': True
    }}))

    return 'pago'

def validar_pedido_existe(id:str, nome:str):

    collection_controle_pedidos = db["controle_pedidos"]

    buscar = list(collection_controle_pedidos.find({
        "usuario_id": id
    }))

    if buscar:
        return "ok"
    else:
        return "nao existe"
