$('.formset_row').formset({
  addText: `
      <div class="text-center">
        <button class="btn btn-info btn-xs" type="button"><i class="glyphicon glyphicon-plus"></i> ADICIONAR NOVO CAMPO</button>
      </div>
  `,
  deleteText: `<button class="btn btn-danger btn-xs" type="button" id="btnFormsetRemove">REMOVER</button>`,
  prefix: $("#alvoForm").data("prefix"),
  added: function (el) {
    let selectField = $(el).find("td select");
    $(selectField).prop("required", true)
    applyDisable(selectField);

    let phoneImeiField = $(el).find("td input.dp-foneimei");
    maskPhoneField(phoneImeiField);

    $(".dp-ddr").one("keyup", function () {
      let defaultValue = "(86)3131-0000"
      $(this).val(defaultValue);
    });
  }
});
