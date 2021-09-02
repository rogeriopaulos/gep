$(document).ready(function () {
  const url = $('#dp-notify_table03').data("url");

  const titulo = $("#dp-notify_table03").data("tablecontent");

  $("#dp-notify_table03").append(`<caption style="caption-side: top">${titulo}</caption>`);

  $("#dp-notify_table03").DataTable({
    language: {
      "sEmptyTable": "Nenhum registro encontrado",
      "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
      "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
      "sInfoFiltered": "(Filtrados de _MAX_ registros)",
      "sInfoPostFix": "",
      "sInfoThousands": ".",
      "sLengthMenu": "_MENU_ resultados por página",
      "sLoadingRecords": "Carregando...",
      "sProcessing": "Processando...",
      "sZeroRecords": "Nenhum registro encontrado",
      "sSearch": "Pesquisar",
      "oPaginate": {
        "sNext": "Próximo",
        "sPrevious": "Anterior",
        "sFirst": "Primeiro",
        "sLast": "Último"
      },
      "oAria": {
        "sSortAscending": ": Ordenar colunas de forma ascendente",
        "sSortDescending": ": Ordenar colunas de forma descendente"
      },
      "select": {
        "rows": {
          "_": "Selecionado %d linhas",
          "0": "Nenhuma linha selecionada",
          "1": "Selecionado 1 linha"
        }
      }
    },
    "pageLength": 10,
    "ajax": url,
    "deferRender": true,
    "columns": [
      { "data": "data" },
      { "data": "msg" },
      { "data": "receptor" },
      { "data": "lida" },
      { "data": "procedimento" },
      { "data": "link" }
    ],
    "order": [[0, "desc"]],
    "columnDefs": [{
      "targets": 0,
      "type": "date-euro",
    }, {
      "targets": 3,
      "data": 'lida',
      "render": function (data) {
        if (data) {
          return '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>'
        } else {
          return '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>'
        }
      }
    }, {
      "targets": -1,
      "data": 'link',
      "render": function (data) {
        return '<a href="' + data + '" target=_blank><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a>'
      }
    }]
  });
});
