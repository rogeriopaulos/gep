function format_flex_row_children_of(responsive_group) {
    const responsive_children = responsive_group.children;

    const cdr_len = responsive_children.length;

    for (var i=cdr_len-1; i>=0; i--){
        var panel = responsive_children[i];

        responsive_group.appendChild(panel);

        if (!Math.floor(i%3)){
            create_break_row(responsive_group);            
        }
    }
}

function create_break_row(parent_group) {
    var row_break = document.createElement('div');
    row_break.className = 'break-panel-row';
    parent_group.appendChild(row_break);
}

$(document).ready(() => {
    const groups = document.getElementsByClassName('flex_row_of_3');

    const gps_len = groups.length;

    for (var i=gps_len-1; i>=0; i--) {
        const responsive_group = groups[i];

        format_flex_row_children_of(responsive_group);
    }
});
