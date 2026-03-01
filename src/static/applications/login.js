/**
 * @author alynch
 */
 
login_ = {
	
   authenticated: false,
   username: '',
   nickname: '',
   
   authentication_change_callbacks: [],
	
   init: function() {
   	login_._authentication_changed();
   	login_._populate_cached_credentials();
   	
   	login_.error_dialog = new dijit.Dialog(
   			{
   			 title: "Email Already In Use",
   		     content: "<p>That email address is already in use!</p>" +
   		     		  "<p>A new password for it will be emailed to you now.</p>" +
   		     		  "<button dojoType=dijit.form.Button type='submit'>OK</button>"
   		    });
	dojo.body().appendChild(login_.error_dialog.domNode);
	login_.error_dialog.startup();
   },
   
   _populate_cached_credentials: function() {
   	  var login_name_widget = dijit.byId('login_username');
   	  var username = read_cookie('username');
   	  if (username) {
   	  	login_name_widget.attr('value', username);
   	  }
   },
   
   _save_cached_credentials: function() {
   	  var login_name_widget = dijit.byId('login_username');
   	  var user_name = login_name_widget.attr('value');
   	  console.debug('save username: ' + user_name);
   	  create_cookie('username', user_name, 1000);
   },
   
   _authentication_changed: function() {
     var nickname = read_cookie('nickname');
   	 if (! nickname || nickname.substring(0,5) === 'Guest') {
   	 	login_.authenticated = false;
   	 }
   	 else {
   		login_.authenticated = true;
   	 }
   	 login_.nickname = nickname;
   	 login_.username = read_cookie('username');
   	 login_._notify_authentication_callbacks();
   	 preferences_manager.fetch_preferences();
   },
   
   register_authentication_change_callback: function(func) {
     login_.authentication_change_callbacks.push(func);
   },
   
   _notify_authentication_callbacks: function() {
   	 console.dir(login_.authentication_change_callbacks);
     for (ix in login_.authentication_change_callbacks) {
     	var callback = login_.authentication_change_callbacks[ix];
     	callback();
     }
   },
   
   server_changed_user_id: function() {
   	login_._authentication_changed();
   },
   
   offer_logout: function() {
   	 login_.logout();
   },
   
   logout: function() {
   	 console.debug('logout 1');
   	 login_.authenticated = false;
   	 erase_cookie('nickname');
   	 erase_cookie('user_id');
   	 create_cookie('nickname', 'Guest', 1);
   	 login_._notify_authentication_callbacks();
   	 login_.show_status('You have logged off.');
   },
	
   submit_signup: function() {
   	 login_.show_status('Working...');
   	 var email_widget = dijit.byId('signup_emailaddress');
   	 var nickname_widget = dijit.byId('signup_nickname');
   	 var email = email_widget.attr('value');
   	 var nickname = nickname_widget.attr('value');
   	 
   	 var address = "/services/session/signup/" + encodeURIComponent(email) + 
   	 												"/" + encodeURIComponent(nickname);
   	 function _after_signup(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            if (error == "ERROR_EMAIL_ALREADY_IN_USE") {
            	login_.show_signup_status("That email address is already in use");
            	login_.error_dialog.show();
            	login_.show_status('Sending new password...');
            	login_.send_new_password(email);
            	mode.goto_login();
            }
            else {
            	login_.show_signup_status(error);
            }
        }
        else {
        	login_.show_signup_status('Your password has been emailed to you');
        }
        
     }
     var login_response = network.pass_reponse_to_function(address, _after_signup, 'json');
   },
   
   show_status: function(status_) {
   	 var login_status_node = dojo.byId('login_status');
   	 login_status_node.innerHTML = status_;
   },
   
   show_signup_status: function(status_) {
   	 var signup_status_node = dojo.byId('signup_status');
   	 signup_status_node.innerHTML = status_;
   },
   
   submit_login: function() {
   	 login_.show_status('Working...');
   	 var email_widget = dijit.byId('login_username');
   	 var password_widget = dijit.byId('login_password');
   	 var email = email_widget.attr('value');
   	 var password = password_widget.attr('value');
   	 console.debug('password is ' + password);
   	 var password_hash = hex_md5(password);
   	 // dummy submit to trigger browser autocomplete - unfortunately causes page to reload
   	 var login_form_node = dojo.byId('login_form');
   	 AIM.submit(login_form_node, {});
   	 var address = "/services/session/logon/" + encodeURIComponent(email) + 
   	 															"/" + password_hash;
   	 function _after_login(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            login_.show_status(error);
            login_.authenticated = false;
        }
        else {
        	login_.show_status('You have successfully logged on');
        	login_.authenticated = true;
        	login_._save_cached_credentials();
        }
     }
     var login_response = network.pass_reponse_to_function(address, _after_login, 'json');
   },
   
   forgotten_password: function() {
   	var email_address_widget = dijit.byId('login_username');
   	var forgotten_email_address_widget = dijit.byId('forgotten_email');
   	var entered_email_address = email_address_widget.attr('value');
   	forgotten_email_address_widget.attr('value', entered_email_address);
   	var forgotten_password_pane_widget = dijit.byId('forgotten_password_pane');
	forgotten_password_pane_widget.show();
   },
   
   reset_password: function(dialog_fields) {
	   login_.show_status('Sending new password...');
	   login_.send_new_password(dialog_fields.email_address);
   },
	   
   send_new_password: function(email_address) {
   	 var address = "/services/session/reset_password/" + encodeURIComponent(email_address);
   	 function _after_reset_password(data) {
   	 	var success = data.success;
        var error = data.data;
        if (success === 0) {
            console.debug(error);
            login_.show_status(error);
        }
        else {
        	login_.show_status('You new password has been sent to you by email.');
        }
     }
     var response = network.pass_reponse_to_function(address, _after_reset_password, 'json');
 }

};


