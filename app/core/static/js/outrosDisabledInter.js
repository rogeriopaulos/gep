let elementsRelated = ["#id_tipo_quebra_link", "#id_inicio_quebra", "#id_final_quebra"]

function enableElements() {
  elementsRelated.forEach(el => {
    $(el).prop("disabled", false)
  })
}

function disableElements() {
  elementsRelated.forEach(el => {
    $(el).prop("disabled", true)
    $(el).prop("value", "")
  })
}

$(document).ready(function() {
  if ($("#id_quebra_dados").is(":checked")) {
    enableElements()
  } else {
    disableElements()
  }
})

$("#id_quebra_dados").change(function() {
  if ($(this).is(":checked")) {
    enableElements()
  } else {
    disableElements()
  }
});
