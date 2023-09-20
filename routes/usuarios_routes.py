from flask import Blueprint, json, render_template, request, redirect, url_for
import re
import uuid
from helpers.exceptions import CustomException, LogErroException
import functions.usuarios_functions as usuarios_functions
import functions.pedidos_function as pedidos_function
from helpers.decorators import check_token

usuarios_routes = Blueprint('usuarios', __name__)

@usuarios_routes.route('/login', methods=["POST"])
def login():
    
    email = request.json.get("email", None)
    senha = request.json.get("senha", None)
    tipo_usuario = request.json.get("inputTipo", None)

    # email = request.form["email"]
    # senha = request.form["senha"]
    # tipo_usuario = request.form["tipo_usuario"]

    if not (email and senha):
        raise CustomException(status_code=400, titulo="campos faltando") 
    
    token = usuarios_functions.login(email=email, senha=senha, adm=tipo_usuario)

    if "Usuario admin não encontrado, por favor tente novamente" in token or "Usuario não encontrado, por favor tente novamente" in token or "Usuario ou senha invalido, tente nomente." in token:
        return json.jsonify({"mensagem": token}), 404
    
    if tipo_usuario == "user_adm":
        buscar_dados_montar_dash = pedidos_function.montar_dados_dash()
        return {'token': token, 'dados_montar_dash': buscar_dados_montar_dash}
    else:
        return json.jsonify({"token": token}), 200
    
    #return render_template("dashboard.html")
@usuarios_routes.route('/dashboard', methods=["GET"])
def renderizar_dashboard(dados):
    return render_template("dashboard.html", dados=dados)

@usuarios_routes.route('/login/adm', methods=["POST"])
def login_adm():
    email = request.json.get("email", None)
    senha = request.json.get("senha", None)

    if not (email and senha):
        raise CustomException(status_code=400, titulo="campos faltando") 
    
    token = usuarios_functions.login_adm(email=email, senha=senha)

    if "usuario não encontrado" in token:
        return json.jsonify({"mensagem": token}), 404

    return json.jsonify({"token": token}), 200

@usuarios_routes.route('/registrar/usuario', methods=["POST"])
def registrar_usuario():

    email = request.json.get("email", None)
    senha = request.json.get("senha", None)
    nome = request.json.get("nome", None)

    rua = request.json.get("rua", None)
    cep = request.json.get("cep", None)
    numero_endereco = request.json.get("numero_endereco", None)
    bairro = request.json.get("bairro", None)
    cidade = request.json.get("cidade", None)

    telefone = request.json.get("telefone", None)

    if not (email and senha and nome and rua and cep and telefone and numero_endereco):
        return json.jsonify({ "mensagem": "campos faltando" }), 403

    # if not (email or senha or nome or rua or cep or telefone or numero_endereco):
    #     return json.jsonify({ "mensagem": "campos faltando" }), 403
    
    if bool(re.match(r"\d{5}-?\d{3}", cep)) == False:
        return json.jsonify({ "mensagem": "cep invalido" }), 403
    
    registrar = usuarios_functions.registrar_novo_usuario(
        nome=nome,
        email=email,
        senha=senha,
        rua=rua,
        cep=cep,
        bairro=bairro,
        cidade=cidade,
        telefone=telefone,
        numero_endereco=numero_endereco
    )

    if "email ja cadastrado" in registrar:
        return json.jsonify({"mensagem": "email ja cadastrado"}), 404
    
    if "sucesso" in registrar:
        return json.jsonify({"status": "sucesso"}), 200
    
@usuarios_routes.route('/registrar/usuario/adm', methods=["POST"])
def registrar_usuario_adm():

    email = request.json.get("email", None)
    senha = request.json.get("senha", None)
    nome = request.json.get("nome", None)
    telefone = request.json.get("telefone", None)
    
    if not (email and senha and nome and telefone):
        return json.jsonify({ "mensagem": "campos faltando" }), 403
    
    registrar = usuarios_functions.registrar_novo_usuario_adm(
        nome=nome,
        email=email,
        senha=senha,
        telefone=telefone
    )

    if "email ja cadastrado" in registrar:
        return json.jsonify({"mensagem": "email ja cadastrado"}), 404
    
    if "sucesso" in registrar:
        return json.jsonify({"status": "sucesso"}), 200
    
@usuarios_routes.route('/atualizar/dados', methods=["POST"])
@check_token()
def atualizar_dados(token:dict):
    if not token:
        return json.jsonify({"mensagem": "usuario não está logado"})
    
    rua = request.json.get("rua", None)
    bairro = request.json.get("bairro", None)
    cidade = request.json.get("cidade", None)
    numero = request.json.get("numero", None)
    cep = request.json.get("cep", None)
    usuario = token.get("email", None)

    if rua == None or bairro == None or cidade == None or numero == None:
        return json.jsonify({"mensagem": "campos digitados estão invalidos"})
    
    atualizar = usuarios_functions.atualizar_endereco(rua=rua, bairro=bairro, cidade=cidade, numero=numero, usuario=usuario, cep=cep)

    if atualizar == "OK":
        return json.jsonify({"sucesso": "atualizado"})
    else:
        return json.jsonify({"mensagem": atualizar})
    
@usuarios_routes.route('/buscar/endereco', methods=["POST"])
@check_token()
def buscar_endereco(token:dict):

    if not token:
        return json.jsonify({"mensagem": "usuario não está logado"})
    
    usuario = token.get("email", None)

    dados = usuarios_functions.exibir_endereco(usuario)
    
    return json.jsonify({"dados": dados}), 200
    # return json.jsonify({"sucesso": "atualizado"})
