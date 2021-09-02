$('.dp-outros').prop("disabled", true);

$('.dp-select').change(function() {
  let selectedValue = $('.dp-select :selected').html().toUpperCase()
  if (selectedValue == "OUTRO(S)" | selectedValue == "OUTROS") {
    $('.dp-outros').prop("disabled", false);
  } else {
    $('.dp-outros').prop("disabled", true);
  }
});
