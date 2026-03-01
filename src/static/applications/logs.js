

function init_logs()
{

	var main_node = dojo.byId('logs_main');
	main_node.innerHTML = "Loading logs, please wait...";
	
	log_view.init();
 	
 	
}
  
  
log_view = {
	
	init: function() {
		
		console.debug('init log view');
		
		function _show_details(data) {
	   	 	var success = data.success;
	        var error = data.data;
	        if (success === 0) {
	            console.debug(error);
	            alert(error);
	        }
	        else {
	        	log_view.show_details(data.data);
	        }
	     }
	 	
	 	var address = "/services/logger/details/";
	 	network.pass_reponse_to_function(address, _show_details, 'json');   	
	},
	
	show_details: function(data) {
		
	  var main_node = dojo.byId('logs_main');
	  html = '<table>';
	  for (ix in data) {
	  	 var row = data[ix];
	  	 html += '<tr>';
	  	 for (ix in row) {
	  	 	html += '<td>';
	  	 	cell = row[ix];
	  	 	try {
	  	 		html += cell;
	  	 	}
	  	 	catch (e) {
	  	 		
	  	 	}
	  	 	html += '</td>';
	  	 }
	  	 html += '</tr>';
	  	
	  }
	  html += '</table>';
	  
	  main_node.innerHTML = html;
	}
	
};