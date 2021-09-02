$(document).on('click', '.btn-pedidobusca-monitor', function () {
  let parentBtn = $(this).parent();
  let btnClicked = $(this);
  let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  var retorno = confirm("Você tem certeza que deseja monitorar este ato?");
  if (retorno == true) {
    $.ajax({
      type: "POST",
      url: $(this).attr("data-url"),
      data: {
        id: $(this).attr("data-id"),
        tipo: $(this).attr("data-tipo")
      },
      statusCode: {
        403: function () {
          alert('Você não possui permissão para realizar esta operação.')
        }
      }
    })
      .done(function (data) {
        const newBtn = `
        <span data-toggle="tooltip" data-placement="left" title="Ato monitorado">
          <a href="${data.url}" target="_blank"><i class="glyphicon glyphicon-screenshot monitoring"></i></a>
        </span>
        `
        $(btnClicked).hide();
        $(parentBtn).prepend(newBtn).hide().fadeIn('slow');
        $('[data-toggle="tooltip"]').tooltip();
      })
  }
})
