/**
 * @author alynch
 */

main_menu = {
	
  init: function() {
  	login_.register_authentication_change_callback(main_menu.login_changed);
  },
  
  login_changed: function() {
  	var nickname = read_cookie('nickname');
  	main_menu._set_nickname(nickname);
  	if (login_.authenticated) {
  	  main_menu.show_logout_item();
  	}
  	else {
  	  main_menu.show_login_item();
  	}
  }, 
	
  _set_nickname: function (nickname) {
  	var nickname_node = dojo.byId('menu_nickname');
  	console.debug('set node nickname data to ' + nickname);
  	nickname_node.firstChild.data = nickname;
  },
  
  show_logout_item: function() {
    var menu_login_node = dojo.byId('menu_login');
    menu_login_node.innerHTML = 'Logout';
  },
  
  show_login_item: function() {
    var menu_login_node = dojo.byId('menu_login');
    menu_login_node.innerHTML = 'Login/Register';
  },
  
  item_selected: function (item) {
  	var menu_ids = ['read', 'upload', 'revise', 'database', 'forum',
  			    'about', 'login', 'help', 'my_reader'];
  	var menu_id = '';
  	var menu_node = null;
  	for (ix in menu_ids) {
  		menu_id = menu_ids[ix];
  		menu_node = dojo.byId('menu_' + menu_id);	
  		if (menu_id == item) {
  			menu_node.className = 'google_menu_text google_menu_chosen';
  		} 
  		else {
  			menu_node.className = 'google_menu_text';
  		}
  	}
  }
 
};
