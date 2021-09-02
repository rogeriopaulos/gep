$('.dp-outros').prop("disabled", true);

function getOutrosField(el) {
  let outrosFieldParent = $(el).parent()
  let outrosFieldTd = $(outrosFieldParent).siblings()[0]
  return $(outrosFieldTd).find('.dp-outros')
}

$('.dp-select').change(function() {
  let selectedValue = $('.dp-select :selected').html().toUpperCase()
  let outrosField = getOutrosField(this)

  if (selectedValue == "OUTROS") {
    $(outrosField).prop("disabled", false);
  } else {
    $(outrosField).prop("disabled", true);
  }
});
