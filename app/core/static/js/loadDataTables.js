$(document).ready(function () {
  let tablesIds = ['#dp-table01', '#dp-table02']
  
  tablesIds.forEach(el => {

    $(el).DataTable({
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
      "ajax": $(el).data('url'),
      "deferRender": true,
      "columns": [
        { "data": "criacao" },
        { "data": "processo" },
        { "data": "nome" },
        { "data": "tipo" },
        { "data": "link" }
      ],
      "order": [[0, "desc"]],
      "columnDefs": [{
        "targets": 0,
        "type": 'date-euro',
      },
      {
        "targets": -1,
        "data": 'link',
        "render": function (data, type, row, meta) {
          return '<a href="' + data + '" target=_blank><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a>'
        }
      },
      // {
      //   "targets": 1,
      //   "data": 'nome',
      //   "render": function (data, type, row, meta) {
      //     if (data == null) {
      //       return '------'
      //     } else {
      //       return data
      //     }
      //   }
      // },
      {
        "targets": 2,
        "data": 'nome',
        "render": function (data, type, row, meta) {
          if (data == null) {
            return '------'
          } else {
            return data
          }
        }
      }]
    });
  })

});

$(document).ready(function () {
  let tablesIds = ['#dp-table03', '#dp-table04']

  tablesIds.forEach(el => {

    $(el).DataTable({
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
      "ajax": $(el).data('url'),
      "deferRender": true,
      "columns": [
        { "data": "criacao" },
        { "data": "ato" },
        { "data": "numero" },
        { "data": "nome" },
        { "data": "tipo" },
        { "data": "link" }
      ],
      "order": [[0, "desc"]],
      "columnDefs": [{
        "targets": 0,
        "type": 'date-euro',
      },
        {
        "targets": -1,
        "data": 'link',
        "render": function (data, type, row, meta) {
          return '<a href="' + data + '" target=_blank><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a>'
        }
      },
      {
        "targets": 3,
        "data": 'nome',
        "render": function (data, type, row, meta) {
          if (data == null) {
            return '------'
          } else {
            return data
          }
        }
      }]
    });

  })

})
