$("#alert").hide();
$("#print").prop("type", "button");
$("button").click(function() {
    $('#alert').hide();
    $(this).button('loading');
	$.ajax({
		url: this.id,
        type: 'POST',
		data: $('form').serialize(),
		success: function(data) {
			$('#results').html(data);
			alert('Load was performed.');
		},
        error: function(jqXHR, textStatus) {
            fancyError('Something went wrong: '+textStatus);
        }
	});
    $(this).button('reset');
});

fancyError = function(message) {
    $('#alert').html('<strong>Error!</strong> '+message).show();
}