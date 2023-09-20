from flask import Blueprint, json, request, render_template, flash, redirect, url_for
import re
import uuid
from helpers.exceptions import CustomException, LogErroException
import functions.cardapio_functions as cardapio_functions
from helpers.decorators import check_token

cardapio_route = Blueprint('cardapio', __name__)

@cardapio_route.route('/cadastro/cardapio/item', methods=["POST"])
def cadastro_item_cardapio():

    nome = request.form["nome_item"]
    valor = request.form["valor"]
    valor_float = float(valor.replace(".", "").replace(",", "."))

    imagem = request.files["file"]
    tipo_alimento = request.form['tipoAlimento']
    quantidade = request.form["quantidade"]
    quantidade = int(quantidade)
    caminho_imagem = f"static/img/upload/{imagem.filename}"

    if imagem and cardapio_functions.allowed_file(imagem.filename):
        imagem.save(caminho_imagem)

    # if not user_type:
    #     return json.jsonify({ "titulo": "token invalido" }), 403
    
    cadastrar = cardapio_functions.cadastro_item_cardapio(nome=nome, valor=valor_float, imagem=caminho_imagem, quantidade=quantidade, tipo_alimento=tipo_alimento)

    if cadastrar == "sucesso":
        mensagem = 'Cadastrado!'  # Sua mensagem aqui
        flash(mensagem)
        return redirect(url_for('paginas.dashboard'))
    else:
        return json.jsonify({"status": "erro interno"}), 403
    

@cardapio_route.route('/listar/cardapio', methods=["GET"])
def listar_cardapio():

    return json.jsonify({"lista_cardapio": cardapio_functions.listar_todo_cardapio() }), 200

# @cardapio_route.route('/listar/renderizar/cardapio', methods=["GET"])
# @check_token()
# def renderizar_cardapio(token: dict):

#     status = token.get("status", None)

#     if not status:
#         return json.jsonify({ "titulo": "token invalido" }), 403

#     lista = cardapio_functions.listar_todo_cardapio()

#     return render_template('food.html', listar_cardapio = lista)

@cardapio_route.route('/atualizar/cardapio', methods=["POST"])
def atulizar_cardapio():

    nome = request.form["nome_item"]
    valor = request.form["valor"]

    valor_float = float(request.form["valor"].replace(".", "").replace(",", "."))

    quantidade = request.form["quantidade"]
    _id = request.form["id"]
    tipo_alimento = request.form["tipoAlimentoAtt"]

    atualizar = cardapio_functions.atualizar_item(nome=nome, valor=valor_float, quantidade=quantidade, id=_id, tipo_alimento=tipo_alimento)

    if atualizar == "atualizado":
        mensagem = 'Atualizado!'  # Sua mensagem aqui
        flash(mensagem)
        return redirect(url_for('paginas.dashboard'))
    else:
        return 500    

@cardapio_route.route('/deletar', methods=["GET"])
def deletar():

    id = request.args.get("id")

    cardapio_functions.deletar_item(id=id)

    return redirect(url_for('paginas.dashboard'))
