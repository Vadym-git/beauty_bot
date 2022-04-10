function write_districts(districts){
	var parsed_districts = JSON.parse(districts)
	var select = document.getElementById("cities");
	select.innerText = null;
	var el = document.createElement("option");
	el.text = 'All Districts';
	el.value = '';
	select.add(el);
	for (key in parsed_districts) {
		var el = document.createElement("option");
	    el.text = parsed_districts[key][1].toUpperCase();
	    el.value = parsed_districts[key][0];
	    select.add(el);
	}
}

function get_districts(county){
	$.ajax({
		url: "/cities/"+county,
		data: {
			county: county
		},
		success: function( result ) {
			write_districts(result);
		}
	});
}

$(function(){
	$("#county").click(function(e){
	value = $("#county option:selected").val();
	get_districts(value)
	});

});