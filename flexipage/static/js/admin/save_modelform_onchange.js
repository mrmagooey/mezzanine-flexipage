
$(document).ready(function(){
    $('#id_template_name').change(function(){
        $('#id_template_name option').each(function(){
            if ($(this).attr('selected') == 'selected' && $(this).val() != '') {
                $('.change-view-save-continue').trigger('click');
            }
        });
    });

});
