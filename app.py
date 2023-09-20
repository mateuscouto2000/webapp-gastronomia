from flask import json, Flask
from flask_cors import CORS
import config
from flask_talisman import Talisman
from routes.usuarios_routes import usuarios_routes
from routes.cardapio_route import cardapio_route
from routes.pedidos_route import pedidos_route
from routes.paginas_routes import paginas_routes
from helpers.exceptions import LogErroException

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = '48g5dkit9ru0d6bk7b5eci79z'

## libera cors
CORS(app)

## bloqueia cors nas rotas de controle
# CORS(controle_routes, resources={r"/*": {"origins": "http://127.0.0.1"}})

app.register_blueprint(usuarios_routes, url_prefix="/usuarios")
app.register_blueprint(cardapio_route, url_prefix="/cardapio")
app.register_blueprint(pedidos_route, url_prefix="/pedidos")
app.register_blueprint(paginas_routes, url_prefix="/paginas")

with open('config.json', 'r') as f:
    config.env = json.load(f)
## handler para 404
@app.errorhandler(404)
def handle_not_found(*args):
    return json.jsonify({ "titulo": "recurso nao encontrado" }), 404

@app.errorhandler(LogErroException)
def handle_log_erro(erro):
    return json.jsonify({"titulo": "erro ao registrar log de erro"}), 500

app.register_blueprint(paginas_routes, url_prefix="/")

if __name__ == "__main__":

    if config.env["DEV"] != 1:
        Talisman(app, force_https=False)

    app.secret_key = '48g5dkit9ru0d6bk7b5eci79z'
    app.run(host="0.0.0.0", threaded=True)