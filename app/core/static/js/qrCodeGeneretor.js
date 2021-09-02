$(function () {
    $('.qrcode').each(function (_, el) {
        let qrcode = new QRCode(el, {
            width: 120,
            height: 120,
            correctLevel: QRCode.CorrectLevel.L
        });
        let content = $(el).data('content')
        qrcode.makeCode(content)
    })
});
$(function () {
    $('.qrCodeBtns').each(function (_, el) {
        $(el).click(function () {
            $(el).siblings().slideToggle('slow')
        })
    })
});