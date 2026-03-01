upload_ = {
	
  init: function() {
  	login_.register_authentication_change_callback(upload_.authentication_changed);
  },
  
  authentication_changed: function() {
  	upload_.update_state();
  },

  update_state: function () {
  	var upload_button_widget = dijit.byId('upload_submit');
  	if (! login_.authenticated) {
  		upload_button_widget.attr('disabled', true);
  		upload_button_widget.attr('label', 'Upload (please log on first)');
  	}
  	else {
  		upload_button_widget.attr('disabled', false);
  		upload_button_widget.attr('label', 'Upload');
  	}
  },
	
  start: function () {
  	console.debug('start upload');
  	return true;
  },
  
  finish: function () {
  	console.debug('finish upload');
  	library.update_state();
  	alert('Your document has been uploaded and should now be available from your private library.');
  }
	
};