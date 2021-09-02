$('#alterarStatusAtoModal').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget)
  let url = button.data('url')
  let modal = $(this)
  let form = modal.find('.form-modal-status')
  $(form).attr("action", url)
})

$('#alterarDataEnvioAtoModal').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget)
  let url = button.data('url')
  let modal = $(this)
  let form = modal.find('.form-modal-dataenvio')
  $(form).attr("action", url)
})

$('#adicionarTagsModal').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget)
  let url = button.data('url')
  let tags = button.data('tags').split(',').join(', ')
  let modal = $(this)
  let form = modal.find('.form-modal-tags')
  let divInput = modal.find('div.bootstrap-tagsinput')
  let input = $(divInput).find('input')
  $(form).attr("action", url)
  $(input).val(tags)
})
