function rendericarRecibo(response) {

    const divContent = document.getElementById('lista_recibo');
    let html = '';

    for (i = 0; i < response.length; i++) {
        data = response[i]['data_pedido_str']
        item = response[i]['item_cardapio']['nome']
        quantidade_por_item = response[i]['quantidade_item_pedido']
        valor_item = quantidade_por_item * response[i]['item_cardapio']['valor_num']
        valor_total = response[i]['valor_total_str']

        html += `
            <tr>
                <td>${item} x${quantidade_por_item}</td>
                <td class="right">R$ ${valor_item}</td>
            </tr>
        `;
    }

    html += `
        <tr>
            <td>Total</td>
            <td class="right">${valor_total}</td>
        </tr>
        <tr>
            <td>
                <br>
                <a href="/pagamento" target="_blank" rel="noopener noreferrer">
                    <button>
                        Pagar
                    </button>
                </a>
            </td>
        </tr>
    `;

    const pedido_date = document.getElementById('pedido_date');
    if (pedido_date) {
        pedido_date.textContent = data;
    }
    divContent.innerHTML = html;

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

var lista = async () => {
    await fetch('http://127.0.0.1:5000/pedidos/listar/recibo', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': usuarioLogado
        }
    })
        .then(resultado => resultado.json())
        .then(resultado => {

            if(resultado.dados){
                rendericarRecibo(resultado.dados)
            }
            else if(resultado.mensagem){
                alert(resultado.mensagem)
            }
        })

}

lista()

