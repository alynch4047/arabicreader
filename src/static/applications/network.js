/**
 * @author alynch
 */

network = {
	
  last_nickname: '',
	
  _user_id_changed: function () {
  	var nickname = read_cookie('nickname');
  	var user_id = read_cookie('user_id');
  	if (nickname !== network.last_nickname) {
	  	console.debug('new nickname is ' + nickname);
	  	network.last_nickname = nickname;
	  	login_.server_changed_user_id();
  	}
  },

  pass_reponse_to_function: function (arg0, func, handle_as_type, query,
		  							  use_post, post_data, timeout_override) {
	  
	var current_user_id = read_cookie('user_id');
  	network.last_nickname = read_cookie('nickname');
  	var hostname = location.hostname;
  	var port = location.port;
  	if (port !== '80') {
    	  hostname += ':' +  port;
    	}
  	
	var address;
	  
	if (arguments.length === 1) {
		var arg_details = arg0;
		address = arg_details.address;
		func = arg_details.func;
		handle_as_type = arg_details.handle_as_type;
		use_post = arg_details.use_post;
		post_data = arg_details.post_data;
		timeout_override = arg_details.timeout_override;
		var query_args = arg_details.query_args;
		for (key in query_args) {
			if (query) {
				query += '&';
			}
			else {
				query = '?';
			}	
			query += key + '=' + encodeURIComponent(query_args[key]);
		}
	}	
	else {
		address = arg0;
	}	

  	if (handle_as_type === 'json') {
  	    address = address + '/json';
  	}
  	
  	address = 'http://' + hostname + address;
  	
  	if (query) {
  		address = address + query;
  	}
  	
  	timeout = timeout_override || 10000;
  	
  	var xhr_func = dojo.xhrGet;
  	if (use_post === true) {
  		xhr_func = dojo.xhrPost;
  		// post_data must come in as an object e.g. {font_size: 12, font_family, 'abc'}
  		// so that it can be converted to kwargs by cherrypy
  		post_data = 'post_data=' + dojo.toJson(post_data);
  	}
  	else {
  		address = network._add_cache_buster(address);
  	}
  	
  	var dfd = xhr_func(
	 { 
        url: address, 
        handleAs: handle_as_type,
        timeout: timeout, 
        postData: post_data,

        load: function(response, ioArgs) {
          if (current_user_id != read_cookie('user_id')) {
          	try {
            	network._user_id_changed();
          	}
          	catch(e) {
          		console.error('user id change mechanism problem');
          	}
          }
          func(response);
          return response;
        },

        error: function(response, ioArgs) { 
          console.dir(response);
          console.dir(ioArgs);
          console.error("HTTP status code: ", ioArgs.xhr.status);
          return response;
        }
    }
	);
  	return dfd;
  },
  
  _add_cache_buster: function(url) {
  	var current_date = new Date();
  	var tag = '_' + current_date.getTime() + 'cb';
  	return url + tag;
  },
  
  get_text_and_links_of_url: function (url, callback_func) {
  	if (url.substr(0, 7) == 'http://') {
  		url = url.substr(7);
  	}
  	// we need to get text via proxy server because security restrictions limit
    // cross site access
  	var address = "/services/proxy/geturl/" + url;
	this.pass_reponse_to_function(address, callback_func);
  }
};
