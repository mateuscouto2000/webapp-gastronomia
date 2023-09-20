// Obtém a referência do elemento HTML do contador
const contadorElemento = document.getElementById('count_carrinho');

let contador = 0;
let listaPedido = [];
let listaNomesPedidos = [];
let docNomesItensSelecionados = [];

function addCountCarrinho(id, nome) {
    const botaoElemento = document.getElementById('addCount');
    if (botaoElemento) {

        item_quantidade = document.getElementById("quantidade"+nome).value;
        contador = parseInt(contador) + parseInt(item_quantidade);

        listaPedido.push(id)
        listaNomesPedidos.push(nome)

        docNomesItensSelecionados.push({
            "id":id,
            "nome": nome,
            "quantidade":item_quantidade
        });

        contadorElemento.textContent = contador;
    }
}

function delete_item_lista(nome, quantidade, _id) {

    if (quantidade === "1") {
        docNomesItensSelecionados.splice(_id, 1);
    }else{
        for (i = 0; i < docNomesItensSelecionados.length; i++) {
            if (docNomesItensSelecionados[i]["id"] == id){
                docNomesItensSelecionados[i]["quantidade"] = quantidade-1
                break;
            }
        }
    }

    contador = contador - 1;
    const botaoElemento = document.getElementById('addCount');
    if (botaoElemento) {

        if (contador < 0){
            contadorElemento.textContent = contador;
        }
        else{
            contadorElemento.textContent = contador;
        }
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

usuarioLogado = getCookie('usuarioLogado')
validar_usuario(usuarioLogado)
function validar_usuario(usuarioLogado) {
    if (!usuarioLogado) {
        window.location = '/'
    }
}

function fazerPedido() {

    var postControlePedidos = async (usuarioLogado, id, qnt, mesa, entrega) => {
        await fetch('http://127.0.0.1:5000/pedidos/cadastro/pedido', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': usuarioLogado
            },
            body: JSON.stringify({ item_id: id, quantidade_item: qnt, mesa: mesa, entrega: entrega })
        })
            .then(resultado => resultado.json())
            .then(resultado => {

                if (resultado.status == "sucesso") {
                    alert("Pedido feito!")
                }
                else if (resultado.status == "acabou") {
                    alert("Infelizmente esse item está em falta")
                }
            })

    }

    const local = document.getElementById('local');

    let entrega = true;
    let mesa = "";

    if (local.checked) {
        entrega = false;
        mesa = document.getElementById('mesa').value;
    }

    for (i = 0; i < docNomesItensSelecionados.length; i++) {
        id = docNomesItensSelecionados[i]["id"]
        var qnt = docNomesItensSelecionados[i]["quantidade"]
        postControlePedidos(usuarioLogado, id, qnt, mesa, entrega)
    }
}

function renderizarEdicoes(response) {

    const divContent = document.getElementById('foods');
    let html = '';

    for (i = 0; i < response.length; i++) {
        nome = response[i]['nome']
        valor = response[i]['valor']
        imagem = response[i]['imagem']
        tipoAlimento = response[i]['tipo_alimento']
        id = response[i]['_id']
        var classe = `food mix col ${tipoAlimento}`

        if (tipoAlimento == "bebida") {
            tipoAlimento = "sets"

        }

        html += `
            <div class="food mix col ${tipoAlimento}">
                <a href="#${id}">
                    <div class="food-picture">
                        <img src="${imagem}" style="border-radius: 30px;"
                            height="181" width="250" />
                    </div>
                </a>
                <div class="food-name">
                    <h3>${nome}</h3>
                    <h4 class="sub-title">${valor}</h4>
                    <!--
                        <a href="#" id='addCount' onclick="addCountCarrinho('${id}')">
                            <div class="button" style="align-items: center;">+1 no carrinho</div>
                        </a>
                    -->
                </div>
            </div>


            <div id="${id}" class="modal_cadastro">
                <div class="content">
                    <h2>Selecione a quantidade</h2>
                    <form id="cadastroPedido">
                        <input type="number" id="quantidade${nome}" name="quantidade" value="1">
                        <a href="#" id='addCount' onclick="addCountCarrinho('${id}', '${nome}')" class="footer-btn-close">
                            Cadastrar item
                        </a><br><br>
                    </form>
                    <a href="#" class="close">&times;</a>
                </div>
            </div>
        `;
    }
    divContent.innerHTML = html;

}


function renderizarListaSelecionados() {

    if (contador > 0){
        document.getElementById("demo-modal-lista").style.display = "flex";
        const selecionados = document.getElementById('selecionados');
        let html = '';

        if (listaNomesPedidos.length > 0) {

            for (i = 0; i < docNomesItensSelecionados.length; i++) {
                nome = docNomesItensSelecionados[i]["nome"]
                quantidade = docNomesItensSelecionados[i]["quantidade"]
                id = docNomesItensSelecionados[i]["id"]

                html += `
                    <tr>
                        <td>
                            <p> <strong>${nome}</strong> x${quantidade}</p>
                        </td>
                        <td>
                            <a href="#" onclick="delete_item_lista('${nome}','${quantidade}','${id}')">
                                <img width="30" height="30" src="https://img.icons8.com/ios-glyphs/30/delete-forever.png" alt="delete-forever"/>
                            </a>
                        </td>
                    </tr>
                `;
            }
        }

        selecionados.innerHTML = html;

    }
    else{
        document.getElementById("demo-modal-lista").style.display = "none";
        alert("Você precisa selecionar um ou mais itens do cardapio.")
    }
}

function validarContador(){
    if (contador > 0){
        document.getElementById("demo-modal").style.display = "flex";
    }else{
        alert("Você precisa selecionar um ou mais itens do cardapio.")
    }
}

function validarContadorRecibo(){
    // if (contador > 0){
    //     document.getElementById("demo-modal").style.display = "flex";
    //     window.location = '/recibo'
    // }else{
    //     alert("Você precisa selecionar um ou mais intens do cardapio.")
    // }

    var validar_pedidos = async () => {
        await fetch('http://127.0.0.1:5000/pedidos/validar/pedido', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': usuarioLogado
            }
        })
            .then(resultado => resultado.json())
            .then(resultado => {

                if (resultado.status == "ok") {
                    document.getElementById("demo-modal").style.display = "flex";
                    window.location = '/recibo'
                }
                else{
                    alert("Sem itens selecionados.")
                }
            })

    }
    validar_pedidos()
}


var lista = async () => {
    await fetch('http://127.0.0.1:5000/cardapio/listar/cardapio', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
        .then(resultado => resultado.json())
        .then(resultado => {
            renderizarEdicoes(resultado.lista_cardapio)
        })

}

const form_finalizar_pedido = document.getElementById('finalizarPedido');
form_finalizar_pedido.addEventListener('submit', fazerPedido);

lista()