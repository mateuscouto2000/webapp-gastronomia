from flask import Blueprint, json, render_template, request
from helpers.decorators import check_token
import functions.pedidos_function as pedidos_function
import functions.usuarios_functions as usuarios_functions

paginas_routes = Blueprint("paginas", __name__)

@paginas_routes.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@paginas_routes.route('/dash', methods=['GET'])
def dashboard():
    dados = pedidos_function.montar_dados_dash()
    return render_template('dashboard.html', dados=dados)

@paginas_routes.route('/food', methods=['GET'])
def food():
    return render_template('food.html')

@paginas_routes.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@paginas_routes.route('/cadastro/adm', methods=['GET'])
def cadastro_adm():
    return render_template('cadastroUserAdm.html')

@paginas_routes.route('/cadastro/usuario', methods=['GET'])
def cadastro_usuario():
    return render_template('cadastroUser.html')

@paginas_routes.route('/atualizar/endereco', methods=['GET'])
def atualizar_endereco():
    return render_template('atualizarEndereco.html') 

@paginas_routes.route('/pagamento', methods=["GET"])
def pagamento():
    return render_template('pagamento.html')

@paginas_routes.route('/recibo', methods=["GET"])
def recibo():
    return render_template('recibo.html')
    
    
    