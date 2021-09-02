$('.dp-outros').prop("disabled", true);

function getOutrosField(el) {
  let outrosFieldParent = $(el).parent()
  let outrosFieldTd = $(outrosFieldParent).siblings()[0]
  return $(outrosFieldTd).find('.dp-outros')
}

function getSelectField(el) {
  let selectFieldParent = $(el).parent().parent()
  let selectFieldValue = $(selectFieldParent).children("td")[0].text().toUpperCase()
  return $(selectFieldTd).find('.dp-select')
}

function applyDisable(el) {
  $(el).change(function () {
    let selectedValue = $(el).children("option:selected").text().toUpperCase()
    let outrosField = getOutrosField(el)

    if (selectedValue == "OUTROS") {
      $(outrosField).prop("disabled", false);
    } else {
      $(outrosField).prop("disabled", true);
    }
  })
}

function getSelectedByPhone(el) {
  let parentEl = $(el).parent().parent()
  let selectTd = $(parentEl).children('td')[0]
  let selectField = $(selectTd).children('select')
  return selectField.children('option:selected').text().toUpperCase()
}

function getMask(el) {
  let selectedValue = getSelectedByPhone(el)
  let masks = ['(00)00000-0000', '0000000000000000'];
  return (selectedValue === 'IMEI') ? masks[1] : masks[0];  
}

function maskPhoneField(el) {
  let options =  {
    onKeyPress: function(fone, e, field, options){
      $(el).mask(getMask(el), options);
    }
  };
  $(el).mask(getMask(el), options);
}

$(document).ready(function () {
  $(".dp-uppercase").keyup(function () {
    let ucase = $(this).val().toUpperCase()
    $(this).val(ucase);
  });

  $(".dp-ddr").one("keyup", function () {
    let defaultValue = "(86)3131-0000"
    $(this).val(defaultValue);
  });

  let selectFields = $(".dp-select").toArray();
  selectFields.forEach(el => {
    $(el).prop("required", true)
    let isOutros = $(el).children("option:selected").text().toUpperCase() === 'OUTROS' ? true : false
    if (isOutros) {
      let outrosField = getOutrosField(el)
      $(outrosField).prop("disabled", false);
    } else {
      applyDisable(el)
    }
  });

  let phoneImeiFields = $(".dp-foneimei").toArray();
  phoneImeiFields.forEach(el => {
    maskPhoneField(el);
  });

});