$(document).ready(function () {
  $('#id_usuarios').multiselect({
    includeSelectAllOption: true,
    enableFiltering: true,
    selectAllJustVisible: true,
    enableCaseInsensitiveFiltering: true,
    buttonWidth: '100%',
    maxHeight: 500,
    allSelectedText: "Todos os usuários selecionados",
    selectAllText: "Selecionar Todos",
    nonSelectedText: "Selecione pelo menos um usuário",
    nSelectedText: " itens selecionados"
  });
  $('#id_usuarios').multiselect('onDeselectAll', true);
  $('#id_usuarios').multiselect('updateButtonText');
});