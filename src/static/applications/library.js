/**
 * @author alynch
 */
 
library = {
	
   background_colour: 0xFFFFFF,
   
   colour:  0x0000,
   
   request_delete_user_id: 0,
   request_delete_title: '',
   request_share_user_id: 0,
   request_share_title: '',
	
   init: function() {
   	var download_widget = dijit.byId("library_download");
   	var text_sample_node = dojo.byId("library_colour_sample");
   	text_sample_node.innerHTML = 'هذه كتابة';  
    dojo.connect(download_widget, 'onClick', library._download_personal_text);
    library.change_colour_scheme();
    library.select_text();
    login_.register_authentication_change_callback(library.update_state);
   },
   
   select_text_old: function() {
   	 console.debug('select text');
	 var select_text_dialog_widget = dijit.byId('library_select_text_dialog');
	 select_text_dialog_widget.show();
   },
   
   get_text: function(dialog_fields) {
   	
   },
   
   select_preferences: function() {
	 var select_preferences_dialog_widget = dijit.byId('library_preferences_dialog');
	 select_preferences_dialog_widget.show();
   },
   
   preferences_done: function() {
		 var select_preferences_dialog_widget = dijit.byId('library_preferences_dialog');
		 select_preferences_dialog_widget.hide();
   },
   
   highlight_unknown_words: function() {
	   	 console.debug('highlight_unknown_words');
	   	central_text.highlight_unknown_words();
   },
   
   set_preferences: function(dialog_fields) {
   	
   },
	
   update_state: function() {
//   	 var user_id = read_cookie('user_id');
//   	 library.populate_personal_texts(user_id);
   },
   
   change_colour_scheme: function () {
   	var text_area = dojo.byId('central_text');
   	text_area.style.backgroundColor = library.background_colour;
   	text_area.style.color = library.colour;
   },
   
   set_background_colour: function(colour) {
   	 var text_sample_node = dojo.byId("library_colour_sample");
   	 library.background_colour = colour;
   	 text_sample_node.style.backgroundColor = colour;
   },
   
   set_font_colour: function(colour) {
   	 var text_sample_node = dojo.byId("library_colour_sample");
   	 library.colour = colour;
   	 text_sample_node.style.color = colour;
   },
   
   do_delete_library_file: function(user_id, title) {
   	  var address = "/services/library/delete/"+ library.request_delete_user_id + "/" + library.request_delete_title;
   	  function library_file_deleted(data) {
   	  	if (data.success) {
   	  		var message = data.data;
   	  		alert(message);
   	  	}
   	  	else {
   	  		var error = data.data;
   	  		alert(error);
   	  	}
   	  }
	  network.pass_reponse_to_function(address, library_file_deleted, 'json');
   },
   
   do_share_library_file: function(user_id, title) {
	   	  var address = "/services/library/share/"+ library.request_share_user_id + "/" + library.request_share_title;
	   	  function library_file_shared(data) {
	   	  	if (data.success) {
	   	  		var message = data.data;
	   	  		alert(message);
	   	  	}
	   	  	else {
	   	  		var error = data.data;
	   	  		alert(error);
	   	  	}
	   	  }
		  network.pass_reponse_to_function(address, library_file_shared, 'json');
	   },
   
   delete_library_file: function(user_id, title) {
   		library.request_delete_user_id = user_id;
   		library.request_delete_title = title;
   		var library_delete_message_node = dojo.byId('library_delete_message');
   		var message = "This will delete your library file titled <b>" + title + "</b>.\n" +
			          "Click OK to continue or click on the 'x' to cancel.";
		library_delete_message_node.innerHTML = message;
		var confirm_delete_dialog = dijit.byId('confirm_library_delete_dialog');	
		confirm_delete_dialog.show();
   },
   
   share_library_file: function(user_id, title) {
   		library.request_share_user_id = user_id;
   		library.request_share_title = title;
   		var library_share_message_node = dojo.byId('library_share_message');
   		var message = "This will share your library file titled <b>" + title + "</b>.\n" +
			          "Click OK to continue or click on the 'x' to cancel.";
   		library_share_message_node.innerHTML = message;
		var confirm_share_dialog = dijit.byId('confirm_library_share_dialog');	
		confirm_share_dialog.show();
   },
   
   _download_personal_text: function() {
   	var personal_texts_combo = dijit.byId('library_personal_texts');
   	selected_title = personal_texts_combo.attr('value');
   	function _show_personal_text(data) {
   	  	if (data.success) {
   	  		central_text.set_central_text(data.data);
   	  	}
   	  }
   	if (selected_title) {
   	  var address = "/services/library/download/"+ selected_title;
	  network.pass_reponse_to_function(address, _show_personal_text, 'json');
   	}
   },
   
   select_text: function() {
   	 console.debug('select text');
   	 function _populate_search_page(data) {
   	 	if (data.success) {
   	 		central_text.set_central_html(data.data);
   	 	}
   	 }
   	 var address = "/services/library/search_page/";
   	 
	 network.pass_reponse_to_function(address, _populate_search_page, 'json');
	 
   },	
   
   populate_personal_texts: function(user_id) {
   	  function _populate_personal_texts(data) {
   	  	if (data.success === 0) {
   	  		return;
   	  	}
   	  	var personal_titles = data.data;
   	    var option_items = [];
        for (ix in personal_titles) {
    	  title = personal_titles[ix];
    	  console.debug('add item ' + title);
    	  option_items[ix] = {name: title};
        }
        var options = new dojo.data.ItemFileReadStore(
			{data: {identifier: 'name',
			        items: option_items }
			}
		   );
	
        var personal_texts_combo = dijit.byId('library_personal_texts');
        personal_texts_combo.store = options;
   	  }
   	  
   	  var address = "/services/library/dir/";
	  network.pass_reponse_to_function(address, _populate_personal_texts, 'json');
   }
};


