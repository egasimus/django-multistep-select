;(function ( $, window, document, undefined ) {

    $(document).ready(function() {
        $("#%(id)s_0").change(function(){
            var request_url = "%(url)s".replace('$VALUE$',$(this).val())
            $.getJSON(request_url,function(data){
                $("#%(id)s_1").empty().append('<option value="">Please select a definition:</option>')
                $(data).each(function(){
                    var option = '<option value=' +
                        $(this)[0].pk+'>' +
                        $(this)[0].fields.text.substring(0,50) +
                        '</option>'
                    $("#%(id)s_1").append(option)
                })
            })
        })
    })

})(jQuery, window, document);
