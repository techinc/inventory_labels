$("#submit").prop("type", "button");
$("#submit").click(function() {
	$.ajax({
		url: 'print',
		data: {},
		success: function(data) {
			$('.result').html(data);
			alert('Load was performed.');
		}
	});
});