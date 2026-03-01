/**
 * @author alynch
 */

db_navigate = {
	
   current_kalima_id: 0,
   
   init: function() {
   	 var filter_text_node = dojo.byId('db_navigate_filter');
   	 var filter_text_widget = dijit.byId('db_navigate_filter');
   	 dojo.connect(filter_text_node, 'onfocus', new_definition.enter_widget);
   	 dojo.connect(filter_text_widget, "onKeyUp", db_navigate.filter_changed);
   },
   
   filter_changed: function() {
   	 var filter_text_widget = dijit.byId('db_navigate_filter');
   	 var text = filter_text_widget.attr('value');
   	 console.debug('filter changed to ' + text);
   },
	
   delete_word: function() {
   	 var address = "/services/modifyword/deletekalima/" + db_navigate.current_kalima_id;
     network.pass_reponse_to_function(address, db_navigate._word_deleted, 'json');
   },
   
   _word_deleted: function(data) {
        var success = data.success;
        var message = '';
        if (success === 0) {
        	var error = data.data;
            console.debug(error);
            message = error;
        }
        else {
	        var previous_kalima_id = data.data;
	        db_navigate.goto_word_of_kalima_id(previous_kalima_id);
	        message = 'Word set deleted from the database';
        }
        new_definition.show_status(message);
   },
   
   last_word: function() {
   	 var address = "/services/modifyword/getlastkalima";
     network.pass_reponse_to_function(address, db_navigate.goto_last_word, 'json');
   },
   
   goto_last_word: function(data) {
   	 last_word_id = data.data;
   	 console.debug('last id is ' + last_word_id);
   	 if (last_word_id > 0) {
   	 	db_navigate.goto_word_of_kalima_id(last_word_id);
   	 }
   	 else {
   	 	console.debug('no next word');
   	 }
   	 new_definition.show_status('Ready');
   },
   
   goto_next_or_previous: function(next_or_previous, callback) {
	 if (db_navigate.current_kalima_id == 'New') {return;}
	 var filter_widget = dijit.byId('db_navigate_filter');
	 var filter_text = filter_widget.attr('value');
   	 var address = "/services/modifyword/" + next_or_previous + "/" + db_navigate.current_kalima_id;
   	 var arg_details = {
   			address: address,
   			func: callback,
   			handle_as_type: 'json'
   	 };
   	 if (filter_text) {
   		arg_details.query_args = {filter: filter_text};
   	 }
     network.pass_reponse_to_function(arg_details);
	   
   },
   
   next_word: function() {
	 db_navigate.goto_next_or_previous("getnextkalima", db_navigate.goto_next_word);  
   },
   
   goto_next_word: function(data) {
   	 next_word_id = data.data;
   	 console.debug('next id is ' + next_word_id);
   	 if (next_word_id > 0) {
   	 	db_navigate.goto_word_of_kalima_id(next_word_id);
   	 }
   	 else {
   	 	console.debug('no next word');
   	 }
   	 new_definition.show_status('Ready');
   },
   
   previous_word: function() {
	 db_navigate.goto_next_or_previous("getpreviouskalima", db_navigate.goto_previous_word);    
   },
   
   goto_previous_word: function(data) {
   	 previous_word_id = data.data;
   	 console.debug('previous id is ' + previous_word_id);
   	 if (previous_word_id > 0) {
   	 	db_navigate.goto_word_of_kalima_id(previous_word_id);
   	 }
   	 else {
   	 	console.debug('no previous word');
   	 }
   	 new_definition.show_status('Ready');
   },
   
   goto_word: function(word_id) {
   	new_definition.set_state('Update');
   	function _show_word(data) {
   		var combined_root = db_data_form.set_form_data(data);
   		root.get_word_meanings_of_root(combined_root);
   	}
   	var address = "/services/modifyword/getvariationforkalvarid/" + word_id;
      network.pass_reponse_to_function(address, _show_word, 'json');
   },

   goto_word_of_kalima_id: function(word_id) {
   	new_definition.set_state('Update');
   	function _show_word(data) {
   		var combined_root = db_data_form.set_form_data(data);
   		root.get_word_meanings_of_root(combined_root);
   	}
   	var address = "/services/modifyword/getvariation/" + word_id;
      network.pass_reponse_to_function(address, _show_word, 'json');
   },
      
   new_word: function() {
   	  new_definition.set_state('New');
   },
   
   save_word: function() {
   	  new_definition.show_status('Working...');
   	  var query = db_data_form.get_form_query();
   	  console.debug('save query is' + query);
      if (new_definition.state == 'Update') {
	   	  db_navigate.update_word_in_db(query);
      }
      else {
          db_navigate.add_word_to_db(query);	
      }
   },
   
   update_word_in_db: function(query) {
       var address = "/services/modifyword/updatewordset/form";
	   function update_db(data) {
	       return db_navigate.show_update_db_result(data);
	   }
	   network.pass_reponse_to_function(address, update_db, 'json', query);
   },
   
   show_update_db_result: function (data) {
   		var success = data.success;
        var message = '';
        if (success === 0) {
        	var error = data.data;
            console.debug(error);
            message = error;
        }
        else {
        	db_navigate.goto_word_of_kalima_id(db_navigate.current_kalima_id);
	        message = ' Words updated in the database';
  	    }
        new_definition.show_status(message);
   },
   
   add_word_to_db: function(query) {
   	  var address = "/services/modifyword/addwordset/form";
      network.pass_reponse_to_function(address, db_navigate.show_add_to_db_result,
      								 'json', query);
   },
   
   show_add_to_db_result: function (data) {
   		var success = data.success;
        var message = '';
        if (success === 0) {
        	var error = data.data;
            console.debug(error);
            message = error;
        }
        else {
	        var num_added = data.data[0];
	        var new_kalima_id = data.data[1];
	        if (num_added === 0) {
	            message = 'Addition to database failed';
	        }
	        else {
	           db_navigate.goto_word_of_kalima_id(new_kalima_id);
	           message = num_added + ' words added to the database';
	        }
        }
        new_definition.show_status(message);
   }
   
};