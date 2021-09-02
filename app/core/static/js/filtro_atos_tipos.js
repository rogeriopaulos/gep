$(function () {
  $('#filtro_atos').multiselect({
    enableClickableOptGroups: true,
    enableCollapsibleOptGroups: true,
    includeSelectAllOption: true,
    enableFiltering: true,
    selectAllJustVisible: false,
    enableCaseInsensitiveFiltering: true,
    buttonWidth: '200px',
    maxHeight: 300,
    allSelectedText: "Exibindo Todos",
    selectAllText: "Todos",
    nonSelectedText: "Selecione Algo",
    nSelectedText: " itens selecionados"
  });
  $("#filtro_atos").multiselect('selectAll', false);
  $("#filtro_atos").multiselect('updateButtonText');
});


$(function () {
  var start = moment('2018-01-01');
  var end = moment();

  function cb(start, end) {
    $('#datefilter span').html(start.format('DD/MM/YYYY') + '-' + end.format('DD/MM/YYYY'));
  }

  $("#datefilter").daterangepicker({
    startDate: start,
    endDate: end,
    locale: {
      format: 'DD/MM/YYYY',
      separator: " - ",
      applyLabel: "Aplicar",
      cancelLabel: "Cancelar",
      fromLabel: "De",
      toLabel: "Até",
      customRangeLabel: "Escolha o Intervalo",
      weekLabel: "W",
      daysOfWeek: [
        "Sab",
        "Dom",
        "Seg",
        "Ter",
        "Qua",
        "Qui",
        "Sex"
      ],
      monthNames: [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
      ],
      firstDay: 1
    },
    ranges: {
      'Hoje': [moment(), moment()],
      'Ontem': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
      'Últimos 7 Dias': [moment().subtract(6, 'days'), moment()],
      'Últimos 15 Dias': [moment().subtract(14, 'days'), moment()],
      'Últimos 30 Dias': [moment().subtract(29, 'days'), moment()],
      'Mês Atual': [moment().startOf('month'), moment().endOf('month')],
      'Último Bimestre': [moment().subtract(2, 'month').startOf('month'), moment().endOf('month')],
    }
  }, cb);
  cb(start, end);

  $('#filtrar').click(function () {
    $('.ato_filtro').hide();

    var selected = $("#filtro_atos option:selected");
    if (selected.text() == "") {
      $('.ato_filtro').hide();
    } else {
      selected.each(function () {
        var sel = $(this).text();
        $('.ato_filtro:contains("' + sel + '")').show(300);
      })
    }

    var str = $('.data_filtro').text();
    var datas = str.match(/\d{2}([\/.-])\d{2}\1\d{4}/g);
    var d = $('.date_select').text();
    var dates_selected = d.match(/\d{2}([\/.-])\d{2}\1\d{4}/g);
    var d_inicial = dates_selected[0].split('/');
    var invert_d_inicial = d_inicial[2] + d_inicial[1] + d_inicial[0];
    var d_final = dates_selected[1].split('/');
    var invert_d_final = d_final[2] + d_final[1] + d_final[0];
    $.each(datas, function (index, value) {
      var dt = value.split('/');
      var dt_s = value.toString();
      var invert_dt = dt[2] + dt[1] + dt[0];
      if (!((parseInt(invert_dt)) >= (parseInt(invert_d_inicial)) && (parseInt(invert_dt)) <= (parseInt(invert_d_final)))) {
        $('.ato_filtro:contains("' + dt_s + '")').hide()
      }
    })
  });
});
