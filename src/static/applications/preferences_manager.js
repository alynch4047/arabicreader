preferences_manager = {
		
  authentication_change_callbacks: [],
  
  _preferences: {},
  
  _preferences_fetched: false,
  
  get_preferences: function() {
	  if (! preferences_manager._preferences_fetched) {
		  preferences_manager.fetch_preferences();
		  preferences_manager._preferences_fetched = true;
	  }
	  return preferences_manager._preferences;
  },
  
  fetch_preferences: function() {
	var address = "/services/session/get_preferences/";
	function _preferences_received(data) {
		var success = data.success;
		var error = data.data;
		if (success === 0) {
			console.debug(error);
		}
		else {
			preferences_manager._preferences = data.data;
			console.debug('preferences is ' + data.data);
			preferences_manager._notify_authentication_callbacks();
		}
	}
	var login_response = network.pass_reponse_to_function(address, _preferences_received, 'json');
  },
  
  update_preferences: function() {
	  function preferences_updated() {
		  var success = data.success;
			var error = data.data;
			if (success === 0) {
				console.debug(error);
			}
			else {
				console.debug('preferences updated');
			}
	  }	  
	  var address = "/services/session/set_preferences/";
	  var arg_details = {
	   			address: address,
	   			func: preferences_updated,
	   			use_post: true,
	   			post_data: {preferences: preferences_manager._preferences},
	   			handle_as_type: 'json'
	   	 };
	     network.pass_reponse_to_function(arg_details);
  },
  
  set_preferences: function(preferences) {
	  for (preference in preferences) {
		  preferences_manager._preferences[preference] = preferences[preference];
		  preferences_manager.update_preferences();
	  }
	  console.dir(preferences_manager._preferences);
	  preferences_manager.update_preferences();
  },
  
  register_authentication_change_callback: function(func) {
	preferences_manager.authentication_change_callbacks.push(func);
  },
  
  _notify_authentication_callbacks: function() {
  	 console.dir(preferences_manager.authentication_change_callbacks);
     for (ix in preferences_manager.authentication_change_callbacks) {
    	var callback = preferences_manager.authentication_change_callbacks[ix];
    	callback();
    }
  }
};