my_reader = {
	
 init: function() {
 	login_.register_authentication_change_callback(my_reader.update_state);
 },
 
 update_state: function() {
 	if (login_.authenticated) {
 		my_reader.show_status('');
 		my_reader.populate();
 	}
 	else {
 		my_reader.show_status('Please log on to use the My Reader functionality.');
 	}
 },
 
 populate: function() {
 	var address = "/services/session/session_info";
    var response = network.pass_reponse_to_function(address,
    									 my_reader.populate_session_details, 'json');
 },	
 
 populate_session_details: function(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
			my_reader._populate_widgets('', read_cookie('nickname'), '');
        }
        else {
        	var email_address = data.data[0];
        	var nickname = data.data[1];
        	var num_words_added = data.data[2];
        	my_reader._populate_widgets(email_address, nickname, num_words_added);
        }
 },
 
 _populate_widgets: function(email_address, nickname, num_words_added) {
 	var my_reader_email_address_node = dojo.byId('my_reader_email_address');
	my_reader_email_address_node.innerHTML = email_address;
	var my_reader_nickname_node = dojo.byId('my_reader_nickname');
	my_reader_nickname_node.innerHTML = nickname;
	var my_reader_num_added_node = dojo.byId('my_reader_num_words_added');
	my_reader_num_added_node.innerHTML = '' + num_words_added;
 },
	
 show_deregister: function() {
	var deregister_pane_widget = dijit.byId('deregister_pane');
	deregister_pane_widget.show();
 },
 
 cancel_deregister: function() {
		var deregister_pane_widget = dijit.byId('deregister_pane');
		deregister_pane_widget.hide();
 },
 
 deregister: function(dialog_fields) {
     my_reader.show_status('Working...');
     
     var password_hash = hex_md5(dialog_fields.password);
   	 
   	 var address = "/services/session/deregister/" + password_hash;
   	 function _after_deregister(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            my_reader.show_status(error);
        }
        else {
        	my_reader.show_status('You have been successfully deregistered.');
        }
     }
     var response = network.pass_reponse_to_function(address, _after_deregister, 'json');
 },

 show_change_password: function() {
	var change_password_pane_widget = dijit.byId('change_password_pane');
	change_password_pane_widget.show();
 },
 
 cancel_change_password: function() {
		var change_password_pane_widget = dijit.byId('change_password_pane');
		change_password_pane_widget.hide();
 },
 
 submit_change_password: function(old_password, new_password) {
   	 my_reader.show_status('Working...');
   	 
   	 var old_password_hash = hex_md5(old_password);
   	 var new_password_hash = hex_md5(new_password);
   	 
   	 var address = "/services/session/change_password/" + old_password_hash + "/" + new_password_hash;
   	 function _after_change_password(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            my_reader.show_status(error);
        }
        else {
        	my_reader.show_status('Your password has been changed successfully');
        }
        
     }
     var response = network.pass_reponse_to_function(address, _after_change_password, 'json');
   },
   
   show_status: function(status_) {
   	 var my_reader_status_node = dojo.byId('my_reader_status');
   	 my_reader_status_node.innerHTML = status_;
   },
 
   change_password: function(dialog_fields) {
 	 if (dialog_fields.change_password_new != dialog_fields.change_password_new_confirm) {
       alert("Confirmation password is different.  Password is unchanged.");
       return;
     }
    my_reader.submit_change_password(dialog_fields.change_password_old,
    			dialog_fields.change_password_new);
   }
	
};