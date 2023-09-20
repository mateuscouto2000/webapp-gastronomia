from flask import Blueprint, json, request, redirect, url_for
import re
import uuid
from helpers.exceptions import CustomException, LogErroException
import functions.pedidos_function as pedidos_function
from helpers.decorators import check_token

pedidos_route = Blueprint('pedidos', __name__)

@pedidos_route.route('/cadastro/pedido', methods=["POST"])
@check_token()
def cadastrar_pedido(token: dict):
    if not token:
        return json.jsonify({ "titulo": "token invalido" }), 403
    
    nome = token.get("nome", None)
    telefone_contato = token.get("telefone_contato", None)
    user_id = token.get("user_id", None)

    item_id = request.json.get("item_id", None)
    mesa = request.json.get("mesa",None)
    entrega = request.json.get("entrega", False)
    quantidade = request.json.get("quantidade_item", None)

    if not (nome and item_id):
        raise CustomException("token invalido", status_code=403)

    if entrega == True:
        novo_endereco = request.json.get("novo_endereco", False)

        if novo_endereco == True:
            rua = request.json.get("rua", None)
            cep = request.json.get("cep", None)
            numero_endereco = request.json.get("numero_endereco", None)

            if not (rua and cep and numero_endereco):
                raise CustomException(status_code=400, titulo="campos faltando") 

            fazer_pedido = pedidos_function.fazer_pedido(
                nome=nome,
                telefone_contato=telefone_contato,
                user_id=user_id,
                item_id=item_id,
                entrega=entrega,
                novo_endereco=novo_endereco,
                quantidade_item_pedido=quantidade,
                rua=rua,
                cep=cep,
                numero_endereco=numero_endereco
            )

        else:
            fazer_pedido = pedidos_function.fazer_pedido(
                nome=nome,
                telefone_contato=telefone_contato,
                quantidade_item_pedido=quantidade,
                user_id=user_id,
                item_id=item_id,
                entrega=entrega
            )

    else:
        fazer_pedido = pedidos_function.fazer_pedido(
            nome=nome,
            telefone_contato=telefone_contato,
            quantidade_item_pedido=int(quantidade),
            user_id=user_id,
            item_id=item_id,
            mesa=mesa
        )

    if fazer_pedido == "sucesso":
        return json.jsonify({"status":"sucesso"}), 200
    else:
        return json.jsonify({"status": "acabou"}), 403

    
@pedidos_route.route('/finalizar', methods=["GET"])
def finalizar_pedido():
    id = request.args.get("id")

    finalizar = pedidos_function.finalizar_pedido(id)

    return redirect(url_for('paginas.dashboard'))

@pedidos_route.route('/pagarusuario', methods=["GET"])
def pagar_pedidoscliente():
    id = request.args.get("id")

    pagarusuario = pedidos_function.pagar_pedidosuser(id)

    return redirect(url_for('paginas.dashboard'))

@pedidos_route.route('/listar/recibo', methods=["GET"])
@check_token()
def recibo(token:dict):
    if not token:
        return json.jsonify({ "titulo": "token invalido" }), 403
    
    nome = token.get("nome", None)
    user_id = token.get("user_id", None)

    montar_recibo = pedidos_function.montarRecibo(userID=user_id, nome=nome)

    if "Sem pedidos pendentes de pagamento" in montar_recibo:
        return {'mensagem': montar_recibo}
    
    return {'dados': montar_recibo}


@pedidos_route.route('/total/pagar', methods=["GET"])
@check_token()
def total_a_pagar(token:dict):
    nome = token.get("nome", None)
    user_id = token.get("user_id", None)

    montar_recibo = pedidos_function.montarRecibo(userID=user_id, nome=nome)

    if "Sem pedidos pendentes de pagamento" in montar_recibo:
        return {'mensagem': montar_recibo}
    
    return {'total': montar_recibo[0]['valor_total_str']}


@pedidos_route.route('/processar/pagamento', methods=["GET"])
@check_token()
def pagamento(token:dict):

    if not token:
        return json.jsonify({ "titulo": "token invalido" }), 403
    
    nome = token.get("nome", None)
    user_id = token.get("user_id", None)

    tipoPagamento = request.json.get("tipoPagamento", None)
    cardNumero = request.json.get("cardNumero",None)
    cardNome = request.json.get("cardNome", False)
    mes = request.json.get("mes", None)
    ano = request.json.get("ano",None)
    cvc = request.json.get("cvc", False)

    if tipoPagamento == None or cardNumero == None or cardNome == None or mes == None or ano == None or cvc == None:
        return {'mensagem': 'Campos invalidos.'}
    
    processar_pagamento = pedidos_function.processar_pagamento(tipoPagamento=tipoPagamento, cardNumero=cardNumero, cardNome=cardNome, mes=mes, ano=ano, cvc=cvc, userId=user_id, nomeUser=nome)

    if processar_pagamento == "pago":
        return {"finalizado": True}, 200
    else:
        return {'mensagem': processar_pagamento}
    
@pedidos_route.route('/validar/pedido', methods=["GET"])
@check_token()
def validar_pedidos(token:dict):

    if not token:
        return json.jsonify({ "titulo": "token invalido" }), 403
    
    nome = token.get("nome", None)
    user_id = token.get("user_id", None)

    validar = pedidos_function.validar_pedido_existe(id=user_id, nome=nome)

    return {"status":validar}
