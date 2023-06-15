async function findOption(select) {
    select = document.getElementById("id_status");
    option = select.options[select.selectedIndex].value;

    if(option == "Расторгнут")
    {
        document.getElementById('visible_reasons_termination').insertAdjacentHTML('afterbegin',
            '<div class="form-group row mt-4" id="group_element_reasons_termination">'+
                '<label for="id_reasons_termination" class="col-sm-3 col-form-label ">Причины расторжения договора</label>'+
                '<div class="col-sm-9">'+
                    '<textarea rows="3" cols="45" class="form-control" name="reasons_termination" id="id_reasons_termination" required>'+
                    '</textarea>'+
                '</div>'+
            '</div>'
        );
    }
    else
    {
        if(document.getElementById('group_element_reasons_termination'))
            document.getElementById('group_element_reasons_termination').remove();
    }; 
}