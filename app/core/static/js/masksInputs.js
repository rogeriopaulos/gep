$(document).ready(function(){
  // var options =  {
  //   onKeyPress: function(fone, e, field, options){
  //     var masks = ['(00)00000-0000', '000000-00-000000-0'];
  //     var mask = (fone.length>13) ? masks[1] : masks[0];
  //     $('.dp-fone_imei').mask(mask, options);
  //   }
  // };
  // $('.dp-fone_imei').mask('(00)00000-0000', options);
  $('.dp-fone').mask('(00) 00000-0000');
  $('#id_cel_pessoal').mask('(00) 00000-0000');
  $('#id_cel_funcional').mask('(00) 00000-0000');
  $('#id_cpf').mask('000.000.000-00', {reverse: true});
  $('#id_cnpj').mask('00.000.000/0000-00', {reverse: true});
  $('#id_num_simba').mask('000-ZZZZ-000000-00', {'translation': {Z: {pattern: /[A-Za-z]/}}});
  $('#id_identidade').mask('YYYYYYYYYYYYYYYYYYYY', {'translation': {Y: {pattern: /\d+/}}});
  $('#id_matricula').mask('000.000-Z', {'translation': {Z: {pattern: /[A-Za-z0-9]/, optional: true}}});
  $('#id_cep').mask('00000-000');
  $('.dp-rif').mask('00000.ZZZ.ZZZZ.ZZZZ', {'translation': {Z: {pattern: /[0-9]/, optional: true}}});
  $('#id_num_rif').mask('00000.ZZZ.ZZZZ.ZZZZ', {'translation': {Z: {pattern: /[0-9]/, optional: true}}});
  $('.dp-sei').mask('00000');
  $('.dp-data').mask('00/00/0000');
  $('#id_data_envio').mask('00/00/0000');
  $('.dp-maxdigit').mask('00000');

  $(".dp-uppercase").keyup(function () {
    var ucase = $(this).val().toUpperCase()
    $(this).val(ucase);
  });
});
