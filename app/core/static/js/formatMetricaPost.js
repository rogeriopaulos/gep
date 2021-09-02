let INPUT_TYPE = {
  'str': 'text',
  'int': 'number',
  'float': 'number'
}

let delay = (function () {
  let timer = 0;
  return function (callback, ms) {
    clearTimeout(timer);
    timer = setTimeout(callback, ms);
  };
})()

function setValueAttr(row) {
  let tdMetrica = $(row)[0]
  let elSelected = $(tdMetrica).children('select').children('option:selected')
  let valueType = $(elSelected).data('type')

  let valueTd = $(".formset_row>td")[1]
  let valueInput = $(valueTd).children('input')

  if (valueType) {
    $(valueInput).prop("type", INPUT_TYPE[valueType])
    $(valueInput).attr("disabled", false)
    switch (valueType) {
      case "float":
        $(valueInput).prop("placeholder", "Ex: 10,0")
        $(valueInput).prop("step", "0.01")
        $(valueInput).keydown(function () {
          delay(function () {
            let inputVal = $(valueInput).val();
            if (inputVal.length > 0) {
              if (Number.isInteger(parseFloat(inputVal))) {
                let formatNum = `${inputVal}.0`; 
                $(valueInput).val(formatNum);
              } else {
                $(valueInput).val(inputVal);
              }
            }
          }, 1000);
        })
        break;
      case "int":
        $(valueInput).prop("placeholder", "Ex: 5")
        $(valueInput).prop("step", "1")
        $(valueInput).mask("#########")
        break;
      default:
        $(valueInput).prop("placeholder", "Valor")
        break;
    }
  } else {
    $(valueInput).val("")
    $(valueInput).attr("disabled", true)
  }
}

let row = $(".formset_row>td")
$(document).ready(function () {
  setValueAttr(row)
})

$(row[0]).click(function () {
  setValueAttr(row)
})