$(document).ready(function () {
  $('#id_grupos').multiselect({
    includeSelectAllOption: true,
    enableFiltering: true,
    selectAllJustVisible: true,
    enableCaseInsensitiveFiltering: true,
    buttonWidth: '100%',
    maxHeight: 500,
    allSelectedText: "Todos os grupos selecionados",
    selectAllText: "Selecionar Todos",
    nonSelectedText: "Selecione pelo menos um grupo",
    nSelectedText: " itens selecionados"
  });
  $('#id_grupos').multiselect('onDeselectAll', true);
  $('#id_grupos').multiselect('updateButtonText');
});