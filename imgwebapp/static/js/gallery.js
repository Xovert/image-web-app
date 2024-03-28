$(document).ready(function(){
    $("#Error").modal('toggle');
});

$('#Deletion').on('show.bs.modal', (e)=>{
    var data = $(e.relatedTarget).data('recordPath')
    $('.btn-confirm').attr("formaction", data)
})