$(document).ready(function(){
    $(".deletepet").click(function(evt){
        evt.preventDefault();
        evt.stopPropagation();
        if(confirm("Esta seguro que desea eliminar este servicio?")){
            urlRedirect = $(this).data('urldelete')
            window.location.href = urlRedirect
        }
    });
});