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

function add_total(response) {
    const amount = document.getElementById('amount');
    if (amount) {
        amount.textContent = "Valor: " + response;
    }
}

var get_total = async () => {
    await fetch('http://127.0.0.1:5000/pedidos/total/pagar', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': usuarioLogado
        }
    })
        .then(resultado => resultado.json())
        .then(resultado => {

            if (resultado.total) {
                add_total(resultado.total)
            }
            else if (resultado.mensagem) {
                alert(resultado.mensagem)
            }
        })

}

var cartoes = {
    Visa: /^4[0-9]{12}(?:[0-9]{3})/,
    Mastercard: /^5[1-5][0-9]{14}/,
    Amex: /^3[47][0-9]{13}/,
    DinersClub: /^3(?:0[0-5]|[68][0-9])[0-9]{11}/,
    Discover: /^6(?:011|5[0-9]{2})[0-9]{12}/,
    JCB: /^(?:2131|1800|35\d{3})\d{11}/
};

function testarCC(nr, cartoes) {
    for (var cartao in cartoes) if (nr.match(cartoes[cartao])) return cartao;
    return false;
}

var pagamento = async (tipoPagamento, cardNumero, cardNome, mes, ano, cvc) => {
    await fetch('http://127.0.0.1:5000/pedidos/processar/pagamento', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': usuarioLogado
        },
        body: JSON.stringify({ tipoPagamento: tipoPagamento, cardNumero: cardNumero, cardNome: cardNome, mes:mes, ano: ano, cvc:cvc })
    })
        .then(resultado => resultado.json())
        .then(resultado => {

            if (resultado.finalizado) {
                alert("Pagamento feito com sucesso!")
            }
            else if (resultado.mensagem) {
                alert(resultado.mensagem)
            }

        })

}

$('#card-btn').click(() => {

    var tipoPagamento = $('#tipoPagamento').val()
    var cardNumero = $('#card-number').val()
    var cardNome = $('#card-holder').val()
    var mes = $('#card-month').val()
    var ano = $('#card-year').val()
    var cvc = $('#card-cvc').val()

    var validarcc = testarCC(cardNumero, cartoes)

    if(validarcc == false){
        alert('Cartão digitado é invalido, por favor tente novamente.')
    }
    else{
        pagamento(tipoPagamento, cardNumero, cardNome, mes, ano, cvc)
    }
})

get_total()