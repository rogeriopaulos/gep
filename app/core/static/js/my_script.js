//Aplica máscaras sobre alguns campos
function formatar(mascara, documento){
    var i = documento.value.length;
    var saida = mascara.substring(0,1);
    var texto = mascara.substring(i);

    if (texto.substring(0,1) != saida){
              documento.value += texto.substring(0,1);
    }
}

//Exibe Tab
function exibe_tab(id) {
    $('#'+id).show();
}

//Oculpta tab
function oculta_tab(id) {
    $('#'+id).hide();
}


var check = function() {
  if (document.getElementById('pass').value ==
    document.getElementById('confirm_pass').value) {
    document.getElementById('message').style.color = 'green';
    document.getElementById('message').innerHTML = 'Senhas confirmadas';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = 'Senhas não coincidem.';
  }
}
