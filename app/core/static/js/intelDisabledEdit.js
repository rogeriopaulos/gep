$('.dp-dataproducao').prop("disabled", true);
$('.dp-anexos').prop("disabled", true);
$('.dp-dataresposta').prop("disabled", true);

$('document').ready(function() {
  if ($('.dp-select :selected').text() == "RELATÓRIO DE INTELIGÊNCIA") {
    $('.dp-dataproducao').prop("disabled", false);
    $('.dp-anexos').prop("disabled", false);
  } else {
    $('.dp-dataproducao').prop("disabled", true);
    $('.dp-anexos').prop("disabled", true);
  }
});

$('document').ready(function() {
  if ($('.dp-select :selected').text() == "PEDIDO DE BUSCA") {
    $('.dp-dataresposta').prop("disabled", false);
  } else {
    $('.dp-dataresposta').prop("disabled", true);
  }
});
