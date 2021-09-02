$(document).ready(function () {
  const url = $('#dp-notify_table01').data("url");

  $("#dp-notify_table01").DataTable({
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
      { "data": "procedimento" },
      { "data": "link" },
      { "data": "lida" },
      { "data": null },
    ],
    "order": [[0, "desc"]],
    "columnDefs": [{
      "targets": 0,
      "type": "date-euro",
    }, {
      "targets": 3,
      "data": 'link',
      "render": function (data) {
        return '<a href="' + data + '" target=_blank><span class="glyphicon glyphicon-eye-open" aria-hidden="true"></span></a>'
      }
    }, {
      "targets": 4,
      "data": 'lida',
      "render": function (data) {
        if (data) {
          return '<span class="glyphicon glyphicon-remove" aria-hidden="true" id="icon-unread"></span>'
        } else {
          return '<span class="glyphicon glyphicon-ok" aria-hidden="true" id="icon-read"></span>'
        }
      }
    }, {
      "targets": -1,
      "render": function (data) {
        if (data.lida) {
          return `<a href="#" class="unread-link" data-url="${data.url}" data-notification_id="${data.id}">Marcar como lida</a>`
        } else {
          return '<i class="fa fa-envelope-open" aria-hidden="true"></i>'
        }
      }
    }],
    "drawCallback": function (settings) {
      $('.unread-link').each(function (_, obj) {
        const url = $(obj).data("url")
        const id = $(obj).data("notification_id")

        const iconRmParent = obj.parentElement.previousElementSibling
        const iconRm = obj.parentElement.previousElementSibling.firstElementChild
        const td = $(obj).parent("td")
        const newEl = `<i class="fa fa-envelope-open" aria-hidden="true"></i>`

        $(obj).click(function () {
          $.ajax({
            url: url,
            data: { "id": id },
          })
            .done(function (res) {
              if (res.data.status === "success") {
                $(iconRm).fadeToggle(function() {
                  $(iconRmParent).append('<span class="glyphicon glyphicon-ok" aria-hidden="true" id="icon-read"></span>')
                });
                $(obj).fadeToggle(function() {
                  $(td).append(newEl)
                });
              } else {
                alert("Ops... Ocorreu um problema! Por favor, informe o administrador.")
              }
            });
        });
      });
    }
  });

});

$(document).on('click', '#all_read_btn', function (e) {
  let response = confirm("Você tem certeza que deseja marcar todas as notificações como lida?");
  if (!response) {
    e.preventDefault();
  }
})