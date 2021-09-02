$("#btnSaveAdd").click(function() {
  url = $(this).data('url')
  $("#idFormGeral").attr("action", url)
  $("#idFormGeral").submit()
})