window.onunload = refreshParent;
function refreshParent() {
    window.opener.location.reload(true);
    self.close();
    closeDetalhes();
}

function closeDetalhes() {
    var path = window.location.pathname;
    var arrayPath = path.split('/');
    var lastPath = arrayPath[arrayPath.length - 2];
    if (lastPath == 'detalhes') {
        window.close();
    }
}