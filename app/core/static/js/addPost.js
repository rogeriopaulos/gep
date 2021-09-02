function resetTableRow(table_row) {
  inputs = table_row.getElementsByTagName('input');
  selects = table_row.getElementsByTagName('select');

  for (let index = 0; index < inputs.length; index++) {
    const element = inputs[index];
    element.value = '';
  }
  for (let index = 0; index < selects.length; index++) {
    const element = selects[index];
    element.selectedIndex = element.defaultSelected;
  }
}

function updateRemoveInput() {
  var remove_input = document.querySelectorAll('[id$="-DELETE"');

  for (var i = 0, max = remove_input.length; i < max; i++) {
    if (remove_input[i].tagName === 'INPUT') {
      remove_input[i].hidden = true;
      var id_delete = remove_input[i].id + "_btn";
      // console.log(id_delete);
      remove_input[i].outerHTML += `<button id="${id_delete}" class="btn btn-danger btn-xs remove-form-row">REMOVER</button>`
    }
  }
}

let table = document.getElementById('table-relatorios');
table = table.getElementsByTagName('tbody')[0];
let tr_array = table.getElementsByTagName('tr');
let tr_backup = tr_array[tr_array.length - 1];
let total_forms = document.getElementById('id_relatoriopost_set-TOTAL_FORMS');
updateRemoveInput();

$(document).on('click', '.add-form-row', function (e) {
  e.preventDefault();
  var table = document.getElementById('table-relatorios');
  table = table.getElementsByTagName('tbody')[0];
  var tr = table.getElementsByTagName('tr');

  var last_id = tr.length - 1;

  if (last_id >= 0) {
    var last_id_regex = new RegExp(`_set-${last_id}`, 'g');
    var new_tr = tr[tr.length - 1].innerHTML;
    new_tr = new_tr.replace(last_id_regex, `_set-${last_id + 1}`);

    table.insertAdjacentHTML('beforeend', new_tr);
    resetTableRow(table.rows[last_id + 1]);
    total_forms.value = table.rows.length;

  } else {
    table.appendChild(tr_backup);
    resetTableRow(table.rows[last_id + 1]);
  }

  return false;
});
$(document).on('click', '.remove-form-row', function (e) {
  e.preventDefault();

  var input_delete = document.getElementById(this.id.replace('_btn', ''));

  input_delete.checked = true;

  this.parentElement.parentElement.hidden = true;
  total_forms.value = table.rows.length;
  return false;
});