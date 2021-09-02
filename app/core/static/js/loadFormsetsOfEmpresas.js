$('.formset_row').formset({
  addText: `
    <div class="text-center">
      <button class="btn btn-info btn-xs" type="button"><i class="glyphicon glyphicon-plus"></i> ADICIONAR NOVO CAMPO</button>
    </div>
  `,
  deleteText: `<button class="btn btn-danger btn-xs" type="button" id="btnFormsetRemove">REMOVER</button>`,
  prefix: $("#ofempresasForm").data("prefix"),
  added: function (el) {
    let selectField = $(el).find("td select.dp-select");
    let outrosField = $(el).find("td input.dp-outros");
    $(selectField).change(function() {
      if ($(selectField).children('option:selected').html().toUpperCase() == "OUTROS") {
        $(outrosField).prop("disabled", false);
      } else {
        $(outrosField).prop("disabled", true);
      }
    });
  }
});
