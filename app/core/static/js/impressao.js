// Imprime apenas a div '#printable', definida no modelo de ofício gerado
function printDiv() {
    var conteudo = document.getElementById('printable').innerHTML;
    var win = window.open();
    win.document.write(conteudo);
    win.print();
    win.close();//Fecha após a impressão.
}
