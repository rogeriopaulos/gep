var cpf = $('#id_cpf')
var cnpj = $('#id_cnpj')
$('#id_cpf').on('change', function () {
  if (this.value != '') {
    cnpj.attr('disabled', true);
  } else {
    cnpj.attr('disabled', false);
  }
});
$('#id_cnpj').on('change', function () {
  if (this.value != '') {
    cpf.attr('disabled', true);
  } else {
    cpf.attr('disabled', false);
  }
});
