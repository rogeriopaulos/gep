$(document).ready(function () {
  $('#logs-table').on('initComplete', function (event, table) {
    $('span.from > label').text('De');
    $('span.to > label').text('Até');
  });

  AjaxDatatableViewUtils.initialize_table(
    // element
    $('#logs-table'),
    // url
    $('#logs-table').data('url'),
    {
      autoWidth: false,
      full_row_select: false,
      scrollX: false,
    },
  );

  $("#buscasTabBtn").one("click", function () {
    $('#buscas-table').on('initComplete', function (event, table) {
      $('span.from > label').text('De');
      $('span.to > label').text('Até');
    });

    AjaxDatatableViewUtils.initialize_table(
      // element
      $('#buscas-table'),
      // url
      $('#buscas-table').data('url'),
      {
        // extra_options
        autoWidth: false,
        full_row_select: false,
        scrollX: false
      }
    );
  })

});
