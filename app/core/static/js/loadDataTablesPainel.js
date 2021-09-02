$(document).ready(function () {
  const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  const userFullName = $("#table_posts").data("user")

  $("#table_posts").DataTable({
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
    "pageLength": 25,
    "ajax": $("#table_posts").data('url'),
    "deferRender": true,
    "columns": [
      { "data": "data", "type": 'date-euro' },
      { "data": "autor" },
      {
        "data": "post",
        "render": function (data) {
          return `
            <span data-toggle="tooltip" data-placement="top" title="${data.titulo}">${data.truncate_titulo}</span>
          `
        }
      },
      {
        "data": "publicar",
        "orderable": false,
        "render": function (data) {
          const icon = data ? "ok" : "remove";
          return `<i class="glyphicon glyphicon-${icon}"></i>`
        }
      },
      {
        "data": null,
        "orderable": false,
        "render": function (data) {
          const is_author = data.autor.toUpperCase() == userFullName.toUpperCase()
          const publish = data.publicar ? { btn: "warning", icon: "fa-ban", title: "Suspender publicação" } : { btn: "primary", icon: "fa-cloud-upload", title: "Publicar" }

          return `
            <div class="actions">
              <a href="${data.post.url_detail}" class="link_clean">
                <button type="button" class="btn btn-success btn-xs btn_action" data-toggle="tooltip" data-placement="top" title="Preview">
                  <i class="fa fa-eye" aria-hidden="true"></i>
                </button>
              </a>
              <a href="${data.post.url_edit}" class="link_clean">
                <button type="button" class="btn btn-info btn-xs btn_action" data-toggle="tooltip" data-placement="top" title="Editar publicação">
                  <i class="fa fa-pencil" aria-hidden="true"></i>
                </button>
              </a>
              <form action="${data.post.url_publish_toggle}" method="post" enctype="multipart/form-data">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                <button type="submit" class="btn btn-${publish.btn} btn-xs btn_action btn_toggle_publish" data-toggle="tooltip" data-placement="top" title="${publish.title}">
                  <i class="fa ${publish.icon}" aria-hidden="true"></i>
                </button>
              </form>
              <form action="${data.post.url_delete}" method="post" enctype="multipart/form-data">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                <button type="submit" class="btn btn-danger btn-xs btn_action btn_delete" data-toggle="tooltip" data-placement="left" title="Remover publicação" ${is_author ? "" : "disabled"}>
                  <i class="fa fa-trash" aria-hidden="true"></i>
                </button>
              </form>
            </div)
          `
        }
      }
    ],
    "order": [
      [0, "desc"]
    ],
    "drawCallback": function (settings) {
      $('[data-toggle="tooltip"]').tooltip();
    }
  });

  let table = $("#table_metrics").DataTable({
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
    "pageLength": 25,
    "ajax": $("#table_metrics").data('url'),
    "deferRender": true,
    "columns": [
      { "data": "data", "type": 'date-euro' },
      { "data": "metrica" },
      {
        "data": "post",
        "render": function (data) {
          return `
            <a href="${data.url_detail}" class="link_clean reports_post_link" target="_blank">
              <span data-toggle="tooltip" data-placement="top" title="${data.titulo}">
                ${data.truncate_titulo} <i class="fa fa-external-link" aria-hidden="true"></i>
              </span>
            </a>
          `
        }
      },
      { "data": "valor" },
    ],
    "order": [
      [0, "desc"]
    ],
    "drawCallback": function (settings) {
      $('[data-toggle="tooltip"]').tooltip();
    }
  });
  yadcf.init(table, [
    {
      column_number: 0,
      filter_type: "range_date",
      date_format: "dd/mm/yyyy",
      filter_default_label: ["De", "Para"]
    },
    {
      column_number: 1,
      filter_type: "multi_select",
      select_type: "chosen",
      select_type_options: {
        no_results_text: "Não encontrado ->",
        search_contains: true,
        width: "190px"
      },
      filter_default_label: "Filtre por métricas"
    }
  ]);

});

$(document).on('click', '.btn_toggle_publish', function (e) {
  let response = confirm("Você tem certeza que deseja alterar essa publicação?");
  if (!response) {
    e.preventDefault();
  }
})

$(document).on('click', '.btn_delete', function (e) {
  let response = confirm("Você tem certeza que deseja remover essa publicação?");
  if (!response) {
    e.preventDefault();
  }
})
