//Máscaras do CEP e Matrícula
// function formatar(mascara, documento){
//   var i = documento.value.length;
//   var saida = mascara.substring(0,1);
//   var texto = mascara.substring(i)
//
//   if (texto.substring(0,1) != saida){
//             documento.value += texto.substring(0,1);
//   }
// }


// Máscara do CPF
// function fMasc(objeto, mascara) {
//   obj = objeto
//   masc = mascara
//   setTimeout("fMascEx()", 1)
// }
//
// function fMascEx() {
//   obj.value = masc(obj.value)
// }
//
// function mCPF(cpf) {
//   cpf = cpf.replace(/\D/g, "")
//   cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2")
//   cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2")
//   cpf = cpf.replace(/(\d{3})(\d{1,2})$/, "$1-$2")
//   return cpf
// }

// Redimensiona Popup
function PopupCenterDual(url, title, w, h) {
  // Fixes dual-screen position Most browsers Firefox
  var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
  var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;
  width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
  height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

  var left = ((width / 2) - (w / 2)) + dualScreenLeft;
  var top = ((height / 2) - (h / 2)) + dualScreenTop;
  var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);

  // Puts focus on the newWindow
  if (window.focus) {
    newWindow.focus();
  };
};

// Collapse DetailView - Atos
$(document).on('click', '.panel-heading span.clickable', function (e) {
  var $this = $(this);
  if (!$this.hasClass('panel-collapsed')) {
      $this.parents('.panel').find('.panel-body').slideUp();
      $this.addClass('panel-collapsed');
      $this.find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus');
  } else {
      $this.parents('.panel').find('.panel-body').slideDown();
      $this.removeClass('panel-collapsed');
      $this.find('i').removeClass('glyphicon-plus').addClass('glyphicon-minus');
  }
});
$(document).on('click', '.panel div.clickable', function (e) {
  var $this = $(this);
  if (!$this.hasClass('panel-collapsed')) {
      $this.parents('.panel').find('.panel-body').slideUp();
      $this.addClass('panel-collapsed');
      $this.find('i').removeClass('glyphicon-minus').addClass('glyphicon-plus');
  } else {
      $this.parents('.panel').find('.panel-body').slideDown();
      $this.removeClass('panel-collapsed');
      $this.find('i').removeClass('glyphicon-plus').addClass('glyphicon-minus');
  }
});
$(document).ready(function () {
  $('.panel-heading span.clickable').click();
  $('.panel div.clickable').click();
});

// Dropdown-Menu - Processos
$(document).ready(function() {
    $('.navbar a.dropdown-toggle').on('click', function(e) {
        var $el = $(this);
        var $parent = $(this).offsetParent(".dropdown-menu");
        $(this).parent("li").toggleClass('open');

        if(!$parent.parent().hasClass('nav')) {
            $el.next().css({"top": $el[0].offsetTop, "right": $parent.outerWidth() - 4});
        }

        $('.nav li.open').not($(this).parents("li")).removeClass("open");

        return false;
    });
});
