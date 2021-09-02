$(function(){
  if ($('.dp-select').val() == "Outro(s)") {
    $('.dp-outros').prop("disabled", false);
  } else {
    $('.dp-outros').prop("disabled", true);
  }
});

$('.dp-select').change(function() {
  if ($('.dp-select :selected').val() != "Outro(s)") {
    $('.dp-outros').val("");
    $('.dp-outros').prop("disabled", true);
  } else {
    $('.dp-outros').prop("disabled", false);
  }
});
