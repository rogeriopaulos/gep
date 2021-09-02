function onlyFileName(div_id) {
  let textFileField = $(`${div_id} div.controls`).children('a').text()
  let filePathArray = textFileField.split('/')
  let fileName = filePathArray[filePathArray.length - 1]
  $(`${div_id} div.controls`).children('a').text(fileName)
}

$(document).ready(function () {
  if ($('#div_id_docs').length) {

    onlyFileName('#div_id_docs')

  } else if ($('#div_id_formulario').length) {

    onlyFileName('#div_id_formulario')

  } else if ($('#div_id_arquivo').length) {

    onlyFileName('#div_id_arquivo')

  }
});