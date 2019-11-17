$(document).ready(function(){
    $(".deletepet").click(function(evt){
        evt.preventDefault();
        evt.stopPropagation();
        if(confirm("Esta seguro que desea eliminar esta mascota?")){
            urlRedirect = $(this).data('urldelete')
            window.location.href = urlRedirect
        }
    });
    $(".hours_contract").change(function(evt){
        var label = $(this).siblings().first();
        var price = parseInt(label.data('rate'));
        var hours = parseInt($(this).val());
        totalPrice = price * hours;
        var spanPrice = $(this).parent().siblings('h3').children('.price').first();
        spanPrice.text(totalPrice);
    });
});