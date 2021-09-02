$(document).ready(function () {
  AjaxDatatableViewUtils.initialize_table(
    $('#datatable_processos'),
    $('#datatable_processos').data('url'),
    {
      "drawCallback": function (settings) {
        rows_arquivados = $("td a.arquivado").parent().parent()
        rows_arquivados.addClass('dp-arquivar')
        rows_processos_externos = $("td a.processo-externo").parent().parent()
        rows_processos_externos.addClass('dp-processo-externo')
      },
      autoWidth: false,
      full_row_select: false,
      scrollX: false,
    },
  );
});

function changeButton(e) {
  var row = e.parentElement.parentElement
  var minus = e.querySelector("a.minus")
  var plus = e.querySelector("a.plus")

  if (!row.classList.contains("shown")) {
    minus.classList.remove("display-none")
    plus.classList.add("display-none")
  } else {
    plus.classList.remove("display-none")
    minus.classList.add("display-none")
  }
}
