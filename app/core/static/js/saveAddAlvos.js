$("#btnSaveAdd").click(function() {
  url = $(this).data('url')
  $("#alvoForm").attr("action", url)
  $("#alvoForm").submit()
})