$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

$('#anularAtoModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var recipient = button.data('item') // Extract info from data-* attributes
    var modal = $(this)
    modal.find('.modal-title').text('Anular Ato')
    let form = modal.find('.form-modal')
    let baseUrl = $(form).data("baseurl").replace(/.$/, recipient)
    $(form).attr("action", baseUrl)
})