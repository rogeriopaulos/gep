$('.unread-link').each(function (_, obj) {
  const url = $(obj).data("url")
  const id = $(obj).data("notification_id")
  const row = $(obj).parent("tr")
  // const thLink = $(obj).children()
  // const newEl = `<i class="fa fa-envelope-open" aria-hidden="true" style="color: rgba(0, 0, 0, 0.3);"></i>`
  const newEl = `<i class="fa fa-envelope-open" aria-hidden="true"></i>`

  $(obj).click(function () {
    $.ajax({
      url: url,
      data: { "id": id },
    })
      .done(function (res) {
        if (res.data.status === "success") {
          // alert(`${res.data.msg}`)
          $(row).addClass('read')
          $(thLink).remove()
          $(obj).append(newEl)
        } else {
          alert("Ops... Ocorreu um problema! Por favor, informe o administrador.")
        }
      });
  });
});