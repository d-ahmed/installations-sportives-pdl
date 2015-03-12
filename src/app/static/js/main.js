$(document).ready(function() {

    $.ajax({
    	url: '/installations/123456789',
        dataType: 'json',
        success: function (data) {
        	$('#error').hide();
        	$('#numero').text(data.numero);
        	$('#nom').text(data.nom);
        },
        error: function (xhr, status, err) {
        	$('#error').show();
        }
    });

});