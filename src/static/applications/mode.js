/**
 * @author alynch
 */

mode = {
	
	_in_full_screen: false,
	
   initial_state: {
       back: function() {
       },
       
       forward: function() {
       }	
   },
   
   state_in_about: {
   	   
   	   changeUrl: 'about',
   	
       back: function() {
          mode.goto_about();	
       },	
       forward: function() {
          mode.goto_about();	
       }
   },
   
   state_in_login: {
   	   
   	   changeUrl: 'login',
   	
       back: function() {
          mode.goto_login();	
       },	
       forward: function() {
          mode.goto_login();	
       }
   },
   
   state_in_signup: {
   	   
   	   changeUrl: 'signup',
   	
       back: function() {
          mode.goto_signup();	
       },	
       forward: function() {
          mode.goto_signup();	
       }
   },
   
   state_in_help: {
   	   
   	   changeUrl: 'help',
   	
       back: function() {
          mode.goto_help();	
       },	
       forward: function() {
          mode.goto_help();	
       }
   },
   
   state_in_myreader: {
   	   
   	   changeUrl: 'myreader',
   	
       back: function() {
          mode.goto_my_reader();	
       },	
       forward: function() {
          mode.goto_my_reader();	
       }
   },
   
   state_in_read: {
   	   
   	   changeUrl: 'read',
   	
       back: function() {
       	var hash = location.hash;
       	if(hash.charAt(0) == "#"){
       		hash = hash.substring(1); 
       	}
       	console.debug('hash is ' + hash);
       	  if (hash != 'read') {
       	  	var memento = hash.substr(5);
       	  	mode.goto_memento(memento);
       	  }
       	  else {
          	mode.goto_read();
       	  }	
       },	
       forward: function() {
          mode.state_in_read.back();	
       }
   },
   
   state_in_upload: {
   	   
   	   changeUrl: 'upload',
   	
       back: function() {
          mode.goto_upload();	
       },	
       forward: function() {
          mode.goto_upload();	
       }
   },
   
   state_in_forum: {
   	   
   	   changeUrl: 'forum',
   	
       back: function() {
          mode.goto_forum();	
       },	
       forward: function() {
          mode.goto_forum();	
       }
   },
   
   state_in_revise: {
   	   
   	   changeUrl: 'revise',
   	
       back: function() {
          mode.goto_revise();	
       },	
       forward: function() {
          mode.goto_revise();	
       }
   },
   
   state_in_database: {
   	
   	   changeUrl: 'database',
   	
       back: function() {
          mode.goto_database(false);	
       },	
       forward: function() {
          mode.goto_database(false);	
       }
   },
   
   switch_large_web: function () {
   	 mode._in_full_screen = ! mode._in_full_screen;
     mode._show_large_web(mode._in_full_screen);
   },
   	
   _show_large_web:function(full_screen) {	
   	var text_browser_container_node = dojo.byId('text_browser_border_container');
   	var large_iframe_holder_node = dojo.byId('large_iframe_holder');
   	var embedded_iframe_holder_node = dojo.byId('embedded_iframe_holder');
   	var full_screen_button = dojo.byId('floating_full_screen_pane');
   	var iframe_node = dojo.byId('central_text_iframe');
   	var floating_word_root_node = dojo.byId('floating_word_root_pane');
   	var floating_word_meaning_node = dojo.byId('floating_word_meaning_pane');
   	if (full_screen) {
   		floating_word_meaning_node.style.display = 'block';
   	    floating_word_root_node.style.display = 'block';
   		text_browser_container_node.dislay = 'none';
   		large_iframe_holder_node.display = 'block';
   		embedded_iframe_holder_node.display = 'none';
   		large_iframe_holder_node.insertBefore(iframe_node, null);
   		full_screen_button.innerHTML = 'Exit Full Screen';
   	}
   	else {
   		floating_word_meaning_node.style.display = 'block';
   	    floating_word_root_node.style.display = 'block';
   		text_browser_container_node.dislay = 'block';
   		large_iframe_holder_node.display = 'none';
   		embedded_iframe_holder_node.display = 'block';
   		embedded_iframe_holder_node.insertBefore(iframe_node, null);
   		full_screen_button.innerHTML = 'Full Screen';
   	}
   },
   
   show_navigate_section: function (section) {
	 if (section == 'navigate_forum') {
		 window.open("http://www.arabicreader.net/smf_forum");
	   	 return;
	 }  	  
	   	 
   	 mode.show_central_text();
   	 var full_screen_button_node = dojo.byId('floating_full_screen_pane');
   	 var floating_word_meaning_node = dojo.byId('floating_word_meaning_pane');
   	 var floating_word_root_node = dojo.byId('floating_word_root_pane');
   	 var navigate_read_text_node = dojo.byId('navigate_read_text_area');
   	 var read_pane_toolbar_node = dojo.byId('read_pane_toolbar');
   	 var maintain_database_node = dojo.byId('maintain_database_panel');
   	 var about_node = dojo.byId('navigate_about');
   	 var login_node = dojo.byId('navigate_login');
   	 var signup_node = dojo.byId('navigate_signup');
   	 var read_node = dojo.byId('navigate_read');
   	 var upload_node = dojo.byId('navigate_upload');
   	 var my_reader_node = dojo.byId('navigate_my_reader');
   	 var revise_node = dojo.byId('navigate_revise');
   	 var revise_test_node = dojo.byId('revise_test');
   	 var revise_organise_node = dojo.byId('revise_organise');
   	 var revise_download_node = dojo.byId('revise_download');
   	 var help_node = dojo.byId('navigate_help');
   	 var forum_node = dojo.byId('forum_placeholder');
   	 navigate_read_text_node.style.display = 'none';
   	 full_screen_button_node.style.display = 'none';
   	 floating_word_meaning_node.style.display = 'none';
   	 floating_word_root_node.style.display = 'none';
   	 read_pane_toolbar_node.style.display = 'none';
   	 dijit.byId('navigate_and_reader_panel').resize();
   	 if (section == 'navigate_about') {
   	   about_node.style.display = 'block';
   	 }
   	 else {
   	   about_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_login') {
   	   login_node.style.display = 'block';
   	 }
   	 else {
   	   login_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_read') {
   	   navigate_read_text_node.style.display = 'block';
   	   read_pane_toolbar_node.style.display = 'block';
   	   read_pane_toolbar_node.style.height = '35px';
   	   dijit.byId('navigate_and_reader_panel').resize();
   	   read_node.style.display = 'block';
   	 }
   	 else {
   	   read_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_signup') {
   	   signup_node.style.display = 'block';
   	 }
   	 else {
   	   signup_node.style.display = 'none';
   	 }
//   	 if (section == 'navigate_web') {
//   	   //full_screen_button_node.style.display = 'block';
//   	   if (mode._in_full_screen) {
//	   	   floating_word_meaning_node.style.display = 'block';
//	   	   floating_word_root_node.style.display = 'block';
//   	   }
//   	   web_node.style.display = 'block';
//   	   central_node_iframe.style.display = 'block';
//   	   navigate_title_widgit.attr('title', 'Web');
//   	 }
//   	 else {
//   	   web_node.style.display = 'none';
//   	 }
   	 if (section == 'navigate_upload') {
   	   upload_node.style.display = 'block';
   	 }
   	 else {
   	   upload_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_database') {
   	   maintain_database_node.style.display = 'block';
   	 }
   	 else {
   	   maintain_database_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_my_reader') {
   	   my_reader_node.style.display = 'block';
   	   my_reader.populate();
   	 }
   	 else {
   	   my_reader_node.style.display = 'none';
   	 }
   	 if (section == 'navigate_revise' || section == 'navigate_download_vocab'
   		 || section == 'navigate_organise_vocab' || section == 'navigate_test_vocab') {
   	   revise_node.style.display = 'block';
       if (section == 'navigate_test_vocab') {
       	   revise_test_node.style.display = 'block';
   	   }
   	   else {
   		   revise_test_node.style.display = 'none';
   	   }
       if (section == 'navigate_download_vocab') {
       	   revise_download_node.style.display = 'block';
   	   }
   	   else {
   		   revise_download_node.style.display = 'none';
   	   }
       if (section == 'navigate_organise_vocab') {
     	     revise_organise_node.style.display = 'block';
  	   }
  	    else {
  	        revise_organise_node.style.display = 'none';
  	   }
   	 }
   	 else {
   	   revise_node.style.display = 'none';
   	 }

   	 if (section == 'navigate_help') {
   	   help_node.style.display = 'block';
   	 }
   	 else {
   	   help_node.style.display = 'none';
   	 }
   },

   goto_about: function(push_stack) {
   	 main_menu.item_selected('about');
   	 mode.show_navigate_section('navigate_about');
   	 if (push_stack) {
			console.debug('push TBABOUT state onto stack');
			dojo.back.addToHistory(mode.state_in_about);
		}
   },
   
   goto_login: function(push_stack) {
     main_menu.item_selected('login');
   	 mode.show_navigate_section('navigate_login');
   	 if (push_stack) {
			console.debug('push TBLOGIN state onto stack');
			dojo.back.addToHistory(mode.state_in_login);
	 }
	 if (login_.authenticated) {
 	   login_.offer_logout();
     }
   },
   
   goto_signup: function(push_stack) {
   	 main_menu.item_selected('login');
   	 mode.show_navigate_section('navigate_signup');
   	 if (push_stack) {
			console.debug('push TBSIGNUP state onto stack');
			dojo.back.addToHistory(mode.state_in_signup);
		}
   },
   
   goto_help: function(push_stack) {
   	 main_menu.item_selected('help');
   	 mode.show_navigate_section('navigate_help');
   	 if (push_stack) {
			console.debug('push TBHELP state onto stack');
			dojo.back.addToHistory(mode.state_in_help);
		}
   },
   
   goto_my_reader: function(push_stack) {
   	 main_menu.item_selected('my_reader');
   	 mode.show_navigate_section('navigate_my_reader');
   	 if (push_stack) {
			console.debug('push TBMYREADER state onto stack');
			dojo.back.addToHistory(mode.state_in_myreader);
		}
   },
   
   goto_read: function(push_stack) {
   	 main_menu.item_selected('read');
	 mode.show_navigate_section('navigate_read');
   	 if (push_stack) {
			console.debug('push TBREAD state onto stack');
			mode.state_in_read.changeUrl = 'read';
			dojo.back.addToHistory(mode.state_in_read);
	 }
   },
   
   goto_upload: function(push_stack) {
   	 main_menu.item_selected('upload');
	 mode.show_navigate_section('navigate_upload');
   	 if (push_stack) {
			console.debug('push TBUPLOAD state onto stack');
			dojo.back.addToHistory(mode.state_in_upload);
		}
   },
   
   goto_forum: function(push_stack) {
   	 main_menu.item_selected('forum');
	 mode.show_navigate_section('navigate_forum');
   	 if (push_stack) {
			console.debug('push TBFORUM state onto stack');
			dojo.back.addToHistory(mode.state_in_forum);
		}
   	//location.href = 'http://www.arabicreader.net/smf_forum';
   },
   
   goto_database: function(push_stack) {
   	 main_menu.item_selected('database');
	 mode.show_navigate_section('navigate_database');
   	 if (push_stack) {
	  console.debug('push TBDATABASE state onto stack');
      dojo.back.addToHistory(mode.state_in_database);
	 }
   },
   
   goto_revise: function(push_stack) {
   	 main_menu.item_selected('revise');
	 mode.show_navigate_section('navigate_revise');
   	 if (push_stack) {
	  console.debug('push TBREVISE state onto stack');
      dojo.back.addToHistory(mode.state_in_revise);
	 }
   	 mode.goto_organise_vocab();
   },
   
   goto_test_vocab: function(push_stack) {
	   	 main_menu.item_selected('revise');
		 mode.show_navigate_section('navigate_test_vocab');
	   	 if (push_stack) {
		  console.debug('push TBREVISE state onto stack');
	      dojo.back.addToHistory(mode.state_in_revise);
		 }
},
   
   goto_download_vocab: function(push_stack) {
	   	 main_menu.item_selected('revise');
		 mode.show_navigate_section('navigate_download_vocab');
	   	 if (push_stack) {
		  console.debug('push TBREVISE state onto stack');
	      dojo.back.addToHistory(mode.state_in_revise);
		 }
   },
   
   goto_organise_vocab: function(push_stack) {
	   	 main_menu.item_selected('revise');
		 mode.show_navigate_section('navigate_organise_vocab');
	   	 if (push_stack) {
		  console.debug('push TBREVISE state onto stack');
	      dojo.back.addToHistory(mode.state_in_revise);
		 }
	   	 organise_vocab.populate();
 },
   
   goto_url: function(url) {
   	mode.goto_read(true);
    central_text.set_central_srclink(url);
  },
  
   goto_library_document: function(user_id, title) {
   	mode.goto_read(true);
    central_text.set_central_librarytext(user_id, title, 1);
  },
   
   add_to_back_history: function(bookmark) {
	   bookmark = encodeURIComponent(bookmark);
	   history_state = {
		   	   
		   	   changeUrl: bookmark,
		   	
		       back: function() {
		          mode.goto_bookmark(bookmark);	
		       },	
		       forward: function() {
		          mode.goto_bookmark(bookmark);	
		       }
	   };
	   dojo.back.addToHistory(history_state);
   },	   
   
   goto_bookmark: function(bookmark) {
	   bookmark = decodeURIComponent(bookmark);
	   console.debug('bookmark is ' + bookmark + bookmark.slice(0,9));
	   if (bookmark == 'database') {
		   dojo.back.setInitialState(mode.goto_database);
		   mode.goto_database();
	   }
	   else if (bookmark == 'read') {
		   dojo.back.setInitialState(mode.goto_read);
		   mode.goto_read();
	   }
	   else if (bookmark == 'revise') {
		   dojo.back.setInitialState(mode.goto_revise);
		   mode.goto_revise();
	   }
	   else if (bookmark.slice(0,9) == 'documents') {
		   dojo.back.setInitialState(mode.goto_read);
		   mode.goto_read();
		   details = bookmark.split('_');
		   user_id = details[1];
		   title = details[2];
		   page_no = details[3];
		   console.debug('load document ' + user_id + ' '  + title +' ' + page_no);
		   central_text.set_central_librarytext(user_id, title, page_no);
	   }
	   else {
		   dojo.back.setInitialState(mode.goto_about);
	       mode.goto_about(true);
	   }
   },
   
   show_central_text: function() {
   	 var new_definition_node = dojo.byId('maintain_database_panel');
	 var text_browser = dojo.byId('navigate_and_reader_panel');
	 new_definition_node.style.display = "none";
	 text_browser.style.display = "block";
   },
   
   show_demo_text: function () {
   	 mode.goto_read(true);
   	 navigate_.use_essay_1();
   }

};