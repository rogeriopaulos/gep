$('.dp-outros').prop("disabled", true);
  $('.dp-select').change(function() {
    if ($('.dp-select :selected').text() == "Outro") {
      $('.dp-outros').prop("disabled", false);
    } else {
      $('.dp-outros').prop("disabled", true);
    }
  }
);

$('.dp-gse').prop("disabled", true);
  $('.dp-select').change(function() {
    if ($('.dp-select :selected').text() == "Oi") {
      $('.dp-gse').prop("disabled", false);
    } else {
      $('.dp-gse').prop("disabled", true);
    }
  }
);

$('.dp-portaljud').prop("disabled", true);
  $('.dp-select').change(function() {
    if ($('.dp-select :selected').text() == "Vivo") {
      $('.dp-portaljud').prop("disabled", false);
    } else {
      $('.dp-portaljud').prop("disabled", true);
    }
  }
);
$('.dp-infoguard').prop("disabled", true);
  $('.dp-select').change(function() {
    if ($('.dp-select :selected').text() == "TIM") {
      $('.dp-infoguard').prop("disabled", false);
    } else {
      $('.dp-infoguard').prop("disabled", true);
    }
  }
);
